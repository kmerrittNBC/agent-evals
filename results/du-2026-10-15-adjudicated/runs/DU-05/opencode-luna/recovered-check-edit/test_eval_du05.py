import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.agent_eval.core import pack_status


class MalformedEvidenceTests(unittest.TestCase):
    @staticmethod
    def evidence_pack(repo_facts):
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

    def test_malformed_repo_facts_are_reported_without_exception(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "pack.json"
            with patch("src.agent_eval.core.pack_path", return_value=path):
                malformed_facts = (
                    None,
                    {"repo": "relayview", "commit": "a" * 40},
                    [None],
                    [{"repo": "relayview"}],
                    [{"repo": "relayview", "commit": "short"}],
                    [{"repo": "relayview", "commit": "g" * 40}],
                    [{"repo": "   ", "commit": "a" * 40}],
                    [{"repo": 1, "commit": "a" * 40}],
                )
                for repo_facts in malformed_facts:
                    with self.subTest(repo_facts=repo_facts):
                        path.write_text(json.dumps(self.evidence_pack(repo_facts)))
                        okay, reason = pack_status("IG-02")
                        self.assertFalse(okay)
                        self.assertIn("repo fact", reason.lower())

    def test_well_formed_repo_fact_keeps_pinned_commit_comparison(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "pack.json"
            commit = "a" * 40
            path.write_text(json.dumps(self.evidence_pack([
                {"repo": "relayview", "commit": commit}
            ])))
            manifest = {"repos": {"relayview": {"path": "/tmp/relayview",
                                                 "commit": commit}}}
            with patch("src.agent_eval.core.pack_path", return_value=path):
                self.assertEqual(pack_status("IG-02", manifest), (True, "ready"))
                manifest["repos"]["relayview"]["commit"] = "b" * 40
                okay, reason = pack_status("IG-02", manifest)
            self.assertFalse(okay)
            self.assertIn("repo pin differs", reason)
