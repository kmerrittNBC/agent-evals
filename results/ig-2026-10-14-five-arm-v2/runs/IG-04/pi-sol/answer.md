No upgrade is needed. `financial-hq-ui/package.json` specifies `@playwright/test` `^1.60.0`, and `yarn.lock` pins 1.60.0. That version supports both:

- **File drops:** use `page.locator('#dropzone').drop({ files: 'path/to/file' })` for a drag-and-drop target. For a file input, use `setInputFiles()` instead.
- **HAR capture:** start and stop recording around the test with `context.tracing.startHar(testInfo.outputPath('network.har'))` and `context.tracing.stopHar()`, or create a context with `recordHar`.

The current Playwright configs enable failure traces, **not HAR capture**, so you would need to add HAR recording to the relevant tests or fixture. I found no existing file-drop or HAR tests in the repo.
