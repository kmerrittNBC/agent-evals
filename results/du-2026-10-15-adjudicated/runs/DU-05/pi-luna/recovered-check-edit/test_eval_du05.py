import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.agent_eval.core import pack_status


class MalformedEvidenceTests(unittest.TestCase):
    @staticmethod
    def pack(repo_facts):
        return {
            "reference_answer": "A substantive answer",
            "sources": [{"title": "source", "url": "repo://relayview/pin/file",
                         "retrieved_at": "2026-10-15", "snapshot_or_excerpt": "evidence"}],
            "repo_facts": repo_facts,
            "ambiguities": [],
            "grading_guidance": {"must_check": [], "acceptable_alternatives": [],
                                 "do_not_penalize": []},
            "decision_changing_errors": []
        }

    def check_pack(self, repo_facts, manifest=None):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "pack.json"
            path.write_text(json.dumps(self.pack(repo_facts)))
            with patch("src.agent_eval.core.pack_path", return_value=path):
                return pack_status("IG-02", manifest)

    def test_malformed_repo_facts_are_reported_without_exception(self):
        malformed_facts = [
            None,
            {"repo": "relayview", "commit": "a" * 40},
            [{"repo": "relayview"}],
            [{"repo": "", "commit": "a" * 40}],
            [{"repo": "relayview", "commit": None}],
            [{"repo": "relayview", "commit": "a" * 39}],
            [{"repo": "relayview", "commit": "g" * 40}],
            [{"repo": 42, "commit": "a" * 40}],
        ]
        for repo_facts in malformed_facts:
            with self.subTest(repo_facts=repo_facts):
                okay, reason = self.check_pack(repo_facts)
                self.assertFalse(okay)
                self.assertIn("repo fact", reason.lower())
                self.assertIn("40-character commit hash", reason)

    def test_well_formed_repo_fact_keeps_pinned_commit_comparison(self):
        commit = "a" * 40
        manifest = {"repos": {"relayview": {"path": "/tmp/relayview", "commit": commit}}}
        self.assertEqual(self.check_pack([{"repo": "relayview", "commit": commit}], manifest),
                         (True, "ready"))
        okay, reason = self.check_pack([{"repo": "relayview", "commit": "b" * 40}], manifest)
        self.assertFalse(okay)
        self.assertIn("repo pin differs", reason)
