I recommend **Node 24 LTS for both local development and CI, pinned to 24.22.0**. The repo's current `.nvmrc` (24.16.0) is already inside every tool's supported range, so nothing is broken. But it is an old patch, and the CI setup and project docs need cleaning up.

## Documented requirements

| Component | Node.js | TypeScript | Source |
|---|---|---|---|
| Angular 22.1.7 (`@angular/core`, `compiler-cli`) | `^22.22.3 \|\| ^24.15.0 \|\| >=26.0.0` | `>=6.0 <6.1` | npm `engines`/`peerDependencies`; angular.dev |
| Angular CLI/build 22.1.8 | same | `>=6.0 <6.1` | `@angular/build` package.json |
| Nx 23.x | 26.x, 24.x, `^22.12.0` | no Nx 23 TypeScript matrix; the Nx 23.1 release post claims "full support for TypeScript 6" | nx.dev Node matrix, 23.1 release post |
| `@nx/angular` 23.2.1 | no `engines` | no TypeScript peer; Angular devkit `>=20 <23` | package.json |
| Nx 23.2.1 ↔ Angular 22.1 | — | — | Nx matrix: Angular `~22.1.0` needs Nx `>=23.2.0` ✅ |
| Playwright 1.60 | docs: "latest 22.x, 24.x or 26.x"; `engines`: `>=18` | — | playwright.dev; package.json |

Node release status on 2026-10-14:
- **Node 22:** maintenance LTS, end of life 2027-04-30.
- **Node 24:** active LTS (latest is 24.22.0). It moves to maintenance on 2026-10-20 and reaches end of life on 2028-04-30.
- **Node 26:** still "Current". It becomes LTS on 2026-10-28.

TypeScript 6.0.3 satisfies Angular's peer range. TypeScript 7 does not: Angular closed the request to support it ([#69704](https://github.com/angular/angular/issues/69704)) as "not planned" for 22.x because it needs a compiler refactor.

## Gaps and conflicting documentation

1. **Angular's table has no 22.1 row.** angular.dev only lists `22.0.x`. The published 22.1.7 packages carry the same ranges, so the package metadata is the real source for 22.1.
2. **`^26.0.0` vs `>=26.0.0`.** angular.dev says `^26.0.0`, but the package `engines` field says `>=26.0.0`. This only matters for Node 27 and later.
3. **The Node 22 floor differs.** Nx accepts `^22.12.0`, but Angular needs `^22.22.3`. The stricter Angular floor is the one that applies.
4. **Playwright contradicts itself.** Its `engines` field says `>=18`, but its docs say "latest 22/24/26". Node 18 and 20 are end-of-life and Angular rejects them anyway, so follow the docs. Note that 1.60 crashes with an unclear error on old Node instead of warning (fixed for 1.61, [#41045](https://github.com/microsoft/playwright/issues/41045)).
5. **Nx documents no TypeScript range for 23.x.** No Nx package declares a TypeScript peer, so Angular's `>=6.0 <6.1` is the effective limit.
6. **Some Nx pages couldn't be read directly.** The Nx Node matrix page returned empty when fetched, so its Nx 23 row comes from search results. Nx 23.3 shipped on Oct 7, so check that page again before relying on it.

## Problems found in the repo

- **`AGENTS.md:35` is out of date.** It says `nvm use` selects Node v20.20.0. Node 20 is end-of-life and Angular 22 won't run on it, so anyone following that file would get a broken setup.
- **One CI job never sets the Node version.** In `.github/workflows/pull-request.yml`, the `lint-test-build` job (lines 44–69) runs lint and tests without `actions/setup-node`. It uses whatever Node the runner image ships, not `.nvmrc`. It also restores `node_modules` from cache with no install if the cache misses. The `setup` job uses `setup-node@v3`; the other workflows use v4.
- **`@types/node` is 18.16.9.** That doesn't match a Node 24 runtime, so type-checking can disagree with the APIs actually available.
- **`nx.json:15` points at a missing file.** `sharedGlobals` references `.github/workflows/ci.yml`, which doesn't exist, so CI config changes never invalidate the Nx cache.
- **No `engines` field.** `package.json` doesn't declare a Node range, so nothing stops installs on an unsupported version.

## Recommendation

1. **Set `.nvmrc` to `24.22.0`.** Node 24 is the only line that every tool documents and that is LTS today. It is the middle of Angular's range and is supported until April 2028. Pinning an exact version keeps local and CI identical. Moving to the latest patch matches Playwright's "latest 24.x" wording and picks up security fixes.
2. **Don't adopt Node 26 yet.** It isn't LTS until Oct 28, and Node itself discourages non-LTS lines for production. Re-evaluate in Q1 2027 once Nx and Playwright have shipped updates against Node 26 LTS.
3. **Don't use Node 22.** It is supported, but only from 22.22.3 and only until April 2027, so it would force another upgrade soon.
4. **Supporting fixes:**
   - Add `setup-node` with `node-version-file: '.nvmrc'` to the `lint-test-build` job, and move all workflows to `setup-node@v4`.
   - Add `"engines": { "node": "^24.15.0" }` to `package.json`.
   - Bump `@types/node` to `^24`.
   - Fix `AGENTS.md`.
   - Point `sharedGlobals` at the real workflow files.
   - Keep TypeScript on `~6.0.3` until an Angular release widens its peer range.

I haven't changed any files. I can make these edits if you want.

Sources:
- [Angular version compatibility](https://angular.dev/reference/versions)
- [Angular issue #69704](https://github.com/angular/angular/issues/69704)
- [@angular/core@22.1.7](https://unpkg.com/@angular/core@22.1.7/package.json), [@angular/compiler-cli@22.1.7](https://unpkg.com/@angular/compiler-cli@22.1.7/package.json), [@angular/build@22.1.8](https://unpkg.com/@angular/build@22.1.8/package.json)
- [Nx and Angular Versions](https://nx.dev/docs/kb/angular-nx-version-matrix)
- [Nx, Node.js and TypeScript Compatibility](https://nx.dev/using-nx/nx-nodejs-typescript-version-matrix)
- [Nx 23.1 release post](https://nx.dev/blog/nx-23-1-release)
- [@nx/angular@23.2.1](https://unpkg.com/@nx/angular@23.2.1/package.json), [nx@23.2.1](https://unpkg.com/nx@23.2.1/package.json), [@nx/js@23.2.1](https://unpkg.com/@nx/js@23.2.1/package.json)
- [Playwright system requirements](https://playwright.dev/docs/intro)
- [playwright-core@1.60.0](https://unpkg.com/playwright-core@1.60.0/package.json)
- [Playwright issue #41045](https://github.com/microsoft/playwright/issues/41045)
- [Node.js release schedule](https://github.com/nodejs/Release)
- [Node.js previous releases](https://nodejs.org/en/about/previous-releases)
