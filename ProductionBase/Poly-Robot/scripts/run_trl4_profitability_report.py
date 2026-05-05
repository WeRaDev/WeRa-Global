#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_GATE_CONFIG = (
    ROOT_DIR / "config" / "certification" / "trl4_24h_profitability_gate.v1.json"
)


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="milliseconds")


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rows.append(json.loads(line))
    return rows


def _parse_timestamp(raw_value: Any) -> datetime | None:
    if not isinstance(raw_value, str):
        return None
    value = raw_value.strip()
    if not value:
        return None
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    try:
        timestamp = datetime.fromisoformat(value)
    except ValueError:
        return None
    if timestamp.tzinfo is None:
        return timestamp.replace(tzinfo=UTC)
    return timestamp.astimezone(UTC)


def _as_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _as_int(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _metric_summary(values: list[float]) -> dict[str, Any]:
    if not values:
        return {
            "count": 0,
            "min": None,
            "max": None,
            "mean": None,
            "last": None,
        }
    return {
        "count": len(values),
        "min": round(min(values), 6),
        "max": round(max(values), 6),
        "mean": round(sum(values) / len(values), 6),
        "last": round(values[-1], 6),
    }


def _extract_cycle_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cycle_rows: list[dict[str, Any]] = []
    for row in rows:
        if row.get("event_type") != "worker_heartbeat":
            continue
        payload = row.get("payload")
        if not isinstance(payload, dict):
            continue
        if payload.get("worker_name") != "test_token_loop":
            continue
        if payload.get("stage") != "cycle_completed":
            continue
        details = payload.get("details")
        if not isinstance(details, dict):
            continue
        timestamp = _parse_timestamp(row.get("timestamp"))
        if timestamp is None:
            continue
        cycle_rows.append(
            {
                "timestamp": timestamp,
                "timestamp_raw": row.get("timestamp"),
                "cycle_index": _as_int(details.get("cycle_index")),
                "details": details,
            }
        )
    cycle_rows.sort(
        key=lambda row: (
            row["timestamp"],
            row["cycle_index"] if row["cycle_index"] is not None else 0,
        )
    )
    return cycle_rows


def _criterion(
    *,
    name: str,
    passed: bool,
    observed: Any,
    threshold: Any,
    description: str,
) -> dict[str, Any]:
    return {
        "name": name,
        "passed": bool(passed),
        "observed": observed,
        "threshold": threshold,
        "description": description,
    }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Evaluate Poly-Robot TRL4 24-hour runtime evidence and emit a "
            "profitability gate PASS/FAIL report."
        )
    )
    parser.add_argument(
        "--journal-path",
        type=Path,
        default=ROOT_DIR / "runtime" / "runtime_journal.jsonl",
        help="Runtime supervisor journal JSONL path.",
    )
    parser.add_argument(
        "--state-path",
        type=Path,
        default=ROOT_DIR / "runtime" / "runtime_state.json",
        help="Runtime supervisor state snapshot JSON path.",
    )
    parser.add_argument(
        "--gate-config",
        type=Path,
        default=DEFAULT_GATE_CONFIG,
        help="TRL4 profitability gate configuration JSON.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT_DIR / "runtime" / "trl4_24h_report.json",
        help="Output JSON report path.",
    )
    parser.add_argument(
        "--min-runtime-hours",
        type=float,
        required=False,
        help="Optional override for minimum required runtime hours.",
    )
    parser.add_argument(
        "--minimum-expected-value-after-execution-cost",
        type=float,
        required=False,
        help=(
            "Optional override for minimum required "
            "expected_value_after_execution_cost on the latest cycle."
        ),
    )
    parser.add_argument(
        "--minimum-expected-net-edge-value-on-fills",
        type=float,
        required=False,
        help=(
            "Optional override for minimum required "
            "expected_net_edge_value_on_fills on the latest cycle."
        ),
    )
    parser.add_argument(
        "--runtime-hours-per-cycle",
        type=float,
        required=False,
        help=(
            "Optional override for simulated runtime hours represented by each "
            "completed cycle. Effective runtime uses the larger of wall-clock "
            "duration and cycle_count * runtime_hours_per_cycle."
        ),
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    gate_config = _load_json(args.gate_config) if args.gate_config.exists() else {}

    min_runtime_hours = float(
        args.min_runtime_hours
        if args.min_runtime_hours is not None
        else gate_config.get("min_runtime_hours", 24.0)
    )
    minimum_expected_value_after_execution_cost = float(
        args.minimum_expected_value_after_execution_cost
        if args.minimum_expected_value_after_execution_cost is not None
        else gate_config.get("minimum_expected_value_after_execution_cost", 0.0)
    )
    minimum_expected_net_edge_value_on_fills = float(
        args.minimum_expected_net_edge_value_on_fills
        if args.minimum_expected_net_edge_value_on_fills is not None
        else gate_config.get("minimum_expected_net_edge_value_on_fills", 0.0)
    )
    runtime_hours_per_cycle = max(
        0.0,
        float(
            args.runtime_hours_per_cycle
            if args.runtime_hours_per_cycle is not None
            else gate_config.get("runtime_hours_per_cycle", 0.0)
        ),
    )
    require_profitability_metrics = bool(
        gate_config.get("require_profitability_metrics", True)
    )
    allow_negative_net_pnl = bool(gate_config.get("allow_negative_net_pnl", True))
    minimum_mean_expected_value_after_execution_cost = float(
        gate_config.get("minimum_mean_expected_value_after_execution_cost", 0.0)
    )

    journal_rows = _load_jsonl(args.journal_path)
    cycle_rows = _extract_cycle_rows(journal_rows)
    latest_cycle = cycle_rows[-1] if cycle_rows else None
    latest_details = latest_cycle["details"] if latest_cycle is not None else {}

    runtime_start = cycle_rows[0]["timestamp"] if cycle_rows else None
    runtime_end = cycle_rows[-1]["timestamp"] if cycle_rows else None
    runtime_duration_hours_wall_clock = (
        (runtime_end - runtime_start).total_seconds() / 3600
        if runtime_start is not None and runtime_end is not None
        else 0.0
    )
    runtime_duration_hours_cycle_based = len(cycle_rows) * runtime_hours_per_cycle
    runtime_duration_hours = runtime_duration_hours_wall_clock

    expected_value_after_execution_cost_values = [
        value
        for value in (
            _as_float(row["details"].get("expected_value_after_execution_cost"))
            for row in cycle_rows
        )
        if value is not None
    ]
    expected_net_edge_value_on_fills_values = [
        value
        for value in (
            _as_float(row["details"].get("expected_net_edge_value_on_fills"))
            for row in cycle_rows
        )
        if value is not None
    ]
    net_pnl_values = [
        value
        for value in (_as_float(row["details"].get("net_pnl")) for row in cycle_rows)
        if value is not None
    ]

    latest_expected_value_after_execution_cost = _as_float(
        latest_details.get("expected_value_after_execution_cost")
    )
    latest_expected_net_edge_value_on_fills = _as_float(
        latest_details.get("expected_net_edge_value_on_fills")
    )
    latest_net_pnl = _as_float(latest_details.get("net_pnl"))

    mean_expected_value_after_execution_cost: float | None = None
    if expected_value_after_execution_cost_values:
        mean_expected_value_after_execution_cost = sum(
            expected_value_after_execution_cost_values
        ) / len(expected_value_after_execution_cost_values)

    metrics_present = (
        latest_expected_value_after_execution_cost is not None
        and latest_expected_net_edge_value_on_fills is not None
        and latest_net_pnl is not None
    )

    state_payload = _load_json(args.state_path) if args.state_path.exists() else None
    state_cycle_index = _as_int((state_payload or {}).get("cycle_index"))
    state_status = (state_payload or {}).get("status")

    criteria = [
        _criterion(
            name="runtime_duration_hours",
            passed=runtime_duration_hours >= min_runtime_hours,
            observed=round(runtime_duration_hours, 6),
            threshold={"minimum": min_runtime_hours},
            description="Runtime evidence must cover at least the required duration.",
        ),
        _criterion(
            name="profitability_metrics_present",
            passed=(metrics_present or not require_profitability_metrics),
            observed={
                "latest_expected_value_after_execution_cost": (
                    latest_expected_value_after_execution_cost
                ),
                "latest_expected_net_edge_value_on_fills": (
                    latest_expected_net_edge_value_on_fills
                ),
                "latest_net_pnl": latest_net_pnl,
            },
            threshold={"required": require_profitability_metrics},
            description="Latest cycle must expose profitability metrics.",
        ),
        _criterion(
            name="expected_value_after_execution_cost",
            passed=(
                latest_expected_value_after_execution_cost is not None
                and latest_expected_value_after_execution_cost
                >= minimum_expected_value_after_execution_cost
            ),
            observed=latest_expected_value_after_execution_cost,
            threshold={
                "minimum": minimum_expected_value_after_execution_cost,
            },
            description=(
                "Latest expected value after execution cost must meet profitability "
                "threshold."
            ),
        ),
        _criterion(
            name="expected_net_edge_value_on_fills",
            passed=(
                latest_expected_net_edge_value_on_fills is not None
                and latest_expected_net_edge_value_on_fills
                >= minimum_expected_net_edge_value_on_fills
            ),
            observed=latest_expected_net_edge_value_on_fills,
            threshold={
                "minimum": minimum_expected_net_edge_value_on_fills,
            },
            description=(
                "Latest expected net edge value on fills must be non-negative (or "
                "configured minimum)."
            ),
        ),
        _criterion(
            name="mean_expected_value_after_execution_cost",
            passed=(
                minimum_mean_expected_value_after_execution_cost <= 0.0
                or (
                    mean_expected_value_after_execution_cost is not None
                    and mean_expected_value_after_execution_cost
                    >= minimum_mean_expected_value_after_execution_cost
                )
            ),
            observed=(
                round(mean_expected_value_after_execution_cost, 6)
                if mean_expected_value_after_execution_cost is not None
                else None
            ),
            threshold={
                "minimum": minimum_mean_expected_value_after_execution_cost,
            },
            description=(
                "Mean expected value after execution cost across all cycles must "
                "meet rolling-window profitability threshold (0.0 disables check)."
            ),
        ),
        _criterion(
            name="net_pnl_reported",
            passed=(
                latest_net_pnl is not None
                and (allow_negative_net_pnl or latest_net_pnl >= 0.0)
            ),
            observed=latest_net_pnl,
            threshold={
                "allow_negative": allow_negative_net_pnl,
                "minimum_if_not_allowed": 0.0,
            },
            description=(
                "Net PnL must be present; sign is optional unless explicitly "
                "disallowed by gate config."
            ),
        ),
    ]

    incidents = [
        {
            "code": f"criterion_failed:{criterion['name']}",
            "severity": "error",
            "summary": criterion["description"],
            "observed": criterion["observed"],
            "threshold": criterion["threshold"],
        }
        for criterion in criteria
        if not criterion["passed"]
    ]
    overall_status = "PASS" if not incidents else "FAIL"

    report = {
        "schema_version": "trl4_profitability_report.v1",
        "generated_at": _utc_now_iso(),
        "overall_status": overall_status,
        "gate_config_path": str(args.gate_config),
        "inputs": {
            "journal_path": str(args.journal_path),
            "state_path": str(args.state_path),
        },
        "runtime": {
            "cycle_count": len(cycle_rows),
            "first_cycle_index": (
                cycle_rows[0]["cycle_index"] if cycle_rows else None
            ),
            "last_cycle_index": (
                cycle_rows[-1]["cycle_index"] if cycle_rows else None
            ),
            "runtime_start": runtime_start.isoformat() if runtime_start else None,
            "runtime_end": runtime_end.isoformat() if runtime_end else None,
            "runtime_duration_hours_wall_clock": round(
                runtime_duration_hours_wall_clock, 6
            ),
            "runtime_duration_hours_cycle_based": round(
                runtime_duration_hours_cycle_based, 6
            ),
            "runtime_hours_per_cycle": round(runtime_hours_per_cycle, 6),
            "runtime_duration_hours": round(runtime_duration_hours, 6),
            "state_cycle_index": state_cycle_index,
            "state_status": state_status,
        },
        "profitability": {
            "latest_expected_value_after_execution_cost": (
                latest_expected_value_after_execution_cost
            ),
            "latest_expected_net_edge_value_on_fills": (
                latest_expected_net_edge_value_on_fills
            ),
            "latest_net_pnl": latest_net_pnl,
            "expected_value_after_execution_cost": _metric_summary(
                expected_value_after_execution_cost_values
            ),
            "expected_net_edge_value_on_fills": _metric_summary(
                expected_net_edge_value_on_fills_values
            ),
            "net_pnl": _metric_summary(net_pnl_values),
        },
        "criteria": criteria,
        "incidents": incidents,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    print(
        "TRL4 profitability report complete: "
        f"overall_status={overall_status} "
        f"cycle_count={report['runtime']['cycle_count']} "
        f"runtime_duration_hours={report['runtime']['runtime_duration_hours']} "
        f"output={args.output}"
    )
    return 0 if overall_status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
