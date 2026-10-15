**As of October 14, 2026, Node 24 is the best choice for both local development and CI.** The repository already pins **24.16.0** in `financial-hq-ui/.nvmrc`, and its GitHub Actions workflows use that file.

| Component | Documented compatibility relevant to this workspace |
|---|---|
| **Angular 22** | The [Angular compatibility table](https://angular.dev/reference/versions) lists **22.0.x** with Node `^22.22.3 \|\| ^24.15.0 \|\| ^26.0.0` and TypeScript `>=6.0.0 <6.1.0`. TypeScript **6.0.3** fits. |
| **Nx 23** | Nx’s [Node table](https://nx.dev/docs/technologies/node/introduction) lists **26.x, 24.x, and `^22.12.0`**; its [TypeScript table](https://nx.dev/docs/technologies/typescript/introduction) lists **`>=5.8.0 <7.1.0`**. The [Angular–Nx matrix](https://nx.dev/docs/kb/angular-nx-version-matrix) puts Angular **22.1.x** at **Nx ≥23.2.0**, so **23.2.1** meets that minimum. |
| **Playwright 1.60** | Its [package requirement](https://raw.githubusercontent.com/microsoft/playwright/v1.60.0/packages/playwright/package.json) is Node **≥18**; the [installation docs](https://playwright.dev/docs/intro) recommend current releases of Node **22, 24, or 26**. It does not narrow the intersection above. |

**Gaps to keep visible:** Angular’s published table has no separate **22.1.x** row, so applying its 22.0.x Node/TypeScript ranges to 22.1.7 is an inference, not an explicit 22.1 listing. Nx *does* explicitly list the Angular 22.1 pairing. Also, Nx’s broader Node and TypeScript ranges do not override Angular’s tighter requirements: in particular, Node **22.12–22.22.2** meets Nx’s range but not Angular’s listed range, and TypeScript **6.1** is outside Angular’s range.

Keep `.nvmrc` as the shared local/CI source of truth, preferably updating its Node 24 pin to a current **24.x patch** after verification. Node 24 was **Active LTS** on the requested date; Node 22 was Maintenance LTS, while Node 26 was still Current rather than LTS ([Node release schedule](https://github.com/nodejs/Release)). The existing **24.16.0** pin is within the documented ranges, so no major-version change is needed.
