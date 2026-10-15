GHSA-w3vv-58gj-gw77 affects the people-and-orgs UI library at Nx 22.7.1, which should go to 22.7.9. The financial HQ UI at Nx 23.2.1 is not affected and needs no change.

## The advisory
- **IDs:** GHSA-w3vv-58gj-gw77 / CVE-2026-104854, in the npm package `nx`.
- **Severity:** High (CVSS v4 8.5). An attacker needs a local account with low privileges, and no user interaction is required. There is no known exploitation in the wild.
- **The problem:** The Nx daemon and its plugin workers talk to each other over Unix sockets. Those sockets sit in a folder under the shared OS temp directory with default permissions, and they have no authentication.
  - The folder name is unique but not secret, so other local users can find it.
  - Another local user who reaches a socket can use the `PROCESS_IN_BACKGROUND` handler to make the daemon load and run a module from an absolute path. That code runs as the daemon's user.
  - Other handlers on the same sockets leak workspace files, the project graph and task hashes.
- **Affected versions:** `>=14.6.0 <22.7.9` and `>=23.0.0 <23.1.2`.
- **Patched versions:** 22.7.9 and 23.1.2.

## Dates
| Event | Date |
|---|---|
| 23.1.2 released (fix, nrwl/nx#36370: "restrict daemon and plugin worker socket access to the owning user") | 2026-08-26 |
| 22.7.9 released (same fix backported) | 2026-09-01 |
| Advisory published on the nrwl/nx repo | 2026-09-11 |
| Published to NVD | 2026-10-02 |
| Added to the GitHub Advisory Database (last updated) | 2026-10-05 |

Both fixes came out before the advisory was published. Neither release note calls the change a security fix, so a team that read only the changelogs could have missed it.

## Is each repo affected?
| Repo | Declared | Lockfile resolves | Affected? |
|---|---|---|---|
| financial-hq-ui | `nx` and all `@nx/*` at 23.2.1 (`package.json:147`) | `nx@23.2.1` (`yarn.lock:9867`) | **No.** 23.2.1 is above 23.1.2. |
| people-and-orgs-ui-library | `nx` and all `@nx/*` at 22.7.1 (`package.json:211`) | `nx@22.7.1` (`pnpm-lock.yaml:7568`) | **Yes.** 22.7.1 is in the `<22.7.9` range. |

## Which environments make it matter
The issue only matters on a machine where **more than one OS user (UID)** can reach the temp directory while Nx is running a command or the daemon is up. That includes:
- **Shared CI runners**, such as self-hosted runners that persist between jobs or are shared by several accounts.
- **Shared build or dev servers**, such as remote dev boxes or jump hosts where several engineers have accounts.
- **Containers or images that run several UIDs** and share `/tmp`.

Turning the daemon off doesn't fully protect you. Plugin worker sockets are used during normal command runs even with `NX_DAEMON=false`.

A single-user laptop or an ephemeral single-tenant VM is not meaningfully exposed.

What I found in these repos:
- **Workflows:** Every job in both repos runs on GitHub-hosted `ubuntu-latest`. Those are throwaway single-tenant VMs, so the risk there is low.
- **Docker build:** The people-and-orgs `Dockerfile` runs Nx only in single-user, root-only build stages. The final image is nginx with no Nx in it.
- **Not covered:** `dev-image.yml` calls an external template (`sportngin/se-actions-workflow-templates`), which I couldn't inspect. The real exposure is wherever this repo runs on self-hosted or shared runners, or on shared dev hosts, so check those.

## Recommendations
**people-and-orgs-ui-library: patch bump from 22.7.1 to 22.7.9.** This is the smallest fixed version, a patch release in the same 22.7 line, so you don't need a major update to 23.x.
```bash
pnpm exec nx migrate 22.7.9
pnpm install
pnpm exec nx migrate --run-migrations   # only if migrations.json was generated
pnpm exec nx reset                      # clears old sockets/dirs, especially on shared hosts
```
Move `nx` and all eight `@nx/*` packages to 22.7.9 together and commit the updated `pnpm-lock.yaml`. Until the update ships, on any shared machine set `NX_SOCKET_DIR` to a directory you own with mode `0700`. The vulnerable versions already honor that setting.

**financial-hq-ui: no update needed.** Keep it at 23.2.1 or later, and don't let it drop below 23.1.2.

Sources:
- [GHSA-w3vv-58gj-gw77](https://github.com/advisories/GHSA-w3vv-58gj-gw77)
- [Nx 22.7.9 release](https://github.com/nrwl/nx/releases/tag/22.7.9)
- [Nx 23.1.2 release](https://github.com/nrwl/nx/releases/tag/23.1.2)
