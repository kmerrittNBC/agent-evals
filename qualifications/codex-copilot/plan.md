# Codex CLI and desktop with GitHub Copilot: gated qualification

Status: proposed

Created: 2026-10-27

Decision owner: development team

## Objective

Determine whether the team can continue using Codex CLI and the **official, unmodified Codex desktop app** after its current Codex subscription access ends, with model inference charged to its GitHub Copilot subscription. Promote the setup only if its authorization, desktop support, tool behavior, context use, reliability, and cost are demonstrated.

This is a new qualification. The October 2026 four-arm study and its frozen prompts, configurations, evidence, and results remain historical records. A successful CLI probe does not qualify the desktop app.

## Candidate and controls

- **Candidate:** Codex CLI and official Codex desktop, each using the same named Copilot model, reasoning level, and authorized inference route. Record the exact account plan and organization policy.
- **Codex control:** the team's current ChatGPT-backed Codex setup, while it remains available. This establishes which desktop features and tools the team expects to retain.
- **Copilot control:** Pi with the same Copilot model and reasoning level. This measures the value of the Codex harness under the subscription that will remain available.
- Run on the same machine or documented equivalent, repository revision, task prompt, MCP catalog, network policy, and time limit. Use fresh sessions and isolated worktrees. Pin client versions and repeat the canaries after any upgrade before promotion.

Record the exact Codex desktop, Codex CLI/app-server, Pi, model, and operating-system versions. A model shown in a picker is not proof that a turn can run on it; a completed request and attributable usage record are required.

## Decision states

Each gate is **pass**, **fail**, or **unresolved**. Stop the qualification at a failed hard gate. An unresolved authorization or billing gate prevents promotion, even if the technical probes pass. Record an alternative such as “CLI only” separately; it does not count as a desktop pass.

## Gate 1: license, terms, and supported connection

1. Identify the applicable GitHub Copilot subscription agreement, organization policy, and OpenAI terms for the accounts that will be used. Save links, effective dates, and the reviewer who checked them.
2. Identify the exact authentication flow and inference endpoint. Obtain vendor documentation or written vendor/organization confirmation that this account may use that route from the proposed client. A GitHub-hosted workflow example is a lead to investigate, not blanket authorization for every client or account.
3. Identify how the official desktop app accepts the provider through documented settings. Do not patch, repackage, inject code into, or replace proprietary desktop components. Changes to Apache-licensed Codex CLI/app-server source, if needed, are a separate software workstream and do not establish desktop permission.
4. Check whether the desktop app requires a ChatGPT account for UI sign-in and whether the account state expected after the subscription change can launch the app and select the provider. Use a separate test account with that exact entitlement when practical; do not cancel a production subscription to run this probe.

**Pass:** the connection and desktop configuration are authorized for the team's accounts, and the official desktop runs through documented configuration without modification. **Fail:** it needs a private endpoint, extracted credential, access-control bypass, or desktop modification. **Unresolved:** terms or vendor support do not establish the route; ask the account owner or vendors for a written answer before proceeding.

## Gate 2: inference, identity, and billing

Use a disposable repository and a fresh isolated Codex configuration. For CLI and desktop independently:

1. Run a simple response and a small repository read/edit turn with the target Copilot model.
2. Capture the effective model and provider, successful streamed response and tool calls, and sanitized request metadata. Never save access tokens or raw authorization headers.
3. Reconcile each isolated run with GitHub Copilot usage or billing records. Check OpenAI API and Codex usage for unexpected charges. If the billing UI cannot attribute the run, obtain another attributable record or mark the gate unresolved.
4. Repeat after signing in with the ChatGPT account state expected after the team's subscription ends.

**Pass:** both clients complete turns with the intended Copilot model, and the usage is attributable to Copilot with no unexpected OpenAI charge. Record any ChatGPT account still needed for desktop sign-in. A working CLI alone yields **CLI only**.

## Gate 3: desktop workflow

Exercise the workflows the team actually uses: open a repository, inspect and edit files, run a command, review a diff, approve/deny a requested action, use an isolated worktree, resume a session, and call an MCP tool. Capture desktop screen evidence and the corresponding app-server or client events where available. Verify which features are local and which require Codex cloud entitlement.

**Pass:** all required local workflows function on the Copilot-backed candidate under the post-subscription account state. Document any optional features lost; do not silently count a CLI or app-server run as a desktop run.

## Gate 4: tool search and context budget

Use the same representative MCP catalog in each control and candidate. Include at least 50 tools across several clearly described services, with a few similarly named tools. Freeze the catalog and the prompts before measuring.

Run these cases in fresh sessions for both CLI and desktop:

| Case | Expected evidence |
| --- | --- |
| No external tool needed | No large eager tool-schema payload and no unnecessary discovery call. |
| One tool needed, named indirectly | Discovery event, correct tool loaded and called, useful result. |
| Similar tool names | Correct service and function selected without guessing. |
| Two tools from different services | Both discovered and called; unrelated definitions remain deferred. |
| Follow-up in same session | Correct tool remains available; caching and context behavior are recorded. |

Save per-turn input, output, and cached tokens; tool definitions initially exposed; discovery and call events; latency; and peak context use. Distinguish OpenAI-hosted `tool_search` from client-executed discovery or eager loading. A tool merely being callable does not prove the context-saving requirement.

**Pass:** all required calls succeed in three consecutive fresh runs per case, the mechanism genuinely defers irrelevant definitions, and median input tokens are no more than **1.25×** the ChatGPT-backed Codex control on matched prompts. Record the Copilot/Pi comparison as additional context. If model or API usage fields cannot support this measurement, mark the budget result unresolved rather than estimating from transcript length. Revisit the 1.25× limit before running the cases if the team wants a different budget.

## Gate 5: native web search and page retrieval

The OpenAI Responses API's hosted web search can emit `search`, `open_page`, and `find_in_page` actions. Codex may expose a client-side web tool with different events. Identify the actual mechanism in each build and distinguish it from a shell `curl`, browser automation, or third-party search MCP. The requirement here is the team's **native OpenAI web capability**, not a merely equivalent answer from another provider.

For both CLI and desktop, run three fresh repetitions of each canary:

1. **Search:** ask for a current fact that cannot be answered reliably from model memory. Require a source URL and a recorded native search call.
2. **Open:** provide a specific public URL containing a unique fact. Require a recorded native open/page retrieval action and the correct fact.
3. **Find:** ask for a detail deep within a long page. Require a recorded page search/find action or equivalent native evidence and a precise citation.
4. **Failure behavior:** try an invalid URL and a blocked or unavailable page. Verify that the client reports the failure without inventing page content.

Capture tool catalogs, request and event types, result metadata, citations, and service usage charges. Establish whether OpenAI's hosted tools can be used while inference runs through Copilot, and which account pays for them. Setting a `web_search` flag or seeing a model answer is insufficient evidence.

**Pass:** the required native actions are exposed and successful in both clients, citations point to the material actually retrieved, and billing is understood. If native search is unavailable through this provider, the candidate fails this gate even if an MCP replacement works; a replacement can be evaluated as a separately named fallback.

## Gate 6: task quality, reliability, and operating cost

After gates 1–5 pass, run two pilot tasks from each existing category (IG, DU, AR) through both candidate clients. Resolve any probe defects, freeze the setup, then run the full 15-task set with the same source revisions and time limits as the existing study. Preserve the distinction between this new run and the historical four-arm results. Use the same prepared checks and blind judging where applicable; add human review of failures and desktop usability.

Record completion, critical errors, prepared-check outcomes, time to first substantive response, final time, input/output/cached tokens, tool failures, context compactions, Copilot credits, and any OpenAI charges. Repeat a short multi-session desktop workflow to catch sign-in expiry, provider reset, and resume problems.

**Pass:** no decision-changing critical error or recurring required-tool failure; task completion and judged quality are at least competitive with Pi on the same model; median time and measured cost fit the team's predeclared budget. If the sample is too small or billing cannot be attributed, report uncertainty rather than ranking by a single aggregate number.

## Evidence and reporting

Create a manifest for each run containing version pins, account-plan category (never credentials), configuration hash, model, reasoning setting, source revision, prompt ID, timestamps, and outcome. Store sanitized CLI events, desktop screenshots/event logs, web tool traces, token and billing reconciliation, and reviewer notes under a new qualification-specific results ID. Keep raw credentials, tokens, and unredacted request headers out of this repository. Large captures should be linked from a controlled artifact store instead of committed to Git.

The final report should give a pass/fail/unresolved row for every gate, evidence links, deviations from the frozen protocol, measured comparisons with both controls, and one recommendation: **promote CLI and desktop**, **CLI only**, **retain Pi**, or **investigate a separately named fallback**. Promotion requires every hard gate above to pass; optional desktop preferences cannot override a failed authorization, billing, tool-search, or native-web gate.

## References to verify at execution time

- [OpenAI Codex open-source components](https://developers.openai.com/blog/codex-as-a-platform) and [Codex source license](https://github.com/openai/codex/blob/main/LICENSE)
- [OpenAI Terms of Use](https://openai.com/policies/row-terms-of-use/) and [Service Terms](https://openai.com/policies/service-terms/)
- [GitHub Copilot terms](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service) and [GitHub Agentic Workflows Codex inference example](https://github.github.com/gh-aw/reference/engines/codex/)
- [OpenAI Docs: tool search](https://developers.openai.com/api/docs/guides/tools-tool-search) and [OpenAI Docs: web search actions](https://developers.openai.com/api/docs/guides/tools-web-search)
- [Current evaluation runner preflight](../../src/agent_eval/preflight.py) and [October study](../../docs/executive-report-2026-10-15.md)
