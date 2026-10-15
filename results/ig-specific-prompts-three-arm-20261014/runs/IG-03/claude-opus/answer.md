I've confirmed the advisory details and checked both repos' lockfiles and CI setup. Only the people-and-orgs repo is affected, and it needs a patch-level bump.

## GHSA-w3vv-58gj-gw77 (CVE-2026-104854)

**What it is:** In affected Nx versions, the background helper process (the "daemon") and the plugin worker processes talk over Unix sockets in a shared temp directory. That directory has default permissions and the sockets have no authentication. Any other local account on the same machine can connect. Through the daemon's `PROCESS_IN_BACKGROUND` request, that account can make the daemon load a file it wrote and run it as your user. It can also read workspace files, the project graph and task hashes. Severity is High (CVSS 4.0 score 8.5, local attack vector, low privileges needed). The advisory reports no known exploitation.

**Affected:** `nx` from 14.6.0 up to (not including) 22.7.9, and from 23.0.0 up to (not including) 23.1.2. **Fixed in:** 22.7.9 and 23.1.2. The fix is "restrict daemon and plugin worker socket access to the owning user" (nrwl/nx#36370).

**Dates:**

| Event | Date |
|---|---|
| 23.1.2 released | Aug 26, 2026 |
| 22.7.9 released | Sep 1, 2026 |
| Advisory published by Nx maintainers | Sep 11, 2026 |
| Published by NVD | Oct 2, 2026 |
| Added to the GitHub Advisory Database (last updated) | Oct 5, 2026 |

## Is each repo affected?

| Repo | Declared | Version in lockfile | Affected? |
|---|---|---|---|
| `financial-hq-ui` | `nx` 23.2.1 (`package.json:147`) | `nx@23.2.1` in `yarn.lock:9867`; all `@nx/*` packages are 23.2.1 | **No**: 23.2.1 is newer than the 23.1.2 fix |
| `people-and-orgs-ui-library` | `nx` 22.7.1 (`package.json:211`) | `nx@22.7.1` in `pnpm-lock.yaml:7568`; all `@nx/*` packages are 22.7.1 | **Yes**: it's in the 14.6.0 to before-22.7.9 range |

## Which environments matter

The issue only matters when **another local user account can reach the same temp directory while Nx is running**:
- **At risk:** shared CI runners where several jobs or users share one host, shared build or dev servers, and containers running processes under more than one user ID.
- **Not at risk:** single-user laptops and ephemeral single-tenant VMs. All workflows in both repos use GitHub-hosted `ubuntu-latest` runners, which are fresh single-tenant VMs, so risk there is low. The `people-and-orgs-ui-library` Dockerfile build runs everything as root in one container, so risk is low there too.
- **Can't see from here:** `dev-image.yml` calls a shared template (`sportngin/se-actions-workflow-templates/.../build-dev-image.yml@main`), so I couldn't see which runner it uses. Also check whether anyone runs this repo on a shared dev box or a self-hosted runner. Those are the cases where the issue really applies.
- **Turning off the daemon doesn't fully help:** Nx turns the daemon off by default in CI, and neither repo sets `NX_DAEMON` or `useDaemonProcess`. But plugin worker sockets are still created during normal runs, so `NX_DAEMON=false` alone doesn't close the hole.

## Recommendations

**people-and-orgs-ui-library: upgrade to 22.7.9.** This is the smallest fix, a patch release within 22.7.x with no major-version migration.
- Bump `nx` and every `@nx/*` package (`angular`, `devkit`, `eslint`, `eslint-plugin`, `js`, `module-federation`, `plugin`, `workspace`) together to `22.7.9`. The simplest way is `pnpm exec nx migrate 22.7.9`, then `pnpm install`.
- Then check that `pnpm-lock.yaml` resolves `nx@22.7.9`, including the indirect `@nx/jest`, `@nx/rspack`, `@nx/web` and `@nx/webpack` entries.
- On any shared machine that ran the old version, run `nx reset` afterwards so the old sockets are deleted rather than reused.
- If the upgrade has to wait, a stopgap that already works in 22.7.1 is to set `NX_SOCKET_DIR` to a directory you own with mode `0700`.

**financial-hq-ui: no change needed.** 23.2.1 already contains the fix. Just make sure any future pin stays at 23.1.2 or later.

Sources:
- [GitHub Advisory GHSA-w3vv-58gj-gw77](https://github.com/advisories/GHSA-w3vv-58gj-gw77)
- [Nx 22.7.9 release](https://github.com/nrwl/nx/releases/tag/22.7.9)
- [Nx 23.1.2 release](https://github.com/nrwl/nx/releases/tag/23.1.2)
