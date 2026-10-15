Updated `tree_digest` in `agent-evals/src/agent_eval/core.py` to hash each symlink’s target text, including when the target is missing. The existing path and file-content hashing remains in place.

Added focused coverage in `agent-evals/tests/test_runner.py` for retargeting valid and broken links, plus file-content and path changes. The runner tests passed (17 tests); the full test discovery passed (18 tests), and `git diff --check` passed. The pre-existing untracked `tests/test_eval_du04.py` was left untouched.
