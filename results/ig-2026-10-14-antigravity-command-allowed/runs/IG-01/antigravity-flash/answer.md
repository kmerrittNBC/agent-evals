Here is the benchmark matrix comparing **Terminal-Bench** and **DeepSWE** results across the requested models:

### Benchmark Comparison Matrix

| Model | Provider / Architecture | Terminal-Bench 2.1 | DeepSWE v1.1 | Terminal-Bench 4.0 *(if evaluated)* |
| :--- | :--- | :---: | :---: | :---: |
| **DeepSeek V4.1 Flash** | DeepSeek (Sparse MoE / Causal Enc-Dec) | **90.6%** | **74.2%** | — |
| **GLM-5.3** | Zhipu AI / Z.ai (MoE) | **88.2%** | **66.9%** | 41.8% |
| **GPT-6 Sol** | OpenAI (Mid-tier Reasoning) | **83.15% – 85.4%** | **68.8%** *(75.2% on 6.1)* | 49.4% *(58.2% on 6.1)* |
| **GPT-6 Luna** | OpenAI (Lightweight / High-Throughput) | **73.0%** | **66.6%** | 16.4% |
| **Qwen3.8-27B** | Alibaba (Dense 27B / Hybrid DeltaNet) | **73.0%** | **42.2%** | — |

---

### Key Takeaways & Context

* **DeepSeek V4.1 Flash**: Leads both benchmarks among this group, scoring **90.6%** on Terminal-Bench 2.1 and **74.2%** on DeepSWE v1.1, demonstrating strong efficiency-to-performance scaling with its sparse activation architecture.
* **GLM-5.3**: Demonstrates substantial post-training gains on long-horizon terminal and systems engineering tasks, reaching **88.2%** on Terminal-Bench 2.1 and **66.9%** on DeepSWE v1.1.
* **GPT-6 Sol**: Acts as OpenAI's primary coding workhorse, achieving **83.15%–85.4%** on Terminal-Bench 2.1 and **68.8%** on DeepSWE v1.1 (with the updated **GPT-6.1 Sol** reaching **75.2%** on DeepSWE v1.1 and **58.2%** on Terminal-Bench 4.0).
* **GPT-6 Luna**: Designed for high throughput and lower inference cost; achieves **73.0%** on Terminal-Bench 2.1 and holds up well on repository-level code generation with **66.6%** on DeepSWE v1.1 at maximum reasoning effort.
* **Qwen3.8-27B**: Performs strongly on command-line agent tasks for an open-weight dense 27B model (**73.0%** on Terminal-Bench 2.1), while showing expected limits on multi-file, long-horizon software refactoring (**42.2%** on DeepSWE v1.1).
