# Copilot CLI headless web-search reprobe (2026-11-02)

This is a capability diagnostic, not a scored evaluation run. It does not
change the October 2026 results.

## Setup

- CLI: GitHub Copilot CLI 1.0.105 (`@github/copilot@1.0.105`), installed under
  `/tmp/agent-evals-copilot-cli-20261102` for this probe.
- Runtime: Node.js 24.21.0 on macOS.
- Model: `gpt-6-luna`, medium reasoning.
- Mode: noninteractive `--prompt`, JSON output, fresh session ID, 120-second
  timeout, `--allow-all-tools`, `--allow-all-urls`,
  `--no-custom-instructions`, and `--no-auto-update`.
- Prompt: the unchanged `PROBE` in `src/agent_eval/preflight.py`, which
  requires a `web_search` call to find the official Python `pathlib.Path`
  documentation followed by a `web_fetch` call on the result.

## Observations

| Run | Tool availability | Exit | Timed out | Observed tool calls | Result |
| --- | --- | ---: | --- | --- | --- |
| Repository preflight (`live_arm_probe`) | `web_search,web_fetch,view,grep,glob,ask_user` | 0 | No | `web_fetch` only | `unavailable`: search and fetch were not both observed in headless events |
| Diagnostic repeat | No `--available-tools` filter | 0 | No | `web_fetch` only | The final answer stated that `web_search` was unavailable and that the documentation URL was fetched directly. |
| Search-engine-fetch workaround | `web_fetch,view,grep,glob,ask_user` | 0 | No | Three `web_fetch` calls | Fetched two Bing query URLs and then a result link; the CLI reported unrelated Saudi Press Agency results for the Python documentation query. |

The second run returned `https://docs.python.org/3/library/pathlib.html` via
`web_fetch`; it did not perform the required search. Removing the tool filter
rules out that filter as the reason the first run lacked `web_search`.

The third run explicitly asked the CLI to fetch a Bing search results page for
`official Python pathlib Path documentation site:docs.python.org`, choose a URL
listed on that page, and fetch it. The event stream shows two
`https://www.bing.com/search?q=...` requests followed by a Bing result link.
This demonstrates a search-engine-page workaround through `web_fetch`; it did
not yield a relevant source in this attempt.

## Decision scope

Copilot CLI 1.0.105 does not pass this repository's **named `web_search` plus
`web_fetch`** gate in the tested account and environment. That is a reason to
exclude it under the current single-setup, three-category protocol, but it is
not proof that the CLI cannot search the web by other means. A functional
search-and-fetch gate could allow search-engine pages fetched through
`web_fetch`; it would need a new protocol and evidence that the discovered
result is relevant and actually used. This diagnostic does not evaluate
defined code updates, architecture tasks, an interactive CLI, or a VS Code
Agents window session. Re-run the gate after a CLI or account-policy change.
