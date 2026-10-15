## Recommended approach

**Resume the same 23-task ledger, but never rerun the slot holding an uncertain native lease.** Reconcile that slot as a terminal infrastructure failure, then continue only with the still-pending slots. If the host cannot prove the work is quiescent, fail closed and do not resume or seal.

This preserves the frozen **23 tasks × 7 standard arms = 161 slots**, the one-attempt-per-slot rule, and the existing futility threshold. It does not add a task, arm, retry, or replacement.

## What the current flow does

- **Freeze and slot plan:** The continuous-cohort runbook and ADR 0016 bind the reviewed release, task order, seven arms, owner approval, and one schedule. The resulting plan has 161 slots. `stage_scheduler.new_state()` derives stable slot/trial identities from the complete freeze digest; validation rejects a different freeze or slot order.
- **Dispatch and execution:** `stage_a_launcher.run_block()` reserves a slot, writes its intent, then calls the native worker. If execution raises, it writes `interrupted.json` and leaves the reservation active. Normal launcher resume rejects that state with `unreconciled active attempt`.
- **Block progress:** `run_cohort_step()` records settled blocks in a chained progress log. If the ledger shows a block settled but its progress file was not written before the interruption, the next invocation can record it as caught up. It does not settle an active lease.
- **Audit and seal:** `stage_a_cohort_audit` requires all 161 slots to be terminal or unstarted, no reservations, a complete progress chain, and retained evidence. `stage_a_seal` requires that passing audit and builds the final execution and outcome seals. An interrupted slot therefore cannot simply be ignored.
- **Recovery runbooks:** The continuous-cohort runbook permits ordinary resume with the same freeze, configuration, ledger, admission, host profile, and artifact root when no attempt is active; after reboot it requires re-exporting the volatile credential leases. It explicitly provides no recovery for an uncertain active attempt. The portable-host checkpoint/reboot procedure is for pre-admission host qualification, not a live cohort ledger. The existing prelaunch-recovery precedent is narrower still: it requires specific evidence of a Claude enrollment failure before native execution and provider contact. It is not evidence that a generic host interruption was pre-native.

Attempt 6’s retained record is a practical example of the gap: the interrupted slot remained in flight, and the accepted one-attempt policy explicitly rejected retrying it.

## Choices

| Choice | Assessment |
|---|---|
| **Replay the interrupted slot** | Reject. It could issue a second native/provider attempt, violates the frozen one-attempt limit, and can alter the arm comparison and charge accounting. |
| **Resume only pending work** | Safe for slots that were never reserved, and for a settled block whose progress record is missing. It does not resolve an active reservation by itself. |
| **Terminally reconcile the active slot, then resume** | Recommended when host and evidence checks pass. Record an infrastructure failure for that original attempt, preserve its charge and identity, and continue with other pending slots. |
| **Stop without reconciliation** | Required if process/resource quiescence or evidence integrity cannot be established. Keep the ledger unmodified and unsealable; do not reset it or pretend the active slot was unstarted. |

A complete-but-unrecorded result is a distinct case: if durable completion evidence exists and validates, record that same result against the existing lease—**do not execute the worker again**.

## Concrete implementation plan

1. **Add an explicit Stage A recovery operation, not an automatic retry.** It should accept only one active lease in the existing canonical ledger and require a recovery receipt bound to that lease. Keep the normal launcher’s active-reservation refusal unchanged; recovery must be a separate, explicit operator path.

2. **Choose the terminal disposition from evidence.**
   - If `completion.json`, normalized result, cleanup evidence, and all referenced artifacts are complete and valid, reconcile the scheduler from those retained bytes.
   - Otherwise, after proving the agent, container, and research worker are stopped, write a recovery receipt and terminalize the original attempt as typed `infrastructure_failed` (for example, `stage_a_host_interrupted`). Do not claim that native execution or provider contact never happened merely because some files are absent.
   - Never change `in_flight` back to `pending`, refund charges, delete the reservation history, create a new attempt for the slot, or classify a reserved slot as `unstarted`.

3. **Preserve the scheduler’s existing accounting.** Use its existing one-attempt terminal path so the original lease, slot, and actual dispatch order remain intact; clear the active reservation only as part of the terminal transition and record the full account consumption. The new error code must not be retryable. The recovery receipt’s digest should be the retained evidence anchor for the terminal completion.

4. **Make the recovery auditable at outcome time.** Add a recovery-specific outcome builder using existing v2 outcome semantics: verifier unavailable, delivery unavailable, score unknown, and infrastructure-missing denominator, with the recovery receipt as evidence. It must not invent a candidate, verifier result, native telemetry, or a capability score. Extend cohort reconstruction to validate this recovery evidence and include the resulting unknown outcome in the all-slot seal. Keep the frozen slot plan, outcome contract, schedule, and futility rule unchanged; version outer audit/seal structures only if their schemas require it.

5. **Resume through the existing continuous path.** After the recovery transition, resume the same invocation and block. `run_cohort_step()` should record any now-settled block as caught up, or the launcher should run the remaining pending slots in order. No progress record should be written ahead of the ledger’s settled slots.

## Trust checks and stop conditions

The recovery command should fail closed unless it can verify:

- Exact freeze digest, owner approval, schedule and outcome-slot plan; exact 161-slot, seven-arm contract.
- Same admitted host identity/profile digest, checkout commit and clean state; same admitted paths, configuration digest, admission and credential/research bindings.
- Active lease and intent match the frozen slot, task, arm, attempt number, configuration, and manifest.
- Recovery evidence and all existing artifacts are canonical, non-symlinked, hash-valid, and pass the existing secret scan.
- No agent process, container, research worker, or competing launcher remains active; task-image state and cleanup evidence are consistent.
- The original conserved research allocation is still in use. A reservation is never refunded because a host stopped.

If the original host is unavailable, its identity no longer validates, evidence is corrupted, or quiescence is uncertain, **do not use another host’s profile or restore a stale snapshot and continue**. Leave the ledger intact for owner disposition. Retirement is not a way to finish this same cohort: a successor freeze would be a new experiment, and rerunning earlier slots would replay attempts.

## Tests and rollback

Test first at the scheduler transition, then the Stage A artifact/audit seam, then the cohort end-to-end seam. Cover: complete result written before scheduler finish; interruption before intent; interruption after reservation with partial evidence; host loss during native execution; interruption after block settlement but before progress recording; and unprovable cleanup. Assert the native worker call count does not increase during recovery, the original lease is retained, the slot has exactly one attempt, charges are not refunded, and all remaining slots proceed in order.

Also test rejection of changed freeze/configuration/approval/host, mismatched lease or task, tampered/missing recovery evidence, duplicate recovery, active processes, and secret-bearing evidence. The final audit/seal tests should prove exactly 161 schedule rows, 23 slots per arm, seven arms, and the unchanged futility calculation—including the recovered slot’s explicitly unknown disposition.

For rollback, keep recovery opt-in and leave existing ledgers untouched by deployment. If recovery fails before committing, leave the active ledger and stop. If it commits but a later audit fails, **do not roll back or edit the ledger**; retain the recovery receipt and stop for disposition. Do not reset state or replay the slot. Any new deployment must be admitted and frozen before a cohort starts; do not update a running cohort’s checkout.

## Local checks and changes

**No files were changed**; this is a plan-only response, and all inspection stayed within `./agent-harness-evals`. I could not run local commands because this session exposes no shell/command-execution tool. The focused checks for implementation should include:

```sh
uv run --locked pytest -q \
  tests/test_stage_scheduler.py \
  tests/test_stage_a_launcher.py \
  tests/test_stage_a_cohort_e2e.py \
  tests/test_stage_a_first_block.py \
  tests/test_task_outcomes_v2.py \
  tests/test_staged_contract_v5.py
```

I also reviewed the applicable `AGENTS.md`, ADR 0016, the continuous-cohort, scheduler, freeze and host-recovery runbooks, scheduler state schema, launcher, audit, and seal paths.
