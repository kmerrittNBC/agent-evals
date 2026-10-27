# Qualification evidence format v1

Use a new `results/codex-copilot-<id>/` directory for every pilot or full run.
Do not write into the October `results/` IDs or existing `evidence/` packs.
Record `protocol_sha256` and `mcp_catalog_sha256` before the first attempt.
Start with [run.template.json](run.template.json) and
[attempt.template.json](attempt.template.json); `null` means a required
measurement has not yet been observed, never a zero value.

```text
results/codex-copilot-<id>/
  manifest.json
  gate-status.json
  runs/<case-id>/<arm-id>/<repetition>/
    attempt.json
    events.jsonl
    answer.md
    billing.json
    screenshots/          # desktop only, reviewed and redacted
```

The run manifest contains `run_id`, `protocol_id`, both SHA-256 values,
`created_at`, account-plan category, organization-policy reference and gate-1
reviewer, authorized route and endpoint category, exact client/app-server/OS
versions and builds, actual model/provider/reasoning per arm, source commits,
prompt IDs and hashes, catalog/network/time limits, sanitized config hash,
and any deviations. No field may be filled with a guessed version. If a
required pin is absent, `execution_status` is `blocked` and no candidate
attempt is valid.

`attempt.json` contains `case_id`, `arm_id`, `repetition`, session/worktree ID,
start/end timestamps, outcome (`pass`, `fail`, `unresolved`), completion and
critical-error flags, time to first substantive response, final latency,
peak context and compaction count, prepared-check outcomes, blinded quality
scores where applicable, and references to the other artifacts. Keep
unavailable quantities as `null` with `measurement_status: unavailable`.

Each line of `events.jsonl` is one sanitized JSON object with:

- `sequence`, `timestamp`, `client`, `session_id`, `case_id`, `arm_id`, and
  `event_type` (`model_request`, `model_response`, `tool_discovery`,
  `tool_definition`, `tool_call`, `tool_result`, `web_action`, `error`,
  `compaction`, or `substantive_response`).
- `provider`, `model`, `reasoning`, `mechanism` (`hosted_tool_search`,
  `client_discovery`, `eager`, `native_web`, `mcp`, or `shell`), tool/service
  name, action, sanitized argument/result summary, and URL/citation when
  relevant. `tool_definition` carries `initially_exposed` and a schema hash;
  discovery carries loaded and deferred definition counts.
- `input_tokens`, `output_tokens`, `cached_input_tokens`,
  `cached_output_tokens`, `context_tokens`, `latency_ms`, and `error` with
  machine-readable code and sanitized message. Preserve provider-reported
  usage as reported; do not derive token counts from transcript length.

`billing.json` contains the provider/source, account-plan category,
measurement window and timezone, the attributable request/usage ID or
redacted stable reference, Copilot credits, OpenAI inference and hosted-tool
charges, currency, reconciliation method, and `attribution_status` (`matched`,
`unmatched`, `unavailable`). An account-level aggregate is not attributable
to one attempt. Keep invoice or usage screenshots only after review.

`gate-status.json` has one row per gate with `pass`, `fail`, or `unresolved`,
evidence paths, reviewer, timestamp, and deviations. A gate cannot be marked
pass from a model picker, a model answer without the required tool event, or
an unmatched billing total.

## Redaction and hash rules

Build artifacts from an allowlist of the fields above. Before committing,
remove access and refresh tokens, cookies, API keys, authorization and proxy
authorization headers, signed URLs, raw request bodies carrying credentials,
private account identifiers, home paths/user names, unrelated files, private
messages, and unrelated user data. Replace necessary identifiers with stable
local labels such as `account-A`; never commit a reversible encoding of a
secret. Keep only endpoint categories or public hosts when the exact endpoint
could expose a private route. Review screenshots for sidebars, notifications,
account menus, browser tabs, and terminal history; crop or mask unrelated
content before saving. Do not commit raw event dumps or captured environment
variables. Large captures belong in a controlled artifact store with an
access-controlled link and retention owner.

For a configuration hash, first construct a canonical sanitized JSON object
from public settings only: client version, provider category, model ID,
reasoning, tool/catalog IDs, network policy, and non-secret feature settings.
Sort keys, serialize with compact separators and UTF-8, then compute SHA-256.
Never hash the raw config as a substitute for redaction: low-entropy secrets
can be guessed from their hashes, and raw config paths can identify users.
Include a second SHA-256 of each committed sanitized artifact to bind review
notes to the exact evidence. Run a manual redaction review before push; a
pattern scan is useful but cannot establish absence of unrelated personal data.
