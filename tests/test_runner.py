import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.agent_eval import adapters
from src.agent_eval.core import (pack_status, prepare_workspace, read_config,
                                 static_arm_check, tree_digest, validate_cutoff)
from src.agent_eval.judge import anonymized_transcript, validate_judgment
from src.agent_eval.preflight import live_arm_probe
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
            prepare_workspace({"relayview": {"path": str(repo), "commit": commit}},
                              {"repos": ["relayview"]}, workspace)
            self.assertEqual((workspace / "relayview/package.json").read_text(), '{"version":"1"}')
            before = tree_digest(workspace)
            (workspace / "relayview/package.json").chmod(0o644)
            (workspace / "relayview/package.json").write_text("changed")
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

    def test_antigravity_quota_failure_is_explained_by_live_probe(self):
        arm = {"id": "antigravity-flash", "harness": "antigravity", "binary": "agy",
               "model": "gemini-3.8-flash-medium", "reasoning": "medium"}
        events = [
            {"channel": "stdout", "data": {"event": "step_update", "step_update": {
                "step_type": "tool", "state": "DONE", "tool_name": "search_web"}}},
            {"channel": "stdout", "data": {"event": "result", "result": {
                "status": "ERROR", "response": "", "error": "Individual quota reached"}}},
            {"channel": "stderr", "data": {"raw_text":
                'AGY_ERROR: {"status":"RESOURCE_EXHAUSTED","error_code":429}'}}
        ]
        for exit_code in (0, 3):
            with self.subTest(exit_code=exit_code), patch(
                    "src.agent_eval.preflight.capture", return_value={
                        "events": events, "exit_code": exit_code, "timed_out": False}):
                probe = live_arm_probe(arm, 180)
                self.assertEqual(probe["status"], "unavailable")
                self.assertIn("quota", probe["reason"].lower())
                self.assertEqual(probe["probe_tool_names"], ["search_web"])

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

    def test_current_tasks_have_complete_judge_packs(self):
        tasks = read_config("tasks")["tasks"]
        self.assertEqual(len(tasks), 5)
        for task in tasks:
            with self.subTest(task=task["id"]):
                self.assertEqual(pack_status(task["id"]), (True, "ready"))
        self.assertEqual(tasks[2]["repos"], ["relayview", "agent-harness-evals"])
        self.assertEqual(tasks[4]["repos"], ["agent-harness-evals"])

    def test_active_arms_exclude_copilot_cli_and_antigravity(self):
        arms = read_config("arms")["arms"]
        self.assertEqual(len(arms), 4)
        self.assertEqual({arm["id"] for arm in arms},
                         {"pi-luna", "pi-sol", "opencode-luna", "claude-opus"})
        opencode = next(arm for arm in arms if arm["harness"] == "opencode")
        self.assertEqual(opencode["search_provider"], "tinyfish")

    def test_opencode_run_is_hermetic_and_pins_keyless_search(self):
        arm = {"id": "opencode-luna", "harness": "opencode", "binary": "opencode",
               "model": "github-copilot/gpt-6-luna", "reasoning": "medium",
               "search_provider": "tinyfish"}
        cmd = adapters.command(arm, "probe prompt", Path("/w"), Path("/r"), "sess-1")
        self.assertIn("--standalone", cmd)
        self.assertEqual(cmd[cmd.index("--model") + 1], "github-copilot/gpt-6-luna#medium")
        self.assertEqual(cmd[cmd.index("--session") + 1], "sess-1")
        self.assertEqual(cmd[-1], "probe prompt")
        config = json.loads(adapters.environment(arm, Path("/w"))["OPENCODE_CONFIG_CONTENT"])
        self.assertEqual(config["websearch"], {"provider": "tinyfish"})
        rules = config["permissions"]
        self.assertEqual(rules[0], {"action": "*", "resource": "*", "effect": "deny"})
        allowed = {rule["action"] for rule in rules[1:]}
        self.assertEqual(allowed, {"read", "glob", "grep", "websearch", "webfetch", "question"})
        self.assertTrue(all(rule["effect"] == "allow" for rule in rules[1:]))

    def test_opencode_events_decode_answer_tools_session_and_usage(self):
        events = [
            {"data": {"type": "step_start", "sessionID": "sess-9", "part": {}}},
            {"data": {"type": "tool_use", "sessionID": "sess-9",
                      "part": {"tool": "websearch", "state": {"status": "completed", "input": {"query": "pathlib"}},
                               "content": [{"type": "text", "text": "docs.python.org"}]}}},
            {"data": {"type": "tool_use", "sessionID": "sess-9",
                      "part": {"tool": "webfetch", "state": {"status": "completed", "input": {"url": "https://docs.python.org"}},
                               "content": [{"type": "text", "text": "pathlib docs"}]}}},
            {"data": {"type": "text", "sessionID": "sess-9", "part": {"text": "The page is the pathlib documentation."}}},
            {"data": {"type": "step_finish", "sessionID": "sess-9",
                      "part": {"cost": {"total": 0.01}, "tokens": {"input": 10, "output": 5}}}},
        ]
        self.assertEqual(adapters.final_answer("opencode", events),
                         "The page is the pathlib documentation.")
        self.assertEqual(adapters.tool_names(events), ["websearch", "webfetch"])
        self.assertEqual(adapters.tool_activity(events),
                         {"search_calls": 1, "fetch_calls": 1, "other_tool_calls": 0})
        self.assertEqual(adapters.session_id("opencode", events), "sess-9")
        self.assertEqual(adapters.usage("opencode", events, Path("/r"))["raw"],
                         {"tokens": {"input": 10, "output": 5}, "cost": {"total": 0.01}})
        transcript = json.dumps(anonymized_transcript(
            [{"index": 1, "channel": "stdout", "elapsed_seconds": 1.0, "data": events[1]["data"]}],
            read_config("arms")["arms"]))
        self.assertIn("websearch", transcript)
        self.assertIn("docs.python.org", transcript)

    def test_opencode_arm_without_keyless_provider_is_unavailable(self):
        arm = {"id": "opencode-luna", "harness": "opencode", "binary": "opencode",
               "model": "github-copilot/gpt-6-luna", "reasoning": "medium",
               "search_provider": "tavily"}
        with patch("src.agent_eval.core._version", return_value="opencode 2.0"):
            details = static_arm_check(arm)
        self.assertEqual(details["status"], "unavailable")
        self.assertIn("tinyfish", details["reason"])

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
