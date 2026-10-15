# Agent evaluation: ig-2026-10-14-five-arm-v2

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
| pi-luna | Unacceptable | 5/5 | 4 | 100.53 (31.67–733.00) | 104.77 (33.08–734.80) | 104.80 (33.10–734.83) | 0 | 3 | unavailable |
| copilot-luna | Unrated | 0/5 | unavailable | unavailable | unavailable | unavailable | 0 | 0 | unavailable |
| pi-sol | Practical | 5/5 | 4 | 70.98 (67.06–109.29) | 74.50 (68.98–113.83) | 74.51 (69.00–113.85) | 0 | 2 | unavailable |
| claude-opus | Unacceptable | 5/5 | 2 | 36.61 (1.95–48.87) | 48.87 (36.61–58.55) | 49.12 (36.84–58.76) | 0 | 7 | separate native usage |
| antigravity-flash | Unacceptable | 4/5 | 1.5 | 71.20 (19.87–111.40) | 71.66 (20.26–111.58) | 130.61 (54.67–286.62) | 0 | 9 | separate native usage |

## Task outcomes

### IG-01

| Arm | Status | Quality | Follow-up | Critical errors | Answer | Judgment |
|---|---|---:|---|---:|---|---|
| pi-luna | completed | 2 | necessary | 2 | [answer](runs/IG-01/pi-luna/answer.md) | [judgment](runs/IG-01/pi-luna/judgment.json) |
| copilot-luna | unavailable | — | — | — | [answer](runs/IG-01/copilot-luna/answer.md) | — |
| pi-sol | completed | 2 | none | 2 | [answer](runs/IG-01/pi-sol/answer.md) | [judgment](runs/IG-01/pi-sol/judgment.json) |
| claude-opus | completed | 2 | necessary | 2 | [answer](runs/IG-01/claude-opus/answer.md) | [judgment](runs/IG-01/claude-opus/judgment.json) |
| antigravity-flash | completed | 1 | necessary | 3 | [answer](runs/IG-01/antigravity-flash/answer.md) | [judgment](runs/IG-01/antigravity-flash/judgment.json) |

### IG-02

| Arm | Status | Quality | Follow-up | Critical errors | Answer | Judgment |
|---|---|---:|---|---:|---|---|
| pi-luna | completed | 4 | none | 0 | [answer](runs/IG-02/pi-luna/answer.md) | [judgment](runs/IG-02/pi-luna/judgment.json) |
| copilot-luna | unavailable | — | — | — | [answer](runs/IG-02/copilot-luna/answer.md) | — |
| pi-sol | completed | 3 | useful_but_avoidable | 0 | [answer](runs/IG-02/pi-sol/answer.md) | [judgment](runs/IG-02/pi-sol/judgment.json) |
| claude-opus | completed | 2 | necessary | 2 | [answer](runs/IG-02/claude-opus/answer.md) | [judgment](runs/IG-02/claude-opus/judgment.json) |
| antigravity-flash | completed | 2 | necessary | 2 | [answer](runs/IG-02/antigravity-flash/answer.md) | [judgment](runs/IG-02/antigravity-flash/judgment.json) |

### IG-03

| Arm | Status | Quality | Follow-up | Critical errors | Answer | Judgment |
|---|---|---:|---|---:|---|---|
| pi-luna | completed | 2 | necessary | 1 | [answer](runs/IG-03/pi-luna/answer.md) | [judgment](runs/IG-03/pi-luna/judgment.json) |
| copilot-luna | unavailable | — | — | — | [answer](runs/IG-03/copilot-luna/answer.md) | — |
| pi-sol | completed | 4 | useful_but_avoidable | 0 | [answer](runs/IG-03/pi-sol/answer.md) | [judgment](runs/IG-03/pi-sol/judgment.json) |
| claude-opus | completed | 1 | necessary | 2 | [answer](runs/IG-03/claude-opus/answer.md) | [judgment](runs/IG-03/claude-opus/judgment.json) |
| antigravity-flash | failed | — | — | — | [answer](runs/IG-03/antigravity-flash/answer.md) | — |

### IG-04

| Arm | Status | Quality | Follow-up | Critical errors | Answer | Judgment |
|---|---|---:|---|---:|---|---|
| pi-luna | completed | 5 | none | 0 | [answer](runs/IG-04/pi-luna/answer.md) | [judgment](runs/IG-04/pi-luna/judgment.json) |
| copilot-luna | unavailable | — | — | — | [answer](runs/IG-04/copilot-luna/answer.md) | — |
| pi-sol | completed | 5 | none | 0 | [answer](runs/IG-04/pi-sol/answer.md) | [judgment](runs/IG-04/pi-sol/judgment.json) |
| claude-opus | completed | 4 | none | 0 | [answer](runs/IG-04/claude-opus/answer.md) | [judgment](runs/IG-04/claude-opus/judgment.json) |
| antigravity-flash | completed | 1 | necessary | 3 | [answer](runs/IG-04/antigravity-flash/answer.md) | [judgment](runs/IG-04/antigravity-flash/judgment.json) |

### IG-05

| Arm | Status | Quality | Follow-up | Critical errors | Answer | Judgment |
|---|---|---:|---|---:|---|---|
| pi-luna | completed | 5 | none | 0 | [answer](runs/IG-05/pi-luna/answer.md) | [judgment](runs/IG-05/pi-luna/judgment.json) |
| copilot-luna | unavailable | — | — | — | [answer](runs/IG-05/copilot-luna/answer.md) | — |
| pi-sol | completed | 5 | none | 0 | [answer](runs/IG-05/pi-sol/answer.md) | [judgment](runs/IG-05/pi-sol/judgment.json) |
| claude-opus | completed | 4 | none | 1 | [answer](runs/IG-05/claude-opus/answer.md) | [judgment](runs/IG-05/claude-opus/judgment.json) |
| antigravity-flash | completed | 2 | necessary | 1 | [answer](runs/IG-05/antigravity-flash/answer.md) | [judgment](runs/IG-05/antigravity-flash/judgment.json) |

## Sol versus Luna Copilot credits

Unavailable: provider-reported credits are not present for paired Pi runs.

Anthropic and Google usage remain in native units in `summary.csv`; they are not converted to Copilot credits.
Copilot values derived from `totalNanoAiu / 1e9` are approximate until reconciled with GitHub billing. See each row's `credit_classification`.

Judge scores are opinions. Times and native usage come from the runner and provider events. A missing value means unavailable, never zero. Antigravity CLI is a headless harness; this report does not measure the desktop app.

Every critical-error judgment should receive blind human review before acting on rankings.
