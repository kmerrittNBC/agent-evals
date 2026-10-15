I wrote a **plan, not code**, in `data-analysis-agent/docs/speculative/plans/2026-10-15-durable-question-run-boundary.md` and linked it from the plans README.

The plan compares desktop-owned state with backend-owned SQLite state and recommends the latter. It covers run and store IDs, API and status transitions, reconnecting after a window or sidecar restart, interrupted work, error handling, migration, tests, and rollback. It keeps the boundary local; no cloud service or credentials are required.

**Checks:** the focused backend run-store suite passed (7 tests), and `git diff --check` passed. No implementation or recovery tests were added, so the proposed restart behavior is not yet verified.
