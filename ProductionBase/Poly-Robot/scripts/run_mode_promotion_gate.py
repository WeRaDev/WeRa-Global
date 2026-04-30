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

from poly_robot.mode_lifecycle import (  # noqa: E402
    build_mode_transition_decision,
    normalize_mode,
    resolve_mode_lifecycle_policy,
)
from poly_robot.reproducibility import stable_hash  # noqa: E402
from poly_robot.schemas import (  # noqa: E402
    MODE_PROMOTION_GATE_AUDIT_EVENT_SCHEMA_VERSION,
    MODE_PROMOTION_GATE_REPORT_SCHEMA_VERSION,
)

PASS_STATUSES = {"PASS", "SUCCESS", "ALLOW", "OK", "APPROVED", "TRUE", "1"}
FAIL_STATUSES = {"FAIL", "FAILED", "DENY", "ERROR", "REJECTED", "FALSE", "0"}


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="milliseconds")


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


def _normalize_status(value: Any) -> str:
    return str(value or "").strip().upper()


def _extract_status(payload: dict[str, Any]) -> str:
    for field_name in (
        "overall_status",
        "status",
        "decision_status",
        "guard_status",
        "certification_status",
    ):
        if field_name in payload:
            status = _normalize_status(payload.get(field_name))
            if status:
                return status
    certification_payload = payload.get("certification")
    if isinstance(certification_payload, dict):
        status = _normalize_status(
            certification_payload.get("overall_status")
            or certification_payload.get("status")
        )
        if status:
            return status
    if "passed" in payload and isinstance(payload.get("passed"), bool):
        return "PASS" if bool(payload.get("passed")) else "FAIL"
    return ""


def _status_to_passed(payload: dict[str, Any], status: str) -> bool:
    if status in PASS_STATUSES:
        return True
    if status in FAIL_STATUSES:
        return False
    if "passed" in payload and isinstance(payload.get("passed"), bool):
        return bool(payload.get("passed"))
    return False


def _build_evidence_entry(path: Path) -> tuple[dict[str, Any], dict[str, Any] | None]:
    summary: dict[str, Any] = {
        "path": str(path),
        "exists": path.exists(),
    }
    if not path.exists():
        return summary, None

    payload = _load_json(path)
    status = _extract_status(payload)
    passed = _status_to_passed(payload, status)
    artifact_hash = stable_hash(payload)
    summary.update(
        {
            "status": status,
            "passed": passed,
            "artifact_hash": artifact_hash,
        }
    )
    evidence = {
        "status": status,
        "passed": passed,
        "artifact_hash": artifact_hash,
        "artifact_path": str(path),
    }
    return summary, evidence


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Evaluate paper/test/live transition evidence against mode lifecycle "
            "policy and emit an audited promotion decision."
        )
    )
    parser.add_argument(
        "--mode-lifecycle-policy",
        type=Path,
        default=ROOT_DIR
        / "config"
        / "integration"
        / "mode_lifecycle_policy.v1.json",
        help="Path to mode lifecycle policy JSON.",
    )
    parser.add_argument(
        "--current-mode",
        type=str,
        required=True,
        choices=["paper", "test", "live"],
        help="Current lifecycle mode.",
    )
    parser.add_argument(
        "--target-mode",
        type=str,
        required=True,
        choices=["paper", "test", "live"],
        help="Requested lifecycle target mode.",
    )
    parser.add_argument(
        "--manual-approval-status",
        type=str,
        choices=["pending", "approved", "rejected"],
        default="pending",
        help="Manual approval status used during transition decisioning.",
    )
    parser.add_argument(
        "--milestone-c-sequence-report",
        type=Path,
        default=ROOT_DIR
        / "runtime"
        / "milestone_c_sequence"
        / "milestone_c_sequence_summary.json",
        help="Milestone-C sequence report used for paper->test gating.",
    )
    parser.add_argument(
        "--trl4-profitability-report",
        type=Path,
        default=ROOT_DIR / "runtime" / "trl4_24h_report.json",
        help="TRL4 profitability report used for paper->test gating.",
    )
    parser.add_argument(
        "--canary-lifecycle-gate-report",
        type=Path,
        default=ROOT_DIR / "runtime" / "canary_lifecycle_gate_report.json",
        help="Canary lifecycle gate report used for test->live gating.",
    )
    parser.add_argument(
        "--test-mode-profitability-report",
        type=Path,
        default=ROOT_DIR / "runtime" / "test_mode_profitability_report.json",
        help="Test-mode profitability report used for test->live gating.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT_DIR / "runtime" / "mode_promotion_gate_report.json",
        help="Output path for promotion gate report JSON.",
    )
    parser.add_argument(
        "--audit-output",
        type=Path,
        default=ROOT_DIR / "runtime" / "mode_promotion_audit.jsonl",
        help="Append-only audit JSONL path for promotion gate decisions.",
    )
    parser.add_argument(
        "--actor",
        type=str,
        default="mode_promotion_gate_runner",
        help="Actor identity persisted in promotion audit events.",
    )
    parser.add_argument(
        "--reason",
        type=str,
        required=False,
        help="Optional reason persisted in promotion report and audit event.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    lifecycle_policy_payload = (
        _load_json(args.mode_lifecycle_policy)
        if args.mode_lifecycle_policy.exists()
        else {}
    )
    resolved_lifecycle_policy = resolve_mode_lifecycle_policy(lifecycle_policy_payload)
    lifecycle_policy_hash = stable_hash(resolved_lifecycle_policy)

    evidence_paths = {
        "milestone_c_sequence": args.milestone_c_sequence_report,
        "trl4_profitability": args.trl4_profitability_report,
        "canary_lifecycle_gate": args.canary_lifecycle_gate_report,
        "test_mode_profitability": args.test_mode_profitability_report,
    }
    evidence_summary: dict[str, dict[str, Any]] = {}
    evidence_payload: dict[str, dict[str, Any]] = {}
    for evidence_key, evidence_path in evidence_paths.items():
        summary, evidence = _build_evidence_entry(evidence_path)
        evidence_summary[evidence_key] = summary
        if evidence is not None:
            evidence_payload[evidence_key] = evidence

    current_mode = normalize_mode(args.current_mode)
    target_mode = normalize_mode(args.target_mode)
    decision = build_mode_transition_decision(
        current_mode=current_mode,
        target_mode=target_mode,
        policy=resolved_lifecycle_policy,
        evidence=evidence_payload,
        manual_approval_status=args.manual_approval_status,
        actor=args.actor,
        reason=args.reason,
    )
    decision_allowed = bool(decision.get("allowed", False))
    decision_status = "ALLOW" if decision_allowed else "DENY"
    report = {
        "schema_version": MODE_PROMOTION_GATE_REPORT_SCHEMA_VERSION,
        "generated_at": _utc_now_iso(),
        "decision_status": decision_status,
        "promotion_allowed": decision_allowed,
        "current_mode": current_mode,
        "target_mode": target_mode,
        "transition_id": str(decision.get("transition_id", "")),
        "manual_approval_status": str(args.manual_approval_status),
        "actor": str(args.actor),
        "reason": str(args.reason or ""),
        "mode_lifecycle_policy_path": str(args.mode_lifecycle_policy),
        "mode_lifecycle_policy_hash": lifecycle_policy_hash,
        "evidence_inputs": evidence_summary,
        "decision": decision,
        "required_evidence": list(decision.get("required_evidence", [])),
        "missing_evidence": list(decision.get("missing_evidence", [])),
        "failing_evidence": list(decision.get("failing_evidence", [])),
        "reason_codes": list(decision.get("reason_codes", [])),
    }
    report["report_hash"] = stable_hash(
        {
            "decision_status": report["decision_status"],
            "promotion_allowed": report["promotion_allowed"],
            "current_mode": report["current_mode"],
            "target_mode": report["target_mode"],
            "transition_id": report["transition_id"],
            "manual_approval_status": report["manual_approval_status"],
            "mode_lifecycle_policy_hash": report["mode_lifecycle_policy_hash"],
            "decision_hash": decision.get("decision_hash"),
            "missing_evidence": report["missing_evidence"],
            "failing_evidence": report["failing_evidence"],
            "reason_codes": report["reason_codes"],
            "evidence_inputs": report["evidence_inputs"],
        }
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    audit_event = {
        "schema_version": MODE_PROMOTION_GATE_AUDIT_EVENT_SCHEMA_VERSION,
        "timestamp": _utc_now_iso(),
        "actor": str(args.actor),
        "reason": str(args.reason or ""),
        "current_mode": current_mode,
        "target_mode": target_mode,
        "transition_id": report["transition_id"],
        "decision_status": decision_status,
        "promotion_allowed": decision_allowed,
        "decision_hash": str(decision.get("decision_hash", "")),
        "report_hash": report["report_hash"],
        "report_path": str(args.output),
        "reason_codes": list(report["reason_codes"]),
        "missing_evidence": list(report["missing_evidence"]),
        "failing_evidence": list(report["failing_evidence"]),
    }
    audit_event["audit_hash"] = stable_hash(
        {
            "timestamp": audit_event["timestamp"],
            "actor": audit_event["actor"],
            "reason": audit_event["reason"],
            "current_mode": audit_event["current_mode"],
            "target_mode": audit_event["target_mode"],
            "transition_id": audit_event["transition_id"],
            "decision_status": audit_event["decision_status"],
            "promotion_allowed": audit_event["promotion_allowed"],
            "decision_hash": audit_event["decision_hash"],
            "report_hash": audit_event["report_hash"],
            "reason_codes": audit_event["reason_codes"],
            "missing_evidence": audit_event["missing_evidence"],
            "failing_evidence": audit_event["failing_evidence"],
        }
    )
    _append_jsonl(args.audit_output, audit_event)

    print(
        "Mode promotion gate complete: "
        f"transition={report['transition_id']} "
        f"decision={decision_status} "
        f"promotion_allowed={decision_allowed} "
        f"decision_hash={str(decision.get('decision_hash', ''))[:12]} "
        f"output={args.output}"
    )
    return 0 if decision_allowed else 1


if __name__ == "__main__":
    raise SystemExit(main())
