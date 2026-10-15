**Not across all of them yet.** Of the 12 top-level Angular repos here, only `sportsengine/se-financial-hq-ui` is on Angular 22, the version whose [official Node compatibility range includes Node 26](https://angular.dev/reference/versions). Its `.nvmrc` still pins Node 24.16.0, so even that repo needs a tested change rather than just a policy announcement.

The blockers are:

- **Angular versions:** `payments` is on Angular 8; `membership_ui` and `se-store-ui` are on 19; four repos are on 20; and four are on 21. Angular 19–21 do **not** list Node 26 as supported. Those repos would need Angular/toolchain upgrades first.
- **Legacy migration work:** `sportsengine/payments` also has `node-sass` 4.13.1 and a `Dockerfile` based on Node **4.2.6**. This is substantially more than an `.nvmrc` bump.
- **Pins outside `.nvmrc`:** `membership_ui/package.json` explicitly excludes 26 in `engines.node`, and its staging/production workflows select Node 18. Several UI-test workflows hard-code Node 20.
- **Build images and package-manager setup:** `people-and-orgs-ui-library/Dockerfile` defaults to Node 24.16.0 and runs `corepack enable`. [Corepack is no longer bundled starting with Node 25](https://nodejs.org/download/release/v25.8.0/docs/api/corepack.html), so that Docker build needs a separate Corepack installation if moved to 26.
- **Release policy:** Node 26 is currently a *Current* release, not LTS; [Node 24 is LTS](https://nodejs.org/en/about/previous-releases).

**Recommendation:** pilot Node 26 on `se-financial-hq-ui` with install, build, test and deploy checks. For a shared baseline now, Node 24 fits the Angular 20–22 repos, but **not** the Angular 19 or 8 repos; keep exceptions and plan their framework migrations rather than forcing one Node version prematurely.
