# Coding agent evaluation: executive report

**Draft — 15 October 2026.** Information gathering (IG) and defined updates
(DU) have scored results. Architecture (AR) results and the final cross-column
conclusion are **TBD**. The DU figures below use the [adjudicated DU
record](../results/du-2026-10-15-adjudicated/ADJUDICATION.md), which replays
saved attempts and corrects the original evaluation; it is not a second agent
run. Result directories are local and ignored by Git, so they must accompany
this report if it is shared outside this checkout.

## Executive summary

### Questions we tried to answer

1. Which model and harness pairs finish useful work across information
   gathering, well-defined code updates, and open-ended architecture tasks?
2. How do completeness, quality, critical errors, time, intervention, and
   measured usage differ by task type?
3. What changes when the same Luna model runs through Pi versus OpenCode, or
   when Pi uses Sol instead of Luna? How does Claude Code with Opus compare?
4. Which observed differences are large enough to inform an operating choice,
   and which need more tasks or human review?

### Brief approach

We assigned the same five frozen tasks in each column to four model and
harness pairs. Each attempt had a fresh session and the same task-specific
starting commit. We retained agent outputs, code changes, checks, timings, and
usage, then used a fresh blinded Codex judgment for each completed attempt.
DU code was validated against prepared tests in disposable worktrees. The
details of task selection, exclusions, judging, and adjudication follow the
results sections.

### Conclusions and overall results

**Provisional finding.** Across IG and DU, Claude Code + Opus completed 9/10
tasks, Pi + Luna 8/10, Pi + Sol 7/10, and OpenCode + Luna 3/10. Pi + Sol had
the highest mean judge quality score (4.5/5) and was faster than Pi + Luna on
all ten matched tasks, while Pi + Luna completed one more. The same named Luna
model completed five more tasks through Pi than through OpenCode. These are
pair-level observations; different tool and search setups prevent assigning
the entire difference to a model or a single harness feature. AR may change
the final operating conclusion. Five tasks per category are exploratory.

| Model + harness pair | IG: tasks complete; rating | DU: tasks complete; rating | AR: tasks complete; rating | IG+DU complete | IG+DU mean quality / 5 | IG+DU critical errors |
|---|---|---|---|---:|---:|---:|
| GPT-6 Luna + Pi | 4/5; Good | 4/5; Good | **TBD** | 8/10 | 4.3 | 2 |
| GPT-6 Sol + Pi | 3/5; Practical | 4/5; Good | **TBD** | 7/10 | 4.5 | 2 |
| GPT-6 Luna + OpenCode | 1/5; Unacceptable | 2/5; Unacceptable | **TBD** | 3/10 | 3.8 | 2 |
| Claude Opus 5.5 + Claude Code | 5/5; Good | 4/5; Good | **TBD** | 9/10 | 4.2 | 1 |

“Tasks complete” is the judge's deliverable-completion judgment, not merely
an agent process exiting successfully. Mean quality summarizes ten ordinal
scores and is not a calibrated estimate of general ability. Category ratings
apply to five tasks in that category; no pooled IG+DU rating was assigned.

| Task type | Pair | Tasks complete | Quality distribution, scores 1/2/3/4/5 | Median final time | Critical errors | Validated green |
|---|---|---:|---|---:|---:|---:|
| IG | Luna + Pi | 4/5 | 0/0/1/1/3 | 65.0 s | 1 | n/a |
| IG | Sol + Pi | 3/5 | 0/0/1/1/3 | 33.8 s | 1 | n/a |
| IG | Luna + OpenCode | 1/5 | 0/1/0/3/1 | 28.9 s | 1 | n/a |
| IG | Opus + Claude Code | 5/5 | 0/0/0/4/1 | 103.7 s | 0 | n/a |
| DU | Luna + Pi | 4/5 | 0/0/1/2/2 | 63.6 s | 1 | 5/5 |
| DU | Sol + Pi | 4/5 | 0/0/1/0/4 | 40.9 s | 1 | 5/5 |
| DU | Luna + OpenCode | 2/5 | 0/0/1/4/0 | 57.7 s | 1 | 5/5 |
| DU | Opus + Claude Code | 4/5 | 0/1/0/1/3 | 43.8 s | 1 | 4/5 |
| AR | Luna + Pi | **TBD** | **TBD** | **TBD** | **TBD** | task-dependent |
| AR | Sol + Pi | **TBD** | **TBD** | **TBD** | **TBD** | task-dependent |
| AR | Luna + OpenCode | **TBD** | **TBD** | **TBD** | **TBD** | task-dependent |
| AR | Opus + Claude Code | **TBD** | **TBD** | **TBD** | **TBD** | task-dependent |

**Decision to fill after AR and review:** [TBD: recommended pair or deployment
rule by task type, with explicit speed, reliability, and cost tradeoffs].

## Detailed results supporting the summary

### IG: information gathering

Each cell gives **quality score / completion**. `C` means complete and `P`
means partial. All 20 agent attempts finished, but a finished attempt can
still have an incomplete deliverable. The full [IG report](../results/local-repos-20261015-122649/report.md)
links every answer and judgment.

| Task | Luna + Pi | Sol + Pi | Luna + OpenCode | Opus + Claude Code |
|---|---:|---:|---:|---:|
| IG-01 — benchmark evidence matrix | 3/P | 3/P | 2/P | 4/C |
| IG-02 — RelayView merge retry investigation | 5/C | 5/C | 4/P | 4/C |
| IG-03 — runtime requirements | 5/C | 5/C | 4/P | 4/C |
| IG-04 — Playwright capability investigation | 4/C | 4/P | 5/C | 4/C |
| IG-05 — qualification versus comparative claims | 5/C | 5/C | 4/P | 5/C |

IG-01 produced the clearest shared difficulty: three pairs were partial and
each received one critical-error judgment. [TBD: human review of the IG-01
critical-error calls and concise explanation of the exact decision-changing
mistakes.] The Sol + Pi score on IG-04 was 4/5 but its deliverable was judged
partial, illustrating why score and completion are shown separately.

### DU: defined repository updates

Each cell gives **quality score / completion / validation**. `V` means the
prepared green and regression commands passed; `F` means validation failed.
Validation alone did not establish complete behavior: all three non-Opus
DU-04 attempts passed the prepared checks yet were judged partial with a
critical error. The [adjudicated DU report](../results/du-2026-10-15-adjudicated/report.md)
links answers, patches, checks, and judgments.

| Task | Luna + Pi | Sol + Pi | Luna + OpenCode | Opus + Claude Code |
|---|---:|---:|---:|---:|
| DU-01 — delete todo API | 5/C/V | 5/C/V | 4/P/V | 5/C/V |
| DU-02 — filter todo list | 5/C/V | 5/C/V | 4/C/V | 5/C/V |
| DU-03 — reject duplicate repo assignments | 4/C/V | 5/C/V | 4/C/V | 4/C/V |
| DU-04 — symlink target in integrity digest | 3/P/V | 3/P/V | 3/P/V | 2/P/F |
| DU-05 — reject malformed repo facts | 4/C/V | 5/C/V | 4/P/V | 5/C/V |

DU-04 was incomplete for every pair and received all four DU critical-error
judgments. [TBD: summarize the human-reviewed collision failure and any
additional task design change before making an operational recommendation.]
The original DU run and the saved-work adjudication must be kept distinct;
the adjudicated table above is the comparison basis.

### AR: architectural planning and refactoring

The AR run is [in progress](../results/ar-2026-10-15-full/manifest.json) as
this draft is written. Four tasks request plans; AR-05 requests a code
refactor. Fill this table from the completed run, judgment, and report, rather
than treating a saved attempt as a scored result.

| Task | Deliverable | Luna + Pi | Sol + Pi | Luna + OpenCode | Opus + Claude Code |
|---|---|---:|---:|---:|---:|
| AR-01 — PR effect coordinators | Plan | **TBD** | **TBD** | **TBD** | **TBD** |
| AR-02 — research MCP sidecar recovery | Plan | **TBD** | **TBD** | **TBD** | **TBD** |
| AR-03 — Stage A scheduler recovery | Plan | **TBD** | **TBD** | **TBD** | **TBD** |
| AR-04 — desktop/backend run durability | Plan | **TBD** | **TBD** | **TBD** | **TBD** |
| AR-05 — runner workspace/conversation seam | Code | **TBD** | **TBD** | **TBD** | **TBD** |

[TBD: distinguish the four plan outcomes from AR-05's patch and test outcome;
record any timeout, incomplete answer, or judge failure in its own cell.]

### Cross-pair interpretation and remaining measurements

On the ten scored IG+DU prompts, Pi + Luna completed 8 versus OpenCode +
Luna's 3 with the same named model. Pi + Sol completed 7 versus Pi + Luna's 8;
Sol was faster on all ten matched prompts and had two quality wins, eight
ties, and no losses. Claude Code + Opus completed 9, one more than Pi + Luna
and two more than Pi + Sol. These comparisons do not isolate model quality
from harness, tool, or provider effects. [TBD: recompute matched comparisons
over all 15 tasks after AR judgment and human review.]

| Measurement needed for final decision | Current status |
|---|---|
| AR completion, score distribution, critical errors, and timing | **TBD** |
| Blind human review of critical errors and disputed judgments | **TBD** |
| Copilot credits attributable to individual runs | Unavailable in IG and DU |
| Comparable monetary cost across Copilot and Anthropic billing | **TBD**; native usage units differ |
| GUI usability | Outside this evaluation; **TBD** separately |

## Methodology and interpretation notes

### Task and run design

The [task design](repo-task-design.md) specifies five prompts in each of three
columns: IG for evidence gathering, DU for bounded code changes with a known
red/green check, and AR for broader plans or refactoring. The prompts,
starting commits, tool access, and 15-minute agent-attempt limit were frozen
before each run. Each pair received the same task record. IG used read-only
repository exports. DU and AR used disposable detached worktrees at pinned
commits, leaving active source checkouts untouched. DU patches were replayed
with pristine prepared checks in a second worktree. An optional standardized
follow-up was available when an agent asked for clarification. The runner
recorded status, event times, artifacts, tool activity, and native usage.

### Evaluated pairs and exclusions

The evaluated pairs were GPT-6 Luna in Pi, GPT-6 Sol in Pi, GPT-6 Luna in
OpenCode, and Claude Opus 5.5 in Claude Code, all at medium reasoning effort.
The standalone Copilot CLI was excluded because its headless probe could not
use web search; Pi still accessed the Luna and Sol models through the Copilot
provider. Antigravity was excluded from the current four-pair configuration
after command-permission problems in an earlier run and an account quota limit
in the command-allowed follow-up. Its historical results were not pooled with
these runs. [TBD: link a durable exclusion decision record if one is created.]

### Agentic judge and evidence packs

Each finished attempt was judged in a fresh Codex CLI process using
**GPT-6 Sol**, a structured rubric, an anonymized transcript, and a
task-specific judge pack. The judge did not receive the arm name, raw provider
billing fields, or other attempts. For DU and AR, it also received the saved
patch and validation results. Packs record source snapshots or excerpts,
repository facts pinned to commits, acceptable alternatives, required checks,
and decision-changing errors. They were kept out of agent workspaces. The
judge assigned a 1–5 quality score, deliverable completion, critical errors,
and follow-up classification. These are judgments, not direct measurements;
recorded time, command exit status, and validation results are separate
observations. [TBD: add inter-rater or blind human-review results.]

### DU adjudication and comparability

The original DU runner marked five attempts failed because agents edited
prepared tests, despite replayed code passing the frozen checks. The
[adjudication record](../results/du-2026-10-15-adjudicated/ADJUDICATION.md)
recovered those saved attempts for judgment without rerunning agents. An
additional symlink-collision check identified a DU-04 flaw in the Claude Code
patch, leading to a revised judgment. The original run remains available as
an audit trail; this report uses the adjudicated DU results consistently.
Subsequent DU runs should use the same revised check across all pairs.

### Limits

This is an exploratory comparison of five tasks per category, with a single
run per pair and task. Ratings are category summaries under the runner's
precommitted rule, not statistically precise rankings. Scores are ordinal and
judge-dependent; code checks can miss defects. Missing cost or timing fields
mean unavailable, never zero. The final recommendation should follow AR
scoring and blind review of consequential errors.
