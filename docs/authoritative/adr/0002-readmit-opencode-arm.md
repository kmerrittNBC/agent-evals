---
status: accepted
supersedes: 0001-drop-opencode-arm
---

# Readmit the OpenCode evaluation arm

ADR 0001 dropped the OpenCode arm because its websearch tool required a search
provider with its own organization approval, account or key, and billing, which
contradicted the arm's purpose as a no-additional-tooling fallback. It set one
reopen condition: search capability through the existing Copilot support
without additional organizational spend.

OpenCode v2 now ships a keyless `tinyfish` search provider. TinyFish is the
OpenCode vendor's own hosted endpoint; with no credential configured the client
sends an explicit keyless access header, so search works with no account, no
API key, no organization approval, and no billing. This was verified live on
2026-10-15: an unauthenticated call to the endpoint returned real results for
the runner's own preflight query (the official Python pathlib documentation
page). The v2 headless mechanics the adapter depends on were verified against
the v2 source: the server process reads an `OPENCODE_CONFIG_CONTENT`
environment variable for per-process config, `opencode run --format json`
emits `text`, `tool_use`, `step_finish`, and `error` events as JSON lines, and
permission rules are ordered action/resource/effect triples where unmatched
actions ask and headless runs auto-reject asks.

The reopen condition is met in substance but not in letter: the search
capability comes through OpenCode's own keyless endpoint rather than Copilot.
Accept that deviation because the condition's purpose — no additional
organizational spend, approval, or account — is exactly what the keyless
provider satisfies. Readmit the arm as `opencode-luna`, pinned to
`github-copilot/gpt-6-luna` at reasoning effort `medium` (billed through the
existing Copilot support), with the keyless `tinyfish` search provider recorded
in `config/arms.yaml`. The adapter injects deny-by-default permissions allowing
only read, glob, grep, websearch, webfetch, and question, and runs every
invocation with `--standalone` so a private server inherits that config instead
of attaching to a user's background service with unrelated config. The
evaluation returns to four arms and 20 run slots.

Accept the model duplication with `pi-luna` (both use `gpt-6-luna`) to measure
the same model under a second harness. Record two caveats with the results:
the keyless endpoint may rate-limit under load with unknown quota — if search
fails during preflight or runs, record the arm or run as unavailable rather
than adding a keyed provider — and the two Luna arms are not perfectly
comparable on the search axis because `pi-luna` searches through Copilot while
`opencode-luna` searches through TinyFish.
