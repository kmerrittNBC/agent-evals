# Agent evaluation: local-repos-20261015-122649

Column: ig
Information cutoff: 2026-10-15T00:00:00-04:00

Five tasks per arm. Ratings and rankings are exploratory, not statistically conclusive.

## Preflight

| Arm | Status | Reason |
|---|---|---|
| pi-luna | ready | — |
| pi-sol | ready | — |
| opencode-luna | ready | — |
| claude-opus | ready | — |

## Arm summary

| Arm | Rating | Attempts complete | Tasks complete | Quality distribution (1–5) | Quality median | First visible seconds median (range) | First substantive seconds median (range) | Final seconds median (range) | Follow-ups | Critical errors | Copilot credits median (range) |
|---|---|---:|---:|---|---:|---|---|---|---:|---:|---|
| pi-luna | Good | 5/5 | 4/5 | 0/0/1/1/3 | 5 | 54.93 (36.84–252.85) | 64.96 (41.69–266.86) | 64.98 (41.71–266.92) | 0 | 1 | unavailable |
| pi-sol | Practical | 5/5 | 3/5 | 0/0/1/1/3 | 5 | 25.26 (19.98–197.64) | 33.80 (22.90–213.12) | 33.82 (23.91–213.21) | 0 | 1 | unavailable |
| opencode-luna | Unacceptable | 5/5 | 1/5 | 0/1/0/3/1 | 4 | 3.66 (3.13–73.65) | 28.77 (22.21–73.65) | 28.91 (22.37–73.85) | 0 | 1 | unavailable |
| claude-opus | Good | 5/5 | 5/5 | 0/0/0/4/1 | 4 | 18.98 (1.83–89.24) | 51.55 (20.22–105.16) | 103.69 (86.07–264.26) | 0 | 0 | separate native usage |

## Task outcomes

### IG-01

| Arm | Status | Quality | Validation | Follow-up | Critical errors | Answer | Patch | Judgment |
|---|---|---:|---|---|---:|---|---|---|
| pi-luna | completed | 3 | — | none | 1 | [answer](runs/IG-01/pi-luna/answer.md) | — | [judgment](runs/IG-01/pi-luna/judgment.json) |
| pi-sol | completed | 3 | — | necessary | 1 | [answer](runs/IG-01/pi-sol/answer.md) | — | [judgment](runs/IG-01/pi-sol/judgment.json) |
| opencode-luna | completed | 2 | — | none | 1 | [answer](runs/IG-01/opencode-luna/answer.md) | — | [judgment](runs/IG-01/opencode-luna/judgment.json) |
| claude-opus | completed | 4 | — | none | 0 | [answer](runs/IG-01/claude-opus/answer.md) | — | [judgment](runs/IG-01/claude-opus/judgment.json) |

### IG-02

| Arm | Status | Quality | Validation | Follow-up | Critical errors | Answer | Patch | Judgment |
|---|---|---:|---|---|---:|---|---|---|
| pi-luna | completed | 5 | — | none | 0 | [answer](runs/IG-02/pi-luna/answer.md) | — | [judgment](runs/IG-02/pi-luna/judgment.json) |
| pi-sol | completed | 5 | — | none | 0 | [answer](runs/IG-02/pi-sol/answer.md) | — | [judgment](runs/IG-02/pi-sol/judgment.json) |
| opencode-luna | completed | 4 | — | none | 0 | [answer](runs/IG-02/opencode-luna/answer.md) | — | [judgment](runs/IG-02/opencode-luna/judgment.json) |
| claude-opus | completed | 4 | — | none | 0 | [answer](runs/IG-02/claude-opus/answer.md) | — | [judgment](runs/IG-02/claude-opus/judgment.json) |

### IG-03

| Arm | Status | Quality | Validation | Follow-up | Critical errors | Answer | Patch | Judgment |
|---|---|---:|---|---|---:|---|---|---|
| pi-luna | completed | 5 | — | none | 0 | [answer](runs/IG-03/pi-luna/answer.md) | — | [judgment](runs/IG-03/pi-luna/judgment.json) |
| pi-sol | completed | 5 | — | none | 0 | [answer](runs/IG-03/pi-sol/answer.md) | — | [judgment](runs/IG-03/pi-sol/judgment.json) |
| opencode-luna | completed | 4 | — | useful_but_avoidable | 0 | [answer](runs/IG-03/opencode-luna/answer.md) | — | [judgment](runs/IG-03/opencode-luna/judgment.json) |
| claude-opus | completed | 4 | — | none | 0 | [answer](runs/IG-03/claude-opus/answer.md) | — | [judgment](runs/IG-03/claude-opus/judgment.json) |

### IG-04

| Arm | Status | Quality | Validation | Follow-up | Critical errors | Answer | Patch | Judgment |
|---|---|---:|---|---|---:|---|---|---|
| pi-luna | completed | 4 | — | none | 0 | [answer](runs/IG-04/pi-luna/answer.md) | — | [judgment](runs/IG-04/pi-luna/judgment.json) |
| pi-sol | completed | 4 | — | none | 0 | [answer](runs/IG-04/pi-sol/answer.md) | — | [judgment](runs/IG-04/pi-sol/judgment.json) |
| opencode-luna | completed | 5 | — | none | 0 | [answer](runs/IG-04/opencode-luna/answer.md) | — | [judgment](runs/IG-04/opencode-luna/judgment.json) |
| claude-opus | completed | 4 | — | none | 0 | [answer](runs/IG-04/claude-opus/answer.md) | — | [judgment](runs/IG-04/claude-opus/judgment.json) |

### IG-05

| Arm | Status | Quality | Validation | Follow-up | Critical errors | Answer | Patch | Judgment |
|---|---|---:|---|---|---:|---|---|---|
| pi-luna | completed | 5 | — | none | 0 | [answer](runs/IG-05/pi-luna/answer.md) | — | [judgment](runs/IG-05/pi-luna/judgment.json) |
| pi-sol | completed | 5 | — | none | 0 | [answer](runs/IG-05/pi-sol/answer.md) | — | [judgment](runs/IG-05/pi-sol/judgment.json) |
| opencode-luna | completed | 4 | — | necessary | 0 | [answer](runs/IG-05/opencode-luna/answer.md) | — | [judgment](runs/IG-05/opencode-luna/judgment.json) |
| claude-opus | completed | 5 | — | none | 0 | [answer](runs/IG-05/claude-opus/answer.md) | — | [judgment](runs/IG-05/claude-opus/judgment.json) |

## Sol versus Luna Copilot credits

Unavailable: provider-reported credits are not present for paired Pi runs.

Non-Copilot usage remains in native units in `summary.csv`; it is not converted to Copilot credits.
Copilot values derived from `totalNanoAiu / 1e9` are approximate until reconciled with GitHub billing. See each row's `credit_classification`.

Judge scores are opinions. Times and native usage come from the runner and provider events. A missing value means unavailable, never zero.

Every critical-error judgment should receive blind human review before acting on rankings.
