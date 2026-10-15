Here is the benchmark performance matrix for **Terminal-Bench** (v4.0) and **DeepSWE** (v1.1) across the requested models:

### Benchmark Comparison Matrix

| Model | Developer / Type | Terminal-Bench (4.0) | DeepSWE (v1.1) | Notes & Key Takeaways |
| :--- | :--- | :---: | :---: | :--- |
| **GPT-6 Sol** | OpenAI (Proprietary / Mid-tier) | **49.4% – 58.2%** | **68.8% – 75.2%** | High reasoning tier; scores reach up to 58.2% on Terminal-Bench and 75.2% on DeepSWE with maximum reasoning effort and the GPT-6.1 Sol checkpoint. |
| **GPT-6 Luna** | OpenAI (Proprietary / Utility) | **16.4%** | **66.6%** | Optimized for high-volume cost efficiency. While terminal navigation struggles on complex sandboxes (16.4%), max-effort test-time reasoning yields a competitive 66.6% on multi-file repo debugging. |
| **GLM-5.3** | Z.ai (Open-Weights / Flagship) | **41.8%** *(32.8%–35.8% Flash)* | **69.0%** *(63.4% Flash)* | Strong all-around open-weights model; competes closely with proprietary mid-tier reasoning models on both command-line navigation and software engineering tasks. |
| **DeepSeek V4.1 Flash** | DeepSeek (MoE / Efficient) | **31.2%** | **74.2%** | Standout efficiency-to-performance ratio on repository-level code fixes (74.2% on DeepSWE), though specialized terminal interactions score moderately lower. |
| **Qwen3.8-27B** | Alibaba (Open-Weights / Dense) | **5.6%** | **42.2%** | Compact 27B parameter footprint; serves as an accessible baseline for local deployment, though heavily constrained on complex multi-step terminal actions. |

---

### Key Benchmark Context

* **Terminal-Bench (4.0):** Evaluates autonomous agent capabilities inside sandboxed CLI environments—requiring multi-step tool execution, environment diagnostics, dependency troubleshooting, and systems administration.
* **DeepSWE (v1.1):** Datacurve’s contamination-resistant benchmark evaluating long-horizon software engineering across multi-file repositories in Python, TypeScript, Go, Rust, and JavaScript, scored using functional program verifiers.
