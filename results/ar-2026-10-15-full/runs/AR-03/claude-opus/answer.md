I've written the plan to `docs/speculative/stage-a-host-interruption-recovery-plan.md`, marked as proposed and not implemented. I changed no code and made no commit. Along the way I found and reproduced a real defect in the existing seal.

**Where an interruption lands today.** If the host goes down while any slot is reserved, the next run stops at `stage_a_launcher.py:270` ("unreconciled active attempt"). It stops the same way whether the agent never started or had worked for 40 minutes. The only remedy in the runbook is to retire the attempt and approve a new freeze. That throws away the whole ledger and re-runs the interrupted slot in a new cohort, which in practice is the replay the rules forbid.

**The plan's core idea.** The code already writes durable files at the point where an attempt first contacts the model provider: `native/ownership.json` is written to disk before any container is created, and it records the host's boot ID. So after a reboot, each interrupted attempt can be sorted into one of four cases:

| Case | Situation | Recommended handling |
|---|---|---|
| C0 | Slot reserved, not launched | Resume under the same reservation |
| C1 | Launched, but stopped before contacting the provider | Resume under the same reservation |
| C2 | Past provider contact, not finished | Record as an infrastructure failure (`host_interrupted`); never re-run |
| C3 | Finished, but the result was never recorded in the ledger | Record the saved result without re-running |

Anything that doesn't fit these cases keeps today's stop.

**What stays fixed:**
- The freeze, the 161-slot schedule (23 tasks × 7 arms), one attempt per slot and the ledger format.
- No refunds, no second attempts, no slot marked unstarted.
- The futility rule is unchanged; a C2 slot counts as "capability unknown".

**Also in the plan:**
- A full trace from freeze to seal, with file and line references.
- Replay, resume and terminal failure compared case by case.
- The state transitions and nine trust checks (same inputs, different boot ID, ledger and progress chain, evidence snapshot, containers, research accounting, image store, credentials and window, owner confirmation).
- Ten test-first slices with the tests named, plus rollout and rollback.

**Gaps the work has to close:**
- **The seal rejects a recovered slot (current defect).** It doesn't pass `execution_commit` (`stage_a_seal.py:220`) and looks for results in the wrong directory (`:251`). Running the seal on the repo's own recovered-slot test fixture fails with `prelaunch recovery differs from the frozen execution`. Any resume design depends on fixing this, so it is slice 0 and can merge alone.
- **Research usage can't be traced to an attempt after a reboot.** The research trial ID and scope are only saved at the end of a run or on tmpfs.
- **A verifier interrupted mid-run leaves partial input files that fail the audit,** and the runbook forbids moving them by hand. The plan adds a reviewed way to record them.
- **The new attempt directory isn't flushed to disk,** so a power loss could lose it.

**Rollout:** this only helps cohorts admitted at a commit that includes it, because every dispatch checks the admitted commit. A cohort already running keeps today's stop-and-retire behaviour.

**Decisions for you:**
- **Accepting the new ADR.** Resuming a reserved slot needs an ADR amending ADR-0016, which says an active attempt is never replayed. The plan argues a pre-contact resume isn't a replay, but that's your decision before slice 6 merges.
- **Owner sign-off per resume.** Should each resume need its own recorded owner confirmation (proposed), or count as a routine operator recovery like enrollment renewal?
- **Timing of interrupted slots.** Should their end time be reported as the reboot time, an upper bound?
- **Regrading.** Should a run that finished but wasn't graded be regraded after the interruption (its own ADR), or stay a failure?

**Checks:** the focused scheduler, launcher, audit, seal, enrollment and scheduler-preflight tests pass at `b0b31dd` (216 passed). I had to run them with uv 0.12.9 and a writable uv cache under `/tmp`, because the default cache is read-only here. The seal reproduction is a throwaway test kept outside the worktree at `/tmp/agent-eval-tpj52mqh/probe/`.
