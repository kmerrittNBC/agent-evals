# OpenCode shell permission correction — 4 November 2026

For revised cross-pair conclusions, see the
[updated executive report](executive-report-2026-11-04.md).

The October 15 OpenCode V2 runner used a deny-all permission rule followed by
an allow rule for `bash`. OpenCode V2 names its command permission `shell`, so
the allow rule did not match. The saved OpenCode IG, DU, and AR task traces
contain no command tool calls. This was a runner configuration error, not an
observed refusal by the agent to run available checks.

Commit `7ece962` changes the writable permission to `shell` and adds a live
preflight probe that requires a successful shell tool call and its expected
filesystem effect. The Linux preflight recorded `shell_probe_tool_names` as
`["shell"]`. The original attempts and reports remain unchanged.

## OpenCode + GPT-6 Luna reruns

| Category | October 15 result | Shell-enabled November 4 result | Validation in the rerun |
|---|---|---|---|
| Defined updates (DU) | 2/5 complete; Unacceptable; quality 3, 4, 4, 4, 4; one critical error | [5/5 complete; Excellent; five 5/5 scores; no critical errors](../results/du-opencode-shell-20261104/report.md) | All five focused and regression command sets passed; every attempt used `shell`. |
| Architecture (AR) | 5/5 complete; Good; quality 4, 4, 4, 4, 5 | [5/5 complete; Excellent; quality 5, 5, 5, 5, 4](../results/ar-opencode-shell-20261104/report.md) | AR-05's frozen code check passed; every attempt used `shell`. |

The DU-04 frozen check includes the valid-symlink collision case added after
the original run. The new patch frames symlink target bytes and passes that
check. The AR-05 judge gave 4/5 because cleanup on exception paths lacks a
direct regression test, although the frozen suite passed.

The new attempts used the same task prompts, pinned starting commits, model,
reasoning effort, and October 15 information cutoff. Only OpenCode was rerun;
the original other-arm attempts were not repeated on November 4. These are
exploratory five-task samples with fresh model outputs and judgments, so the
score changes cannot be assigned solely to command access. The original
OpenCode DU and AR scores are unsuitable for an operational harness ranking
because the arm lacked a task capability that the runner intended to provide.

IG was intentionally read-only for every arm and received no command
permission. Its earlier OpenCode result is not affected by this writable-task
permission mismatch.
