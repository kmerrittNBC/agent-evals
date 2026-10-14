from __future__ import annotations

import csv
import json
import statistics
from pathlib import Path

from .core import RESULTS, atomic_json, read_config


def _number(value: object) -> float | None:
    return float(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def _credit(usage: dict, reconciliation: dict | None = None) -> tuple[float | None, str]:
    if reconciliation:
        reported = _number(reconciliation.get("billing_credits"))
        if reported is not None:
            raw = usage.get("raw")
            native = _number(raw.get("totalNanoAiu")) if isinstance(raw, dict) else None
            if native is None:
                return reported, "measured_billing"
            estimated = native / 1e9
            if abs(estimated - reported) <= max(0.01, reported * 0.05):
                return reported, "reconciled"
            return estimated, "estimated_billing_mismatch"
    if usage.get("classification") != "measured":
        return None, usage.get("classification", "unavailable")
    raw = usage.get("raw")
    if not isinstance(raw, dict):
        return None, "unavailable"
    for key in ("aiCredits", "ai_credits", "totalCredits", "credits"):
        value = _number(raw.get(key))
        if value is not None:
            return value, "measured"
    nano = _number(raw.get("totalNanoAiu"))
    if nano is not None:
        # GitHub's SDK example divides nano-AIU by 1e9 but says to verify
        # billing before treating the result as an exact credit charge.
        return nano / 1e9, "estimated"
    return None, "unavailable"


def _fmt(values: list[float]) -> str:
    if not values:
        return "unavailable"
    return f"{statistics.median(values):.2f} ({min(values):.2f}–{max(values):.2f})"


def _rating(judgments: list[dict], attempts: int) -> str:
    rubric = read_config("rubric")
    if len(judgments) < rubric["unrated_if_completed_below"]:
        return "Unrated"
    median = statistics.median(j["overall_quality"] for j in judgments)
    completion = sum(j["completion_status"] == "complete" for j in judgments) / attempts
    critical = sum(len(j["critical_errors"]) for j in judgments)
    for name, threshold in rubric["headline_thresholds"].items():
        if (median >= threshold["minimum_median_overall"] and
                completion >= threshold["minimum_completion_rate"] and
                critical <= threshold["maximum_critical_errors"]):
            return name
    return "Unacceptable"


def make_report(evaluation_id: str, manifest: dict) -> tuple[Path, Path]:
    directory = RESULTS / evaluation_id
    arms = read_config("arms")["arms"]
    tasks = read_config("tasks")["tasks"]
    rows: list[dict] = []
    for task in tasks:
        for arm in arms:
            run_dir = directory / "runs" / task["id"] / arm["id"]
            metrics = json.loads((run_dir / "metrics.json").read_text()) if (run_dir / "metrics.json").exists() else {}
            judgment = json.loads((run_dir / "judgment.json").read_text()) if (run_dir / "judgment.json").exists() else None
            reconciliation = json.loads((run_dir / "credit-reconciliation.json").read_text()) if (run_dir / "credit-reconciliation.json").exists() else None
            credit, classification = _credit(metrics.get("usage", {}), reconciliation)
            rows.append({"task_id": task["id"], "arm_id": arm["id"],
                         "harness": arm["harness"], "model": arm["model"],
                         "billing_family": arm["billing"],
                         "status": metrics.get("status", "not_run"),
                         "reason": metrics.get("reason") or "",
                         "time_first_visible_seconds": metrics.get("first_visible_seconds"),
                         "time_first_substantive_seconds": metrics.get("first_substantive_seconds"),
                         "time_final_seconds": metrics.get("elapsed_seconds"),
                         "asked_clarification": metrics.get("asked_clarification"),
                         "follow_up_classification": judgment["follow_up_classification"] if judgment else "",
                         "completion_status": judgment["completion_status"] if judgment else "",
                         "overall_quality": judgment["overall_quality"] if judgment else "",
                         "critical_error_count": len(judgment["critical_errors"]) if judgment else "",
                         "copilot_credits": credit if arm["billing"] == "copilot" else None,
                         "copilot_nano_aiu": metrics.get("usage", {}).get("raw", {}).get("totalNanoAiu")
                         if arm["billing"] == "copilot" and isinstance(metrics.get("usage", {}).get("raw"), dict) else None,
                         "credit_classification": classification if arm["billing"] == "copilot" else "not_applicable",
                         "native_usage_json": json.dumps(metrics.get("usage", {}).get("raw"), sort_keys=True),
                         "search_calls": metrics.get("tool_activity", {}).get("search_calls"),
                         "fetch_calls": metrics.get("tool_activity", {}).get("fetch_calls"),
                         "answer_path": str((run_dir / "answer.md").relative_to(directory)) if metrics else "",
                         "judgment_path": str((run_dir / "judgment.json").relative_to(directory)) if judgment else ""})
    csv_path = directory / "summary.csv"
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    lines = [f"# Agent evaluation: {evaluation_id}", "", f"Information cutoff: {manifest['cutoff']}",
             "", "Five tasks per arm. Ratings and rankings are exploratory, not statistically conclusive.",
             "", "## Arm summary", "",
             "| Arm | Rating | Completed | Quality median | First visible seconds median (range) | First substantive seconds median (range) | Final seconds median (range) | Follow-ups | Critical errors | Copilot credits median (range) |",
             "|---|---|---:|---:|---|---|---|---:|---:|---|"]
    for arm in arms:
        selected = [row for row in rows if row["arm_id"] == arm["id"]]
        judgments = []
        for task in tasks:
            path = directory / "runs" / task["id"] / arm["id"] / "judgment.json"
            if path.exists():
                judgments.append(json.loads(path.read_text()))
        final = [_number(row["time_final_seconds"]) for row in selected if row["status"] == "completed"]
        visible = [_number(row["time_first_visible_seconds"]) for row in selected]
        substantive = [_number(row["time_first_substantive_seconds"]) for row in selected]
        credits = [_number(row["copilot_credits"]) for row in selected]
        quality = [j["overall_quality"] for j in judgments]
        rating = _rating(judgments, len(tasks))
        lines.append(f"| {arm['id']} | {rating} | {sum(row['status'] == 'completed' for row in selected)}/5 | "
                     f"{statistics.median(quality) if quality else 'unavailable'} | "
                     f"{_fmt([x for x in visible if x is not None])} | "
                     f"{_fmt([x for x in substantive if x is not None])} | "
                     f"{_fmt([x for x in final if x is not None])} | "
                     f"{sum(bool(row['asked_clarification']) for row in selected)} | "
                     f"{sum(len(j['critical_errors']) for j in judgments)} | "
                     f"{('~' if any(str(row['credit_classification']).startswith('estimated') for row in selected) else '') + _fmt([x for x in credits if x is not None]) if arm['billing'] == 'copilot' else 'separate native usage'} |")
    lines += ["", "## Task outcomes", ""]
    for task in tasks:
        lines += [f"### {task['id']}", "", "| Arm | Status | Quality | Follow-up | Critical errors | Answer | Judgment |",
                  "|---|---|---:|---|---:|---|---|"]
        for row in [r for r in rows if r["task_id"] == task["id"]]:
            answer = f"[answer]({row['answer_path']})" if row["answer_path"] else "—"
            judgment = f"[judgment]({row['judgment_path']})" if row["judgment_path"] else "—"
            lines.append(f"| {row['arm_id']} | {row['status']} | {row['overall_quality'] or '—'} | "
                         f"{row['follow_up_classification'] or '—'} | {row['critical_error_count'] if row['critical_error_count'] != '' else '—'} | {answer} | {judgment} |")
        lines.append("")
    pairs = []
    for task in tasks:
        luna = next(row for row in rows if row["task_id"] == task["id"] and row["arm_id"] == "pi-luna")
        sol = next(row for row in rows if row["task_id"] == task["id"] and row["arm_id"] == "pi-sol")
        if _number(luna["copilot_credits"]) and _number(sol["copilot_credits"]):
            pairs.append((task["id"], float(sol["copilot_credits"]), float(luna["copilot_credits"])))
    lines += ["## Sol versus Luna Copilot credits", ""]
    if pairs:
        lines += ["| Task | Pi Sol | Pi Luna | Sol/Luna |", "|---|---:|---:|---:|"]
        for task_id, sol, luna in pairs:
            lines.append(f"| {task_id} | ~{sol:.4f} | ~{luna:.4f} | {sol/luna:.2f} |")
        lines += ["", f"Median ratio: {statistics.median(sol/luna for _, sol, luna in pairs):.2f}."]
    else:
        lines.append("Unavailable: provider-reported credits are not present for paired Pi runs.")
    lines += ["", "Anthropic and Google usage remain in native units in `summary.csv`; they are not converted to Copilot credits.",
              "Copilot values derived from `totalNanoAiu / 1e9` are approximate until reconciled with GitHub billing. See each row's `credit_classification`.",
              "", "Judge scores are opinions. Times and native usage come from the runner and provider events. "
              "A missing value means unavailable, never zero. Antigravity CLI is a headless harness; this report does not measure the desktop app.",
              "", "Every critical-error judgment should receive blind human review before acting on rankings.", ""]
    report_path = directory / "report.md"
    report_path.write_text("\n".join(lines))
    return csv_path, report_path
