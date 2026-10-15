`tree_digest` now includes each symlink's target text, so pointing a link somewhere else changes the workspace digest. That holds for broken links too. The runner tests pass (17 run, OK).

**Change** (`src/agent_eval/core.py`, in `tree_digest`): when a path is a symlink, the link's target text is added to the hash with a `\0symlink\0` prefix, so it can't be mistaken for file content. The existing checks are unchanged: every relative path is still hashed, and file contents are still hashed whenever `is_file()` is true. That means a link to a file still adds the file's contents, as it did before.

**Test** (`tests/test_runner.py`): `test_digest_tracks_symlink_targets_including_broken_links` checks three things:
- Switching a working link between two files with identical contents changes the digest. Only the link text differs, so this tests the new behaviour directly.
- Switching a broken link from `missing-a` to `missing-b` changes the digest.
- Pointing it back at `missing-a` gives the original digest again, so the result is repeatable.

**Run:** `python -m unittest tests.test_runner tests.test_eval_du04` (17 run, OK). I didn't run the new test against the old code. I expect it would fail there, because the old code hashed only the path for a broken link.

The worktree already had an untracked `tests/test_eval_du04.py` that wasn't mine. It tests the same broken-link case and passes with this change; I left it as it was. Nothing is committed.
