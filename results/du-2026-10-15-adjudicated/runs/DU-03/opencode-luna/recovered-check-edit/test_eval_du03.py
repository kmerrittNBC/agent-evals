import subprocess
import tempfile
import unittest
from pathlib import Path

from src.agent_eval.core import validate_repos


class DuplicateRepoTests(unittest.TestCase):
    def make_repo(self, repo: Path) -> str:
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        subprocess.run(["git", "-C", str(repo), "config", "user.email", "eval@example.test"], check=True)
        subprocess.run(["git", "-C", str(repo), "config", "user.name", "Eval"], check=True)
        (repo / "file").write_text("content")
        subprocess.run(["git", "-C", str(repo), "add", "file"], check=True)
        subprocess.run(["git", "-C", str(repo), "commit", "-qm", "pin"], check=True)
        return subprocess.check_output(
            ["git", "-C", str(repo), "rev-parse", "HEAD"], text=True
        ).strip()

    def test_duplicate_assignment_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            self.make_repo(repo)
            assignment = f"relayview={repo}"
            with self.assertRaisesRegex(ValueError, "duplicate|Duplicate"):
                validate_repos([assignment, assignment])

    def test_duplicate_name_with_different_path_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary) / "repo"
            repo.mkdir()
            self.make_repo(repo)
            with self.assertRaisesRegex(ValueError, "Duplicate --repo assignment for 'relayview'"):
                validate_repos([f"relayview={repo}", f"relayview={repo / 'other'}"])

    def test_single_assignment_is_preserved(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary) / "repo"
            repo.mkdir()
            commit = self.make_repo(repo)
            result = validate_repos([f"relayview={repo}"])
            self.assertEqual(result["relayview"]["path"], str(repo.resolve()))
            self.assertEqual(result["relayview"]["commit"], commit)
