"""CLI command construction and conservative event decoding.

Flags are deliberately explicit. A vendor upgrade must pass live preflight before
the runner will use it for an evaluation.
"""
from __future__ import annotations

import json
import os
import shutil
from pathlib import Path


def pi_binary_env() -> dict[str, str]:
    env = os.environ.copy()
    node = shutil.which("node")
    if node:
        try:
            import subprocess
            version = subprocess.check_output([node, "--version"], text=True, timeout=3).strip()
            if int(version.lstrip("v").split(".")[0]) >= 24:
                return env
        except (ValueError, OSError, subprocess.SubprocessError):
            pass
    nvm = Path.home() / ".nvm/versions/node"
    candidates = sorted(nvm.glob("v24.*/bin"), reverse=True)
    if candidates:
        env["PATH"] = str(candidates[0]) + os.pathsep + env.get("PATH", "")
    return env


def environment(arm: dict, workspace: Path) -> dict[str, str]:
    env = pi_binary_env() if arm["harness"] == "pi" else os.environ.copy()
    if arm["harness"] == "opencode":
        # OpenCode's documented env override makes this per-process and keeps
        # permissions independent from a user's global config.
        env["OPENCODE_CONFIG_CONTENT"] = json.dumps({
            "permission": {"*": "deny", "read": "allow", "glob": "allow",
                           "grep": "allow", "websearch": "allow", "webfetch": "allow",
                           "question": "allow"}
        })
    env["AGENT_EVAL_WORKSPACE"] = str(workspace)
    return env


def command(arm: dict, prompt: str, workspace: Path, run_dir: Path,
            session: str | None = None) -> list[str]:
    harness = arm["harness"]
    binary = arm["binary"]
    model = arm["model"]
    effort = arm["reasoning"]
    if harness == "pi":
        cmd = [binary, "--print", "--mode", "json", "--model", model,
               "--thinking", effort, "--tools", "read,grep,find,ls,web_search,web_fetch",
               "--no-context-files", "--no-skills", "--no-approve",
               "--session", str(run_dir / "pi-session.jsonl")]
        return cmd + ["--", prompt]
    if harness == "copilot":
        cmd = [binary, "--prompt", prompt, "--model", model,
               "--reasoning-effort", effort, "--output-format", "json",
               "--allow-all-tools", "--allow-all-urls", "--no-custom-instructions",
               "--no-auto-update", "--usage-output-file", str(run_dir / "copilot-usage.json"),
               "-C", str(workspace), "--session-id", session or run_dir.name,
               "--available-tools=web_search,web_fetch,view,grep,glob,ask_user"]
        return cmd
    if harness == "opencode":
        cmd = [binary, "run", "--format", "json", "--model", model,
               "--variant", effort]
        if session:
            cmd += ["--session", session]
        return cmd + [prompt]
    if harness == "claude":
        cmd = [binary, "-p", prompt, "--model", model, "--effort", effort,
               "--output-format", "stream-json", "--verbose", "--restricted",
               "--tools", "Read,Glob,Grep,WebSearch,WebFetch,AskUserQuestion",
               "--disallowedTools", "mcp__*"]
        if session:
            cmd += ["--resume", session]
        return cmd
    if harness == "antigravity":
        cmd = [binary, "-p", prompt, "--model", model, "--effort", effort,
               "--output-format", "stream-json", "--sandbox"]
        if session:
            cmd += ["--conversation", session]
        return cmd
    raise ValueError(f"Unknown harness: {harness}")


def event_text(harness: str, obj: object) -> str:
    if not isinstance(obj, dict):
        return ""
    if harness == "pi":
        if obj.get("type") == "message_update":
            delta = obj.get("assistantMessageEvent", {})
            return delta.get("delta", "") if isinstance(delta, dict) and delta.get("type") == "text_delta" else ""
        if obj.get("type") == "message_end":
            message = obj.get("message", {})
            return _content_text(message.get("content")) if message.get("role") == "assistant" else ""
    if harness == "copilot":
        data = obj.get("data", {})
        if obj.get("type") in ("assistant.message_delta", "assistant.message"):
            return data.get("deltaContent") or data.get("content") or ""
    if harness == "opencode":
        part = obj.get("part", {})
        if obj.get("type") == "text":
            return part.get("text", "") if isinstance(part, dict) else ""
    if harness == "claude":
        if obj.get("type") == "assistant":
            return _content_text(obj.get("message", {}).get("content"))
        if obj.get("type") == "stream_event":
            delta = obj.get("event", {}).get("delta", {})
            return delta.get("text", "") if isinstance(delta, dict) else ""
        if obj.get("type") == "result":
            return obj.get("result", "") if isinstance(obj.get("result"), str) else ""
    if harness == "antigravity":
        if obj.get("event") == "step_update":
            return obj.get("step_update", {}).get("text_delta", "")
        if obj.get("event") == "result":
            return obj.get("result", {}).get("response", "")
    return ""


def _content_text(content: object) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(str(x.get("text", "")) for x in content if isinstance(x, dict) and x.get("type") == "text")
    return ""


def final_answer(harness: str, events: list[dict]) -> str:
    # Prefer a terminal answer; fall back to the last complete assistant event,
    # then assembled deltas. Never use tool output as an answer.
    completed: list[str] = []
    deltas: list[str] = []
    for entry in events:
        obj = entry.get("data")
        if not isinstance(obj, dict):
            continue
        kind = str(obj.get("type", obj.get("event", "")))
        value = event_text(harness, obj)
        if not value:
            continue
        if kind in ("result", "message_end", "assistant.message", "assistant", "text"):
            completed.append(value)
        else:
            deltas.append(value)
    return (completed[-1] if completed else "".join(deltas)).strip()


def session_id(harness: str, events: list[dict]) -> str | None:
    keys = {"pi": ("sessionId",), "copilot": ("sessionId", "session_id"),
            "opencode": ("sessionID", "sessionId"), "claude": ("session_id",),
            "antigravity": ("conversation_id",)}[harness]
    for entry in events:
        obj = entry.get("data")
        if not isinstance(obj, dict):
            continue
        for container in (obj, obj.get("data", {}), obj.get("result", {})):
            if isinstance(container, dict):
                for key in keys:
                    if isinstance(container.get(key), str) and container[key]:
                        return container[key]
    return None


def tool_names(events: list[dict]) -> list[str]:
    names: list[str] = []
    for entry in events:
        obj = entry.get("data")
        if not isinstance(obj, dict):
            continue
        event_type = str(obj.get("type", obj.get("event", ""))).lower()
        if any(term in event_type for term in ("tool_execution_start", "tool.execution_start", "tool_call", "function", "question")):
            for container in (obj, obj.get("data"), obj.get("part"), obj.get("tool_call"),
                              obj.get("toolCall"), obj.get("step_update")):
                if isinstance(container, dict):
                    for key in ("toolName", "tool_name", "tool", "name"):
                        value = container.get(key)
                        if isinstance(value, str):
                            names.append(value)
        if event_type == "step_update":
            step = obj.get("step_update", {})
            if isinstance(step, dict) and step.get("step_type") == "tool" and step.get("state") == "DONE":
                value = step.get("tool_name")
                if isinstance(value, str):
                    names.append(value)
        # Pi and Claude include tool calls as assistant content blocks.
        message = obj.get("message")
        if isinstance(message, dict) and message.get("role") == "assistant":
            for block in message.get("content", []):
                if isinstance(block, dict) and block.get("type") in ("toolCall", "tool_use"):
                    value = block.get("name")
                    if isinstance(value, str):
                        names.append(value)
    return list(dict.fromkeys(names))


def tool_activity(events: list[dict]) -> dict[str, int]:
    counts = {"search_calls": 0, "fetch_calls": 0, "other_tool_calls": 0}
    for entry in events:
        obj = entry.get("data")
        if not isinstance(obj, dict):
            continue
        kind = str(obj.get("type", obj.get("event", "")))
        name = None
        if kind in ("tool_execution_start", "tool.execution_start", "tool"):
            container = obj.get("data") or obj.get("part") or obj
            if isinstance(container, dict):
                name = container.get("toolName") or container.get("tool") or container.get("name")
        elif kind == "step_update":
            step = obj.get("step_update", {})
            if isinstance(step, dict) and step.get("step_type") == "tool" and step.get("state") == "DONE":
                name = step.get("tool_name")
        if not isinstance(name, str):
            continue
        if "web_search" in name.lower() or "websearch" in name.lower():
            counts["search_calls"] += 1
        elif any(term in name.lower() for term in ("fetch", "browse", "webpage")):
            counts["fetch_calls"] += 1
        else:
            counts["other_tool_calls"] += 1
    return counts


def asked_question(events: list[dict], answer: str) -> bool:
    if any(any(term in name.lower() for term in ("question", "ask_user", "askuser")) for name in tool_names(events)):
        return True
    # Only a question-only final response is treated as a request to continue.
    lines = [line.strip() for line in answer.splitlines() if line.strip()]
    return bool(lines) and len(lines) <= 3 and lines[-1].endswith("?") and not any("." in line for line in lines)


def usage(harness: str, events: list[dict], run_dir: Path) -> dict:
    if harness == "copilot" and (run_dir / "copilot-usage.json").exists():
        try:
            raw = json.loads((run_dir / "copilot-usage.json").read_text())
            return {"classification": "measured", "source": "copilot --usage-output-file", "raw": raw}
        except (OSError, json.JSONDecodeError):
            pass
    for entry in reversed(events):
        obj = entry.get("data")
        if not isinstance(obj, dict):
            continue
        for container in (obj, obj.get("result", {}), obj.get("message", {})):
            if isinstance(container, dict) and isinstance(container.get("usage"), dict):
                return {"classification": "measured", "source": "provider event", "raw": container["usage"]}
    return {"classification": "unavailable", "source": None, "raw": None}
