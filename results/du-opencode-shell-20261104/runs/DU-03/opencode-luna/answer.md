Implemented duplicate `--repo` detection in `src/agent_eval/core.py`. Repeated assignments for the same repository name now raise a clear `ValueError`, even when the paths differ; valid single assignments still work. Existing manifest pin behavior is unchanged.

Added coverage in `tests/test_duplicate_repo_assignments.py`. All 18 local tests pass with `python3 -m unittest discover -s tests -v`. No further changes are planned.
