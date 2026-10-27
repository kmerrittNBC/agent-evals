# Frozen qualification protocol v1

**The Codex-to-Copilot experiment was stopped on 2026-10-27.** Read the
[stop decision](stop-decision-2026-10-27.md) for the operating rationale,
recommendation, unresolved gate, and conditions for reopening. The frozen
protocol below remains a historical record; no Copilot-backed Codex candidate
was run.

Frozen 2026-10-27, before candidate results. [The plan](plan.md) defines six
gates; [protocol.json](protocol.json) locks the cases, controls, revisions,
prompt hashes, and decision thresholds. This protocol has **no candidate
results**. Issue [#3](https://tea.kyle-merritt.com/anodyine/agent-evals/issues/3)
is the human authorization gate. Do not run a Copilot-backed Codex candidate
or mark that gate passed until its route, account terms, and documented desktop
configuration are confirmed.

The 2026-10-27 [Gate 1 route review](gate-1-route-review.md) records the
organization's approval, the documented generic desktop gateway setting, a
disposable CLI fixture result, and the unresolved GitHub local route. The
fixture is not a candidate run and does not change this frozen protocol.

## Cases and controls

All 15 existing prompts are referenced by ID and SHA-256 in `protocol.json`.
Their source files remain in `config/`; no October manifest, evidence pack, or
result is edited. The two-pilot-per-category order is IG-02, IG-04, DU-01,
DU-03, AR-01, AR-05. After pilot defects are resolved, record a new protocol
version before the full 15-task run. A pilot result is never a full-run result.

Use five matched arms: candidate Codex CLI, candidate official desktop,
ChatGPT-backed Codex CLI, ChatGPT-backed official desktop, and Pi on Copilot.
The candidate and Pi must use the same exact Copilot model ID and `medium`
reasoning; both Codex controls must use the same named model and reasoning
where available. If a control cannot match, record the difference and leave
the matched comparison unresolved. Use the same machine or documented
equivalent, network policy, MCP catalog, prompt, source commits, 900-second
limit, fresh session, and isolated worktree. Preserve the IG information cutoff.
For DU/AR, use the frozen `starting_commit`; for IG, use the pinned October
source revisions and verify their evidence packs agree.

The local Codex CLI, Pi, and OS versions observed when freezing are listed as
reference values in `protocol.json`. They are **not** evidence of the future
run environment. Before collecting any candidate result, create a new run ID
under `results/codex-copilot-<id>/`, fill every `required_run_pins` field in
that run's manifest, record the exact official desktop and app-server builds,
and hash the configuration after removing secrets. If a required pin is
unknown, the run is blocked. Any client/model/catalog upgrade needs a new run
ID and all canaries repeated before promotion.

Gate 2 uses the [disposable smoke repository](smoke-repo/README.md). Make a
fresh temporary copy and Git commit for every attempt; run the same read/edit
prompt and compare the resulting diff. The template is not a candidate run.

## MCP catalog and tool-search cases

[`mcp-catalog.json`](mcp-catalog.json) defines 50 read-only tools across docs,
tickets, calendar, assets, and metrics. Operations such as `search_*` and
`get_*` are intentionally similar across services. The stdio fixture is
`python3 qualifications/codex-copilot/mcp_fixture.py`; it returns a service,
operation, and record marker so the selected function can be audited. Pin the
catalog SHA-256 in the run manifest. The fixture does not itself implement
deferred discovery; the client/tool-search mechanism must supply that.

| ID | Frozen prompt | Required observation |
| --- | --- | --- |
| TS-01 | Without using external data, calculate 17 + 25. | No unnecessary discovery or call; irrelevant definitions remain deferred. |
| TS-02 | Find the documentation page about the release decision using the connected services. | Discover and call `docs_search_pages`; record the returned service marker. |
| TS-03 | Find the issue tracker record about the release decision, then inspect it. | Select `tickets_search_issues` and `tickets_get_issue`, not docs tools. |
| TS-04 | Find the calendar event about the release decision and the asset assigned for it. | Call one correct calendar and one correct assets tool. |
| TS-05 | In the same TS-04 session, inspect the event again. | Correct tool remains available; record cached tokens and context. |

Run each case three times in fresh sessions per Codex client and matched
control. TS-05 follows TS-04 within each session. Record definitions initially
exposed, discovery events, definitions subsequently loaded, tool calls, and
whether discovery was hosted `tool_search`, client-side, or eager. A callable
tool alone does not meet the deferred-definition requirement.

## Native web canaries

Use the same prompts in CLI and desktop, three fresh sessions each. Record
actual action types (`search`, `open_page`, `find_in_page`, or the build's
documented native equivalents), retrieved URL, citation, response metadata,
and service charge. Shell fetches, browser automation, and search MCP calls
cannot satisfy this gate.

| ID | Frozen prompt | Oracle and failure condition |
| --- | --- | --- |
| WEB-S | Search for the latest stable Python 3 release listed on python.org at the run timestamp. Cite the official release/download page. | Native search event plus a current official URL; compare with a same-time manual source snapshot, not model memory. |
| WEB-O | Open https://www.iana.org/domains/reserved and report the A-label for the Korean test IDN in its table. Cite the page. | Native open action and `xn--9t4b11yi5a`. |
| WEB-F | Open https://www.rfc-editor.org/rfc/rfc9110.html, find section 15.5.20, and state which intermediary MUST NOT generate a 421 response. Cite the exact section. | Native page find action and `proxy`. |
| WEB-X | Open https://example.invalid/qualification-missing and report what happened. Do not infer its contents. | Native failure event, no invented page content. |
| WEB-B | Open https://www.rfc-editor.org/rfc/qualification-page-does-not-exist.html and report what happened. Do not infer its contents. | Native unavailable-page event, no invented page content. |

The static oracles were checked against [IANA reserved domains](https://www.iana.org/domains/reserved)
and [RFC 9110 §15.5.20](https://www.rfc-editor.org/rfc/rfc9110.html#section-15.5.20)
on 2026-10-27. Recheck page availability at execution time; a changed source
is a documented deviation, never a silent oracle change.

## Decision rules

`protocol.json` records the predeclared limits. Tool calls need three of
three successes; median input tokens may be at most 1.25 times the matched
ChatGPT-backed Codex control. Native web actions and citations need three of
three successes in both clients. The full task comparison allows zero
decision-changing critical errors and no recurring required-tool failure.
Median latency and measured operating cost must each be at most 1.25 times
matched Pi. Completion and blinded judged quality must be at least Pi on the
matched model, reported by case with uncertainty. Missing provider token or
billing fields produce `unresolved`, never a transcript-length estimate.
Any failed hard gate stops dependent work; unresolved authorization or billing
prevents promotion. Report CLI-only as its own outcome.

See [evidence-format.md](evidence-format.md) for the run layout, event fields,
attribution, hashes, and redaction rules.
