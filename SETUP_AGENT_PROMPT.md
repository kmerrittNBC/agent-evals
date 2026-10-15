# Manual setup prompt

Help me finish manual CLI setup for the evaluation repository at
`/Users/206768009@bwt3.com/repos/agent-evals` on this Mac. Walk me through one
step at a time. Use current official vendor documentation to verify install,
login, model names, headless flags, search tools, and pricing before giving
commands. Pause only when I must sign in or approve organizational access.
Never ask me to paste a token into chat or print a secret in a log.

The four pinned arms are in `config/arms.yaml`. Please:

1. Install and authenticate Claude Code CLI for the exact pinned model
   `claude-opus-5-5`. If a
   model is unavailable to my organization, record that fact; do not substitute
   one.
2. Install OpenCode CLI (v2) and authenticate it for the pinned
   `github-copilot` provider so the exact model `github-copilot/gpt-6-luna`
   with the `medium` variant resolves. Verify against current OpenCode v2
   documentation that `opencode run --standalone --format json --model
   github-copilot/gpt-6-luna#medium` is the correct headless form. Do not sign
   up for any search provider or API key: the arm pins OpenCode's keyless
   `tinyfish` websearch provider, which needs no account or billing. Confirm
   from the documentation that no key is required before proceeding.
3. Read `README.md`, then create a new evaluation manifest with
   `financial-hq-ui=$HOME/sportsengine/se-financial-hq-ui`,
   `people-and-orgs-ui-library=$HOME/sportsengine/people-and-orgs-ui-library`,
   using an explicit information cutoff.
   Run live preflight, report every arm's ready/unavailable status and remaining
   manual action, and do not start the 20 evaluation runs.

Read `README.md` and `config/arms.yaml` first. Preserve the exact task prompts
and model choices. Keep credentials out of Git and recorded event streams.
