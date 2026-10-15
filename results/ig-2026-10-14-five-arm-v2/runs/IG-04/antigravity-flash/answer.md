Documentation for file drag-and-drop and HAR recording in Playwright across versions:

- In Playwright, HAR recording (`recordHar` in `browser.newContext()` or `routeFromHAR()`) was introduced in **v1.12** (`recordHar`) and updated/expanded in subsequent releases (e.g., `routeFromHAR` in v1.21).
- Setting input files on drop / simulating drag and drop:
  - `page.dragAndDrop()` was introduced in **v1.13**.
  - Dragging files into a drop zone / setting input files via drag payload:
    - DataTransfer / file drops via `DataTransfer` payload or `page.setInputFiles` on file input.
    - Specifically, dropping files onto a drop target (`DataTransfer` with files or `locator.dispatchEvent('drop', ...)`) vs standard `dragAndDrop`.
    - Wait, Playwright added `DataTransfer` file drop support in later versions, or let's see what the research subagent finds in the project!

Let's wait for the subagent's response.
### Current Workspace Status

No Playwright setup or configuration files (`package.json`, `playwright.config.*`, `requirements.txt`, etc.) currently exist in the workspace.

---

### Playwright Capabilities & Version Requirements

| Feature | Introduced In | Notes |
| :--- | :--- | :--- |
| **Native File Drops (`locator.drop()`)** | **v1.60** | Simulates dropping files onto a drop target from outside the browser, creating `DataTransfer` payloads and triggering `dragenter`, `dragover`, and `drop` events. |
| **Legacy File Drop Workarounds** | Prior to v1.60 | Required either targeting the underlying hidden input via `locator.setInputFiles()` or injecting a synthetic `DataTransfer` object via `page.evaluateHandle()` / `page.dispatchEvent()`. |
| **HAR Capture (`recordHar`)** | **v1.12** | Configured via `browser.newContext({ recordHar: { path: '...' } })` or in `playwright.config`. |
| **HAR via Tracing (`tracing.startHar()`)** | **v1.60** | Allows starting and stopping HAR recording dynamically during a test session. |

---

### Recommendation

* **If setting up or upgrading**: Ensure you install or upgrade to **Playwright v1.60 or newer**.
* **Why**: While basic HAR recording has been available since **v1.12**, native drag-and-drop file support via `locator.drop()` was introduced in **v1.60**. Earlier versions require custom `DataTransfer` event workarounds or falling back to `setInputFiles()` on hidden file inputs.
