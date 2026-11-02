# Local Qwen on Linux: IG, DU, and AR

The IG entries are from the original 2026-10-29 run. DU and AR are fresh 2026-10-30 retries after the SSH tunnel was restored. These are separate evaluation runs, not one continuous 15-slot cohort. Each task used the pinned Pi local Qwen arm; web search used Copilot Luna.

| Task | Status | Time (min) | Judge | Completion | Critical errors | Run |
|---|---|---:|---:|---|---:|---|
| IG-01 | completed | 6.2 | 3/5 | partial | 1 | ig-local-qwen-linux-20261029 |
| IG-02 | completed | 4.9 | 4/5 | complete | 0 | ig-local-qwen-linux-20261029 |
| IG-03 | failed | 5.3 | — | — | — | ig-local-qwen-linux-20261029 |
| IG-04 | completed | 5.5 | 3/5 | partial | 1 | ig-local-qwen-linux-20261029 |
| IG-05 | failed | 2.2 | — | — | — | ig-local-qwen-linux-20261029 |
| DU-01 | completed | 3.4 | 5/5 | complete | 0 | du-local-qwen-linux-retry-20261030 |
| DU-02 | completed | 4.4 | 3/5 | partial | 1 | du-local-qwen-linux-retry-20261030 |
| DU-03 | completed | 4.3 | 5/5 | complete | 0 | du-local-qwen-linux-retry-20261030 |
| DU-04 | completed | 5.9 | 4/5 | complete | 0 | du-local-qwen-linux-retry-20261030 |
| DU-05 | completed | 4.7 | 4/5 | partial | 1 | du-local-qwen-linux-retry-20261030 |
| AR-01 | failed | 3.2 | — | — | — | ar-local-qwen-linux-retry-20261030 |
| AR-02 | failed | 6.2 | — | — | — | ar-local-qwen-linux-retry-20261030 |
| AR-03 | failed | 1.5 | — | — | — | ar-local-qwen-linux-retry-20261030 |
| AR-04 | failed | 1.8 | — | — | — | ar-local-qwen-linux-retry-20261030 |
| AR-05 | failed | 0.9 | — | — | — | ar-local-qwen-linux-retry-20261030 |

- IG: 3/5 completed; 3 judged; mean judged quality 3.33/5.
- DU: 5/5 completed; 5 judged; mean judged quality 4.20/5.
- AR: 0/5 completed; no judged answers.

Failed and timed-out slots remain in the denominator. Judge scores summarize only answers the judge could evaluate; they do not assign a zero to infrastructure failures.
