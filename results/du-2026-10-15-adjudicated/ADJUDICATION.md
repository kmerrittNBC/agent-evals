# DU adjudication of `du-2026-10-15-full`

The original run is preserved at `../du-2026-10-15-full/`. This directory is a separate adjudication of its saved attempts, not a new agent run. All agent timing and usage values are copied from the original run.

## Method

For each of the five attempts originally rejected for a changed prepared check, I created a detached worktree at the manifest's pinned commit, installed the original frozen check, applied the saved `patch.diff`, and ran the task's configured green and regression commands. All ten command invocations passed, and the frozen checks stayed byte-for-byte intact. These replay commands ran directly in isolated worktrees, rather than through the original Bubblewrap wrapper. Their command outputs are saved as `replay-validation.json` in each run directory and summarized in `adjudication-replays.json`.

The runner had excluded the agent's edits to prepared checks from its patch and untracked archive. I recovered those edited test files from the original event traces and saved them in each run's `recovered-check-edit/` directory. The adjudication judge saw them as separately labeled evidence; they were **not** applied to the pristine-check replay. The copied `changes.json` marks the replayed checks intact and retains `original_setup_checks_intact: false`.

I then invoked the repository's `judge_one` path in a fresh Codex CLI process for each recovered attempt: `gpt-6-sol`, the same output schema, rubric, prompt construction, evidence pack, and 300-second timeout as the original run. The first, superseded judgments made before the recovered test evidence was attached are in `preliminary-judgments/`. All other original judgments were copied unchanged except Claude Opus on DU-04.

For Claude Opus DU-04, a supplemental test retargeted a live symlink from `a` (file content `bc`) to `ab` (file content `c`). Its digest did not change. I added that failing test result to the replay validation and used the same judge path to rejudge this attempt. The original focused and regression commands both passed; only this added collision test failed.

## Changed judgments

| Task | Arm | Original | Adjudicated | Reason |
|---|---|---|---|---|
| DU-01 | Pi Luna | Failed integrity gate | 5/5, complete | The frozen checks pass; the original change was `gofmt` formatting of an unformatted prepared Go test. |
| DU-03 | OpenCode Luna | Failed integrity gate | 4/5, complete | The source patch rejects duplicate names; frozen focused and full suites pass. |
| DU-04 | Pi Luna | Failed integrity gate | 3/5, partial; 1 critical error | Original checks pass, but an unframed symlink target and file content can collide. |
| DU-05 | Pi Luna | Failed integrity gate | 4/5, complete | The source patch handles malformed facts; frozen focused and full suites pass. |
| DU-05 | OpenCode Luna | Failed integrity gate | 4/5, partial | Code and focused coverage address the behavior, but the candidate did not run the requested runner tests. |
| DU-04 | Claude Opus | 4/5, complete | 2/5, partial; 1 critical error | The new collision test disproves the claimed retargeting guarantee. |

## Revised arm ratings

| Arm | Original | Adjudicated | Tasks complete |
|---|---|---|---:|
| Pi Luna | Unrated | Good | 4/5 |
| Pi Sol | Good | Good | 4/5 |
| OpenCode Luna | Unacceptable | Unacceptable | 2/5 |
| Claude Opus | Excellent | Good | 4/5 |

These remain exploratory judge opinions on five tasks per arm. The recovered attempts were graded from archived artifacts, so candidate-authored edits to prepared checks are available as trace-derived evidence rather than ordinary repository patches. The original result files remain the authoritative record of what the runner reported at execution time.
