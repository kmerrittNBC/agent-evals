I found every DeepSWE score, but the Terminal-Bench numbers can't go in one column. The labs report different versions of it (2.1, 3.0 and 4.0), and their scales are very different: 2.1 scores are in the 70s–90s, while 3.0 and 4.0 scores are mostly below 45. So the matrix gives each version its own column.

| Model | DeepSWE v1.1 | Terminal-Bench 2.1 | Terminal-Bench 3.0 | Terminal-Bench 4.0 |
|---|---|---|---|---|
| **GPT-6 Sol** | 68.8 (max effort)¹ | 83.2 (Vals) | — | 44.4 (Vals)² |
| **GPT-6 Luna** | 66.6 (max effort)¹ | 73.0 (Vals) | — | 13.6 (Vals)² |
| **Qwen3.8-27B** | 42.2 | 73.0 | — | — |
| **GLM-5.3** | 66.9 | — | 28.3 | — |
| **DeepSeek V4.1 Flash** | **74.2** | **90.6** | 30.0 | 31.2³ |

"—" means I couldn't find a published score.

**Where the numbers come from and what to watch for:**
- **DeepSWE:** every score is reported by the company that made the model, and no independent group has re-run them under a single setup. The DeepSWE results show both GPT-6 models are very sensitive to reasoning effort:
  - Sol: 37.2 / 56.6 / 65.3 / 66.6 / 68.8 (low, medium, high, xhigh, max)
  - Luna: 2.4 / 44.5 / 59.3 / 61.3 / 66.6
- **Terminal-Bench for GPT-6:** OpenAI didn't publish any Terminal-Bench scores for Sol or Luna. The figures above come from Vals AI's independent runs at max effort.
- **² Vals disagrees with itself:** its Sept 22 update lists lower Terminal-Bench 4.0 scores than its main table: Sol 34.3, Luna 9.6.
- **³** The DeepSeek 4.0 score comes from a single secondary source, so treat it as soft. Its 2.1 and DeepSWE scores match DeepSeek's technical report and NVIDIA's model card.
- **Qwen3.8-27B:** the numbers come from Alibaba's model card, passed along by blogs. A widely shared claim that it "beats Opus on DeepSWE" is wrong: the Opus cell in that table is blank.
- **Possible mix-up:** GPT-6.1 Sol is a different model. It reportedly scores about 75.2 on DeepSWE, so check which Sol you need.

**Takeaway:** on the numbers available, DeepSeek V4.1 Flash leads both benchmarks. GPT-6 Sol is next, with GLM-5.3 and GPT-6 Luna close together on DeepSWE. Qwen3.8-27B trails, though it's much smaller than the others. Even so, all the DeepSWE scores and most of the Terminal-Bench scores are self-reported, and the labs used different test setups, so the comparison is rough.

Sources:
- [Emergent – GPT-6 Sol benchmarks](https://emergent.sh/learn/gpt-6-sol-benchmarks)
- [Kingy AI – GPT-6 Sol & Luna](https://kingy.ai/blog/gpt-6-sol-luna-specs-benchmarks-pricing-comparison/)
- [Vals AI – GPT-6 Luna](https://www.vals.ai/models/openai_gpt-6-luna)
- [Vals AI – GPT-6 Sol](https://www.vals.ai/models/openai_gpt-6-sol)
- [Artificial Analysis – GPT-6 Sol and Luna](https://artificialanalysis.ai/articles/gpt-6-sol-and-luna-push-the-cost-efficiency-frontier)
- [Emergent – GPT-6.1 Sol](https://emergent.sh/learn/gpt-6-1-sol-benchmarks)
- [Northflank – Qwen3.8-27B](https://northflank.com/blog/qwen3-8-27b-performance-benchmarks-gpu-requirements-and-how-to-run-it)
- [Developers Digest – Qwen3.8-27B vs Opus](https://www.developersdigest.tech/blog/qwen-3-8-27b-local-agentic-coding-2026)
- [Codersera – Qwen3.8-27B](https://codersera.com/blog/qwen-3-8-27b-complete-guide-2026/)
- [Z.ai – GLM-5.3 docs](https://docs.z.ai/guides/llm/glm-5.3)
- [MorphLLM – GLM-5.3](https://www.morphllm.com/glm-5-3)
- [Emergent – GLM 5.3](https://emergent.sh/learn/glm-5-3-benchmarks)
- [DeepSeek-V4.1-Flash technical report (arXiv)](https://arxiv.org/pdf/2609.19969)
- [NVIDIA – DeepSeek-V4.1-Flash model card](https://build.nvidia.com/deepseek-ai/deepseek-v4.1-flash/modelcard)
- [MindStudio – DeepSeek V4.1 Flash](https://www.mindstudio.ai/blog/deepseek-v4-1-flash-benchmarks)
- [MorphLLM – DeepSeek V4](https://www.morphllm.com/deepseek-v4)
