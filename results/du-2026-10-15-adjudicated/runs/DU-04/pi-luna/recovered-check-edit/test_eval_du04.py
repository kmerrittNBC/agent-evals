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

    def test_live_symlink_target_changes_digest_even_with_same_content(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "first").write_text("same content")
            (root / "second").write_text("same content")
            link = root / "link"
            link.symlink_to("first")
            before = tree_digest(root)
            link.unlink()
            link.symlink_to("second")
            self.assertNotEqual(before, tree_digest(root))
