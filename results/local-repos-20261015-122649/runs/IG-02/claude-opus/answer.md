I read the code but didn't run anything (I had no shell access). So everything below comes from the source, not from test results.

## Short answer

**No, not for the same candidate.** After a timeout the record is marked `unknown`. Any later `merge()` call for the same `(bindingId, nativePrId, headRevision)` only reads the PR from the provider and never sends the merge again. The one gap: if a caller supplies a fixed `effectId()` and two processes run at once, both could send it (point 1 under "Where the guarantee stops").

One important caveat: **nothing in production calls this coordinator.** `PullRequestMergeCoordinator` is only created in tests. The store is built at `src/storage/store.ts:220`, but `pullRequestMerges` is never used anywhere else. `verifyAuthority` (the check of the approval decision) is meant to come from an "owner workflow" that doesn't exist yet. The docs agree: "No general agent or browser merge command exists at this adapter boundary" (`docs/authoritative/pull-request-adapter.md:94-99`). What follows is the designed path, not a live one.

## How a merge is recorded and sent (`src/pr/mergeCoordinator.ts:32-63`)

1. `verifyAuthority(candidate)` runs on every call, including retries.
2. `getByCandidate` looks for an existing row. The coordinator then proposes an effect ID: the old one if a row exists, otherwise `effectId?.()` or `randomUUID()`.
3. `admit()` (`mergeStore.ts:28-44`) runs in one SQLite transaction. It inserts a `pending` row that pins the binding revision, repository, PR ID, head SHA, base ref and revision, decision ID and actor ID. If a row already exists with the same intent, it returns that row with its original `effectId`. The database also enforces `UNIQUE(binding_id, native_pr_id, head_revision)` (`src/storage/migrations.ts:3045`).
4. **Decision point (line 38):** if a row already existed, or `admit` returned a different `effectId` than proposed, the call takes the read-only path. Otherwise it sends the merge.
5. **Send path:** `requestExactMerge` (`contract.ts:64-114`) reads the PR first and checks that it is open, not a draft, not queued, has the same head, base ref and base revision, is fast-forward-only, mergeable, has all required checks passing, and has current human approvals. Only then does it call `mergeFastForward`. Gitea is sent `do: fast-forward-only`, `head_commit_id`, `force_merge: false` and `merge_when_checks_succeed: false` (`gitea.ts:158-164`).
   - **Errors from the merge call itself are swallowed** (line 105). The code then reads the PR again to see what actually happened.
   - Any exception from the send path calls `markUnknown` and rethrows (lines 59-61).

## Stored states

`pending → unknown`, `pending → confirmed`, `unknown → confirmed`. The schema only allows these three values.
- `markUnknown` only changes rows that are `pending` (`mergeStore.ts:63`).
- `confirmed` is final. `confirm` refuses unless `mergedRevision === headRevision` (`mergeStore.ts:71`).
- Nothing ever moves a row back to `pending`, and nothing sends the merge again from `unknown`.

## What counts as success

A record becomes `confirmed` only when a provider read passes `validateObservation` (repository and PR ID match, SHAs are well-formed) and shows **`state === "merged"`, `head.revision === approved head`, and `mergedRevision === approved head`** (`mergeCoordinator.ts:42-43`, `contract.ts:111-112`). For Gitea, `mergedRevision` is `merge_commit_sha` (`gitea.ts:76`).

`confirmed` means "seen merged at exactly this head", not "RelayView did the merge". If the first read already shows the PR merged at that head, the code confirms without sending anything (`contract.ts:71-72`).

## Timeout, then retry

The first call sends the merge, the request times out, and the follow-up read still shows the PR open, so the call throws `merge_outcome_unknown` and the record becomes `unknown`. On retry, `previous` exists, so the call goes straight to the read-only path (lines 38-48). If the PR now shows as merged at that head, the record is confirmed. If not, it stays `unknown` and the call throws again.

## Conflicting or concurrent admissions

- **Same candidate, different intent** (different decision ID, binding revision, base revision or actor): `admit` throws `pr_merge_identity_conflict` before any provider call, and nothing is changed. Since `sameIntent` ignores `effectId` and `recordedAt`, a retry with a new UUID counts as the same intent.
- **Concurrent calls in one process:** `getByCandidate` and `admit` run back to back with no `await` between them, so the second caller always sees the first caller's row. It either gets `previous` back or gets an `effectId` that doesn't match its proposal, and takes the read-only path.
- **Concurrent calls in separate processes:** the `UNIQUE` constraint, or SQLite's busy/snapshot errors, make the losing insert throw before any send. That error is raised outside the `try`, so no state changes.

## Where the guarantee stops (from the code)

1. **A fixed `effectId()` across processes.** If process B's `getByCandidate` misses, and then B's `admit` finds A's already-committed row with the same intent, B gets back an `effectId` equal to its own proposal. The check at line 38 then passes, and B sends a second merge. The default `randomUUID()` avoids this. Because the option is injectable, callers must keep IDs unique per call.
2. **Rejections before the merge is sent are also marked `unknown`.** `head_moved`, `approval_missing`, `merge_conflict`, or a failed first read all hit the same `catch`. That candidate can then never be merged by RelayView. It can only be confirmed if someone else merges it. This favors safety over progress, and nothing documents a way out.
3. **There's no recovery on restart.** The comment says "restart recovery only reads", but `unresolved()` is never called. `unknown` records only get resolved if someone calls `merge()` again, and that requires `verifyAuthority` to still pass.
4. **The guarantee covers one row: binding, PR and head.** A new head SHA creates a new row and can lead to a new send. What stands in the way is the pre-send read (`merge_identity_mismatch` if the PR is already merged, `head_moved`) and the need for a fresh approval.
5. If the provider returns an invalid observation on the read-only path, the error is thrown before `markUnknown` (line 41). A `pending` row can then stay `pending`. It still never sends again.

## Provider assumptions (not enforced by RelayView)

- Gitea treats `head_commit_id` as a compare-and-swap, and fast-forward-only produces `merge_commit_sha == head`. The docs rely on this to cover the base moving between the read and the send (`pull-request-adapter.md:101-104`). If the provider broke this, the result would be a stuck `unknown`, not a false `confirmed`.
- Reads eventually reflect a merge that happened. A request that timed out but is still in flight may land later. Progress depends on reads catching up and on someone retrying.
- **Nothing depends on the provider ignoring duplicate merge requests.** The code avoids sending twice instead.
- The `merged` flag and `merge_commit_sha` from Gitea are trusted as accurate, given authenticated HTTPS.
- The "already queued" check never fires on Gitea: the docs say `queuedMerge` is `unknown` there, and the code never asks for auto-merge.

## What the tests actually show

| Test | What it shows | What it doesn't |
|---|---|---|
| `mergeCoordinator.test.ts:19` | The row is `pending` at the moment of sending (asserted inside the stub). A timeout leads to `unknown`. A retry doesn't send again (`dispatched === 1`). A later merged read leads to `confirmed` without sending. | Uses a stub adapter, a no-op `verifyAuthority`, and runs sequentially. |
| `mergeCoordinator.test.ts:50` | It patches `admit` to plant a `"winner"` row first. Result: zero sends and the winner row kept. | It fakes the race inside one process. No real concurrency, no `UNIQUE` violation, no fixed `effectId` case. |
| `mergeStore.test.ts` | Admitting the same intent twice returns the original ID. A different `decisionId` or `baseRevision` causes a conflict. `unknown` works. `confirm` rejects a mismatched SHA. | Doesn't test `unresolved()`. |
| `contract.test.ts` | Pre-send rejections make no provider calls. A timeout gives `merge_outcome_unknown`. The happy path sends once. | Doesn't involve the coordinator or the stored states. |
| `gitea.test.ts:67` | The exact request body Gitea receives. | No real provider involved. |
| `gitea.real.test.ts` | Opt-in and skipped unless its environment variables are set. On real Gitea, merging a draft is refused, and after a fast-forward merge `mergedRevision == head`. | Doesn't test timeouts, the coordinator, or human reviews (its docs say so). |

The test tables are written by hand with `CREATE TABLE`, not built from migration 077. That means the real schema's `NOT NULL` and `CHECK` constraints are never exercised. Gaps the tests leave open:
- concurrency across processes
- a fixed `effectId`
- recovery after a restart
- pre-send rejections permanently marking a candidate `unknown`
- the coordinator hitting an identity conflict
- any production caller

**Bottom line:** the code does guarantee at most one merge request per stored candidate, with success confirmed only by an exact-SHA merged read, as long as effect IDs are unique per call. Two things are still unproven or missing: how it behaves against a real provider when requests time out, and any production wiring.
