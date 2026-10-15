## Decision

**Fail closed on standalone research MCP sidecar loss.** Close the bridge/client, mark the research trial interrupted, and retain its directory, `started` marker, and compact evidence. Do not restart under the same trial identity or retry an uncertain call.

The current standalone sidecar uses a `VolatileWorkLedger`; restarting it would create fresh allowance. Its exclusive `started` marker prevents that. The owner-managed research-trial path is different: its SQLite ledger durably reserves work and preserves uncertain maxima, but it is a supervised broker over private pipes—not restart support for the standalone MCP sidecar.

A safe same-trial restart is possible only as a later, explicitly approved design backed by durable owner accounting, generation fencing, and a new client/service identity. A reconnect loop or restoring an in-memory quota snapshot is not sufficient.

## Plan recorded

Added [`docs/speculative/research-mcp-sidecar-recovery.md`](relayview/docs/speculative/research-mcp-sidecar-recovery.md) with the decision, contract comparison, staged tests and implementation gates, and rollback. Added a pointer in [`docs/authoritative/research-mcp.md`](relayview/docs/authoritative/research-mcp.md); it explicitly leaves the current fail-closed contract unchanged.

The safe-restart proposal requires:

- **No quota reset:** use the owner’s durable ledger; retain maximum reservations for uncertain work; never replay an uncertain provider effect. An explicit retry is a new charged call.
- **No credential exposure:** reacquire credentials only through the trusted encrypted source and a fresh bounded inherited descriptor. Keep them out of argv, environment, agent workspaces, MCP traffic, logs, and durable evidence.
- **No stale client attaching to a new session:** give each service generation a unique private socket path and immutable client configuration; fence old generations and reject stale identity in a versioned handshake. Do not reuse or repoint the old socket path.
- **Rollback to interruption:** disable restart and preserve ledger state, markers, and evidence. Never roll back accounting or continue the interrupted trial under a different artifact.

## Checks

- Focused MCP and owner-trial tests: **50 passed** across 4 files.
- `npm run docs:references`: **passed**.
- `git diff --check`: **passed**.
- `npm run typecheck`: **failed** on four `TS2344` errors in `node_modules/saxes/saxes.d.ts`. No project-source error was reported. Installation also warned that this environment’s Node 24.11.0 is below some dependencies’ declared Node 24.15.0 minimum.

No runtime code or recovery behavior was changed; the restart design remains a proposal.
