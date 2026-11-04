# Coding agent evaluation — corrected OpenCode comparison

**4 November 2026.** This report combines the original Pi and Claude Code
attempts with corrected OpenCode attempts in all three categories. It replaces
the [earlier 4 November report](<executive-report-2026-11-04 (superseeded).md>)
and the [15 October report](<executive-report-2026-10-15 (superseeded).md>) for
current decisions. Both earlier reports and every original run remain
available as historical records.

## Executive summary

**OpenCode + GPT-6 Luna is now a credible general-purpose pilot candidate.**
It completed **14/15** selected tasks, tying Claude Code + Opus for the most,
and received the highest mean judged quality, **4.80/5**. Its corrected
defined-update (DU) and architecture (AR) runs each completed 5/5; its new
information-gathering (IG) run completed 4/5. This is a stronger observed
result than the October data supported. It does not establish an ideal or
definitive winner: IG-01 still had two judge-identified critical errors, and
Copilot credits per attempt remain unavailable.

| Model + coding agent | IG complete; rating | DU complete; rating | AR complete; rating | Total complete | Mean quality / 5 | Median final time | Critical errors |
|---|---|---|---|---:|---:|---:|---:|
| GPT-6 Luna + Pi | 4/5; Good | 4/5; Good | 5/5; Excellent | 13/15 | 4.47 | 75.7 s | 2 |
| GPT-6 Sol + Pi | 3/5; Practical | 4/5; Good | 5/5; Excellent | 12/15 | 4.60 | 44.3 s | 2 |
| GPT-6 Luna + OpenCode | **4/5; Practical** | **5/5; Excellent** | **5/5; Excellent** | **14/15** | **4.80** | **88.1 s** | **2** |
| Claude Opus 5.5 + Claude Code | 5/5; Good | 4/5; Good | 5/5; Good | 14/15 | 4.20 | 102.7 s | 1 |

“Complete” is the judge's task-completion assessment. The scores are ordinal
judge opinions, not calibrated capability measurements. Category ratings use
the [precommitted five-task rubric](../config/rubric.yaml); there is no pooled
15-task rating. The OpenCode IG rating is only **Practical** despite four
completions and four 5/5 scores because IG-01 contained two critical errors.

## Why the OpenCode evidence changed

The October OpenCode DU and AR attempts lacked command execution because the
runner allowed V1 `bash` instead of V2 `shell`. The
[shell correction](opencode-shell-correction-2026-11-04.md) and fresh
[DU](../results/du-opencode-shell-20261104/report.md) and
[AR](../results/ar-opencode-shell-20261104/report.md) runs corrected that
capability. All ten new attempts used `shell`; every DU focused and regression
check set passed, as did AR-05's code check.

The October OpenCode IG attempts had a different runner defect. The child
process changed directories but inherited `PWD` pointing at the evaluator
checkout. OpenCode located that project instead of the disposable pinned
source snapshot. Four of its five original IG traces read judge evidence packs
or prior result files; IG-02, IG-03, and IG-05 did not directly read the
required pinned repository files. Those attempts are unsuitable for ranking
OpenCode's source-research ability. A Linux A/B probe reproduced the misplaced
read and showed that setting `PWD` to the snapshot restores it.

The runner now pins `opencode-websearch@0.7.1` and selects its `native`
web-search provider, which uses OpenCode's authenticated Copilot model through
Responses API search. The default search model is pinned to the same Copilot
Luna model as the task. OpenCode IG runs use Bubblewrap to hide judge evidence,
prior results, and the configured source checkouts while exposing the pinned exports.
Live preflight requires a successful local `read`, `websearch`, and `webfetch`.
The [configuration decision](authoritative/adr/0003-use-copilot-search-for-opencode.md)
records the route and the workspace fix.

The [new OpenCode IG run](../results/ig-opencode-copilot-20261104/report.md)
used the original IG prompts, the same two pinned source commits, GPT-6 Luna
at medium reasoning, and the original 15 October information cutoff. All five
attempts completed as processes. IG-02 through IG-05 directly read the
appropriate pinned files; no new attempt accessed a judge pack or previous
answer. The attempts ran with runner commit `fcc6154`; the subsequent
commit tightened preflight and documentation without changing the task
invocation. The judge assessed four tasks complete. Search route and source
visibility changed together, and fresh model outputs were produced on a later
date. The score gain cannot be assigned to Copilot search alone.

## Task-level results

Each cell below gives judged quality and completion (`C` complete, `P`
partial). The selected OpenCode cells come from the corrected runs; other
cells remain from the October study.

| IG task | Luna + Pi | Sol + Pi | Luna + OpenCode | Opus + Claude Code |
|---|---:|---:|---:|---:|
| IG-01 — reconcile benchmark scores | 3/P | 3/P | **3/P** | 4/C |
| IG-02 — retried pull-request merge | 5/C | 5/C | **5/C** | 4/C |
| IG-03 — repository runtime requirements | 5/C | 5/C | **5/C** | 4/C |
| IG-04 — Playwright feature support | 4/C | 4/P | **5/C** | 4/C |
| IG-05 — qualification and ranking claims | 5/C | 5/C | **5/C** | 5/C |

IG-01 is the principal remaining failure. The corrected OpenCode answer found
the Vals AI Luna and Sol scores missed in October, but the judge identified
two new critical errors: it included sources and a model variant published
after the cutoff, and attributed a wrong GLM-5.3 value to a linked source.
It took **307 seconds**, with **29 web-search calls and 22 page fetches**.
These judgments and the other critical-error calls need blind human review
before a rollout decision.

| DU task | Luna + Pi | Sol + Pi | Luna + OpenCode | Opus + Claude Code |
|---|---:|---:|---:|---:|
| DU-01 — delete todo API | 5/C | 5/C | **5/C** | 5/C |
| DU-02 — filter todo list | 5/C | 5/C | **5/C** | 5/C |
| DU-03 — reject duplicate assignments | 4/C | 5/C | **5/C** | 4/C |
| DU-04 — hash symlink target | 3/P | 3/P | **5/C** | 2/P |
| DU-05 — reject malformed metadata | 4/C | 5/C | **5/C** | 5/C |

All five corrected OpenCode DU patches passed the frozen focused and
regression checks. DU-04's new check includes a valid-symlink collision case
added after the original run; the other arms' October checks did not include
it, so this row is not a fully matched validation comparison.

| AR task | Luna + Pi | Sol + Pi | Luna + OpenCode | Opus + Claude Code |
|---|---:|---:|---:|---:|
| AR-01 — effect coordination plan | 5/C | 5/C | **5/C** | 5/C |
| AR-02 — research helper recovery plan | 5/C | 5/C | **5/C** | 4/C |
| AR-03 — scheduler recovery plan | 5/C | 4/C | **5/C** | 4/C |
| AR-04 — desktop/backend restart plan | 5/C | 5/C | **5/C** | 4/C |
| AR-05 — runner module refactor | 4/C | 5/C | **4/C** | 4/C |

AR-05's frozen code check passed for every pair. The corrected OpenCode run
lost one quality point because its own tests did not directly exercise
exception-path cleanup. The four plan tasks have no automated implementation
check.

## Decision and limits

**Pilot OpenCode + Luna alongside Pi + Luna.** The corrected OpenCode results
justify testing it as one Copilot-backed agent across all three categories,
not just DU and AR. Keep Claude Code + Opus as a strong comparison arm where
its separate billing is acceptable. Pi + Sol remains the fastest observed
pair at a 44.3-second overall median, but its Copilot credit draw still needs
attributable accounting. OpenCode's 14/15 ties Claude's completion count;
Claude has fewer critical errors and completed IG-01, while OpenCode has
stronger corrected DU and AR outcomes.

This composite selects 45 original Pi and Claude attempts plus 15 corrected
OpenCode attempts from November. The study contains 75 saved agent attempts in
total. It is an exploratory comparison across dates, with only five tasks per
category. The October account-level Copilot screenshot predates the new
OpenCode runs and cannot price them; the search plugin's own Copilot requests
also need attribution. Do not infer credit efficiency from the runner's
provider cost fields. A repeated, same-day cohort, verified per-attempt billing,
and blind human review of critical errors are the next gates for a default
recommendation.

The unchanged [October IG](../results/local-repos-20261015-122649/report.md),
[adjudicated DU](../results/du-2026-10-15-adjudicated/report.md), and
[AR](../results/ar-2026-10-15-full/report.md) reports supply the other arms.
The old OpenCode attempts remain available there for audit.
