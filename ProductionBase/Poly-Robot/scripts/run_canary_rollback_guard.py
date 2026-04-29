#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from poly_robot.canary_rollback_guard import (  # noqa: E402
    append_canary_rollback_guard_audit_event,
    build_canary_rollback_guard_report,
)


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _cycle_report_sort_key(path: Path) -> tuple[int, str]:
    match = re.search(r"cycle_(\d+)", path.stem)
    if match is not None:
        return int(match.group(1)), str(path)
    return -1, str(path)


def _load_cycle_reports(
    *,
    cycle_report_dir: Path,
    cycle_report_pattern: str,
    max_cycle_reports: int,
) -> tuple[list[dict[str, Any]], list[str]]:
    if not cycle_report_dir.exists():
        return [], []
    report_paths = sorted(
        cycle_report_dir.glob(cycle_report_pattern),
        key=_cycle_report_sort_key,
    )
    if max_cycle_reports > 0 and len(report_paths) > max_cycle_reports:
        report_paths = report_paths[-max_cycle_reports:]
    reports: list[dict[str, Any]] = []
    report_path_strings: list[str] = []
    for path in report_paths:
        if not path.is_file():
            continue
        reports.append(_load_json(path))
        report_path_strings.append(str(path))
    return reports, report_path_strings


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Evaluate automated canary rollback enforcement triggers from canary "
            "artifacts and live-cycle telemetry, then emit incident handoff evidence."
        )
    )
    parser.add_argument(
        "--enablement-decision",
        type=Path,
        default=ROOT_DIR / "runtime" / "canary_stage_enablement_decision.json",
        help="Path to canary stage enablement decision artifact JSON.",
    )
    parser.add_argument(
        "--certification-report",
        type=Path,
        default=ROOT_DIR / "runtime" / "canary_rollout_certification_report.json",
        help="Path to canary readiness certification artifact JSON.",
    )
    parser.add_argument(
        "--rehearsal-report",
        type=Path,
        default=ROOT_DIR / "runtime" / "rollout_rehearsal_report.json",
        help="Path to rollout rehearsal report JSON.",
    )
    parser.add_argument(
        "--cycle-report-dir",
        type=Path,
        default=ROOT_DIR / "runtime" / "live_cycles",
        help="Directory containing live cycle telemetry JSON artifacts.",
    )
    parser.add_argument(
        "--cycle-report-pattern",
        type=str,
        default="cycle_*.json",
        help="Glob pattern used to load cycle telemetry reports.",
    )
    parser.add_argument(
        "--max-cycle-reports",
        type=int,
        default=0,
        help=(
            "Maximum number of most-recent cycle reports to evaluate; "
            "0 means all matching reports."
        ),
    )
    parser.add_argument(
        "--policy-config",
        type=Path,
        default=ROOT_DIR / "config" / "integration" / "canary_rollback_policy.v1.json",
        help="Path to canary rollback guard policy JSON.",
    )
    parser.add_argument(
        "--guard-output",
        type=Path,
        default=ROOT_DIR / "runtime" / "canary_rollback_guard_report.json",
        help="Path to write rollback guard report JSON.",
    )
    parser.add_argument(
        "--incident-output",
        type=Path,
        default=ROOT_DIR / "runtime" / "canary_rollback_incident_report.json",
        help="Path to write rollback incident handoff JSON.",
    )
    parser.add_argument(
        "--audit-output",
        type=Path,
        default=ROOT_DIR / "runtime" / "canary_rollback_guard_audit.jsonl",
        help="Append-only JSONL audit path for rollback guard evaluations.",
    )
    parser.add_argument(
        "--actor",
        type=str,
        default="canary_rollback_guard_runner",
        help="Actor identity recorded in rollback guard audit event.",
    )
    parser.add_argument(
        "--reason",
        type=str,
        required=False,
        help="Optional note stored with rollback guard audit event.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)

    enablement_decision = _load_json(args.enablement_decision)
    certification_report = _load_json(args.certification_report)
    rehearsal_report = _load_json(args.rehearsal_report)
    policy = _load_json(args.policy_config)
    cycle_reports, cycle_report_paths = _load_cycle_reports(
        cycle_report_dir=args.cycle_report_dir,
        cycle_report_pattern=args.cycle_report_pattern,
        max_cycle_reports=args.max_cycle_reports,
    )

    guard_report = build_canary_rollback_guard_report(
        canary_enablement_decision=enablement_decision,
        certification_report=certification_report,
        rehearsal_report=rehearsal_report,
        cycle_reports=cycle_reports,
        policy=policy,
        metadata={
            "enablement_decision_path": str(args.enablement_decision),
            "certification_report_path": str(args.certification_report),
            "rehearsal_report_path": str(args.rehearsal_report),
            "policy_config_path": str(args.policy_config),
            "cycle_report_dir": str(args.cycle_report_dir),
            "cycle_report_pattern": args.cycle_report_pattern,
            "cycle_report_paths": cycle_report_paths,
        },
    )
    incident_handoff = guard_report.get("incident_handoff", {})

    args.guard_output.parent.mkdir(parents=True, exist_ok=True)
    args.guard_output.write_text(
        json.dumps(guard_report, indent=2) + "\n",
        encoding="utf-8",
    )
    args.incident_output.parent.mkdir(parents=True, exist_ok=True)
    args.incident_output.write_text(
        json.dumps(incident_handoff, indent=2) + "\n",
        encoding="utf-8",
    )

    audit_event = append_canary_rollback_guard_audit_event(
        audit_path=args.audit_output,
        guard_report=guard_report,
        actor=args.actor,
        reason=args.reason,
    )

    print(
        "Canary rollback guard complete: "
        f"guard_status={guard_report['guard_status']} "
        f"triggered_conditions={guard_report['triggered_condition_count']} "
        f"incident_status={incident_handoff.get('incident_status', 'UNKNOWN')} "
        f"cycle_reports={guard_report['telemetry_summary']['cycle_report_count']} "
        f"guard_output={args.guard_output} "
        f"incident_output={args.incident_output} "
        f"audit_output={args.audit_output} "
        f"audit_guard_hash={audit_event['guard_hash']}"
    )
    return 0 if guard_report["guard_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
