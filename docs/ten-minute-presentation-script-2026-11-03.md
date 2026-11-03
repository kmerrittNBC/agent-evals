# Coding agent evaluation: 10-minute presentation script

Use with the seven-slide “Coding agent evaluation — 10-minute results and recommendation” presentation. Timing is approximate; the slide numbers match the deck. The bracketed text is a cue, not spoken copy.

## Slide 1 — Coding agent evaluation (0:00–0:30)

If we won't have access to Codex or Claude Code, which coding agent and model should we use for our daily work? Going forward, we have 1,900 Copilot credits per person per month, pooled across the team. I’ll explain the question, which setups were eligible, how we judged them, what we observed, and why I recommend one pair as our starting default.

## Slide 2 — Question, task design, and judging (0:30–2:05)

I broke up the tasks into three kinds of work that are important to our daily dev work: information gathering, well defined and scoped code updates, and architecture or refactoring. I chose five tasks in each category using my personal projects as test material. Four agent setups attempted all 15 tasks, giving 60 total task attempts. Each pair saw the same task prompt and starting repository revision in a fresh session, with a 15-minute limit. This measures the first response to a task, not what would happen several follow-up prompts.

I judged the work with a separate GPT-6 Sol judge. It reviewed each saved attempt in a fresh context. It saw the correct answer, anonymized agent activity, and a task-specific evidence pack with reference facts, acceptable alternative answers. It did not see the pair’s identity, billing fields, or the other pairs’ attempts. The judge scored quality from one to five based on the instructions, rubric, and evidence I provided it, marked the requested deliverable complete or partial, and flagged critical errors. The rubric considered factual accuracy, task completion, source quality, synthesis and judgment, ambiguity handling, and actionability and clarity. For code tasks, it also replayed the saved patch in a clean checkout and ran prepared and regression checks. The checks and the judge’s assessment are separate signals; a green check can still miss incomplete behavior. 

## Slide 3 — Four pairs entered the scored comparison (2:05–3:05)

The four scored pairs were Pi with GPT-6 Luna, Pi with GPT-6 Sol, OpenCode with GPT-6 Luna, and Claude Code with Opus 5.5. The first three used GitHub Copilot; Claude Code used a separate Anthropic account. All four passed the preliminary tool probes needed for this study, including search and page fetch, and writable tools for the code tasks. Because a pair includes both the model and the agent program, the results describe each setup as a whole. For example, Pi and OpenCode used different search routes even when both ran Luna.

## Slide 4 — Setups outside the scored comparison (3:05–4:25)

Several other setups were considered, but they are not part of the 60-attempt comparison. The standalone Copilot CLI did not pass our headless web-search gate. A diagnostic fetched bing search results, but still didn't perform the named search call the protocol required. The lack of native web search tools slowed down the information gathering tasks in manual testing. Antigravity hit an account quota limit, because even if we have Gemini Pro, we don't have Antigravity subscriptions which seem to be billed separately from Gemini Pro. 

Codex with Copilot also considered. We stopped before candidate runs: I couldn't find a publicly documented, well supported route to run Copilot models through Codex CLI and desktop, and a team-maintained bridge would leave too much operational risk. I also tried Pi with a local Qwen model. Its current serving setup produced no architecture deliverables, so it is not a general mixed-workload choice today. 

## Slide 5 — Results across 15 tasks (4:25–6:35)

The results suggest tradeoffs between completing work consistently, judged quality, and speed. Claude Code with Opus had the strongest completion record: 14 of 15 tasks, with at least four of five complete in every category. Its mean judged quality was 4.20 out of five, and its median final time was about 103 seconds. Pi with Sol was the fastest, at about 44 seconds, and had the highest mean quality, 4.60, but completed 12 of 15 tasks. Pi with Luna sat between them on all three measures: 13 complete, a 4.47 quality mean, and a 76-second median, with at least four completions in every category. OpenCode with Luna completed all five architecture tasks but only one research task and two defined updates, so its architecture strength did not carry across the mixed workload.


## Slide 6 — Pooled Copilot credits (6:35–8:05)

If we have 1,900 credits per person per month, cost become a major factor. The bars show Copilot credits used during the experiment on an isolated account: 367.98 credits attributed to Sol and 50.32 to Luna. They are total credits by model, not normalized per task or use. This strongly suggests Sol draws more credits for the tasks we evaluated. The Luna total combines the Pi and OpenCode runs. If we consider that, Sol is using 14.6 times more credits than Luna. That alignts directionally with the 20 times larger credit cost that Github posts for Sol. Sol does seem to give a faster and higher average quality result, but going forward it is worth considering on a task by task basis whether or not the extra credits are worth it. 


## Slide 7 — Recommendation (8:05–10:00)

My recommendation is a pilot of Pi with GPT-6 Luna as the default for mixed work escalating to GPT-6 Sol when needed. Luna is the sensible default inside the pool, with Sol reserved for cases where its speed or quality advantage may justify the extra draw.



## Source notes (not spoken)

- [Executive report](executive-report-2026-10-15.md): research questions, design, scored results, judging method, credit limits, and recommendation.
- [Rubric](../config/rubric.yaml): quality dimensions and category rating thresholds.
- [Copilot usage snapshot](../results/copilot-ai-usage-2026-10-15/README.md): personal-account model totals and attribution limits.
- [Copilot CLI reprobe](../results/copilot-search-reprobe-2026-11-02/README.md): November headless search diagnostic.
- [Codex–Copilot stop decision](../qualifications/codex-copilot/stop-decision-2026-10-27.md): later qualification and maintenance decision.
- [Local Qwen follow-up](../results/local-qwen-linux-combined-20261030.md): separate pilot results.
- The 1,900-credit monthly allowance was supplied by the presenter; it is not a measurement in the October report.
