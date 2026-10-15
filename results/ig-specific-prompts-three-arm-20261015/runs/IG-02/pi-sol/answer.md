## Confirmed facts

- [GHSA-ff3f-86qr-9cv3](https://github.com/angular/angular/security/advisories/GHSA-ff3f-86qr-9cv3) was published by Angular on **September 23, 2026**. It was published to the [GitHub Advisory Database](https://github.com/advisories/GHSA-ff3f-86qr-9cv3) on **September 30, 2026**.
- The affected `@angular/router` ranges are **≤19.2.25**, **20.0.0–20.3.31**, **21.0.0–21.2.23**, and **22.0.0–22.1.x**. The listed fixes are **20.3.32**, **21.2.24**, and **22.2.0**, respectively; no 19.x fix is listed. This repo declares **22.1.7** in `financial-hq-ui/package.json`, and `financial-hq-ui/yarn.lock` resolves that version.
- Exploitation requires **Node.js/V8 server-side rendering** that passes attacker-controlled request URLs to Angular’s router, with an edge/proxy that permits the crafted semicolon-containing paths. Numeric URL matrix parameters can cause excessive memory allocation and crash an SSR worker. A browser-only SPA does **not** meet the SSR prerequisite.

## Repo assessment and action

The repo **appears to be browser-only**: app build targets specify `browser` entries without SSR/server entries (for example, `financial-hq-ui/apps/orders/project.json` and `apps/docs/project.json`); `financial-hq-ui/scripts/deploy-static-site.sh` uploads built files to S3 and invalidates CloudFront; and `financial-hq-ui/terraform/env/production/main.tf` selects static-site modules. No Node SSR runtime is evident here. **Assumption to verify:** the deployed system follows these configurations and no separate service renders these apps with Angular on Node. A read-only repo inspection cannot establish the live architecture or edge filtering.

**Recommendation:** verify that production and staging do not route requests through an Angular Node SSR service. If they do not, this advisory is **version-applicable but not apparently exploitable in this deployment**; plan an upgrade to **22.2.0 or later**, keeping Angular package versions aligned. If SSR exists elsewhere, prioritize that upgrade and, until deployed, reject the relevant semicolon-containing request paths at the edge.
