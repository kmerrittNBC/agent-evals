## Verdict

**Neither repository’s committed dependency resolution contains the malicious Nx versions from the August 2025 npm supply-chain incident.** The issue was in specific published Nx packages, not Angular itself.

- **`financial-hq-ui`** — `package.json` and `yarn.lock` pin Nx and its Nx plugins to **23.2.1**.
- **`other-angular`** — `package.json` and `yarn.lock` pin Nx and its Nx plugins to **22.5.3**.

Those versions are outside the incident’s affected versions. I also found no affected Nx packages such as `@nx/node`, `@nx/key`, or `@nx/enterprise-cloud` in either repository.

## What to do

No dependency change is needed **for this incident based on the current manifests and lockfiles**. To rule out historical exposure, check whether either repo—or Nx Console on a developer machine—installed an affected version during the incident window. Review relevant lockfile history and CI/install logs. If an affected package was installed and its install code ran, follow the incident response guidance: investigate the machine or runner and rotate credentials that may have been accessible there. The current lockfiles alone can’t establish what was installed in the past.

[Official Nx advisory](https://github.com/nrwl/nx/security/advisories/GHSA-cxm3-wv7p-598c)
