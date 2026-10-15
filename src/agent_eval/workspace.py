"""Disposable task checkouts and local validation.

Writable tasks use detached Git worktrees at the manifest's exact commit.
The source checkout's working tree is never reset, checked out, or edited.
"""
from __future__ import annotations

import contextlib
import json
import os
import shutil
import subprocess
import tarfile
from pathlib import Path
from typing import Iterator

from .core import ROOT, prepare_workspace


@contextlib.contextmanager
def task_workspace(task: dict, repos: dict[str, dict], destination: Path) -> Iterator[tuple[Path, Path]]:
    destination.mkdir()
    if task.get("category", "ig") == "ig":
        snapshot = destination / "snapshot"
        prepare_workspace(repos, task, snapshot)
        yield snapshot, snapshot
        return
    if len(task["repos"]) != 1:
        raise ValueError("Writable tasks require exactly one repository")
    name = task["repos"][0]
    source = Path(repos[name]["path"])
    checkout = destination / name
    subprocess.run(["git", "-C", str(source), "worktree", "add", "--detach",
                    str(checkout), repos[name]["commit"]],
                   check=True, text=True, capture_output=True, timeout=60)
    try:
        for item in task.get("setup_files", []):
            origin = (ROOT / item["source"]).resolve()
            target = (checkout / item["target"]).resolve()
            if not origin.is_relative_to(ROOT) or not target.is_relative_to(checkout):
                raise ValueError("Unsafe setup file path")
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(origin, target)
        yield destination, checkout
    finally:
        subprocess.run(["git", "-C", str(source), "worktree", "remove", "--force",
                        str(checkout)], text=True, capture_output=True, timeout=60, check=True)


def run_check(command: list[str], cwd: Path, timeout: int = 180) -> dict:
    if not command or not all(isinstance(arg, str) and arg for arg in command):
        raise ValueError("Validation command must be a nonempty argument list")
    try:
        result = subprocess.run(command, cwd=cwd, text=True, capture_output=True,
                                timeout=timeout, env=os.environ.copy())
        return {"command": command, "exit_code": result.returncode,
                "stdout": result.stdout[-8000:], "stderr": result.stderr[-8000:],
                "timed_out": False}
    except subprocess.TimeoutExpired as exc:
        return {"command": command, "exit_code": None,
                "stdout": str(exc.stdout or "")[-8000:],
                "stderr": str(exc.stderr or "")[-8000:], "timed_out": True}
    except OSError as exc:
        return {"command": command, "exit_code": None,
                "stdout": "", "stderr": str(exc), "timed_out": False}


def sandbox_command(command: list[str], workspace: Path, run_dir: Path,
                    source_paths: list[Path]) -> list[str]:
    """Give CLIs normal home/network access, but make active project trees read-only."""
    if not shutil.which("bwrap"):
        raise ValueError("Bubblewrap is required for writable task isolation")
    args = ["bwrap", "--ro-bind", "/", "/",
            "--bind", str(Path.home()), str(Path.home()),
            "--ro-bind", str(ROOT.parent), str(ROOT.parent),
            "--tmpfs", str(ROOT / "evidence"),
            "--tmpfs", str(ROOT / "checks"),
            "--tmpfs", str(ROOT / "config"),
            "--tmpfs", str(ROOT / "results"),
            "--bind", "/tmp", "/tmp"]
    for path in source_paths:
        resolved = str(path.resolve())
        if not Path(resolved).is_relative_to(ROOT.parent):
            args += ["--ro-bind", resolved, resolved]
    args += ["--bind", str(workspace), str(workspace),
             "--bind", str(run_dir), str(run_dir),
             "--dev-bind", "/dev", "/dev", "--proc", "/proc",
             "--setenv", "GIT_OPTIONAL_LOCKS", "0", "--"]
    return args + command


def collect_changes(task: dict, checkout: Path, run_dir: Path, base_commit: str) -> dict:
    """Save the candidate patch and any edits to evaluator-provided checks."""
    setup = {item["target"]: item["source"] for item in task.get("setup_files", [])}
    diff_command = ["git", "-C", str(checkout), "diff", "--binary", base_commit,
                    "--", ".", *(f":(exclude){name}" for name in setup)]
    diff = subprocess.run(diff_command,
                          text=True, capture_output=True, check=True, timeout=30).stdout
    (run_dir / "patch.diff").write_text(diff)
    raw = subprocess.run(["git", "-C", str(checkout), "ls-files", "--others",
                          "--exclude-standard", "-z"], capture_output=True,
                         check=True, timeout=30).stdout
    untracked = [name.decode() for name in raw.split(b"\0") if name and name.decode() not in setup]
    archive_path = run_dir / "untracked.tar"
    with tarfile.open(archive_path, "w") as archive:
        for name in untracked:
            path = checkout / name
            if path.is_symlink() or (path.resolve().is_relative_to(checkout.resolve())
                                     and path.is_file()):
                archive.add(path, arcname=name, recursive=False)
    edited_checks = []
    with tarfile.open(run_dir / "prepared-check-edits.tar", "w") as archive:
        for target_name, source_name in setup.items():
            target = checkout / target_name
            if not target.is_file() or target.is_symlink():
                edited_checks.append({"path": target_name, "status": "removed_or_replaced"})
            elif target.read_bytes() != (ROOT / source_name).read_bytes():
                edited_checks.append({"path": target_name, "status": "modified"})
                archive.add(target, arcname=target_name, recursive=False)
    summary = {"tracked_patch_bytes": len(diff.encode()), "untracked_paths": untracked,
               "setup_checks_intact": not edited_checks,
               "prepared_check_edits": edited_checks,
               "final_head": subprocess.run(["git", "-C", str(checkout), "rev-parse", "HEAD"],
                                            text=True, capture_output=True, check=True).stdout.strip()}
    (run_dir / "changes.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


def replay_changes(checkout: Path, run_dir: Path) -> None:
    """Apply the saved candidate work to a fresh checkout with frozen checks."""
    patch_path = run_dir / "patch.diff"
    if patch_path.stat().st_size:
        for args in (["--check", str(patch_path)], [str(patch_path)]):
            result = subprocess.run(["git", "-C", str(checkout), "apply", "--binary", *args],
                                    text=True, capture_output=True, timeout=30)
            if result.returncode:
                raise ValueError(f"Saved patch could not be replayed: {result.stderr.strip()}")
    with tarfile.open(run_dir / "untracked.tar") as archive:
        for member in archive.getmembers():
            name = Path(member.name)
            if not (member.isfile() or member.issym()) or name.is_absolute() or ".." in name.parts:
                raise ValueError(f"Unsafe untracked artifact: {member.name}")
            target = checkout / name
            target.parent.mkdir(parents=True, exist_ok=True)
            if (not target.parent.resolve().is_relative_to(checkout.resolve()) or
                    target.exists() or target.is_symlink()):
                raise ValueError(f"Untracked artifact conflicts with replay checkout: {member.name}")
            if member.issym():
                link = Path(member.linkname)
                if link.is_absolute() or not (target.parent / link).resolve().is_relative_to(checkout.resolve()):
                    raise ValueError(f"Unsafe untracked symlink: {member.name}")
                target.symlink_to(member.linkname)
                continue
            stream = archive.extractfile(member)
            if stream is None:
                raise ValueError(f"Untracked artifact has no contents: {member.name}")
            with target.open("wb") as output:
                shutil.copyfileobj(stream, output)
            target.chmod(member.mode & 0o777)
