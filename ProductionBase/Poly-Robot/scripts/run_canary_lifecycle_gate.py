#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from poly_robot.canary_enablement import (  # noqa: E402
    append_canary_stage_enablement_audit_event,
    build_canary_stage_enablement_decision,
)
from poly_robot.canary_readiness import build_canary_readiness_report  # noqa: E402
from poly_robot.canary_rollback_guard import (  # noqa: E402
    append_canary_rollback_guard_audit_event,
    build_canary_rollback_guard_report,
)
from poly_robot.schemas import CANARY_LIFECYCLE_GATE_REPORT_SCHEMA_VERSION  # noqa: E402


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="milliseconds")


def _as_dict(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    return {}


def _as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    return []


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _load_cycle_reports(
    *,
    cycle_report_dir: Path,
    cycle_report_pattern: str,
    max_cycle_reports: int,
) -> tuple[list[dict[str, Any]], list[str]]:
    if not cycle_report_dir.exists():
        return [], []
    report_paths = sorted(cycle_report_dir.glob(cycle_report_pattern))
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


def _auto_approve_required_approvers(
    *, approval_record: dict[str, Any], required_approvers: list[str]
) -> dict[str, Any]:
    updated_record = json.loads(json.dumps(approval_record))
    approvals = [
        entry
        for entry in _as_list(updated_record.get("approvals"))
        if isinstance(entry, dict)
    ]
    approvals_by_actor: dict[str, dict[str, Any]] = {}
    for entry in approvals:
        actor = str(entry.get("actor", "")).strip()
        if actor and actor not in approvals_by_actor:
            approvals_by_actor[actor] = entry

    now = _utc_now_iso()
    note_suffix = "[auto-approved-required-approver]"
    for required_actor in required_approvers:
        actor = str(required_actor).strip()
        if not actor:
            continue
        entry = approvals_by_actor.get(actor)
        if entry is None:
            entry = {"actor": actor}
            approvals.append(entry)
            approvals_by_actor[actor] = entry
        entry["decision"] = "approved"
        entry["recorded_at"] = now
        existing_note = str(entry.get("note", "")).strip()
        if note_suffix in existing_note:
            entry["note"] = existing_note
        elif existing_note:
            entry["note"] = f"{existing_note} {note_suffix}"
        else:
            entry["note"] = note_suffix

    updated_record["approvals"] = approvals
    updated_record["updated_at"] = now
    return updated_record


def _build_summary_report(
    *,
    requested_stage: str,
    certification_report: dict[str, Any],
    decision_report: dict[str, Any],
    guard_report: dict[str, Any],
    incident_handoff: dict[str, Any],
    cycle_report_paths: list[str],
    artifact_paths: dict[str, str],
    auto_approve_required_approvers: bool,
    decision_audit_event: dict[str, Any],
    guard_audit_event: dict[str, Any],
) -> dict[str, Any]:
    certification_status = str(
        certification_report.get("overall_status", "UNKNOWN")
    ).strip()
    decision_status = str(decision_report.get("decision_status", "UNKNOWN")).strip()
    guard_status = str(guard_report.get("guard_status", "UNKNOWN")).strip()
    incident_status = str(incident_handoff.get("incident_status", "UNKNOWN")).strip()
    triggered_condition_ids = [
        str(item.get("id", "")).strip()
        for item in _as_list(guard_report.get("triggered_conditions"))
        if isinstance(item, dict) and str(item.get("id", "")).strip()
    ]
    overall_status = (
        "PASS"
        if (
            certification_status == "PASS"
            and decision_status == "ALLOW"
            and guard_status == "PASS"
            and incident_status == "NONE"
        )
        else "FAIL"
    )

    return {
        "schema_version": CANARY_LIFECYCLE_GATE_REPORT_SCHEMA_VERSION,
        "generated_at": _utc_now_iso(),
        "requested_stage": requested_stage,
        "overall_status": overall_status,
        "statuses": {
            "certification_status": certification_status,
            "enablement_decision_status": decision_status,
            "rollback_guard_status": guard_status,
            "incident_status": incident_status,
        },
        "promotion_allowed": bool(
            decision_report.get("canary_stage_enablement_allowed", False)
        ),
        "incident_required": bool(guard_report.get("incident_required", False)),
        "failed_reason_codes": list(decision_report.get("failed_reason_codes", [])),
        "triggered_condition_ids": triggered_condition_ids,
        "auto_approved_required_approvers": auto_approve_required_approvers,
        "cycle_report_paths": cycle_report_paths,
        "artifact_paths": artifact_paths,
        "evidence": {
            "certification_hash": str(
                _as_dict(certification_report.get("evidence")).get(
                    "certification_hash", ""
                )
            ).strip(),
            "decision_hash": str(
                _as_dict(decision_report.get("evidence")).get("decision_hash", "")
            ).strip(),
            "guard_hash": str(
                _as_dict(guard_report.get("evidence")).get("guard_hash", "")
            ).strip(),
            "decision_audit_hash": str(
                decision_audit_event.get("decision_hash", "")
            ).strip(),
            "guard_audit_hash": str(guard_audit_event.get("guard_hash", "")).strip(),
        },
    }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run canary readiness certification, stage enablement decisioning, and "
            "rollback guard evaluation as a single lifecycle gate sequence."
        )
    )
    parser.add_argument(
        "--rehearsal-report",
        type=Path,
        default=ROOT_DIR / "runtime" / "rollout_rehearsal_report.json",
        help="Path to rollout rehearsal report artifact JSON.",
    )
    parser.add_argument(
        "--criteria-config",
        type=Path,
        default=ROOT_DIR / "config" / "integration" / "canary_promotion_criteria.v1.json",
        help="Path to canary readiness certification criteria config JSON.",
    )
    parser.add_argument(
        "--approval-record",
        type=Path,
        default=ROOT_DIR
        / "config"
        / "integration"
        / "canary_approval_record_template.v1.json",
        help="Path to canary approval record JSON.",
    )
    parser.add_argument(
        "--rollout-config",
        type=Path,
        default=ROOT_DIR / "config" / "integration" / "live_trade_rollout.v1.json",
        help="Path to rollout stage control config JSON.",
    )
    parser.add_argument(
        "--policy-config",
        type=Path,
        default=ROOT_DIR / "config" / "integration" / "canary_rollback_policy.v1.json",
        help="Path to canary rollback guard policy JSON.",
    )
    parser.add_argument(
        "--cycle-report-dir",
        type=Path,
        default=ROOT_DIR / "runtime" / "rollout_rehearsal",
        help="Directory containing cycle report artifacts for rollback guard input.",
    )
    parser.add_argument(
        "--cycle-report-pattern",
        type=str,
        default="**/cycle_*.json",
        help="Glob pattern used to load cycle report artifacts.",
    )
    parser.add_argument(
        "--max-cycle-reports",
        type=int,
        default=0,
        help="Maximum number of most-recent cycle reports to load; 0 means all.",
    )
    parser.add_argument(
        "--requested-stage",
        type=str,
        default="canary_live",
        help="Requested rollout stage evaluated by stage enablement decisioning.",
    )
    parser.add_argument(
        "--approval-status",
        type=str,
        choices=["pending", "approved", "rejected"],
        default="pending",
        help="Manual approval status supplied to readiness certification metadata.",
    )
    parser.add_argument(
        "--approval-actor",
        type=str,
        required=False,
        help="Optional approval actor supplied to readiness certification metadata.",
    )
    parser.add_argument(
        "--approval-note",
        type=str,
        required=False,
        help="Optional approval note supplied to readiness certification metadata.",
    )
    parser.add_argument(
        "--auto-approve-required-approvers",
        action="store_true",
        help=(
            "When set, mutate approval-record payload in-memory to mark all required "
            "approvers as approved before stage enablement evaluation."
        ),
    )
    parser.add_argument(
        "--certification-output",
        type=Path,
        default=ROOT_DIR / "runtime" / "canary_rollout_certification_report.json",
        help="Path to write canary readiness certification report JSON.",
    )
    parser.add_argument(
        "--decision-output",
        type=Path,
        default=ROOT_DIR / "runtime" / "canary_stage_enablement_decision.json",
        help="Path to write canary stage enablement decision JSON.",
    )
    parser.add_argument(
        "--enablement-audit-output",
        type=Path,
        default=ROOT_DIR / "runtime" / "canary_stage_enablement_audit.jsonl",
        help="Append-only JSONL audit path for canary stage enablement decisions.",
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
        help="Path to write rollback incident handoff report JSON.",
    )
    parser.add_argument(
        "--guard-audit-output",
        type=Path,
        default=ROOT_DIR / "runtime" / "canary_rollback_guard_audit.jsonl",
        help="Append-only JSONL audit path for rollback guard evaluations.",
    )
    parser.add_argument(
        "--summary-output",
        type=Path,
        default=ROOT_DIR / "runtime" / "canary_lifecycle_gate_report.json",
        help="Path to write consolidated lifecycle gate summary JSON.",
    )
    parser.add_argument(
        "--decision-actor",
        type=str,
        default="canary_lifecycle_gate_runner",
        help="Actor identity written to stage enablement audit events.",
    )
    parser.add_argument(
        "--guard-actor",
        type=str,
        default="runtime_operator_on_call",
        help="Actor identity written to rollback guard audit events.",
    )
    parser.add_argument(
        "--reason",
        type=str,
        required=False,
        help="Optional reason persisted in stage enablement and rollback guard audits.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    rehearsal_report = _load_json(args.rehearsal_report)
    criteria_config = _load_json(args.criteria_config)
    approval_record = _load_json(args.approval_record)
    rollout_config = _load_json(args.rollout_config)
    rollback_policy = _load_json(args.policy_config)
    cycle_reports, cycle_report_paths = _load_cycle_reports(
        cycle_report_dir=args.cycle_report_dir,
        cycle_report_pattern=args.cycle_report_pattern,
        max_cycle_reports=args.max_cycle_reports,
    )

    certification_report = build_canary_readiness_report(
        rehearsal_report=rehearsal_report,
        policy=criteria_config,
        approval_status=args.approval_status,
        approval_actor=args.approval_actor,
        approval_note=args.approval_note,
        metadata={
            "rehearsal_report_path": str(args.rehearsal_report),
            "criteria_config_path": str(args.criteria_config),
            "lifecycle_gate_runner": "run_canary_lifecycle_gate.py",
        },
    )
    _write_json(args.certification_output, certification_report)

    required_approvers = [
        str(value).strip()
        for value in _as_list(
            _as_dict(certification_report.get("promotion_decision")).get(
                "required_approvers"
            )
        )
        if str(value).strip()
    ]
    if args.auto_approve_required_approvers:
        approval_record = _auto_approve_required_approvers(
            approval_record=approval_record,
            required_approvers=required_approvers,
        )

    decision_report = build_canary_stage_enablement_decision(
        certification_report=certification_report,
        approval_record=approval_record,
        rollout_config=rollout_config,
        requested_stage=args.requested_stage,
        metadata={
            "certification_report_path": str(args.certification_output),
            "approval_record_path": str(args.approval_record),
            "approval_record_auto_approved": args.auto_approve_required_approvers,
            "rollout_config_path": str(args.rollout_config),
        },
    )
    _write_json(args.decision_output, decision_report)
    decision_audit_event = append_canary_stage_enablement_audit_event(
        audit_path=args.enablement_audit_output,
        decision_report=decision_report,
        actor=args.decision_actor,
        reason=args.reason,
    )

    guard_report = build_canary_rollback_guard_report(
        canary_enablement_decision=decision_report,
        certification_report=certification_report,
        rehearsal_report=rehearsal_report,
        cycle_reports=cycle_reports,
        policy=rollback_policy,
        metadata={
            "decision_output_path": str(args.decision_output),
            "certification_output_path": str(args.certification_output),
            "rehearsal_report_path": str(args.rehearsal_report),
            "cycle_report_dir": str(args.cycle_report_dir),
            "cycle_report_pattern": args.cycle_report_pattern,
            "cycle_report_paths": cycle_report_paths,
            "rollback_policy_path": str(args.policy_config),
        },
    )
    incident_handoff = _as_dict(guard_report.get("incident_handoff"))
    _write_json(args.guard_output, guard_report)
    _write_json(args.incident_output, incident_handoff)
    guard_audit_event = append_canary_rollback_guard_audit_event(
        audit_path=args.guard_audit_output,
        guard_report=guard_report,
        actor=args.guard_actor,
        reason=args.reason,
    )

    artifact_paths = {
        "certification_report": str(args.certification_output),
        "decision_report": str(args.decision_output),
        "enablement_audit": str(args.enablement_audit_output),
        "guard_report": str(args.guard_output),
        "incident_report": str(args.incident_output),
        "guard_audit": str(args.guard_audit_output),
        "summary_report": str(args.summary_output),
    }
    summary_report = _build_summary_report(
        requested_stage=args.requested_stage,
        certification_report=certification_report,
        decision_report=decision_report,
        guard_report=guard_report,
        incident_handoff=incident_handoff,
        cycle_report_paths=cycle_report_paths,
        artifact_paths=artifact_paths,
        auto_approve_required_approvers=args.auto_approve_required_approvers,
        decision_audit_event=decision_audit_event,
        guard_audit_event=guard_audit_event,
    )
    _write_json(args.summary_output, summary_report)

    print(
        "Canary lifecycle gate complete: "
        f"overall_status={summary_report['overall_status']} "
        f"certification={summary_report['statuses']['certification_status']} "
        f"decision={summary_report['statuses']['enablement_decision_status']} "
        f"guard={summary_report['statuses']['rollback_guard_status']} "
        f"incident={summary_report['statuses']['incident_status']} "
        f"summary_output={args.summary_output}"
    )

    return 0 if summary_report["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
