**Short answer:** You're on an affected version, but the bug can't be exploited in Financial HQ UI the way it's built. So this isn't urgent. Pick up the fix in your next routine dependency update.

**The advisory:** [GHSA-ff3f-86qr-9cv3](https://github.com/angular/angular/security/advisories/GHSA-ff3f-86qr-9cv3) (CVE-2026-101896), published Sep 23, 2026, rated High (7.5). Numbers placed after semicolons in a URL can make a Node.js server-side rendering (SSR) worker use too much memory and crash.
- Affected: `@angular/router` from 22.0.0 up to (but not including) 22.2.0, with matching ranges on the 21.x and 20.x lines.
- Fixed in: 22.2.0, 21.2.24 and 20.3.32.
- It only affects apps that render on the server. The advisory says apps that run purely in the browser are not vulnerable.

**Financial HQ UI:**
- `financial-hq-ui/package.json:56` pins `@angular/router` to `22.1.7`, and `yarn.lock` resolves to the same version. That is inside the affected range.
- The app doesn't render on the server. There's no `@angular/ssr`, `@angular/platform-server` or Express in its dependencies, and no SSR, server or prerender settings anywhere outside `yarn.lock`. It's a browser-only Nx workspace, so the vulnerable server code never runs.

The three other recent router-related advisories (GHSA-57xq-rjx2-v5xh, GHSA-62vg-58rm-qff7 and GHSA-w739-gvwx-grc3, all Sep 30–Oct 1) are also server-side only, so the same reasoning applies. I didn't check their exact affected versions.

**Recommendation:** Upgrade to 22.2.x in your normal update cycle. It closes the issue and stops security scanners from flagging it.
- Bump every `@angular/*` package together, because they're all pinned to `22.1.7` (the CLI and devkit packages are at `22.1.8`).
- Run the `postinstall` patch scripts and the tests afterwards, since those scripts patch third-party packages for Angular compatibility.

If anyone later adds server-side rendering to this app, or to another app that uses these packages, treat this as urgent and upgrade first.

Sources:
- [GHSA-ff3f-86qr-9cv3 – Angular advisory](https://github.com/angular/angular/security/advisories/GHSA-ff3f-86qr-9cv3)
- [Angular security advisories list](https://github.com/angular/angular/security/advisories)
- [GitHub Advisory Database entry](https://github.com/advisories/GHSA-ff3f-86qr-9cv3)
- [GitLab advisory for @angular/router](https://advisories.gitlab.com/npm/@angular/router/CVE-2026-101896/)
