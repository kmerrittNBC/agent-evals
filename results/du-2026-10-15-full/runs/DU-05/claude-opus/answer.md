`pack_status` now returns a clear not-ready reason for malformed `repo_facts` instead of raising `KeyError` or `TypeError`. All 17 runner tests pass, including the new one.

**Change in `src/agent_eval/core.py`:** a new check runs after the grading-guidance check and before the pinned-commit comparison. It returns `(False, "judge evidence pack has a malformed repo fact (needs repo name and 40-character commit)")` when:
- `repo_facts` is not a list, or
- an entry is not an object, or
- an entry's `repo` is missing, not a string, or blank, or
- an entry's `commit` is not exactly 40 hex characters (new `COMMIT_HASH` regex).

Two decisions you may want to revisit:
- **It runs even without a manifest.** The check is structural, so it doesn't depend on a manifest. All five current evidence packs already pass it (IG-01's list is empty; the others have well-formed 40-hex pins).
- **Commits must be hex, not just 40 characters long.** A 40-character non-hex string is rejected. If you only want a length check, the regex is the one line to change.

Well-formed packs go through the same pinned-commit comparison as before.

**New test in `tests/test_runner.py`:** `test_malformed_repo_facts_are_not_ready` covers each malformed shape (missing, blank or wrong-type repo or commit; short or non-hex commit; a non-object fact; a non-list `repo_facts`), both with and without a manifest. It also checks that a well-formed pack is still `ready` and a wrong pin still gives `"repo pin differs for relayview"`.

**Checks:** pytest isn't installed, so I ran `python3 -m unittest tests.test_runner tests.test_eval_du05`. The worktree already had an untracked `tests/test_eval_du05.py` that tests this behaviour; I didn't change it, and it passes too.

There's no AGENTS.md in the repo. Nothing is committed.
