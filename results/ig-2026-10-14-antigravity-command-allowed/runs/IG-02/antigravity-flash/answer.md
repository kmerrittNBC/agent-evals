### Summary & Urgency

* **Do we need to update?** **Yes, eventually**, but primarily for dependency hygiene and to clear security scanner alerts (Dependabot/Snyk). 
* **How urgent is it?** **Low / Non-Urgent.** There is **no immediate threat** and **no emergency release is needed**.

---

### Advisory Details

The recent advisories (**GHSA-62vg-58rm-qff7** and **GHSA-57xq-rjx2-v5xh**) address High-severity Denial of Service (DoS) vulnerabilities in `@angular/router`:

1. **GHSA-62vg-58rm-qff7**: Unmatched empty-path auxiliary outlet route matching can trigger excessive CPU / memory consumption.
2. **GHSA-57xq-rjx2-v5xh**: Memory heap exhaustion caused by `RouterLink` query parameter retention when using `merge` or `preserve`.
3. **Patched Versions**:
   - Angular 22.x: **`22.2.1+`**
   - Angular 21.x: **`21.2.25+`**
   - Angular 20.x: **`20.3.33+`**

---

### Impact on Financial HQ UI

Financial HQ UI is **not affected by the exploit**:

1. **Server-Side Rendering (SSR) Prerequisite**: Both vulnerabilities **only** affect applications running Server-Side Rendering (SSR) on a Node.js server where route matching and link generation run per-request on the server.
2. **Current Architecture**:
   - In [`financial-hq-ui/package.json`](file:///private/var/folders/xx/6423_8894pxc1qvbnrrf87vm0000gp/T/agent-eval-ims4h_c4/workspace/financial-hq-ui/package.json#L46-L56), the workspace uses Angular **`22.1.7`** (which matches the unpatched version range if SSR were present).
   - However, all apps in the monorepo (`orders`, `transactions`, `invoices`, `payment-terms`, `docs`) are configured as pure client-side SPAs using `@angular-devkit/build-angular:application` (e.g. [`apps/orders/project.json`](file:///private/var/folders/xx/6423_8894pxc1qvbnrrf87vm0000gp/T/agent-eval-ims4h_c4/workspace/financial-hq-ui/apps/orders/project.json#L9-L37)) without `@angular/ssr` or `@angular/platform-server`.
   - As documented in [`README.md`](file:///private/var/folders/xx/6423_8894pxc1qvbnrrf87vm0000gp/T/agent-eval-ims4h_c4/workspace/financial-hq-ui/README.md#L17-L22) and implemented in [`scripts/deploy-static-site.sh`](file:///private/var/folders/xx/6423_8894pxc1qvbnrrf87vm0000gp/T/agent-eval-ims4h_c4/workspace/financial-hq-ui/scripts/deploy-static-site.sh), builds are deployed statically to **AWS S3** and served via **CloudFront CDN**. There is no Node.js backend executing route rendering that could crash or experience heap exhaustion.

---

### Recommended Action Plan

* **Routine Maintenance**: Schedule updating `@angular/*` dependencies from `22.1.7` to `22.2.1` (or latest `22.x`) during regular sprint maintenance.
* **Compatibility Check**: When bumping Angular, verify compatibility with the repository's post-install compatibility scripts ([`scripts/patch-se-fe-table-angular-compat.mjs`](file:///private/var/folders/xx/6423_8894pxc1qvbnrrf87vm0000gp/T/agent-eval-ims4h_c4/workspace/financial-hq-ui/scripts/patch-se-fe-table-angular-compat.mjs) and [`scripts/patch-se-fe-modal-angular-21.mjs`](file:///private/var/folders/xx/6423_8894pxc1qvbnrrf87vm0000gp/T/agent-eval-ims4h_c4/workspace/financial-hq-ui/scripts/patch-se-fe-modal-angular-21.mjs)).
