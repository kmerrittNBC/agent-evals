## Declared runtime requirements

| Repository | Node engine | Python / uv |
|---|---|---|
| **RelayView** | `>=22.19 <23 || >=24.11 <25` in `package.json` and the root entry of `package-lock.json`. Its README repeats these ranges. | No Python or uv requirement is declared for the root npm package. Some scripts and optional components invoke Python; their requirements are specific to those tasks, not a single root-level runtime declaration. |
| **agent-harness-evals** | `>=22.19.0` in `package.json` and its lockfile root entry. | `pyproject.toml` and `uv.lock` require Python `>=3.12`; `.python-version` selects `3.12`. The project requires **uv `==0.12.9`** (`tool.uv.required-version`); the README gives `uvx --from uv==0.12.9 uv` as an alternative when host uv differs. |

**The declared Node overlap is Node 22 from 22.19.0 onward, and Node 24 from 24.11.0 onward.** RelayView excludes Node 23 and Node 25; agent-harness-evals’ broader Node lower bound does not change that intersection.

## Relevant locked dependencies

- **RelayView browser tests:** `@playwright/test`, `playwright`, and `playwright-core` are all locked at **1.62.1**. Its native SQLite dependency, `better-sqlite3`, is locked at **13.0.3** and has an install script. These are npm lockfile resolutions; the Playwright browser binaries are a separate installation concern.
- **agent-harness-evals native CLI/runtime packages:** the npm manifest pins Claude Code **2.1.270**, Pi **0.85.0**, Codex **0.144.0**, and OpenCode **1.18.28** (`opencode-ai` and `@opencode-ai/plugin`). The lockfile resolves these versions and records platform-specific optional packages where applicable.
- **agent-harness-evals Python environment:** `pyproject.toml` pins Inspect AI **0.3.261**, Inspect Evals **0.16.0**, `jsonschema` **4.26.0**, and SWE-bench **3.0.15**; dev dependency pytest is **9.1.1**. `uv.lock` records the resolved packages and artifacts for the locked environment.

## What this establishes—and what it doesn’t

The manifests establish the projects’ declared engine and interpreter constraints, direct dependency specifications, and—alongside their lockfiles—the chosen npm/Python dependency resolutions. Lock entries also record details such as package integrity and, for some packages, engine or platform metadata.

They do **not** prove that installation or execution succeeds on a particular host. In particular, a real install/test is needed to check native-module installation, platform-specific CLI binaries, Playwright browser availability and system libraries, and the Python environment on the target platform. The evals README additionally calls for Linux and Docker/Compose; those are operational requirements beyond the Node engine declaration. No install or test was run for this comparison.

The supplied workspace trees do not include `.git` metadata, so I can compare their checked-in metadata and lockfiles but cannot independently verify the pinned commit hashes.
