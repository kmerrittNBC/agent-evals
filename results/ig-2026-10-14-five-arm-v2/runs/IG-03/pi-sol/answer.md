**One repo needs an Nx update; the other is already past the affected versions.** For the recent Nx-core advisories, `other-angular` pins `nx` and its `@nx/*` packages to **22.5.3** in `package.json` and `yarn.lock`. `financial-hq-ui` pins them to **23.2.1**.

| Repo | Assessment |
|---|---|
| `other-angular` | **Affected version.** `nx@22.5.3` falls within the advisories for [locally accessible daemon/plugin-worker sockets](https://github.com/nrwl/nx/security/advisories/GHSA-w3vv-58gj-gw77), [self-hosted remote-cache Zip-Slip](https://github.com/nrwl/nx/security/advisories/GHSA-vp3h-ghgh-jr7g), and [`nx graph` CORS](https://github.com/nrwl/nx/security/advisories/GHSA-g2r8-wvmj-jf5w). Exploitability depends on use: the socket issue matters on shared hosts; the cache issue requires a self-hosted remote cache; the graph issue requires running `nx graph`. I found no self-hosted remote-cache configuration in its `nx.json` or package manifest. |
| `financial-hq-ui` | **Not affected by those advisories:** its locked `nx@23.2.1` is beyond their patched versions. |

**What to do:** Upgrade `other-angular` to **Nx 22.7.9 or a later compatible 22.x release**, keeping `nx` and the `@nx/*` packages aligned; commit both `package.json` and `yarn.lock`, then run its usual build and tests. If Nx runs on a shared machine or runner, run `nx reset` there after upgrading to remove old sockets. Until upgraded, use a private `NX_SOCKET_DIR` with `0700` permissions on shared hosts; `NX_DAEMON=false` alone does **not** address plugin-worker sockets.

If by “recent issue” you meant the **2025 malicious npm releases (S1ngularity)**, neither *current lockfile* contains a listed malicious Nx version. That cannot rule out a past install on a developer machine or CI runner; check install history before concluding there was no exposure. No files were changed.
