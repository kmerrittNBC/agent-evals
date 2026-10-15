## Outcome

**No code or documentation was changed.** This is an implementation plan based on the coordinators, stores, tests, migrations, and pull-request adapter contract in `./relayview`.

### Recommended seam: share settlement, keep dispatch and authority local

Add a small internal helper in `src/pr/` for the repeated **observe → match → confirm, otherwise mark unknown** portion of an effect lifecycle. Give it typed callbacks for observing provider state, deciding whether that observation proves this specific effect, confirming it in the effect’s store, and recording an unknown outcome.

Use the helper only after a possible provider write and when reconciling a retained effect. Each coordinator should continue to own admission, authority checks, preflight, and the exact rule that permits a write. In particular, the helper must never turn an uncertain retry into another external dispatch.

### Compared seams

| Seam | Benefit | Risk / decision |
|---|---|---|
| A shared base coordinator or complete generic lifecycle runner | Could remove the most repeated control flow. | The lifecycle differences are consequential: draft uses branch-pair lookup and admits one effect per report; ready has a retryable `preflight` state and an atomic transition to `pending`; merge records Human-decision identity and delegates provider preconditions to `requestExactMerge`. A universal runner risks blurring dispatch eligibility and failure semantics. **Do not start here.** |
| A narrow provider-observation settlement helper | Centralizes the repeated reconciliation and durable outcome pattern while leaving the three state machines and their policies explicit. | It removes less duplication, and must allow effect-specific match/validation behavior and error mapping. **Recommended.** |
| Shared SQL/store base class | Could consolidate repeated `unresolved`, `markUnknown`, and confirmation mechanics. | The stores have different intent keys, persisted fields, state sets, and confirmation payloads. Sharing SQL risks hiding those contracts for little lifecycle benefit. Defer unless a later change demonstrates a separate, clear need. |

### Keep these authorities and provider rules effect-specific

- **Draft** (`src/pr/draftCoordinator.ts`): require a confirmed hosting publication and frozen policy requiring a PR. A new effect requires an enabled binding; a retained one uses its recorded binding revision. Preserve repository identity checks, default-base selection, and branch-pair lookup. Confirm only a matching repository, head/base refs, exact head revision, and draft state.
- **Ready** (`src/pr/readyCoordinator.ts`): retain `verifyAuthority` for the trusted policy milestone. Preserve its preflight read and exact open/head/base-ref/base-revision checks. Only the caller that wins `markDispatching` may make the readiness write; only an exact open, non-draft observation proves readiness.
- **Merge** (`src/pr/mergeCoordinator.ts` and `src/pr/contract.ts`): retain `verifyAuthority` for the current candidate and Human decision. Keep `requestExactMerge` responsible for provider-specific checks—open and ready status, exact head and base, fast-forward-only strategy, mergeability, required checks and current Human reviews. Confirm only a merged observation whose merged revision equals the approved head.

The common helper should not own `verifyAuthority`, binding selection, dispatch permission, provider calls, or effect-specific observation predicates. Preserve current error codes and state transitions rather than “normalizing” them as part of this refactor.

### Migration and rollback

1. Add the helper and focused tests without changing effect schemas or public API shapes.
2. Refactor one coordinator at a time, retaining each store and its current durable intent identity.
3. Do **not** add a database migration or rewrite existing rows. Migrations 76–78 create separate draft, merge, and ready effect tables, with intentionally different state constraints.
4. If the change needs rollback, revert the helper and coordinator call sites. Leave effect rows intact: the existing coordinator/store code can continue reading them because their schema and meanings are unchanged.

### Tests to preserve no-duplicate effects

Keep the existing focused tests in `src/pr/draftCoordinator.test.ts`, `src/pr/readyCoordinator.test.ts`, and `src/pr/mergeCoordinator.test.ts`, especially:

- Draft: “published candidate creates one draft and reconciles a lost create response” and “a concurrent draft admission does not dispatch a second provider create.”
- Ready: “owner-authorized readiness persists identity, reconciles a lost response, and never redispatches”; “uncertain readiness stays unknown and does not retry the provider write”; and the preflight-retry test.
- Merge: “merge intent precedes dispatch and uncertain retries only observe” and “a concurrent merge admission does not dispatch a second provider merge.”

Add restart-focused cases: after an uncertain outcome, construct a new coordinator over the same store, retry while provider state remains inconclusive, and assert the create/ready/merge write count is still **exactly one**. Then expose the exact successful provider observation and assert the same retained effect confirms without another write. This specifically verifies the durable—not just same-instance—no-duplicate guarantee.

### Verification

The focused checks for an implementation would be `vitest run src/pr` and `npm run typecheck`. The repository’s pull-request adapter documentation also names `vitest run src/pr` as the contract/effect recovery check.

**I could not run local checks in this session:** the available tools here provide file reading and search but no shell/command execution. **Ablation is not required for the proposed refactor** because it changes lifecycle code structure, not an experimental workflow mechanism or its behavior.
