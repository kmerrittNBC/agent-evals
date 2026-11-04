# Agent evaluation: ar-opencode-shell-20261104

Column: ar
Information cutoff: 2026-10-15T14:00:00-04:00

Five tasks per arm. Ratings and rankings are exploratory, not statistically conclusive.

## Preflight

| Arm | Status | Reason |
|---|---|---|
| pi-luna | needs_live_probe | — |
| pi-sol | needs_live_probe | — |
| pi-local-qwen | needs_live_probe | — |
| opencode-luna | ready | — |
| claude-opus | needs_live_probe | — |

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
| pi-luna | Unrated | 0/5 | 0/5 | 0/0/0/0/0 | unavailable | unavailable | unavailable | unavailable | 0 | 0 | unavailable |
| pi-sol | Unrated | 0/5 | 0/5 | 0/0/0/0/0 | unavailable | unavailable | unavailable | unavailable | 0 | 0 | unavailable |
| pi-local-qwen | Unrated | 0/5 | 0/5 | 0/0/0/0/0 | unavailable | unavailable | unavailable | unavailable | 0 | 0 | separate native usage |
| opencode-luna | Excellent | 5/5 | 5/5 | 0/0/0/1/4 | 5 | 3.86 (3.68–30.27) | 30.27 (13.61–80.13) | 141.49 (64.48–541.69) | 0 | 0 | unavailable |
| claude-opus | Unrated | 0/5 | 0/5 | 0/0/0/0/0 | unavailable | unavailable | unavailable | unavailable | 0 | 0 | separate native usage |

## Task outcomes

### AR-01

| Arm | Status | Quality | Validation | Follow-up | Critical errors | Answer | Patch | Judgment |
|---|---|---:|---|---|---:|---|---|---|
| pi-luna | not_run | — | — | — | — | — | — | — |
| pi-sol | not_run | — | — | — | — | — | — | — |
| pi-local-qwen | not_run | — | — | — | — | — | — | — |
| opencode-luna | completed | 5 | — | none | 0 | [answer](runs/AR-01/opencode-luna/answer.md) | [patch](runs/AR-01/opencode-luna/patch.diff) | [judgment](runs/AR-01/opencode-luna/judgment.json) |
| claude-opus | not_run | — | — | — | — | — | — | — |

### AR-02

| Arm | Status | Quality | Validation | Follow-up | Critical errors | Answer | Patch | Judgment |
|---|---|---:|---|---|---:|---|---|---|
| pi-luna | not_run | — | — | — | — | — | — | — |
| pi-sol | not_run | — | — | — | — | — | — | — |
| pi-local-qwen | not_run | — | — | — | — | — | — | — |
| opencode-luna | completed | 5 | — | none | 0 | [answer](runs/AR-02/opencode-luna/answer.md) | [patch](runs/AR-02/opencode-luna/patch.diff) | [judgment](runs/AR-02/opencode-luna/judgment.json) |
| claude-opus | not_run | — | — | — | — | — | — | — |

### AR-03

| Arm | Status | Quality | Validation | Follow-up | Critical errors | Answer | Patch | Judgment |
|---|---|---:|---|---|---:|---|---|---|
| pi-luna | not_run | — | — | — | — | — | — | — |
| pi-sol | not_run | — | — | — | — | — | — | — |
| pi-local-qwen | not_run | — | — | — | — | — | — | — |
| opencode-luna | completed | 5 | — | none | 0 | [answer](runs/AR-03/opencode-luna/answer.md) | [patch](runs/AR-03/opencode-luna/patch.diff) | [judgment](runs/AR-03/opencode-luna/judgment.json) |
| claude-opus | not_run | — | — | — | — | — | — | — |

### AR-04

| Arm | Status | Quality | Validation | Follow-up | Critical errors | Answer | Patch | Judgment |
|---|---|---:|---|---|---:|---|---|---|
| pi-luna | not_run | — | — | — | — | — | — | — |
| pi-sol | not_run | — | — | — | — | — | — | — |
| pi-local-qwen | not_run | — | — | — | — | — | — | — |
| opencode-luna | completed | 5 | — | none | 0 | [answer](runs/AR-04/opencode-luna/answer.md) | [patch](runs/AR-04/opencode-luna/patch.diff) | [judgment](runs/AR-04/opencode-luna/judgment.json) |
| claude-opus | not_run | — | — | — | — | — | — | — |

### AR-05

| Arm | Status | Quality | Validation | Follow-up | Critical errors | Answer | Patch | Judgment |
|---|---|---:|---|---|---:|---|---|---|
| pi-luna | not_run | — | — | — | — | — | — | — |
| pi-sol | not_run | — | — | — | — | — | — | — |
| pi-local-qwen | not_run | — | — | — | — | — | — | — |
| opencode-luna | completed | 4 | True | none | 0 | [answer](runs/AR-05/opencode-luna/answer.md) | [patch](runs/AR-05/opencode-luna/patch.diff) | [judgment](runs/AR-05/opencode-luna/judgment.json) |
| claude-opus | not_run | — | — | — | — | — | — | — |

## Sol versus Luna Copilot credits

Unavailable: provider-reported credits are not present for paired Pi runs.

Non-Copilot usage remains in native units in `summary.csv`; it is not converted to Copilot credits.
Copilot values derived from `totalNanoAiu / 1e9` are approximate until reconciled with GitHub billing. See each row's `credit_classification`.

Judge scores are opinions. Times and native usage come from the runner and provider events. A missing value means unavailable, never zero.

Every critical-error judgment should receive blind human review before acting on rankings.
