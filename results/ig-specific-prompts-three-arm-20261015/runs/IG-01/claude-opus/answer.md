# Terminal-Bench 2.1 and DeepSWE v1.1 results for five models (as of 14 Oct 2026)

**Bottom line:** No single source runs all five models on both benchmarks under one setup. Only one source covers all five on Terminal-Bench 2.1: Vals AI. For DeepSWE v1.1, no independent source covers all five. Most of the higher numbers are reported by the model makers, each on its own harness, so they can't be compared with each other.

## Matrix

### Terminal-Bench 2.1 (89 tasks; a 2.1 refresh of 2.0 that fixes 28 tasks)

| Model | Score | Reported by | Harness / settings | Comparable? |
|---|---|---|---|---|
| **GPT-6 Sol** | **83.15%** | Vals AI (independent) | Terminus 2 on Daytona, pass@1, time limit (value not stated). Snapshot 28 Sep 2026; Vals has archived the benchmark. | ✅ Vals group |
| | No maker score | OpenAI | I found no Terminal-Bench 2.1 number in OpenAI's launch coverage. The openai.com page returned 403 to me, so I couldn't check it directly. | — |
| **GPT-6 Luna** | **73.03%** | Vals AI | Same as above | ✅ Vals group |
| | No maker score | OpenAI | Same as above | — |
| **Qwen3.8-27B** | **58.43%** | Vals AI | Same as above | ✅ Vals group |
| | 73.0 | Alibaba/Qwen (model card) | Labelled "Terminus". No temperature, runs or timeouts disclosed. | ⚠️ Maker-reported, settings not disclosed |
| **GLM-5.3** | **71.54%** | Vals AI | Same as above | ✅ Vals group |
| | 88.2 | Z.ai (model card) | Claude Code 2.1.207, temp 1.0, top_p 1, 65,536-token output cap, 6-hour timeout | ⚠️ Different harness |
| | (88.2) | DeepSeek V4.1 Flash paper, Table 3 | Identical to Z.ai's number. The paper doesn't say whether it re-ran it, so I treat it as copied, not a second measurement. | ⚠️ Not independent |
| **DeepSeek V4.1 Flash** | **74.53%** | Vals AI | Same as above | ✅ Vals group |
| | 90.6 | DeepSeek (arXiv 2609.19969, Table 3) | DeepSeek's own harness ("Minimal" mode), max effort, temp 1.0, top_p 0.95, 1M context, max 500 steps, no network. The paper states N=3 runs for its harness-comparison table but doesn't say it applies to the headline number. | ⚠️ Different harness |

### DeepSWE v1.1 (Datacurve, 113 tasks). Epoch AI rates this benchmark "Flawed" (see caveats)

| Model | Score | Reported by | Harness / settings | Comparable? |
|---|---|---|---|---|
| **GPT-6 Sol** | 68.8% (max). Also 66.6 xhigh, 65.3 high, 56.6 medium, 37.2 low | OpenAI launch post (via secondary coverage and the deepswe-tracker dataset) | "OpenAI's research environment", harness not named. Competitor numbers were taken from public reports, not re-run. | ⚠️ Maker-reported, unnamed harness |
| | 70.5% ±7.2 (max) | Mercor APEX, as recorded by deepswe-tracker | mini-swe-agent | ⚠️ **Partly unverified:** Mercor's live page now shows GPT-6.1 Sol (72.3%), not GPT-6 Sol |
| | Not on board | Datacurve official board | The board has added no models since GPT-6 Astra (3 Sep) | — |
| **GPT-6 Luna** | 66.6% (max). Also 61.3 xhigh, 59.3 high | OpenAI | Same as above | ⚠️ |
| | 64% (max) | Artificial Analysis | OpenAI's Codex harness | ⚠️ Different harness |
| | 67% ±6.8 (max) | Mercor APEX, via tracker | mini-swe-agent | ⚠️ **Partly unverified:** not on Mercor's live page |
| **Qwen3.8-27B** | 42.2 | Alibaba/Qwen (model card) | **Claude Code** harness, temp 1.0, top_p 0.95, 256K context | ⚠️ Only score found; maker-reported and not on the standard harness |
| | Not on board | Datacurve / Mercor | Datacurve lists only qwen3.8-max (57%), which is a different model | **Independent score: unverified** |
| **GLM-5.3** | 66.9 | Z.ai (model card) | mini-swe-agent, temp 0.95, top_p 1.0, 6-hour timeout, 400K context | ◐ Same harness as Datacurve, different sampling |
| | **69% ±3% (68.96)** (max) | **Datacurve official board** | mini-swe-agent, 4 passes over the tasks | ✅ Only official-board entry among the five |
| | 70.5% ±6.3 (max) | Mercor APEX, via tracker | mini-swe-agent | ⚠️ **Partly unverified:** not on Mercor's live page |
| **DeepSeek V4.1 Flash** | 74.2 (max) | DeepSeek (paper, Table 3) | mini-SWE harness, N=8, temp 1.0, top_p 0.95, max 500 steps | ◐ Same harness family |
| | 69.8 / 65.6 / 65.5 / 66.2 / 72.6 | DeepSeek (model card, via tracker) | Claude Code / Codex / OpenCode / Pi / DeepSeek's own harness. This is the same model on five harnesses. | ⚠️ Shows how much the harness alone moves the score |
| | **71.7%** ±6.3 (max) | **Mercor APEX** (confirmed on the live page) | mini-swe-agent | ✅ Independent |
| | Not on board | Datacurve official board | — | — |

**Aggregators are not separate sources.** llm-stats (TB2.1: 0.906 / 0.882 / 0.730; DeepSWE: 0.742 / 0.688 / 0.669 / 0.666 / 0.422) and BenchLM repeat the makers' numbers. Both label every entry "self-reported" or "unverified". BenchLM's and llm-stats' Terminal-Bench 2.1 pages list **GPT-5.6** Sol/Luna (88.8–91.9 / 84.7), not GPT-6, so don't read those as GPT-6 scores. A search snippet claimed Artificial Analysis measured GLM-5.3 at 83.9% on Terminal-Bench 2.1. I couldn't confirm that on Artificial Analysis's page, which showed only the top three entries, so I left it out.

## Results that can't be compared

1. **Maker scores vs. Vals on Terminal-Bench 2.1.** The gaps are 15–17 points: DeepSeek 90.6 vs 74.5, GLM 88.2 vs 71.5, Qwen 73.0 vs 58.4. Each maker used a different harness (DeepSeek's own, Claude Code, Terminus), with different timeouts and sampling.
2. **DeepSWE harness effects are as large as the gaps between models.** DeepSeek's own data show a spread of about 9 points from harness alone (74.2 on mini-SWE vs 65.5 on OpenCode). So Qwen's 42.2 (Claude Code) and OpenAI's internal-harness numbers can't be ranked directly against mini-swe-agent scores.
3. **Effort levels differ.** OpenAI publishes five effort levels. Only the "max" figures line up with the others.
4. **DeepSWE v1.1 itself is questionable.** Epoch AI found false negatives (correct work graded as failing) in at least 23 of the 113 tasks (over 20%) and rates it "Flawed". In 18 of those cases the model had edited existing tests. Models or harnesses that tend to touch tests are penalized, which distorts both absolute scores and cross-harness comparisons.
5. **Terminal-Bench 2.1 is retired.** Vals replaced it with Terminal-Bench 4.0. Vals also notes that some headline runs used fallback models on certain tasks, and I couldn't tell whether that affected these five models.

## Comparisons the evidence supports

**Terminal-Bench 2.1 (Vals only, one harness, all five models):**
- **GPT-6 Sol is clearly ahead** (83.2). **Qwen3.8-27B is clearly behind** (58.4). Both gaps are well beyond noise.
- **DeepSeek V4.1 Flash (74.5), GPT-6 Luna (73.0) and GLM-5.3 (71.5) are effectively tied.** One task is about 1.1 points, and Vals reports single pass@1 runs with no confidence intervals. With 89 tasks the sampling error is roughly ±4–5 points, so don't rank these three.
- The maker-reported order (DeepSeek > GLM > Qwen) only matches Vals for Qwen being last. Vals does **not** support the makers' claimed ~88–91 levels.

**DeepSWE v1.1 (weaker evidence):**
- The best like-for-like set is Mercor's mini-swe-agent runs: DeepSeek 71.7, Sol 70.5, GLM 70.5, Luna 67. Their ±6–7 point intervals overlap completely, so **the four are statistically indistinguishable**. Only DeepSeek's entry is confirmed on Mercor's current page; the other three come from a third-party tracker.
- **Sol over Luna** is directional only. OpenAI's own numbers favour Sol by about 2 points at max effort, which is within the error margins.
- **Qwen3.8-27B being lower** (42.2) is plausible because the gap of ~25 points is larger than any harness effect seen. But the only score is the maker's own, on a different harness, so I've marked Qwen's independent DeepSWE score **unverified**.
- **No source supports a full ranking of all five on DeepSWE v1.1.** The benchmark's flaw rating weakens any small difference further.

**Across the two benchmarks:** there's no basis for combining them. Only GLM-5.3 and DeepSeek V4.1 Flash have independent scores on both, and on each benchmark their two independent scores are within error of each other.

**Gaps I couldn't close:** I couldn't fetch OpenAI's launch post directly (HTTP 403), so the GPT-6 DeepSWE numbers come from secondary coverage and the deepswe-tracker dataset. Artificial Analysis's Terminal-Bench 2.1 page showed only its top three entries.

Sources:
- [Vals AI – Terminal-Bench 2.1](https://www.vals.ai/benchmarks/terminal-bench-2-1)
- [Artificial Analysis – Terminal-Bench 2.1](https://artificialanalysis.ai/evaluations/terminalbench-2-1)
- [Artificial Analysis – GPT-6 Sol and Luna](https://artificialanalysis.ai/articles/gpt-6-sol-and-luna-push-the-cost-efficiency-frontier)
- [Snorkel – Terminal-Bench 2.1](https://snorkel.ai/leaderboard/terminal-bench-2-1/)
- [tbench.ai – Terminal-Bench 2.1](https://www.tbench.ai/news/terminal-bench-2-1)
- [OpenAI – Introducing GPT-6 Sol and Luna](https://openai.com/index/introducing-gpt-6-sol-and-luna/) (blocked) and [Digital Applied summary](https://www.digitalapplied.com/blog/gpt-6-sol-luna-launch-pricing-benchmarks-2026)
- [Qwen3.8-27B model card](https://huggingface.co/Qwen/Qwen3.8-27B)
- [GLM-5.3 model card](https://huggingface.co/zai-org/GLM-5.3)
- [DeepSeek-V4.1-Flash paper (arXiv 2609.19969)](https://arxiv.org/html/2609.19969)
- [Datacurve – DeepSWE v1.1](https://deepswe.datacurve.ai/blog/deepswe-v1-1)
- [Mercor APEX DeepSWE leaderboard](https://www.mercor.com/apex/oss-benchmarks/oss-deep-swe-leaderboard/)
- [deepswe-tracker (GitHub)](https://github.com/lprhodes/deepswe-tracker)
- [Epoch AI – DeepSWE review](https://epoch.ai/benchmarks/deepswe/review)
- [llm-stats – DeepSWE 1.1](https://llm-stats.com/benchmarks/deepswe-1.1)
- [llm-stats – Terminal-Bench 2.1](https://llm-stats.com/benchmarks/terminal-bench-2.1)
- [BenchLM – Terminal-Bench 2.1](https://benchlm.ai/benchmarks/terminalbench21)
- [DeepInfra – GLM-5.3](https://deepinfra.com/zai-org/GLM-5.3)
- [InferenceX – GLM-5.3](https://inferencex.semianalysis.com/model/glm-5-3)
- [DataLearner – GLM-5.3](https://www.datalearner.com/en/ai-models/pretrained-models/glm-5-3)
- [CometAPI – DeepSeek V4.1 Flash](https://www.cometapi.com/de/models/deepseek/deepseek-v4-1-flash/)
