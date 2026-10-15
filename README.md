# Coding agent information-gathering evaluation

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
  --repo financial-hq-ui=/absolute/path/to/se-financial-hq-ui \
  --repo people-and-orgs-ui-library=/absolute/path/to/people-and-orgs-ui-library
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
The current IG-05 asks about financial HQ UI only. `--angular-root` remains
available for a future fleet task but is not needed for these five prompts.
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
