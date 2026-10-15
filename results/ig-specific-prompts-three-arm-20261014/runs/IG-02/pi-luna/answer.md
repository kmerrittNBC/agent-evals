## Advisory

**GHSA-ff3f-86qr-9cv3** is a denial-of-service flaw in Angular Router URL parsing. The Angular advisory page says it was published **September 23, 2026**. There is a date discrepancy: the GitHub Advisory Database record reports **September 30, 2026, 15:40 UTC**. [Angular advisory](https://github.com/angular/angular/security/advisories/GHSA-ff3f-86qr-9cv3) · [database record](https://github.com/github/advisory-database/blob/main/advisories/github-reviewed/2026/09/GHSA-ff3f-86qr-9cv3/GHSA-ff3f-86qr-9cv3.json)

Affected and fixed versions:

| Angular line | Affected versions | Fixed version |
|---|---|---|
| 22.x | `>=22.0.0 <22.2.0` | `22.2.0` |
| 21.x | `>=21.0.0 <21.2.24` | `21.2.24` |
| 20.x | `>=20.0.0 <20.3.32` | `20.3.32` |
| 19.x | Through `19.2.25` | No fix listed; that line is unsupported |

The issue is exploitable when a vulnerable router parses attacker-controlled URLs **during SSR on Node.js/V8**. Crafted paths with numeric matrix-parameter names—values following semicolons in path segments—can cause excessive memory allocation; repeated requests can exhaust the server worker’s memory. This is a server-side availability issue, not a browser-only SPA issue.

## What the repository shows

**Confirmed facts:**

- [`package.json`](financial-hq-ui/package.json) declares `@angular/router` as `22.1.7`; [`yarn.lock`](financial-hq-ui/yarn.lock) resolves it to `22.1.7`. That version is in the affected range.
- The app build configurations use browser entry points, and the project files define static serving/deployment targets. [`scripts/deploy-static-site.sh`](financial-hq-ui/scripts/deploy-static-site.sh) uploads built assets to S3 and invalidates CloudFront; [`terraform/env/production/main.tf`](financial-hq-ui/terraform/env/production/main.tf) uses static-site modules.
- I found no Angular SSR package or server-rendering configuration in the repository.

**Assessment and limits:** The checked-in configuration therefore points to client-side apps served as static files, not a Node SSR worker parsing incoming URLs. The advisory’s SSR exploit conditions **do not appear to apply to the deployment architecture represented here**. Repository inspection cannot rule out an untracked or separately operated SSR service or a runtime architecture that differs from these deployment definitions.

## Recommendation

Plan a coordinated Angular upgrade to a supported release that includes **`@angular/router` 22.2.0 or later**, with the usual compatibility checks across Angular packages. The repo does not indicate an SSR-specific emergency exposure, but the declared and locked router version is affected, so update it rather than leaving the vulnerable dependency in place. If a separate Node SSR deployment exists, verify it promptly and treat it as exposed until patched; edge filtering of semicolon paths is only a temporary mitigation.
