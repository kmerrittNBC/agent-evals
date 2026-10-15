Version 22.1.7 is in the affected range, but this repo shows no sign of the server-side rendering (SSR) setup the exploit needs. I'd treat it as a low-priority upgrade to 22.2.0, not an emergency.

## The advisory (GHSA-ff3f-86qr-9cv3 / CVE-2026-101896)
- **Published:** 23 September 2026. Added to the GitHub Advisory Database on 30 September 2026.
- **Severity:** High, CVSS v4 8.2 (`AV:N/AC:L/AT:P/PR:N/UI:N/VA:H`). It's a denial of service: it can only crash the server, not leak or change data.
- **Package:** `@angular/router` on npm.

| Release line | Affected | Fixed in |
|---|---|---|
| 22.x | >= 22.0.0, < 22.2.0 | **22.2.0** |
| 21.x | >= 21.0.0, < 21.2.24 | 21.2.24 |
| 20.x | >= 20.0.0, < 20.3.32 | 20.3.32 |
| <= 19.2.25 | affected | no fix listed |

- **How it works:** a URL with many path segments carrying numeric matrix parameters (e.g. `/a;990;2522/a;990;2522/...`) makes Node's JavaScript engine reserve a lot of memory for each segment, about 350× the URL's size. A few dozen concurrent requests can crash an SSR worker with "JavaScript heap out of memory."
- **Exploitable only if all of these hold:**
  1. The app uses SSR on Node.js.
  2. The router parses attacker-controlled request URLs on the server.
  3. No upstream proxy strips or rejects URLs containing `;` or very deep paths.
- The advisory says plain browser-only Angular apps are **not affected**.

## What the repo shows (read-only)
**Confirmed:**
- `package.json:56` declares `"@angular/router": "22.1.7"`, and `yarn.lock:312` resolves only that version. **It is in the affected range.**
- There's no SSR anywhere in the repo:
  - No `@angular/ssr`, `@angular/platform-server`, `@nguniversal/*` or `express` dependency.
  - No `server.ts`, `main.server.ts` or `app.config.server.ts`.
  - No SSR settings in any build config.
  - Every app builds with `@angular-devkit/build-angular:application` and only a `browser` entry point (e.g. `apps/invoices/project.json:10-15`).
- **Deployment is static files only.** `scripts/deploy-static-site.sh` uploads the build output to S3 and refreshes the CloudFront cache. The Terraform in `terraform/env/{production,staging}/main.tf` only uses the `tflib-appinfra-static-site` module with `custom_origin_path = "/browser"`. Nothing defines a Node server, container or Lambda.
- The router therefore only ever runs in users' browsers. That breaks condition 1, so conditions 2 and 3 don't matter.

**Assumptions (not verifiable from this repo):**
- Nothing outside this repo renders these bundles on a server. That would mean another service, a different deploy pipeline, or code inside the remote Terraform module that I didn't inspect. The `modals-package-consumer` web-component bundles are the ones to ask about: whoever embeds them could in theory run them in their own SSR app.
- The advisory details come from GitHub's advisory page via a summarizing fetch. I didn't read the patch commits or the GitHub issue/PR (angular/angular#70716 / #70717) directly.

## Recommendation
1. **Treat it as not exploitable in this deployment, and upgrade in a normal release.** Bump all the `@angular/*` 22.1.7 packages together to ≥ 22.2.0 (and the matching 22.1.8 tooling). This clears scanner findings and protects against SSR being added later.
2. **Record the reasoning** wherever you track Dependabot or scanner exceptions, e.g. "SSR not used; static S3/CloudFront delivery."
3. **Before closing it out, confirm** with the platform team or the owners of the embedding apps that nothing renders these bundles on Node.
4. **If you ever add SSR,** upgrade first. As a stopgap, the advisory suggests rejecting URLs containing `;` or more than about 20–30 path segments at the proxy.

Sources:
- [GitHub Advisory GHSA-ff3f-86qr-9cv3](https://github.com/advisories/GHSA-ff3f-86qr-9cv3)
