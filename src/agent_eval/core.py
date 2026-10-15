from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import queue
import random
import shutil
import subprocess
import tarfile
import tempfile
import threading
import time
from pathlib import Path
from typing import Any

from . import adapters

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results"


def read_config(name: str) -> dict:
    return json.loads((ROOT / "config" / f"{name}.yaml").read_text())


TASK_CONFIG = {"ig": "tasks", "du": "defined-updates", "ar": "architecture"}


def read_tasks(column: str = "ig") -> list[dict]:
    return read_config(TASK_CONFIG[column])["tasks"]


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")
    temp.replace(path)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def config_hashes(column: str = "ig") -> dict[str, str]:
    names = ("arms", TASK_CONFIG[column], "run-policy", "rubric")
    hashes = {name: sha256(ROOT / "config" / f"{name}.yaml") for name in names}
    for task in read_tasks(column):
        for item in task.get("setup_files", []):
            hashes[f"setup:{item['source']}"] = sha256(ROOT / item["source"])
    return hashes


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def validate_cutoff(value: str) -> str:
    parsed = dt.datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError("--cutoff must include a timezone offset")
    return parsed.isoformat()


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(repo), *args], text=True,
                            capture_output=True, timeout=30, check=True)
    return result.stdout.strip()


def validate_repos(repo_args: list[str], column: str = "ig") -> dict[str, dict]:
    tasks = read_tasks(column)
    required = {name for task in tasks for name in task["repos"]}
    repos: dict[str, dict] = {}
    for item in repo_args:
        if "=" not in item:
            raise ValueError("--repo requires name=/absolute/path")
        name, value = item.split("=", 1)
        if name not in required or not Path(value).is_absolute():
            raise ValueError(f"Invalid repository assignment: {item}")
        path = Path(value).resolve()
        if not path.is_dir():
            raise ValueError(f"Repository not found: {path}")
        pins = {task["starting_commit"] for task in tasks
                if name in task["repos"] and task.get("starting_commit")}
        if len(pins) > 1:
            raise ValueError(f"Conflicting frozen commits for {name}")
        source_head = git(path, "rev-parse", "HEAD")
        commit = next(iter(pins)) if pins else source_head
        git(path, "cat-file", "-e", f"{commit}^{{commit}}")
        if not commit or len(commit) != 40:
            raise ValueError(f"Could not pin commit for {path}")
        repos[name] = {"path": str(path), "commit": commit,
                       "working_tree_dirty": bool(git(path, "status", "--porcelain"))}
        if pins:
            repos[name]["source_head"] = source_head
    return repos


def task_repo_names(task: dict, manifest: dict) -> list[str]:
    return task["repos"]


def pack_path(task_id: str) -> Path:
    return ROOT / "evidence" / task_id / "pack.json"


def pack_status(task_id: str, manifest: dict | None = None) -> tuple[bool, str]:
    path = pack_path(task_id)
    if not path.exists():
        return False, "judge evidence pack missing"
    try:
        pack = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return False, "judge evidence pack is invalid JSON"
    if not isinstance(pack, dict):
        return False, "judge evidence pack must be an object"
    fields = ("reference_answer", "sources", "repo_facts", "ambiguities",
              "grading_guidance", "decision_changing_errors")
    if any(field not in pack for field in fields):
        return False, "judge evidence pack is incomplete"
    if "REPLACE" in json.dumps(pack) or not pack["reference_answer"] or not pack["sources"]:
        return False, "judge evidence pack contains placeholders or no sources"
    if not isinstance(pack["sources"], list) or any(
           not isinstance(source, dict) or
           not all(source.get(key) for key in ("title", "url", "retrieved_at", "snapshot_or_excerpt"))
           for source in pack["sources"]):
        return False, "judge evidence pack has an incomplete source"
    guidance = pack["grading_guidance"]
    if not isinstance(guidance, dict) or any(not isinstance(guidance.get(key), list) or
                                             not all(isinstance(item, str) and item for item in guidance[key])
                                             for key in ("must_check", "acceptable_alternatives", "do_not_penalize")):
        return False, "judge evidence pack has incomplete grading guidance"
    if manifest is not None:
        column = manifest.get("column", "ig")
        task = next(task for task in read_tasks(column) if task["id"] == task_id)
        selected = task_repo_names(task, manifest)
        if task["repos"] and not selected:
            return False, "task has no pinned repositories"
        facts = {item["repo"]: item["commit"] for item in pack["repo_facts"]}
        for name in selected:
            info = manifest["repos"].get(name)
            if info is None:
                return False, f"missing pinned repo {name}"
            if facts.get(name, facts.get(Path(info["path"]).name)) != info["commit"]:
                return False, f"judge evidence pack repo pin differs for {name}"
    return True, "ready"


def manifest_path(evaluation_id: str) -> Path:
    if not evaluation_id or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for c in evaluation_id):
        raise ValueError("Evaluation ID must contain only letters, digits, hyphens, underscores")
    return RESULTS / evaluation_id / "manifest.json"


def load_manifest(evaluation_id: str) -> dict:
    path = manifest_path(evaluation_id)
    if not path.exists():
        raise ValueError(f"No manifest for {evaluation_id}; run preflight first")
    value = json.loads(path.read_text())
    if value["config_hashes"] != config_hashes(value.get("column", "ig")):
        raise ValueError("Config changed since preflight; use a new evaluation ID")
    return value


def _version(binary: str, env: dict[str, str] | None = None) -> str | None:
    if not shutil.which(binary, path=(env or os.environ).get("PATH")):
        return None
    try:
        proc = subprocess.run([binary, "--version"], text=True, capture_output=True,
                              timeout=10, env=env)
        return (proc.stdout or proc.stderr).strip().splitlines()[0][:200]
    except (OSError, subprocess.SubprocessError, IndexError):
        return None


def static_arm_check(arm: dict) -> dict:
    env = adapters.environment(arm, ROOT)
    binary = arm["binary"]
    version = _version(binary, env)
    if version is None:
        return {"status": "unavailable", "reason": f"{binary} not found in PATH", "version": None}
    details: dict[str, Any] = {"status": "needs_live_probe", "reason": None, "version": version,
                               "model": arm["model"], "reasoning": arm["reasoning"],
                               "search_provider": arm.get("search_provider"), "usage_fields": "unverified"}
    if arm["harness"] == "pi":
        try:
            output = subprocess.run([binary, "--list-models", arm["model"].split("/")[-1]],
                                    env=env, text=True, capture_output=True, timeout=15)
            if arm["model"].split("/")[-1] not in output.stdout:
                details.update(status="unavailable", reason="Pinned Pi model not listed")
            extensions = subprocess.run([binary, "list"], env=env, text=True,
                                        capture_output=True, timeout=15)
            details["extensions"] = extensions.stdout.strip().splitlines() if extensions.returncode == 0 else []
            if not all(package in extensions.stdout for package in ("pi-web-search", "pi-web-fetch")):
                details.update(status="unavailable", reason="Pi web search/fetch extensions are missing")
        except (OSError, subprocess.SubprocessError):
            details.update(status="unavailable", reason="Could not list Pi models")
    if arm["harness"] == "opencode" and arm.get("search_provider") != "tinyfish":
        # Only the keyless vendor-hosted provider is permitted: it needs no
        # account, key, or billing (ADR 0002). A keyed provider would reintroduce
        # the organizational dependency the OpenCode arm must not have.
        details.update(status="unavailable",
                       reason="OpenCode arm must pin the keyless tinyfish search provider")
    return details


def prepare_workspace(repos: dict[str, dict], task: dict, destination: Path) -> dict[str, str]:
    destination.mkdir(parents=True, exist_ok=False)
    commits: dict[str, str] = {}
    for name in task["repos"]:
        info = repos[name]
        source = Path(info["path"])
        target = destination / name
        target.mkdir(parents=True)
        proc = subprocess.Popen(["git", "-C", str(source), "archive", "--format=tar", info["commit"]],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        assert proc.stdout is not None
        links: list[tuple[Path, str]] = []
        with tarfile.open(fileobj=proc.stdout, mode="r|") as tar:
            for member in tar:
                member_path = (target / member.name).resolve()
                if not member_path.is_relative_to(target.resolve()):
                    proc.kill()
                    raise ValueError("Unsafe path in git archive")
                if member.issym():
                    if Path(member.linkname).is_absolute() or not (member_path.parent / member.linkname).resolve().is_relative_to(target.resolve()):
                        proc.kill()
                        raise ValueError("Unsafe symlink in git archive")
                    links.append((member_path, member.linkname))
                    continue
                if member.islnk():
                    proc.kill()
                    raise ValueError("Unsupported hard link in git archive")
                tar.extract(member, target, filter="data")
        stderr = proc.stderr.read().decode(errors="replace") if proc.stderr else ""
        if proc.wait() != 0:
            raise RuntimeError(f"git archive failed: {stderr[:500]}")
        proc.stdout.close()
        if proc.stderr:
            proc.stderr.close()
        for link_path, link_target in links:
            link_path.symlink_to(link_target)
        commits[name] = info["commit"]
    for path in destination.rglob("*"):
        if path.is_file():
            path.chmod(0o444)
        elif path.is_dir():
            path.chmod(0o555)
    destination.chmod(0o555)
    return commits


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        digest.update(str(path.relative_to(root)).encode())
        if path.is_file():
            digest.update(path.read_bytes())
    return digest.hexdigest()


def capture(command: list[str], cwd: Path, env: dict[str, str], timeout: int,
            events_path: Path) -> dict:
    """Capture stdout/stderr as received with monotonic offsets and no shell."""
    started_at = utc_now()
    start = time.monotonic()
    events: list[dict] = []
    q: queue.Queue[tuple[str, str | None]] = queue.Queue()
    proc = subprocess.Popen(command, cwd=cwd, env=env, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, bufsize=1)

    def pump(stream: Any, channel: str) -> None:
        for line in stream:
            q.put((channel, line.rstrip("\n")))
        q.put((channel, None))

    assert proc.stdout and proc.stderr
    for channel, stream in (("stdout", proc.stdout), ("stderr", proc.stderr)):
        threading.Thread(target=pump, args=(stream, channel), daemon=True).start()
    ended = 0
    timed_out = False
    events_path.parent.mkdir(parents=True, exist_ok=True)
    with events_path.open("w") as output:
        while ended < 2:
            remaining = timeout - (time.monotonic() - start)
            if remaining <= 0 and proc.poll() is None:
                proc.kill()
                timed_out = True
            try:
                channel, line = q.get(timeout=0.2)
            except queue.Empty:
                continue
            if line is None:
                ended += 1
                continue
            try:
                data: Any = json.loads(line)
            except json.JSONDecodeError:
                data = {"raw_text": line}
            entry = {"index": len(events), "elapsed_seconds": round(time.monotonic() - start, 6),
                     "channel": channel, "data": data}
            events.append(entry)
            output.write(json.dumps(entry, ensure_ascii=False) + "\n")
            output.flush()
    exit_code = proc.wait()
    return {"events": events, "exit_code": exit_code, "timed_out": timed_out,
            "elapsed_seconds": round(time.monotonic() - start, 6), "started_at": started_at}


def run_one(arm: dict, task: dict, manifest: dict, evaluation_id: str,
            timeout: int | None = None) -> dict:
    run_dir = RESULTS / evaluation_id / "runs" / task["id"] / arm["id"]
    if run_dir.exists():
        raise ValueError(f"Run already exists: {run_dir}; use a new evaluation ID")
    run_dir.mkdir(parents=True)
    status = manifest["preflight"][arm["id"]]["status"]
    if status == "unavailable":
        metrics = {"task_id": task["id"], "arm_id": arm["id"], "status": "unavailable",
                   "reason": manifest["preflight"][arm["id"]]["reason"],
                   "started_at": utc_now(), "elapsed_seconds": 0, "answer": "",
                   "usage": {"classification": "unavailable", "source": None, "raw": None},
                   "first_visible_seconds": None, "first_substantive_seconds": None}
        (run_dir / "events.jsonl").write_text("")
        (run_dir / "answer.md").write_text("")
        atomic_json(run_dir / "metrics.json", metrics)
        return metrics
    if status != "ready":
        raise ValueError(f"Arm {arm['id']} has not passed live preflight")
    from .workspace import task_workspace
    with tempfile.TemporaryDirectory(prefix="agent-eval-") as temporary:
        with task_workspace(task, manifest["repos"], Path(temporary) / "workspace") as (workspace, checkout):
            return _run_in_workspace(arm, task, manifest, run_dir, workspace, checkout, timeout)


def _run_in_workspace(arm: dict, task: dict, manifest: dict, run_dir: Path,
                      workspace: Path, checkout: Path, timeout: int | None) -> dict:
    writable = task.get("category", "ig") != "ig"
    before = None if writable else tree_digest(workspace)
    env = adapters.environment(arm, workspace, writable=writable)
    session = None
    all_events: list[dict] = []
    phase_results: list[dict] = []
    asked = False
    answer = ""
    policy = read_config("run-policy")
    first_prompt = task["prompt"]
    if writable:
        first_prompt += (f"\n\nWork only in the disposable Git worktree at ./{task['repos'][0]}. "
                         "The original source checkout is outside this workspace. "
                         "Read the repository's AGENTS.md if present. This prompt is the assigned "
                         "task record; no external issue lookup is required. "
                         "Run relevant local checks and report what you changed or planned.")
        if task.get("setup_files"):
            first_prompt += (" Evaluator-provided checks are fixed for grading; "
                             "add your own tests in separate files. The evaluator validates "
                             "your changes with fresh copies of its checks.")
    (run_dir / "effective-prompt.txt").write_text(first_prompt + "\n")
    prompts = [first_prompt, policy["continuation_response"]]
    for phase, prompt in enumerate(prompts):
        if phase and not asked:
            break
        event_path = run_dir / f"phase-{phase}.jsonl"
        cmd = adapters.command(arm, prompt, workspace, run_dir, session, writable=writable)
        if writable:
            from .workspace import sandbox_command
            cmd = sandbox_command(cmd, workspace, run_dir,
                                  [Path(info["path"]) for info in manifest["repos"].values()])
        if arm["harness"] == "copilot" and phase == 0:
            import uuid
            cmd[cmd.index("--session-id") + 1] = str(uuid.uuid4())
        result = capture(cmd, workspace, env,
                         timeout or task.get("timeout_seconds", policy["timeout_seconds"]),
                         event_path)
        phase_results.append({key: value for key, value in result.items() if key != "events"})
        offset = sum(item["elapsed_seconds"] for item in phase_results[:-1])
        for entry in result["events"]:
            entry["index"] = len(all_events)
            entry["elapsed_seconds"] += offset
            entry["phase"] = phase
            all_events.append(entry)
        answer = adapters.final_answer(arm["harness"], result["events"])
        if phase == 0:
            asked = adapters.asked_question(result["events"], answer)
            session = adapters.session_id(arm["harness"], result["events"])
            if arm["harness"] == "copilot":
                session = cmd[cmd.index("--session-id") + 1]
            if arm["harness"] == "pi":
                session = str(run_dir / "pi-session.jsonl")
        if result["exit_code"] != 0 or result["timed_out"]:
            break
        if phase == 0 and asked and not session:
            break
    with (run_dir / "events.jsonl").open("w") as f:
        for entry in all_events:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    after = None if writable else tree_digest(workspace)
    if not writable and before != after:
        status = "failed"
        reason = "Repository snapshot was modified"
    elif phase_results[-1]["timed_out"]:
        status, reason = "timeout", "Harness exceeded timeout"
    elif phase_results[-1]["exit_code"] != 0:
        status, reason = "failed", f"Harness exited {phase_results[-1]['exit_code']}"
    elif asked and not session:
        status, reason = "failed", "Clarification asked but session continuation was unavailable"
    elif not answer:
        status, reason = "failed", "No final answer parsed from events"
    else:
        status, reason = "completed", None
    changes = None
    validation: list[dict] = []
    if writable:
        from .workspace import (collect_changes, replay_changes, run_check,
                                sandbox_command, task_workspace)
        changes = collect_changes(task, checkout, run_dir,
                                  manifest["repos"][task["repos"][0]]["commit"])
        commands = ([task["green_command"], *task.get("regression_commands", [])]
                    if task.get("category") == "defined-update"
                    else task.get("validation_commands", []))
        try:
            with task_workspace(task, manifest["repos"], workspace.parent / "validation") as (validation_workspace, validation_checkout):
                replay_changes(validation_checkout, run_dir)
                changes["validation_checks_intact"] = all(
                    (validation_checkout / item["target"]).is_file() and
                    (validation_checkout / item["target"]).read_bytes() ==
                    (ROOT / item["source"]).read_bytes()
                    for item in task.get("setup_files", [])
                )
                if not changes["validation_checks_intact"]:
                    raise ValueError("Frozen check changed in validation checkout")
                validation = [run_check(sandbox_command(command, validation_workspace, run_dir,
                                                        [Path(info["path"]) for info in manifest["repos"].values()]),
                                        validation_checkout) for command in commands]
        except (OSError, ValueError, subprocess.SubprocessError) as exc:
            status, reason = "failed", f"Validation replay failed: {exc}"
        atomic_json(run_dir / "changes.json", changes)
    first_visible = next((entry["elapsed_seconds"] for entry in all_events
                          if entry["channel"] == "stdout" and
                          adapters.event_text(arm["harness"], entry["data"])), None)
    usage = adapters.usage(arm["harness"], all_events, run_dir)
    (run_dir / "answer.md").write_text(answer + ("\n" if answer else ""))
    metrics = {"task_id": task["id"], "arm_id": arm["id"], "status": status,
               "reason": reason, "started_at": phase_results[0]["started_at"],
               "elapsed_seconds": sum(x["elapsed_seconds"] for x in phase_results),
               "answer": answer, "usage": usage, "asked_clarification": asked,
               "continuations": len(phase_results) - 1, "first_visible_seconds": first_visible,
               "first_substantive_seconds": None, "snapshot_digest_before": before,
               "snapshot_digest_after": after, "phases": phase_results,
               "tool_activity": adapters.tool_activity(all_events)}
    if writable:
        metrics["changes"] = changes
        metrics["validation"] = validation
    atomic_json(run_dir / "metrics.json", metrics)
    return metrics


def randomized_slots(tasks: list[dict], arms: list[dict], seed: int) -> list[tuple[dict, dict]]:
    rng = random.Random(seed)
    result: list[tuple[dict, dict]] = []
    for task in tasks:
        order = list(arms)
        rng.shuffle(order)
        result.extend((task, arm) for arm in order)
    return result
