# Pi + GPT-6 Luna setup (macOS)

The macOS coding-agent installer currently sets up the Pi CLI, the two web extensions used in the evaluation, and pi-gui through Homebrew. It sets the **shared default for new CLI sessions and GUI threads** to `github-copilot/gpt-6-luna` with `high` thinking. Existing threads keep their own model settings. The evaluation used `medium`, so `high` is a team preference that still needs a separate smoke test.

## Install

1. Install [Homebrew](https://brew.sh/) if needed.
2. From this repository, run:

   ```sh
   bash scripts/macos-coding-agent-setup.sh
   ```

   Re-running the script is safe. It preserves other keys in `~/.pi/agent/settings.json`, including other model settings and packages. Pi and extension versions are pinned for a fresh install; an existing Pi binary is left in place and its version is printed. The script also installs the Chromium build needed by `web_fetch` when npm skips Puppeteer's install script.

3. Open `pi` or pi-gui. Sign in to **GitHub Copilot** with your organization account using the interactive account sign-in. In the Pi CLI, `/login` first shows an authentication-method menu; choose **Sign in with an account**, then GitHub Copilot. No token needs to be pasted into this repository.
4. Verify the account and model in a terminal:

   ```sh
   pi auth check --provider github-copilot --model gpt-6-luna
   pi --list-models gpt-6-luna
   ```

5. Restart pi-gui if it was already open. Start a **new** CLI session or GUI thread and confirm the model is `github-copilot/gpt-6-luna` and thinking is `high`. Test both web tools:

   ```sh
   pi --print --provider github-copilot --model gpt-6-luna --thinking high \
     --tools web_search,web_fetch -- \
     "Use web_search to find the official Python pathlib documentation, then use web_fetch to read it. Report its title and URL."
   ```

If `web_fetch` still fails to launch a browser, record the error before changing the team script.

The default-setting step can also be run alone with `node scripts/set_pi_luna_defaults.mjs`. It respects `PI_CODING_AGENT_DIR` if a custom Pi agent directory is configured. Pi's [settings reference](https://pi.dev/docs/latest/settings) documents the default keys; [pi-gui](https://www.pi-gui.com/) confirms it uses Pi's settings. The [evaluation report](executive-report-2026-10-15.md) describes the tested medium-reasoning setup.
