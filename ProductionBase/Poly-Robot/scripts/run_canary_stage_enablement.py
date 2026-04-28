#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
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


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Build audited canary stage enablement ALLOW/DENY decision from canary "
            "readiness certification, approval record, and rollout-stage controls, "
            "including financial and micro-notional promotion gates."
        )
    )
    parser.add_argument(
        "--certification-report",
        type=Path,
        default=ROOT_DIR / "runtime" / "canary_rollout_certification_report.json",
        help="Path to canary readiness certification report JSON artifact.",
    )
    parser.add_argument(
        "--approval-record",
        type=Path,
        default=ROOT_DIR
        / "config"
        / "integration"
        / "canary_approval_record_template.v1.json",
        help="Path to canary approval record JSON artifact.",
    )
    parser.add_argument(
        "--rollout-config",
        type=Path,
        default=ROOT_DIR / "config" / "integration" / "live_trade_rollout.v1.json",
        help="Path to live rollout stage controls JSON.",
    )
    parser.add_argument(
        "--requested-stage",
        type=str,
        default="canary_live",
        help="Rollout stage requested for enablement decision.",
    )
    parser.add_argument(
        "--decision-output",
        type=Path,
        default=ROOT_DIR / "runtime" / "canary_stage_enablement_decision.json",
        help="Path to write canary stage enablement decision JSON.",
    )
    parser.add_argument(
        "--audit-output",
        type=Path,
        default=ROOT_DIR / "runtime" / "canary_stage_enablement_audit.jsonl",
        help="Append-only JSONL audit path for canary stage enablement decisions.",
    )
    parser.add_argument(
        "--actor",
        type=str,
        default="canary_enablement_runner",
        help="Actor identity recorded in append-only enablement audit event.",
    )
    parser.add_argument(
        "--reason",
        type=str,
        required=False,
        help="Optional decision note captured in append-only audit event.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    certification_report = _load_json(args.certification_report)
    approval_record = _load_json(args.approval_record)
    rollout_config = _load_json(args.rollout_config)

    decision_report = build_canary_stage_enablement_decision(
        certification_report=certification_report,
        approval_record=approval_record,
        rollout_config=rollout_config,
        requested_stage=args.requested_stage,
        metadata={
            "certification_report_path": str(args.certification_report),
            "approval_record_path": str(args.approval_record),
            "rollout_config_path": str(args.rollout_config),
        },
    )

    args.decision_output.parent.mkdir(parents=True, exist_ok=True)
    args.decision_output.write_text(
        json.dumps(decision_report, indent=2) + "\n",
        encoding="utf-8",
    )

    audit_event = append_canary_stage_enablement_audit_event(
        audit_path=args.audit_output,
        decision_report=decision_report,
        actor=args.actor,
        reason=args.reason,
    )

    print(
        "Canary stage enablement decision complete: "
        f"decision_status={decision_report['decision_status']} "
        "canary_stage_enablement_allowed="
        f"{decision_report['canary_stage_enablement_allowed']} "
        f"failed_reason_codes={len(decision_report['failed_reason_codes'])} "
        f"decision_output={args.decision_output} "
        f"audit_output={args.audit_output} "
        f"audit_decision_hash={audit_event['decision_hash']}"
    )
    return 0 if decision_report["decision_status"] == "ALLOW" else 1


if __name__ == "__main__":
    raise SystemExit(main())
