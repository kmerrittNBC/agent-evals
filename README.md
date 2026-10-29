# Coding agent capability evaluation

This repository compares **model plus harness pairs** on the work a development team might assign an agent. It evaluates three task categories:

| Category | What the agent does | Tasks |
|---|---|---:|
| Information gathering (IG) | Researches several sources or pinned repositories and synthesizes an answer. | 5 |
| Defined repository updates (DU) | Changes code against a prepared failing check and nearby regression checks. | 5 |
| Architectural planning and refactoring (AR) | Produces a concrete implementation plan (four tasks) or makes a bounded refactor (one task). | 5 |

The original comparison used **Pi + GPT-6 Luna**, **Pi + GPT-6 Sol**, **OpenCode + GPT-6 Luna**, and **Claude Code + Opus 5.5**: **15 tasks × 4 pairs = 60 initial attempts**. The additional `pi-local-qwen` arm supports a separate pilot. Each pair receives the same prompt and repository revision for a task, in a fresh session with a 15-minute limit. The study measures those first attempts; it does not measure improvement after follow-up prompts or graphical-interface usability.

The runner saves each answer, agent events, timing, code changes, available usage fields, and code-check results. A separate GPT-6 Sol judge scores each completed attempt in a fresh context without the pair's identity or other attempts. The report separates measured time and check results from judged quality, completion, critical errors, and whether clarification would have helped. Copilot credits per attempt are unavailable unless an attributable billing record is supplied; the [executive report](docs/executive-report-2026-10-15.md) discusses the account-level Sol/Luna usage comparison and its limits.

### Local Qwen IG-01 pilot

The optional `pi-local-qwen` arm uses Pi with `omlx-local/Qwen3.8-27B-oQ6e-mtp` for the task. Its `pi-web-search` extension uses Copilot Luna as a dedicated search model, so searches consume Copilot usage; `pi-web-fetch` fetches pages locally. The local oMLX server must be running on port 8001 with the 6-bit checkpoint installed. This pilot has its own result ID and does not change the earlier comparisons.

```sh
python3 scripts/configure_pi_local_ig.py
../local-llm-setup/scripts/start_ssd_100k_8gb_36g.sh  # keep running in another terminal
python3 -m agent_eval preflight --column ig --evaluation-id ig-local-qwen-pilot \
  --cutoff 2026-10-15T00:00:00-04:00 --live --arm pi-local-qwen
python3 -m agent_eval run --evaluation-id ig-local-qwen-pilot --task IG-01 --arm pi-local-qwen
```

`configure_pi_local_ig.py` pins both Pi extensions, selects local Qwen for new Pi sessions, and writes `~/.pi/agent/web-search.json` for Copilot Luna search. It backs up Pi settings before changes and refuses to replace a different existing search-model choice. The preflight must observe both web tool calls before the task can run. The default 15-minute task limit still applies; an incomplete local run remains an observed outcome.

**Read the results:** [Executive report](docs/executive-report-2026-10-15.md) · [IG run](results/local-repos-20261015-122649/report.md) · [adjudicated DU run](results/du-2026-10-15-adjudicated/report.md) · [AR run](results/ar-2026-10-15-full/report.md). The [task-design criteria](docs/repo-task-design.md) explain what each category is meant to represent. Earlier pilots and excluded-arm probes remain under `results/`; do not pool their scores with these three runs.

## Run all 15 tasks

Run the commands below from this repository's root. **Use three new evaluation IDs**, one per category: `--full` runs five tasks against all four configured pairs, or 20 slots per ID. Replace the example absolute repository paths with your local checkouts. The checkouts must contain the frozen commits named in the DU and AR task files; they do not need to be checked out at those commits. IG pins the source checkouts' current `HEAD`, which must agree with its judge packs. Choose a timezone-qualified information cutoff appropriate to the evidence you will judge.

```sh
RELAYVIEW_REPO=/absolute/path/to/relayview
HARNESS_EVALS_REPO=/absolute/path/to/agent-harness-evals
TODOS_REPO=/absolute/path/to/lit-go-todos
DATA_ANALYSIS_REPO=/absolute/path/to/data-analysis-agent
AGENT_EVALS_REPO="$PWD"
CUTOFF=2026-10-15T00:00:00-04:00
IG_ID=ig-new-run
DU_ID=du-new-run
AR_ID=ar-new-run
```

For each category, the first `preflight` records task and repository pins. The second runs live model, search/fetch, writable-tool (DU/AR), and judge probes. Inspect its reported arm, task, evidence, and judge statuses before starting `run --full`. Live probes consume model usage. Use a different ID if you repeat a run; an existing attempt cannot be overwritten.

### 1. Information gathering: IG-01 through IG-05

```sh
python3 -m agent_eval preflight --column ig --evaluation-id "$IG_ID" --cutoff "$CUTOFF" \
  --repo "relayview=$RELAYVIEW_REPO" \
  --repo "agent-harness-evals=$HARNESS_EVALS_REPO"
python3 -m agent_eval preflight --column ig --evaluation-id "$IG_ID" --live
python3 -m agent_eval run --evaluation-id "$IG_ID" --full
python3 -m agent_eval judge --evaluation-id "$IG_ID"
python3 -m agent_eval report --evaluation-id "$IG_ID"
```

### 2. Defined repository updates: DU-01 through DU-05

```sh
python3 -m agent_eval preflight --column du --evaluation-id "$DU_ID" --cutoff "$CUTOFF" \
  --repo "lit-go-todos=$TODOS_REPO" \
  --repo "agent-evals=$AGENT_EVALS_REPO"
python3 -m agent_eval preflight --column du --evaluation-id "$DU_ID" --live
python3 -m agent_eval run --evaluation-id "$DU_ID" --full
python3 -m agent_eval judge --evaluation-id "$DU_ID"
python3 -m agent_eval report --evaluation-id "$DU_ID"
```

### 3. Architectural planning and refactoring: AR-01 through AR-05

```sh
python3 -m agent_eval preflight --column ar --evaluation-id "$AR_ID" --cutoff "$CUTOFF" \
  --repo "relayview=$RELAYVIEW_REPO" \
  --repo "agent-harness-evals=$HARNESS_EVALS_REPO" \
  --repo "data-analysis-agent=$DATA_ANALYSIS_REPO" \
  --repo "agent-evals=$AGENT_EVALS_REPO"
python3 -m agent_eval preflight --column ar --evaluation-id "$AR_ID" --live
python3 -m agent_eval run --evaluation-id "$AR_ID" --full
python3 -m agent_eval judge --evaluation-id "$AR_ID"
python3 -m agent_eval report --evaluation-id "$AR_ID"
```

Each report is written to `results/ID/report.md`, with a CSV summary, manifest, run plan, and per-attempt artifacts under `results/ID/`. To try one slot before a full run, use a **separate pilot ID** and filter by both task and pair, for example `python3 -m agent_eval run --evaluation-id ig-pilot --task IG-01 --arm pi-luna` after preflighting that ID. Do not reuse the pilot ID for `--full`.

## Requirements and run behavior

- Python 3.11 or newer and Git. The Python runner uses the standard library; repository-specific checks also need their declared toolchains and dependencies (for example, Go for the todo API tasks).
- Authenticated `pi`, `opencode`, `claude`, and `codex` CLIs with access to the exact models in [`config/arms.yaml`](config/arms.yaml). The judge uses `codex exec` with GPT-6 Sol. [`SETUP_AGENT_PROMPT.md`](SETUP_AGENT_PROMPT.md) is a separate installation/sign-in handoff prompt.
- **Linux with Bubblewrap (`bwrap`) for DU and AR.** Their writable agent processes run in disposable Git worktrees behind a Bubblewrap boundary. The current runner marks those arms unavailable when `bwrap` is missing; a macOS host cannot complete the DU/AR commands above as written. IG uses read-only repository exports and does not require `bwrap`.
- Complete judge-only [`evidence/IG-*`, `evidence/DU-*`, and `evidence/AR-*`](evidence/README.md) packs. The runner checks them against pinned commits and refuses changed packs after live preflight. Keep source excerpts and timestamps consistent with the chosen cutoff.
- Working web search and page fetch for each headless agent. Pi uses `pi-web-search` through GitHub Copilot and `pi-web-fetch`; OpenCode uses its pinned `tinyfish` search route and `webfetch`; Claude Code uses `WebSearch` and `WebFetch`. The live probe verifies that both tools were actually called. The standalone Copilot CLI and Antigravity CLI are not among the current four pairs; the executive report explains their exclusion.

DU and AR use detached worktrees at their frozen commits, leaving active checkouts untouched. DU preflight confirms that the prepared check is red. After each code attempt, the runner replays the saved patch in another clean worktree and runs the prepared and regression checks with pristine evaluator files. It saves patches, untracked files, prepared-check edits, check results, events, answers, and metrics before removing the worktrees. Bubblewrap protects the active project tree from agent writes; it is not a general isolation boundary for all home-directory files. IG exports pinned repository trees read-only. Uncommitted changes in a source checkout are not exported.

The runner records unavailable and failed slots instead of substituting a different model. The blinded judge sees a task-specific evidence pack and the saved answer; for code tasks it also sees the patch and validation results. The judge does not receive the pair name, raw billing fields, or other attempts. Review repository access and sensitive content before publishing evidence packs or run artifacts.

For an isolated Copilot run with an attributable GitHub billing record, see `python3 -m agent_eval reconcile-credits --help`. A matching credit record can be attached to that single task/pair; account-level usage alone cannot assign credits to individual attempts. The task files under `config/` use JSON syntax valid as YAML, so no YAML package is required. Run `python3 -m agent_eval --help` for the complete CLI command list.
