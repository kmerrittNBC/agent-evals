Not yet for most of them. Only 1 of the 12 repos can run Node 26 as a supported setup today. For the rest, the blocker is the Angular version, not Node.

## What blocks us

**1. Angular version (main blocker).** According to the [official compatibility table](https://angular.dev/reference/versions), Node 26 is supported only from Angular 22. Angular 20.x and 21.x stop at `^24.0.0`, and 19.x stops at `^22.0.0`. The table only lists 22.0.x, but since 22.0 supports Node 26, I'm assuming 22.1 does too.

| Repo | Angular | Current `.nvmrc` | Node 26 ready? |
|---|---|---|---|
| se-financial-hq-ui | 22.1.7 (Nx 23.2.1, TS 6.0.3) | 24.16.0 | ✅ Yes |
| se-commerce-ui | 21.2 | 24.16.0 | ❌ Needs Angular 22 |
| people-and-orgs-ui-library | 21.2 | 24.16.0 | ❌ Needs Angular 22 |
| se-product-management-ui | 21.2 | 20.19.0 | ❌ Needs Angular 22 |
| se-financial-admin-ui-library | 21.2 | 22.13.0 | ❌ Needs Angular 22 |
| se-fe-angular-services | 20.3 | 20.19.5 | ❌ Needs 20 → 21 → 22 |
| se-payments-ui | 20.3 | 22.13.0 | ❌ Needs 20 → 21 → 22 |
| se-financial-settings-ui | 20.3 | 22.13.0 | ❌ Needs 20 → 21 → 22 |
| se-financial-reports-ui | 20.3 | 22.13.0 | ❌ Needs 20 → 21 → 22 |
| se-store-ui | 19.2 (TS 5.5) | 20.19.0 | ❌ Needs 3 major versions; 19 is already out of support |
| membership_ui | 19.2, `node-sass` 8 | 18.20.2 | ❌ Same, plus node-sass |
| payments | **8.1.2**, `node-sass` 4, TS 3.4 | 14.21.3 | ❌ Needs a rewrite or a big migration project |

**2. Angular 22 also raises the minimum Node to `^22.22.3 || ^24.15.0 || ^26.0.0`.** The repos pinned to 20.19.x or 22.13.0 will need a newer Node anyway once they move to Angular 22.

**3. `node-sass` in `payments` and `membership_ui`.** It's deprecated and its native bindings won't build on modern Node. You'd need to switch to `sass` (Dart Sass) first, whatever the Node target.

**4. Shared library order.** `se-fe-angular-services` and the `*-ui-library` repos are dependencies of the apps. Their Angular 22 builds need to be released before the apps that use them can move.

**5. Timing.** Node 26 is still "Current" and becomes LTS around Oct 28, 2026 ([devx](https://www.devx.com/coding/nodejs-26-lts-new-features-release-date/), [endoflife.date](https://endoflife.date/nodejs)). Node 24 stays in maintenance until April 2028, so there's no rush.

**6. Other tooling (not checked).** I haven't confirmed Node 26 support for Nx 22.5.x/22.7.x, Karma 6, Cypress 13 (`se-payments-ui`) or older Playwright versions. Nx and Playwright usually just need a version bump alongside Angular 22. Karma is deprecated, so treat it as a risk.

## Recommendation
Standardize on **Node 24.15+ now** as the floor. It's supported by Angular 20, 21 and 22, so every repo except the three legacy ones can switch immediately. Make **Node 26 the target** once each repo is on Angular 22, starting after Node 26 goes LTS at the end of October. `se-financial-hq-ui` can go first as the pilot. Treat `payments` (Angular 8) as its own project; it shouldn't hold up the standard.

Sources:
- [Angular – Version compatibility](https://angular.dev/reference/versions)
- [stackblitz/starters #105 (Angular 22 Node minimums)](https://github.com/stackblitz/starters/issues/105)
- [HeroDevs – Angular/Node compatibility matrix](https://www.herodevs.com/blog-posts/angular-supported-node-js-versions-the-complete-compatibility-matrix)
- [endoflife.date – Node.js](https://endoflife.date/nodejs)
- [DevX – Node.js 26 LTS](https://www.devx.com/coding/nodejs-26-lts-new-features-release-date/)
- [InMotion – Node.js v26 released](https://www.inmotionhosting.com/support/news/nodejs-v26-released/)
