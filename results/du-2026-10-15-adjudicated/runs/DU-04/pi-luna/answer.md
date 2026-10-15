Updated `src/agent_eval/core.py` so `tree_digest` includes each symlink’s target text, including broken links. Existing relative-path and file-content hashing remains unchanged.

Added focused coverage in `tests/test_eval_du04.py` for retargeting both broken links and live links whose targets have identical contents.

**Checks:** `python3 -m unittest discover -s tests -v` — all 17 tests passed, including the runner tests. No `AGENTS.md` was present.
