## Declared requirements

| Repository | Root Node engine range | Python / uv |
|---|---|---|
| **RelayView** | `>=22.19 <23 || >=24.11 <25` (`relayview/package.json`). Its README gives the same range. | No root Python version or uv requirement is declared. Some scripts invoke `python`/`python3`, and separate embedding experiments document Python and sometimes uv prerequisites; those are not a general root install requirement. |
| **agent-harness-evals** | `>=22.19.0` (`agent-harness-evals/package.json`). | Python `>=3.12` and uv `==0.12.9` (`pyproject.toml`). `uv.lock` also declares `requires-python = ">=3.12"`. The README says to use `uvx --from uv==0.12.9 uv` if the host uv differs. |

## Locked CLI and browser-test dependencies

- **RelayView:** `package-lock.json` resolves `better-sqlite3` to **13.0.3**; it has an install script and declares Node `>=22`. Browser testing resolves `@playwright/test`, `playwright`, and `playwright-core` to **1.62.1**. RelayView also locks `@earendil-works/pi-tui` at **0.85.0**. Its README describes compatibility with an external Pi CLI **0.85.0**; that external CLI is not itself a root dependency in this lockfile.
- **agent-harness-evals:** `package-lock.json` resolves **Claude Code 2.1.270**, **Pi coding agent 0.85.0**, **Codex 0.144.0**, and **OpenCode 1.18.28** (`opencode-ai` and `@opencode-ai/plugin`). The CLI packages include platform-specific optional packages and/or install scripts. No Playwright dependency appears in this root lockfile.
- **agent-harness-evals Python packages:** `uv.lock` resolves the declared direct dependencies to `inspect-ai` **0.3.261**, `inspect-evals` **0.16.0**, `jsonschema` **4.26.0**, `swebench` **3.0.15**, and dev dependency `pytest` **9.1.1**.

## Shared Node version

The **root package engine ranges alone** overlap starting at Node **22.19.0**. But the lockfiles contain package engine declarations requiring `^22.22.2 || ^24.15.0 || >=26.0.0`—including dependencies in RelayView’s lock and `ini` in agent-harness-evals’ lock. Accounting for those declarations, the lowest shared choice is **Node 22.22.2**. **Node 24.15.0** is another shared choice; Node 24.11 satisfies the roots but not those stricter locked dependency declarations.

## What this evidence does—and does not—show

The package metadata establishes the repositories’ declared engine ranges and Python/uv constraints. The npm lockfiles establish the selected package versions, tarball identities, and recorded package engine metadata; the uv lock establishes resolved Python package versions and artifact hashes. These are useful compatibility constraints, not proof that installation or execution succeeds.

A real install and test run is still needed to check the host’s platform and native build/runtime prerequisites, CLI install behavior, and whether Playwright’s browser binaries are available and usable. For example, RelayView’s npm lock pins the Playwright packages, not evidence that the required browser has been installed and can run on a particular host. The agent-harness-evals README’s prescribed `npm ci --ignore-scripts` also does not test install-script behavior.

The supplied trees did not expose Git metadata, so I treated their checked-in files as the pinned snapshots but could not independently verify their repository commit SHAs.
