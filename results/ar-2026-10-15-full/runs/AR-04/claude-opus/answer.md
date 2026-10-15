I've written the plan at `docs/speculative/plans/2026-10-15-durable-question-clarification-runs.md` and added it to the plans index in `README.md`. Only docs changed, and nothing is committed.

## Why a restart loses the run today
- **Rust shell:** in the default desktop setup, the shell kills the backend process it started when the window closes (`backend_sidecar.rs`). That ends any model call in progress.
- **Backend:** `InMemoryRunStore` keeps runs only in memory, so they're gone when the process stops.
- **Desktop:** the current run lives only in the UI's in-memory state (`insight-specialist-app.ts`), so the app forgets which run it had open. The file name is never sent to the backend, so it can't be restored either.

Other problems that block a safe reconnect:
- **Clarification is marked finished too early.** It's marked `succeeded` even when it's waiting for the user's answers. Submitting answers then flips it back to `running`, so a reconnecting client can't tell "waiting for you" from "done".
- **Double submissions start duplicate work.** Nothing stops answers being submitted twice. A retry after a restart would start a second interpretation.
- **Answer submission isn't atomic.** It's four separate writes, so a crash partway through leaves the run half-updated.

## Options compared
- **A (recommended): the backend owns the runs.** It saves them in SQLite in the app data folder; the desktop saves only a small pointer to the run it had open. This matches the repo's existing decisions to use SQLite and to keep run state in the backend, and it reuses the current reconnect support in the event stream.
- **B: the desktop keeps a copy of each run.** Rejected: there would be two copies that can disagree, and it can't continue a run after the backend restarts.
- **C: keep the backend running after the desktop closes.** This only survives until the backend crashes or the machine reboots, and it leaves stray processes. I've left it as an open question to add on top of A later.

## What the plan specifies
- **IDs:**
  - run IDs stay as they are;
  - a new database ID lets the desktop detect a wiped or different database instead of hitting confusing "not found" errors;
  - the desktop sends a key with each create and answer request so a retry can't create a duplicate;
  - each stage execution gets an attempt counter.
- **Statuses:** new `awaiting_input` and `interrupted` statuses, a full table of allowed changes with the event each one emits, and a "conflict" error for anything else.
- **Startup recovery:** when the backend starts, runs whose work died with the old process are marked `interrupted`, and a Resume action restarts them. Only one backend may own the database at a time, so a second backend can't wrongly interrupt the first one's live runs.
- **Error handling:** a table covering about a dozen failure cases. If the database can't be opened, the backend keeps working in memory and the desktop shows a "runs won't survive a restart" warning. It can't fail silently, because the backend's error output is currently discarded.
- **Migration:** no existing data to move; schema changes only go forward, with a backup first. The status change must ship in one change across backend, frontend and both mock backends.
- **Tests:** at each layer, including a restart test that kills the real backend process mid-call against a local fake model server, so no live LLM is needed. There's also a manual test plan.
- **Rollback:** setting `INSIGHT_SPECIALIST_RUN_STORE=memory` restores today's behavior without a code change. The restore feature only turns on when the backend reports support for it.
- **Rust:** no changes needed.

## Checks
- **Run:** the existing backend unit tests (28) passed using the system Python 3.14.7, since there is no backend virtual environment in this worktree. They confirm the current run-store behavior the plan describes.
- **Couldn't run:**
  - `test_main` fails because `fastapi` isn't installed.
  - The frontend tests (`pnpm test`, `test:ui`, `test:desktop`) and `cargo test` weren't run: there are no `node_modules`, `pnpm` isn't installed, and no code changed.

Also checked: all links in the plan to other docs resolve.

**Decision for you:** the plan defaults to a manual Resume, so restarting the desktop never triggers a model call by itself. An automatic option would better match the product's "don't make the user come back to a stalled run" goal. It's listed as open question 1.
