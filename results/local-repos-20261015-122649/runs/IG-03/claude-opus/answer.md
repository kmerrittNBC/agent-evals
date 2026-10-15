## Answer

Going by the declarations, Node 22 and Node 24 can each run both repos:

- **Node 22: 22.22.2 or later** (still below 23)
- **Node 24: 24.15.0 or later** (still below 25)

If you want one version, use **Node 24.15.0**. RelayView already targets Node 24 for its types (`@types/node ^24.2.1`). Node 23, Node 25 and later, and anything below 22.22.2 are ruled out. Node 26 is excluded too: some packages accept `>=26.0.0`, but RelayView's own range and the vendored `@relayview/research-mcp` both stop below 25.

The root `engines` fields don't give you that floor. Both lockfiles contain packages with stricter requirements.

One caveat: this workspace isn't a git repository, so I couldn't confirm that these files match the pinned commits. Everything below is read from the files as they are on disk. I didn't edit, install or run anything.

## Node engine ranges

| | RelayView | agent-harness-evals |
|---|---|---|
| Root `engines.node` | `>=22.19 <23 \|\| >=24.11 <25` (`package.json:87`; README line 47 says the same) | `>=22.19.0` (`package.json:5`; README says "Node 22.19+") |
| Stricter locked dependencies | `jsdom` 30.1.1, `@asamuzakjp/css-color`, `@asamuzakjp/dom-selector`, `w3c-xmlserializer`: `^22.22.2 \|\| ^24.15.0 \|\| >=26.0.0` (`package-lock.json:109,125,2313,3691`). Looser ones it also has: `whatwg-url` `^22.14.0 \|\| >=24`, `html-encoding-sniffer` `^22.13.0 \|\| >=24`, `pdfjs-dist` `>=22.13.0`, `better-sqlite3` `>=22` | `ini` 7.0.0 (pulled in through `effect`, a dependency of `@opencode-ai/plugin`): `^22.22.2 \|\| ^24.15.0 \|\| >=26.0.0` (`package-lock.json:2756`). `@relayview/research-mcp` 1.1.0 (vendored tgz): `>=22.19 <23 \|\| >=24.11 <25` (`:2659`) |
| Effective range | 22.22.2 up to 23, or 24.15.0 up to 25 | 22.22.2 up to 23, or 24.15.0 up to 25 |

Both repos end up with exactly the same range. Even agent-harness-evals' open-ended `>=22.19.0` gets narrowed by its locked dependencies.

## Python and uv

- **agent-harness-evals:**
  - Python: `requires-python = ">=3.12"`, `.python-version` is `3.12`, and `uv.lock` agrees (revision 3, with resolution markers split at 3.14).
  - uv: `[tool.uv] required-version = "==0.12.9"`. If your uv is a different version, the README says to use `uvx --from uv==0.12.9 uv`.
  - Exact pins: `inspect-ai==0.3.261`, `inspect-evals[swe-bench]==0.16.0`, `swebench==3.0.15`, `jsonschema==4.26.0`, plus dev `pytest==9.1.1`.
  - It also requires Docker/Compose.
- **RelayView:** it declares no Python version and has no pyproject, uv lock or `.python-version`. Several scripts still call an interpreter: `verify:first-party-skills-source` uses `python3`, while `test:peerqa`, `test:hybrid*` and `verify:research-mcp:native` use plain `python`. They're optional spike/verification scripts, and their Python requirements are undeclared.

## Locked native CLI and browser-test packages

**RelayView**
- Browser tests: `@playwright/test`, `playwright` and `playwright-core` at 1.62.1 (Node `>=20`). The config uses `chromium`.
- Native addons:
  - `better-sqlite3` 13.0.3 has an install script and builds a native addon.
  - `@napi-rs/canvas` 1.0.9 is an optional dependency of `pdfjs-dist` 6.3.289.
- Build tools with per-platform binaries: `esbuild` 0.28.2, `rolldown` 1.2.4, `lightningcss` 1.33.0. These sit under `vite` 8.2.1, `vitest` 4.1.11 and `tsx` 4.23.12.
- Pi: `@earendil-works/pi-tui` 0.85.0 (`>=22.19.0`).

**agent-harness-evals**
- `@anthropic-ai/claude-code` 2.1.270: `>=22.0.0`, has an install script, its `bin` points to `bin/claude.exe`, and binaries come as per-platform optional dependencies.
- `@openai/codex` 0.144.0: `>=16`, with per-platform binaries installed through npm aliases.
- `opencode-ai` 1.18.28: has an install script, restricted by os/cpu, declares no engines. `@opencode-ai/plugin` is also 1.18.28.
- `@earendil-works/pi-coding-agent` 0.85.0: `>=22.19.0` and ships its own shrinkwrap. This is the same Pi 0.85.0 line that RelayView pins.

## What metadata and lockfiles establish

- They record exactly what each repo declares and what it resolved: package versions, integrity hashes, per-dependency `engines`, os/cpu limits, and which packages run install scripts. That's enough to work out the Node range above, which is fully determined by the files.
- uv itself enforces the pinned uv version. `uv sync --locked` / `uv run --locked` refuse to proceed if the lock is out of date.
- npm does not enforce `engines`. There's no `.npmrc` with `engine-strict`, so `npm ci` only warns (`EBADENGINE`) on an unsupported Node. The range above is the authors' stated support, not something npm checks.

## What still needs a real install or test run

1. **better-sqlite3 on the chosen Node.** It's compiled for a specific Node ABI, and 22 and 24 differ. You need `npm ci` on that Node, then a step that actually loads it. Whether a prebuilt binary exists or it falls back to a node-gyp build (needing a compiler toolchain) only shows up at install time.
2. **Playwright's browser.** The lockfile pins the npm package, not the Chromium build or its system libraries. `npx playwright install chromium` (plus OS dependencies), followed by `npm run test:browser`, is the only real check.
3. **The CLIs with install scripts under `--ignore-scripts`.** agent-harness-evals installs with `npm ci --ignore-scripts` (Makefile and README), but `claude-code` and `opencode-ai` both have install scripts. Whether `claude` and `opencode` work with those scripts skipped needs a real run. `make native-smoke` checks the OpenCode version and that `codex --version` is exactly `codex-cli 0.144.0`. Claude needs its own `--version` check.
4. **Codex as actually used.** The README says the evaluation uses a separately built Codex/Muse runtime ("Do not replace it with stock Codex"). The npm Codex 0.144.0 in the lockfile therefore doesn't define what runs in real evaluations.
5. **Per-platform binaries.** esbuild, rolldown, lightningcss and the CLI optional dependencies are picked for your OS, CPU and libc (glibc or musl) at install time.
6. **Python and Docker.** You need `uv sync --locked` with uv 0.12.9 and a Python 3.12 interpreter, then `make test` / `make smoke`. Docker-backed SWE-bench scoring (the `benchmark_docker` tests) needs a working Docker/Compose host. For RelayView's Python scripts, you'd have to check whether `python` even exists on the host, and what version it is.
7. **Behaviour, not just declarations.** An engine range only says what the authors claim to support. Running `npm run verify:pi-compat` / `npm test` in RelayView and `make check` in agent-harness-evals on the chosen Node is what would actually confirm it.
