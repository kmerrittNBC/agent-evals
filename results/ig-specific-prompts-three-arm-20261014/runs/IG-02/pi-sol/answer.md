**GHSA-ff3f-86qr-9cv3 is an SSR denial-of-service advisory, not a general client-side Angular Router vulnerability.** Angular [published the advisory](https://github.com/angular/angular/security/advisories/GHSA-ff3f-86qr-9cv3) on **September 23, 2026**; it was [published to the GitHub Advisory Database](https://github.com/advisories/GHSA-ff3f-86qr-9cv3) on **September 30, 2026**.

| Affected `@angular/router` versions | First fixed version |
|---|---|
| `22.0.0` through `<22.2.0` | `22.2.0` |
| `21.0.0` through `<21.2.24` | `21.2.24` |
| `20.0.0` through `<20.3.32` | `20.3.32` |
| `<=19.2.25` | None listed; that line is out of support |

**Runtime conditions:** Exploitation requires Angular SSR on Node.js/V8, attacker-controlled request URLs being parsed by `@angular/router` during SSR, and an upstream path that lets the relevant semicolons and multiple path segments reach it. Crafted numeric matrix parameters can cause excessive memory allocation and crash an SSR worker. A browser-only SPA does not meet the advisory’s SSR condition.

**Confirmed in this repo:** `financial-hq-ui/package.json` declares `@angular/router` **22.1.7**, and `financial-hq-ui/yarn.lock` resolves that version—so the *version* is in the affected range. The five frontend app build targets use browser entry points without configured SSR server entry points (for example, `financial-hq-ui/apps/invoices/project.json`). Their entry points bootstrap in the browser (for example, `apps/invoices/src/main.ts`). `financial-hq-ui/scripts/deploy-static-site.sh` publishes built files to S3 and invalidates CloudFront; `terraform/env/production/main.tf` references static-site infrastructure.

**Assessment and action:** The repo strongly indicates static, client-rendered deployment, so the required Node SSR request-parsing condition **does not appear to apply**. That is an inference from checked-in configuration, **not verification of the live deployment** or every system that might consume its code. Confirm with the deployment owners that no separate SSR service renders these apps or consumes this router version. If there is one, prioritize upgrading the Angular packages together to a compatible **22.2.0 or later** release; edge rejection of semicolons or excessive path depth is an interim mitigation. If deployment is static-only, record this advisory as **version-present but SSR condition not met**, while still planning a routine upgrade.
