Refactored `src/agent_eval/core.py` so `snapshot_workspace` owns creation and cleanup of the pinned read-only workspace, while `capture_conversation` runs the harness in a workspace supplied by its caller. `run_one` still checks the snapshot digest and produces the same events, answer, usage, continuation, and metrics outputs.

Added tests in `tests/test_runner.py` for cleanup on error, continuation and session handling, event timing, usage, and snapshot modification. A future writable-worktree runner could supply its own workspace lifecycle to `capture_conversation` and apply a different integrity policy without changing conversation capture.

Checks passed: 18 unit tests and `git diff --check`.
