**Decision: if the research MCP sidecar dies mid-trial, the trial ends (fail-closed), and no restart should be built now.** A restart would only be safe with changes that don't exist yet, chiefly moving the quota ledger out of the sidecar. That work belongs to the separate `agent-harness-evals` repository and needs your approval. I wrote this up as a proposal doc; no code changed.

**Why a restart isn't safe with the current design:**
- **Quota reset:** usage is tracked only in the sidecar's memory (`VolatileWorkLedger`). When the process dies, all usage is lost. Only finished calls leave evidence, so up to 16 in-flight calls and their costs leave no record. Rebuilding usage from logs would undercount. Call IDs include a random per-connection value, so nothing can be replayed after a restart either.
- **Stale client:** the bridge only checks the socket's path, mode and owner. It carries no session identity. The native clients' config points at one fixed socket path, so a relaunched bridge would attach to whatever new sidecar is listening there. Today two things prevent that: the `started` marker blocks a relaunch in the same directory, and the supervisor must never point a running client at a different directory.
- **Credential exposure (a real gap, confirmed by running it):** the sidecar reads the setup and the Brave API key *before* checking the marker. A relaunch that will be refused has already received the key. The error message also can't tell "already started" apart from other socket failures.

**Comparison:** fail-closed costs little and makes quota reset impossible. A safe restart would need all of the following. Even then it only saves the trial's remaining quota, because the client has to be torn down anyway so it can't reach the new session:
- a durable ledger outside the sidecar;
- a new setup version with a generation number;
- a fresh directory per generation;
- the bridge checking it is attached to the expected session;
- the supervisor checking the old process is dead before handing over the key;
- a fixed restart limit (default 0, at most 1) set before the trial starts.

It may be cheaper to run restart-sensitive work through the owner's trial path, which already keeps durable accounting.

**Staged plan:**
- **Prerequisite:** fix the transport check so it passes again (see below).
- **Stage 1 (this repo):** check the marker before reading the key, add a distinct "already started" error, and add a test that kills the sidecar mid-call. Each starts with a failing test.
- **Stage 2:** the sidecar logs each reservation as it is made, so a crash leaves a conservative usage record. The supervisor then stops the client, records the trial as interrupted, and never relaunches.
- **Stage 3 (needs your approval):** the restart design above.

The doc also covers the checks for each stage. Rollback always selects the whole previous release for a new trial, and never rolls back or edits the ledger.

**What I changed (not committed):**
- Added `docs/speculative/research-mcp-sidecar-loss-recovery.md` with the decision, comparison, plan, verification and rollback.
- Added one sentence to the Limitations section of `docs/authoritative/research-mcp.md` linking to it.

**Checks:**
- **Passed:** MCP and core service tests (41/41), documentation checks (51/51, `docs:references` exit 0) and `git diff --check`.
- **Failed:** `npm run verify:research-mcp` fails on the unmodified code. The smoke test (`smoke.js:72`) expects 2 tools, but there are now 3 since `youtube_transcript` was added. The package README is also out of date (version 1.1.0, two tools), and the packaging steps name a 1.2.0 file. I left this alone; it's the prerequisite card above.
- **Not run:** the full suite, the native-client checks and the live (paid) smoke.

I installed dependencies in the worktree and removed the two temporary directories my test runs created.

**Process records:** ablation decision `not_required` (this is safety behavior, not a quality feature). Whether any cohort may allow a restart is a separate decision for you. Documentation disposition: `not_required`, since no behavior changed and the proposal stays speculative.
