import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.agent_eval.core import pack_status


class MalformedEvidenceTests(unittest.TestCase):
    def test_malformed_repo_fact_is_reported_without_exception(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "pack.json"
            path.write_text(json.dumps({
                "reference_answer": "A substantive answer",
                "sources": [{"title": "source", "url": "repo://relayview/pin/file",
                             "retrieved_at": "2026-10-15", "snapshot_or_excerpt": "evidence"}],
                "repo_facts": [{"repo": "relayview"}],
                "ambiguities": [],
                "grading_guidance": {"must_check": [], "acceptable_alternatives": [],
                                     "do_not_penalize": []},
                "decision_changing_errors": []
            }))
            manifest = {"repos": {"relayview": {"path": "/tmp/relayview",
                                                 "commit": "a" * 40}}}
            with patch("src.agent_eval.core.pack_path", return_value=path):
                okay, reason = pack_status("IG-02", manifest)
            self.assertFalse(okay)
            self.assertIn("repo fact", reason.lower())
