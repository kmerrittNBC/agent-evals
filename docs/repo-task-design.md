# Task design for repository work

The selected records now live in `config/defined-updates.yaml` and
`config/architecture.yaml`. Their evaluator-only packs are in
`evidence/DU-*/pack.json` and `evidence/AR-*/pack.json`. The criteria below
remain the selection and review standard. A task changed after an attempt
needs a new version and evaluation ID.

The information-gathering pilot covers the first column of the proposed capability matrix. This document describes the criteria used to select the five tasks for each of the two remaining columns. It does not change the active evaluation arms.

The two categories should measure work developers actually delegate. Give every arm the same starting commit, task prompt, repository access, tool permissions, time limit, and opportunity for one standardized follow-up. Run each task in a fresh session and an isolated checkout. Keep the identity of the model and harness out of the judge's materials.

## Defined repo updates with clear red/green loops

These tasks should have a narrow, observable outcome. A developer should be able to point to the behavior to change and an existing or prepared check that fails before the change and passes after it. The agent still needs to inspect the code, choose a sound implementation, and verify it; the task must not be reduced to copying a patch or following a file-by-file recipe.

A suitable task has all of these properties:

- The prompt states the user-visible behavior or defect, relevant constraints, and what counts as done. It does not prescribe the implementation.
- The pinned starting commit has a reproducible **red** signal tied to that behavior, such as a focused test, a type or build error, a lint rule, or another deterministic check. Record the exact command and expected failure before any arm runs.
- A correct change can produce a **green** signal with the same command. The evaluator also checks nearby regressions, not just whether the agent makes the focused check pass.
- The required change is small enough to complete in the run limit but substantial enough to require code reading and judgment. Include a range of code shapes and difficulty across the five tasks.
- The task can be done in an isolated checkout without production credentials, a deployment, or a GUI. If a service or fixture is needed, make it available to every arm in the same way.

Prefer real, previously encountered maintenance work whose expected behavior can be reconstructed from an issue, acceptance criteria, or a reviewed fix. If a check must be prepared for the evaluation, prepare and freeze it before running any arm. Do not reveal a reference patch or hidden grading checks to agents. A known red check is part of the task setup; graders may also use held-out checks to catch superficial fixes.

Format prepared checks before freezing them. Tell agents to add their own tests
in separate files. If they edit a prepared check, archive that edit as evidence
of their attempted coverage, then replay their code against the frozen check
in a fresh checkout for validation. A modified check alone must not turn a
finished attempt into a harness failure.

Measure whether the agent reaches a correct green state, what it changed, how much time and intervention it needed, and whether its explanation accurately describes the result. A passing command alone is insufficient: review the diff for broken behavior, unsafe shortcuts, unnecessary scope, and whether the implementation satisfies the requested behavior. Record failures and partial attempts rather than silently retrying them.

## Deep architectural planning and refactors

These tasks should represent work where the right change is not fully specified at the outset. The agent must understand the existing design, identify constraints and tradeoffs, and choose a defensible direction. Some tasks may ask for a plan; others may ask for a bounded refactor. Mark the requested deliverable before running the task, because a plan and a code change have different completion criteria.

A suitable task has all of these properties:

- The prompt names a real engineering goal, its motivation, and the known constraints, while leaving room for the agent to discover repository facts and make design choices.
- More than one plausible approach exists. The repository contains enough code and history to compare those approaches using concrete evidence.
- The expected work crosses meaningful boundaries, such as modules, packages, API contracts, data flow, deployment assumptions, or ownership. It is not merely a larger version of a focused bug fix.
- The evaluator can assess a response against a prewritten evidence pack: current architecture, constraints, important risks, acceptable approaches, and decisions that would be clearly wrong. The pack should allow justified alternatives rather than encode one preferred design as the only correct answer.
- The scope fits the run limit. For a code refactor, specify the boundary of work and the invariants to preserve. For a planning task, specify the decision or implementation plan needed for a developer to act.

Strong planning results should show accurate system understanding, make assumptions explicit, compare viable options, address migration and rollback where relevant, and give a sequence of implementable steps. Strong refactor results should also preserve behavior and interfaces, leave a coherent diff, and use appropriate existing checks. Do not reward volume or a confident tone in place of evidence. A useful agent may identify that a proposed refactor should be narrowed or staged; judge that against the task's actual goal.

Across the five tasks, include varied architectural shapes and degrees of ambiguity. Avoid five variations of the same subsystem or five prompts that reward the same design pattern. Do not make access to undocumented tribal knowledge a hidden requirement; supply any essential constraint in the prompt or the repository snapshot.

## Preparing a task before any arm sees it

For each selected task, freeze a task record with:

1. The exact prompt, task category, requested deliverable, repository and starting commit, and any allowed supporting materials.
2. The environment setup, allowed commands and network access, time limit, and known external dependencies.
3. The evaluator-only evidence pack and acceptance criteria, including acceptable alternatives and disqualifying mistakes.
4. For defined updates, the reproducible red command, expected failure, green command, and any held-out regression checks.
5. For architecture work, the relevant boundaries, invariants, known risks, and the evidence a sound plan or refactor should use.

Keep evaluator-only materials out of agent workspaces. Use the same task record for every arm. Pilot one task per category to check that the prompt and environment are usable, then freeze the remaining tasks before comparing arms. Any task changed after a run needs a new task version; results from different versions should not be pooled.

## Reporting alongside the information-gathering results

Retain the pilot's distinction between observed measurements and judgment. For every attempt, record start and end time, time to first substantive answer if the harness exposes it, time to completed deliverable, tool usage, whether the standardized follow-up was needed, credit or other cost data with its source, final artifact, and validation results. Mark unavailable measurements as unavailable rather than estimating them without a basis.

Use a fresh blinded judge context for each response and include the task-specific evidence pack. Apply the existing quality dimensions where they fit, plus category-specific evidence: correctness and regression safety for defined updates; system understanding, tradeoff quality, feasibility, and preservation of invariants for architecture work. Human review should inspect code diffs and a sample of plans, especially any critical error or disputed judgment.

Only assign **Excellent**, **Good**, **Practical**, or **Unacceptable** to an arm's category after aggregating its five attempts under a precommitted rule. Show completion rate, quality distribution, critical errors, intervention rate, timing, and cost beside the headline rating. Five tasks per arm are an exploratory comparison, not a precise estimate of general performance. GUI usability remains a separate evaluation.
