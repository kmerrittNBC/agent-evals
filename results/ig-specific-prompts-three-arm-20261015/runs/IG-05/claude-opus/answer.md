The stack is compatible, and the repo's `.nvmrc` already selects a valid Node version (24.16.0). The problems are stale repo docs and a few smaller mismatches. **I recommend Node 24 LTS for both local development and CI.** All of this comes from reading files and published docs and npm metadata. I didn't install anything, build, or run tests (there's no `node_modules`).

## Documented requirements

| Component (version locked in `yarn.lock`) | Node.js | TypeScript | Other |
|---|---|---|---|
| Angular 22.1.7 / `@angular/build` & CLI 22.1.8 (npm `engines`) | `^22.22.3 \|\| ^24.15.0 \|\| >=26.0.0` | `>=6.0 <6.1` | — |
| Nx 23.x (Nx compatibility matrix) | 26.x, 24.x, `^22.12.0` | Nx 23.1+ supports TS 6 (release post) | Angular ~22.1 needs Nx ≥23.2.0 |
| `@nx/angular` 23.2.1 (npm peer deps) | no `engines` field | — | `@angular-devkit/*`, `@angular/build`, `ng-packagr` `>=20 <23` |
| Playwright 1.60.0 | docs: "latest 22.x, 24.x or 26.x"; npm `engines`: `>=18` | — | — |
| jest-preset-angular 17.0.0 | `^20.11.1 \|\| >=22.0.0` | `>=5.8` | Angular `>=20 <23` |
| ts-jest 29.4.12 | `>=20` | `>=4.3 <7` | — |

The safe Node range is the overlap of all of these: **`^22.22.3 || ^24.15.0 || ^26`**, and Angular sets that floor. TypeScript 6.0.3 is in Angular's 6.0-only range, and Nx 23.2.1 meets the ≥23.2.0 minimum for Angular 22.1.

Node.js release status today: 20 and 25 are end-of-life, 22 and 24 are LTS (latest v22.23.3 and v24.22.0), and 26 is still "Current". The exact phase dates aren't on the page I fetched. From the published Node schedule, Node 26 should become LTS on about Oct 28, 2026, and Node 22 reaches end-of-life in April 2027.

## Gaps and conflicts

1. **`AGENTS.md` contradicts `.nvmrc`.** `AGENTS.md:35` says `nvm use` selects Node v20.20.0, but `.nvmrc` contains `24.16.0`. Node 20 is end-of-life and fails Angular 22's `engines` check, so anyone or any agent following `AGENTS.md` gets an unsupported runtime.
2. **Nx and Angular disagree on the Node 22 minimum.** Nx documents `^22.12.0`, Angular requires `^22.22.3`. For a Node 22 user, Angular's stricter floor is the one that applies, because Nx itself has no `engines` field.
3. **Angular's docs table lags its packages.** angular.dev only has a `22.0.x` row; 22.1.x isn't listed. The 22.1.7/22.1.8 npm `engines` fields match that row, so they're the authoritative source here.
4. **Playwright's docs and package disagree.** The docs say 22/24/26, but the package declares `>=18`. Follow the docs, since `engines` won't catch an unsupported version.
5. **Nx documentation is thin.** The live Nx Node/TypeScript matrix page returned 404 or empty when I fetched it. The Nx 23.x row above comes from a search-indexed copy, and TypeScript 6 support is only stated in the [Nx 23.1 release post](https://nx.dev/blog/nx-23-1-release), not in a matrix row.
6. **Smaller repo issues:**
   - `@types/node` is pinned to `18.16.9`, which doesn't match a Node 24 runtime.
   - `package.json` has no `engines` field, so nothing enforces the Node floor.
   - `.github/workflows/pull-request.yml:26` uses `actions/setup-node@v3`, while the other workflows use `@v4`.

## Recommendation: Node 24 LTS, the same version locally and in CI

- **Why 24:** It's the only line that meets every documented requirement and has the longest stable support. It's LTS until about April 2028, and it's already what `.nvmrc` and every CI workflow use (they all read `node-version-file: .nvmrc`).
- **Why not 22:** It's allowed only from 22.22.3 up, and it ends support in about six months.
- **Why not 26:** It's allowed, but it isn't LTS yet. Consider adding a non-blocking Node 26 CI job after about Oct 28 to prepare for the next upgrade.
- **Version to pin:** `24.16.0` already satisfies `^24.15.0`. I'd bump `.nvmrc` to the current `24.22.0` to pick up security fixes, keeping an exact version so local and CI match.

Changes I'd make:
- Fix `AGENTS.md:35` to say "Node 24.x, from `.nvmrc`" instead of naming a hard-coded old version.
- Add `"engines": { "node": "^24.15.0" }` (or Angular's full range) to `package.json`.
- Bump `@types/node` to `^24`, and expect possible type fallout.
- Update `pull-request.yml` to `setup-node@v4`.

I haven't edited any files. I can make these changes if you'd like.

Sources:
- [Angular version compatibility](https://angular.dev/reference/versions)
- npm registry metadata: [@angular/core 22.1.7](https://registry.npmjs.org/@angular/core/22.1.7), [@angular/compiler-cli 22.1.7](https://registry.npmjs.org/@angular/compiler-cli/22.1.7), [@angular/build 22.1.8](https://registry.npmjs.org/@angular/build/22.1.8), [@nx/angular 23.2.1](https://registry.npmjs.org/@nx/angular/23.2.1), [nx 23.2.1](https://registry.npmjs.org/nx/23.2.1), [playwright-core 1.60.0](https://registry.npmjs.org/playwright-core/1.60.0), [jest-preset-angular 17.0.0](https://registry.npmjs.org/jest-preset-angular/17.0.0), [ts-jest 29.4.12](https://registry.npmjs.org/ts-jest/29.4.12)
- [Nx–Angular version matrix](https://nx.dev/docs/kb/angular-nx-version-matrix)
- [Nx Node.js compatibility matrix (search-indexed copy)](https://nx.dev/nx-api/workspace/documents/nx-nodejs-typescript-version-matrix)
- [Nx 23.1 release post](https://nx.dev/blog/nx-23-1-release)
- [Playwright installation / system requirements](https://playwright.dev/docs/intro)
- [Node.js releases](https://nodejs.org/en/about/previous-releases)
