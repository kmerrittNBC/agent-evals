# Agent evaluation: ig-opencode-copilot-20261104

Column: ig
Information cutoff: 2026-10-15T00:00:00-04:00

Five tasks per arm. Ratings and rankings are exploratory, not statistically conclusive.

## Preflight

| Arm | Status | Reason |
|---|---|---|
| pi-luna | needs_live_probe | — |
| pi-sol | needs_live_probe | — |
| pi-local-qwen | needs_live_probe | — |
| opencode-luna | ready | — |
| claude-opus | needs_live_probe | — |

## Arm summary

| Arm | Rating | Attempts complete | Tasks complete | Quality distribution (1–5) | Quality median | First visible seconds median (range) | First substantive seconds median (range) | Final seconds median (range) | Follow-ups | Critical errors | Copilot credits median (range) |
|---|---|---:|---:|---|---:|---|---|---|---:|---:|---|
| pi-luna | Unrated | 0/5 | 0/5 | 0/0/0/0/0 | unavailable | unavailable | unavailable | unavailable | 0 | 0 | unavailable |
| pi-sol | Unrated | 0/5 | 0/5 | 0/0/0/0/0 | unavailable | unavailable | unavailable | unavailable | 0 | 0 | unavailable |
| pi-local-qwen | Unrated | 0/5 | 0/5 | 0/0/0/0/0 | unavailable | unavailable | unavailable | unavailable | 0 | 0 | separate native usage |
| opencode-luna | Practical | 5/5 | 4/5 | 0/0/1/0/4 | 5 | 93.27 (70.98–306.94) | 93.27 (70.98–306.94) | 93.46 (71.19–307.21) | 0 | 2 | unavailable |
| claude-opus | Unrated | 0/5 | 0/5 | 0/0/0/0/0 | unavailable | unavailable | unavailable | unavailable | 0 | 0 | separate native usage |

## Task outcomes

### IG-01

| Arm | Status | Quality | Validation | Follow-up | Critical errors | Answer | Patch | Judgment |
|---|---|---:|---|---|---:|---|---|---|
| pi-luna | not_run | — | — | — | — | — | — | — |
| pi-sol | not_run | — | — | — | — | — | — | — |
| pi-local-qwen | not_run | — | — | — | — | — | — | — |
| opencode-luna | completed | 3 | — | none | 2 | [answer](runs/IG-01/opencode-luna/answer.md) | — | [judgment](runs/IG-01/opencode-luna/judgment.json) |
| claude-opus | not_run | — | — | — | — | — | — | — |

### IG-02

| Arm | Status | Quality | Validation | Follow-up | Critical errors | Answer | Patch | Judgment |
|---|---|---:|---|---|---:|---|---|---|
| pi-luna | not_run | — | — | — | — | — | — | — |
| pi-sol | not_run | — | — | — | — | — | — | — |
| pi-local-qwen | not_run | — | — | — | — | — | — | — |
| opencode-luna | completed | 5 | — | none | 0 | [answer](runs/IG-02/opencode-luna/answer.md) | — | [judgment](runs/IG-02/opencode-luna/judgment.json) |
| claude-opus | not_run | — | — | — | — | — | — | — |

### IG-03

| Arm | Status | Quality | Validation | Follow-up | Critical errors | Answer | Patch | Judgment |
|---|---|---:|---|---|---:|---|---|---|
| pi-luna | not_run | — | — | — | — | — | — | — |
| pi-sol | not_run | — | — | — | — | — | — | — |
| pi-local-qwen | not_run | — | — | — | — | — | — | — |
| opencode-luna | completed | 5 | — | none | 0 | [answer](runs/IG-03/opencode-luna/answer.md) | — | [judgment](runs/IG-03/opencode-luna/judgment.json) |
| claude-opus | not_run | — | — | — | — | — | — | — |

### IG-04

| Arm | Status | Quality | Validation | Follow-up | Critical errors | Answer | Patch | Judgment |
|---|---|---:|---|---|---:|---|---|---|
| pi-luna | not_run | — | — | — | — | — | — | — |
| pi-sol | not_run | — | — | — | — | — | — | — |
| pi-local-qwen | not_run | — | — | — | — | — | — | — |
| opencode-luna | completed | 5 | — | none | 0 | [answer](runs/IG-04/opencode-luna/answer.md) | — | [judgment](runs/IG-04/opencode-luna/judgment.json) |
| claude-opus | not_run | — | — | — | — | — | — | — |

### IG-05

| Arm | Status | Quality | Validation | Follow-up | Critical errors | Answer | Patch | Judgment |
|---|---|---:|---|---|---:|---|---|---|
| pi-luna | not_run | — | — | — | — | — | — | — |
| pi-sol | not_run | — | — | — | — | — | — | — |
| pi-local-qwen | not_run | — | — | — | — | — | — | — |
| opencode-luna | completed | 5 | — | none | 0 | [answer](runs/IG-05/opencode-luna/answer.md) | — | [judgment](runs/IG-05/opencode-luna/judgment.json) |
| claude-opus | not_run | — | — | — | — | — | — | — |

## Sol versus Luna Copilot credits

Unavailable: provider-reported credits are not present for paired Pi runs.

Non-Copilot usage remains in native units in `summary.csv`; it is not converted to Copilot credits.
Copilot values derived from `totalNanoAiu / 1e9` are approximate until reconciled with GitHub billing. See each row's `credit_classification`.

Judge scores are opinions. Times and native usage come from the runner and provider events. A missing value means unavailable, never zero.

Every critical-error judgment should receive blind human review before acting on rankings.
