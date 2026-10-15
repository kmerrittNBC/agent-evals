Updated `agent-evals/src/agent_eval/core.py` so `pack_status` returns a clear not-ready reason when `repo_facts` is malformed. Each fact must have a nonempty string repo name and a 40-character hexadecimal commit hash. The existing pinned-commit comparison remains unchanged for well-formed packs.

Added focused malformed-fact and pin-comparison coverage in `agent-evals/tests/test_runner.py`. The runner tests pass (17 tests); the full test discovery also passed (18 tests), and `git diff --check` is clean. The pre-existing untracked `tests/test_eval_du05.py` was left untouched.
