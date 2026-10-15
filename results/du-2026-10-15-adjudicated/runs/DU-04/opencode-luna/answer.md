Updated `src/agent_eval/core.py` so `tree_digest` includes each symlink’s target text while retaining path hashing and content hashing for links to existing files. Added runner coverage in `tests/test_runner.py` showing that retargeting a link changes the digest even when both targets have identical content. The existing broken-symlink regression in `tests/test_eval_du04.py` covers broken links.

I couldn’t run the tests because this environment doesn’t provide a command-execution tool. The relevant check to run from `./agent-evals` is `python3 -m unittest discover -s tests -v`.
