## Declared runtime overlap

| Repository | Node requirement | Other runtime requirements | Relevant locked dependencies |
|---|---|---|---|
| **RelayView** (`f7c03941cf32…`) | `>=22.19 <23 || >=24.11 <25` | No Python or uv requirement is recorded in the cited runtime metadata. | `@playwright/test` and `playwright` **1.62.1**; TypeScript **5.9.3**. |
| **agent-harness-evals** (`b0b31dda6916…`) | `>=22.19.0`, with no declared upper bound | Python **>=3.12**; uv **==0.12.9**. Its Python metadata also pins `inspect-ai==0.3.261` and `inspect-evals[swe-bench]==0.16.0`. | Native CLI packages: `@anthropic-ai/claude-code` **2.1.270**, `@openai/codex` **0.144.0**, `opencode-ai` **1.18.28**, and `@earendil-works/pi-coding-agent` **0.85.0**. |

**The lowest shared Node choice is Node 22.19.0.** The declared overlap is Node `>=22.19.0 <23.0.0` or `>=24.11.0 <25.0.0`. Node 23 is excluded by RelayView’s range.

## What the metadata establishes—and what it doesn’t

The `package.json` files declare Node engine ranges and dependency requirements; the npm lockfiles record resolved package versions. The harness’s `pyproject.toml` declares its Python floor, exact Python dependency pins, and required uv version. These are declarations and version selections—not proof that installation succeeds, native CLI binaries work on a particular OS or architecture, Playwright’s browser can launch, or tests pass.

Those outcomes require a real install and test run in the target environment. In particular, browser binaries and system libraries, native package installation, and the Python/uv environment need to be exercised.

The pinned source references and excerpts are recorded in [`evidence/IG-03/pack.json`](evidence/IG-03/pack.json): RelayView’s `package.json` and `package-lock.json` at `f7c03941cf32b8e25720b5eb1aa91364a236b005`, and agent-harness-evals’ `package.json`, `package-lock.json`, and `pyproject.toml` at `b0b31dda691620edae30db7127c1e1d8da907813`.
