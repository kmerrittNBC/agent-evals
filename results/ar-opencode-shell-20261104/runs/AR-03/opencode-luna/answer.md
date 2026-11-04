Added **`docs/runbooks/stage-a-host-interruption-recovery-plan.md`** in the disposable worktree. It is explicitly marked as a proposal—not implemented behavior or execution authorization.

The plan traces the existing freeze, stable slot plan, dispatch/completion path, block-progress catch-up, cohort audit and outcome seal. It preserves the **23-task, seven-arm, 161-slot** contract and recommends:

- **No replay** of a native coding attempt.
- **Resume the cohort** at pending work only after the existing trust checks pass; do not resume a native process without a proven checkpoint protocol.
- For an interrupted reserved slot, either record-only settle a complete, validated result for its existing lease, or—after proving quiescence and obtaining the required acknowledgment—settle that same lease as infrastructure-missing. If proof is incomplete, leave it unresolved and stop.

It also specifies proposed state transitions, trust and durability checks, tests, audit/seal requirements, and rollback. No runtime code was changed.

**Checks:** 240 focused Stage A, scheduler and outcome tests passed. The first test invocation hit the repository’s pinned-`uv` version mismatch; rerunning with pinned `uv` and a worktree-local cache succeeded. Relative documentation links and whitespace checks passed.
