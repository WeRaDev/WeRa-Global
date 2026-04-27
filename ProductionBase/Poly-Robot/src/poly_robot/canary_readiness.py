from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from .reproducibility import stable_hash
from .schemas import CANARY_ROLLOUT_CERTIFICATION_REPORT_SCHEMA_VERSION


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="milliseconds")


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


def _non_negative_float_or_none(value: Any) -> float | None:
    parsed = _to_float(value, default=float("nan"))
    if parsed != parsed:  # NaN check
        return None
    if parsed < 0:
        return None
    return parsed


def _default_criteria_weights() -> dict[str, float]:
    return {
        "rehearsal_overall_success": 25.0,
        "no_blocking_metadata_failures": 15.0,
        "no_failed_command_bundles": 10.0,
        "no_blocking_rollback_recommendations": 20.0,
        "required_control_scenarios_passed": 30.0,
    }


def default_canary_readiness_policy() -> dict[str, Any]:
    return {
        "minimum_readiness_score": 90.0,
        "blocking_rollback_severities": ["blocker", "critical", "high"],
        "required_control_scenarios": [
            "kill_switch_gate",
            "cancel_all_gate",
            "restart_acknowledgement_gate",
        ],
        "criteria_weights": _default_criteria_weights(),
        "blocking_criteria_ids": [
            "rehearsal_overall_success",
            "no_blocking_metadata_failures",
            "no_failed_command_bundles",
            "no_blocking_rollback_recommendations",
            "required_control_scenarios_passed",
            "readiness_score_threshold_met",
        ],
        "manual_approval_policy": {
            "manual_approval_required": True,
            "promotion_owner": "release_manager",
            "required_approvers": [
                "release_manager",
                "runtime_operator_on_call",
            ],
            "rollback_authority": [
                "runtime_operator_on_call",
                "incident_commander",
            ],
        },
    }


def _resolve_policy(policy: dict[str, Any] | None) -> dict[str, Any]:
    resolved = default_canary_readiness_policy()
    if not policy:
        return resolved
    resolved.update(policy)

    default_weights = _default_criteria_weights()
    custom_weights = policy.get("criteria_weights")
    weights = dict(default_weights)
    if isinstance(custom_weights, dict):
        for key, value in custom_weights.items():
            parsed = _non_negative_float_or_none(value)
            if parsed is not None:
                weights[str(key)] = parsed
    resolved["criteria_weights"] = weights

    manual_policy = dict(
        default_canary_readiness_policy().get("manual_approval_policy", {})
    )
    custom_manual_policy = policy.get("manual_approval_policy")
    if isinstance(custom_manual_policy, dict):
        manual_policy.update(custom_manual_policy)
    resolved["manual_approval_policy"] = manual_policy
    return resolved


def _scenario_status_map(rehearsal_report: dict[str, Any]) -> dict[str, str]:
    status_by_scenario: dict[str, str] = {}
    scenario_results = rehearsal_report.get("scenario_results")
    if not isinstance(scenario_results, list):
        return status_by_scenario
    for scenario_result in scenario_results:
        if not isinstance(scenario_result, dict):
            continue
        scenario_id = str(scenario_result.get("id", "")).strip()
        if not scenario_id:
            continue
        status_by_scenario[scenario_id] = str(
            scenario_result.get("status", "UNKNOWN")
        ).strip()
    return status_by_scenario


def _criterion(
    *,
    criterion_id: str,
    description: str,
    passed: bool,
    reason_code: str,
    observed: Any,
    expected: Any,
    weight: float,
    blocking: bool,
) -> dict[str, Any]:
    return {
        "id": criterion_id,
        "description": description,
        "passed": bool(passed),
        "reason_code": reason_code,
        "observed": observed,
        "expected": expected,
        "weight": weight,
        "blocking": bool(blocking),
    }


def build_canary_readiness_report(
    *,
    rehearsal_report: dict[str, Any],
    policy: dict[str, Any] | None = None,
    approval_status: str = "pending",
    approval_actor: str | None = None,
    approval_note: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolved_policy = _resolve_policy(policy)
    weights = dict(resolved_policy.get("criteria_weights", {}))
    minimum_readiness_score = _to_float(
        resolved_policy.get("minimum_readiness_score", 90.0),
        default=90.0,
    )
    blocking_criteria_ids = {
        str(value)
        for value in resolved_policy.get("blocking_criteria_ids", [])
        if str(value).strip()
    }
    required_control_scenarios = [
        str(value).strip()
        for value in resolved_policy.get("required_control_scenarios", [])
        if str(value).strip()
    ]
    blocking_rollback_severities = {
        str(value).strip().lower()
        for value in resolved_policy.get("blocking_rollback_severities", [])
        if str(value).strip()
    }

    summary = rehearsal_report.get("summary")
    if not isinstance(summary, dict):
        summary = {}
    blocking_metadata = rehearsal_report.get("blocking_metadata")
    if not isinstance(blocking_metadata, dict):
        blocking_metadata = {}
    rollback_recommendations = rehearsal_report.get("rollback_recommendations")
    if not isinstance(rollback_recommendations, list):
        rollback_recommendations = []
    scenario_statuses = _scenario_status_map(rehearsal_report)

    rehearsal_overall_status = str(
        summary.get("overall_status", "UNKNOWN")
    ).strip().upper()
    failed_command_bundles = _to_int(summary.get("failed_command_bundles", 0))
    failed_bundle_commands = _to_int(summary.get("failed_bundle_commands", 0))
    has_blocking_metadata_failures = bool(
        blocking_metadata.get("has_blocking_failures", False)
    )

    blocking_rollbacks: list[dict[str, Any]] = []
    for recommendation in rollback_recommendations:
        if not isinstance(recommendation, dict):
            continue
        severity = str(recommendation.get("severity", "")).strip().lower()
        if severity in blocking_rollback_severities:
            blocking_rollbacks.append(recommendation)

    control_failures: list[str] = []
    for scenario_id in required_control_scenarios:
        if scenario_statuses.get(scenario_id) != "PASS":
            control_failures.append(scenario_id)

    criteria: list[dict[str, Any]] = [
        _criterion(
            criterion_id="rehearsal_overall_success",
            description="Rollout rehearsal summary.overall_status must be SUCCESS.",
            passed=rehearsal_overall_status == "SUCCESS",
            reason_code=(
                "ok"
                if rehearsal_overall_status == "SUCCESS"
                else "rehearsal_overall_status_not_success"
            ),
            observed=rehearsal_overall_status,
            expected="SUCCESS",
            weight=_to_float(weights.get("rehearsal_overall_success", 0.0)),
            blocking="rehearsal_overall_success" in blocking_criteria_ids,
        ),
        _criterion(
            criterion_id="no_blocking_metadata_failures",
            description=(
                "Rollout rehearsal blocking metadata must report no unresolved blockers."
            ),
            passed=not has_blocking_metadata_failures,
            reason_code=(
                "ok"
                if not has_blocking_metadata_failures
                else "blocking_metadata_has_failures"
            ),
            observed={
                "has_blocking_failures": has_blocking_metadata_failures,
                "blocking_reasons": list(
                    blocking_metadata.get("blocking_reasons", [])
                ),
            },
            expected={"has_blocking_failures": False},
            weight=_to_float(weights.get("no_blocking_metadata_failures", 0.0)),
            blocking="no_blocking_metadata_failures" in blocking_criteria_ids,
        ),
        _criterion(
            criterion_id="no_failed_command_bundles",
            description=(
                "Rehearsal command bundles must complete without failed bundle or "
                "failed command entries."
            ),
            passed=failed_command_bundles == 0 and failed_bundle_commands == 0,
            reason_code=(
                "ok"
                if failed_command_bundles == 0 and failed_bundle_commands == 0
                else "command_bundle_failures_present"
            ),
            observed={
                "failed_command_bundles": failed_command_bundles,
                "failed_bundle_commands": failed_bundle_commands,
            },
            expected={
                "failed_command_bundles": 0,
                "failed_bundle_commands": 0,
            },
            weight=_to_float(weights.get("no_failed_command_bundles", 0.0)),
            blocking="no_failed_command_bundles" in blocking_criteria_ids,
        ),
        _criterion(
            criterion_id="no_blocking_rollback_recommendations",
            description=(
                "Rollback recommendations with configured blocking severities must be "
                "resolved before canary promotion."
            ),
            passed=not blocking_rollbacks,
            reason_code=(
                "ok"
                if not blocking_rollbacks
                else "blocking_rollback_recommendations_present"
            ),
            observed={
                "blocking_recommendation_count": len(blocking_rollbacks),
                "blocking_triggers": [
                    str(row.get("trigger", "")) for row in blocking_rollbacks
                ],
            },
            expected={"blocking_recommendation_count": 0},
            weight=_to_float(
                weights.get("no_blocking_rollback_recommendations", 0.0)
            ),
            blocking="no_blocking_rollback_recommendations" in blocking_criteria_ids,
        ),
        _criterion(
            criterion_id="required_control_scenarios_passed",
            description=(
                "Runtime control rehearsal scenarios (kill switch, cancel-all, "
                "restart acknowledgement) must all PASS."
            ),
            passed=not control_failures,
            reason_code=(
                "ok"
                if not control_failures
                else "runtime_control_scenario_failed_or_missing"
            ),
            observed={
                "status_by_scenario": {
                    scenario_id: scenario_statuses.get(scenario_id, "MISSING")
                    for scenario_id in required_control_scenarios
                },
                "failed_or_missing_scenarios": control_failures,
            },
            expected={
                "required_scenarios": required_control_scenarios,
                "all_status": "PASS",
            },
            weight=_to_float(weights.get("required_control_scenarios_passed", 0.0)),
            blocking="required_control_scenarios_passed" in blocking_criteria_ids,
        ),
    ]

    total_weight = sum(max(_to_float(item.get("weight", 0.0)), 0.0) for item in criteria)
    passed_weight = sum(
        max(_to_float(item.get("weight", 0.0)), 0.0)
        for item in criteria
        if bool(item.get("passed"))
    )
    readiness_score = 0.0
    if total_weight > 0:
        readiness_score = round((passed_weight / total_weight) * 100, 3)
    score_threshold_passed = readiness_score >= minimum_readiness_score
    criteria.append(
        _criterion(
            criterion_id="readiness_score_threshold_met",
            description="Readiness score must meet or exceed minimum threshold.",
            passed=score_threshold_passed,
            reason_code=(
                "ok" if score_threshold_passed else "readiness_score_below_threshold"
            ),
            observed=readiness_score,
            expected={">=": minimum_readiness_score},
            weight=0.0,
            blocking="readiness_score_threshold_met" in blocking_criteria_ids,
        )
    )

    blockers: list[dict[str, Any]] = []
    for criterion in criteria:
        if criterion.get("passed"):
            continue
        if not criterion.get("blocking"):
            continue
        blockers.append(
            {
                "code": f"criterion_failed:{criterion['id']}",
                "severity": "blocker",
                "summary": criterion.get("description"),
                "reason_code": criterion.get("reason_code"),
                "observed": criterion.get("observed"),
                "expected": criterion.get("expected"),
            }
        )
    for recommendation in blocking_rollbacks:
        blockers.append(
            {
                "code": (
                    "unresolved_rollback_trigger:"
                    f"{str(recommendation.get('trigger', 'unknown'))}"
                ),
                "severity": str(recommendation.get("severity", "unknown")),
                "summary": str(recommendation.get("condition", "")),
                "observed": recommendation,
                "expected": "resolved_before_canary_promotion",
            }
        )

    overall_status = "PASS" if not blockers else "FAIL"
    manual_policy = dict(resolved_policy.get("manual_approval_policy", {}))
    normalized_approval_status = str(approval_status).strip().lower() or "pending"
    manual_approval_required = bool(manual_policy.get("manual_approval_required", True))
    approval_requirement_met = (
        not manual_approval_required or normalized_approval_status == "approved"
    )
    canary_enablement_allowed = overall_status == "PASS" and approval_requirement_met

    certification_hash = stable_hash(
        {
            "rehearsal_report_hash": stable_hash(rehearsal_report),
            "policy": resolved_policy,
            "criteria": criteria,
            "blockers": blockers,
            "overall_status": overall_status,
            "readiness_score": readiness_score,
            "minimum_readiness_score": minimum_readiness_score,
            "approval_status": normalized_approval_status,
            "approval_actor": approval_actor,
            "metadata": metadata or {},
        }
    )

    return {
        "schema_version": CANARY_ROLLOUT_CERTIFICATION_REPORT_SCHEMA_VERSION,
        "generated_at": _utc_now_iso(),
        "overall_status": overall_status,
        "readiness_score": readiness_score,
        "minimum_readiness_score": minimum_readiness_score,
        "policy": {
            "blocking_rollback_severities": sorted(blocking_rollback_severities),
            "required_control_scenarios": required_control_scenarios,
            "criteria_weights": weights,
            "blocking_criteria_ids": sorted(blocking_criteria_ids),
        },
        "rehearsal_summary": {
            "overall_status": rehearsal_overall_status,
            "scenario_count": _to_int(summary.get("scenario_count", 0)),
            "failed_scenarios": _to_int(summary.get("failed_scenarios", 0)),
            "failed_command_bundles": failed_command_bundles,
            "failed_bundle_commands": failed_bundle_commands,
            "rollback_recommendation_count": len(rollback_recommendations),
        },
        "criteria": criteria,
        "blockers": blockers,
        "promotion_decision": {
            "manual_approval_required": manual_approval_required,
            "approval_status": normalized_approval_status,
            "approval_actor": approval_actor,
            "approval_note": approval_note,
            "promotion_owner": manual_policy.get("promotion_owner"),
            "required_approvers": list(manual_policy.get("required_approvers", [])),
            "rollback_authority": list(manual_policy.get("rollback_authority", [])),
            "canary_enablement_allowed": canary_enablement_allowed,
        },
        "evidence": {
            "rehearsal_report_hash": stable_hash(rehearsal_report),
            "blocking_recommendation_count": len(blocking_rollbacks),
            "certification_hash": certification_hash,
        },
        "metadata": metadata or {},
    }
