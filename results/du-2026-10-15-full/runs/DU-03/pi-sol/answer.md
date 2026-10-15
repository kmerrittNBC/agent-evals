Updated `agent-evals/src/agent_eval/core.py` so preflight raises a clear `ValueError` when the same `--repo` name is assigned twice, even if both assignments use the same path. Single assignments still produce the same commit pin, and the existing manifest pin logic is unchanged.

Added coverage in `agent-evals/tests/test_runner.py`. All 17 tests pass; `git diff --check` is clean. I left the pre-existing untracked `tests/test_eval_du03.py` untouched.
