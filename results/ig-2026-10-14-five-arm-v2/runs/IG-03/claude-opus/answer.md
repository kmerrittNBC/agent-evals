**Short answer:** The repos themselves aren't affected. The risk is on developer machines, because both repos recommend the compromised VS Code extension.

## What the incident was
On **May 18, 2026** someone published a malicious **Nx Console VS Code extension v18.95.0** (`nrwl.angular-console`). It was live from about 12:30 to 13:09 UTC: roughly 11 minutes on the VS Code Marketplace and 36 minutes on Open VSX. When the extension activated, it stole credentials and installed a backdoor. Nx says the `nx` CLI, the `@nx/*` npm packages and Nx Cloud were **not** affected. The attackers got in through the TanStack npm compromise on May 11.

## What I found
| | financial-hq-ui | other-angular |
|---|---|---|
| Nx version in the yarn.lock | 23.2.1 | 22.5.3 |
| Affected by the 2026 extension incident? | No (npm packages weren't involved) | No |
| Affected by the Aug 2025 "s1ngularity" npm attack? | No (those bad versions were 20.x and 21.x) | No |
| `@tanstack/*` packages in the lockfile | None | None |
| Recommends `nrwl.angular-console` in `.vscode/extensions.json` | **Yes** | **Yes** |

The lockfiles are clean. But both repos prompt developers to install Nx Console, so anyone who had it installed and auto-updating on May 18 may have pulled v18.95.0. A repo can't tell you that. Each person has to check their own machine.

## What to do
1. **Every developer on either repo** (including Cursor and other VS Code fork users) should run:
   ```
   code --list-extensions --show-versions | grep angular-console
   ```
   Then update to **18.100.x or later**. The current release is 18.100.5. An up-to-date version now doesn't rule out having auto-updated through 18.95.0 during the window, so also do step 2.
2. **Check for signs of the malware on macOS/Linux:**
   - `~/.local/share/kitty/cat.py`
   - `~/Library/LaunchAgents/com.user.kitty-monitor.plist`
   - `/var/tmp/.gh_update_state`
   - `/tmp/kitty-*`
   - a `python` process running `cat.py`, or any process with `__DAEMONIZED=1` set
   - on Linux, unexpected entries in `/etc/sudoers`
3. **If anyone was exposed,** treat that machine as compromised:
   - Rotate GitHub, npm, SSH, AWS/GCP, Kubernetes and Vault credentials, plus any 1Password CLI sessions.
   - Rotate secrets in `.env` files. That matters here because other-angular's `ui:tests:setup` script writes SSM secrets to `.env`, and its scripts use `AWS_PROFILE=se-staging`.
   - Think about rebuilding the machine.
4. **Optional hardening:** turn off extension auto-update, or delay it, on dev machines. You could also pin a minimum Nx Console version in your onboarding docs.

No code or lockfile changes are needed in either repo.

Sources:
- [Nx Console v18.95.0 postmortem](https://nx.dev/blog/nx-console-v18-95-0-postmortem)
- [The Hacker News: Compromised Nx Console 18.95.0](https://thehackernews.com/2026/05/compromised-nx-console-18950-targeted.html)
- [GHSA-cxm3-wv7p-598c (2025 Nx npm advisory)](https://github.com/nrwl/nx/security/advisories/GHSA-cxm3-wv7p-598c)
- [StepSecurity: s1ngularity](https://www.stepsecurity.io/blog/supply-chain-security-alert-popular-nx-build-system-package-compromised-with-data-stealing-malware)
- [Aikido: nx packages compromised](https://www.aikido.dev/blog/popular-nx-packages-compromised-on-npm)
- [The Register: Nx packages poisoned](https://www.theregister.com/2025/08/27/nx_npm_supply_chain_attack/)
- [Cloudsmith: NX supply chain attack](https://cloudsmith.com/blog/nx-npm-supply-chain-attack)
