## Implementation plan — Stage A interrupted-host recovery

**No tracked files were changed** in `./agent-harness-evals`; this is a design and test plan for the existing 23-task continuous cohort.

### Current contract and recovery boundary

The approved `staged-multilang-benchmark/5` freeze is the immutable cohort identity. For `archive-stage-a-cohort/1`, it binds the reviewed 23-task set, the seven canonical standard arms, one repetition, one attempt per slot, the seeded schedule, numerical policy, and outcome contract. The schedule and outcome slot plan must match slot-for-slot: **23 × 7 = 161 slots**. The 23 blocks run continuously in schedule order; there is no first-block stop or between-block approval.

The scheduler assigns a stable trial, attempt, and lease identity when it reserves a slot. It records the reservation before the launcher writes `intent.json` and starts the worker. The worker writes completion evidence before the scheduler records the typed terminal outcome. A host interruption can therefore leave evidence at several different points:

- **Before reservation:** the slot is still pending; the normal launcher can resume it.
- **After reservation, before trustworthy completion:** the slot is `in_flight`, with provider and research reservations still held.
- **After completion is durably written, before scheduler finish:** evidence may be adoptable without rerunning the worker.
- **After scheduler finish, before the block progress record:** the launcher’s existing `caught_up=true` path can reconstruct that record from the settled ledger.
- **After a block progress record:** resume verifies the chained record and unchanged settled slots before advancing.

Today, the launcher refuses an active reservation as `unreconciled active attempt; retain evidence, do not rerun`. Scheduler reconciliation only marks *pending* slots unstarted after the fixed cohort window and refuses while any slot is in flight. The cohort audit requires all slots terminal or explicitly unstarted, no reservation, quiescent resources, and a complete progress chain. The seal requires a passing audit of that exact freeze and final ledger checkpoint. It produces task-outcome-v2 records for attempted slots; if any slot is unstarted, the outer execution seal retains that disposition, but the task-outcome seal is not complete.

There is an existing narrow prelaunch-recovery precedent: the runbooks and audit code permit an explicit, evidence-bound recovery of a Claude reservation when the native phase demonstrably never began. That is not permission to replay an ambiguous native attempt.

### Recommended policy: resume evidence, never replay native work

| Choice | Assessment |
|---|---|
| **Replay the attempt** | Reject. A second native attempt would violate the one-attempt limit, add provider/research exposure, and risk biasing that arm. Do not mint a new lease, refund the old reservation, or rerun native work because artifacts are missing. |
| **Resume the cohort** | Choose for safe cases. Resume later pending slots and blocks from the same freeze, configuration, ledger, admission, approval, host profile, and artifact roots. If a completion is already fully persisted and validates, adopt it into the scheduler without executing the native agent again. Allow same-lease continuation only where durable evidence proves native execution/provider contact never began, under an explicit recovery receipt; never infer this from a missing output file alone. |
| **Terminal infrastructure failure** | Choose when native work began or its phase is uncertain, but scoped cleanup and process quiescence can be proven. Settle that *existing* attempt once as `infrastructure_failed`, with a typed interruption code and retained recovery evidence. It is an unknown/infrastructure-missing outcome—not a fabricated capability zero—and the full workflow charge remains consumed. Continue with the remaining slots. |
| **Unresolved stop** | Required when evidence, ownership, or quiescence cannot be established. Keep the reservation active, block further dispatch, and do not audit or seal. At window end, ordinary pending-slot reconciliation still cannot resolve this in-flight lease. Preserve the incomplete cohort for owner disposition; do not manufacture a terminal outcome to get a seal. |

### Proposed states and recovery operation

Add an explicit, locked recovery path rather than a reset/force-resume option. Recovery decisions must be evidence-driven and idempotent:

1. **`pending → in_flight`** remains unchanged: normal dispatch reserves the stable lease.
2. **`in_flight → terminal (adopted)`** when a complete `completion.json`, `result.json`, lifecycle evidence, and cleanup evidence are already durable and all validate. Recovery records the scheduler finish from those artifacts; it does not invoke native execution.
3. **`in_flight → same lease continues`** only for a narrowly defined, proven pre-native interruption. Retain the original intent/interruption, run any permitted remainder under a separate sibling evidence directory, and bind an owner recovery decision to the same lease. No new attempt identity or reservation is created.
4. **`in_flight → terminal infrastructure failure`** when native work began or cannot be proven not to have begun, and scoped cleanup proves no worker or owned resource remains. Write a recovery receipt and a valid v2 unknown/infrastructure-missing outcome using the existing outcome vocabulary; then consume, rather than refund, the reservation.
5. **`in_flight → unresolved`** when any trust or cleanup check fails. Do not mutate the ledger or advance.

The recovery receipt should bind the exact manifest digest, configuration and admission identities, slot/trial/attempt/lease IDs, original scheduler checkpoint, host/boot interruption evidence, inventory and hashes of original artifacts, phase reached, cleanup/quiescence receipts, the selected recovery disposition, owner decision where required, and the evidence digest used to finish the scheduler record. Write and fsync this receipt **before** the scheduler transition. Repeating recovery against the same receipt should either complete the same transition or report that it was already applied; it must never create a second charge or attempt.

Use the existing scheduler finish accounting for a terminal recovery: remove the active reservation once, retain the attempt’s account consumption, and append the normal finish event. If the transition cannot be completed, leave the reservation intact. Do not mark a dispatched slot `unstarted`.

### Trust checks and implementation seams

Implement this before the cohort’s admitted freeze is published/launched, then qualify and approve the exact execution source. Do not hot-patch a running admitted checkout. The recovery path should:

- Revalidate the **whole canonical freeze digest**, owner approval, configuration, host profile, admission, and the original outcome contract. Reject changes to the 23-task cohort, seed/order, seven arms, schedule, slot plan, limits, or paths.
- Verify the exact slot-to-lease lineage against the ledger; require one active reservation and no competing launcher. Keep the fixed 161-slot denominator and one attempt per slot.
- Use scoped Inspect ownership receipts and verify process, container, volume, and research-service cleanup. Follow `inspect-recovery-and-shakedown.md`; never use global Docker cleanup.
- Verify artifact roots and recovery files are canonical, private, regular, non-symlink files with matching hashes. Preserve original files; put resumed evidence in a distinct sibling directory.
- Distinguish a fully persisted result from partial native evidence. Partial candidate output is not a completed result. Never infer a successful score, a timeout, or “no provider contact” from missing artifacts.
- Conserve provider and shared-research charges, including interrupted workflow reservations. Do not refund usage or reset the conserved research ledger. Keep actual provider/account failures typed.
- Require a fresh host check before dispatch resumes. If the admitted host/runtime/configuration no longer validates, stop and seek a new admission/freeze decision rather than altering the existing cohort.

### Planned code, documentation, and test work

Likely seams are `stage_a_launcher.py` and `stage_a_execution.py` for durable phase/completion evidence; `stage_scheduler.py` and `scripts/stage_scheduler.py` for the explicit recovery command; and the shared attempt reconstruction/audit path (`stage_a_first_block.py`, `stage_a_cohort_audit.py`, `stage_a_seal.py`) for validating recovery receipts and preserving v2 outcomes. Update `stage-a-continuous-cohort.md` and the scoped Inspect recovery runbook with decision steps and stop conditions.

Tests should cover:

- 23-task/161-slot and seven-arm schedule/slot-plan invariants, including rejection of any altered freeze or slot order.
- Fault injection after reservation, intent, native start, completion persistence, scheduler finish, and block settlement; restart must never execute native work twice.
- Adoption of valid persisted completion; rejection of partial, tampered, cross-linked, or missing evidence.
- The narrowly permitted pre-native continuation, with proof of no native/provider contact and an unchanged lease.
- Terminal interruption settlement as infrastructure-unknown—not score zero—with one attempt, one retained charge, one finish event, and no replay/refund.
- Unconfirmed quiescence or ambiguous phase evidence leaving the reservation active and preventing dispatch, progress, audit, and seal.
- Idempotent recovery receipt handling, concurrent-launch rejection, symlink/hardlink/path attacks, and evidence tampering.
- End-to-end audit/seal reconstruction for the exact 161-slot contract, plus finite-window reconciliation behavior and the explicit rule that an in-flight slot cannot be silently reconciled as pending/unstarted.

Run the existing focused scheduler, launcher, execution, cohort-audit/e2e, outcome-v2, and runbook tests, then the documented Stage A integration set before admission. Keep live provider/Docker execution out of these recovery tests.

### Rollback

Ship recovery as a fail-closed path with no automatic invocation. Before any recovery transition, rollback means disabling/reverting the new command and retaining all original files and the active reservation; the existing runner will continue to refuse it. After a transition, do **not** restore an older ledger snapshot, edit the receipt, reset the scheduler, or downgrade and attempt to seal with code that cannot validate the recovery evidence. Preserve the state for a forward fix or an owner-directed retirement/new freeze. A changed policy or implementation must not change the current freeze in place.

### Local verification

No tracked files were changed. `uv run --locked pytest` initially stopped because the installed uv was `0.13.0` while the repository requires `0.12.9`. I reran the focused checks using the pinned uv with a writable temporary cache:

`UV_CACHE_DIR=/tmp/agent-eval-uv-cache uvx --from uv==0.12.9 uv run --locked pytest -q tests/test_stage_scheduler.py tests/test_stage_a_launcher.py tests/test_stage_a_execution.py tests/test_stage_a_cohort_audit.py tests/test_stage_a_cohort_e2e.py tests/test_task_outcomes_v2.py tests/test_stage_a_archive_cohort_runbook.py`

**Result: 176 passed.** The test setup created an ignored `.venv` in the disposable worktree; `git status --short` remained clean.
