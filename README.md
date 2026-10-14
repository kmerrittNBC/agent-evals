# Coding agent information-gathering evaluation

This repository runs the five prompts in `config/tasks.yaml` through six pinned
model/harness arms. It keeps the agent transcript, a fresh blinded Codex
judgment, and a traceable report for every attempted run. The first evaluation
is 30 agent runs and up to 30 judgments. No evaluation has been run yet.

## Requirements

- Python 3.11 or newer; no Python packages are required.
- The CLIs in `config/arms.yaml`, authenticated for the exact models.
- A pinned Git checkout of each relevant Angular repository for IG-02 through
  IG-05. The runner exports the commits into temporary read-only directories.
- Completed judge-only packs in `evidence/IG-*/pack.json`. See the template and
  `evidence/README.md`. These are intentionally absent from agent workspaces.
- A confirmed information cutoff (`--cutoff`, ISO 8601 with timezone).

Run `python3 -m agent_eval --help` for commands. A typical sequence is:

```sh
python3 -m agent_eval preflight --evaluation-id pilot --cutoff 2026-10-14T17:00:00-04:00 \
  --repo financial-hq-ui=/absolute/path --repo other-angular=/absolute/path
python3 -m agent_eval preflight --evaluation-id pilot --live
python3 -m agent_eval run --evaluation-id pilot --full
python3 -m agent_eval judge --evaluation-id pilot
python3 -m agent_eval report --evaluation-id pilot
```

`preflight --live` spends a small amount of model usage to verify the exact
model, search, and page fetch in each headless harness, plus a schema-conforming
Codex judgment. The runner refuses `run` until all provisioned arms have
passed those probes. An unavailable arm is recorded as unavailable; its model
is never replaced. `run` also refuses missing repository commits or judge
packs. Use `--arm` and `--task` on `run` for a pilot. The full run has a separate
`--full` flag and requires all 30 slots to be preflighted. A failed or timed-out
run remains in the record; rerunning it requires a new evaluation ID.

If a GitHub billing record can be attributed to one isolated run, attach it
with `python3 -m agent_eval reconcile-credits --evaluation-id pilot --task IG-01
--arm copilot-luna --billing-credits 0.36 --billing-record-id RECORD-ID`.
The report marks a matching `totalNanoAiu / 1e9` value reconciled; a mismatch
stays approximate. Pi and OpenCode credits remain unavailable unless a native
field or an attributable billing record is present.

Agent workspaces contain exported repository trees only. The configuration,
judge packs, and results stay outside those workspaces. The runner verifies
their contents did not change after each run. The tool allowlists further limit
file editing. This is an integrity check, not an OS-level security boundary;
run untrusted agents in a separate sandbox if that guarantee is required.

## Measurements and review

Each `events.jsonl` entry has a monotonic offset from run start and the raw
harness event. `metrics.json` identifies the source and confidence of every
usage field. The judge receives anonymized events and answer only; it cannot
see the arm name, raw provider billing fields, or other runs. The first
substantive answer event is judged, then its timestamp is computed by the
runner. If an adapter has no reliable intermediate answer stream, that time
is unavailable. The report keeps observed measurements distinct from judge
opinions and links to all answers and judgments.

Judge-only evidence is never passed to agent sessions. Do not commit private
repository facts or security notes without reviewing repository access.

## Implementation notes

The `.yaml` files use JSON syntax, which is valid YAML; Python's standard
`json` module reads them without an added dependency. CLI commands are built
in `src/agent_eval/adapters.py` and checked by preflight. If a vendor changes
flags or event structure, update and re-probe the adapter before a full run.

The source plan is the user-provided pasted document. CLI behavior was checked
against installed Pi/Copilot/Codex help and the official
[OpenCode](https://dev.opencode.ai/docs/cli),
[Claude Code](https://code.claude.com/docs/en/cli-usage), and
[Antigravity CLI](https://www.antigravity.google/docs/cli/headless/) references.
