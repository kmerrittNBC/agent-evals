# IG and DU results so far — 15 October 2026

This compares the five information-gathering (IG) tasks in the [IG run](../results/local-repos-20261015-122649/report.md) with the five defined-update (DU) tasks in the [adjudicated DU run](../results/du-2026-10-15-adjudicated/report.md). The [DU adjudication](../results/du-2026-10-15-adjudicated/ADJUDICATION.md) replays five attempts that the original runner rejected for edits to prepared checks and rejudges Claude Opus on DU-04 with a symlink-collision test. The [original DU report](../results/du-2026-10-15-full/report.md) remains available. All four pairs used medium reasoning effort. No AR results are included yet.

## Outcomes

| Model and harness pair | IG rating; complete | DU rating; complete | Complete across 10 | Mean quality (1–5) | Critical errors | Median final time, IG / DU |
|---|---|---|---:|---:|---:|---:|
| Pi + Luna | Good; 4/5 | Good; 4/5 | 8/10 | 4.3 | 2 | 65.0 / 63.6 s |
| Pi + Sol | Practical; 3/5 | Good; 4/5 | 7/10 | **4.5** | 2 | 33.8 / 40.9 s |
| OpenCode + Luna | Unacceptable; 1/5 | Unacceptable; 2/5 | 3/10 | 3.8 | 2 | **28.9** / 57.7 s |
| Claude Code + Opus | Good; 5/5 | Good; 4/5 | **9/10** | 4.2 | **1** | 103.7 / **43.8** s |

“Complete” is the judge's task-completion judgment, not merely a finished agent process. Mean quality describes these ten ordinal scores; it is not a calibrated measure of general ability. Times are agent finish times, excluding adjudication. The headline ratings are the run's precommitted five-task category ratings; there is no pooled ten-task rating.

## Matched comparisons

Each row compares answers to the *same ten prompts*. Quality wins/ties/losses count which pair received the higher 1–5 score on each prompt. “Faster” counts the first pair's shorter final time.

| First pair versus second | Complete tasks | Quality wins / ties / losses | First pair faster | What the sample shows |
|---|---:|---:|---:|---|
| **Pi Luna vs OpenCode Luna** | 8 vs 3 | 6 / 3 / 1 | 2/10 | Pi completed five more tasks with the same named Luna model; OpenCode finished faster on eight. |
| **Pi Sol vs Pi Luna** | 7 vs 8 | 2 / 8 / 0 | 10/10 | Sol scored at least as high on every task and finished faster on every task; Luna completed one more task. |
| **Claude Opus vs Pi Luna** | 9 vs 8 | 2 / 5 / 3 | 7/10 | Claude's completion lead is one task, with no quality-score lead. |
| **Claude Opus vs Pi Sol** | 9 vs 7 | 1 / 5 / 4 | 1/10 | Claude completed two more tasks; Sol usually scored as high or higher and was faster on nine. |
| **Claude Opus vs OpenCode Luna** | 9 vs 3 | 5 / 3 / 2 | 5/10 | Claude completed six more tasks, with no consistent speed advantage. |

## Brief analysis

**OpenCode versus Pi.** The closest harness comparison is Luna in both: Pi's 8/10 completion versus OpenCode's 3/10 is a large operational gap in this sample. OpenCode's speed advantage does not offset five additional incomplete answers for tasks where completion matters. The harnesses also differ in tools, permissions, and search provider, so this does not isolate a single harness feature as the cause.

**Luna versus Sol.** Within Pi, Sol is the clear speed choice and has the highest mean quality score. Its completion deficit is one task: IG-04 was judged partial for Pi Sol but complete for Pi Luna. Both completed four of five DU tasks. Copilot credit data was unavailable, so there is no measured price comparison.

**How much better is Claude Opus?** On *completion*, Claude leads Pi Luna by **one task out of ten**, Pi Sol by **two**, and OpenCode Luna by **six**. Its advantage over the Pi pairs comes from IG: Claude completed 5/5 IG tasks versus Pi Luna's 4/5 and Pi Sol's 3/5; all three completed 4/5 DU tasks after adjudication. Claude does **not** lead on average quality score or consistently on speed. The evidence supports a modest reliability lead over Pi on these prompts, and a larger lead over OpenCode Luna, rather than a general claim that Opus is a stronger model in every respect.

## Limits on the comparison

- Five tasks per category are exploratory. A one- or two-task gap should not be treated as a precise estimate of future performance.
- Claude Opus uses a different model **and** harness from the Pi and OpenCode pairs. The observed gap cannot be attributed to the model alone. Pi Luna versus OpenCode Luna is closer to a harness comparison, while Pi Sol versus Pi Luna is closer to a model comparison.
- The adjudicated DU results are a replay and fresh judgment of saved work, not a new agent run. Claude DU-04 received an additional collision test after the original judge missed a defect already identified in other DU-04 patches. Future DU runs use the revised frozen check for every arm.
- Three IG-01 critical-error judgments and all decision-changing DU critical errors still merit blind human review before an operational selection. Provider-reported Copilot credits were unavailable, and Anthropic usage was recorded in different native units, so these runs do not establish cost efficiency.
- Linked result directories are local and ignored by Git. This document records their current state; the underlying reports and judgments must accompany it if shared outside this workspace.
