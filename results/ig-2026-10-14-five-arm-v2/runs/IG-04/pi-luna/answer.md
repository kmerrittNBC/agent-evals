No upgrade needed. The repo is locked to **Playwright 1.60.0** (`financial-hq-ui/package.json`, `financial-hq-ui/yarn.lock`), which supports both:

- **File uploads:** `locator.setInputFiles(...)` for a file input.
- **File drops:** `locator.drop({ files: ... })` to simulate dropping files onto a drop zone.
- **HAR capture:** via the `recordHar` browser-context option, or the newer `context.tracing.startHar()` / `stopHar()` API.

The existing Playwright config doesn’t enable HAR recording, and I found no current use of file-drop or HAR APIs—but the installed version supports them.
