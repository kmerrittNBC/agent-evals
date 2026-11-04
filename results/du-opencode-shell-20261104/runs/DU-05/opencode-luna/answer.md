Updated `src/agent_eval/core.py` to reject malformed `repo_facts` with the clear reason **“judge evidence pack has an invalid repo fact.”** Each fact must be an object with a nonblank repo name and a 40-character string commit. Well-formed facts still use the existing pinned-commit comparison.

Added focused coverage in `tests/test_pack_status_repo_facts.py` for malformed facts and matching/mismatching pins.

**Checks passed:** `python -m unittest discover -s tests` (18 tests) and `git diff --check`. The pre-existing untracked `tests/test_eval_du05.py` was left untouched.
