# Agent evaluation: ar-2026-10-15-full

Column: ar
Information cutoff: 2026-10-15T14:00:00-04:00

Five tasks per arm. Ratings and rankings are exploratory, not statistically conclusive.

## Preflight

| Arm | Status | Reason |
|---|---|---|
| pi-luna | ready | — |
| pi-sol | ready | — |
| opencode-luna | ready | — |
| claude-opus | ready | — |

## Task preparation

| Task | Status | Red exit | Reason |
|---|---|---:|---|
| AR-01 | ready | — | — |
| AR-02 | ready | — | — |
| AR-03 | ready | — | — |
| AR-04 | ready | — | — |
| AR-05 | ready | — | — |

Validation runs the saved candidate changes in a fresh checkout with frozen prepared checks. Agent edits to those checks are archived separately and do not replace the evaluator's checks.

## Arm summary

| Arm | Rating | Attempts complete | Tasks complete | Quality distribution (1–5) | Quality median | First visible seconds median (range) | First substantive seconds median (range) | Final seconds median (range) | Follow-ups | Critical errors | Copilot credits median (range) |
|---|---|---:|---:|---|---:|---|---|---|---:|---:|---|
| pi-luna | Excellent | 5/5 | 5/5 | 0/0/0/1/4 | 5 | 176.44 (110.12–433.83) | 178.88 (122.45–454.06) | 178.91 (122.46–454.08) | 0 | 0 | unavailable |
| pi-sol | Excellent | 5/5 | 5/5 | 0/0/0/1/4 | 5 | 95.51 (27.96–237.16) | 103.72 (66.52–239.13) | 103.74 (66.54–239.15) | 0 | 0 | unavailable |
| opencode-luna | Good | 5/5 | 5/5 | 0/0/0/4/1 | 4 | 3.59 (2.88–15.29) | 23.22 (12.03–27.82) | 164.98 (84.34–217.42) | 0 | 0 | unavailable |
| claude-opus | Good | 5/5 | 5/5 | 0/0/0/4/1 | 4 | 2.14 (1.64–19.60) | 45.64 (23.96–233.99) | 254.58 (102.73–534.81) | 0 | 0 | separate native usage |

## Task outcomes

### AR-01

| Arm | Status | Quality | Validation | Follow-up | Critical errors | Answer | Patch | Judgment |
|---|---|---:|---|---|---:|---|---|---|
| pi-luna | completed | 5 | — | none | 0 | [answer](runs/AR-01/pi-luna/answer.md) | [patch](runs/AR-01/pi-luna/patch.diff) | [judgment](runs/AR-01/pi-luna/judgment.json) |
| pi-sol | completed | 5 | — | none | 0 | [answer](runs/AR-01/pi-sol/answer.md) | [patch](runs/AR-01/pi-sol/patch.diff) | [judgment](runs/AR-01/pi-sol/judgment.json) |
| opencode-luna | completed | 4 | — | none | 0 | [answer](runs/AR-01/opencode-luna/answer.md) | [patch](runs/AR-01/opencode-luna/patch.diff) | [judgment](runs/AR-01/opencode-luna/judgment.json) |
| claude-opus | completed | 5 | — | none | 0 | [answer](runs/AR-01/claude-opus/answer.md) | [patch](runs/AR-01/claude-opus/patch.diff) | [judgment](runs/AR-01/claude-opus/judgment.json) |

### AR-02

| Arm | Status | Quality | Validation | Follow-up | Critical errors | Answer | Patch | Judgment |
|---|---|---:|---|---|---:|---|---|---|
| pi-luna | completed | 5 | — | none | 0 | [answer](runs/AR-02/pi-luna/answer.md) | [patch](runs/AR-02/pi-luna/patch.diff) | [judgment](runs/AR-02/pi-luna/judgment.json) |
| pi-sol | completed | 5 | — | none | 0 | [answer](runs/AR-02/pi-sol/answer.md) | [patch](runs/AR-02/pi-sol/patch.diff) | [judgment](runs/AR-02/pi-sol/judgment.json) |
| opencode-luna | completed | 5 | — | none | 0 | [answer](runs/AR-02/opencode-luna/answer.md) | [patch](runs/AR-02/opencode-luna/patch.diff) | [judgment](runs/AR-02/opencode-luna/judgment.json) |
| claude-opus | completed | 4 | — | none | 0 | [answer](runs/AR-02/claude-opus/answer.md) | [patch](runs/AR-02/claude-opus/patch.diff) | [judgment](runs/AR-02/claude-opus/judgment.json) |

### AR-03

| Arm | Status | Quality | Validation | Follow-up | Critical errors | Answer | Patch | Judgment |
|---|---|---:|---|---|---:|---|---|---|
| pi-luna | completed | 5 | — | none | 0 | [answer](runs/AR-03/pi-luna/answer.md) | [patch](runs/AR-03/pi-luna/patch.diff) | [judgment](runs/AR-03/pi-luna/judgment.json) |
| pi-sol | completed | 4 | — | none | 0 | [answer](runs/AR-03/pi-sol/answer.md) | [patch](runs/AR-03/pi-sol/patch.diff) | [judgment](runs/AR-03/pi-sol/judgment.json) |
| opencode-luna | completed | 4 | — | none | 0 | [answer](runs/AR-03/opencode-luna/answer.md) | [patch](runs/AR-03/opencode-luna/patch.diff) | [judgment](runs/AR-03/opencode-luna/judgment.json) |
| claude-opus | completed | 4 | — | useful_but_avoidable | 0 | [answer](runs/AR-03/claude-opus/answer.md) | [patch](runs/AR-03/claude-opus/patch.diff) | [judgment](runs/AR-03/claude-opus/judgment.json) |

### AR-04

| Arm | Status | Quality | Validation | Follow-up | Critical errors | Answer | Patch | Judgment |
|---|---|---:|---|---|---:|---|---|---|
| pi-luna | completed | 5 | — | none | 0 | [answer](runs/AR-04/pi-luna/answer.md) | [patch](runs/AR-04/pi-luna/patch.diff) | [judgment](runs/AR-04/pi-luna/judgment.json) |
| pi-sol | completed | 5 | — | none | 0 | [answer](runs/AR-04/pi-sol/answer.md) | [patch](runs/AR-04/pi-sol/patch.diff) | [judgment](runs/AR-04/pi-sol/judgment.json) |
| opencode-luna | completed | 4 | — | none | 0 | [answer](runs/AR-04/opencode-luna/answer.md) | [patch](runs/AR-04/opencode-luna/patch.diff) | [judgment](runs/AR-04/opencode-luna/judgment.json) |
| claude-opus | completed | 4 | — | useful_but_avoidable | 0 | [answer](runs/AR-04/claude-opus/answer.md) | [patch](runs/AR-04/claude-opus/patch.diff) | [judgment](runs/AR-04/claude-opus/judgment.json) |

### AR-05

| Arm | Status | Quality | Validation | Follow-up | Critical errors | Answer | Patch | Judgment |
|---|---|---:|---|---|---:|---|---|---|
| pi-luna | completed | 4 | True | useful_but_avoidable | 0 | [answer](runs/AR-05/pi-luna/answer.md) | [patch](runs/AR-05/pi-luna/patch.diff) | [judgment](runs/AR-05/pi-luna/judgment.json) |
| pi-sol | completed | 5 | True | none | 0 | [answer](runs/AR-05/pi-sol/answer.md) | [patch](runs/AR-05/pi-sol/patch.diff) | [judgment](runs/AR-05/pi-sol/judgment.json) |
| opencode-luna | completed | 4 | True | none | 0 | [answer](runs/AR-05/opencode-luna/answer.md) | [patch](runs/AR-05/opencode-luna/patch.diff) | [judgment](runs/AR-05/opencode-luna/judgment.json) |
| claude-opus | completed | 4 | True | none | 0 | [answer](runs/AR-05/claude-opus/answer.md) | [patch](runs/AR-05/claude-opus/patch.diff) | [judgment](runs/AR-05/claude-opus/judgment.json) |

## Sol versus Luna Copilot credits

Unavailable: provider-reported credits are not present for paired Pi runs.

Non-Copilot usage remains in native units in `summary.csv`; it is not converted to Copilot credits.
Copilot values derived from `totalNanoAiu / 1e9` are approximate until reconciled with GitHub billing. See each row's `credit_classification`.

Judge scores are opinions. Times and native usage come from the runner and provider events. A missing value means unavailable, never zero.

Every critical-error judgment should receive blind human review before acting on rankings.
