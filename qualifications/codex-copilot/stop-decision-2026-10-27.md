# Decision: stop the local Codex–Copilot qualification

**Decision date:** 2026-10-27  
**Decision owner:** account holder and team sponsor, as stated in the issue discussion  
**Outcome:** stop work on the local Codex-to-Copilot connection and do not recommend it for team rollout. Retain Pi with GPT-6 Luna as the recommended mixed-workload pilot/default, subject to the limitations below.

## Why the experiment stopped

The organization approved using Codex with its Copilot Business seat. This was not an organizational permission rejection. OpenAI [documents custom Responses gateways for Codex CLI and the official desktop](https://learn.chatgpt.com/docs/enterprise/connect-to-a-gateway), and a disposable local fixture completed streamed text turns for the `gpt-6-sol` and `gpt-6-luna` aliases. Those observations establish the Codex-facing configuration path, not a Copilot-backed candidate.

GitHub [documents Copilot-backed Codex inference in Agentic Workflows](https://github.github.com/gh-aw/reference/engines/codex/), but requires that product's sandbox. No publicly documented, supported **local** Copilot Responses route was established for the team's CLI and unmodified desktop. The [Gate 1 route review](gate-1-route-review.md) catalogs community bridges and Pi's implementation. They demonstrate technical feasibility, but the local routes examined depend on internal or token-derived Copilot interfaces and do not provide a vendor-backed compatibility commitment. No Copilot-backed Codex candidate, desktop run, billing check, or later qualification gate was performed.

The team requires a coding-agent route that will not leave all developers blocked while one specialist repairs a locally maintained gateway after a Codex or Copilot change. Maintaining such a bridge is outside the team's acceptable operating model. This is a **decision to stop an unresolved qualification**, not a failed model-quality comparison or a claim that GitHub prohibits every possible future route.

## Operating recommendation and limits

The [October executive report](../../docs/executive-report-2026-10-15.md) calls Pi + GPT-6 Luna the **best provisional balance** among its four tested pairs: 13/15 tasks judged complete, mean judged quality 4.47/5, and Good/Good/Excellent ratings across information gathering, defined updates, and architecture work. Claude Code + Opus completed 14/15; Pi + Sol was faster and had higher mean judged quality. The account-level Copilot usage record gives a directional, model-level credit advantage for Luna, not a Pi-specific per-task price. The report's blind human review of critical errors and cost reconciliation remain pending. Its screenshot came from a personal Pro+ account, so it cannot establish Copilot Business billing.

Recommend **Pi + GPT-6 Luna as a pilot/default for mixed work**, with a short Business-seat operational and cost check and human review of the consequential October errors before calling it an unqualified organization-wide standard. The organization admin already approved the prior Pi/Copilot work, according to the account holder. Pi [documents Copilot as a built-in provider](https://pi.dev/docs/latest/providers) and its [release notes](https://github.com/earendil-works/pi/releases/tag/v1.4.0) show Copilot-specific fixes and model updates. This distributes maintenance across a project used beyond this team; it is not a support guarantee. Pi's published [authentication implementation](https://github.com/earendil-works/pi/blob/main/packages/ai/src/auth/oauth/github-copilot.ts) also depends on an internal Copilot token route. We found no published Copilot-path service-level commitment from Pi in the reviewed docs.

## Gate record and preservation

| Gate | Closing disposition |
| --- | --- |
| Gate 1: authorization and supported connection | Organization approval recorded; supported local upstream and account-specific desktop proof **unresolved**. The team stopped pursuing this route. |
| Gates 2–6: inference/billing, desktop workflow, tool search/context, native web, task comparison | **Not run**. No pass or fail is inferred. |

The [frozen v1 protocol](protocol.json), [evidence format](evidence-format.md), October source records, and October results remain unchanged. The loopback fixture and route review are research artifacts, not candidate evidence. Do not start the live dependent issues from them.

Reopen the idea only if GitHub supplies a documented supported local interface or vendor-backed product for the Business seat, the team accepts the support and fallback model, and a new pinned protocol qualifies both official clients and models. Any future study gets its own run ID and does not rewrite the October results.
