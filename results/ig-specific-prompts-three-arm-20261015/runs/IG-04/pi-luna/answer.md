**Yes—Playwright 1.60 supports both, so you don’t need to upgrade** for either use case, provided the installed `@playwright/test` package is actually 1.60.

- **Record a HAR through tracing:** `tracing.startHar(path, options?)` and `tracing.stopHar()` were added in **v1.60.0**, released **May 11, 2026**. They record network traffic to a HAR artifact; this is separate from the usual Trace Viewer recording. The API is on `BrowserContext.tracing`. Playwright’s HAR-recording options include content, mode, and URL filtering; only one HAR recording can be active per tracing instance. ([release notes](https://playwright.dev/docs/release-notes), [Tracing API](https://playwright.dev/docs/api/class-tracing))  
  *For context:* the older `recordHar` context option predates this tracing-specific API; it was added in v1.23. ([v1.23 release](https://github.com/microsoft/playwright/releases/tag/v1.23.0))

- **Simulate dropping a file:** `locator.drop(payload)` was also added in **v1.60**. It works across Playwright’s Chromium, Firefox, and WebKit engines. It dispatches page-level drag-and-drop events with a synthetic `DataTransfer`, rather than performing an OS-level drag. The drop zone must accept the drag—typically by calling `preventDefault()` in its `dragover` handler—or Playwright treats the drop as rejected. ([Locator API](https://playwright.dev/docs/api/class-locator))

**Implementation recommendation:** start HAR recording before the requests you want captured, and stop it in a `finally` block. For file-drop tests, use a buffer so the test doesn’t depend on a local fixture path, then assert the application’s upload result. For a financial UI, use non-sensitive test data: HARs can contain request and response content, so URL filtering alone should not be treated as redaction.

```ts
await context.tracing.startHar('artifacts/hq.har.zip');
try {
  await page.goto('/upload');
  await page.getByTestId('dropzone').drop({
    files: {
      name: 'statement.csv',
      mimeType: 'text/csv',
      buffer: Buffer.from('date,amount\n2026-01-01,10.00'),
    },
  });
  // Assert the upload result.
} finally {
  await context.tracing.stopHar();
}
```
