"""Verify an isolated Codex CLI can use the local Responses fixture.

This probe never contacts Copilot and never reads the user's Codex config.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
MODELS = ("gpt-6-sol", "gpt-6-luna")


def probe(codex: str) -> int:
    with tempfile.TemporaryDirectory(prefix="codex-copilot-fixture-") as directory:
        root = Path(directory)
        record = root / "requests.jsonl"
        fixture = subprocess.Popen(
            [sys.executable, str(HERE / "responses_fixture.py"), "--record", str(record)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        try:
            assert fixture.stdout is not None
            ready = fixture.stdout.readline()
            if not ready:
                raise RuntimeError("fixture did not start")
            base_url = json.loads(ready)["base_url"]
            home = root / "codex-home"
            home.mkdir()
            workspace = root / "workspace"
            workspace.mkdir()
            (home / "config.toml").write_text(
                "model_provider = \"fixture\"\n"
                "check_for_update_on_startup = false\n"
                "[features]\nplugins = false\n"
                "[model_providers.fixture]\n"
                "name = \"Local fixture\"\n"
                f"base_url = \"{base_url}\"\n"
                "env_key = \"FIXTURE_API_KEY\"\n"
                "wire_api = \"responses\"\n"
                "requires_openai_auth = false\n"
                "supports_websockets = false\n",
                encoding="utf-8",
            )
            env = {
                "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
                "HOME": str(root),
                "CODEX_HOME": str(home),
                "FIXTURE_API_KEY": "local-fixture-placeholder",
                "NO_PROXY": "127.0.0.1,localhost",
                "no_proxy": "127.0.0.1,localhost",
            }
            if sys.platform == "darwin":
                env["TMPDIR"] = os.environ.get("TMPDIR", "/tmp")
            for model in MODELS:
                result = subprocess.run(
                    [codex, "exec", "--strict-config", "--ephemeral", "--skip-git-repo-check", "--json", "--sandbox", "read-only", "--model", model, "--cd", str(workspace), "Reply with one sentence."],
                    env=env,
                    capture_output=True,
                    text=True,
                    timeout=60,
                    check=False,
                )
                events = []
                for line in result.stdout.splitlines():
                    try:
                        events.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
                completed = any(event.get("type") in ("turn.completed", "turn/completed") for event in events)
                failed = any(event.get("type") in ("turn.failed", "turn/failed") for event in events)
                print(json.dumps({"model": model, "exit_code": result.returncode, "completed": completed, "failed": failed}))
                if result.returncode != 0 or not completed or failed:
                    print(result.stderr[-1200:], file=sys.stderr)
                    return 1
            observed = [json.loads(line) for line in record.read_text(encoding="utf-8").splitlines()]
            for model in MODELS:
                if not any(item["model"] == model and item["stream"] for item in observed):
                    print(f"missing streamed fixture request for {model}", file=sys.stderr)
                    return 1
            print(json.dumps({"result": "pass", "observed_models": [item["model"] for item in observed]}))
            return 0
        finally:
            fixture.terminate()
            try:
                fixture.wait(timeout=5)
            except subprocess.TimeoutExpired:
                fixture.kill()
                fixture.wait(timeout=5)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex", default="codex", help="Path to the Codex CLI binary")
    args = parser.parse_args()
    raise SystemExit(probe(args.codex))


if __name__ == "__main__":
    main()
