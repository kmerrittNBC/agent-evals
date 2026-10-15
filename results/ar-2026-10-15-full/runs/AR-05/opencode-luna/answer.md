Implemented the workspace lifecycle seam in `agent-evals/src/agent_eval/workspace.py`. `run_one` now accepts an optional `WorkspaceProvider`; the default archive provider still exports pinned, read-only snapshots, checks their integrity, and cleans up its temporary directory. Harness capture and conversation handling remain in the runner.

The seam is a context manager that yields a workspace path, its initial digest, and an integrity check. A future writable-worktree provider could create and register Git worktrees in `open`, apply its own integrity policy, and remove the worktrees when the context exits—without changing the conversation loop.

Added tests for provider cleanup and for clarification continuation, merged events, final answer, and measured usage through an injected provider. No task prompts, arm models, or output schema were changed.

**Checks:** I couldn’t run the tests or other local checks because no command-execution tool is available in this session. No `AGENTS.md` was present in `./agent-evals`.
