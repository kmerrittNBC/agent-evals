I split `run_one` into three parts: workspace creation and cleanup, harness conversation capture, and status classification. The event, answer, usage and continuation contracts are unchanged. All 20 tests pass (`python3 -m unittest tests.test_runner`): the 15 that were there before and 5 new ones. `python3 -m agent_eval --help` still works. I didn't commit anything, and the IG prompts, arms, configs and schemas are untouched.

**How I checked the behaviour didn't change:** before editing the runner, I wrote tests for `run_one` and ran them against the original code, where they passed. They still pass after the refactor. They fix:
- the continuation flow: the first prompt asks a clarifying question, so the continuation runs and reuses the same session;
- how the two phases are merged in `events.jsonl`: indexes, phase numbers and time offsets;
- the per-phase files `phase-N.jsonl`;
- the contents of `answer.md` and `metrics.json`, including usage, the time to first visible output, and the before/after snapshot digests;
- that a modified snapshot makes the run fail even when there is an answer;
- that a non-zero exit stops the run without a continuation;
- that the temporary workspace is deleted afterwards.

## The new seam (`src/agent_eval/core.py`)

- **`SnapshotWorkspace`** wraps the existing `prepare_workspace` and `tree_digest`. It has a small interface:
  - Entering it creates the read-only export and records the starting digest. If the export fails, it cleans up the temporary directory.
  - `path` is the only thing the harness sees.
  - `verify()` runs after the conversation and returns a failure reason or `None`. Here it returns "Repository snapshot was modified" if the digest changed.
  - `record()` returns the fields this workspace adds to the metrics. Here that's `snapshot_digest_before` and `snapshot_digest_after`, in the same position in the output as before.
  - Exiting it removes the directory.
- **`converse(...)`** contains only the harness conversation: running the phases, merging events, picking the final answer, detecting a clarifying question, and the per-harness session handling (Copilot UUID, Pi session file). It knows nothing about snapshots or digests; it just gets a directory and an environment.
- **`run_status(conversation, workspace_failure)`** applies the same status rules in the same order as before, with the workspace failure checked first.
- **`run_one(..., workspace_factory=snapshot_workspace)`** puts these together. The default keeps the current read-only behaviour, so `__main__` didn't need changing.

## How a future writable-worktree workspace would use it

A `WorktreeWorkspace(task, manifest)` would implement the same five pieces:
- **On enter:** run `git worktree add --detach <tmp> <pinned commit>` for each repo, instead of exporting a read-only copy.
- **`verify()`:** save `git diff <commit>` and the list of untracked files into the run directory as the result to be judged. Editing files would no longer count as a failure. It would only return a reason for real violations, such as a changed `HEAD`, new commits, or files written outside the worktree.
- **`record()`:** return its own fields, such as the diff path, diff stats or the final commit, instead of the snapshot digests.
- **On exit:** run `git worktree remove --force` and `git worktree prune`.

The conversation and status code would not change. The new test `test_workspace_factory_owns_integrity_policy_and_record` shows this with a writable workspace: the agent writes a file, the run completes, the workspace's own fields appear in the metrics, and enter → verify → exit happen in that order.

Two things a real worktree arm would still need, which I left out of this change:
- The adapters currently grant read-only tools (for example OpenCode's deny-by-default rules and Pi's `--tools`), so writing would need a tool profile chosen per workspace.
- The new metrics fields aren't required by `schemas/agent-run.schema.json`, so they fit without changing the schema. The report and judge would still need to learn to read the diff artifact.
