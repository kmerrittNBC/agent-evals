**Yes to both, with no upgrade needed.** Both capabilities were introduced in **Playwright 1.60**.

| Use case | API and support |
|---|---|
| Record a HAR through tracing | Use `await context.tracing.startHar('network.har')`, then `await context.tracing.stopHar()` to finalize the file. This records the browser context’s network activity as a **separate HAR**; `tracing.start()` records a Playwright trace, not a HAR. The HAR API is context-level and is not documented as Chromium-only. [Tracing API](https://playwright.dev/docs/api/class-tracing#tracing-starthar) |
| Simulate dropping a file onto an element | Use `await page.locator('#dropzone').drop({ files: 'path/to/file.csv' })`. `locator.drop()` works cross-browser and sends synthetic `dragenter`, `dragover`, and `drop` events; it is not an OS-level drag gesture. The drop target must accept the drop by calling `preventDefault()` during `dragover`, or Playwright throws. [Locator API](https://playwright.dev/docs/api/class-locator#locator-drop) |

**Recommendation:** In the relevant `@playwright/test` test, bracket only the network activity you need with `startHar()`/`stopHar()`, and use `locator.drop()` for the upload zone rather than `dragTo()` (which drags an existing page element). Assert that the application actually processes the file. Both additions are listed in the [1.60 release notes](https://playwright.dev/docs/release-notes#version-160).
