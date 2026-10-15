## Results matrix

Scores below are **reported results**, not a controlled rerun. “Unverified” means I could not establish a sourced score for that cell—not that the model scored zero. Terminal-Bench 2.1 is the 89-task revision of 2.0; DeepSWE v1.1 keeps the same 113 tasks as v1 but changes execution and grading. Those exact variants matter. ([Terminal-Bench 2.1 release](https://www.tbench.ai/news/terminal-bench-2-1); [DeepSWE v1.1 methodology](https://deepswe.datacurve.ai/blog/deepswe-v1-1))

| Model | Terminal-Bench 2.1 | DeepSWE v1.1 |
|---|---|---|
| **GPT-6 Luna** | **Unverified.** I found no sourced score for this model on the exact 2.1 variant. | **66.6%** — reported by **OpenAI**, max effort. OpenAI does not specify the harness or detailed run settings for this score. |
| **GPT-6 Sol** | **Unverified.** I found no sourced score for this model on the exact 2.1 variant. | **68.8%** — reported by **OpenAI**, max effort. Harness and detailed run settings are not specified. |
| **Qwen3.8-27B** | **73.0%** — reported by **Qwen**; the model card labels this **Terminal-Bench 2.1 (Terminus)**. The card does not specify the Terminus version or other run settings. | **42.2%** — reported by **Qwen**, using the **Claude Code harness**, `temperature=1.0`, `top_p=0.95`, and a 256K context window. This is not the DeepSWE leaderboard’s mini-swe-agent setup. |
| **GLM-5.3** | **88.2%** — reported by **Z.ai**, using **Claude Code 2.1.207**, `temperature=1.0`, `top_p=1`, `max_new_tokens=65,536`, and a six-hour timeout. | **66.9%** — reported by **Z.ai**, using **mini-swe-agent**, `temperature=0.95`, `top_p=1.0`, a six-hour timeout, and 400K context. **Separate result:** Datacurve’s leaderboard reports **69% ±3%** for GLM-5.3 at max effort on its mini-swe-agent leaderboard. These are different reported runs; settings are not fully aligned or disclosed for both. |
| **DeepSeek V4.1 Flash** | **90.6%** — reported by **DeepSeek**, **DeepSeek Harness Minimal**. DeepSeek also reports **90.3%** with **mini-SWE-agent**. Its cross-scaffold table reports 88.0% Claude Code, 84.1% Codex, 85.0% OpenCode, 86.1% Pi, 85.8% DSH Standard, and 85.8% DSH PTC. | **74.2% resolved** — reported by **DeepSeek**, **mini-SWE-agent**. DeepSeek’s cross-scaffold results are 69.8% Claude Code, 65.6% Codex, 65.5% OpenCode, 66.2% Pi, 72.6% DSH Minimal, 70.5% DSH Standard, and 67.6% DSH PTC. |

### Sources and settings

- **OpenAI:** [GPT-6 Sol and Luna announcement](https://openai.com/index/introducing-gpt-6-sol-and-luna/). It reports the two DeepSWE scores and max effort, but not the harness or a detailed evaluation configuration. OpenAI also notes its evaluations may differ from production due to system prompts and available tools.
- **Qwen:** [Qwen3.8-27B model card](https://huggingface.co/Qwen/Qwen3.8-27B). It names the Terminal-Bench result as Terminus and documents Claude Code settings for DeepSWE.
- **Z.ai:** [GLM-5.3 model card](https://huggingface.co/zai-org/GLM-5.3). Its notes specify the harnesses and settings above. The same card reports 66.9% on DeepSWE; the [Datacurve leaderboard](https://deepswe.datacurve.ai/) separately shows 69% ±3%.
- **DeepSeek:** [DeepSeek V4.1 Flash model card](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash). It reports maximum reasoning effort (`reasoning_effort=100`), `temperature=1.0`, `top_p=0.95`, and 1M context. Across the scaffold comparison, Terminal-Bench uses N=3 samples per task and no network access; DeepSWE uses N=8, Linux containers, and `max_steps=500`.

## What the evidence supports

- **No sourced Terminal-Bench 2.1 comparison is established for GPT-6 Luna or GPT-6 Sol.** Their cells should not be filled by borrowing a different GPT model’s score or a Terminal-Bench 2.0 result.
- **Qwen’s 73.0%, Z.ai’s 88.2%, and DeepSeek’s 90.6% are all attributed results for Terminal-Bench 2.1, but they do not establish a clean model-only ranking.** The harness differs: Qwen names Terminus, Z.ai uses Claude Code, and DeepSeek’s headline is DeepSeek Harness Minimal. DeepSeek’s own scores vary from 84.1% to 90.6% across scaffolds, illustrating why harness matters.
- **The DeepSWE figures are especially unsafe to rank as one uniform table.** The Datacurve leaderboard runs models on mini-swe-agent for consistency. Qwen’s 42.2% uses Claude Code, while OpenAI does not disclose the harness for its GPT-6 scores. DeepSeek’s 74.2% is explicitly a mini-SWE result. Z.ai’s 66.9% and Datacurve’s 69% ±3% are separate reports; the latter’s uncertainty interval overlaps the former, and the runs’ settings are not fully matched.
- **The strongest like-for-like evidence here is within a fixed scaffold**, such as DeepSeek’s own cross-scaffold table or Datacurve’s mini-swe-agent leaderboard. Those comparisons still depend on matching the same benchmark version, effort, and run settings. The evidence does **not** support a definitive all-five-model ranking across either benchmark.
