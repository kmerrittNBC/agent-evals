import subprocess
import tempfile
import unittest
from pathlib import Path

from src.agent_eval.core import validate_repos


class DuplicateRepoTests(unittest.TestCase):
    def test_duplicate_assignment_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            subprocess.run(["git", "-C", str(repo), "config", "user.email", "eval@example.test"], check=True)
            subprocess.run(["git", "-C", str(repo), "config", "user.name", "Eval"], check=True)
            (repo / "file").write_text("content")
            subprocess.run(["git", "-C", str(repo), "add", "file"], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-qm", "pin"], check=True)
            assignment = f"relayview={repo}"
            with self.assertRaisesRegex(ValueError, "duplicate|Duplicate"):
                validate_repos([assignment, assignment])
