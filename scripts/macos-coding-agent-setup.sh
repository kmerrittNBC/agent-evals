#!/usr/bin/env bash
set -euo pipefail

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "This installer supports macOS. See docs/pi-luna-setup.md for other platforms." >&2
  exit 1
fi
if ! command -v brew >/dev/null 2>&1; then
  echo "Install Homebrew first: https://brew.sh/" >&2
  exit 1
fi

if ! command -v node >/dev/null 2>&1 || ! node -e 'const [major, minor] = process.versions.node.split(".").map(Number); process.exit(major > 22 || (major === 22 && minor >= 19) ? 0 : 1)' ; then
  brew install node
fi
if ! command -v uvx >/dev/null 2>&1; then
  brew install uv
fi
if ! command -v pi >/dev/null 2>&1; then
  npm install -g --ignore-scripts @earendil-works/pi-coding-agent@1.4.0
fi

pi install npm:pi-web-search@1.7.0
pi install npm:pi-web-fetch@1.1.0

# npm may skip Puppeteer's postinstall script, leaving web_fetch without Chrome.
agent_dir="${PI_CODING_AGENT_DIR:-$HOME/.pi/agent}"
"$agent_dir/npm/node_modules/.bin/puppeteer" browsers install chrome

if [[ ! -d /Applications/pi-gui.app && ! -d "$HOME/Applications/pi-gui.app" ]]; then
  brew tap minghinmatthewlam/tap
  brew trust minghinmatthewlam/tap
  brew install --cask pi-gui
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
node "$script_dir/set_pi_luna_defaults.mjs"

echo
echo "Installed Pi $(pi --version) and extensions:"
pi list
echo
echo "Next: open Pi or pi-gui and sign in to GitHub Copilot with your organization account."
echo "Then create a new thread and verify github-copilot/gpt-6-luna at high."
