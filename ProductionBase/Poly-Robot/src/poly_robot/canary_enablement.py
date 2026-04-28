from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .reproducibility import stable_hash
from .schemas import (
    CANARY_APPROVAL_RECORD_SCHEMA_VERSION,
    CANARY_STAGE_ENABLEMENT_AUDIT_EVENT_SCHEMA_VERSION,
    CANARY_STAGE_ENABLEMENT_DECISION_SCHEMA_VERSION,
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


def _normalize_decision(value: Any) -> str:
    return str(value).strip().lower()

def _to_int(value: Any, *, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _to_float_or_none(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _criterion(
    *,
    criterion_id: str,
    description: str,
    passed: bool,
    reason_code: str,
    observed: Any,
    expected: Any,
) -> dict[str, Any]:
    return {
        "id": criterion_id,
        "description": description,
        "passed": bool(passed),
        "reason_code": reason_code,
        "observed": observed,
        "expected": expected,
    }


def _approval_decisions_by_actor(approval_record: dict[str, Any]) -> dict[str, str]:
    decisions_by_actor: dict[str, str] = {}
    for approval in _as_list(approval_record.get("approvals")):
        if not isinstance(approval, dict):
            continue
        actor = str(approval.get("actor", "")).strip()
        if not actor:
            continue
        decisions_by_actor[actor] = _normalize_decision(approval.get("decision", ""))
    return decisions_by_actor


def _rollout_stage_payload(
    rollout_config: dict[str, Any], *, requested_stage: str
) -> dict[str, Any] | None:
    for stage_payload in _as_list(rollout_config.get("rollout_stages")):
        if not isinstance(stage_payload, dict):
            continue
        stage_name = str(stage_payload.get("stage", "")).strip()
        if stage_name == requested_stage:
            return stage_payload
    return None


def build_canary_stage_enablement_decision(
    *,
    certification_report: dict[str, Any],
    approval_record: dict[str, Any],
    rollout_config: dict[str, Any],
    requested_stage: str = "canary_live",
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    promotion_decision = _as_dict(certification_report.get("promotion_decision"))
    required_approvers = [
        str(value).strip()
        for value in _as_list(promotion_decision.get("required_approvers"))
        if str(value).strip()
    ]
    manual_approval_required = bool(
        promotion_decision.get("manual_approval_required", True)
    )
    promotion_owner = str(promotion_decision.get("promotion_owner", "")).strip()
    rollback_authority = [
        str(value).strip()
        for value in _as_list(promotion_decision.get("rollback_authority"))
        if str(value).strip()
    ]

    decisions_by_actor = _approval_decisions_by_actor(approval_record)
    approved_required_approvers = [
        actor for actor in required_approvers if decisions_by_actor.get(actor) == "approved"
    ]
    missing_required_approvers = [
        actor for actor in required_approvers if actor not in decisions_by_actor
    ]
    rejected_required_approvers = [
        actor for actor in required_approvers if decisions_by_actor.get(actor) == "rejected"
    ]
    pending_required_approvers = [
        actor for actor in required_approvers if decisions_by_actor.get(actor) == "pending"
    ]

    certification_overall_status = str(
        certification_report.get("overall_status", "UNKNOWN")
    ).strip()
    certification_blockers = _as_list(certification_report.get("blockers"))
    certification_blocker_count = len(certification_blockers)
    readiness_score = certification_report.get("readiness_score")
    certification_hash = str(
        _as_dict(certification_report.get("evidence")).get("certification_hash", "")
    ).strip()

    stage_payload = _rollout_stage_payload(
        rollout_config,
        requested_stage=requested_stage,
    )
    stage_payload_dict = _as_dict(stage_payload)
    stage_exists = stage_payload is not None
    stage_enabled = bool(stage_payload_dict.get("enabled", False))
    stage_real_order_submission = bool(
        stage_payload_dict.get("real_order_submission", False)
    )
    stage_financial_preconditions = _as_dict(
        stage_payload_dict.get("financial_preconditions")
    )
    stage_micro_notional_requirements = _as_dict(
        stage_payload_dict.get("micro_notional_canary_evidence")
    )

    promotion_evidence = _as_dict(approval_record.get("promotion_evidence"))
    financial_kpis = _as_dict(promotion_evidence.get("financial_kpis"))
    micro_notional_canary_evidence = _as_dict(
        promotion_evidence.get("micro_notional_canary")
    )

    required_rolling_window_cycles = max(
        0,
        _to_int(stage_financial_preconditions.get("rolling_window_cycles"), default=0),
    )
    required_rolling_realized_pnl_floor = _to_float_or_none(
        stage_financial_preconditions.get("rolling_realized_pnl_floor")
    )
    required_edge_realization_ratio_floor = _to_float_or_none(
        stage_financial_preconditions.get("edge_realization_ratio_floor")
    )
    required_max_ingestion_degraded_cycle_ratio = _to_float_or_none(
        stage_financial_preconditions.get("max_ingestion_degraded_cycle_ratio")
    )

    observed_rolling_window_cycles = max(
        0,
        _to_int(financial_kpis.get("rolling_window_cycles"), default=0),
    )
    observed_rolling_realized_pnl = _to_float_or_none(
        financial_kpis.get("rolling_realized_pnl")
    )
    observed_edge_realization_ratio = _to_float_or_none(
        financial_kpis.get("edge_realization_ratio")
    )
    observed_ingestion_degraded_cycle_ratio = _to_float_or_none(
        financial_kpis.get("ingestion_degraded_cycle_ratio")
    )

    required_micro_sample_size = max(
        0,
        _to_int(stage_micro_notional_requirements.get("minimum_sample_size"), default=0),
    )
    required_micro_max_order_notional_usd = _to_float_or_none(
        stage_micro_notional_requirements.get("max_order_notional_usd")
    )
    required_micro_max_execution_cost_degradation_ratio = _to_float_or_none(
        stage_micro_notional_requirements.get(
            "max_execution_cost_degradation_ratio"
        )
    )
    required_micro_max_slippage_bps_delta = _to_float_or_none(
        stage_micro_notional_requirements.get("max_slippage_bps_delta")
    )
    required_micro_max_edge_capture_ratio_delta = _to_float_or_none(
        stage_micro_notional_requirements.get("max_edge_capture_ratio_delta")
    )

    observed_micro_sample_size = max(
        0,
        _to_int(micro_notional_canary_evidence.get("sample_size"), default=0),
    )
    observed_micro_max_order_notional_usd = _to_float_or_none(
        micro_notional_canary_evidence.get("max_order_notional_usd")
    )
    observed_modeled_execution_cost_per_fill = _to_float_or_none(
        micro_notional_canary_evidence.get("modeled_execution_cost_per_fill")
    )
    observed_realized_execution_cost_per_fill = _to_float_or_none(
        micro_notional_canary_evidence.get("realized_execution_cost_per_fill")
    )
    observed_modeled_slippage_bps = _to_float_or_none(
        micro_notional_canary_evidence.get("modeled_slippage_bps")
    )
    observed_realized_slippage_bps = _to_float_or_none(
        micro_notional_canary_evidence.get("realized_slippage_bps")
    )
    observed_modeled_edge_capture_ratio = _to_float_or_none(
        micro_notional_canary_evidence.get("modeled_edge_capture_ratio")
    )
    observed_realized_edge_capture_ratio = _to_float_or_none(
        micro_notional_canary_evidence.get("realized_edge_capture_ratio")
    )
    observed_micro_execution_cost_degradation_ratio: float | None = None
    if (
        observed_modeled_execution_cost_per_fill is not None
        and observed_modeled_execution_cost_per_fill > 0.0
        and observed_realized_execution_cost_per_fill is not None
    ):
        observed_micro_execution_cost_degradation_ratio = (
            observed_realized_execution_cost_per_fill
            / observed_modeled_execution_cost_per_fill
        )
    observed_micro_slippage_bps_delta: float | None = None
    if (
        observed_modeled_slippage_bps is not None
        and observed_realized_slippage_bps is not None
    ):
        observed_micro_slippage_bps_delta = (
            observed_realized_slippage_bps - observed_modeled_slippage_bps
        )
    observed_micro_edge_capture_ratio_delta: float | None = None
    if (
        observed_modeled_edge_capture_ratio is not None
        and observed_realized_edge_capture_ratio is not None
    ):
        observed_micro_edge_capture_ratio_delta = (
            observed_modeled_edge_capture_ratio - observed_realized_edge_capture_ratio
        )

    criteria = [
        _criterion(
            criterion_id="certification_pass",
            description="Canary readiness certification overall_status must be PASS.",
            passed=certification_overall_status == "PASS",
            reason_code=(
                "ok"
                if certification_overall_status == "PASS"
                else "certification_not_pass"
            ),
            observed=certification_overall_status,
            expected="PASS",
        ),
        _criterion(
            criterion_id="certification_blockers_clear",
            description="Readiness certification blockers list must be empty.",
            passed=certification_blocker_count == 0,
            reason_code=(
                "ok"
                if certification_blocker_count == 0
                else "certification_blockers_present"
            ),
            observed={"blocker_count": certification_blocker_count},
            expected={"blocker_count": 0},
        ),
        _criterion(
            criterion_id="required_approvers_present",
            description="All required approvers must have approval-record entries.",
            passed=not missing_required_approvers,
            reason_code=(
                "ok"
                if not missing_required_approvers
                else "required_approver_missing"
            ),
            observed={"missing_required_approvers": missing_required_approvers},
            expected={"missing_required_approvers": []},
        ),
        _criterion(
            criterion_id="required_approvers_approved",
            description="All required approvers must have decision=approved.",
            passed=(
                (not manual_approval_required)
                or (
                    not missing_required_approvers
                    and not rejected_required_approvers
                    and not pending_required_approvers
                    and len(approved_required_approvers) == len(required_approvers)
                )
            ),
            reason_code=(
                "ok"
                if (
                    (not manual_approval_required)
                    or (
                        not missing_required_approvers
                        and not rejected_required_approvers
                        and not pending_required_approvers
                        and len(approved_required_approvers) == len(required_approvers)
                    )
                )
                else "required_approver_not_approved"
            ),
            observed={
                "approved_required_approvers": approved_required_approvers,
                "pending_required_approvers": pending_required_approvers,
                "rejected_required_approvers": rejected_required_approvers,
            },
            expected={"all_required_decision": "approved"},
        ),
        _criterion(
            criterion_id="requested_stage_exists",
            description="Requested rollout stage must exist in live rollout config.",
            passed=stage_exists,
            reason_code="ok" if stage_exists else "requested_stage_not_found",
            observed={"requested_stage": requested_stage},
            expected={"stage_exists": True},
        ),
        _criterion(
            criterion_id="requested_stage_live_capable",
            description=(
                "Requested stage must be configured for real_order_submission=true."
            ),
            passed=stage_exists and stage_real_order_submission,
            reason_code=(
                "ok"
                if stage_exists and stage_real_order_submission
                else "requested_stage_not_live_capable"
            ),
            observed={"real_order_submission": stage_real_order_submission},
            expected={"real_order_submission": True},
        ),
        _criterion(
            criterion_id="requested_stage_currently_disabled",
            description=(
                "Requested stage should remain disabled before enablement decision."
            ),
            passed=stage_exists and not stage_enabled,
            reason_code=(
                "ok" if stage_exists and not stage_enabled else "requested_stage_already_enabled"
            ),
            observed={"enabled": stage_enabled},
            expected={"enabled": False},
        ),
    ]
    if stage_financial_preconditions:
        criteria.extend(
            [
                _criterion(
                    criterion_id="rolling_window_cycles_sufficient",
                    description=(
                        "Financial KPI evidence window must include at least the "
                        "required rolling cycle count."
                    ),
                    passed=(
                        required_rolling_window_cycles <= 0
                        or observed_rolling_window_cycles >= required_rolling_window_cycles
                    ),
                    reason_code=(
                        "ok"
                        if (
                            required_rolling_window_cycles <= 0
                            or observed_rolling_window_cycles
                            >= required_rolling_window_cycles
                        )
                        else (
                            "financial_window_cycles_missing"
                            if observed_rolling_window_cycles <= 0
                            else "rolling_window_cycles_below_requirement"
                        )
                    ),
                    observed={"rolling_window_cycles": observed_rolling_window_cycles},
                    expected={">=": required_rolling_window_cycles},
                ),
                _criterion(
                    criterion_id="rolling_realized_pnl_floor_met",
                    description=(
                        "Rolling realized PnL must meet or exceed configured floor."
                    ),
                    passed=(
                        required_rolling_realized_pnl_floor is None
                        or (
                            observed_rolling_realized_pnl is not None
                            and observed_rolling_realized_pnl
                            >= required_rolling_realized_pnl_floor
                        )
                    ),
                    reason_code=(
                        "ok"
                        if (
                            required_rolling_realized_pnl_floor is None
                            or (
                                observed_rolling_realized_pnl is not None
                                and observed_rolling_realized_pnl
                                >= required_rolling_realized_pnl_floor
                            )
                        )
                        else (
                            "rolling_realized_pnl_missing"
                            if observed_rolling_realized_pnl is None
                            else "rolling_realized_pnl_below_floor"
                        )
                    ),
                    observed={"rolling_realized_pnl": observed_rolling_realized_pnl},
                    expected={
                        "rolling_realized_pnl_floor": required_rolling_realized_pnl_floor
                    },
                ),
                _criterion(
                    criterion_id="edge_realization_ratio_floor_met",
                    description=(
                        "Edge-realization ratio must meet or exceed configured floor."
                    ),
                    passed=(
                        required_edge_realization_ratio_floor is None
                        or (
                            observed_edge_realization_ratio is not None
                            and observed_edge_realization_ratio
                            >= required_edge_realization_ratio_floor
                        )
                    ),
                    reason_code=(
                        "ok"
                        if (
                            required_edge_realization_ratio_floor is None
                            or (
                                observed_edge_realization_ratio is not None
                                and observed_edge_realization_ratio
                                >= required_edge_realization_ratio_floor
                            )
                        )
                        else (
                            "edge_realization_ratio_missing"
                            if observed_edge_realization_ratio is None
                            else "edge_realization_ratio_below_floor"
                        )
                    ),
                    observed={"edge_realization_ratio": observed_edge_realization_ratio},
                    expected={
                        "edge_realization_ratio_floor": (
                            required_edge_realization_ratio_floor
                        )
                    },
                ),
                _criterion(
                    criterion_id="ingestion_quality_ceiling_met",
                    description=(
                        "Ingestion degraded-cycle ratio must stay at or below "
                        "configured ceiling."
                    ),
                    passed=(
                        required_max_ingestion_degraded_cycle_ratio is None
                        or (
                            observed_ingestion_degraded_cycle_ratio is not None
                            and observed_ingestion_degraded_cycle_ratio
                            <= required_max_ingestion_degraded_cycle_ratio
                        )
                    ),
                    reason_code=(
                        "ok"
                        if (
                            required_max_ingestion_degraded_cycle_ratio is None
                            or (
                                observed_ingestion_degraded_cycle_ratio is not None
                                and observed_ingestion_degraded_cycle_ratio
                                <= required_max_ingestion_degraded_cycle_ratio
                            )
                        )
                        else (
                            "ingestion_degraded_ratio_missing"
                            if observed_ingestion_degraded_cycle_ratio is None
                            else "ingestion_degraded_ratio_above_ceiling"
                        )
                    ),
                    observed={
                        "ingestion_degraded_cycle_ratio": (
                            observed_ingestion_degraded_cycle_ratio
                        )
                    },
                    expected={
                        "max_ingestion_degraded_cycle_ratio": (
                            required_max_ingestion_degraded_cycle_ratio
                        )
                    },
                ),
            ]
        )
    if stage_micro_notional_requirements:
        criteria.extend(
            [
                _criterion(
                    criterion_id="micro_notional_sample_size_sufficient",
                    description=(
                        "Micro-notional canary evidence must include required minimum "
                        "sample size."
                    ),
                    passed=(
                        required_micro_sample_size <= 0
                        or observed_micro_sample_size >= required_micro_sample_size
                    ),
                    reason_code=(
                        "ok"
                        if (
                            required_micro_sample_size <= 0
                            or observed_micro_sample_size >= required_micro_sample_size
                        )
                        else (
                            "micro_notional_sample_size_missing"
                            if observed_micro_sample_size <= 0
                            else "micro_notional_sample_size_below_requirement"
                        )
                    ),
                    observed={"sample_size": observed_micro_sample_size},
                    expected={">=": required_micro_sample_size},
                ),
                _criterion(
                    criterion_id="micro_notional_notional_cap_respected",
                    description=(
                        "Micro-notional canary evidence must stay within configured "
                        "maximum order notional."
                    ),
                    passed=(
                        required_micro_max_order_notional_usd is None
                        or (
                            observed_micro_max_order_notional_usd is not None
                            and observed_micro_max_order_notional_usd
                            <= required_micro_max_order_notional_usd
                        )
                    ),
                    reason_code=(
                        "ok"
                        if (
                            required_micro_max_order_notional_usd is None
                            or (
                                observed_micro_max_order_notional_usd is not None
                                and observed_micro_max_order_notional_usd
                                <= required_micro_max_order_notional_usd
                            )
                        )
                        else (
                            "micro_notional_max_order_notional_missing"
                            if observed_micro_max_order_notional_usd is None
                            else "micro_notional_order_notional_above_cap"
                        )
                    ),
                    observed={"max_order_notional_usd": observed_micro_max_order_notional_usd},
                    expected={"max_order_notional_usd": required_micro_max_order_notional_usd},
                ),
                _criterion(
                    criterion_id="micro_notional_execution_cost_alignment_met",
                    description=(
                        "Realized execution cost degradation versus modeled execution "
                        "cost must stay within configured tolerance."
                    ),
                    passed=(
                        required_micro_max_execution_cost_degradation_ratio is None
                        or (
                            observed_micro_execution_cost_degradation_ratio is not None
                            and observed_micro_execution_cost_degradation_ratio
                            <= required_micro_max_execution_cost_degradation_ratio
                        )
                    ),
                    reason_code=(
                        "ok"
                        if (
                            required_micro_max_execution_cost_degradation_ratio is None
                            or (
                                observed_micro_execution_cost_degradation_ratio
                                is not None
                                and observed_micro_execution_cost_degradation_ratio
                                <= required_micro_max_execution_cost_degradation_ratio
                            )
                        )
                        else (
                            "micro_notional_execution_cost_evidence_missing"
                            if observed_micro_execution_cost_degradation_ratio is None
                            else "micro_notional_execution_cost_degradation_exceeded"
                        )
                    ),
                    observed={
                        "modeled_execution_cost_per_fill": (
                            observed_modeled_execution_cost_per_fill
                        ),
                        "realized_execution_cost_per_fill": (
                            observed_realized_execution_cost_per_fill
                        ),
                        "execution_cost_degradation_ratio": (
                            observed_micro_execution_cost_degradation_ratio
                        ),
                    },
                    expected={
                        "max_execution_cost_degradation_ratio": (
                            required_micro_max_execution_cost_degradation_ratio
                        )
                    },
                ),
                _criterion(
                    criterion_id="micro_notional_slippage_alignment_met",
                    description=(
                        "Realized slippage delta versus modeled slippage must remain "
                        "within configured tolerance (bps)."
                    ),
                    passed=(
                        required_micro_max_slippage_bps_delta is None
                        or (
                            observed_micro_slippage_bps_delta is not None
                            and observed_micro_slippage_bps_delta
                            <= required_micro_max_slippage_bps_delta
                        )
                    ),
                    reason_code=(
                        "ok"
                        if (
                            required_micro_max_slippage_bps_delta is None
                            or (
                                observed_micro_slippage_bps_delta is not None
                                and observed_micro_slippage_bps_delta
                                <= required_micro_max_slippage_bps_delta
                            )
                        )
                        else (
                            "micro_notional_slippage_evidence_missing"
                            if observed_micro_slippage_bps_delta is None
                            else "micro_notional_slippage_delta_exceeded"
                        )
                    ),
                    observed={
                        "modeled_slippage_bps": observed_modeled_slippage_bps,
                        "realized_slippage_bps": observed_realized_slippage_bps,
                        "slippage_bps_delta": observed_micro_slippage_bps_delta,
                    },
                    expected={
                        "max_slippage_bps_delta": required_micro_max_slippage_bps_delta
                    },
                ),
                _criterion(
                    criterion_id="micro_notional_edge_capture_alignment_met",
                    description=(
                        "Realized edge-capture ratio degradation versus modeled edge "
                        "capture must stay within configured tolerance."
                    ),
                    passed=(
                        required_micro_max_edge_capture_ratio_delta is None
                        or (
                            observed_micro_edge_capture_ratio_delta is not None
                            and observed_micro_edge_capture_ratio_delta
                            <= required_micro_max_edge_capture_ratio_delta
                        )
                    ),
                    reason_code=(
                        "ok"
                        if (
                            required_micro_max_edge_capture_ratio_delta is None
                            or (
                                observed_micro_edge_capture_ratio_delta is not None
                                and observed_micro_edge_capture_ratio_delta
                                <= required_micro_max_edge_capture_ratio_delta
                            )
                        )
                        else (
                            "micro_notional_edge_capture_evidence_missing"
                            if observed_micro_edge_capture_ratio_delta is None
                            else "micro_notional_edge_capture_delta_exceeded"
                        )
                    ),
                    observed={
                        "modeled_edge_capture_ratio": (
                            observed_modeled_edge_capture_ratio
                        ),
                        "realized_edge_capture_ratio": (
                            observed_realized_edge_capture_ratio
                        ),
                        "edge_capture_ratio_delta": (
                            observed_micro_edge_capture_ratio_delta
                        ),
                    },
                    expected={
                        "max_edge_capture_ratio_delta": (
                            required_micro_max_edge_capture_ratio_delta
                        )
                    },
                ),
            ]
        )

    failed_reason_codes = [
        str(criterion.get("reason_code", "unknown"))
        for criterion in criteria
        if not bool(criterion.get("passed"))
    ]
    decision_status = "ALLOW" if not failed_reason_codes else "DENY"
    canary_stage_enablement_allowed = decision_status == "ALLOW"

    decision_payload = {
        "schema_version": CANARY_STAGE_ENABLEMENT_DECISION_SCHEMA_VERSION,
        "generated_at": _utc_now_iso(),
        "requested_stage": requested_stage,
        "decision_status": decision_status,
        "canary_stage_enablement_allowed": canary_stage_enablement_allowed,
        "criteria": criteria,
        "failed_reason_codes": failed_reason_codes,
        "certification_state": {
            "overall_status": certification_overall_status,
            "readiness_score": readiness_score,
            "blocker_count": certification_blocker_count,
        },
        "approval_state": {
            "schema_version": str(
                approval_record.get(
                    "schema_version", CANARY_APPROVAL_RECORD_SCHEMA_VERSION
                )
            ),
            "record_id": str(approval_record.get("record_id", "")).strip(),
            "requested_by": str(approval_record.get("requested_by", "")).strip(),
            "required_approvers": required_approvers,
            "approved_required_approvers": approved_required_approvers,
            "missing_required_approvers": missing_required_approvers,
            "pending_required_approvers": pending_required_approvers,
            "rejected_required_approvers": rejected_required_approvers,
        },
        "promotion_boundary": {
            "manual_approval_required": manual_approval_required,
            "promotion_owner": promotion_owner,
            "required_approvers": required_approvers,
            "rollback_authority": rollback_authority,
        },
        "rollout_stage_state": {
            "stage_exists": stage_exists,
            "enabled": stage_enabled,
            "real_order_submission": stage_real_order_submission,
            "max_order_notional_usd": stage_payload_dict.get("max_order_notional_usd"),
            "max_daily_notional_usd": stage_payload_dict.get("max_daily_notional_usd"),
            "max_open_orders": stage_payload_dict.get("max_open_orders"),
            "financial_preconditions": stage_financial_preconditions,
            "micro_notional_canary_evidence": stage_micro_notional_requirements,
        },
        "promotion_evidence": {
            "financial_kpis": financial_kpis,
            "micro_notional_canary": micro_notional_canary_evidence,
            "derived": {
                "execution_cost_degradation_ratio": (
                    observed_micro_execution_cost_degradation_ratio
                ),
                "slippage_bps_delta": observed_micro_slippage_bps_delta,
                "edge_capture_ratio_delta": observed_micro_edge_capture_ratio_delta,
            },
        },
        "rollback_handoff": {
            "rollback_authority": rollback_authority,
            "emergency_actions": _as_list(rollout_config.get("emergency_actions")),
        },
        "metadata": metadata or {},
    }
    decision_payload["evidence"] = {
        "certification_hash": certification_hash,
        "approval_record_hash": stable_hash(approval_record),
        "decision_hash": stable_hash(
            {
                "requested_stage": requested_stage,
                "decision_status": decision_status,
                "failed_reason_codes": failed_reason_codes,
                "certification_hash": certification_hash,
                "approval_record_hash": stable_hash(approval_record),
                "criteria": criteria,
                "metadata": metadata or {},
            }
        ),
    }
    return decision_payload


def append_canary_stage_enablement_audit_event(
    *,
    audit_path: Path,
    decision_report: dict[str, Any],
    actor: str,
    reason: str | None = None,
) -> dict[str, Any]:
    evidence = _as_dict(decision_report.get("evidence"))
    event = {
        "schema_version": CANARY_STAGE_ENABLEMENT_AUDIT_EVENT_SCHEMA_VERSION,
        "recorded_at": _utc_now_iso(),
        "actor": str(actor).strip(),
        "reason": reason,
        "requested_stage": str(decision_report.get("requested_stage", "")).strip(),
        "decision_status": str(decision_report.get("decision_status", "UNKNOWN")).strip(),
        "canary_stage_enablement_allowed": bool(
            decision_report.get("canary_stage_enablement_allowed", False)
        ),
        "failed_reason_codes": list(decision_report.get("failed_reason_codes", [])),
        "certification_hash": str(evidence.get("certification_hash", "")).strip(),
        "approval_record_hash": str(evidence.get("approval_record_hash", "")).strip(),
        "decision_hash": str(evidence.get("decision_hash", "")).strip(),
    }
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    with audit_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, sort_keys=True) + "\n")
    return event
