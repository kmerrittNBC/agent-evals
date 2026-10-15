**Yes—Playwright 1.60 supports both, so no upgrade is needed.** The repo declares `@playwright/test: ^1.60.0` in `financial-hq-ui/package.json:129`.

- **HAR via tracing:** `context.tracing.startHar(path, options?)` and `context.tracing.stopHar()` were added in **v1.60** (released May 11, 2026). This writes a HAR; it’s distinct from the configured `trace: 'retain-on-failure'`, which saves a Playwright trace. The HAR API is a browser-context API and isn’t documented as Chromium-only, though the docs don’t provide a separate engine-by-engine support matrix.
- **Dropping a file:** `locator.drop({ files: ... })` was also added in **v1.60**. It’s documented as cross-browser for Chromium, Firefox, and WebKit. It accepts file paths or in-memory files such as `{ name, mimeType, buffer }`. The drop target must accept the drag—typically by calling `preventDefault()` on `dragover`—or `drop()` throws.

**Implementation recommendation:** Start HAR recording on the test’s `context` with a per-test output path, perform the actions, and call `stopHar()` in a `finally` block. For a drop zone, use `locator.drop({ files: { name, mimeType, buffer } })`. The current Playwright config runs Chrome only, so that covers Chromium; add browser projects only if you want cross-engine coverage.

References: [Tracing API](https://playwright.dev/docs/api/class-tracing) · [Locator API](https://playwright.dev/docs/api/class-locator) · [Release notes](https://playwright.dev/docs/release-notes)
