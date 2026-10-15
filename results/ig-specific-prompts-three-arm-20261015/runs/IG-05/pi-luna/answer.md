## Compatibility snapshot — October 14, 2026

| Component | Documented requirement | Result for this project |
|---|---|---|
| **Angular 22.1.7** | Angular’s compatibility table gives Node `^22.22.3 || ^24.15.0 || ^26.0.0` and TypeScript `>=6.0.0 <6.1.0`. | Node 24.16.0 and TypeScript 6.0.3 fit. |
| **Nx 23.2.1** | Nx 23 supports Node `^22.12.0`, 24.x, and 26.x; its TypeScript range is `>=5.8.0 <7.1.0`. Nx’s Angular matrix lists Angular 22.1.x with Nx `>=23.2.0`. | Nx 23.2.1 supports this Angular line. The Angular TypeScript range narrows the usable overlap to TypeScript 6.0.x, so 6.0.3 fits. |
| **Playwright 1.60** | Its package engine minimum is Node `>=18`, but that is only a minimum—not a recommendation for a new stack. Playwright’s current guidance favors Node 22, 24, or 26; Node 18 support was deprecated earlier. | Node 24 is a supported, current choice. |

Sources: [Angular compatibility table](https://angular.dev/reference/versions), [Nx Node requirements](https://nx.dev/docs/technologies/node/introduction), [Nx TypeScript requirements](https://nx.dev/docs/technologies/typescript/introduction), [Nx–Angular matrix](https://nx.dev/docs/kb/angular-nx-version-matrix), [Playwright installation guidance](https://playwright.dev/docs/intro), [Playwright package metadata](https://github.com/microsoft/playwright/blob/v1.60.0/packages/playwright/package.json).

## Gaps and documentation conflicts

- **Angular’s table is not granular enough for the declared patch line:** it labels its row `22.0.x`, not `22.1.x`. Nx’s matrix does explicitly cover Angular 22.1.x, and Angular’s published compiler-cli metadata provides the Node and TypeScript constraints. Treat the Angular table as the broad compatibility range, not as evidence that 22.1.7 is unsupported.
- **The tool ranges differ, but their intersection is clear:** Nx permits Node 22 starting at 22.12.0, while Angular requires 22.22.3 or later. So for Node 22, use at least 22.22.3. Node 24 satisfies both sets of requirements.
- **TypeScript’s own Node engine minimum is not the stack’s minimum.** It is much older; Angular, Nx, and Playwright impose the relevant constraints here.
- **The repo pins old Node typings:** [`package.json`](financial-hq-ui/package.json) specifies `@types/node` 18.16.9, despite using a Node 24 runtime. That does not itself prevent running on Node 24, but its type declarations may lag Node 24 APIs. Consider aligning it with the chosen runtime, for example with Node 24 typings.
- **The repo does already select a compatible Node version:** [`.nvmrc`](financial-hq-ui/.nvmrc) is `24.16.0`, and the GitHub workflows read that file through `actions/setup-node`. [`package.json`](financial-hq-ui/package.json) does not declare a Node `engines` range.

## Recommendation

Use **Node 24 LTS**, pinned consistently for local development and CI. The repo’s existing **24.16.0** pin meets Angular’s `^24.15.0` requirement, Nx’s 24.x support, and Playwright’s recommended Node line. It also avoids the narrower Node 22 lower-bound intersection and the risk of adopting Node 26 while it is the newer, non-LTS line on this date. Keep the exact pin in `.nvmrc` and have all CI workflows use it; update `@types/node` to match.
