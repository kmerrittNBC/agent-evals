## GHSA-w3vv-58gj-gw77

The advisory concerns **Nx daemon and plugin-worker Unix sockets** that may be accessible to other local users. A user who can access those sockets could potentially execute code with the privileges of the account running Nx. This is a **local, shared-host risk**, not an issue that makes a deployed UI vulnerable merely because it was built with Nx.

| Nx version range | Status |
|---|---|
| `>=14.6.0 <22.7.9` | Affected |
| `>=23.0.0 <23.1.2` | Affected |
| `22.7.9` and later in the 22.x line | Fixed |
| `23.1.2` and later in the 23.x line | Fixed |

The advisory was published **September 11, 2026**. The relevant fix releases were **Nx 23.1.2 on August 26, 2026**, and **Nx 22.7.9 on September 1, 2026**. [GitHub advisory](https://github.com/nrwl/nx/security/advisories/GHSA-w3vv-58gj-gw77) · [23.1.2 release](https://github.com/nrwl/nx/releases/tag/23.1.2) · [22.7.9 release](https://github.com/nrwl/nx/releases/tag/22.7.9)

## Relevance and recommended updates

- **`financial-hq-ui`** — `/financial-hq-ui/package.json` declares `nx` and its `@nx/*` packages at **23.2.1**. That is **not affected**: it is newer than the 23.x fix threshold of 23.1.2. **No update is needed for this advisory.**
- **`people-and-orgs-ui-library`** — `/people-and-orgs-ui-library/package.json` declares `nx` and its `@nx/*` packages at **22.7.1**; `/people-and-orgs-ui-library/pnpm-lock.yaml` also locks them to 22.7.1. That is **affected**. The smallest appropriate update is **22.7.9**, keeping `nx` and the Nx plugins/packages aligned at that version and updating the lockfile.

The issue is relevant when Nx runs on a host where **other, untrusted local users** can access its sockets—for example, shared developer machines, shared CI/build servers, or multi-user containers. It is generally not relevant to a single-user workstation or an isolated CI runner without other local users. After upgrading on a shared host, run `nx reset` to clear old daemon state; disabling the daemon alone is not a complete mitigation because plugin-worker sockets are also involved.
