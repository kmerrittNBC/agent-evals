import tempfile
import unittest
from pathlib import Path

from src.agent_eval.core import tree_digest


class SymlinkDigestTests(unittest.TestCase):
    def test_broken_symlink_target_changes_digest(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            link = root / "link"
            link.symlink_to("missing-a")
            before = tree_digest(root)
            link.unlink()
            link.symlink_to("missing-b")
            self.assertNotEqual(before, tree_digest(root))

    def test_valid_symlink_target_is_separate_from_file_contents(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "a").write_text("bc")
            (root / "ab").write_text("c")
            link = root / "link"
            link.symlink_to("a")
            before = tree_digest(root)
            link.unlink()
            link.symlink_to("ab")
            self.assertNotEqual(before, tree_digest(root))
