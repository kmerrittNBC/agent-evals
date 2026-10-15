# Agent evaluation: du-2026-10-15-full

Column: du
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
| DU-01 | ready | 1 | — |
| DU-02 | ready | 1 | — |
| DU-03 | ready | 1 | — |
| DU-04 | ready | 1 | — |
| DU-05 | ready | 1 | — |

## Arm summary

| Arm | Rating | Attempts complete | Tasks complete | Quality distribution (1–5) | Quality median | First visible seconds median (range) | First substantive seconds median (range) | Final seconds median (range) | Follow-ups | Critical errors | Copilot credits median (range) |
|---|---|---:|---:|---|---:|---|---|---|---:|---:|---|
| pi-luna | Unrated | 2/5 | 2/5 | 0/0/0/1/1 | 4.5 | 63.15 (43.63–75.18) | 65.85 (63.56–68.13) | 65.86 (63.58–68.15) | 0 | 0 | unavailable |
| pi-sol | Good | 5/5 | 4/5 | 0/0/1/0/4 | 5 | 26.44 (12.67–39.60) | 26.95 (15.02–40.87) | 40.89 (26.96–44.34) | 0 | 1 | unavailable |
| opencode-luna | Unacceptable | 3/5 | 1/5 | 0/0/1/2/0 | 4 | 3.43 (2.47–30.77) | 29.83 (17.99–31.71) | 72.45 (32.58–92.52) | 0 | 1 | unavailable |
| claude-opus | Excellent | 5/5 | 5/5 | 0/0/0/2/3 | 5 | 14.41 (11.05–31.98) | 29.77 (11.05–43.51) | 43.76 (30.05–58.74) | 0 | 0 | separate native usage |

## Task outcomes

### DU-01

| Arm | Status | Quality | Validation | Follow-up | Critical errors | Answer | Patch | Judgment |
|---|---|---:|---|---|---:|---|---|---|
| pi-luna | failed | — | True | — | — | [answer](runs/DU-01/pi-luna/answer.md) | [patch](runs/DU-01/pi-luna/patch.diff) | — |
| pi-sol | completed | 5 | True | none | 0 | [answer](runs/DU-01/pi-sol/answer.md) | [patch](runs/DU-01/pi-sol/patch.diff) | [judgment](runs/DU-01/pi-sol/judgment.json) |
| opencode-luna | completed | 4 | True | useful_but_avoidable | 0 | [answer](runs/DU-01/opencode-luna/answer.md) | [patch](runs/DU-01/opencode-luna/patch.diff) | [judgment](runs/DU-01/opencode-luna/judgment.json) |
| claude-opus | completed | 5 | True | none | 0 | [answer](runs/DU-01/claude-opus/answer.md) | [patch](runs/DU-01/claude-opus/patch.diff) | [judgment](runs/DU-01/claude-opus/judgment.json) |

### DU-02

| Arm | Status | Quality | Validation | Follow-up | Critical errors | Answer | Patch | Judgment |
|---|---|---:|---|---|---:|---|---|---|
| pi-luna | completed | 5 | True | none | 0 | [answer](runs/DU-02/pi-luna/answer.md) | [patch](runs/DU-02/pi-luna/patch.diff) | [judgment](runs/DU-02/pi-luna/judgment.json) |
| pi-sol | completed | 5 | True | none | 0 | [answer](runs/DU-02/pi-sol/answer.md) | [patch](runs/DU-02/pi-sol/patch.diff) | [judgment](runs/DU-02/pi-sol/judgment.json) |
| opencode-luna | completed | 4 | True | none | 0 | [answer](runs/DU-02/opencode-luna/answer.md) | [patch](runs/DU-02/opencode-luna/patch.diff) | [judgment](runs/DU-02/opencode-luna/judgment.json) |
| claude-opus | completed | 5 | True | none | 0 | [answer](runs/DU-02/claude-opus/answer.md) | [patch](runs/DU-02/claude-opus/patch.diff) | [judgment](runs/DU-02/claude-opus/judgment.json) |

### DU-03

| Arm | Status | Quality | Validation | Follow-up | Critical errors | Answer | Patch | Judgment |
|---|---|---:|---|---|---:|---|---|---|
| pi-luna | completed | 4 | True | none | 0 | [answer](runs/DU-03/pi-luna/answer.md) | [patch](runs/DU-03/pi-luna/patch.diff) | [judgment](runs/DU-03/pi-luna/judgment.json) |
| pi-sol | completed | 5 | True | none | 0 | [answer](runs/DU-03/pi-sol/answer.md) | [patch](runs/DU-03/pi-sol/patch.diff) | [judgment](runs/DU-03/pi-sol/judgment.json) |
| opencode-luna | failed | — | True | — | — | [answer](runs/DU-03/opencode-luna/answer.md) | [patch](runs/DU-03/opencode-luna/patch.diff) | — |
| claude-opus | completed | 4 | True | none | 0 | [answer](runs/DU-03/claude-opus/answer.md) | [patch](runs/DU-03/claude-opus/patch.diff) | [judgment](runs/DU-03/claude-opus/judgment.json) |

### DU-04

| Arm | Status | Quality | Validation | Follow-up | Critical errors | Answer | Patch | Judgment |
|---|---|---:|---|---|---:|---|---|---|
| pi-luna | failed | — | True | — | — | [answer](runs/DU-04/pi-luna/answer.md) | [patch](runs/DU-04/pi-luna/patch.diff) | — |
| pi-sol | completed | 3 | True | necessary | 1 | [answer](runs/DU-04/pi-sol/answer.md) | [patch](runs/DU-04/pi-sol/patch.diff) | [judgment](runs/DU-04/pi-sol/judgment.json) |
| opencode-luna | completed | 3 | True | necessary | 1 | [answer](runs/DU-04/opencode-luna/answer.md) | [patch](runs/DU-04/opencode-luna/patch.diff) | [judgment](runs/DU-04/opencode-luna/judgment.json) |
| claude-opus | completed | 4 | True | none | 0 | [answer](runs/DU-04/claude-opus/answer.md) | [patch](runs/DU-04/claude-opus/patch.diff) | [judgment](runs/DU-04/claude-opus/judgment.json) |

### DU-05

| Arm | Status | Quality | Validation | Follow-up | Critical errors | Answer | Patch | Judgment |
|---|---|---:|---|---|---:|---|---|---|
| pi-luna | failed | — | True | — | — | [answer](runs/DU-05/pi-luna/answer.md) | [patch](runs/DU-05/pi-luna/patch.diff) | — |
| pi-sol | completed | 5 | True | none | 0 | [answer](runs/DU-05/pi-sol/answer.md) | [patch](runs/DU-05/pi-sol/patch.diff) | [judgment](runs/DU-05/pi-sol/judgment.json) |
| opencode-luna | failed | — | True | — | — | [answer](runs/DU-05/opencode-luna/answer.md) | [patch](runs/DU-05/opencode-luna/patch.diff) | — |
| claude-opus | completed | 5 | True | none | 0 | [answer](runs/DU-05/claude-opus/answer.md) | [patch](runs/DU-05/claude-opus/patch.diff) | [judgment](runs/DU-05/claude-opus/judgment.json) |

## Sol versus Luna Copilot credits

Unavailable: provider-reported credits are not present for paired Pi runs.

Non-Copilot usage remains in native units in `summary.csv`; it is not converted to Copilot credits.
Copilot values derived from `totalNanoAiu / 1e9` are approximate until reconciled with GitHub billing. See each row's `credit_classification`.

Judge scores are opinions. Times and native usage come from the runner and provider events. A missing value means unavailable, never zero.

Every critical-error judgment should receive blind human review before acting on rankings.
