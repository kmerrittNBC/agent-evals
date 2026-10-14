from __future__ import annotations

import json
import tempfile
from pathlib import Path

from . import adapters
from .core import (RESULTS, ROOT, atomic_json, capture, config_hashes,
                   discover_angular_root, load_manifest, manifest_path, pack_status, read_config,
                   static_arm_check, utc_now, validate_cutoff, validate_repos)


PROBE = ("Use the tool named web_search to search for the official Python "
         "documentation page for pathlib Path. Then use the tool named web_fetch "
         "to fetch that result. Report the page title and URL. Both tool calls "
         "are required for this capability check.")


def _judge_probe(directory: Path, timeout: int) -> dict:
    schema = directory / "probe-schema.json"
    schema.write_text(json.dumps({"type": "object", "additionalProperties": False,
                                  "required": ["ok"], "properties": {"ok": {"type": "boolean"}}}))
    output = directory / "probe-output.json"
    cmd = ["codex", "exec", "--model", "gpt-6-sol", "--ephemeral",
           "--sandbox", "read-only", "--skip-git-repo-check", "--ignore-user-config",
           "--output-schema", str(schema), "--output-last-message", str(output),
           "Reply with JSON containing ok=true."]
    try:
        import os
        result = capture(cmd, directory, os.environ.copy(), timeout, directory / "judge-probe-events.jsonl")
        payload = json.loads(output.read_text()) if output.exists() else None
        return {"status": "ready" if result["exit_code"] == 0 and payload == {"ok": True} else "failed",
                "reason": None if payload == {"ok": True} else "Codex did not return schema-conforming JSON",
                "version": _version("codex")}
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return {"status": "failed", "reason": str(exc), "version": _version("codex")}


def _version(binary: str) -> str | None:
    import subprocess
    try:
        return subprocess.check_output([binary, "--version"], text=True, timeout=10).strip()
    except (OSError, subprocess.SubprocessError):
        return None


def live_arm_probe(arm: dict, timeout: int) -> dict:
    with tempfile.TemporaryDirectory(prefix="agent-eval-probe-") as temporary:
        directory = Path(temporary)
        run_dir = directory / "run"
        run_dir.mkdir()
        command = adapters.command(arm, PROBE, directory, run_dir)
        if arm["harness"] == "copilot":
            import uuid
            command[command.index("--session-id") + 1] = str(uuid.uuid4())
        env = adapters.environment(arm, directory)
        try:
            result = capture(command, directory, env, timeout, directory / "events.jsonl")
        except OSError as exc:
            return {"status": "unavailable", "reason": str(exc)}
        answer = adapters.final_answer(arm["harness"], result["events"])
        names = (adapters.completed_claude_tool_names(result["events"])
                 if arm["harness"] == "claude" else adapters.tool_names(result["events"]))
        search = any(any(word in name.lower() for word in ("web_search", "websearch", "search_web")) for name in names)
        fetch = any(any(word in name.lower() for word in ("fetch", "webpage", "browse", "open_url", "read_url_content")) for name in names)
        if result["exit_code"] or result["timed_out"] or not answer:
            return {"status": "unavailable", "reason": "Live probe failed or produced no answer",
                    "probe_exit_code": result["exit_code"], "probe_tool_names": names}
        if not (search and fetch):
            return {"status": "unavailable", "reason": "Search and page fetch were not both observed in headless events",
                    "probe_tool_names": names}
        usage = adapters.usage(arm["harness"], result["events"], run_dir)
        return {"status": "ready", "reason": None, "probe_tool_names": names,
                "usage_fields": sorted(usage["raw"].keys()) if isinstance(usage["raw"], dict) else [],
                "usage_classification": usage["classification"]}


def preflight(evaluation_id: str, cutoff: str | None, repo_args: list[str],
              angular_root: str | None, live: bool) -> dict:
    def same_pin(left: dict, right: dict) -> bool:
        return left["path"] == right["path"] and left["commit"] == right["commit"]

    path = manifest_path(evaluation_id)
    if path.exists():
        manifest = load_manifest(evaluation_id)
        if any((RESULTS / evaluation_id / "runs").rglob("metrics.json")):
            raise ValueError("Cannot modify preflight after runs begin")
        if cutoff and validate_cutoff(cutoff) != manifest["cutoff"]:
            raise ValueError("Cutoff differs from existing manifest")
        if repo_args:
            repos = validate_repos(repo_args)
            for name, info in repos.items():
                if name in manifest["repos"] and not same_pin(manifest["repos"][name], info):
                    raise ValueError("Repository pin differs from existing manifest")
            manifest["repos"].update(repos)
        if angular_root:
            repos, group = discover_angular_root(angular_root)
            if manifest.get("angular_root") and manifest["angular_root"] != group:
                raise ValueError("Angular root selection differs from existing manifest")
            for name, info in repos.items():
                if name in manifest["repos"] and not same_pin(manifest["repos"][name], info):
                    raise ValueError("Angular repository pin differs from existing manifest")
            manifest["repos"].update(repos)
            manifest["angular_root"] = group
    else:
        if not cutoff:
            raise ValueError("A new evaluation requires --cutoff")
        repos = validate_repos(repo_args)
        group = None
        if angular_root:
            discovered, group = discover_angular_root(angular_root)
            repos.update(discovered)
        manifest = {"evaluation_id": evaluation_id, "created_at": utc_now(),
                    "cutoff": validate_cutoff(cutoff), "config_hashes": config_hashes(),
                    "repos": repos, "angular_root": group, "preflight": {},
                    "judge_preflight": {"status": "needs_live_probe"}}
    arms = read_config("arms")["arms"]
    tasks = read_config("tasks")["tasks"]
    for arm in arms:
        state = static_arm_check(arm)
        if live and state["status"] == "needs_live_probe":
            state.update(live_arm_probe(arm, read_config("run-policy")["probe_timeout_seconds"]))
        manifest["preflight"][arm["id"]] = state
    manifest["evidence"] = {task["id"]: {"status": pack_status(task["id"], manifest)[1],
                                        "sha256": None} for task in tasks}
    if live:
        from .core import sha256, pack_path
        for task in tasks:
            if pack_status(task["id"], manifest)[0]:
                manifest["evidence"][task["id"]]["sha256"] = sha256(pack_path(task["id"]))
        with tempfile.TemporaryDirectory(prefix="agent-eval-judge-probe-") as temporary:
            manifest["judge_preflight"] = _judge_probe(Path(temporary), read_config("run-policy")["judge_timeout_seconds"])
    atomic_json(path, manifest)
    return manifest
