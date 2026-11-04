# Coding agent evaluation — updated executive report

**4 November 2026.** This report replaces the [15 October report (superseeded)](<executive-report-2026-10-15 (superseeded).md>) for current decisions. It uses the original information-gathering (IG) results and original Pi and Claude Code results, with the [shell-enabled OpenCode defined-update (DU)](../results/du-opencode-shell-20261104/report.md) and [architecture (AR)](../results/ar-opencode-shell-20261104/report.md) reruns. The original attempts remain available for audit.

## Executive summary

We tested five tasks each in information gathering, defined code updates, and architectural planning or refactoring. Four model-and-agent pairs attempted every task. The central question is which setup can complete useful work across all three categories with acceptable quality, time, intervention, and cost.

**The OpenCode exclusion in the October report is withdrawn.** The OpenCode V2 runner accidentally allowed the V1 `bash` action while denying all other actions by default. [V2 calls command execution `shell`](https://opencode.ai/v2/docs/migrate-v1), so OpenCode could not run commands in the original DU and AR attempts. A corrected permission and a live shell preflight were added in [commit `7ece962`](../src/agent_eval/adapters.py). The shell-enabled reruns completed **5/5 DU** and **5/5 AR** tasks. All five DU focused and regression check sets passed; AR-05's code check passed. The [correction record](opencode-shell-correction-2026-11-04.md) explains the defect and replay boundaries.

The revised evidence supports these conclusions:

- **Claude Code + Opus completed the most tasks:** 14/15, compared with 13/15 for Pi + Luna, 12/15 for Pi + Sol, and 11/15 for OpenCode + Luna. Its completion lead is concentrated in IG, where it finished 5/5.
- **OpenCode + Luna is a strong candidate for DU and AR work:** it completed 10/10 across those categories, compared with 9/10 for each other pair. Its unchanged IG result remains 1/5, so it is not yet a demonstrated single setup for all three kinds of work. The poor original DU result was a harness configuration failure, not evidence for excluding it from code updates.
- **Pi + Sol was fastest overall and had the highest mean judged quality:** median final time 44.3 seconds and mean score 4.60/5. OpenCode followed on mean quality at 4.53/5, Pi + Luna at 4.47/5, and Claude Code + Opus at 4.20/5. These means summarize ordinal judge scores; they are not calibrated measures of ability.
- **A single default remains a provisional choice.** Pi + Luna completed at least four tasks in every category and is a reasonable Copilot-backed generalist to pilot. Claude Code + Opus has the strongest observed completion record but uses separate billing. For a split workflow, OpenCode + Luna deserves a DU/AR pilot alongside another IG route. Cost per attempt and blind human review are still missing, so the data do not justify a definitive rollout ranking.

| Model + coding agent | IG complete; rating | DU complete; rating | AR complete; rating | Total complete | Mean quality / 5 | Median final time | Critical errors |
|---|---|---|---|---:|---:|---:|---:|
| GPT-6 Luna + Pi | 4/5; Good | 4/5; Good | 5/5; Excellent | 13/15 | 4.47 | 75.7 s | 2 |
| GPT-6 Sol + Pi | 3/5; Practical | 4/5; Good | 5/5; Excellent | 12/15 | 4.60 | 44.3 s | 2 |
| GPT-6 Luna + OpenCode | 1/5; Unacceptable | **5/5; Excellent** | **5/5; Excellent** | **11/15** | **4.53** | **64.5 s** | **1** |
| Claude Opus 5.5 + Claude Code | 5/5; Good | 4/5; Good | 5/5; Good | 14/15 | 4.20 | 102.7 s | 1 |

“Complete” is the judge's task-completion assessment, separate from a finished process or a passing check. Ratings follow the [precommitted five-task category rubric](../config/rubric.yaml); there is no pooled 15-task rating. The table combines attempts made on different dates, as explained below.

## What changed in the evidence

The October study generated 60 first attempts: 15 tasks for each of four pairs. On 4 November, only OpenCode + Luna was rerun on the five DU and five AR tasks, producing ten more attempts. This report selects those ten new attempts and the other 50 original attempts. The DU adjudication rejudged saved October work; it was not another agent run.

The new attempts used the same task prompts, model, reasoning effort, pinned starting commits, and 15 October information cutoff. The DU-04 prepared check now includes the valid-symlink collision case found during adjudication. OpenCode's new preflight observed a successful `shell` call; each new DU and AR task trace also contains shell calls. IG was intentionally read-only for every arm, so the permission mistake did not change its tool contract and IG was not rerun. Different dates, fresh model outputs, and the revised DU-04 check mean the score changes cannot be attributed solely to shell access.

| Category | Pair | Tasks complete | Quality distribution (scores 1/2/3/4/5) | Median final time | Critical errors | Code validation |
|---|---|---:|---|---:|---:|---|
| IG | Luna + Pi | 4/5 | 0/0/1/1/3 | 65.0 s | 1 | n/a |
| IG | Sol + Pi | 3/5 | 0/0/1/1/3 | 33.8 s | 1 | n/a |
| IG | Luna + OpenCode | 1/5 | 0/1/0/3/1 | 28.9 s | 1 | n/a |
| IG | Opus + Claude Code | 5/5 | 0/0/0/4/1 | 103.7 s | 0 | n/a |
| DU | Luna + Pi | 4/5 | 0/0/1/2/2 | 63.6 s | 1 | 5/5 green |
| DU | Sol + Pi | 4/5 | 0/0/1/0/4 | 40.9 s | 1 | 5/5 green |
| DU | Luna + OpenCode | **5/5** | **0/0/0/0/5** | **53.9 s** | **0** | **5/5 green** |
| DU | Opus + Claude Code | 4/5 | 0/1/0/1/3 | 43.8 s | 1 | 4/5 green |
| AR | Luna + Pi | 5/5 | 0/0/0/1/4 | 178.9 s | 0 | AR-05 green |
| AR | Sol + Pi | 5/5 | 0/0/0/1/4 | 103.7 s | 0 | AR-05 green |
| AR | Luna + OpenCode | **5/5** | **0/0/0/1/4** | **141.5 s** | **0** | **AR-05 green** |
| AR | Opus + Claude Code | 5/5 | 0/0/0/4/1 | 254.6 s | 0 | AR-05 green |

The five-task samples are exploratory. The [IG run](../results/local-repos-20261015-122649/report.md), [adjudicated October DU run](../results/du-2026-10-15-adjudicated/report.md), and [October AR run](../results/ar-2026-10-15-full/report.md) supply the unchanged rows. The two November OpenCode reports supply the replacement rows.

## Task-level findings

### Information gathering

| Task | Luna + Pi | Sol + Pi | Luna + OpenCode | Opus + Claude Code |
|---|---:|---:|---:|---:|
| IG-01 — reconcile model benchmark scores | 3/P | 3/P | 2/P | 4/C |
| IG-02 — investigate retried pull-request merge | 5/C | 5/C | 4/P | 4/C |
| IG-03 — compare repository runtime requirements | 5/C | 5/C | 4/P | 4/C |
| IG-04 — check Playwright feature support | 4/C | 4/P | 5/C | 4/C |
| IG-05 — decide whether qualification results justify ranking | 5/C | 5/C | 4/P | 5/C |

`C` means judged complete and `P` partial. IG-01 produced three partial answers and three critical-error judgments across the four pairs. These calls still need blind human review. Pi and OpenCode used different search providers and page-fetch tools even when both used Luna, limiting a pure harness comparison.

### Defined updates

Each cell gives **quality / completion / validation**. `V` means the frozen focused and regression checks passed; `F` means validation failed.

| Task | Luna + Pi | Sol + Pi | Luna + OpenCode | Opus + Claude Code |
|---|---:|---:|---:|---:|
| DU-01 — delete todo API | 5/C/V | 5/C/V | **5/C/V** | 5/C/V |
| DU-02 — filter todo list | 5/C/V | 5/C/V | **5/C/V** | 5/C/V |
| DU-03 — reject duplicate repository assignments | 4/C/V | 5/C/V | **5/C/V** | 4/C/V |
| DU-04 — hash a symbolic link's target | 3/P/V | 3/P/V | **5/C/V** | 2/P/F |
| DU-05 — reject malformed repository metadata | 4/C/V | 5/C/V | **5/C/V** | 5/C/V |

In the shell-enabled DU rerun, OpenCode ran relevant local commands and produced five complete patches. Its DU-04 patch framed symlink target bytes before hashing them and passed both the broken-link check and the collision case. The October DU-04 answers remained partial for all other arms after adjudication; a green October check by itself did not prove the broader retargeting requirement. The new OpenCode DU-04 and October other-arm DU-04 validations therefore used different check sets, though the prompt and starting code were the same.

### Architecture and refactoring

| Task | Deliverable | Luna + Pi | Sol + Pi | Luna + OpenCode | Opus + Claude Code |
|---|---|---:|---:|---:|---:|
| AR-01 — consolidate pull-request effect coordination | Plan | 5/C | 5/C | **5/C** | 5/C |
| AR-02 — recover a research helper process | Plan | 5/C | 5/C | **5/C** | 4/C |
| AR-03 — recover an interrupted scheduler | Plan | 5/C | 4/C | **5/C** | 4/C |
| AR-04 — preserve desktop/backend runs through a restart | Plan | 5/C | 5/C | **5/C** | 4/C |
| AR-05 — separate runner workspace and conversation handling | Code | 4/C/V | 5/C/V | **4/C/V** | 4/C/V |

The four plans have no automated implementation check. AR-05's frozen runner suite passed for every pair. The new OpenCode AR-05 judgment deducted a point because its added tests did not directly inject preparation or capture failures to verify cleanup on those paths. OpenCode's AR-03 took 542 seconds, near the 15-minute task limit; its category median was 141.5 seconds.

## Matched comparisons and operational fit

For the same 15 prompts, Pi + Luna completed 13 tasks versus OpenCode + Luna's 11. That gap now comes from IG (4/5 versus 1/5); OpenCode completed one more DU task and tied AR completion. Their quality scores split **4 wins, 7 ties, and 4 losses** from Pi's perspective, and OpenCode finished faster on 10/15 tasks. These observations no longer support a broad claim that Pi's harness produces better Luna code updates. They do support a remaining IG reliability concern for OpenCode in this setup.

Pi + Sol completed 12/15, earned the highest mean judged quality, and finished faster than Pi + Luna on all 15 matched tasks. Claude Code + Opus completed 14/15, the highest total, but its advantage did not also produce the highest mean quality or shortest time. OpenCode's 10/10 DU-plus-AR completion is promising for a split workflow; it is still only one new attempt per task and does not establish a future success rate.

**Provisional operating choice:** Pilot Pi + Luna when one Copilot-backed agent must handle all three categories. Keep Claude Code + Opus as the observed completion leader where its separate billing and access are acceptable. Pilot OpenCode + Luna on defined updates and architecture work rather than excluding it; pair it with another IG route until its research reliability is investigated. Use Pi + Sol selectively when its observed speed or quality advantage merits its likely greater model-level credit draw. Revisit the choice after human review and attributable cost measurements.

## Cost evidence and limits

The [account-level Copilot screenshot for 1–15 October](../results/copilot-ai-usage-2026-10-15/README.md) showed 367.98 credits attributed to Sol and 50.32 to Luna. It is a historical model-level total, not a per-task record. It predates the November OpenCode reruns and cannot assign credits to Pi versus OpenCode, or price the corrected OpenCode results. Provider token and cost fields are not reconciled Copilot credits. Anthropic usage is in different native units, so this report does not compare monetary cost across the four pairs.

The [local Qwen follow-up](../results/local-qwen-linux-combined-20261030.md) remains a separate Pi pilot and is not included in the four-pair table. It produced 3/5 complete DU tasks, 1/5 complete IG tasks, and no AR deliverables in its tested serving setup.

Before a rollout ranking, blind reviewers should inspect the consequential critical-error judgments, the new DU patches, representative AR plans, and AR-05's cleanup behavior. Five prompts per category, ordinal judge scores, different search routes, and non-concurrent reruns limit generalization. The retained [October report (superseeded)](<executive-report-2026-10-15 (superseeded).md>) describes the original, misconfigured comparison and its earlier recommendation.
