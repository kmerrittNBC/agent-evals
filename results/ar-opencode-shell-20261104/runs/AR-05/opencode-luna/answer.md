Refactored the runner in `./agent-evals` to separate workspace lifecycle from harness conversation capture.

- Added a `Workspace` protocol and `SnapshotWorkspace` implementation in `src/agent_eval/core.py`. The snapshot implementation owns temporary-directory creation, pinned archive preparation, digest checks, and cleanup.
- Extracted harness phases, event normalization, answer/session handling, and event-file writing into `_capture_conversation`. `run_one` accepts an optional workspace factory so a different workspace can be supplied without changing conversation handling.
- Added tests for workspace cleanup and integrity reporting, plus a runner test covering continuation, event timing/indexes, answer, usage, and persisted output.

A future writable-worktree implementation could implement the same context-manager interface and provide its own `integrity_error` policy—for example, allowing expected edits while still checking other invariants. The current snapshot integrity behavior remains unchanged.

No IG prompts, arm models, or output schema were changed. No `AGENTS.md` was found.

Checks passed: **18 unit tests**, `compileall`, `git diff --check`, and CLI `--help`.
