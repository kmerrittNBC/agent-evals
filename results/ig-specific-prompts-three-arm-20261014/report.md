# Agent evaluation: ig-specific-prompts-three-arm-20261014

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
| pi-luna | Good | 5/5 | 4 | 146.65 (75.47–157.10) | 146.72 (79.05–169.03) | 151.17 (79.07–169.10) | 0 | 1 | unavailable |
| pi-sol | Practical | 5/5 | 4 | 106.26 (65.83–273.84) | 108.60 (68.87–288.78) | 108.65 (68.89–288.85) | 0 | 0 | unavailable |
| claude-opus | Unacceptable | 5/5 | 4 | 54.04 (3.45–59.83) | 54.19 (53.88–307.82) | 54.86 (54.13–308.17) | 0 | 3 | separate native usage |

## Task outcomes

### IG-01

| Arm | Status | Quality | Follow-up | Critical errors | Answer | Judgment |
|---|---|---:|---|---:|---|---|
| pi-luna | completed | 3 | necessary | 1 | [answer](runs/IG-01/pi-luna/answer.md) | [judgment](runs/IG-01/pi-luna/judgment.json) |
| pi-sol | completed | 4 | useful_but_avoidable | 0 | [answer](runs/IG-01/pi-sol/answer.md) | [judgment](runs/IG-01/pi-sol/judgment.json) |
| claude-opus | completed | 4 | none | 0 | [answer](runs/IG-01/claude-opus/answer.md) | [judgment](runs/IG-01/claude-opus/judgment.json) |

### IG-02

| Arm | Status | Quality | Follow-up | Critical errors | Answer | Judgment |
|---|---|---:|---|---:|---|---|
| pi-luna | completed | 4 | none | 0 | [answer](runs/IG-02/pi-luna/answer.md) | [judgment](runs/IG-02/pi-luna/judgment.json) |
| pi-sol | completed | 5 | none | 0 | [answer](runs/IG-02/pi-sol/answer.md) | [judgment](runs/IG-02/pi-sol/judgment.json) |
| claude-opus | completed | 3 | necessary | 1 | [answer](runs/IG-02/claude-opus/answer.md) | [judgment](runs/IG-02/claude-opus/judgment.json) |

### IG-03

| Arm | Status | Quality | Follow-up | Critical errors | Answer | Judgment |
|---|---|---:|---|---:|---|---|
| pi-luna | completed | 5 | none | 0 | [answer](runs/IG-03/pi-luna/answer.md) | [judgment](runs/IG-03/pi-luna/judgment.json) |
| pi-sol | completed | 5 | none | 0 | [answer](runs/IG-03/pi-sol/answer.md) | [judgment](runs/IG-03/pi-sol/judgment.json) |
| claude-opus | completed | 4 | none | 0 | [answer](runs/IG-03/claude-opus/answer.md) | [judgment](runs/IG-03/claude-opus/judgment.json) |

### IG-04

| Arm | Status | Quality | Follow-up | Critical errors | Answer | Judgment |
|---|---|---:|---|---:|---|---|
| pi-luna | completed | 5 | none | 0 | [answer](runs/IG-04/pi-luna/answer.md) | [judgment](runs/IG-04/pi-luna/judgment.json) |
| pi-sol | completed | 4 | useful_but_avoidable | 0 | [answer](runs/IG-04/pi-sol/answer.md) | [judgment](runs/IG-04/pi-sol/judgment.json) |
| claude-opus | completed | 4 | none | 0 | [answer](runs/IG-04/claude-opus/answer.md) | [judgment](runs/IG-04/claude-opus/judgment.json) |

### IG-05

| Arm | Status | Quality | Follow-up | Critical errors | Answer | Judgment |
|---|---|---:|---|---:|---|---|
| pi-luna | completed | 4 | none | 0 | [answer](runs/IG-05/pi-luna/answer.md) | [judgment](runs/IG-05/pi-luna/judgment.json) |
| pi-sol | completed | 4 | none | 0 | [answer](runs/IG-05/pi-sol/answer.md) | [judgment](runs/IG-05/pi-sol/judgment.json) |
| claude-opus | completed | 3 | useful_but_avoidable | 2 | [answer](runs/IG-05/claude-opus/answer.md) | [judgment](runs/IG-05/claude-opus/judgment.json) |

## Sol versus Luna Copilot credits

Unavailable: provider-reported credits are not present for paired Pi runs.

Non-Copilot usage remains in native units in `summary.csv`; it is not converted to Copilot credits.
Copilot values derived from `totalNanoAiu / 1e9` are approximate until reconciled with GitHub billing. See each row's `credit_classification`.

Judge scores are opinions. Times and native usage come from the runner and provider events. A missing value means unavailable, never zero.

Every critical-error judgment should receive blind human review before acting on rankings.
