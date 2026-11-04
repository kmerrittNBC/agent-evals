## Short answer

**In `PullRequestMergeCoordinator`, a retry of the same candidate does not dispatch a second merge.** Once an effect is recorded, retries read the pull request and either confirm the original merge or leave the effect unresolved. They do not call the merge endpoint again.

There is an important scope caveat: **the pinned source does not wire this coordinator into an owner API merge operation.** `src/api/application.ts` uses the Gitea PR adapter for probing, inspection, and draft creation, but has no merge-coordinator call. The coordinator is referenced in its tests, not in production call sites. So this is a guarantee of the coordinator implementation, not evidence that the current owner exposes an end-to-end approved-PR-merge flow.

## Trace and durable states

- The coordinator first calls `verifyAuthority(candidate)`. That trusted owner callback is responsible for validating the current candidate, Human decision, and binding; the coordinator does not establish that authority itself. It then admits an effect keyed by binding, PR ID, and head revision. See `src/pr/mergeCoordinator.ts:32–37` and `src/pr/mergeStore.ts:28–43`.
- Migration 77 creates `pr_merge_effect` with a unique constraint on `(binding_id, native_pr_id, head_revision)`. The record also pins the binding revision, repository, base ref and revision, decision ID, and actor ID. Its states are `pending`, `unknown`, and `confirmed`. See `src/storage/migrations.ts:3029–3047`.
- The first admission is persisted as `pending` before the provider preflight and possible write. Dispatch then goes through `requestExactMerge`, which reads and checks the current PR before calling the adapter. If that path does not return a confirmed result, the coordinator marks the effect `unknown`. A qualifying read can move it to `confirmed`. See `src/pr/mergeCoordinator.ts:36–61`.
- A retry finds the existing candidate record. It reads the PR; if that read does not prove the exact merge, it leaves the effect `unknown` and returns `merge_outcome_unknown`—it does not dispatch again. See `src/pr/mergeCoordinator.ts:34–48`.

One conservative detail: failures from `requestExactMerge`, including preflight failures that may have occurred before any write, are also marked `unknown`. This code has no “definitively not dispatched, safe to retry” effect state.

## What confirms success—and what dispatch asks the provider to do

Success is not inferred from a successful HTTP response or from a timeout resolving. The accepted observation must identify the same repository and PR and report the PR as **merged**, with the approved head still present and `mergedRevision` equal to that head. `requestExactMerge` applies this check after dispatch; the coordinator applies it during retry reconciliation. See `src/pr/contract.ts:104–113` and `src/pr/mergeCoordinator.ts:39–45`.

The request path checks the observed head and base, mergeability, required checks, and current attributed Human approvals before dispatch. The Gitea adapter sends `fast-forward-only`, the exact `head_commit_id`, `force_merge: false`, and `merge_when_checks_succeed: false`. See `src/pr/contract.ts:68–104` and `src/pr/gitea.ts:158–164`.

Those are **RelayView’s checks and request parameters**. They are not an independent proof of Gitea’s behavior: correctness still assumes the provider honors those parameters and returns accurate, sufficiently current merge observations. RelayView’s success decision is based on the authenticated provider readback.

## Conflicting and concurrent admission

For the same binding/PR/head key:

- A repeat with the same pinned intent coalesces to the existing effect, even if the retry proposed a different effect ID.
- A repeat that changes pinned intent—such as the binding revision, base revision, decision ID, or actor—fails with `pr_merge_identity_conflict`; it does not create another candidate effect.
- If another admission already won, the losing coordinator sees an existing effect ID and takes the read-only reconciliation path rather than dispatching.

The store performs the lookup and insert transactionally, with the database uniqueness constraint backing the candidate key. See `src/pr/mergeStore.ts:28–43, 95–101` and `src/storage/migrations.ts:3045`.

## What the repository tests establish

- `src/pr/mergeCoordinator.test.ts` simulates a provider-call timeout, verifies the effect was `pending` at dispatch and becomes `unknown`, then verifies an open-PR retry does not increase the dispatch count. It simulates an exact merged observation and verifies confirmation, still with only one dispatch.
- The concurrent-admission test injects a “winner” admission before the tested admission and verifies the loser does not call the provider merge. **That is a controlled admission collision, not a genuinely parallel multi-process or cross-database test.**
- `src/pr/mergeStore.test.ts` covers same-intent coalescing, conflicting decision/base identity, state changes, and rejection of a mismatched merged revision.
- `src/pr/contract.test.ts` exercises pre-dispatch checks and ambiguous outcomes with a fake adapter. `src/pr/gitea.test.ts` checks the merge request body using a fake fetcher.
- `src/pr/gitea.real.test.ts` is an opt-in Gitea smoke test, skipped without its configured disposable repository and credentials. It calls the adapter directly, and the documentation notes that it does **not** prove Human-review authorization.

These tests support the coordinator’s no-blind-redispatch logic and its exact-observation rule. They do **not** establish provider-side exactly-once semantics, behavior across independent owner databases, or that a production owner route currently invokes this coordinator. I inspected the pinned source read-only; I did not run the tests.
