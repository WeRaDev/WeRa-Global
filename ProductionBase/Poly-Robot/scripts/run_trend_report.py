#!/usr/bin/env python3
"""Weekly trend report runner for Poly-Robot.

Reads supervisor journal and lifecycle gate outputs to produce a
formatted reliability + economics summary.
"""
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


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="milliseconds")


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def _extract_journal_summary(
    journal_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    """Extract reliability and economics metrics from supervisor journal."""
    cycle_count = 0
    ingestion_ok_count = 0
    ingestion_degraded_count = 0
    worker_failure_count = 0
    total_risk_allowed = 0
    total_fills = 0
    total_exits = 0

    for row in journal_rows:
        event_type = row.get("event_type", "")
        payload = row.get("payload", {})
        if not isinstance(payload, dict):
            continue

        if event_type == "worker_heartbeat" and payload.get("stage") == "cycle_completed":
            cycle_count += 1
            details = payload.get("details", {})
            if isinstance(details, dict):
                total_risk_allowed += int(details.get("risk_allowed_count", 0) or 0)
                total_fills += int(details.get("filled_trade_count", 0) or 0)
                total_exits += int(details.get("confirmed_exit_count", 0) or 0)

        if event_type == "ingestion_status":
            status = str(payload.get("status", "")).upper()
            if status == "OK":
                ingestion_ok_count += 1
            elif status == "DEGRADED":
                ingestion_degraded_count += 1

        if event_type == "worker_failure":
            worker_failure_count += 1

    return {
        "cycle_count": cycle_count,
        "ingestion_ok_count": ingestion_ok_count,
        "ingestion_degraded_count": ingestion_degraded_count,
        "worker_failure_count": worker_failure_count,
        "total_risk_allowed": total_risk_allowed,
        "total_fills": total_fills,
        "total_exits": total_exits,
        "avg_trades_per_cycle": round(total_risk_allowed / max(1, cycle_count), 2),
        "avg_fills_per_cycle": round(total_fills / max(1, cycle_count), 2),
    }


def _extract_gate_summary(gate_report: dict[str, Any]) -> dict[str, Any]:
    """Extract key fields from a TRL4 or lifecycle gate report."""
    return {
        "overall_status": gate_report.get("overall_status", "UNKNOWN"),
        "reliability_status": gate_report.get("reliability_status", "N/A"),
        "economic_quality_status": gate_report.get("economic_quality_status", "N/A"),
        "gate_mode": gate_report.get("gate_mode", "N/A"),
        "cycle_count": (gate_report.get("runtime", {}) or {}).get("cycle_count"),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate weekly trend report")
    parser.add_argument(
        "--journal-path",
        type=Path,
        default=ROOT_DIR / "runtime" / "runtime_journal.jsonl",
    )
    parser.add_argument(
        "--gate-report-path",
        type=Path,
        default=ROOT_DIR / "runtime" / "trl4_24h_report.json",
    )
    parser.add_argument(
        "--lifecycle-report-path",
        type=Path,
        default=ROOT_DIR / "runtime" / "canary_lifecycle_gate_report.json",
    )
    parser.add_argument(
        "--output", type=Path, required=True, help="Output report JSON"
    )
    args = parser.parse_args(argv)

    journal_rows = _load_jsonl(args.journal_path)
    gate_report = _load_json(args.gate_report_path)
    lifecycle_report = _load_json(args.lifecycle_report_path)

    journal_summary = _extract_journal_summary(journal_rows)
    gate_summary = _extract_gate_summary(gate_report)
    lifecycle_summary = _extract_gate_summary(lifecycle_report)

    report = {
        "schema_version": "weekly_trend_report.v1",
        "generated_at": _utc_now_iso(),
        "period": {
            "journal_events": len(journal_rows),
        },
        "reliability": {
            "cycle_count": journal_summary["cycle_count"],
            "ingestion_ok_count": journal_summary["ingestion_ok_count"],
            "ingestion_degraded_count": journal_summary["ingestion_degraded_count"],
            "worker_failure_count": journal_summary["worker_failure_count"],
        },
        "economics": {
            "total_risk_allowed": journal_summary["total_risk_allowed"],
            "total_fills": journal_summary["total_fills"],
            "total_exits": journal_summary["total_exits"],
            "avg_trades_per_cycle": journal_summary["avg_trades_per_cycle"],
            "avg_fills_per_cycle": journal_summary["avg_fills_per_cycle"],
        },
        "gate_status": {
            "trl4": gate_summary,
            "lifecycle": lifecycle_summary,
        },
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(
        f"Trend report: cycles={journal_summary['cycle_count']} "
        f"trades={journal_summary['total_risk_allowed']} "
        f"fills={journal_summary['total_fills']} "
        f"trl4={gate_summary['overall_status']} "
        f"output={args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
