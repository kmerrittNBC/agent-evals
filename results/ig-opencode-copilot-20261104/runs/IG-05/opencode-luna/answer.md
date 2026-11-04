**No.** The 35 qualification outcomes do not justify ranking the seven arms or saying comparative Stage A is complete. They establish that a bounded **operational qualification** completed; they are not results from the comparative cohort. The README says this explicitly, though its “25-task” description is stale relative to the amended current contract. [README.md:8–11, 27–31](README.md)

### What the qualification establishes

Issue #180 recorded and audited **35/35 outcomes** across seven arms and five Python projects: 31 passes, three verifier failures, one eligible timeout, and no unresolved slots. The run involved 36 attempts because an original infrastructure-failed attempt was retained separately. It also spanned documented repair revisions. The final evidence says the solve rate was not the operational gate’s acceptance criterion, and these results “do not support a comparative ranking or numerical freeze.” [docs/evidence/current-qualification-180-final.md:3–15, 41–52](docs/evidence/current-qualification-180-final.md)

The qualification does provide evidence that the shared execution path—task preparation, candidate capture, cleanup/quiescence, independent verification, and result recording—worked for that five-project check. It does **not** qualify the MultiLang-specific parser and compiled-language resource requirements, or Stage B. [README.md:15–20](README.md); [docs/runbooks/current-qualification.md:28–30, 174–179](docs/runbooks/current-qualification.md)

The seven-arm pass counts might look sortable, but the README and final report explicitly classify them as operational evidence, not comparative results. They are five Python-project outcomes, not trials on the frozen Stage A corpus.

### What the current comparative cohort requires

There are two task counts to reconcile:

- The README’s “25-task” wording reflects the selected MultiLang corpus.
- The current v5 amendment screens the **23-task reviewed archive subset**: two of the 25 selected tasks were left unresolved and dropped without replacement. The effective schedule is **23 tasks × 7 standard arms × 1 attempt = 161 slots**, not 175. ADR-0016 explicitly supersedes the earlier 25-task/175-slot count; the v5 contract carries that amendment. [docs/authoritative/adr/0016-screen-stage-a-on-23-reviewed-tasks.md:10–15, 39–43, 108–123](docs/authoritative/adr/0016-screen-stage-a-on-23-reviewed-tasks.md); [docs/contracts/staged-multilang-benchmark-v5.md:13–20, 38–46](docs/contracts/staged-multilang-benchmark-v5.md)

- Stage A must run the full frozen schedule under one admitted configuration and owner-approved numerical freeze. The 23-task cohort advances through its blocks continuously; a non-clean block stops it. After every slot is terminal or explicitly unstarted, an offline audit precedes the seal. [docs/authoritative/adr/0016-screen-stage-a-on-23-reviewed-tasks.md:51–65, 83–89](docs/authoritative/adr/0016-screen-stage-a-on-23-reviewed-tasks.md); [docs/runbooks/stage-a-continuous-cohort.md:3–19, 21–42](docs/runbooks/stage-a-continuous-cohort.md)

- The freeze is more than a task list: v5 requires exact arm and runtime identities, corpus and verifier, policy, schedule, budgets/resources, window, admissions, outcome-slot plan, and owner approval. The v5 document is a prospective contract—not itself an actual numerical freeze or execution authorization. [docs/contracts/staged-multilang-benchmark-v5.md:3–10, 22–36](docs/contracts/staged-multilang-benchmark-v5.md)

Even a completed screening report is not a precise league table. It must report denominators, missingness, uncertainty and paired comparisons; one task is 1/23 of an arm’s denominator. The futility rule is an absolute near-total-failure threshold, not a relative ranking. [docs/contracts/staged-multilang-benchmark-v5.md:240–271, 348–373](docs/contracts/staged-multilang-benchmark-v5.md)

### What remains unverified

The retained comparative execution evidence does not show a completed 161-slot cohort, full audit, Stage A seal, or screening report. For example, attempt 6 stopped after 28 slots: 15 results (12 passes, three failures), 13 infrastructure-failed/unknown slots, and an interrupted in-flight slot. The ledger-transfer record says attempt 6 was retired before the move for attempt 7; ADR-0027 records that attempt 7’s Claude admission probes failed before reaching a provider. These are execution/recovery evidence, not a completed cohort. [docs/evidence/stage-a-cohort-attempt-6-20261008.md:9–28](docs/evidence/stage-a-cohort-attempt-6-20261008.md); [docs/evidence/research-ledger-transfer-cachyos-asrock-to-cachyos-alexander-20261009.md:3–6](docs/evidence/research-ledger-transfer-cachyos-asrock-to-cachyos-alexander-20261009.md); [docs/authoritative/adr/0027-hand-the-agent-its-files-without-crossing-into-mounts.md:14–18](docs/authoritative/adr/0027-hand-the-agent-its-files-without-crossing-into-mounts.md)

Accordingly, the cited evidence does **not** verify a seven-arm ranking, Stage A completion, futility dispositions or survivor set, or Stage B results. Stage B requires the sealed Stage A disposition and report, then a separately frozen cohort on new tasks; its results are not pooled with Stage A. [docs/contracts/staged-multilang-benchmark-v5.md:38–61, 273–298](docs/contracts/staged-multilang-benchmark-v5.md)

One more source of confusion: the September 2026 freeze publication describes an approved **historical 25-task numerical freeze**, but says the whole issue was not complete and that no comparative slot had run at that point. That approval cannot be read as evidence of a finished cohort, and it does not change the later 23-task amendment. [docs/evidence/stage-a-unsigned-review-50-20260920.md:14–38, 40–45](docs/evidence/stage-a-unsigned-review-50-20260920.md)

This was a read-only inspection; no files were changed.
