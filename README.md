# Coding agent capability evaluation

The three columns are information gathering (IG), defined repository updates
(DU), and architectural planning/refactoring (AR). The task criteria are in
[`docs/repo-task-design.md`](docs/repo-task-design.md). IG remains in
`config/tasks.yaml`; the two new columns are in
`config/defined-updates.yaml` and `config/architecture.yaml`.

This repository runs the five prompts in `config/tasks.yaml` through four pinned
model/harness arms. It keeps the agent transcript, a fresh blinded Codex
judgment, and a traceable report for every attempted run. The first full run is
in [`results/ig-2026-10-14-five-arm-v2/report.md`](results/ig-2026-10-14-five-arm-v2/report.md)
(local, ignored by Git). It used the earlier, broader prompts and evidence
packs. Its scores should not be pooled with runs of the current prompts. It
attempted all 25 slots; unavailable and failed slots remain visible in the
report. Use a new evaluation ID for the current five prompts.

A separate [Antigravity command-permission follow-up](results/ig-2026-10-14-antigravity-command-allowed/report.md)
completed IG-01 and IG-02 after explicitly allowing commands in its sandbox.
The remaining three tasks hit the account's individual quota and are recorded
as failures. These follow-up results are not pooled with the first run.
Antigravity is inactive in the current configuration; its adapter and historical
results remain available if it is added back later.

## Repository task columns

DU has five code tasks: two Go todo API changes and three runner validation or
integrity fixes. Each has a prepared test that fails at the frozen commit, an
exact red/green command, and a nearby regression command. AR has five tasks
across RelayView, agent-harness-evals, data-analysis-agent, and this runner:
four request a concrete architecture plan and one requests a bounded code
refactor. Each task record freezes its prompt, deliverable, commit, tools,
time limit, setup and acceptance context. Judge packs are under
`evidence/DU-*/` and `evidence/AR-*/`.
The verified red and green exit codes are recorded in
`checks/baseline-results.json`; reference patches are not stored.

Use a fresh evaluation ID for each column. For example, DU:

```sh
python3 -m agent_eval preflight --column du --evaluation-id du-pilot \
  --cutoff 2026-10-15T00:00:00-04:00 \
  --repo lit-go-todos=/home/anodyine/Projects/lit-go-todos \
  --repo agent-evals=/home/anodyine/Projects/agent-evals
python3 -m agent_eval preflight --column du --evaluation-id du-pilot --live
python3 -m agent_eval run --evaluation-id du-pilot --arm pi-luna --task DU-01
python3 -m agent_eval judge --evaluation-id du-pilot --arm pi-luna --task DU-01
python3 -m agent_eval report --evaluation-id du-pilot
```

For AR, pass `--column ar` and `--repo` assignments for `relayview`,
`agent-harness-evals`, `data-analysis-agent`, and `agent-evals`. A full
column run uses `run --evaluation-id ID --full` after live preflight; it has
20 arm/task slots. Do not reuse a pilot ID for a full run. The existing IG
manifests and five IG prompts remain valid and separate.

DU and AR tasks use a fresh detached Git worktree at the task's frozen commit,
even if the source checkout has uncommitted work or has advanced to a newer
HEAD. The runner never checks out or resets the active source tree. It copies
prepared DU checks into the disposable worktree, runs the frozen red command
before live work, grants editing tools for these columns, and runs green and
regression checks after each attempt in a second detached worktree. It replays
the saved code patch there with pristine prepared checks, so formatting or
editing a prepared check cannot change the evaluator's tests. It saves the
patch, untracked files, separately archived prepared-check edits, replayed
check results, events, answer and metrics under `results/ID/runs/` before
removing the worktrees. The judge sees the task pack, answer, code patch,
candidate test edits and pristine-check results in a fresh blinded process.
Bubblewrap is required for these columns: agent
processes see the active project tree read-only, the disposable worktree and
run output writable, and their normal home for CLI authentication. The live
probe verifies file-writing access inside that boundary. This protects active
project checkouts from writes by the agent process; it is not a general
container isolation boundary for other writable home files.

## Requirements

- Python 3.11 or newer; no Python packages are required.
- The CLIs in `config/arms.yaml`, authenticated for the exact models.
- Pinned Git checkouts of RelayView and agent-harness-evals for IG-02 through
  IG-05. The runner exports the commits into temporary read-only directories.
- Completed judge-only packs in `evidence/IG-*/pack.json`. See the template and
  `evidence/README.md`. These are intentionally absent from agent workspaces.
- A confirmed information cutoff (`--cutoff`, ISO 8601 with timezone).

Run `python3 -m agent_eval --help` for commands. A typical sequence is:

```sh
python3 -m agent_eval preflight --evaluation-id pilot --cutoff 2026-10-15T00:00:00-04:00 \
  --repo relayview=/home/anodyine/Projects/relayview \
  --repo agent-harness-evals=/home/anodyine/Projects/agent-harness-evals
python3 -m agent_eval preflight --evaluation-id pilot --live
python3 -m agent_eval run --evaluation-id pilot --full
python3 -m agent_eval judge --evaluation-id pilot
python3 -m agent_eval report --evaluation-id pilot
```

If you need help with CLI installation or sign-in,
give a separate agent the prompt in
[`SETUP_AGENT_PROMPT.md`](SETUP_AGENT_PROMPT.md). It requests no evaluation run.

Pi's installed `pi-web-search` extension is configured with the
`github-copilot` provider and sends a native `web_search` request through the
Copilot model endpoint. Pi's `pi-web-fetch` extension renders and extracts
pages locally, then can use the configured Copilot model to process their
contents. The standalone Copilot CLI arm was removed after its headless probe
could not use web search. Pi still uses the Copilot-backed Luna and Sol models.

The OpenCode arm was readmitted (ADR 0002) after OpenCode v2 shipped a keyless
`tinyfish` search provider: OpenCode's own hosted endpoint, requiring no
account, key, or billing. The adapter pins that provider through a per-process
`OPENCODE_CONFIG_CONTENT` config (deny-by-default permissions allowing only
read, glob, grep, websearch, webfetch, and question) and runs every invocation
with `--standalone` so a private server inherits that config instead of
attaching to a background service.

`preflight --live` spends a small amount of model usage to verify the exact
model, search, and page fetch in each headless harness, plus a schema-conforming
Codex judgment. The runner refuses `run` until all provisioned arms have
passed those probes. An unavailable arm is recorded as unavailable; its model
is never replaced. `run` also refuses missing repository commits or judge
packs. Use `--arm` and `--task` on `run` for a pilot. The full run has a separate
`--full` flag and requires all 20 slots to be preflighted. A failed or timed-out
run remains in the record; rerunning it requires a new evaluation ID.
The stopped four-arm evaluation has a recorded run plan; start a new evaluation
ID for the current four-arm configuration.

If a GitHub billing record can be attributed to one isolated run, attach it
with `python3 -m agent_eval reconcile-credits --evaluation-id pilot --task IG-01
--arm pi-luna --billing-credits 0.36 --billing-record-id RECORD-ID`.
The report marks a matching `totalNanoAiu / 1e9` value reconciled; a mismatch
stays approximate. Pi credits remain unavailable unless a native
field or an attributable billing record is present.

Agent workspaces contain exported repository trees only. The configuration,
judge packs, and results stay outside those workspaces. The runner verifies
their contents did not change after each run. The tool allowlists further limit
file editing. This is an integrity check, not an OS-level security boundary;
run untrusted agents in a separate sandbox if that guarantee is required.
Uncommitted work is never exported; the manifest records whether each source
checkout was dirty.

## Measurements and review

Each `events.jsonl` entry has a monotonic offset from run start and the raw
harness event. `metrics.json` identifies the source and confidence of every
usage field. The judge receives anonymized events and answer only; it cannot
see the arm name, raw provider billing fields, or other runs. The first
substantive answer event is judged, then its timestamp is computed by the
runner. If an adapter has no reliable intermediate answer stream, that time
is unavailable. The report keeps observed measurements distinct from judge
opinions and links to all answers and judgments.

Judge-only evidence is never passed to agent sessions. Review repository access
before sharing or pushing private repository facts and security notes.

## Implementation notes

The `.yaml` files use JSON syntax, which is valid YAML; Python's standard
`json` module reads them without an added dependency. CLI commands are built
in `src/agent_eval/adapters.py` and checked by preflight. If a vendor changes
flags or event structure, update and re-probe the adapter before a full run.

The source plan is the user-provided pasted document. CLI behavior was checked
against installed Pi/Copilot/Codex help and the official
[Claude Code](https://code.claude.com/docs/en/cli-usage),
[OpenCode](https://opencode.ai/v2/docs/websearch), and
[Antigravity CLI](https://www.antigravity.google/docs/cli/headless/) references.
