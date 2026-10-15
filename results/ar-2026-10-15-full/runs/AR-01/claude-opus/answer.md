I wrote the refactor plan as a new speculative document, `docs/speculative/pull-request-effect-lifecycle-refactor.md`. No source code changed and nothing is committed.

**Recommendation.** Add one shared "lifecycle runner", `runDurableEffect(spec)` in a new `src/pr/effectLifecycle.ts`. It would own the shared sequence: check authority, record the intent, claim the right to send, send once, then confirm from a read or mark the outcome unknown. Each of the three existing stores keeps its own SQL and just exposes a small common interface. The runner supports both ways the coordinators currently decide who may send: draft and merge claim it when the intent is first recorded, while ready uses its separate `preflight` state. That keeps today's behavior exactly. Merge needs one extra step: split `requestExactMerge` into the checks, the provider call, and the result check, while still exporting the combined function so `contract.test.ts` doesn't change.

**Seams compared.**
- **Shared store base (SQL only):** lowest risk, but the logic that actually prevents duplicate sends would still be copied across three coordinators.
- **Lifecycle runner (recommended):** puts the no-duplicate rule in one place where it can be tested with fakes.
- **One combined table and coordinator:** rejected, because it needs a data migration and would mix three different kinds of authority behind one switch.

**What stays separate for each effect:**
- **Who may trigger it:** draft needs a confirmed publication, a policy that requires a PR, and the local operator; ready needs a verified milestone; merge needs a verified Human decision.
- **Draft-only setup:** which binding revision to use (current or pinned) and the default base branch.
- **Checks before sending:** ready's exact head/base check, and all of merge's gates (checks, approvals, fast-forward only).
- **What counts as confirmed:** each effect has its own test of the provider's answer.
- **Provider rules:** the Gitea specifics stay in the adapter.

**Three existing behaviors I confirmed with throwaway tests** (deleted afterwards). The refactor keeps all three and pins them with tests; fixing them is left to a later issue:
- **A failed merge check permanently blocks that merge.** If a check fails before anything is sent (for example, required checks still pending), the effect is marked unknown. Later calls only read, so the same head can't be merged even after the checks pass.
- **A draft interrupted before it is created can never be created.** If the first search fails, or the owner stops between recording the intent and creating the draft, every later call returns `create_outcome_unknown` and never creates it.
- **Retries of finished effects can report unknown.** A confirmed effect is re-read on retry; if that read fails, the caller gets `*_outcome_unknown` even though the stored record says confirmed.

**Two gaps the plan also addresses:**
- The coordinator tests build tables by hand without the real schema's allowed-state constraints. Writing `preflight` to the merge table would pass those tests and fail in production, so slice 0 switches them to the migrated schema.
- Only the draft coordinator is used in production; ready and merge have no callers yet. Nothing scans for unresolved effects after a restart; they are only reconciled when retried.

**Migration and rollback.** Six slices, each one commit with its test written first:
0. tests that pin current behavior, including the three above;
1. the runner and its tests;
2. move ready onto it;
3. split the merge helper and move merge onto it;
4. move draft onto it;
5. one doc sentence.

Rollback is a plain revert of any slice: there is no schema change, and records written before and after look the same. The later fixes (adding a `preflight` state to draft and merge) would need a table rebuild. Rolling that back needs a restored backup or a forward fix, because the store refuses a database written by a newer schema.

**No-duplicate tests named in the plan.** Every one counts provider writes:
- a lost response is sent only once;
- after a restart, a recorded intent is only read, never re-sent;
- the loser of a simultaneous first attempt never sends;
- when two callers race at the preflight claim, only one sends;
- a failed or invalid read keeps the effect unknown;
- a conflicting intent never reaches the provider;
- a test that closes and reopens the real store and checks no effect of any kind is re-sent.

**Checks run** (after `npm ci`, which was needed because `node_modules` was missing):
- `npx vitest run src/pr`: 54 passed, 1 skipped (the opt-in real-Gitea test).
- The API pull-request tests (`-t 'pull-request|PR inspection'`): 2 passed.
- Server typecheck: clean.
- `src/docsStandards` tests: 51 passed.

`npm` warned that Node v22.19.0 is older than some packages ask for, but nothing failed.

No ablation flag is needed, since this isn't an experimental mechanism. Documentation is limited to one sentence in the adapter doc once the runner exists.
