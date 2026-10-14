# Copy this prompt into a separate setup agent chat

Help me finish the manual CLI setup for the evaluation repository at
`/Users/206768009@bwt3.com/repos/agent-evals` on this Mac. Walk me through one
step at a time. Use current official vendor documentation to verify install,
login, model names, headless flags, search tools, and pricing before giving me
commands. You may run harmless local checks yourself. Pause only when I must
sign in, approve organizational access, choose a paid provider, or enter a
secret. Never ask me to paste a token into chat or print a secret in a log.

The runner's exact arms are in `config/arms.yaml`. Please help me:

1. Install and authenticate OpenCode CLI, Claude Code CLI, and Antigravity CLI
   (`agy`) for the pinned models `github-copilot/gpt-6-luna`,
   `claude-opus-5-5`, and `gemini-3.8-flash-medium`. If a model is unavailable
   to my organization, record that fact; do not substitute one.
2. For OpenCode, verify the exact Copilot model ID and a headless `websearch`
   plus `webfetch` configuration. Show me the allowed search-provider options
   and any separate fee. Ask me which provider my organization permits before
   enabling one, then record the choice and charge in `config/arms.yaml`.
3. Investigate why installed Copilot CLI does not execute `web_search` in the
   runner's headless probe even though `web_fetch` works. Check its documented
   tool names, permissions, version and event stream. Fix the adapter or local
   setup only if the behavior can be verified; do not count a GitHub code
   search as web search.
4. From the evaluation repo, run `python3 -m agent_eval preflight
   --evaluation-id <new-id> --live` after reading its README. If a new manifest
   is needed, initialize it with `financial-hq-ui=$HOME/sportsengine/se-financial-hq-ui`,
   `other-angular=$HOME/sportsengine/se-product-management-ui`,
   `--angular-root $HOME/sportsengine`, and an explicit information cutoff.
   Report each arm's ready/unavailable status and
   what manual action remains. Do not start the 30 evaluation runs.

The code and judge-only evidence packs are already in this repository. Read
`README.md` and `config/arms.yaml` first. Preserve the exact task prompts and
model choices. Keep credentials out of Git and the recorded event streams.
