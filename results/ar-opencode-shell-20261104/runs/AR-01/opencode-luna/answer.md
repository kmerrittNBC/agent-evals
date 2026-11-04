## Proposed bounded refactor

**Recommendation:** add a small, provider-neutral lifecycle runner in `src/pr/` for the common “admit once, dispatch only when permitted, otherwise reconcile” flow. Keep the three typed coordinators, stores, provider adapters, and authority checks in place. Treat this as an internal refactor—not a new effect framework.

### Compare the seams

1. **Shared lifecycle runner — recommended.** It could centralize the repeated control flow for a retained intent: decide whether its state permits dispatch, invoke effect-specific preflight and dispatch callbacks when permitted, otherwise reconcile by observation, and preserve the effect-specific unknown outcome. Each coordinator would still define its own state eligibility and proof of confirmation. This reduces lifecycle duplication without making the provider or authorization rules generic.

2. **Shared store/base class — not recommended.** The stores repeat some SQLite patterns, but their admission keys, immutable identity fields, state transitions, and confirmation data differ. A generic store would either hide those distinctions behind many options or invite a schema change that this refactor does not need. Keep each store and table explicit.

### Shared behavior and effect-specific authority

The common lifecycle is: persist an immutable intent before an external write; reuse that intent on retry; confirm only from an observation that proves the intended effect; and retain uncertainty rather than blindly repeating an external write.

The differences must remain explicit:

- **Draft:** admission is tied to a confirmed publication and frozen PR requirement. It resolves the published ref/SHA and pinned binding, and searches by repository and branch pair. A retained draft intent may reconcile a matching draft, but an absent search result must **not** authorize another create. First-time creation additionally needs the provider’s draft/WIP behavior and exact head/draft verification.
- **Ready:** the owner verifies the policy milestone and records its authority ID and exact head/base identity. `preflight` is deliberately retryable before dispatch; the store’s transition to `pending` is the one-shot write boundary. An already-ready, exact observation can confirm without writing; an uncertain dispatched effect retries by reading only.
- **Merge:** the owner verifies the current Human decision and actor. Preserve `requestExactMerge` and its provider checks: exact head/base, open and ready state, mergeability, required checks, current attributed Human approvals, and fast-forward-only merge. A retry or restart reads for proof of the exact merged commit; it must not issue another merge.

In particular, do not collapse the existing state vocabularies into a shared persisted state machine. `draft` has `pending/unknown/confirmed`; `ready` also has a meaningful retryable `preflight`; `merge` has its own intent and proof requirements.

### Migration sequence

1. Add or sharpen characterization tests first, especially tests that count provider writes after uncertain outcomes.
2. Introduce the runner with typed callbacks for effect-specific eligibility, preflight, dispatch, reconciliation, and confirmation. Keep authority verification and observation validation in the coordinators.
3. Migrate readiness first, then merge, preserving `markDispatching` and `requestExactMerge` respectively. Migrate draft last because its create-by-branch lookup and “unknown absence never recreates” rule are the most distinctive.
4. Keep each store’s schema, identity checks, and state transitions unchanged. Update authoritative PR documentation only if implementation or verification shows a contract change; a behavior-preserving refactor alone does not justify changing the contract.

**No database migration is planned.** Existing durable rows remain readable with their current states and identities by either implementation.

### Rollback

Keep the refactor separable by coordinator. If an adopter changes dispatch or recovery behavior, restore that coordinator’s prior local flow and remove the shared runner only after no coordinator uses it. Do not rewrite, delete, or “repair” durable effect rows during rollback; retry them through the existing conservative behavior.

### Tests to preserve no-duplicate effects

Retain the existing focused coverage in:

- `src/pr/draftCoordinator.test.ts` — “published candidate creates one draft and reconciles a lost create response” and “a concurrent draft admission does not dispatch a second provider create.”
- `src/pr/readyCoordinator.test.ts` — “uncertain readiness stays unknown and does not retry the provider write,” “a failed readiness preflight remains retryable without claiming an unknown write,” and “an invalid post-write observation leaves the readiness effect unknown.”
- `src/pr/mergeCoordinator.test.ts` — “merge intent precedes dispatch and uncertain retries only observe” and “a concurrent merge admission does not dispatch a second provider merge.”

Add or strengthen cases for a draft create that times out, is not found by the follow-up lookup, and remains absent on retry—asserting the create call count stays at one. Also exercise retries through a newly constructed coordinator using the same store, so restart-like recovery proves the same no-duplicate invariant for draft, ready, and merge. For readiness and merge, cover the case where the write may have happened but the reconciliation read is unavailable, followed by a later read that either proves the exact effect or leaves it unknown without another write.

**Ablation decision:** not required. This is a behavior-preserving lifecycle refactor, not a change to an experimental workflow mechanism.

### Local check

I attempted `npm test -- src/pr` in `./relayview`, but it could not start because `vitest` is not installed (`vitest: command not found`). I did not install dependencies. The worktree was clean, and I made **no code or documentation changes**; the implementation plan is the deliverable.
