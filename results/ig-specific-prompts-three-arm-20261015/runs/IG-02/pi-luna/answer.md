## Advisory facts

GHSA-ff3f-86qr-9cv3 was **published September 23, 2026**. It describes a denial of service in `@angular/router`: parsing URLs with numeric matrix parameters can cause excessive memory allocation **when Angular SSR parses attacker-controlled requests on Node.js/V8**. Using Node.js only to build the app does not by itself meet that condition.

Affected ranges and fixes reported by the advisory:

| `@angular/router` range | Fixed version |
|---|---|
| `19.0.0`–`19.2.25` | No patch listed; 19.x is unsupported |
| `20.0.0`–`20.3.31` | `20.3.32` |
| `21.0.0`–`21.2.23` | `21.2.24` |
| `22.0.0`–`<22.2.0` | `22.2.0` |

Source: [Angular’s GHSA-ff3f-86qr-9cv3 advisory](https://github.com/angular/angular/security/advisories/GHSA-ff3f-86qr-9cv3).

## What the repo shows

- **Confirmed:** `financial-hq-ui/package.json` declares `@angular/router` **22.1.7**, which is in the affected range.
- **Confirmed:** `financial-hq-ui/README.md` says all five apps deploy as static sites. `financial-hq-ui/scripts/deploy-static-site.sh` uploads files to S3 and uses CloudFront; the app project configs use browser builds and static serving.
- **Confirmed:** I found no SSR package, server-rendering target, or SSR setup in the searched repo files.

**Assessment:** The dependency version is affected, but the repo’s documented deployment does **not** appear to meet the advisory’s SSR-on-Node runtime condition. A static host serving the browser bundle does not execute Angular Router’s SSR URL parsing.

## Recommendation

Upgrade the Angular packages together to a patched release—**22.2.0 or later**—rather than treating the version finding alone as evidence of an exploitable production issue. Prioritize confirming that the deployed environment matches this repo’s static S3/CloudFront configuration. If any deployment instead runs SSR on Node.js and routes attacker-controlled requests through Angular Router, treat that as exposed and patch promptly.

**Assumption:** This assessment relies on the repo’s deployment documentation and configuration matching the actual production runtime; the repo alone cannot confirm production infrastructure or any external SSR layer.
