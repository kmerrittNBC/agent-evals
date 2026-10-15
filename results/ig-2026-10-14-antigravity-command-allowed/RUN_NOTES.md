# Supplemental Antigravity run notes

This pilot uses the same information cutoff, repository commits, task prompts,
and judge packs as `ig-2026-10-14-five-arm-v2`. It changes only the temporary
Antigravity CLI permission setup: `--sandbox` was retained, and the local
settings permitted `read_url(*)` and `command(*)` while denying
`write_file(*)`, `execute_url(*)`, and `mcp(*)`. These settings were restored
to the user's original file after the run.

Preflight passed. IG-01 and IG-02 completed and were judged. IG-03, IG-04,
and IG-05 exited with `RESOURCE_EXHAUSTED (429): Individual quota reached`;
the CLI reported a reset in about seven days. Those failures should not be
interpreted as answer-quality results. See each run's `metrics.json` and
`events.jsonl` for the exact error and timing.

This is a partial follow-up, separate from the 25-slot primary evaluation.
