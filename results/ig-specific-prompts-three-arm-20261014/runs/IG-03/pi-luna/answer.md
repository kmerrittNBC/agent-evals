## Advisory and fixed releases

[GHSA-w3vv-58gj-gw77](https://github.com/nrwl/nx/security/advisories/GHSA-w3vv-58gj-gw77) concerns Nx daemon and plugin-worker sockets that other local users could access. The advisory was published **September 11, 2026**. Its affected ranges are **`>=14.6.0 <22.7.9`** and **`>=23.0.0 <23.1.2`**.

The fixes were released on the two supported branches:

- **Nx 22.7.9** — released **September 1, 2026** ([release](https://github.com/nrwl/nx/releases/tag/22.7.9))
- **Nx 23.1.2** — released **August 26, 2026** ([release](https://github.com/nrwl/nx/releases/tag/23.1.2))

## Assessment and smallest appropriate update

| Repo | Declared Nx | Affected? | Recommendation |
|---|---:|---|---|
| `financial-hq-ui` | `23.2.1` | **No.** It is above the affected 23.x range’s upper bound, `23.1.2`. Its `nx` and `@nx/*` dependencies are also declared at `23.2.1`. | **No security update needed** for this advisory; keep the Nx packages aligned at `23.2.1` or later. |
| `people-and-orgs-ui-library` | `22.7.1` | **Yes.** It is within `>=14.6.0 <22.7.9`. | Smallest branch-preserving update: move `nx` and the declared `@nx/*` packages together to **`22.7.9`**, then regenerate and commit `pnpm-lock.yaml`. |

## When it matters

This is a **local, multi-user** issue: a user who can reach an Nx socket may be able to execute code as the account running Nx. It is most relevant when Nx runs on a host or in a container shared with **other local accounts**, such as some shared CI/build runners or development servers. It is not an application-runtime vulnerability, and a shared CI label alone does not establish exposure—the relevant condition is another local user being able to reach the socket.

Both repos have Nx-based development/build/test commands, including CI-oriented scripts, so evaluate the machines that run those commands. After upgrading on an exposed shared machine, run `nx reset` to clear old sockets.
