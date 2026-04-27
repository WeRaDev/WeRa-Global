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

from poly_robot.canary_readiness import build_canary_readiness_report  # noqa: E402


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Build canary rollout readiness certification from rollout rehearsal "
            "evidence with weighted scoring and blocking criteria."
        )
    )
    parser.add_argument(
        "--rehearsal-report",
        type=Path,
        default=ROOT_DIR / "runtime" / "rollout_rehearsal_report.json",
        help="Path to rollout rehearsal report JSON artifact.",
    )
    parser.add_argument(
        "--criteria-config",
        type=Path,
        default=ROOT_DIR / "config" / "integration" / "canary_promotion_criteria.v1.json",
        help="Path to canary promotion criteria and approval policy JSON.",
    )
    parser.add_argument(
        "--approval-status",
        type=str,
        choices=["pending", "approved", "rejected"],
        default="pending",
        help="Manual approval status for canary enablement decision metadata.",
    )
    parser.add_argument(
        "--approval-actor",
        type=str,
        required=False,
        help="Optional approver identity recorded in certification metadata.",
    )
    parser.add_argument(
        "--approval-note",
        type=str,
        required=False,
        help="Optional approval note captured in certification metadata.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT_DIR / "runtime" / "canary_rollout_certification_report.json",
        help="Path to write canary readiness certification report JSON.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    rehearsal_report = _load_json(args.rehearsal_report)
    criteria_config = _load_json(args.criteria_config)
    report = build_canary_readiness_report(
        rehearsal_report=rehearsal_report,
        policy=criteria_config,
        approval_status=args.approval_status,
        approval_actor=args.approval_actor,
        approval_note=args.approval_note,
        metadata={
            "rehearsal_report_path": str(args.rehearsal_report),
            "criteria_config_path": str(args.criteria_config),
        },
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(
        "Canary readiness certification complete: "
        f"overall_status={report['overall_status']} "
        f"readiness_score={report['readiness_score']:.3f} "
        f"blockers={len(report['blockers'])} "
        "canary_enablement_allowed="
        f"{report['promotion_decision']['canary_enablement_allowed']} "
        f"output_path={args.output}"
    )
    return 0 if report["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
