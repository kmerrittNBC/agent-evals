Updated `agent-evals/src/agent_eval/core.py` to check all `--repo` names before resolving repository paths. Repeated names now raise a clear `ValueError`, even when both assignments use the same path. Single assignments and existing manifest pin handling are unchanged.

Checks passed: the duplicate-assignment test, all 15 runner tests, and `git diff --check`. No `AGENTS.md` was present.
