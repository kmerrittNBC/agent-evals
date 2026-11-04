Updated `src/agent_eval/core.py` so `tree_digest` includes symlink target text—even for broken links—using a marker and length prefix to avoid ambiguous hash concatenation. Existing path and file-content hashing remains in place.

Added focused coverage in `tests/test_tree_digest_symlinks.py` for broken links and valid links whose targets have identical contents. No `AGENTS.md` was present.

**Checks:** `python3 -m unittest discover -s tests -v` passed all 19 tests; `git diff --check` passed.
