from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .reproducibility import stable_hash
from .schemas import (
    CANARY_ROLLBACK_GUARD_AUDIT_EVENT_SCHEMA_VERSION,
    CANARY_ROLLBACK_GUARD_REPORT_SCHEMA_VERSION,
    CANARY_ROLLBACK_INCIDENT_REPORT_SCHEMA_VERSION,
)


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


def _to_int(value: Any, *, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _to_float(value: Any, *, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _to_float_or_none(value: Any) -> float | None:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    return parsed


def _dedupe_preserve_order(values: list[str]) -> list[str]:
    deduped: list[str] = []
    seen: set[str] = set()
    for value in values:
        normalized = str(value).strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        deduped.append(normalized)
    return deduped


def _max_consecutive_true(values: list[bool]) -> int:
    max_run = 0
    current_run = 0
    for value in values:
        if value:
            current_run += 1
            if current_run > max_run:
                max_run = current_run
        else:
            current_run = 0
    return max_run


def default_canary_rollback_policy() -> dict[str, Any]:
    return {
        "thresholds": {
            "max_execution_cost_to_expected_net_ratio": 1.0,
            "execution_cost_ratio_consecutive_cycles": 3,
            "minimum_expected_value_after_execution_cost": 0.0,
            "negative_expected_value_consecutive_cycles": 3,
            "negative_realized_pnl_consecutive_cycles": 3,
            "open_notional_without_confirmed_exits_consecutive_cycles": 3,
            "minimum_confirmed_exit_ratio": 0.5,
            "confirmed_exit_ratio_breach_consecutive_cycles": 3,
            "max_stale_position_ratio": 0.35,
            "stale_position_ratio_breach_consecutive_cycles": 3,
        },
        "default_rollback_authority": [
            "runtime_operator_on_call",
            "incident_commander",
        ],
        "rollback_triggers": [
            {
                "trigger": "enablement_decision_denied",
                "condition": (
                    "Canary stage enablement decision is DENY, so canary promotion "
                    "must be blocked."
                ),
                "severity": "blocker",
                "required_actions": [
                    "stop_canary_rollout_progression",
                    "retain_canary_stage_disabled",
                    "resolve_enablement_failed_reason_codes",
                ],
            },
            {
                "trigger": "certification_not_pass",
                "condition": (
                    "Canary readiness certification overall_status is not PASS."
                ),
                "severity": "blocker",
                "required_actions": [
                    "block_canary_live_orders",
                    "rerun_canary_readiness_certification",
                    "route_findings_to_release_manager",
                ],
            },
            {
                "trigger": "certification_blockers_present",
                "condition": "Canary readiness certification blockers list is non-empty.",
                "severity": "critical",
                "required_actions": [
                    "open_incident_bridge",
                    "resolve_certification_blockers",
                    "rerun_canary_readiness_certification",
                ],
            },
            {
                "trigger": "rehearsal_rollback_recommendations_present",
                "condition": (
                    "Rollout rehearsal report contains rollback recommendations that "
                    "remain unresolved."
                ),
                "severity": "critical",
                "required_actions": [
                    "switch_to_paper_mode",
                    "execute_rollback_rehearsal",
                    "clear_rehearsal_recommendations",
                ],
            },
            {
                "trigger": "order_lifecycle_failed_present",
                "condition": (
                    "Live cycle telemetry includes at least one execution_result "
                    "status=FAILED."
                ),
                "severity": "critical",
                "required_actions": [
                    "disable_new_orders",
                    "cancel_all_open_orders",
                    "collect_failed_order_lifecycle_artifacts",
                ],
            },
            {
                "trigger": "execution_cost_ratio_breach_consecutive",
                "condition": (
                    "execution_cost_to_expected_net_ratio exceeds threshold for "
                    "configured consecutive cycles."
                ),
                "severity": "high",
                "required_actions": [
                    "reduce_order_notional_limits",
                    "switch_to_paper_mode",
                    "investigate_execution_cost_regression",
                ],
            },
            {
                "trigger": "negative_expected_value_after_cost_consecutive",
                "condition": (
                    "expected_value_after_execution_cost remains below threshold for "
                    "configured consecutive cycles."
                ),
                "severity": "high",
                "required_actions": [
                    "disable_new_orders",
                    "switch_to_paper_mode",
                    "review_strategy_signal_quality",
                ],
            },
            {
                "trigger": "negative_realized_pnl_consecutive",
                "condition": (
                    "Realized net_pnl remains negative for configured consecutive "
                    "cycles."
                ),
                "severity": "high",
                "required_actions": [
                    "disable_new_orders",
                    "switch_to_paper_mode",
                    "review_realized_pnl_deterioration",
                ],
            },
            {
                "trigger": "open_notional_without_confirmed_exits_consecutive",
                "condition": (
                    "Open notional remains above zero while confirmed exits stay at "
                    "zero for configured consecutive cycles."
                ),
                "severity": "high",
                "required_actions": [
                    "suppress_new_entries",
                    "reduce_open_inventory",
                    "review_exit_path_health",
                ],
            },
            {
                "trigger": "confirmed_exit_ratio_breach_consecutive",
                "condition": (
                    "confirmed_exit_ratio remains below threshold for configured "
                    "consecutive cycles."
                ),
                "severity": "high",
                "required_actions": [
                    "suppress_new_entries",
                    "reduce_open_inventory",
                    "review_exit_conversion_health",
                ],
            },
            {
                "trigger": "stale_position_ratio_breach_consecutive",
                "condition": (
                    "stale_position_ratio exceeds threshold for configured "
                    "consecutive cycles."
                ),
                "severity": "high",
                "required_actions": [
                    "suppress_new_entries",
                    "reduce_open_inventory",
                    "review_position_aging_regression",
                ],
            },
            {
                "trigger": "no_cycle_telemetry_available",
                "condition": (
                    "No cycle telemetry artifacts are available for rollback "
                    "enforcement evaluation."
                ),
                "severity": "high",
                "required_actions": [
                    "block_rollout_progression",
                    "restore_cycle_artifact_pipeline",
                    "rerun_canary_rollback_guard",
                ],
            },
        ],
        "incident_handoff": {
            "responsible_authority": "runtime_operator_on_call",
            "secondary_authorities": [
                "incident_commander",
                "release_manager",
            ],
            "handoff_sequence": [
                "runtime_operator_on_call acknowledges rollback trigger evidence",
                "incident_commander confirms emergency action execution",
                "release_manager records release hold and remediation checkpoint",
            ],
        },
    }


def _resolve_policy(policy: dict[str, Any] | None) -> dict[str, Any]:
    resolved = default_canary_rollback_policy()
    if not policy:
        return resolved
    resolved.update(policy)

    default_thresholds = dict(
        default_canary_rollback_policy().get("thresholds", {})
    )
    custom_thresholds = _as_dict(policy.get("thresholds"))
    default_thresholds.update(custom_thresholds)
    resolved["thresholds"] = default_thresholds

    default_handoff = dict(
        default_canary_rollback_policy().get("incident_handoff", {})
    )
    custom_handoff = _as_dict(policy.get("incident_handoff"))
    default_handoff.update(custom_handoff)
    resolved["incident_handoff"] = default_handoff

    custom_triggers = _as_list(policy.get("rollback_triggers"))
    if custom_triggers:
        resolved["rollback_triggers"] = custom_triggers
    return resolved


def _trigger_definition_map(policy: dict[str, Any]) -> dict[str, dict[str, Any]]:
    definitions: dict[str, dict[str, Any]] = {}
    for item in _as_list(policy.get("rollback_triggers")):
        if not isinstance(item, dict):
            continue
        trigger_name = str(item.get("trigger", "")).strip()
        if not trigger_name:
            continue
        definitions[trigger_name] = item
    return definitions


def _evaluate_trigger(
    *,
    trigger_name: str,
    triggered: bool,
    reason_code: str,
    observed: Any,
    expected: Any,
    trigger_definition_map: dict[str, dict[str, Any]],
    default_rollback_authority: list[str],
) -> dict[str, Any]:
    definition = _as_dict(trigger_definition_map.get(trigger_name))
    rollback_authority = _dedupe_preserve_order(
        [str(value) for value in _as_list(definition.get("rollback_authority"))]
        or default_rollback_authority
    )
    return {
        "id": trigger_name,
        "triggered": bool(triggered),
        "severity": str(definition.get("severity", "unknown")).strip() or "unknown",
        "condition": str(definition.get("condition", "")).strip(),
        "reason_code": reason_code,
        "observed": observed,
        "expected": expected,
        "required_actions": _dedupe_preserve_order(
            [str(value) for value in _as_list(definition.get("required_actions"))]
        ),
        "rollback_authority": rollback_authority,
    }


def _extract_cycle_telemetry(cycle_reports: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized_rows: list[dict[str, Any]] = []
    for fallback_index, cycle_report in enumerate(cycle_reports, start=1):
        if not isinstance(cycle_report, dict):
            continue
        run_context = _as_dict(cycle_report.get("run_context"))
        cycle_index = _to_int(
            run_context.get("cycle_index", cycle_report.get("cycle_index", fallback_index)),
            default=fallback_index,
        )
        records = _as_list(cycle_report.get("records"))
        failed_record_count = 0
        for record in records:
            if not isinstance(record, dict):
                continue
            execution_result = _as_dict(record.get("execution_result"))
            if str(execution_result.get("status", "")).strip() == "FAILED":
                failed_record_count += 1
        normalized_rows.append(
            {
                "cycle_index": cycle_index,
                "record_count": len(records),
                "failed_order_lifecycle_count": failed_record_count,
                "execution_cost_to_expected_net_ratio": _to_float_or_none(
                    cycle_report.get("execution_cost_to_expected_net_ratio")
                ),
                "expected_value_after_execution_cost": _to_float_or_none(
                    cycle_report.get("expected_value_after_execution_cost")
                ),
                "net_pnl": _to_float_or_none(cycle_report.get("net_pnl")),
                "open_notional": _to_float_or_none(cycle_report.get("open_notional")),
                "confirmed_exit_count": _to_int(
                    cycle_report.get("confirmed_exit_count", 0),
                    default=0,
                ),
                "confirmed_exit_ratio": _to_float_or_none(
                    cycle_report.get("confirmed_exit_ratio")
                ),
                "stale_position_ratio": _to_float_or_none(
                    cycle_report.get("stale_position_ratio")
                ),
            }
        )
    return sorted(normalized_rows, key=lambda row: _to_int(row.get("cycle_index", 0)))


def _build_incident_handoff(
    *,
    triggered_conditions: list[dict[str, Any]],
    policy: dict[str, Any],
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    handoff_policy = _as_dict(policy.get("incident_handoff"))
    default_rollback_authority = _dedupe_preserve_order(
        [str(value) for value in _as_list(policy.get("default_rollback_authority"))]
    )
    trigger_required_actions: list[str] = []
    trigger_rollback_authorities: list[str] = []
    for condition in triggered_conditions:
        trigger_required_actions.extend(
            [str(value) for value in _as_list(condition.get("required_actions"))]
        )
        trigger_rollback_authorities.extend(
            [str(value) for value in _as_list(condition.get("rollback_authority"))]
        )
    required_emergency_actions = _dedupe_preserve_order(trigger_required_actions)
    rollback_authority = (
        _dedupe_preserve_order(trigger_rollback_authorities) or default_rollback_authority
    )
    responsible_authority = str(
        handoff_policy.get("responsible_authority", rollback_authority[0] if rollback_authority else "")
    ).strip()
    secondary_authorities = _dedupe_preserve_order(
        [str(value) for value in _as_list(handoff_policy.get("secondary_authorities"))]
    )
    handoff_sequence = _dedupe_preserve_order(
        [str(value) for value in _as_list(handoff_policy.get("handoff_sequence"))]
    )
    incident_status = "OPEN" if triggered_conditions else "NONE"
    incident_payload = {
        "schema_version": CANARY_ROLLBACK_INCIDENT_REPORT_SCHEMA_VERSION,
        "generated_at": _utc_now_iso(),
        "incident_status": incident_status,
        "incident_id": None,
        "summary": (
            "No rollback triggers fired."
            if not triggered_conditions
            else (
                f"{len(triggered_conditions)} rollback condition(s) triggered; "
                "execute emergency actions and hold rollout progression."
            )
        ),
        "trigger_evidence": triggered_conditions,
        "required_emergency_actions": required_emergency_actions,
        "rollback_authority": rollback_authority,
        "responsible_authority": responsible_authority,
        "secondary_authorities": secondary_authorities,
        "handoff_sequence": handoff_sequence,
        "metadata": metadata or {},
    }
    if incident_status == "OPEN":
        incident_seed = {
            "trigger_evidence": triggered_conditions,
            "required_emergency_actions": required_emergency_actions,
            "rollback_authority": rollback_authority,
            "responsible_authority": responsible_authority,
            "metadata": metadata or {},
        }
        incident_payload["incident_id"] = f"canary-rollback-{stable_hash(incident_seed)[:12]}"
    return incident_payload


def build_canary_rollback_guard_report(
    *,
    canary_enablement_decision: dict[str, Any],
    certification_report: dict[str, Any],
    rehearsal_report: dict[str, Any],
    cycle_reports: list[dict[str, Any]] | None = None,
    policy: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolved_policy = _resolve_policy(policy)
    trigger_definition_map = _trigger_definition_map(resolved_policy)
    thresholds = _as_dict(resolved_policy.get("thresholds"))
    default_rollback_authority = _dedupe_preserve_order(
        [str(value) for value in _as_list(resolved_policy.get("default_rollback_authority"))]
    )

    decision_status = str(
        canary_enablement_decision.get("decision_status", "UNKNOWN")
    ).strip()
    certification_status = str(
        certification_report.get("overall_status", "UNKNOWN")
    ).strip()
    certification_blockers = _as_list(certification_report.get("blockers"))
    rehearsal_rollback_recommendations = _as_list(
        rehearsal_report.get("rollback_recommendations")
    )
    normalized_cycle_telemetry = _extract_cycle_telemetry(cycle_reports or [])
    cycle_report_count = len(normalized_cycle_telemetry)

    ratio_threshold = _to_float(
        thresholds.get("max_execution_cost_to_expected_net_ratio", 1.0),
        default=1.0,
    )
    ratio_consecutive_required = max(
        1,
        _to_int(thresholds.get("execution_cost_ratio_consecutive_cycles", 3), default=3),
    )
    expected_value_minimum = _to_float(
        thresholds.get("minimum_expected_value_after_execution_cost", 0.0),
        default=0.0,
    )
    expected_value_consecutive_required = max(
        1,
        _to_int(thresholds.get("negative_expected_value_consecutive_cycles", 3), default=3),
    )
    negative_realized_pnl_consecutive_required = max(
        1,
        _to_int(
            thresholds.get("negative_realized_pnl_consecutive_cycles", 3),
            default=3,
        ),
    )
    open_notional_without_confirmed_exits_consecutive_required = max(
        1,
        _to_int(
            thresholds.get(
                "open_notional_without_confirmed_exits_consecutive_cycles",
                3,
            ),
            default=3,
        ),
    )
    minimum_confirmed_exit_ratio = _to_float(
        thresholds.get("minimum_confirmed_exit_ratio", 0.5),
        default=0.5,
    )
    confirmed_exit_ratio_breach_consecutive_required = max(
        1,
        _to_int(
            thresholds.get("confirmed_exit_ratio_breach_consecutive_cycles", 3),
            default=3,
        ),
    )
    max_stale_position_ratio = _to_float(
        thresholds.get("max_stale_position_ratio", 0.35),
        default=0.35,
    )
    stale_position_ratio_breach_consecutive_required = max(
        1,
        _to_int(
            thresholds.get("stale_position_ratio_breach_consecutive_cycles", 3),
            default=3,
        ),
    )

    failed_order_lifecycle_total = sum(
        _to_int(row.get("failed_order_lifecycle_count", 0))
        for row in normalized_cycle_telemetry
    )
    ratio_flags = [
        (row.get("execution_cost_to_expected_net_ratio") is not None)
        and (_to_float(row.get("execution_cost_to_expected_net_ratio"), default=0.0) > ratio_threshold)
        for row in normalized_cycle_telemetry
    ]
    negative_expected_value_flags = [
        (row.get("expected_value_after_execution_cost") is not None)
        and (
            _to_float(row.get("expected_value_after_execution_cost"), default=0.0)
            < expected_value_minimum
        )
        for row in normalized_cycle_telemetry
    ]
    max_ratio_consecutive = _max_consecutive_true(ratio_flags)
    max_negative_expected_value_consecutive = _max_consecutive_true(
        negative_expected_value_flags
    )
    negative_realized_pnl_flags = [
        (row.get("net_pnl") is not None)
        and (_to_float(row.get("net_pnl"), default=0.0) < 0.0)
        for row in normalized_cycle_telemetry
    ]
    max_negative_realized_pnl_consecutive = _max_consecutive_true(
        negative_realized_pnl_flags
    )
    open_notional_without_confirmed_exits_flags = [
        (row.get("open_notional") is not None)
        and (_to_float(row.get("open_notional"), default=0.0) > 0.0)
        and (_to_int(row.get("confirmed_exit_count", 0), default=0) <= 0)
        for row in normalized_cycle_telemetry
    ]
    max_open_notional_without_confirmed_exits_consecutive = _max_consecutive_true(
        open_notional_without_confirmed_exits_flags
    )
    confirmed_exit_ratio_flags = [
        (row.get("confirmed_exit_ratio") is not None)
        and (
            _to_float(row.get("confirmed_exit_ratio"), default=0.0)
            < minimum_confirmed_exit_ratio
        )
        for row in normalized_cycle_telemetry
    ]
    max_confirmed_exit_ratio_breach_consecutive = _max_consecutive_true(
        confirmed_exit_ratio_flags
    )
    stale_position_ratio_flags = [
        (row.get("stale_position_ratio") is not None)
        and (
            _to_float(row.get("stale_position_ratio"), default=0.0)
            > max_stale_position_ratio
        )
        for row in normalized_cycle_telemetry
    ]
    max_stale_position_ratio_breach_consecutive = _max_consecutive_true(
        stale_position_ratio_flags
    )
    ratio_breach_cycles = [
        _to_int(row.get("cycle_index", 0))
        for row, breached in zip(normalized_cycle_telemetry, ratio_flags, strict=False)
        if breached
    ]
    negative_expected_value_cycles = [
        _to_int(row.get("cycle_index", 0))
        for row, breached in zip(
            normalized_cycle_telemetry, negative_expected_value_flags, strict=False
        )
        if breached
    ]
    negative_realized_pnl_cycles = [
        _to_int(row.get("cycle_index", 0))
        for row, breached in zip(
            normalized_cycle_telemetry,
            negative_realized_pnl_flags,
            strict=False,
        )
        if breached
    ]
    open_notional_without_confirmed_exits_cycles = [
        _to_int(row.get("cycle_index", 0))
        for row, breached in zip(
            normalized_cycle_telemetry,
            open_notional_without_confirmed_exits_flags,
            strict=False,
        )
        if breached
    ]
    confirmed_exit_ratio_breach_cycles = [
        _to_int(row.get("cycle_index", 0))
        for row, breached in zip(
            normalized_cycle_telemetry,
            confirmed_exit_ratio_flags,
            strict=False,
        )
        if breached
    ]
    stale_position_ratio_breach_cycles = [
        _to_int(row.get("cycle_index", 0))
        for row, breached in zip(
            normalized_cycle_telemetry,
            stale_position_ratio_flags,
            strict=False,
        )
        if breached
    ]

    trigger_evaluations = [
        _evaluate_trigger(
            trigger_name="enablement_decision_denied",
            triggered=decision_status != "ALLOW",
            reason_code=("ok" if decision_status == "ALLOW" else "enablement_decision_denied"),
            observed={"decision_status": decision_status},
            expected={"decision_status": "ALLOW"},
            trigger_definition_map=trigger_definition_map,
            default_rollback_authority=default_rollback_authority,
        ),
        _evaluate_trigger(
            trigger_name="certification_not_pass",
            triggered=certification_status != "PASS",
            reason_code=("ok" if certification_status == "PASS" else "certification_not_pass"),
            observed={"overall_status": certification_status},
            expected={"overall_status": "PASS"},
            trigger_definition_map=trigger_definition_map,
            default_rollback_authority=default_rollback_authority,
        ),
        _evaluate_trigger(
            trigger_name="certification_blockers_present",
            triggered=bool(certification_blockers),
            reason_code=("ok" if not certification_blockers else "certification_blockers_present"),
            observed={"blocker_count": len(certification_blockers)},
            expected={"blocker_count": 0},
            trigger_definition_map=trigger_definition_map,
            default_rollback_authority=default_rollback_authority,
        ),
        _evaluate_trigger(
            trigger_name="rehearsal_rollback_recommendations_present",
            triggered=bool(rehearsal_rollback_recommendations),
            reason_code=(
                "ok"
                if not rehearsal_rollback_recommendations
                else "rehearsal_rollback_recommendations_present"
            ),
            observed={"rollback_recommendation_count": len(rehearsal_rollback_recommendations)},
            expected={"rollback_recommendation_count": 0},
            trigger_definition_map=trigger_definition_map,
            default_rollback_authority=default_rollback_authority,
        ),
        _evaluate_trigger(
            trigger_name="order_lifecycle_failed_present",
            triggered=failed_order_lifecycle_total > 0,
            reason_code=("ok" if failed_order_lifecycle_total == 0 else "order_lifecycle_failed_present"),
            observed={"failed_order_lifecycle_count": failed_order_lifecycle_total},
            expected={"failed_order_lifecycle_count": 0},
            trigger_definition_map=trigger_definition_map,
            default_rollback_authority=default_rollback_authority,
        ),
        _evaluate_trigger(
            trigger_name="execution_cost_ratio_breach_consecutive",
            triggered=max_ratio_consecutive >= ratio_consecutive_required,
            reason_code=(
                "ok"
                if max_ratio_consecutive < ratio_consecutive_required
                else "execution_cost_ratio_breach_consecutive"
            ),
            observed={
                "max_consecutive_breaches": max_ratio_consecutive,
                "breach_cycle_indices": ratio_breach_cycles,
            },
            expected={
                "max_consecutive_breaches": f"< {ratio_consecutive_required}",
                "threshold": ratio_threshold,
            },
            trigger_definition_map=trigger_definition_map,
            default_rollback_authority=default_rollback_authority,
        ),
        _evaluate_trigger(
            trigger_name="negative_expected_value_after_cost_consecutive",
            triggered=max_negative_expected_value_consecutive >= expected_value_consecutive_required,
            reason_code=(
                "ok"
                if max_negative_expected_value_consecutive < expected_value_consecutive_required
                else "negative_expected_value_after_cost_consecutive"
            ),
            observed={
                "max_consecutive_breaches": max_negative_expected_value_consecutive,
                "breach_cycle_indices": negative_expected_value_cycles,
            },
            expected={
                "max_consecutive_breaches": f"< {expected_value_consecutive_required}",
                "minimum_expected_value_after_execution_cost": expected_value_minimum,
            },
            trigger_definition_map=trigger_definition_map,
            default_rollback_authority=default_rollback_authority,
        ),
        _evaluate_trigger(
            trigger_name="negative_realized_pnl_consecutive",
            triggered=(
                max_negative_realized_pnl_consecutive
                >= negative_realized_pnl_consecutive_required
            ),
            reason_code=(
                "ok"
                if (
                    max_negative_realized_pnl_consecutive
                    < negative_realized_pnl_consecutive_required
                )
                else "negative_realized_pnl_consecutive"
            ),
            observed={
                "max_consecutive_breaches": max_negative_realized_pnl_consecutive,
                "breach_cycle_indices": negative_realized_pnl_cycles,
            },
            expected={
                "max_consecutive_breaches": (
                    f"< {negative_realized_pnl_consecutive_required}"
                ),
                "net_pnl_threshold": 0.0,
            },
            trigger_definition_map=trigger_definition_map,
            default_rollback_authority=default_rollback_authority,
        ),
        _evaluate_trigger(
            trigger_name="open_notional_without_confirmed_exits_consecutive",
            triggered=(
                max_open_notional_without_confirmed_exits_consecutive
                >= open_notional_without_confirmed_exits_consecutive_required
            ),
            reason_code=(
                "ok"
                if (
                    max_open_notional_without_confirmed_exits_consecutive
                    < open_notional_without_confirmed_exits_consecutive_required
                )
                else "open_notional_without_confirmed_exits_consecutive"
            ),
            observed={
                "max_consecutive_breaches": (
                    max_open_notional_without_confirmed_exits_consecutive
                ),
                "breach_cycle_indices": open_notional_without_confirmed_exits_cycles,
            },
            expected={
                "max_consecutive_breaches": (
                    f"< {open_notional_without_confirmed_exits_consecutive_required}"
                ),
                "open_notional": "> 0",
                "confirmed_exit_count": "== 0",
            },
            trigger_definition_map=trigger_definition_map,
            default_rollback_authority=default_rollback_authority,
        ),
        _evaluate_trigger(
            trigger_name="confirmed_exit_ratio_breach_consecutive",
            triggered=(
                max_confirmed_exit_ratio_breach_consecutive
                >= confirmed_exit_ratio_breach_consecutive_required
            ),
            reason_code=(
                "ok"
                if (
                    max_confirmed_exit_ratio_breach_consecutive
                    < confirmed_exit_ratio_breach_consecutive_required
                )
                else "confirmed_exit_ratio_breach_consecutive"
            ),
            observed={
                "max_consecutive_breaches": (
                    max_confirmed_exit_ratio_breach_consecutive
                ),
                "breach_cycle_indices": confirmed_exit_ratio_breach_cycles,
            },
            expected={
                "max_consecutive_breaches": (
                    f"< {confirmed_exit_ratio_breach_consecutive_required}"
                ),
                "minimum_confirmed_exit_ratio": minimum_confirmed_exit_ratio,
            },
            trigger_definition_map=trigger_definition_map,
            default_rollback_authority=default_rollback_authority,
        ),
        _evaluate_trigger(
            trigger_name="stale_position_ratio_breach_consecutive",
            triggered=(
                max_stale_position_ratio_breach_consecutive
                >= stale_position_ratio_breach_consecutive_required
            ),
            reason_code=(
                "ok"
                if (
                    max_stale_position_ratio_breach_consecutive
                    < stale_position_ratio_breach_consecutive_required
                )
                else "stale_position_ratio_breach_consecutive"
            ),
            observed={
                "max_consecutive_breaches": (
                    max_stale_position_ratio_breach_consecutive
                ),
                "breach_cycle_indices": stale_position_ratio_breach_cycles,
            },
            expected={
                "max_consecutive_breaches": (
                    f"< {stale_position_ratio_breach_consecutive_required}"
                ),
                "max_stale_position_ratio": max_stale_position_ratio,
            },
            trigger_definition_map=trigger_definition_map,
            default_rollback_authority=default_rollback_authority,
        ),
        _evaluate_trigger(
            trigger_name="no_cycle_telemetry_available",
            triggered=cycle_report_count == 0,
            reason_code=("ok" if cycle_report_count > 0 else "no_cycle_telemetry_available"),
            observed={"cycle_report_count": cycle_report_count},
            expected={"cycle_report_count": "> 0"},
            trigger_definition_map=trigger_definition_map,
            default_rollback_authority=default_rollback_authority,
        ),
    ]

    triggered_conditions = [
        evaluation for evaluation in trigger_evaluations if bool(evaluation.get("triggered"))
    ]
    incident_handoff = _build_incident_handoff(
        triggered_conditions=triggered_conditions,
        policy=resolved_policy,
        metadata={"guard_metadata": metadata or {}},
    )
    guard_status = "PASS" if not triggered_conditions else "FAIL"

    enablement_decision_hash = str(
        _as_dict(canary_enablement_decision.get("evidence")).get("decision_hash", "")
    ).strip() or stable_hash(canary_enablement_decision)
    certification_hash = str(
        _as_dict(certification_report.get("evidence")).get("certification_hash", "")
    ).strip() or stable_hash(certification_report)
    rehearsal_report_hash = stable_hash(rehearsal_report)
    cycle_reports_hash = stable_hash(normalized_cycle_telemetry)

    guard_hash_seed = {
        "guard_status": guard_status,
        "triggered_conditions": triggered_conditions,
        "thresholds": thresholds,
        "enablement_decision_hash": enablement_decision_hash,
        "certification_hash": certification_hash,
        "rehearsal_report_hash": rehearsal_report_hash,
        "cycle_reports_hash": cycle_reports_hash,
        "metadata": metadata or {},
    }
    guard_hash = stable_hash(guard_hash_seed)
    incident_hash = stable_hash(
        {
            "incident_handoff": incident_handoff,
            "guard_hash": guard_hash,
        }
    )
    incident_handoff["evidence"] = {
        "guard_hash": guard_hash,
        "incident_hash": incident_hash,
    }

    return {
        "schema_version": CANARY_ROLLBACK_GUARD_REPORT_SCHEMA_VERSION,
        "generated_at": _utc_now_iso(),
        "guard_status": guard_status,
        "trigger_evaluations": trigger_evaluations,
        "triggered_condition_count": len(triggered_conditions),
        "triggered_conditions": triggered_conditions,
        "thresholds": {
            "max_execution_cost_to_expected_net_ratio": ratio_threshold,
            "execution_cost_ratio_consecutive_cycles": ratio_consecutive_required,
            "minimum_expected_value_after_execution_cost": expected_value_minimum,
            "negative_expected_value_consecutive_cycles": expected_value_consecutive_required,
            "negative_realized_pnl_consecutive_cycles": (
                negative_realized_pnl_consecutive_required
            ),
            "open_notional_without_confirmed_exits_consecutive_cycles": (
                open_notional_without_confirmed_exits_consecutive_required
            ),
            "minimum_confirmed_exit_ratio": minimum_confirmed_exit_ratio,
            "confirmed_exit_ratio_breach_consecutive_cycles": (
                confirmed_exit_ratio_breach_consecutive_required
            ),
            "max_stale_position_ratio": max_stale_position_ratio,
            "stale_position_ratio_breach_consecutive_cycles": (
                stale_position_ratio_breach_consecutive_required
            ),
        },
        "telemetry_summary": {
            "cycle_report_count": cycle_report_count,
            "failed_order_lifecycle_count": failed_order_lifecycle_total,
            "max_execution_cost_ratio_consecutive_breaches": max_ratio_consecutive,
            "max_negative_expected_value_consecutive_breaches": (
                max_negative_expected_value_consecutive
            ),
            "max_negative_realized_pnl_consecutive_breaches": (
                max_negative_realized_pnl_consecutive
            ),
            "max_open_notional_without_confirmed_exits_consecutive_breaches": (
                max_open_notional_without_confirmed_exits_consecutive
            ),
            "max_confirmed_exit_ratio_breach_consecutive_breaches": (
                max_confirmed_exit_ratio_breach_consecutive
            ),
            "max_stale_position_ratio_breach_consecutive_breaches": (
                max_stale_position_ratio_breach_consecutive
            ),
        },
        "incident_required": bool(triggered_conditions),
        "incident_handoff": incident_handoff,
        "metadata": metadata or {},
        "evidence": {
            "enablement_decision_hash": enablement_decision_hash,
            "certification_hash": certification_hash,
            "rehearsal_report_hash": rehearsal_report_hash,
            "cycle_reports_hash": cycle_reports_hash,
            "guard_hash": guard_hash,
            "incident_hash": incident_hash,
        },
    }


def append_canary_rollback_guard_audit_event(
    *,
    audit_path: Path,
    guard_report: dict[str, Any],
    actor: str,
    reason: str | None = None,
) -> dict[str, Any]:
    incident_handoff = _as_dict(guard_report.get("incident_handoff"))
    evidence = _as_dict(guard_report.get("evidence"))
    incident_evidence = _as_dict(incident_handoff.get("evidence"))
    event = {
        "schema_version": CANARY_ROLLBACK_GUARD_AUDIT_EVENT_SCHEMA_VERSION,
        "recorded_at": _utc_now_iso(),
        "actor": str(actor).strip(),
        "reason": reason,
        "guard_status": str(guard_report.get("guard_status", "UNKNOWN")).strip(),
        "triggered_condition_count": _to_int(
            guard_report.get("triggered_condition_count", 0)
        ),
        "incident_status": str(
            incident_handoff.get("incident_status", "UNKNOWN")
        ).strip(),
        "incident_id": str(incident_handoff.get("incident_id", "")).strip() or None,
        "guard_hash": str(evidence.get("guard_hash", "")).strip(),
        "incident_hash": str(incident_evidence.get("incident_hash", "")).strip(),
    }
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    with audit_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")
    return event
