Added an implementation plan at `agent-harness-evals/docs/speculative/stage-a-interruption-recovery-plan.md`; no scheduler code or live runbook was changed.

The plan traces freeze publication, reservation, completion, progress, audit, seal and existing recovery boundaries. It rejects native replay and partial-process continuation. For an interrupted reservation, it proposes either finishing the **same lease** from an already valid completion or, with owner authorization and proven cleanup, recording a terminal infrastructure failure without inventing a score. It specifies trust checks, test seams and rollback while retaining the 23-task, seven-arm, 161-slot freeze.

Checks: 75 focused scheduler, launcher and cohort-audit tests passed. The plan file passed the whitespace check.
