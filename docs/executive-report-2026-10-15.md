# Coding agent evaluation: executive report

**Draft — 15 October 2026.** All three columns have scored results. Human
review of consequential judgments, comparable cost data, and the final
operating recommendation remain **TBD**. The DU figures below use the [adjudicated DU
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
DU code was validated against prepared tests in disposable worktrees; AR-05
was checked with the runner test suite. Details of task selection, exclusions,
judging, and adjudication follow the results sections.

### Conclusions and overall results

Across the 15 tasks, the strongest result depends on whether completion,
judged quality, or time matters most:

- **Most consistent completion: Claude Code + Opus.** It completed 14/15
  tasks, the most of any pair, and finished at least four of five in every
  column. Pi + Luna was close at 13/15, with Good, Good, and Excellent
  category ratings. These two pairs have the strongest completion records in
  this sample.
- **Highest judged quality: Pi + Sol.** It received 5/5 on 11 of 15 tasks,
  the most of any pair, and its mean quality was 4.60/5. Pi + Luna followed
  with nine 5s and a 4.47 mean. Sol completed 12/15 tasks, so its quality
  lead did not also give it the completion lead. Both Pi pairs had two
  critical-error judgments that still need human review.
- **Fastest overall: Pi + Sol.** Its median final deliverable time was 44.3
  seconds, the lowest of the four pairs. It finished faster than Pi + Luna
  on all 15 matched tasks and faster than Claude Code + Opus on 14/15.
- **Aggregate Copilot credit signal: Sol consumed more.** A user-supplied
  GitHub AI usage screenshot for 1–15 October shows 367.98 credits for
  GPT-6 Sol and 50.32 for GPT-6 Luna, a 7.31× model-level difference. The
  operator reports using this Copilot account only for the evaluations. If
  Luna was used twice as often as Sol, as in the scored matrix, Sol's
  usage-normalized credit intensity was about **14.6×** Luna's. That ratio
  is a rough estimate across tests and probes, not measured credits for any
  pair's individual attempts.
- **Recommended mixed-workload exclusion: OpenCode + Luna.** It completed 8/15
  tasks, including only 1/5 IG and 2/5 DU tasks, and received Unacceptable
  ratings in both columns. It also had the lowest mean quality (3.93/5) and
  only two 5/5 scores. Its 5/5 AR completion and Good AR rating make it a
  plausible candidate for architecture work specifically, pending review.

These are results for model **and** harness pairs. Different tool and search
setups prevent assigning a pair's performance entirely to its model or to a
single harness feature. Five tasks per category and one run per task make the
comparison exploratory.

| Model + harness pair | IG: complete; rating | DU: complete; rating | AR: complete; rating | All complete | 5/5 scores | Mean quality / 5 | Median final time | Critical errors |
|---|---|---|---|---:|---:|---:|---:|---:|
| GPT-6 Luna + Pi | 4/5; Good | 4/5; Good | 5/5; Excellent | 13/15 | 9/15 | 4.47 | 75.7 s | 2 |
| GPT-6 Sol + Pi | 3/5; Practical | 4/5; Good | 5/5; Excellent | 12/15 | 11/15 | 4.60 | 44.3 s | 2 |
| GPT-6 Luna + OpenCode | 1/5; Unacceptable | 2/5; Unacceptable | 5/5; Good | 8/15 | 2/15 | 3.93 | 72.4 s | 2 |
| Claude Opus 5.5 + Claude Code | 5/5; Good | 4/5; Good | 5/5; Good | 14/15 | 5/15 | 4.20 | 102.7 s | 1 |

“Tasks complete” is the judge's deliverable-completion judgment, not merely
an agent process exiting successfully. Mean quality summarizes 15 ordinal
scores and is not a calibrated estimate of general ability. Category ratings
apply to five tasks in that category; no pooled 15-task rating was assigned.

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
| AR | Luna + Pi | 5/5 | 0/0/0/1/4 | 178.9 s | 0 | 1/1 code task |
| AR | Sol + Pi | 5/5 | 0/0/0/1/4 | 103.7 s | 0 | 1/1 code task |
| AR | Luna + OpenCode | 5/5 | 0/0/0/4/1 | 165.0 s | 0 | 1/1 code task |
| AR | Opus + Claude Code | 5/5 | 0/0/0/4/1 | 254.6 s | 0 | 1/1 code task |

**Provisional operating read:** Pi + Sol leads when turnaround and judged
quality are the priorities; Claude Code + Opus leads when the goal is the
highest observed completion rate. Pi + Luna offers nearly the same completion
rate as Opus with more 5/5 judgments. [TBD: final operating choice after
blind human review and cost reconciliation.]

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

All 20 AR attempts finished and were judged complete, with zero critical
errors. Four tasks requested plans; AR-05 requested a code refactor. Each cell
gives **quality score / completion**. `V` on AR-05 also means the runner test
suite passed in a fresh checkout. The full [AR report](../results/ar-2026-10-15-full/report.md)
links each answer, patch, and judgment.

| Task | Deliverable | Luna + Pi | Sol + Pi | Luna + OpenCode | Opus + Claude Code |
|---|---|---:|---:|---:|---:|
| AR-01 — PR effect coordinators | Plan | 5/C | 5/C | 4/C | 5/C |
| AR-02 — research MCP sidecar recovery | Plan | 5/C | 5/C | 5/C | 4/C |
| AR-03 — Stage A scheduler recovery | Plan | 5/C | 4/C | 4/C | 4/C |
| AR-04 — desktop/backend run durability | Plan | 5/C | 5/C | 4/C | 4/C |
| AR-05 — runner workspace/conversation seam | Code | 4/C/V | 5/C/V | 4/C/V | 4/C/V |

Pi + Sol and Pi + Luna had the same score distribution (four 5s and one 4).
Sol's median final time was 103.7 seconds versus Luna's 178.9 seconds, and it
finished faster on each of the five matched AR tasks. Their 4s came on
different tasks. The judge found an unresolved migration step in Sol's AR-03
recovery plan; Luna's AR-05 code change lacked direct tests of cleanup and
failure behavior. OpenCode + Luna completed all five tasks, in contrast with
its lower completion rate in IG and DU. Claude Code + Opus also completed all
five, but had the longest median final time at 254.6 seconds.

All four AR-05 patches passed the configured runner suite in a fresh checkout:
18 tests for Pi + Luna, 18 for Pi + Sol, 17 for OpenCode + Luna, and 20 for
Claude Code + Opus. Counts differ because agents added different tests. The
four planning tasks had no automated pass/fail validation; their scores are
judgments of the proposed plans, not proof that the plans will work when
implemented. [TBD: blind human review of selected AR plans and AR-05 diffs.]

**AR final deliverable time, seconds** (rounded from the runner's measurements):

| Task | Luna + Pi | Sol + Pi | Luna + OpenCode | Opus + Claude Code |
|---|---:|---:|---:|---:|
| AR-01 | 122 | 104 | 84 | 255 |
| AR-02 | 209 | 67 | 94 | 234 |
| AR-03 | 454 | 239 | 217 | 535 |
| AR-04 | 164 | 164 | 165 | 279 |
| AR-05 | 179 | 97 | 171 | 103 |

Sol + Pi was faster than Luna + Pi on AR-04 by about 0.05 seconds; rounding
both to 164 seconds conceals that small difference. The full CSV retains the
unrounded values. First visible event times are not substituted for final
deliverable times because harness event streams differ.

### Cross-pair interpretation and remaining measurements

Across all 15 prompts, Pi + Luna completed 13 versus OpenCode + Luna's 8 with
the same named model. Pi + Sol completed 12 versus Pi + Luna's 13; Sol was
faster on all 15 matched prompts and had three quality wins, eleven ties, and
one loss. Claude Code + Opus completed 14, one more than Pi + Luna and two
more than Pi + Sol. Its greater completion rate did not come with a lead in
mean judge quality or final time. These comparisons do not isolate model
quality from harness, tool, or provider effects. [TBD: revisit matched
comparisons after blind human review.]

| First pair versus second | Column | Quality wins / ties / losses for first pair | First pair faster |
|---|---|---:|---:|
| Sol + Pi vs Luna + Pi | IG | 0 / 5 / 0 | 5/5 |
| Sol + Pi vs Luna + Pi | DU | 2 / 3 / 0 | 5/5 |
| Sol + Pi vs Luna + Pi | AR | 1 / 3 / 1 | 5/5 |
| Sol + Pi vs Opus + Claude Code | IG | 2 / 2 / 1 | 5/5 |
| Sol + Pi vs Opus + Claude Code | DU | 2 / 3 / 0 | 4/5 |
| Sol + Pi vs Opus + Claude Code | AR | 3 / 2 / 0 | 5/5 |
| Luna + Pi vs Luna + OpenCode | IG | 4 / 0 / 1 | 0/5 |
| Luna + Pi vs Luna + OpenCode | DU | 2 / 3 / 0 | 2/5 |
| Luna + Pi vs Luna + OpenCode | AR | 3 / 2 / 0 | 1/5 |

**Account-level Copilot usage, 1–15 October 2026.** The operator supplied a
[GitHub AI usage snapshot](../results/copilot-ai-usage-2026-10-15/README.md)
and confirmed that this Copilot account was used only for these evaluations
in the period. The page showed:

| Model | Included AI credits | Displayed included usage |
|---|---:|---:|
| GPT-6 Sol | 367.98 | $3.68 |
| GPT-6 Luna | 50.32 | $0.50 |

Sol accounted for about 88% of the 418.30 model-attributed credits shown;
its aggregate was 7.31 times Luna's. This includes evaluation activity
beyond the scored attempts, such as live probes and any pilots or reruns.
The scored comparison itself contains 15 Sol + Pi attempts and 30 Luna
attempts split between Pi and OpenCode. Assuming the 2:1 Luna-to-Sol use
ratio also held across all account activity, the usage-normalized comparison
is `(367.98 / 1) / (50.32 / 2) = 14.63`, or about **14.6× more Sol credits
per assumed use**. This is an estimate: the mix of probes, pilots, and reruns
is unknown. The screenshot groups by model, so
it cannot allocate Luna credits between those harnesses or assign credits
to individual tasks. It establishes a strong **directional, model-level**
consumption difference for this account; neither ratio is a measured per-task
price ratio. The
original screenshot and a machine-readable transcription are preserved with
the results.

| Measurement needed for final decision | Current status |
|---|---|
| AR completion, score distribution, critical errors, and timing | Available in the AR report and table above |
| Blind human review of critical errors and disputed judgments | **TBD** |
| Copilot credits attributable to individual runs | Unavailable; an account-level model comparison is available below |
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
The goal was to identify a versatile coding agent setup that can serve all
three task categories, rather than select a different harness for each one.
The standalone Copilot CLI's headless probe could not use web search, a
requirement for the information-gathering category, so it was excluded from
the shared three-category comparison. This is a scope decision, not a measured
result for Copilot CLI on repository updates or architecture work. Pi still
accessed the Luna and Sol models through the Copilot provider. Antigravity was
excluded from the current four-pair configuration
after command-permission problems in an earlier run and an account quota limit
in the command-allowed follow-up. Its historical results were not pooled with
these runs. [TBD: link a durable exclusion decision record if one is created.]

### Web search and page fetch by pair

The pairs had different routes to online evidence. The runner exposed both
search and fetch tools in every column, but equal tool names do not imply
equal search results, page extraction, latency, or source coverage.

| Pair | Web search route | Web fetch route |
|---|---|---|
| GPT-6 Luna + Pi | Installed `pi-web-search` extension sends `web_search` through the configured GitHub Copilot model endpoint. | Installed `pi-web-fetch` extension renders and extracts pages locally and can use the configured Copilot model to process the content. |
| GPT-6 Sol + Pi | Same Pi extension and Copilot route, using the Sol model. | Same Pi fetch extension, using the Sol model when model processing is needed. |
| GPT-6 Luna + OpenCode | OpenCode's `websearch` uses the pinned `tinyfish` hosted search provider, set in a per-process `OPENCODE_CONFIG_CONTENT` configuration. | OpenCode's `webfetch` tool was explicitly allowed in that configuration. |
| Claude Opus 5.5 + Claude Code | Claude Code's built-in `WebSearch` tool was explicitly allowed. | Claude Code's built-in `WebFetch` tool was explicitly allowed. |

OpenCode ran with `--standalone` so its private process inherited the pinned
search configuration instead of a user's background service. The live
preflight for **each pair in IG, DU, and AR** observed both a search and a
page-fetch tool call before admitting the pair. This proves that the tools
were callable in those probe sessions; it does not establish comparable
result quality, indexing, extraction, or reliability on the evaluation
prompts. The difference is especially relevant to IG tasks requiring external
sources, and limits how confidently the Luna-in-Pi versus Luna-in-OpenCode
gap can be attributed to the harness alone. Configuration and probe records
are in the [adapter](../src/agent_eval/adapters.py), [arm
configuration](../config/arms.yaml), and the [IG](../results/local-repos-20261015-122649/manifest.json),
[DU](../results/du-2026-10-15-adjudicated/manifest.json), and
[AR](../results/ar-2026-10-15-full/manifest.json) manifests.

### Copilot credit attribution

The [account screenshot](../results/copilot-ai-usage-2026-10-15/source.png) is
a point-in-time billing view for 1–15 October,
not an export keyed to evaluation IDs. GitHub's [billing report
reference](https://docs.github.com/en/billing/reference/billing-reports)
describes AI usage grouped by date, model, and username. The runner saved
per-attempt token counts and harness-native cost fields, but none of the 45
Copilot-backed scored attempts emitted an AI credit or `totalNanoAiu` field.
Those native cost fields were therefore not converted into Copilot credits.
The screenshot supports the model-level comparison above under the operator's
exclusive-use statement, while per-pair and per-task credit totals remain
unavailable. Live preflight probes also consume model usage and are outside
the scored attempt rows.

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
mean unavailable, never zero. First visible event times are also less
comparable across harnesses than final deliverable times because event streams
differ. The final recommendation should follow blind review of consequential
errors and representative AR plans and code changes.
