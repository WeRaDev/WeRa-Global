from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from .reproducibility import stable_hash
from .schemas import STRESS_CERTIFICATION_REPORT_SCHEMA_VERSION


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="milliseconds")


def default_certification_thresholds() -> dict[str, Any]:
    return {
        "minimum_scenario_count": 3,
        "minimum_total_allowed_trades": 1,
        "maximum_zero_trade_scenarios": 3,
        "maximum_open_notional": 300.0,
        "require_soak_summary": True,
        "require_soak_overall_success": True,
        "maximum_failed_intervals": 0,
        "maximum_drill_unexpected_success": 0,
        "maximum_recovery_failures": 0,
    }


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


def build_stress_certification_report(
    *,
    matrix_report: dict[str, Any],
    soak_summary: dict[str, Any] | None = None,
    thresholds: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    threshold_values = {**default_certification_thresholds(), **(thresholds or {})}
    aggregate = matrix_report.get("aggregate") or {}

    scenario_count = int(aggregate.get("scenario_count", 0))
    total_allowed_trades = int(aggregate.get("total_allowed_trades", 0))
    zero_trade_scenarios = list(aggregate.get("zero_trade_scenarios", []))
    zero_trade_count = len(zero_trade_scenarios)
    max_open_notional = float(aggregate.get("max_open_notional", 0.0))

    criteria: list[dict[str, Any]] = [
        _criterion(
            name="scenario_count",
            passed=scenario_count >= int(threshold_values["minimum_scenario_count"]),
            observed=scenario_count,
            threshold={"minimum": int(threshold_values["minimum_scenario_count"])},
            description="Stress campaign must include enough scenarios to be meaningful.",
        ),
        _criterion(
            name="total_allowed_trades",
            passed=total_allowed_trades >= int(threshold_values["minimum_total_allowed_trades"]),
            observed=total_allowed_trades,
            threshold={"minimum": int(threshold_values["minimum_total_allowed_trades"])},
            description="Campaign must exercise at least one allowed-trade path.",
        ),
        _criterion(
            name="zero_trade_scenarios",
            passed=zero_trade_count <= int(threshold_values["maximum_zero_trade_scenarios"]),
            observed={"count": zero_trade_count, "scenarios": zero_trade_scenarios},
            threshold={"maximum": int(threshold_values["maximum_zero_trade_scenarios"])},
            description="Too many zero-trade scenarios indicate over-conservative or broken behavior.",
        ),
        _criterion(
            name="max_open_notional",
            passed=max_open_notional <= float(threshold_values["maximum_open_notional"]),
            observed=max_open_notional,
            threshold={"maximum": float(threshold_values["maximum_open_notional"])},
            description="Open notional must stay within configured stress envelope.",
        ),
    ]

    require_soak_summary = bool(threshold_values.get("require_soak_summary", True))
    has_soak_summary = soak_summary is not None
    criteria.append(
        _criterion(
            name="soak_summary_present",
            passed=(has_soak_summary or not require_soak_summary),
            observed=has_soak_summary,
            threshold={"required": require_soak_summary},
            description="Certification requires soak evidence when enabled.",
        )
    )

    soak_metrics: dict[str, Any] = {
        "overall_status": None,
        "failed_intervals": None,
        "drill_unexpected_success": None,
        "recovery_failure_count": None,
    }

    if has_soak_summary:
        soak_overall_status = str(soak_summary.get("overall_status", "UNKNOWN"))
        interval_counts = soak_summary.get("interval_status_counts") or {}
        failed_intervals = int(interval_counts.get("failed", 0))
        drill_unexpected_success = int(interval_counts.get("drill_unexpected_success", 0))
        recovery_checks = list(soak_summary.get("recovery_checks", []))
        recovery_failure_count = sum(
            1 for check in recovery_checks if not bool(check.get("recovered_after_interval", False))
        )
        soak_metrics = {
            "overall_status": soak_overall_status,
            "failed_intervals": failed_intervals,
            "drill_unexpected_success": drill_unexpected_success,
            "recovery_failure_count": recovery_failure_count,
        }
        if bool(threshold_values.get("require_soak_overall_success", True)):
            criteria.append(
                _criterion(
                    name="soak_overall_status",
                    passed=soak_overall_status == "SUCCESS",
                    observed=soak_overall_status,
                    threshold={"expected": "SUCCESS"},
                    description="Soak run must conclude with SUCCESS status.",
                )
            )
        criteria.extend(
            [
                _criterion(
                    name="soak_failed_intervals",
                    passed=failed_intervals <= int(threshold_values["maximum_failed_intervals"]),
                    observed=failed_intervals,
                    threshold={"maximum": int(threshold_values["maximum_failed_intervals"])},
                    description="Unexpected failed intervals must remain within threshold.",
                ),
                _criterion(
                    name="soak_drill_unexpected_success",
                    passed=drill_unexpected_success
                    <= int(threshold_values["maximum_drill_unexpected_success"]),
                    observed=drill_unexpected_success,
                    threshold={"maximum": int(threshold_values["maximum_drill_unexpected_success"])},
                    description="Expected-failure drills must not silently succeed unexpectedly.",
                ),
                _criterion(
                    name="soak_recovery_failures",
                    passed=recovery_failure_count
                    <= int(threshold_values["maximum_recovery_failures"]),
                    observed=recovery_failure_count,
                    threshold={"maximum": int(threshold_values["maximum_recovery_failures"])},
                    description="All drill intervals should demonstrate deterministic recovery.",
                ),
            ]
        )

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
    certification_hash = stable_hash(
        {
            "matrix_report_hash": matrix_report.get("report_hash"),
            "soak_summary_schema": soak_summary.get("schema_version") if soak_summary else None,
            "thresholds": threshold_values,
            "criteria": criteria,
            "incidents": incidents,
            "overall_status": overall_status,
            "metadata": metadata or {},
        }
    )

    return {
        "schema_version": STRESS_CERTIFICATION_REPORT_SCHEMA_VERSION,
        "generated_at": _utc_now_iso(),
        "overall_status": overall_status,
        "thresholds": threshold_values,
        "metrics": {
            "scenario_matrix": {
                "scenario_count": scenario_count,
                "total_allowed_trades": total_allowed_trades,
                "zero_trade_scenarios": zero_trade_scenarios,
                "max_open_notional": max_open_notional,
            },
            "soak": soak_metrics,
        },
        "criteria": criteria,
        "incidents": incidents,
        "evidence": {
            "matrix_report_hash": matrix_report.get("report_hash"),
            "soak_summary_schema_version": soak_summary.get("schema_version")
            if soak_summary
            else None,
            "certification_hash": certification_hash,
        },
        "metadata": metadata or {},
    }
