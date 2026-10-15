## Bottom line

**No.** The 35 outcomes are evidence that the seven adapters completed an **operational qualification** on five Python projects. They do not support ranking the seven arms, and they do not establish that comparative Stage A is complete.

The README itself draws that distinction: it says the qualification had 35 recorded outcomes and 31 passes, but calls them operational evidence across repair revisions—not a comparative ranking—and says a complete comparative Stage A has not been published ([`README.md`](agent-harness-evals/README.md); [`current-qualification-180-final.md`](agent-harness-evals/docs/evidence/current-qualification-180-final.md)).

## What the qualification establishes

Issue #180’s final evidence records **35/35 slots, 31 passes, three verifier failures, one eligible deadline timeout, and zero unresolved slots**. There were 36 task attempts because the original OpenCode/Sol infrastructure failure is retained separately from its completed successor. The five projects were Astropy, Matplotlib, Requests, Xarray, and Pylint.

This establishes completion of that operational gate and supports specific execution, capture, verification, recovery, and accounting claims under the recorded revisions. It does not make the failure counts a comparative capability result:

- Execution spans four revisions; the final revision supplies only four Claude outcomes, while earlier revisions supply the others.
- The three Matplotlib failures were unsuccessful patches on the same hidden test, not evaluation-infrastructure failures. The GLM Pylint timeout is a terminal zero, not a missing result.
- The qualification runbook explicitly says the five Python projects do **not** qualify the MultiLang parser or compiled-language resource requirements ([`current-qualification-180-final.md`](agent-harness-evals/docs/evidence/current-qualification-180-final.md), including its revision table and investigation dispositions; [`current-qualification.md`](agent-harness-evals/docs/runbooks/current-qualification.md)).

So the outcome table can describe this qualification’s observed results; it cannot be treated as a controlled seven-arm Stage A ranking.

## What the comparative cohort and freeze require

There are two different task counts in the repo. The v3 MultiLang selection contains **25** tasks, but the current executable Stage A target is the reviewed archive release of **23** tasks: two unresolved archive candidates are dropped without replacement. The current contract amendment specifies one continuous cohort of **23 tasks × 7 arms = 161 slots**. The prepared release record also says `dispatch_authorized: false` ([`staged-multilang-benchmark-v5.md`](agent-harness-evals/docs/contracts/staged-multilang-benchmark-v5.md), amendment and Stage A sections; [`stage-a-prepared-23-v1.md`](agent-harness-evals/docs/releases/stage-a-prepared-23-v1.md)). Thus the README’s opening “25-task” description refers to the selected corpus framing, not the current 161-slot executable archive cohort.

A comparative result requires more than having seven arms and recorded outcomes. The v5 freeze must bind the exact arm/runtime/provider and admission identities, corpus and task inputs, environment and verifier, resources, budgets, schedule and slot plan, retry/analysis policy, owner approval, and outcome contract. The Stage A run must then execute all scheduled blocks under one admitted configuration; after completion, it must be audited and sealed before a screening report and capability disposition can be published. A schema-valid manifest alone is not launch authorization ([`staged-multilang-benchmark-v5.md`](agent-harness-evals/docs/contracts/staged-multilang-benchmark-v5.md); [`stage-a-continuous-cohort.md`](agent-harness-evals/docs/runbooks/stage-a-continuous-cohort.md)).

The README explicitly says comparative Stage A has **not** been published. The qualification report likewise says its gate is separate from the comparative admission/freeze gates. The tracked prepared-23 release is not dispatch authorization. These sources do not establish a completed, sealed comparative Stage A.

## Claims that remain unverified

At this pinned repository state, the qualification does **not** verify:

- comparative Stage A outcome rates, arm ordering, paired wins/losses, or a numerical freeze;
- completion and sealing of the current 161-slot cohort, or its survivor/futility disposition;
- MultiLang parser and compiled-language execution behavior from the five-project qualification;
- that historical approvals or admissions authorize a new current freeze or dispatch;
- Stage B outcomes, which require a separate post-Stage-A freeze and cohort.

Even a completed 23-task screen would be a directional near-total-failure screen, not a precise ranking: each task is 1/23 of an arm’s denominator, and the contract cautions against treating close ordering as a reliable ranking or generalizing language-level performance from this purposive sample ([`staged-multilang-benchmark-v5.md`](agent-harness-evals/docs/contracts/staged-multilang-benchmark-v5.md), reporting and disposition sections).

I inspected the pinned checkout read-only; no files were changed.
