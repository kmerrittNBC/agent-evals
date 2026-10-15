## Compatibility summary — as of October 14, 2026

The declared versions are compatible on **TypeScript**. The recommended Node range is also clear: use **Node 24.15.0 or later in the 24.x line**. The repository already pins **Node 24.16.0**, and its CI workflows read that pin from `.nvmrc`.

| Component | Documented compatibility | Assessment |
|---|---|---|
| **Angular 22.1.7** | Angular’s compatibility table gives TypeScript `>=6.0.0 <6.1.0` and Node `^22.22.3`, `^24.15.0`, or `^26.0.0`. | TypeScript **6.0.3** fits. Node **24.16.0** fits. |
| **Nx 23.2.1** | Nx’s current Node guidance lists `^22.12.0`, 24.x, and 26.x for Nx 23.x. Its TypeScript guidance lists `>=5.8.0 <7.1.0`. | TypeScript **6.0.3** and Node **24.16.0** fit. |
| **Nx + Angular pairing** | Nx’s Angular matrix lists Angular `~22.1.0` with Nx `>=23.2.0`. | **Nx 23.2.1** matches Angular 22.1.7. |
| **Playwright 1.60** | Its package metadata declares Node `>=18`. | It does not narrow the Node range imposed by Angular and Nx. |

The workspace declares Angular 22.1.7, Nx 23.2.1, TypeScript 6.0.3, and `@playwright/test` `^1.60.0` in [`financial-hq-ui/package.json`](financial-hq-ui/package.json).

## Documentation gaps and conflicts

- **Angular’s version-table label is behind the project’s minor version:** the compatibility table shows a `22.0.x` row, not a separate `22.1.x` row. Its listed TypeScript range includes 6.0.3, but the table does not explicitly label that row 22.1.x.
- **Nx’s launch announcement is broader than its current compatibility guidance:** the Nx 23 launch post says Node 22+ and TypeScript 5.4+. Current Nx compatibility tables give more specific requirements—Node `^22.12.0` or supported 24.x/26.x releases, and TypeScript `>=5.8.0 <7.1.0`. Use the current tables for version selection; treat the launch figures as broad, older guidance.
- **Nx package metadata does not settle the question by itself:** Nx’s compatibility guidance is documented separately from the package’s declared `engines` and peer dependencies. The Nx documentation and Angular/Nx pairing matrix are therefore the relevant compatibility references.
- **The project’s Node type definitions lag its runtime:** `@types/node` is pinned to 18.16.9 while the runtime pin is Node 24.16.0. That is not a runtime incompatibility, but the types may not describe Node 24 APIs accurately; consider updating them to a matching Node 24 release.

## Recommendation

Use **Node 24.16.0 consistently for local development and CI**. It is inside the Angular/Nx overlap, satisfies Playwright, and is already the repository’s chosen version: [`financial-hq-ui/.nvmrc`](financial-hq-ui/.nvmrc) specifies `24.16.0`, and the GitHub Actions workflows use that file for setup. Keep that shared pin rather than selecting different versions locally and in CI. Node 26 is also listed as compatible, but choosing the established Node 24 line avoids moving the default environment to a newer major without a compatibility need.

**References:** [Angular version compatibility](https://angular.dev/reference/versions) · [Nx Node.js guidance](https://nx.dev/docs/technologies/node/introduction) · [Nx TypeScript guidance](https://nx.dev/docs/technologies/typescript/introduction) · [Nx/Angular version matrix](https://nx.dev/docs/kb/angular-nx-version-matrix) · [Nx 23 announcement](https://nx.dev/blog/nx-23-release) · [Playwright 1.60 package metadata](https://raw.githubusercontent.com/microsoft/playwright/v1.60.0/packages/playwright/package.json)
