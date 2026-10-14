import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from src.agent_eval import adapters
from src.agent_eval.core import prepare_workspace, tree_digest, validate_cutoff
from src.agent_eval.judge import anonymized_transcript, validate_judgment
from src.agent_eval.report import _credit


class RunnerContractTests(unittest.TestCase):
    def test_snapshot_uses_pinned_commit_and_omits_later_changes(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp) / "repo"
            repo.mkdir()
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            subprocess.run(["git", "-C", str(repo), "config", "user.email", "eval@example.test"], check=True)
            subprocess.run(["git", "-C", str(repo), "config", "user.name", "Eval"], check=True)
            (repo / "package.json").write_text('{"version":"1"}')
            subprocess.run(["git", "-C", str(repo), "add", "package.json"], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-qm", "pin"], check=True)
            commit = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
            (repo / "package.json").write_text('{"version":"2"}')
            workspace = Path(temp) / "export"
            prepare_workspace({"financial-hq-ui": {"path": str(repo), "commit": commit}},
                              {"repos": ["financial-hq-ui"]}, workspace)
            self.assertEqual((workspace / "financial-hq-ui/package.json").read_text(), '{"version":"1"}')
            before = tree_digest(workspace)
            (workspace / "financial-hq-ui/package.json").chmod(0o644)
            (workspace / "financial-hq-ui/package.json").write_text("changed")
            self.assertNotEqual(before, tree_digest(workspace))

    def test_no_usage_is_not_zero_credits(self):
        self.assertEqual(_credit({"classification": "unavailable", "raw": None}), (None, "unavailable"))
        self.assertEqual(_credit({"classification": "measured", "raw": {"totalNanoAiu": 100}}), (1e-07, "estimated"))
        self.assertEqual(_credit({"classification": "measured", "raw": {"aiCredits": 0}}), (0.0, "measured"))
        self.assertEqual(_credit({"classification": "measured", "raw": {"totalNanoAiu": 360000000}},
                                 {"billing_credits": 0.36}), (0.36, "reconciled"))
        self.assertEqual(_credit({"classification": "measured", "raw": {"totalNanoAiu": 360000000}},
                                 {"billing_credits": 0.60}), (0.36, "estimated_billing_mismatch"))

    def test_terminal_output_does_not_become_early_answer(self):
        events = [
            {"data": {"type": "system", "text": "ready"}},
            {"data": {"event": "step_update", "step_update": {"text_delta": "The result is 42."}}},
            {"data": {"event": "result", "result": {"response": "The result is 42."}}},
        ]
        self.assertEqual(adapters.final_answer("antigravity", events), "The result is 42.")
        self.assertEqual(adapters.event_text("antigravity", events[0]["data"]), "")

    def test_declared_tools_do_not_count_as_tool_activity(self):
        events = [{"data": {"type": "message_end", "message": {"role": "system", "toolsAdded": [
            {"name": "web_search"}, {"name": "web_fetch"}]}}}]
        self.assertEqual(adapters.tool_names(events), [])

    def test_antigravity_search_and_fetch_count_as_activity(self):
        events = [{"data": {"event": "step_update", "step_update": {
            "step_type": "tool", "state": "DONE", "tool_name": name}}}
            for name in ("search_web", "read_url_content")]
        self.assertEqual(adapters.tool_activity(events),
                         {"search_calls": 1, "fetch_calls": 1, "other_tool_calls": 0})

    def test_claude_permission_denial_does_not_count_as_web_activity(self):
        events = [
            {"data": {"type": "assistant", "message": {"role": "assistant", "content": [
                {"type": "tool_use", "id": "search-1", "name": "WebSearch"},
                {"type": "tool_use", "id": "fetch-1", "name": "WebFetch"}]} }},
            {"data": {"type": "user", "message": {"role": "user", "content": [
                {"type": "tool_result", "tool_use_id": "search-1", "is_error": True, "content": "permission denied"},
                {"type": "tool_result", "tool_use_id": "fetch-1", "content": "fetched page"}]} }}]
        self.assertEqual(adapters.completed_claude_tool_names(events), ["WebFetch"])
        self.assertEqual(adapters.tool_activity(events),
                         {"search_calls": 0, "fetch_calls": 1, "other_tool_calls": 0})

    def test_judge_transcript_hides_identity_and_usage(self):
        arms = [{"id": "pi-luna", "harness": "pi", "binary": "pi", "model": "github-copilot/gpt-6-luna"}]
        events = [{"index": 0, "channel": "stdout", "elapsed_seconds": 2.0,
                   "data": {"type":"message_end", "model": "github-copilot/gpt-6-luna", "usage": {"credits": 2},
                            "message": {"role":"assistant", "content":[{"type":"text","text":"gpt-6-luna benchmark"}]}}}]
        text = json.dumps(anonymized_transcript(events, arms))
        self.assertIn("gpt-6-luna benchmark", text)
        self.assertNotIn("github-copilot", text)
        self.assertNotIn("credits", text)
        self.assertNotIn('"model"', text)

    def test_cutoff_requires_timezone(self):
        with self.assertRaises(ValueError):
            validate_cutoff("2026-10-14T17:00:00")

    def test_judgment_rejects_missing_evidence(self):
        names = ["factual_accuracy", "task_completion", "source_quality", "synthesis_and_judgment",
                 "ambiguity_handling", "actionability_and_clarity"]
        judgment = {"dimensions": {name: {"score": 4, "reason": "Evidence"} for name in names},
                    "overall_quality": 4, "completion_status": "complete", "follow_up_classification": "none",
                    "critical_errors": [], "deductions": [{"dimension": "source_quality",
                                                       "answer_passage": "claim", "evidence": "", "reason": "unsupported"}],
                    "first_substantive_event_index": 1}
        with self.assertRaises(ValueError):
            validate_judgment(judgment)


if __name__ == "__main__":
    unittest.main()
