Updated `agent-evals/src/agent_eval/core.py` so `pack_status` rejects non-list `repo_facts` and entries without a nonempty repo name and a 40-character hexadecimal commit hash. It returns a clear malformed-repo-fact reason instead of raising during map construction. Well-formed packs still use the existing pinned-commit comparison.

Added focused coverage in `agent-evals/tests/test_eval_du05.py` for malformed fact shapes and values, plus matching and differing pinned commits. I found no `AGENTS.md` in the workspace.

I couldn’t run the runner tests because this session has no shell or command-execution tool. The planned check is `python3 -m unittest discover -s tests -v`, run from `agent-evals`.
