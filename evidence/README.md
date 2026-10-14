# Judge-only evidence

Complete one `pack.json` per task before the full run. Each pack needs a short
reference answer, dated primary sources or preserved source snapshots, the
pinned repository facts, known ambiguity, and decision-changing errors. Keep
this directory outside every agent workspace. The runner checks that no pack
contains placeholder text before `run` or `judge`.

Use `pack.template.json` as a shape guide. Source URLs alone can change after
the information cutoff; save relevant excerpts with retrieval timestamps or
commit a stable snapshot when license and access rules allow it.
