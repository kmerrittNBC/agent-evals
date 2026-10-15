I'm done: I checked the official docs and release notes against the repo's lockfile and configs. **Version 1.62.1 can do both, so you don't need to upgrade for either one.**

## When each capability was released

| Capability | API | Added in | Date |
|---|---|---|---|
| Record a HAR through tracing | `context.tracing.startHar(path, options?)` returns `Promise<Disposable>`; `tracing.stopHar()` | v1.60 | 11 May (the GitHub page shows no year; 2026 by sequence) |
| Drop a file onto an element | `locator.drop(payload, options?)` | v1.60 | same release |

`package-lock.json` pins `@playwright/test`, `playwright` and `playwright-core` all at 1.62.1, two minor versions past 1.60. Releases since then:
- **1.61:** HAR and trace recordings now include WebSocket requests. You already have this.
- **1.62:** `locator.drop()` gained an AbortSignal option (`signal`). You already have this.
- **1.62.1:** bug fixes only, none touching HAR, tracing or drop.
- **1.63 and 1.64:** nothing changes either API. 1.64 is the latest.

## API details and limits
**`tracing.startHar`**
- **Options:** `content` (`omit`, `embed` or `attach`), `mode` (`full` or `minimal`), `resourcesDir` (only with `attach`, and not with `.zip`), and `urlFilter`.
- **File output:** the file is written when you call `stopHar()` or when the returned Disposable is disposed, which means you can scope it with `await using`. If the path ends in `.zip`, response bodies are stored as separate entries.
- **Limits:** only one HAR recording can run per context at a time. The docs don't list any browser limits, or say anything about Android, Electron or API-request-only contexts.
- **Config:** setting `trace: 'on'` in the config does **not** create a HAR. You have to call the API yourself, or use `recordHar` instead.

**`locator.drop`**
- **Payload:** `files` (a path or paths, or `{name, mimeType, buffer}` objects) and/or `data` (a map from MIME type to string).
- **Options:** `position`, `signal` and `timeout`.
- **How it works:** it fires `dragenter`, `dragover` and `drop` events with a synthetic DataTransfer built inside the page, so the docs say it works in every browser.
- **The catch:** the target's `dragover` handler must call `preventDefault()`. If it doesn't, Playwright fires `dragleave` and the call throws.
- **Not covered by the docs:** they say nothing about custom elements or Shadow DOM. Playwright locators do reach into open shadow roots, though, and Lit components use open ones by default.

## What's in the repo
- There are four configs: `browser/playwright.config.ts`, `browser/showcase.playwright.config.ts`, `browser/workflow.playwright.config.ts` and `spikes/transcript-virtualizer/playwright.config.ts`.
  - All four run Chromium only.
  - None sets `trace`, `recordHar` or `contextOptions`.
  - The spike uses the system browser at `/usr/bin/chromium` rather than Playwright's bundled one.
- No code uses HAR, `drop`, `dragTo` or `setInputFiles` anywhere.
- No component handles `dragover` or `drop` yet. There are many Lit custom elements (`owner-*`), but none is a drop target today.
- `node_modules` isn't installed, so I couldn't check the 1.62.1 type definitions on disk. The version check rests on the docs and the lockfile.

## Recommendation
1. **HAR:** leave the configs alone. Add a small test fixture (or put it in specific tests) that runs `await using har = await context.tracing.startHar(testInfo.outputPath('network.har'), { urlFilter: '**/api/**' })`. That keeps HARs out of every run and saves them next to the other test results. If you ever want a HAR for every test, use `use.contextOptions.recordHar` in the config instead.
2. **Drop:** first, the component needs real drop handling: call `preventDefault()` on `dragover` and read `event.dataTransfer.files` on `drop`. Put the listener on the custom element or on an element inside its shadow root. Then test it with something like `page.locator('owner-…').getByTestId('dropzone').drop({ files: { name, mimeType, buffer } })`. Use `setInputFiles` only if the component wraps a real `<input type=file>`.
3. **Pinning:** keep the lock at 1.62.1. `^1.62.1` already covers 1.60+, so you could pin it exactly if you'd rather not drift to 1.64 on a fresh install. If you keep the system Chromium in the spike, check that its version matches what Playwright 1.62 expects.

Sources:
- [Playwright release notes](https://playwright.dev/docs/release-notes)
- [Tracing API (startHar/stopHar)](https://playwright.dev/docs/api/class-tracing)
- [Locator API (drop)](https://playwright.dev/docs/api/class-locator#locator-drop)
- [GitHub release v1.60.0](https://github.com/microsoft/playwright/releases/tag/v1.60.0)
- [GitHub release v1.62.1](https://github.com/microsoft/playwright/releases/tag/v1.62.1)
- Secondary sources, used only to cross-check: [TestDino 1.60 overview](https://cms.testdino.com/blog/playwright-1-60-release/), [qaskills startHar guide](https://qaskills.sh/blog/playwright-starthar-tracing-guide), [qaskills 1.60 features](https://qaskills.sh/blog/playwright-1-60-release-features), [Playwright Java tracing docs](https://playwright.dev/java/docs/api/class-tracing), [Playwright .NET tracing docs](https://playwright.dev/dotnet/docs/api/class-tracing), [playwright-python 1.60 MR](https://repo1.dso.mil/dsop/edl/playwright-python/-/merge_requests/37), [lilting.ch on MCP browser_drop](https://lilting.ch/en/articles/playwright-mcp-browser-drop-drag-and-drop)
