**Not as a blanket change today.** Of the Angular repos I checked, only **`se-financial-hq-ui`** is on Angular 22, whose official compatibility table includes Node 26. The Angular 19–21 repos are not officially supported on Node 26, even where their `package.json` engine range is broad enough to allow it.

| Angular version | Repos | Node 26 status |
|---|---|---|
| 22 | `se-financial-hq-ui` | Supported; currently pinned to Node 24.16.0 |
| 21 | `se-commerce-ui`, `people-and-orgs-ui-library`, `se-product-management-ui`, `se-financial-admin-ui-library` | Not in Angular’s supported Node range |
| 20 | `se-financial-settings-ui`, `se-financial-reports-ui`, `se-payments-ui`, `se-fe-angular-services` | Not in Angular’s supported Node range |
| 19 | `se-store-ui`, `membership_ui` | Not in Angular’s supported Node range |
| 8 | Angular checkout in `payments` | Legacy toolchain; not viable as-is |

**The main blockers:**

- **Angular versions:** Angular 19–21’s supported Node ranges stop at Node 22 or 24, depending on the version. Angular 22 is the first version in this inventory whose official range includes Node 26. An `engines.node: ">=22.13.0"` declaration does not change Angular CLI’s compatibility range.
- **The Angular 8 checkout:** `payments` is pinned to Node 14.21.3 and includes `node-sass@4.13.1` and Angular CLI 8.1.2. That legacy stack needs substantial modernization—or an explicit Node 26 exception.
- **CI/runtime pins:** Most modern workflows take their version from `.nvmrc`, but `membership_ui`’s deploy workflows explicitly use Node 18. Some UI-test workflows also hard-code Node 20 for a separate `hqf-test-automation` checkout; check that project independently if the goal is literally Node 26 in every job.
- **Validation still needed:** `se-financial-hq-ui` is a reasonable pilot: it uses Angular 22 and Nx 23, which supports Node 26. It is currently on 24.16.0, though, so builds, tests, install scripts, and deployment should be exercised on 26 before making it the default. Its `@types/node` is still version 18, which is a typing mismatch to review—not by itself proof of a runtime blocker.

**Recommendation:** Pilot Node 26 in `se-financial-hq-ui`; don’t change every repo’s `.nvmrc` yet. For a blanket policy, first bring the Angular 19–21 apps onto a Node-26-compatible Angular release, and decide whether `payments` is an exception or gets upgraded. Also consider timing: Node 26 is currently the Current release, with Active LTS scheduled for October 2026.

Sources: [Angular’s version compatibility table](https://angular.dev/reference/versions) · [Nx Node.js compatibility](https://nx.dev/docs/technologies/node/introduction) · [Node.js release schedule](https://github.com/nodejs/Release/blob/main/README.md)
