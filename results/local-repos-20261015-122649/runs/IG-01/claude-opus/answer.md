# Terminal-Bench 2.1 and DeepSWE v1.1 results for five models (as of 2026-10-15)

Only one source has scores for all five models on the same harness: Vals AI on Terminal-Bench 2.1. No source covers all five on DeepSWE v1.1. The vendors' Terminal-Bench 2.1 numbers are 14–17 points above independent runs, and each vendor used a different harness.

## Matrix 1: Terminal-Bench 2.1 (89 tasks, the revised 2.0 set with 28 tasks fixed)

| Model | Vendor-reported | Independent (Vals AI) | Other |
|---|---|---|---|
| **GPT-6 Luna** | **Unverified.** OpenAI's 2026-09-22 launch charts have no Terminal-Bench figure. | **73.03%**. Terminus 2, pass@1, max effort, default temperature, 128K max output. | Snorkel: 75.7% ±1.3, Codex CLI. ⚠️ Dated 2026-06-26, three months before launch and the same date as GPT-5.6 Terra. Probably mislabeled; I treat it as unverified. |
| **GPT-6 Sol** | **Unverified.** No Terminal-Bench figure in the launch charts. | **83.15%**. Terminus 2, max effort, default temperature, 128K max output. | No Snorkel row. Snorkel's "GPT-6.1 Sol" is a different model. |
| **Qwen3.8-27B** | **73.0**. Qwen's Hugging Face card, labeled "(Terminus)". No harness version, effort, runs or timeout given. | **58.43% ±5.25**. Terminus 2, **xhigh** effort, temperature 1, 65,536 max output, Alibaba as provider. | A search snippet claimed Artificial Analysis scores of 79.8 (xhigh) and 65.2 (medium). I couldn't find them on the cited page, so they are excluded. |
| **GLM-5.3** | **88.2**. Z.ai's card. **Claude Code 2.1.207**, temperature 1.0, top_p 1, max_new_tokens 65,536, 6-hour timeout. | **71.54%**. Vals leaderboard page, Terminus 2. ⚠️ Vals' GLM-5.3 model page shows no Terminal-Bench 2.1 entry, only 4.0. | — |
| **DeepSeek V4.1 Flash** | **90.6**. DeepSeek's card, using its own **DeepSeek Harness (DSH) Minimal**. reasoning_effort=100 (max), N=3, no network, 1M context, 500 max steps. The same card reports other harnesses: mini-SWE 90.3, Claude Code 88.0, Pi 86.1, DSH Standard 85.8, DSH PTC 85.8, OpenCode 85.0, Codex 84.1. | **74.53%**. Terminus 2, 3 full trials, max effort, temperature 1, 384K max output. | — |

## Matrix 2: DeepSWE v1.1 (Datacurve benchmark, 113 tasks, 91 repos, 5 languages)

| Model | Vendor-reported | Mercor | Other independent |
|---|---|---|---|
| **GPT-6 Luna** | **66.6%** at max effort (also xhigh 61.3, high 59.3, medium 44.5, low 2.4). From OpenAI's launch chart as transcribed by secondary sites. Harness not stated. | **67.0% ±6.8**. mini-swe-agent, 500 steps, 2-hour limit, max effort, 339 samples. ⚠️ Mirror only (BenchLM); not shown on Mercor's top-level page. | Artificial Analysis: **64%**, Codex harness, max effort. |
| **GPT-6 Sol** | **68.8%** at max effort (also xhigh 66.6, high 65.3, medium 56.6, low 37.2). Same caveat as Luna. | **70.5% ±7.2**, same settings, 338 samples. ⚠️ Mirror only. Not the same as Mercor's GPT-6.1 Sol (72.3%). | None found. |
| **Qwen3.8-27B** | **42.2**. Qwen's card. **Claude Code harness**, temperature 1.0, top_p 0.95, 256K context. | **Unverified.** Mercor lists only Qwen3.8-**Max** (53.1%, xhigh). | **Unverified.** Datacurve also lists only Qwen3.8-Max. |
| **GLM-5.3** | **66.9**. Z.ai's card. mini-swe-agent, temperature 0.95, top_p 1.0, 6-hour timeout, 400K context. | **70.5% ±6.3**, 339 samples. ⚠️ Mirror only. | Datacurve: **68.96%** (95% CI 65.94–71.98), mini-swe-agent, max effort, about 451 rollouts (4 per task). Pass@4 is 87.61%. Datacurve's own site shows it rounded to 69% ±3. |
| **DeepSeek V4.1 Flash** | **74.2**. DeepSeek's card. mini-SWE, max effort, N=8, 1M context, 500 steps. The same card reports other harnesses: DSH Minimal 72.6, DSH Standard 70.5, Claude Code 69.8, DSH PTC 67.6, Pi 66.2, Codex 65.6, OpenCode 65.5. | **71.7%** at max effort, confirmed on Mercor's own page. The mirror adds ±6.3 and mini-swe-agent with a 500-step / 2-hour limit. | Not on the Datacurve leaderboard (last updated 2026-09-22). |

## Results that aren't directly comparable

- **The vendor Terminal-Bench 2.1 numbers use three different harnesses.** GLM-5.3 ran in Claude Code, DeepSeek in its own harness, and Qwen in an unspecified "Terminus". DeepSeek's own table shows that changing the harness alone moves its score by 6.5 points.
- **The vendor tables copy competitors' numbers.** DeepSeek's card lists GLM-5.3 at 88.2 next to its own 90.6. That 88.2 is Z.ai's Claude Code result, not a DeepSeek rerun. The 88.8 shown for GPT-5.6 Sol is likewise copied from elsewhere.
- **Vendor and Vals scores are far apart on Terminal-Bench 2.1:** GLM −16.7, DeepSeek −16.1, Qwen −14.6. The gaps come from different harnesses, timeouts and runs, so treat the vendor numbers as best-case setups.
- **Vals settings aren't identical.** Qwen ran at xhigh rather than max effort, and maximum output length was 65K for Qwen, 128K for GPT/GLM and 384K for DeepSeek.
- **DeepSWE is sensitive to the harness.** DeepSeek's own scores range from 65.5 to 74.2 depending on harness. Qwen's 42.2 used Claude Code, while most other figures used mini-swe-agent.
- **Watch for similar model names.** I excluded GPT-6.1 Sol, GPT-5.6 Sol/Luna, GLM-5.3-Flash, Qwen3.8-Max and DeepSeek V4 Flash. Several aggregators mix these up; llm-stats, for example, marks all of its Terminal-Bench 2.1 rows as self-reported.
- **Mercor rows for GPT-6 Sol, GPT-6 Luna and GLM-5.3 come only from BenchLM's mirror.** Mercor's own page showed only the top six rows.

## Which comparisons the evidence supports

1. **Terminal-Bench 2.1: use Vals only.** It is the only source with one harness and one evaluator for all five models. GPT-6 Sol (83.2) is clearly ahead. DeepSeek V4.1 Flash (74.5), GPT-6 Luna (73.0) and GLM-5.3 (71.5) are within about 3 points of each other. With 89 tasks, one task is worth about 1.1 points, so those three can't be reliably ranked. Qwen3.8-27B (58.4 ±5.25) is clearly last, though it also ran at a lower effort setting.
2. **DeepSWE v1.1: the four non-Qwen models are statistically tied.** On Mercor's mini-swe-agent run they score 67.0–71.7 with margins of ±6–7. That supports "same tier" but not a ranking. Datacurve's GLM-5.3 result (69%) and Z.ai's own 66.9 sit in the same band.
3. **Sol vs Luna within one source is fine.** OpenAI's chart (68.8 vs 66.6) and Mercor's run (70.5 vs 67.0) both put Sol slightly ahead, but within the error margins.
4. **Qwen3.8-27B on DeepSWE supports only a directional claim.** Its 42.2 is self-reported in a different harness, and no independent run exists. It is likely well behind the others, but the size of the gap is unverified.
5. **Don't compare vendor numbers with each other or with independent runs.** That includes headline claims such as "DeepSeek V4.1 Flash 90.6 beats GLM-5.3 88.2".

Two things I couldn't check: OpenAI's own launch page (the GPT-6 DeepSWE numbers come via secondary transcriptions) and the full body of DeepSeek's arXiv report.

Sources:
- [Vals AI – Terminal-Bench 2.1](https://www.vals.ai/benchmarks/terminal-bench-2-1)
- Vals AI model pages: [GPT-6 Sol](https://www.vals.ai/models/openai_gpt-6-sol), [GPT-6 Luna](https://www.vals.ai/models/openai_gpt-6-luna), [Qwen3.8-27B](https://www.vals.ai/models/alibaba_qwen3.8-27b), [GLM-5.3](https://www.vals.ai/models/zai_glm-5.3), [DeepSeek V4.1 Flash](https://www.vals.ai/models/deepseek_deepseek-v4.1-flash)
- [Snorkel – Terminal-Bench 2.1](https://snorkel.ai/leaderboard/terminal-bench-2-1/)
- [Artificial Analysis – Terminal-Bench 2.1](https://artificialanalysis.ai/evaluations/terminalbench-2-1)
- [tbench.ai – Terminal-Bench 2.1 announcement](https://www.tbench.ai/news/terminal-bench-2-1)
- [Mercor – DeepSWE v1.1 leaderboard](https://www.mercor.com/apex/oss-benchmarks/oss-deep-swe-leaderboard/)
- [BenchLM – Mercor DeepSWE v1.1 mirror](https://benchlm.ai/benchmarks/mercordeepswe11)
- [Datacurve DeepSWE leaderboard](https://deepswe.datacurve.ai)
- [Datacurve – DeepSWE v1.1 changelog](https://deepswe.datacurve.ai/blog/deepswe-v1-1)
- [benchmarklist – DeepSWE 1.1](https://benchmarklist.com/benchmarks/deepswe_1_1/)
- [DeepSWE paper (arXiv 2607.07946)](https://arxiv.org/abs/2607.07946)
- Vendor model cards: [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B), [GLM-5.3](https://huggingface.co/zai-org/GLM-5.3), [DeepSeek-V4.1-Flash](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash)
- [Artificial Analysis – GPT-6 Sol and Luna](https://artificialanalysis.ai/articles/gpt-6-sol-and-luna-push-the-cost-efficiency-frontier)
- [Computing for Geeks – GPT-6 Sol and Luna](https://computingforgeeks.com/gpt-6-sol-luna-released-features-benchmarks/)
- llm-stats: [Terminal-Bench 2.1](https://llm-stats.com/benchmarks/terminal-bench-2.1), [DeepSWE 1.1](https://llm-stats.com/benchmarks/deepswe-1.1)
