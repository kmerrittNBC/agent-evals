# Manual setup prompt

Help me finish manual CLI setup for the evaluation repository at
`/Users/206768009@bwt3.com/repos/agent-evals` on this Mac. Walk me through one
step at a time. Use current official vendor documentation to verify install,
login, model names, headless flags, search tools, and pricing before giving
commands. Pause only when I must sign in or approve organizational access.
Never ask me to paste a token into chat or print a secret in a log.

The five pinned arms are in `config/arms.yaml`. Please:

1. Install and authenticate Claude Code CLI and Antigravity CLI (`agy`) for the
   exact pinned models `claude-opus-5-5` and `gemini-3.8-flash-medium`. If a
   model is unavailable to my organization, record that fact; do not substitute
   one.
2. Investigate why installed Copilot CLI does not execute `web_search` in the
   runner's headless probe even though `web_fetch` works. Check documented tool
   names, permissions, version, and event stream. Fix the adapter or local
   setup only when verified; do not count GitHub code search as web search.
3. Read `README.md`, then create a new evaluation manifest with
   `financial-hq-ui=$HOME/sportsengine/se-financial-hq-ui`,
   `other-angular=$HOME/sportsengine/se-product-management-ui`, and
   `--angular-root $HOME/sportsengine`, using an explicit information cutoff.
   Run live preflight, report every arm's ready/unavailable status and remaining
   manual action, and do not start the 25 evaluation runs.

Read `README.md` and `config/arms.yaml` first. Preserve the exact task prompts
and model choices. Keep credentials out of Git and recorded event streams.

## Local setup note

Antigravity CLI sign-in on this Mac required a certificate configuration fix
in `~/.zshrc_local`. Keep the certificate values and file contents out of this
repository.
