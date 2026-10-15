**No.** The 35/31 qualification result can't support ranking the seven arms, and it doesn't mean the comparative Stage A is complete. The README and the final evidence both say so. The repository also has no Stage A seal, futility disposition or screening report, and the most recent cohort attempt I found (attempt 11) stopped fail-closed. I inspected the repository read-only and ran nothing.

## What the qualification establishes

Source: `docs/evidence/current-qualification-180-final.md`

- **The counts add up.** Seven arms × five tasks gives 35 outcomes: 31 passes, three verifier failures and one deadline timeout (lines 3–9). There were 36 task attempts, because the original OpenCode/Sol infrastructure failure is kept separately.
- **The tasks are not the benchmark corpus.** They are five SWE-bench Python projects (Astropy, Matplotlib, Requests, Xarray, Pylint), not MultiLang tasks (lines 59–67).
- **It shows the production path works end to end.** The shared `execute_attempt` lifecycle, candidate capture, independent verification, accounting, recovery and cleanup ran across all seven arms, and an offline audit of the retained evidence passed (lines 6–9, 161–170).
- **Solve rate was explicitly not the goal.** "Solve rate is not its infrastructure acceptance criterion… do not support a comparative ranking or numerical freeze" (lines 11–15). The README repeats this at `README.md:27-31`.
- **The failures were investigated.** All three Matplotlib failures are valid but incomplete patches: none changed `OffsetFrom` (lines 87–113). The GLM/Pylint timeout is an eligible, score-zero outcome (lines 127–140).

**Why a ranking from it would be invalid:**
- **The runs were not under one configuration.** Outcomes were produced at four execution revisions, with repairs between them (lines 41–46). The contract requires one cohort under one admitted configuration and one numerical freeze (`staged-multilang-benchmark-v5.md:95-98, 202-213`).
- **The sample is too small.** One task is 20 points of an arm's score here. The spread is four arms at 5/5, two at 4/5 and one at 3/5, which is one or two tasks apart.
- **The contract forbids pooling.** "Screening, expansion, pilot, shakedown and conformance evidence are never pooled" (`v5.md:114`).
- **Stage A isn't a ranking procedure either.** Even the real Stage A screen must not be presented as a precise ranking (`v5.md:246-248, 370-373`). Its only decision rule is the absolute futility gate, `resolved + capability_unknown + unstarted <= 1` (`v5.md:254-272`).

## What the comparative cohort and freeze require

Sources: v5 contract and ADR-0016

- **Corpus:** 23 reviewed archive tasks × 7 arms × 1 repetition = 161 slots, one attempt per slot (`ADR-0016:12-15, 39-43`). ADR-0029 changes the release to `stage-a-prepared-23-v1`.
- **Approval:** an owner-approved numerical freeze, which is the only launch decision. Before it come fresh admission of all seven arms and a reconciled research and provider capacity plan (`ADR-0016:136-138`; `v5.md:130-140`).
- **Execution:** a continuous run from one ledger under one admitted configuration. There is no replay and no ledger reset (`v5.md:202-213`).
- **Audit and seal:** an offline audit of all 161 slots, then issue #24 seals the cohort (`v5.md:225-227`).
- **Disposition:** issue #25 publishes the `stage-a-capability-disposition/1` artifact (161 records) and the screening report, with the required denominators, bounds and uncertainty. The report must state that one task is about 4.35 points (`v5.md:240-272`).

## Where Stage A actually stands

- **Attempt 3** stopped on its first slot (`stage-a-unattended-cohort-271-20261006.md:18-27`).
- **Attempts 4 and 5** stopped too; their stop records are in `docs/evidence/`.
- **Attempt 6** ended 28 of 161 slots: 12 passed, 3 failed and 13 were terminal infrastructure failures, before it stopped on a lost process (`stage-a-cohort-attempt-6-20261008.md:17-28, 143-147`).
- **Attempt 7** failed at Claude admission (`ADR-0027:14-18`).
- **Attempt 11** stopped fail-closed in block 2 on 2026-10-14 (`ADR-0034:10-21`).
- **No seal, disposition or report** exists anywhere in the repository.

## Where the documents disagree

- **`README.md:8-9`** still says a "25-task, seven-arm Stage A". The contract and ADR-0016 now specify 23 tasks and 161 slots, superseding 25 tasks and 175 slots (`ADR-0016:108-117`).
- **`README.md:23`** links `multilang-stage-a-freeze.md`, which describes the old 25-task v3 corpus (lines 5–10). The current procedure is `docs/runbooks/stage-a-continuous-cohort.md`.
- **`docs/contracts/unified-benchmark-roadmap.md`** is out of date: it still says 25 tasks and 175 slots, and lists a `java=2` allocation (lines 18–22, 52, 86–88). The contract's `java=0` allocations override it.
- **`README.md:11`** ("A complete comparative Stage A has not yet been published") is still accurate.

## Still unverified

- **The 35-outcome audit.** It relies on the retained raw evidence on the Alexander host. I didn't run the read-only `ssh` audit (`current-qualification-180-final.md:185-211`). I also didn't check every field of the JSON export against the Markdown, only the headline counts.
- **Attempts 8–10.** I found no dedicated evidence records for them.
- **Live state after 2026-10-14.** The repository can't show whether a later attempt has launched, is running or was sealed.
- **Any claim about relative arm capability.** No comparative claim is supported until a sealed 161-slot cohort and its #25 disposition exist. Even then, the result is a futility screen, not a precise ranking.
