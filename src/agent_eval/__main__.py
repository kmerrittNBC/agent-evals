from __future__ import annotations

import argparse
import json
import sys

from .core import (RESULTS, load_manifest, pack_status, randomized_slots,
                   read_config, run_one)
from .judge import judge_one
from .preflight import preflight
from .report import make_report


def main() -> int:
    parser = argparse.ArgumentParser(prog="agent_eval")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("preflight", "run", "judge", "report", "reconcile-credits"):
        part = sub.add_parser(name)
        part.add_argument("--evaluation-id", required=True)
        if name == "preflight":
            part.add_argument("--cutoff")
            part.add_argument("--repo", action="append", default=[])
            part.add_argument("--live", action="store_true")
        elif name in ("run", "judge"):
            part.add_argument("--arm", action="append")
            part.add_argument("--task", action="append")
            if name == "run":
                part.add_argument("--full", action="store_true")
        elif name == "reconcile-credits":
            part.add_argument("--arm", required=True)
            part.add_argument("--task", required=True)
            part.add_argument("--billing-credits", required=True, type=float)
            part.add_argument("--billing-record-id", required=True)
    args = parser.parse_args()
    try:
        if args.command == "preflight":
            result = preflight(args.evaluation_id, args.cutoff, args.repo, args.live)
            print(json.dumps({"manifest": str(RESULTS / args.evaluation_id / "manifest.json"),
                              "arms": {key: value["status"] for key, value in result["preflight"].items()},
                              "judge": result["judge_preflight"]["status"],
                              "evidence": {key: value["status"] for key, value in result["evidence"].items()},
                              "repos": result["repos"]}, indent=2))
            return 0
        manifest = load_manifest(args.evaluation_id)
        arms = read_config("arms")["arms"]
        tasks = read_config("tasks")["tasks"]
        if args.command == "reconcile-credits":
            from .core import atomic_json
            if args.billing_credits < 0:
                raise ValueError("Billing credits must be nonnegative")
            if args.arm not in [a["id"] for a in arms if a["billing"] == "copilot"]:
                raise ValueError("Arm must use Copilot billing")
            if args.task not in [t["id"] for t in tasks]:
                raise ValueError("Unknown task")
            run_dir = RESULTS / args.evaluation_id / "runs" / args.task / args.arm
            if not (run_dir / "metrics.json").exists():
                raise ValueError("Run does not exist")
            path = run_dir / "credit-reconciliation.json"
            if path.exists():
                raise ValueError("Billing record already attached to this run")
            atomic_json(path, {"billing_credits": args.billing_credits,
                               "billing_record_id": args.billing_record_id,
                               "source": "GitHub billing record supplied by operator"})
            print(path)
            return 0
        if args.command in ("run", "judge"):
            selected_arms = [arm for arm in arms if not args.arm or arm["id"] in args.arm]
            selected_tasks = [task for task in tasks if not args.task or task["id"] in args.task]
            if not selected_arms or not selected_tasks:
                raise ValueError("No matching arms or tasks")
        if args.command == "run":
            if args.full and (args.arm or args.task):
                raise ValueError("--full cannot be combined with filters")
            if not args.full and not (args.arm or args.task):
                raise ValueError("Use --full for all 30 slots, or select --arm/--task for a pilot")
            if manifest["judge_preflight"]["status"] != "ready":
                raise ValueError("Codex judge has not passed live preflight")
            for task in selected_tasks:
                okay, reason = pack_status(task["id"])
                if not okay:
                    raise ValueError(f"{task['id']}: {reason}")
                if any(repo not in manifest["repos"] for repo in task["repos"]):
                    raise ValueError(f"{task['id']}: missing pinned repo")
            if any(manifest["preflight"][arm["id"]]["status"] not in ("ready", "unavailable") for arm in selected_arms):
                raise ValueError("All selected arms must pass live preflight or be recorded unavailable")
            slots = randomized_slots(selected_tasks, selected_arms, read_config("run-policy")["seed"])
            from .core import atomic_json
            plan_path = RESULTS / args.evaluation_id / "run-plan.json"
            plan = {"seed": read_config("run-policy")["seed"],
                    "slots": [{"task_id": task["id"], "arm_id": arm["id"]} for task, arm in slots]}
            if plan_path.exists() and json.loads(plan_path.read_text()) != plan:
                raise ValueError("Run selection differs from the recorded run plan")
            if not plan_path.exists():
                atomic_json(plan_path, plan)
            for task, arm in slots:
                result = run_one(arm, task, manifest, args.evaluation_id)
                print(f"{task['id']} {arm['id']}: {result['status']}", flush=True)
            return 0
        if args.command == "judge":
            for task in selected_tasks:
                for arm in selected_arms:
                    result = judge_one(args.evaluation_id, task, arm, manifest)
                    if result:
                        print(f"{task['id']} {arm['id']}: {result['overall_quality']}/5", flush=True)
            return 0
        csv_path, report_path = make_report(args.evaluation_id, manifest)
        print(csv_path)
        print(report_path)
        return 0
    except (ValueError, RuntimeError, OSError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
