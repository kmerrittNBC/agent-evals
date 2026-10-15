Preflight now rejects a repeated `--repo` name with a `ValueError` instead of silently keeping the last one.

**Change:** I added two lines to `validate_repos` in `src/agent_eval/core.py:69`. Once an assignment's name and path pass the existing format checks, it raises `ValueError("Duplicate --repo assignment for <name>")` if that name already appeared. This applies whether the paths match or differ. Because `preflight` sends every `--repo` argument through `validate_repos`, both new and existing evaluations get the check. Duplicates are caught before any git commands run on them.

**Unchanged:**
- A single valid assignment works as before: it records the path, pinned commit and whether the working tree is dirty.
- When a manifest already exists, the check that the pin matches it (`same_pin`) and the merge into it are the same.

**Checks:**
- `python -m unittest tests.test_runner tests.test_eval_du03 -v`: all 16 tests pass. That includes the untracked `tests/test_eval_du03.py` that was already in the worktree, which covers a duplicate with the same name and path.
- `python -m unittest discover -s tests` fails with "Start directory is not importable" before running anything, because `tests/` has no `__init__.py`. I ran the test modules directly instead.
- A quick manual script confirmed that a single assignment still returns the pinned entry and that a duplicate name with a different path raises the new error.

There's no AGENTS.md in the repo. I didn't add a separate test for the different-path case or commit anything; `git diff` shows only the two lines in `core.py`.
