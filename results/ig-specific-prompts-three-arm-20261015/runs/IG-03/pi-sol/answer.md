[GHSA-w3vv-58gj-gw77](https://github.com/nrwl/nx/security/advisories/GHSA-w3vv-58gj-gw77) was published **September 11, 2026**. The fixes had already shipped: [Nx 23.1.2](https://github.com/nrwl/nx/releases/tag/23.1.2) on **August 26, 2026**, and [Nx 22.7.9](https://github.com/nrwl/nx/releases/tag/22.7.9) on **September 1, 2026**.

| Repo | Declared Nx | Advisory status | Smallest appropriate action |
|---|---:|---|---|
| `financial-hq-ui/` | 23.2.1 | **Not affected**; the affected 23.x range ends before 23.1.2. | No update needed for this advisory. |
| `people-and-orgs-ui-library/` | 22.7.1 | **Affected**; the affected 22.x range is `>=14.6.0 <22.7.9`. | Update `nx` and the aligned `@nx/*` packages to **22.7.9**, then regenerate `pnpm-lock.yaml`. No major-version upgrade is necessary. |

The issue is **local**, not a network-only attack: another user on the same machine could access permissively exposed Nx daemon or plugin-worker sockets, potentially obtaining workspace data or running code as the Nx user. It matters most on multi-user development machines and shared or persistent CI hosts/runners where jobs under different local users overlap. An isolated, single-user runner does not present that cross-user scenario. `NX_DAEMON=false` only reduces exposure—plugin-worker sockets can still be used. Until upgraded, the advisory recommends a user-owned, mode-`0700` `NX_SOCKET_DIR`; on shared hosts, run `nx reset` after upgrading to clear old sockets.
