Updated `agent-evals/src/agent_eval/core.py` to raise a clear `ValueError` when a `--repo` name is assigned more than once, including when the paths are identical. Single assignments still produce the same repository pin, and the existing manifest pin checks were left unchanged.

Extended `agent-evals/tests/test_eval_du03.py` to cover duplicate names with different paths and a valid single assignment; the existing test covers identical repeated assignments.

I couldn’t run the tests because this environment provides no command-execution tool. The focused check to run is `python3 -m unittest discover -s tests -p test_eval_du03.py`. No `AGENTS.md` was found in the worktree.
