Implemented in `./agent-evals`:

- Added `src/agent_eval/workspaces.py` to own pinned snapshot provisioning and temporary workspace cleanup.
- Added a `workspace_provider` seam to `run_one`, and extracted the harness prompt/continuation and event handling into `capture_conversation` in `core.py`.
- Added tests for workspace lifecycle, provider injection, and the clarification, continuation, event, and answer contracts.

A future writable-worktree provider could create a worktree at the pinned commits, yield its path, and remove it on context exit; conversation capture would use it unchanged. The current runner still treats workspace modifications as failures, so accepting agent writes would also require changing that integrity policy.

No `AGENTS.md` was found. Task prompts, arm models, and output schema were not changed.

Checks passed: `python3 -m unittest discover -s tests -v` (18 tests), `python3 -m compileall -q src tests`, and `git diff --check`.
