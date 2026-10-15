I built the matrix below from 6 primary or near-primary sources. Every cell has at least one sourced score, so none is fully unverified. Two pieces are unverified, though: an independent DeepSWE v1.1 score for Qwen3.8-27B, and any OpenAI-reported Terminal-Bench 2.1 score for GPT-6. Few of the numbers can be compared directly across rows; only scores from the same evaluator on the same harness line up.

## Summary matrix

Scores are pass@1 %. Each cell starts with the independent result where one exists, followed by the vendor's own claim.

| Model | Terminal-Bench 2.1 | DeepSWE v1.1 |
|---|---|---|
| **GPT-6 Sol** | **83.15** (Vals, Terminus 2) · vendor: *unverified*, OpenAI published none | **70.5 ±7.2** (Mercor) · vendor 68.8 (OpenAI, max) · not on the Datacurve board |
| **GPT-6 Luna** | **73.03** (Vals, Terminus 2) · vendor: *unverified*, OpenAI published none | **67.0 ±6.8** (Mercor) · 64 (Artificial Analysis) · vendor 66.6 (OpenAI, max) |
| **Qwen3.8-27B** | **58.43** (Vals, Terminus 2) · vendor 73.0 (Qwen, "Terminus") | Vendor only: 42.2 (Qwen, Claude Code). **No independent score: unverified** |
| **GLM-5.3** | **71.54** (Vals, Terminus 2) · vendor 88.2 (Z.ai, Claude Code) | **69 ±3** (Datacurve official) · 70.5 ±6.3 (Mercor) · vendor 66.9 (Z.ai) |
| **DeepSeek V4.1 Flash** | **74.53** (Vals, Terminus 2, 3 trials) · vendor 90.6 (DeepSeek's own harness) | **71.7 ±6.3** (Mercor) · vendor 74.2 (DeepSeek, mini-SWE) · not on the Datacurve board |

## Terminal-Bench 2.1: each score in detail

Terminal-Bench 2.1 has the same 89 tasks as 2.0, with fixes to 28 of them. Most model/agent pairs score higher on 2.1 than on 2.0.

| Model | Score | Reported by | Harness and settings | Comparable? |
|---|---|---|---|---|
| GPT-6 Sol | 83.15 | Vals.ai | Terminus 2 on Daytona, pass@1, time limit rather than turn limit; effort not shown on the benchmark page | Yes, within the Vals set |
| GPT-6 Luna | 73.03 | Vals.ai | Same as above | Yes, within the Vals set |
| Qwen3.8-27B | 58.43 | Vals.ai | Same as above | Yes, within the Vals set |
| Qwen3.8-27B | 73.0 | Qwen (HF model card) | Row label is "Terminal Bench 2.1 (Terminus)". No temperature, timeout or run count given | ⚠️ Settings unknown |
| GLM-5.3 | 71.54 | Vals.ai | Terminus 2 | Yes, within the Vals set |
| GLM-5.3 | 88.2 | Z.ai (HF model card) | Claude Code 2.1.207, temp 1.0, top_p 1, 65,536 max new tokens, 6-hour timeout | ⚠️ Different harness, long timeout |
| DeepSeek V4.1 Flash | 74.53 | Vals.ai | 3 full trials. The model page lists max effort and temp 1 as general settings | Yes, within the Vals set |
| DeepSeek V4.1 Flash | 90.6 | DeepSeek (arXiv 2609.19969, Table 3) | Its own "DeepSeek Harness, Minimal mode", 1M context, temp 1.0, top_p 0.95, N=3, max 500 steps, no network, max effort | ⚠️ Proprietary harness |
| DeepSeek V4.1 Flash | 88.0 | DeepSeek (same paper, Table 4) | Claude Code v2.1.251. Four Claude Code versions average 87.8 | ⚠️ Closest to GLM's setup, but a different Claude Code version and timeout |

Notes:
- **Who has no number.** Artificial Analysis's Terminal-Bench 2.1 page and Snorkel's 2.1 board list none of the five models. Snorkel only lists predecessors such as GPT-5.6 Luna and GLM-5.1. llm-stats lists 0.906, 0.882 and 0.730 for DeepSeek, GLM and Qwen, but marks every entry "self-reported, unverified". Those are copies of the vendor numbers, not separate confirmations.
- **Unconfirmed figure.** One aggregator cites an Artificial Analysis score of 79.8 (xhigh) for Qwen3.8-27B. I could not find it at the source.
- **Benchmark status.** Vals says Terminal-Bench 2.1 has been superseded by 4.0 and is no longer run on new models.

## DeepSWE v1.1: each score in detail

DeepSWE v1.1 is Datacurve's benchmark: 113 tasks, with each agent's committed patch graded in a fresh container. The official board runs every model on mini-swe-agent.

| Model | Score | Reported by | Harness and settings | Comparable? |
|---|---|---|---|---|
| GLM-5.3 | 69 ±3 | **Datacurve official board** | mini-swe-agent, max effort, $3.99/task | Yes. The only official entry among the five |
| GPT-6 Sol | 70.5 ±7.2 | Mercor (via BenchLM, captured Oct 12) | mini-swe-agent, 500-step limit, 2-hour limit, k=3, max effort | Yes, within the Mercor set |
| GPT-6 Luna | 67.0 ±6.8 | Mercor | Same as above | Yes, within the Mercor set |
| GLM-5.3 | 70.5 ±6.3 | Mercor | Same as above | Yes, within the Mercor set |
| DeepSeek V4.1 Flash | 71.7 ±6.3 | Mercor | Same as above | Yes, within the Mercor set |
| GPT-6 Luna | 64 | Artificial Analysis (Sep 22 article) | Max effort; harness not stated | ⚠️ Harness unknown |
| GPT-6 Sol | 68.8 | OpenAI launch charts (via secondary coverage; openai.com returned 403) | Max effort, "OpenAI's research environment", harness not named | ⚠️ Internal harness |
| GPT-6 Luna | 66.6 | OpenAI | Max effort, same caveat. Lower efforts: xhigh 61.3, high 59.3, medium 44.5, low 2.4 | ⚠️ Internal harness |
| GLM-5.3 | 66.9 | Z.ai (HF model card) | mini-swe-agent, temp 0.95, top_p 1.0, 6-hour timeout, 400K context | ~ Same harness as official, different limits |
| DeepSeek V4.1 Flash | 74.2 | DeepSeek (arXiv Table 3) | mini-SWE, N=8, max 500 steps, max effort | ~ Same harness as official |
| DeepSeek V4.1 Flash | 65.5–72.6 | DeepSeek (arXiv Table 4) | Same model on other harnesses: Claude Code 69.8, Codex 65.6, OpenCode 65.5, Pi 66.2, DeepSeek Minimal 72.6 / Standard 70.5 / PTC 67.6 | Shows how much the harness alone moves the score (~9 pts) |
| Qwen3.8-27B | 42.2 | Qwen (HF model card, footnote 3) | **Claude Code**, temp 1.0, top_p 0.95, 256K context; effort and run count not stated | ⚠️ Different harness, no independent check |

Notes:
- **Wrong models on the official board.** Datacurve lists `qwen3.8-max` (57%) and `deepseek-v4-flash` (53%). Those are different models and should not be used for Qwen3.8-27B or V4.1 Flash.
- **GPT-6.1 Sol.** Secondary coverage says it replaced GPT-6 Sol on Sep 29 and scored 75.2 (high effort) on DeepSWE 1.1. Don't mix it up with GPT-6 Sol.
- **Possible grading defects.** A community tracker reports that Epoch AI found grading defects in at least 23 of the 113 tasks. I have this second-hand and did not check it against Epoch's own write-up.

## What comparisons the evidence supports

**Terminal-Bench 2.1:** Vals is the only source that ran all five models on one harness, so that ranking is the only clean one:
- GPT-6 Sol (83.2) is ahead.
- DeepSeek V4.1 Flash (74.5), GPT-6 Luna (73.0) and GLM-5.3 (71.5) sit within 3 points of each other. With 89 tasks, I'd treat that cluster as tied. Vals doesn't publish confidence intervals, so this is my own estimate.
- Qwen3.8-27B (58.4) is clearly last. Its 13–16 point gap is likely real.
- Sol's lead of about 9 points over the cluster is probable but not certain without confidence intervals.

**Vendor Terminal-Bench numbers (90.6, 88.2, 73.0):** these can't be ranked against each other or against Vals. Each vendor used a different harness, and each claim is 15–17 points above the Vals result for the same model. The DeepSeek-vs-GLM "lead" in vendor tables comes from different harnesses, not demonstrated ability. The nearest like-for-like pairing is DeepSeek on Claude Code (88.0) against GLM on Claude Code (88.2), and that looks like a tie, but the Claude Code versions and timeouts differ.

**DeepSWE v1.1:** Mercor ran four of the models on the same harness: DeepSeek 71.7, Sol 70.5, GLM 70.5, Luna 67.0. Their ±6–7 point margins all overlap, so the evidence does not separate them. Two consistency checks hold up:
- GLM-5.3's three scores (official 69, Mercor 70.5, Z.ai 66.9) agree with each other.
- DeepSeek's own 74.2 is within the margin of Mercor's 71.7.

**Not supported:**
- **Qwen3.8-27B on DeepSWE.** The only score is Qwen's 42.2 on Claude Code, with no independent run. DeepSeek's own table shows the harness can move a score by about 9 points, so 42.2 can't be compared against mini-swe-agent numbers. On available evidence it trails clearly, but how far is unknown.
- **OpenAI's DeepSWE numbers** (68.8 / 66.6) come from an unnamed internal harness. Use Mercor's figures to compare GPT-6 models with the others.
- **Mixing versions.** Don't combine these with Terminal-Bench 3.0/4.0 or DeepSWE v1.0 scores, or with GLM-5.3-Flash, Qwen3.8-Max or GPT-6.1 Sol.

**Bottom line:**
- Terminal-Bench 2.1: GPT-6 Sol is ahead, then a three-way tie (DeepSeek V4.1 Flash, GPT-6 Luna, GLM-5.3), then Qwen3.8-27B.
- DeepSWE v1.1: DeepSeek V4.1 Flash, GPT-6 Sol, GLM-5.3 and GPT-6 Luna are statistically indistinguishable. Qwen3.8-27B has only a vendor score.

Sources:
- [Vals.ai – Terminal-Bench 2.1](https://www.vals.ai/benchmarks/terminal-bench-2-1)
- [Vals.ai – DeepSeek V4.1 Flash](https://www.vals.ai/models/deepseek_deepseek-v4.1-flash)
- [tbench.ai – Terminal-Bench 2.1 announcement](https://www.tbench.ai/news/terminal-bench-2-1)
- [Artificial Analysis – Terminal-Bench 2.1](https://artificialanalysis.ai/evaluations/terminalbench-2-1)
- [Snorkel – Terminal-Bench 2.1](https://snorkel.ai/leaderboard/terminal-bench-2-1/)
- [llm-stats – Terminal-Bench 2.1](https://llm-stats.com/benchmarks/terminal-bench-2.1)
- [llm-stats – DeepSWE 1.1](https://llm-stats.com/benchmarks/deepswe-1.1)
- [Datacurve DeepSWE leaderboard](https://deepswe.datacurve.ai/)
- [Datacurve – DeepSWE v1.1 blog](https://deepswe.datacurve.ai/blog/deepswe-v1-1)
- [BenchLM – DeepSWE v1.1 (Mercor)](https://benchlm.ai/benchmarks/mercordeepswe11)
- [DeepSWE 1.1 Tracker](https://www.deepswe.dev/)
- [lprhodes/deepswe-tracker](https://github.com/lprhodes/deepswe-tracker)
- [Respan – DeepSWE v1.1](https://www.respan.ai/models/benchmarks/deepswe-v1-1)
- [Artificial Analysis – GPT-6 Sol and Luna](https://artificialanalysis.ai/articles/gpt-6-sol-and-luna-push-the-cost-efficiency-frontier)
- [Digital Applied – GPT-6 Sol/Luna benchmarks](https://www.digitalapplied.com/blog/gpt-6-sol-luna-launch-pricing-benchmarks-2026)
- [ComputingForGeeks – GPT-6 Sol/Luna](https://computingforgeeks.com/gpt-6-sol-luna-released-features-benchmarks/)
- [Qwen/Qwen3.8-27B model card](https://huggingface.co/Qwen/Qwen3.8-27B)
- [Qubrid – Qwen3.8-27B results](https://www.qubrid.com/blog/qwen38-27b-benchmarks-official-and-independent-results)
- [zai-org/GLM-5.3 model card](https://huggingface.co/zai-org/GLM-5.3)
- [DeepSeek-V4.1-Flash paper (arXiv 2609.19969)](https://arxiv.org/html/2609.19969v1)
