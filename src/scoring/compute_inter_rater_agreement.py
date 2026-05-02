"""Prepare and score the inter-rater agreement workflow for Tenacious-Bench."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
import sys
from typing import Any

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.scoring.scoring_evaluator import score_candidate


SUBSET_TASK_IDS = (
    "dev-programmatic-013-competitor-gap-research-frame",
    "dev-programmatic-016-competitor-gap-research-frame",
    "dev-trace-derived-001-competitor-gap-restraint",
    "dev-trace-derived-004-competitor-gap-restraint",
    "dev-programmatic-033-leadership-gap-frame",
    "dev-programmatic-001-ai-maturity-structured-reply",
    "dev-programmatic-004-ai-maturity-structured-reply",
    "dev-trace-derived-007-ai-maturity-structured-visibility",
    "dev-trace-derived-010-ai-maturity-structured-visibility",
    "dev-programmatic-037-maturity-score-conservative",
    "dev-programmatic-021-output-clean-abstain",
    "dev-programmatic-024-output-clean-abstain",
    "dev-trace-derived-019-thin-evidence-restraint",
    "dev-trace-derived-022-thin-evidence-restraint",
    "dev-programmatic-041-reengagement-format-check",
    "dev-programmatic-005-thin-signal-restraint",
    "dev-programmatic-008-thin-signal-restraint",
    "dev-programmatic-025-pricing-scope-boundary",
    "dev-programmatic-027-pricing-scope-boundary",
    "dev-programmatic-028-pricing-scope-boundary",
    "dev-programmatic-009-fixture-live-boundary",
    "dev-programmatic-012-fixture-live-boundary",
    "dev-trace-derived-013-demo-boundary-honesty",
    "dev-trace-derived-016-demo-boundary-honesty",
    "dev-programmatic-045-style-prefix-explicit",
    "dev-programmatic-017-timezone-aware-next-step",
    "dev-programmatic-020-timezone-aware-next-step",
    "dev-programmatic-029-capacity-gate-first",
    "dev-programmatic-030-capacity-gate-first",
    "dev-programmatic-032-capacity-gate-first",
)
FAILURE_DIMENSIONS = (
    "gap_condescension",
    "ai_maturity_consistency",
    "output_validity",
    "signal_grounding",
    "style_guide_adherence",
    "next_step_quality",
)
LABEL_FIELDS = ("first_pass_label", "second_pass_label", "second_labeler_label")
DEFAULT_SUBSET_PATH = Path("docs/inter_rater_subset.jsonl")
DEFAULT_TEMPLATE_PATH = Path("inter_rater_agreement.md")
DEFAULT_DEV_DIR = Path("tenacious_bench_v0.1/dev")
SECOND_PASS_DATE = "2026-05-01"
BASELINE_LABELER = "src/scoring/scoring_evaluator.py"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=True, sort_keys=True))
            handle.write("\n")


def load_dev_tasks(dev_dir: Path) -> dict[str, dict[str, Any]]:
    tasks: dict[str, dict[str, Any]] = {}
    for path in sorted(dev_dir.glob("*.jsonl")):
        for row in load_jsonl(path):
            task_id = row.get("task_id")
            if not task_id:
                continue
            if row.get("partition") != "dev":
                continue
            tasks[task_id] = row
    return tasks


def make_empty_dimension_map(dimensions: list[str]) -> dict[str, str]:
    return {dimension: "" for dimension in dimensions}


def merge_dimension_map(
    existing: dict[str, Any] | None, dimensions: list[str]
) -> dict[str, str]:
    merged = make_empty_dimension_map(dimensions)
    if not isinstance(existing, dict):
        return merged
    for dimension in dimensions:
        value = existing.get(dimension, "")
        merged[dimension] = value if isinstance(value, str) else str(value)
    return merged


def build_subset_row(task: dict[str, Any], existing: dict[str, Any] | None = None) -> dict[str, Any]:
    judge_dimensions = list(task.get("scoring_config", {}).get("judge_dimensions", []))
    baseline = score_candidate(task, task.get("candidate_output", {})).to_dict()
    existing_human = existing.get("human_agreement", {}) if isinstance(existing, dict) else {}

    row = {
        "task_id": task["task_id"],
        "partition": task["partition"],
        "failure_dimension": task["failure_dimension"],
        "difficulty": task["difficulty"],
        "source_mode": task["source_mode"],
        "channel": task["channel"],
        "message_kind": task["message_kind"],
        "candidate_output": task["candidate_output"],
        "ground_truth": task["ground_truth"],
        "rubric": task["rubric"],
        "judge_dimensions": judge_dimensions,
        "deterministic_baseline": {
            "labeler": BASELINE_LABELER,
            "labeled_at": "2026-04-30",
            "passed": baseline["passed"],
            "total": baseline["total"],
            "scores": baseline["scores"],
        },
        "human_agreement": {
            "first_pass_label": merge_dimension_map(
                existing_human.get("first_pass_label"), judge_dimensions
            ),
            "second_pass_label": merge_dimension_map(
                existing_human.get("second_pass_label"), judge_dimensions
            ),
            "second_labeler_label": merge_dimension_map(
                existing_human.get("second_labeler_label"), judge_dimensions
            ),
            "agreement_status": merge_dimension_map(
                existing_human.get("agreement_status"), judge_dimensions
            ),
            "notes": merge_dimension_map(existing_human.get("notes"), judge_dimensions),
            "scheduled_second_pass_at": existing_human.get(
                "scheduled_second_pass_at", SECOND_PASS_DATE
            ),
        },
    }
    return row


def bootstrap_subset(
    subset_path: Path, dev_dir: Path, task_ids: tuple[str, ...] = SUBSET_TASK_IDS
) -> list[dict[str, Any]]:
    tasks = load_dev_tasks(dev_dir)
    existing_rows = {}
    if subset_path.exists():
        existing_rows = {row["task_id"]: row for row in load_jsonl(subset_path)}

    missing = [task_id for task_id in task_ids if task_id not in tasks]
    if missing:
        raise ValueError(f"Missing dev tasks for subset bootstrap: {missing}")

    rows = [build_subset_row(tasks[task_id], existing_rows.get(task_id)) for task_id in task_ids]
    write_jsonl(subset_path, rows)
    return rows


def validate_subset(rows: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    if len(rows) != 30:
        errors.append(f"Expected 30 subset rows, found {len(rows)}.")

    task_ids = [row.get("task_id", "") for row in rows]
    duplicate_task_ids = [task_id for task_id, count in Counter(task_ids).items() if count > 1]
    if duplicate_task_ids:
        errors.append(f"Duplicate task IDs found: {duplicate_task_ids}.")

    partitions = {row.get("partition") for row in rows}
    if partitions != {"dev"}:
        errors.append(f"Subset must use dev only, found partitions={sorted(partitions)}.")

    if any("held_out" in str(row.get("task_id", "")) for row in rows):
        errors.append("Subset includes a held_out-like task_id, which is forbidden.")

    dimension_counts = Counter(row.get("failure_dimension") for row in rows)
    for dimension in FAILURE_DIMENSIONS:
        if dimension_counts.get(dimension, 0) != 5:
            errors.append(
                f"Expected 5 tasks for failure_dimension={dimension}, "
                f"found {dimension_counts.get(dimension, 0)}."
            )

    missing_dimensions = sorted(set(dimension_counts) - set(FAILURE_DIMENSIONS))
    if missing_dimensions:
        errors.append(f"Unexpected failure dimensions in subset: {missing_dimensions}.")

    for row in rows:
        if row.get("partition") != "dev":
            continue
        judge_dimensions = row.get("judge_dimensions")
        if not isinstance(judge_dimensions, list) or not judge_dimensions:
            errors.append(f"Task {row.get('task_id')} is missing judge_dimensions.")
            continue
        human_agreement = row.get("human_agreement", {})
        for field in ("agreement_status", "notes", *LABEL_FIELDS):
            if not isinstance(human_agreement.get(field), dict):
                errors.append(f"Task {row.get('task_id')} has invalid human_agreement.{field}.")

    return errors


def normalize_label(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip().lower()


def summarize_label_progress(rows: list[dict[str, Any]]) -> dict[str, int]:
    summary = {
        "tasks_with_any_first_pass_label": 0,
        "tasks_with_any_second_pass_label": 0,
        "tasks_with_any_second_labeler_label": 0,
    }
    for row in rows:
        human = row.get("human_agreement", {})
        if any(normalize_label(value) for value in human.get("first_pass_label", {}).values()):
            summary["tasks_with_any_first_pass_label"] += 1
        if any(normalize_label(value) for value in human.get("second_pass_label", {}).values()):
            summary["tasks_with_any_second_pass_label"] += 1
        if any(normalize_label(value) for value in human.get("second_labeler_label", {}).values()):
            summary["tasks_with_any_second_labeler_label"] += 1
    return summary


def compute_agreement(
    rows: list[dict[str, Any]], threshold: float
) -> dict[str, dict[str, dict[str, Any]]]:
    comparisons = {
        "test_retest": ("first_pass_label", "second_pass_label"),
        "inter_rater": ("first_pass_label", "second_labeler_label"),
    }
    summary: dict[str, dict[str, dict[str, Any]]] = {}
    for dimension in FAILURE_DIMENSIONS:
        dimension_rows = [row for row in rows if dimension in row.get("judge_dimensions", [])]
        dimension_summary: dict[str, dict[str, Any]] = {}
        for comparison_name, (left_field, right_field) in comparisons.items():
            completed = 0
            matches = 0
            for row in dimension_rows:
                human = row.get("human_agreement", {})
                left = normalize_label(human.get(left_field, {}).get(dimension, ""))
                right = normalize_label(human.get(right_field, {}).get(dimension, ""))
                if not left or not right:
                    continue
                completed += 1
                if left == right:
                    matches += 1
            agreement_rate = None if completed == 0 else round(matches / completed, 3)
            dimension_summary[comparison_name] = {
                "applicable_tasks": len(dimension_rows),
                "completed_pairs": completed,
                "pending_pairs": len(dimension_rows) - completed,
                "matches": matches,
                "agreement_rate": agreement_rate,
                "below_threshold": agreement_rate is not None and agreement_rate < threshold,
            }
        summary[dimension] = dimension_summary
    return summary


def format_candidate_output(candidate_output: Any) -> str:
    if isinstance(candidate_output, dict):
        subject = candidate_output.get("subject")
        body = candidate_output.get("body")
        parts = []
        if isinstance(subject, str) and subject.strip():
            parts.append(f"Subject: {subject.strip()}")
        if isinstance(body, str) and body.strip():
            parts.append(f"Body: {body.strip()}")
        if parts:
            return "\n".join(parts)
    return json.dumps(candidate_output, ensure_ascii=True, sort_keys=True, indent=2)


def render_template(subset_path: Path, output_path: Path) -> None:
    rows = load_jsonl(subset_path)
    lines = [
        "# Inter-Rater Agreement - Tenacious-Bench v0.1",
        "",
        "Generated: 2026-04-30. This workflow is prepared, but final human agreement remains pending until",
        "the label columns below are filled by one human on first pass, the same human on second pass after",
        "at least 24 hours, and ideally a second human labeler.",
        "",
        f"Subset path: `{subset_path.as_posix()}`",
        "",
        "Status note: the deterministic baseline below is preserved for reference only. It is not human",
        "agreement and should not be reported as human calibration.",
        "",
        "## Protocol Status",
        "",
        "- Subset prepared: 30 dev-only tasks, stratified to 5 tasks per failure dimension.",
        "- Human first-pass labels: pending.",
        f"- Human second-pass labels: pending. Scheduled relabel time: {SECOND_PASS_DATE}.",
        "- Second labeler review: pending.",
        "- Agreement calculator: `python src/scoring/compute_inter_rater_agreement.py`.",
        "",
        "## Human Label Scale",
        "",
        "Use a simple label per rubric dimension such as `pass`, `fail`, `unsure` or a consistent `1-5`",
        "rating scale. Keep one scale throughout a pass.",
        "",
        "## Task Templates",
        "",
    ]

    for index, row in enumerate(rows, start=1):
        lines.extend(
            [
                f"### {index}. {row['task_id']}",
                "",
                f"- failure_dimension: `{row['failure_dimension']}`",
                f"- difficulty: `{row['difficulty']}`",
                f"- source_mode: `{row['source_mode']}`",
                f"- partition: `{row['partition']}`",
                f"- judge_dimensions: `{', '.join(row['judge_dimensions'])}`",
                f"- deterministic baseline: `{'PASS' if row['deterministic_baseline']['passed'] else 'FAIL'}` via `{BASELINE_LABELER}`",
                "",
                "```text",
                format_candidate_output(row["candidate_output"]),
                "```",
                "",
                "| rubric_dimension | deterministic_baseline | first_pass_label | second_pass_label | second_labeler_label | agreement_status | notes |",
                "|---|---|---|---|---|---|---|",
            ]
        )
        human = row["human_agreement"]
        baseline_scores = row["deterministic_baseline"]["scores"]
        for dimension in row["judge_dimensions"]:
            baseline_value = baseline_scores.get(dimension, "n/a")
            lines.append(
                "| {dimension} | {baseline} | {first_pass} | {second_pass} | {second_labeler} | {status} | {notes} |".format(
                    dimension=dimension,
                    baseline=baseline_value,
                    first_pass=human["first_pass_label"].get(dimension, ""),
                    second_pass=human["second_pass_label"].get(dimension, ""),
                    second_labeler=human["second_labeler_label"].get(dimension, ""),
                    status=human["agreement_status"].get(dimension, ""),
                    notes=human["notes"].get(dimension, ""),
                )
            )
        lines.append("")

    lines.extend(
        [
            "## Reporting Notes",
            "",
            "- If the human label fields are still blank, report the protocol as prepared but incomplete.",
            "- Do not overwrite existing human labels when refreshing the subset or rerendering this template.",
            "- Treat the deterministic baseline as a scaffold only; the actual agreement numbers must come from",
            "  human-entered labels in `docs/inter_rater_subset.jsonl`.",
            "",
        ]
    )

    output_path.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare and score inter-rater agreement scaffolding.")
    parser.add_argument("--subset-path", type=Path, default=DEFAULT_SUBSET_PATH)
    parser.add_argument("--dev-dir", type=Path, default=DEFAULT_DEV_DIR)
    parser.add_argument("--template-path", type=Path, default=DEFAULT_TEMPLATE_PATH)
    parser.add_argument("--threshold", type=float, default=0.8)
    parser.add_argument(
        "--bootstrap-subset",
        action="store_true",
        help="Create or refresh the JSONL subset from the existing dev tasks while preserving labels.",
    )
    parser.add_argument(
        "--render-template",
        action="store_true",
        help="Render inter_rater_agreement.md from the current subset file.",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Validate subset composition without failing on pending human labels.",
    )
    parser.add_argument(
        "--fail-below-threshold",
        action="store_true",
        help="Exit non-zero if any completed agreement rate falls below the threshold.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.bootstrap_subset:
        bootstrap_subset(args.subset_path, args.dev_dir)
    if args.render_template:
        render_template(args.subset_path, args.template_path)

    rows = load_jsonl(args.subset_path)
    validation_errors = validate_subset(rows)
    progress = summarize_label_progress(rows)
    agreement_summary = compute_agreement(rows, threshold=args.threshold)

    result = {
        "subset_path": args.subset_path.as_posix(),
        "task_count": len(rows),
        "dimension_counts": Counter(row["failure_dimension"] for row in rows),
        "source_modes": sorted({row["source_mode"] for row in rows}),
        "partitions": sorted({row["partition"] for row in rows}),
        "validation_errors": validation_errors,
        "label_progress": progress,
        "agreement": agreement_summary,
    }
    print(json.dumps(result, indent=2, sort_keys=True, default=str))

    if validation_errors:
        return 1
    if args.validate_only:
        return 0
    if args.fail_below_threshold:
        any_below_threshold = any(
            comparison["below_threshold"]
            for dimension in agreement_summary.values()
            for comparison in dimension.values()
        )
        if any_below_threshold:
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
