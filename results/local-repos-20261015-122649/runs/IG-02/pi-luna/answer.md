**No—on the retry path for the same candidate, the coordinator does not issue a second merge request**, provided the retry uses the same durable store and candidate identity. RelayView achieves this by recording intent before provider work and making retries reconcile by read; it does not rely on the provider making merge requests idempotent.

### Flow and durable states

In [`src/pr/mergeCoordinator.ts`](relayview/src/pr/mergeCoordinator.ts), the coordinator first calls the owner-supplied `verifyAuthority`, then looks up an effect by `(bindingId, nativePrId, headRevision)`. For a new candidate, [`PullRequestMergeStore.admit`](relayview/src/pr/mergeStore.ts) transactionally writes a `pending` row **before** calling `requestExactMerge`.

That row pins the binding revision, repository and PR identity, exact head and base, Human decision ID, actor ID, and effect ID. The migration adds a unique constraint on `(binding_id, native_pr_id, head_revision)`. The durable states are:

- `pending`: the intent was admitted; it does not by itself prove that a provider request was sent.
- `unknown`: the outcome was ambiguous or an error occurred. This includes failures from `requestExactMerge`; the coordinator’s catch marks the effect unknown even if failure happened during its pre-dispatch checks.
- `confirmed`: an accepted observation matches the candidate head.

For a new effect, `requestExactMerge` reads the PR and checks that it is open, ready, mergeable, still at the recorded head and base, has successful required checks, and has the necessary current Human approval. It then calls the adapter and reads again. The Gitea adapter sends a fast-forward-only merge request naming the exact head, with force and queued merge disabled.

### Timeout and retry

If the call times out or throws, RelayView attempts a read. Success is confirmed only when the provider observation says the PR is **merged**, its head is the candidate head, and its merged commit SHA is that same head. If that observation is unavailable or does not match, RelayView records `unknown` and reports `merge_outcome_unknown`.

On retry, the coordinator finds the existing effect. For an existing effect it only reads the PR: an exact merged observation changes the record to `confirmed`; otherwise it keeps the result unknown and does not call `mergeFastForward` again. Thus a timeout can leave the actual provider outcome uncertain, but retrying that same candidate is not a second merge attempt.

### Conflicting and concurrent admission

An existing row for the same binding, PR, and head is reused only if the rest of the intent matches. A change to pinned details such as the base, binding revision, decision, or actor is rejected as an identity conflict rather than dispatched.

For concurrent admissions of the same candidate, the database uniqueness constraint and transactional admission select one retained effect. A losing coordinator that discovers a different effect ID takes the existing-effect, read-only path; it does not dispatch its proposed merge. This protection assumes the contenders share the same durable store. It is not a provider-side lock.

### What the tests establish—and do not

- [`mergeCoordinator.test.ts`](relayview/src/pr/mergeCoordinator.test.ts) makes the provider stub throw a timeout, verifies the record becomes `unknown`, retries the same candidate and checks that the merge-call count remains one, then supplies an exact merged observation and verifies confirmation.
- Its “concurrent admission” test inserts a winning effect before the coordinator’s admission. It establishes that this admission collision does not dispatch another merge; it is not a stress test of simultaneous provider requests or multiple owner processes.
- [`mergeStore.test.ts`](relayview/src/pr/mergeStore.test.ts) checks candidate uniqueness, identical-intent reuse, conflicting-intent rejection, and confirmation only for the recorded head.
- [`contract.test.ts`](relayview/src/pr/contract.test.ts) checks exact-merge preconditions and that an ambiguous result is not treated as success.
- [`gitea.test.ts`](relayview/src/pr/gitea.test.ts) checks the outbound request body, not the live provider’s semantics. The opt-in [`gitea.real.test.ts`](relayview/src/pr/gitea.real.test.ts) exercises a real disposable Gitea repository, but it calls the adapter directly and does not test timeout recovery through the coordinator.

So the code and deterministic tests support **“RelayView does not blindly resend this candidate’s merge.”** They do **not** prove that a timed-out request was or was not applied, that a provider read is immediately consistent, or that provider behavior under every race matches the assumed fast-forward semantics. Those remain provider assumptions; when RelayView cannot observe the exact merged result, it leaves the effect unresolved rather than guessing or retrying the write. The PR contract identifies adapter version 1, but the PR verification instructions call for recording the Gitea version on an opt-in run rather than pinning a tested server version as a code guarantee.
