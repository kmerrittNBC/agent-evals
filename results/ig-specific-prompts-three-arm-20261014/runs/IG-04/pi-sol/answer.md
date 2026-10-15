**Yes to both.** Playwright introduced HAR recording through tracing and external file drops in **v1.60**, so your `@playwright/test` 1.60 installation needs **no upgrade for either use case**.

| Use case | API and support |
|---|---|
| Record a HAR | `await context.tracing.startHar('network.har')`, then `await context.tracing.stopHar()` to write it. This produces a HAR **separately from** a normal trace ZIP. The API docs list no browser-engine restriction; only one HAR recording can be active per tracing instance. [Tracing API](https://playwright.dev/docs/api/class-tracing) |
| Drop a file onto an element | `await page.locator('#dropzone').drop({ files: '/path/to/file.csv' })`. This simulates an external drop using drag events and a `DataTransfer`; it is documented as cross-browser. The drop target must accept the drag (typically by calling `preventDefault()` during `dragover`), or `drop()` throws. [Locator API](https://playwright.dev/docs/api/class-locator) |

**Recommendation:** Scope HAR recording around the relevant test action and stop it in a `finally` block; treat HARs from financial workflows as sensitive artifacts. Use `locator.drop()` for a drop zone, but `setInputFiles()` if the UI exposes a file input. Both additions appear in the [v1.60 release notes](https://playwright.dev/docs/release-notes).
