# Agent evaluation: ig-2026-10-14-antigravity-command-allowed

Information cutoff: 2026-10-14T15:34:07-04:00

Five tasks per arm. Ratings and rankings are exploratory, not statistically conclusive.

## Preflight

| Arm | Status | Reason |
|---|---|---|
| pi-luna | ready | — |
| copilot-luna | unavailable | Search and page fetch were not both observed in headless events |
| pi-sol | ready | — |
| claude-opus | ready | — |
| antigravity-flash | ready | — |

## Arm summary

| Arm | Rating | Completed | Quality median | First visible seconds median (range) | First substantive seconds median (range) | Final seconds median (range) | Follow-ups | Critical errors | Copilot credits median (range) |
|---|---|---:|---:|---|---|---|---:|---:|---|
| pi-luna | Unrated | 0/5 | unavailable | unavailable | unavailable | unavailable | 0 | 0 | unavailable |
| copilot-luna | Unrated | 0/5 | unavailable | unavailable | unavailable | unavailable | 0 | 0 | unavailable |
| pi-sol | Unrated | 0/5 | unavailable | unavailable | unavailable | unavailable | 0 | 0 | unavailable |
| claude-opus | Unrated | 0/5 | unavailable | unavailable | unavailable | unavailable | 0 | 0 | separate native usage |
| antigravity-flash | Unrated | 2/5 | 2.0 | 103.64 (90.59–116.69) | 104.15 (90.64–117.65) | 109.28 (97.03–121.54) | 0 | 5 | separate native usage |

## Task outcomes

### IG-01

| Arm | Status | Quality | Follow-up | Critical errors | Answer | Judgment |
|---|---|---:|---|---:|---|---|
| pi-luna | not_run | — | — | — | — | — |
| copilot-luna | not_run | — | — | — | — | — |
| pi-sol | not_run | — | — | — | — | — |
| claude-opus | not_run | — | — | — | — | — |
| antigravity-flash | completed | 2 | none | 3 | [answer](runs/IG-01/antigravity-flash/answer.md) | [judgment](runs/IG-01/antigravity-flash/judgment.json) |

### IG-02

| Arm | Status | Quality | Follow-up | Critical errors | Answer | Judgment |
|---|---|---:|---|---:|---|---|
| pi-luna | not_run | — | — | — | — | — |
| copilot-luna | not_run | — | — | — | — | — |
| pi-sol | not_run | — | — | — | — | — |
| claude-opus | not_run | — | — | — | — | — |
| antigravity-flash | completed | 2 | necessary | 2 | [answer](runs/IG-02/antigravity-flash/answer.md) | [judgment](runs/IG-02/antigravity-flash/judgment.json) |

### IG-03

| Arm | Status | Quality | Follow-up | Critical errors | Answer | Judgment |
|---|---|---:|---|---:|---|---|
| pi-luna | not_run | — | — | — | — | — |
| copilot-luna | not_run | — | — | — | — | — |
| pi-sol | not_run | — | — | — | — | — |
| claude-opus | not_run | — | — | — | — | — |
| antigravity-flash | failed | — | — | — | [answer](runs/IG-03/antigravity-flash/answer.md) | — |

### IG-04

| Arm | Status | Quality | Follow-up | Critical errors | Answer | Judgment |
|---|---|---:|---|---:|---|---|
| pi-luna | not_run | — | — | — | — | — |
| copilot-luna | not_run | — | — | — | — | — |
| pi-sol | not_run | — | — | — | — | — |
| claude-opus | not_run | — | — | — | — | — |
| antigravity-flash | failed | — | — | — | [answer](runs/IG-04/antigravity-flash/answer.md) | — |

### IG-05

| Arm | Status | Quality | Follow-up | Critical errors | Answer | Judgment |
|---|---|---:|---|---:|---|---|
| pi-luna | not_run | — | — | — | — | — |
| copilot-luna | not_run | — | — | — | — | — |
| pi-sol | not_run | — | — | — | — | — |
| claude-opus | not_run | — | — | — | — | — |
| antigravity-flash | failed | — | — | — | [answer](runs/IG-05/antigravity-flash/answer.md) | — |

## Sol versus Luna Copilot credits

Unavailable: provider-reported credits are not present for paired Pi runs.

Anthropic and Google usage remain in native units in `summary.csv`; they are not converted to Copilot credits.
Copilot values derived from `totalNanoAiu / 1e9` are approximate until reconciled with GitHub billing. See each row's `credit_classification`.

Judge scores are opinions. Times and native usage come from the runner and provider events. A missing value means unavailable, never zero. Antigravity CLI is a headless harness; this report does not measure the desktop app.

Every critical-error judgment should receive blind human review before acting on rankings.
