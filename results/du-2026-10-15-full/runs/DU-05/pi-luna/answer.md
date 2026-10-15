Updated `agent-evals/src/agent_eval/core.py` so `pack_status` rejects non-list or malformed `repo_facts` with a clear not-ready reason. Each fact must have a nonblank repo name and a 40-character hexadecimal commit hash. Well-formed facts still use the existing pinned-commit comparison.

Added focused coverage in `agent-evals/tests/test_eval_du05.py` for malformed facts and matching versus mismatching pins. No `AGENTS.md` was present.

Checks: `python -m unittest discover -s tests -v` passed all 17 tests; `git diff --check` passed.
