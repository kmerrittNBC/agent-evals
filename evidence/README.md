# Judge-only evidence

Complete one `pack.json` per task before the full run. Each pack needs a
reference answer, dated primary sources or preserved source snapshots, pinned
repository facts, known uncertainty, grading guidance, and decision-changing
errors. The reference answer is one defensible synthesis, not an exhaustive
answer key. `grading_guidance` names decisive checks, acceptable supported
alternatives, and justified uncertainty that should not be penalized. The judge
must distinguish unsupported claims from claims contradicted by evidence.

Keep this directory outside every agent workspace. The runner checks source
and guidance fields, repo commits, and placeholder text before `run` or `judge`.

Use `pack.template.json` as a shape guide. Source URLs alone can change after
the information cutoff; save relevant excerpts with retrieval timestamps or
commit a stable snapshot when license and access rules allow it.
`repo://<name>/<commit>/<path>` locates a file in a pinned repository snapshot
for repo-specific facts; the runner exports that same commit for the agent.
