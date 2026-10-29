"""Configure Pi's existing extensions for local-Qwen IG pilots.

Search uses Copilot Luna's provider-native web search. Pi's selected task model
remains the locally served Qwen checkpoint; web_fetch reads pages locally.
"""
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


agent_dir = Path.home() / ".pi" / "agent"
models = json.loads((agent_dir / "models.json").read_text())
model_id = "Qwen3.8-27B-oQ6e-mtp"
if model_id not in [model["id"] for model in models["providers"]["omlx-local"]["models"]]:
    raise SystemExit("Local Qwen 6-bit model is not registered in Pi")

for package in ("npm:pi-web-search@1.7.0", "npm:pi-web-fetch@1.1.0"):
    subprocess.run(["pi", "install", package], check=True)

settings_path = agent_dir / "settings.json"
settings = json.loads(settings_path.read_text())
settings["defaultProvider"] = "omlx-local"
settings["defaultModel"] = model_id
search_path = agent_dir / "web-search.json"
search = {"provider": "github-copilot", "model": "gpt-6-luna"}
if search_path.exists() and json.loads(search_path.read_text()) != search:
    raise SystemExit(f"Existing {search_path} selects another search model; leaving it untouched")
if not search_path.exists():
    search_path.write_text(json.dumps(search, indent=2) + "\n")
    search_path.chmod(0o600)
if json.loads(settings_path.read_text()) != settings:
    backup = settings_path.with_name(settings_path.name + ".before-local-ig-" +
                                     datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    shutil.copy2(settings_path, backup)
    settings_path.write_text(json.dumps(settings, indent=2) + "\n")
print("Pi task model: omlx-local/" + model_id)
print("Pi web_search model: github-copilot/gpt-6-luna")
print("Pi web_fetch: local extension")
