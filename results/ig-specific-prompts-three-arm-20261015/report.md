# Agent evaluation: ig-specific-prompts-three-arm-20261015

Information cutoff: 2026-10-14T17:44:35-04:00

Five tasks per arm. Ratings and rankings are exploratory, not statistically conclusive.

## Preflight

| Arm | Status | Reason |
|---|---|---|
| pi-luna | ready | — |
| pi-sol | ready | — |
| claude-opus | ready | — |

## Arm summary

| Arm | Rating | Completed | Quality median | First visible seconds median (range) | First substantive seconds median (range) | Final seconds median (range) | Follow-ups | Critical errors | Copilot credits median (range) |
|---|---|---:|---:|---|---|---|---:|---:|---|
| pi-luna | Practical | 5/5 | 4 | 177.15 (92.58–471.44) | 186.59 (98.72–489.78) | 186.63 (98.75–489.84) | 0 | 0 | unavailable |
| pi-sol | Good | 5/5 | 5 | 148.20 (72.45–215.25) | 150.68 (74.99–228.87) | 150.72 (75.01–228.93) | 0 | 0 | unavailable |
| claude-opus | Unacceptable | 5/5 | 4 | 20.88 (2.34–42.96) | 54.69 (42.96–175.57) | 54.95 (43.21–175.80) | 0 | 4 | separate native usage |

## Task outcomes

### IG-01

| Arm | Status | Quality | Follow-up | Critical errors | Answer | Judgment |
|---|---|---:|---|---:|---|---|
| pi-luna | completed | 4 | useful_but_avoidable | 0 | [answer](runs/IG-01/pi-luna/answer.md) | [judgment](runs/IG-01/pi-luna/judgment.json) |
| pi-sol | completed | 4 | none | 0 | [answer](runs/IG-01/pi-sol/answer.md) | [judgment](runs/IG-01/pi-sol/judgment.json) |
| claude-opus | completed | 4 | useful_but_avoidable | 1 | [answer](runs/IG-01/claude-opus/answer.md) | [judgment](runs/IG-01/claude-opus/judgment.json) |

### IG-02

| Arm | Status | Quality | Follow-up | Critical errors | Answer | Judgment |
|---|---|---:|---|---:|---|---|
| pi-luna | completed | 4 | none | 0 | [answer](runs/IG-02/pi-luna/answer.md) | [judgment](runs/IG-02/pi-luna/judgment.json) |
| pi-sol | completed | 5 | none | 0 | [answer](runs/IG-02/pi-sol/answer.md) | [judgment](runs/IG-02/pi-sol/judgment.json) |
| claude-opus | completed | 4 | none | 1 | [answer](runs/IG-02/claude-opus/answer.md) | [judgment](runs/IG-02/claude-opus/judgment.json) |

### IG-03

| Arm | Status | Quality | Follow-up | Critical errors | Answer | Judgment |
|---|---|---:|---|---:|---|---|
| pi-luna | completed | 5 | none | 0 | [answer](runs/IG-03/pi-luna/answer.md) | [judgment](runs/IG-03/pi-luna/judgment.json) |
| pi-sol | completed | 5 | none | 0 | [answer](runs/IG-03/pi-sol/answer.md) | [judgment](runs/IG-03/pi-sol/judgment.json) |
| claude-opus | completed | 4 | none | 0 | [answer](runs/IG-03/claude-opus/answer.md) | [judgment](runs/IG-03/claude-opus/judgment.json) |

### IG-04

| Arm | Status | Quality | Follow-up | Critical errors | Answer | Judgment |
|---|---|---:|---|---:|---|---|
| pi-luna | completed | 4 | none | 0 | [answer](runs/IG-04/pi-luna/answer.md) | [judgment](runs/IG-04/pi-luna/judgment.json) |
| pi-sol | completed | 4 | none | 0 | [answer](runs/IG-04/pi-sol/answer.md) | [judgment](runs/IG-04/pi-sol/judgment.json) |
| claude-opus | completed | 4 | none | 0 | [answer](runs/IG-04/claude-opus/answer.md) | [judgment](runs/IG-04/claude-opus/judgment.json) |

### IG-05

| Arm | Status | Quality | Follow-up | Critical errors | Answer | Judgment |
|---|---|---:|---|---:|---|---|
| pi-luna | completed | 4 | none | 0 | [answer](runs/IG-05/pi-luna/answer.md) | [judgment](runs/IG-05/pi-luna/judgment.json) |
| pi-sol | completed | 5 | none | 0 | [answer](runs/IG-05/pi-sol/answer.md) | [judgment](runs/IG-05/pi-sol/judgment.json) |
| claude-opus | completed | 3 | unnecessary | 2 | [answer](runs/IG-05/claude-opus/answer.md) | [judgment](runs/IG-05/claude-opus/judgment.json) |

## Sol versus Luna Copilot credits

Unavailable: provider-reported credits are not present for paired Pi runs.

Non-Copilot usage remains in native units in `summary.csv`; it is not converted to Copilot credits.
Copilot values derived from `totalNanoAiu / 1e9` are approximate until reconciled with GitHub billing. See each row's `credit_classification`.

Judge scores are opinions. Times and native usage come from the runner and provider events. A missing value means unavailable, never zero.

Every critical-error judgment should receive blind human review before acting on rankings.
