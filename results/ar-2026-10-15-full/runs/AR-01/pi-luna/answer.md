## Implementation plan — no code changed

The worktree is clean. I read `AGENTS.md`, the PR adapter contract, architecture heuristics, testing strategy, and the draft/ready/merge coordinators, stores, migrations, and tests.

### Current boundary

There is useful lifecycle overlap: each coordinator persists an effect identity before a possible external write, binds the effect to an exact candidate, and uses observations to confirm or leave an outcome unknown. Existing effects are not simply redispatched after uncertainty.

The important differences are part of the safety contract:

- **Draft:** keyed by report ID. It resolves and pins the publication, binding revision, repository, head and base; searches by branch pair; and creates only when the intent is newly admitted and no matching PR was found. An uncertain absence on a later call does not authorize another create.
- **Ready:** keyed by binding, PR and head. It verifies owner authority on every call, admits in `preflight`, checks the exact open draft and base, then atomically claims `pending` immediately before the write. Preflight failures remain retryable; post-dispatch uncertainty is read-only on retry.
- **Merge:** keyed by binding, PR and head, with the Human decision and actor pinned. It verifies owner authority, admits as `pending`, and delegates first-attempt checks and dispatch to `requestExactMerge`. Later calls only observe; confirmation requires the exact merged head and commit.
- **Provider rules:** the provider-neutral contract and Gitea adapter own observation validation and provider operations. In particular, merge remains fast-forward-only with the approved head, required checks and current Human approval rules; draft creation and readiness have their own exact identity checks. A shared lifecycle helper must not replace these rules or imply stronger provider guarantees.

### Seams compared

1. **One generic durable-effect coordinator/state machine.** It could centralize admission, dispatch, reconciliation and confirmation. However, draft’s branch-search/create sequence, ready’s preflight-and-claim transition, and merge’s pending-at-admission flow differ enough that the abstraction would need multiple hooks or modes. That raises the risk of hiding when dispatch is permitted or treating an inconclusive observation as permission to retry.

2. **A small shared lifecycle kernel beneath the three coordinators — recommended.** Keep the existing coordinators and typed stores. Extract only common bookkeeping for admitting/resuming an intent and for reconciling an observation into “confirmed” or “unknown,” with explicit caller-supplied rules for dispatch eligibility, identity matching and confirmation. Keep each coordinator’s authority checks, preflight, provider calls, and error semantics visible in its own flow.

The second seam is bounded and makes the safety distinction explicit: shared code can manage durable lifecycle mechanics, but only the effect-specific coordinator decides whether a write may happen and what observation proves success.

### Migration and rollback

1. Add the internal helper without changing the three public coordinator entry points or their store record shapes.
2. Refactor one coordinator at a time, preserving each effect’s current dispatch boundary and exact identity checks; run its focused tests before moving to the next.
3. Do **not** combine the stores or change the existing draft/merge/ready tables or migrations (76–78). Existing pending, preflight, unknown and confirmed rows must remain readable with unchanged meaning.
4. If the refactor fails validation, revert the helper and coordinator changes. No data rollback or database migration should be necessary; retain unresolved effects for reconciliation rather than clearing or recreating them.

If implementation changes the documented behavior or ownership boundary, reconcile `docs/authoritative/pull-request-adapter.md` after verification. A behavior-preserving internal refactor should not promote proposed design details into authoritative behavior claims.

### Tests to preserve and extend

Keep the existing coordinator tests, especially:

- `published candidate creates one draft and reconciles a lost create response`
- `a concurrent draft admission does not dispatch a second provider create`
- `owner-authorized readiness persists identity, reconciles a lost response, and never redispatches`
- `uncertain readiness stays unknown and does not retry the provider write`
- `a failed readiness preflight remains retryable without claiming an unknown write`
- `an invalid post-write observation leaves the readiness effect unknown`
- `merge intent precedes dispatch and uncertain retries only observe`
- `a concurrent merge admission does not dispatch a second provider merge`

Add bounded restart/retry cases that reconstruct a coordinator over the same durable store after an uncertain outcome and assert the external write count remains **one** for each effect. Also cover unresolved draft absence after restart: it must remain unknown/read-only, not attempt a second create. These checks should continue to exercise the real SQLite stores with deterministic provider fakes. Preserve the Gitea adapter tests for exact merge request fields and draft behavior.

### Local checks

- `git diff --check` passed.
- `npm test -- src/pr` could not run: `vitest` is unavailable because this worktree has no `node_modules`.
- No files were changed. Install dependencies before implementation verification, then run `npm test -- src/pr` and the relevant typecheck.
