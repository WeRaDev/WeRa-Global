from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from .reproducibility import stable_hash
from .schemas import MODE_LIFECYCLE_DECISION_SCHEMA_VERSION

MODE_PAPER = "paper"
MODE_TEST = "test"
MODE_LIVE = "live"
SUPPORTED_MODES = (MODE_PAPER, MODE_TEST, MODE_LIVE)


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="milliseconds")


def normalize_mode(value: Any) -> str:
    mode = str(value or MODE_PAPER).strip().lower()
    if mode not in SUPPORTED_MODES:
        return MODE_PAPER
    return mode


def transition_id(from_mode: str, to_mode: str) -> str:
    return f"{normalize_mode(from_mode)}_to_{normalize_mode(to_mode)}"


def default_mode_lifecycle_policy() -> dict[str, Any]:
    return {
        "schema_version": "mode_lifecycle_policy.v1",
        "default_mode": MODE_PAPER,
        "test_mode_execution": {
            "primary_environment": "polygon_amoy_testnet",
            "fallback_environment": "mainnet_micro_notional_canary",
            "fallback_reason_code": "testnet_parity_unavailable",
        },
        "transitions": [
            {
                "id": "paper_to_test",
                "from_mode": MODE_PAPER,
                "to_mode": MODE_TEST,
                "required_evidence": [
                    "milestone_c_sequence",
                    "trl4_profitability",
                ],
                "require_manual_approval": True,
                "allowed_approval_statuses": ["approved"],
            },
            {
                "id": "test_to_live",
                "from_mode": MODE_TEST,
                "to_mode": MODE_LIVE,
                "required_evidence": [
                    "canary_lifecycle_gate",
                    "test_mode_profitability",
                ],
                "require_manual_approval": True,
                "allowed_approval_statuses": ["approved"],
            },
        ],
        "allow_emergency_rollback_to_paper": True,
    }


def resolve_mode_lifecycle_policy(policy: dict[str, Any] | None) -> dict[str, Any]:
    resolved = default_mode_lifecycle_policy()
    if not policy:
        return resolved
    resolved.update(policy)

    transitions = policy.get("transitions")
    if isinstance(transitions, list):
        cleaned: list[dict[str, Any]] = []
        for row in transitions:
            if not isinstance(row, dict):
                continue
            from_mode = normalize_mode(row.get("from_mode"))
            to_mode = normalize_mode(row.get("to_mode"))
            transition_name = str(row.get("id", "")).strip() or transition_id(
                from_mode, to_mode
            )
            required_evidence = [
                str(item).strip()
                for item in row.get("required_evidence", [])
                if str(item).strip()
            ]
            allowed_approval_statuses = [
                str(item).strip().lower()
                for item in row.get("allowed_approval_statuses", [])
                if str(item).strip()
            ]
            cleaned.append(
                {
                    "id": transition_name,
                    "from_mode": from_mode,
                    "to_mode": to_mode,
                    "required_evidence": required_evidence,
                    "require_manual_approval": bool(
                        row.get("require_manual_approval", True)
                    ),
                    "allowed_approval_statuses": (
                        allowed_approval_statuses or ["approved"]
                    ),
                }
            )
        if cleaned:
            resolved["transitions"] = cleaned
    return resolved


def _transition_row(
    *, from_mode: str, to_mode: str, policy: dict[str, Any]
) -> dict[str, Any] | None:
    for row in policy.get("transitions", []):
        if not isinstance(row, dict):
            continue
        if normalize_mode(row.get("from_mode")) != normalize_mode(from_mode):
            continue
        if normalize_mode(row.get("to_mode")) != normalize_mode(to_mode):
            continue
        return row
    return None


def _evidence_passes(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, dict):
        status = str(value.get("status", "")).strip().upper()
        if status in {"PASS", "SUCCESS", "ALLOW", "OK"}:
            return True
        if status in {"FAIL", "FAILED", "DENY", "ERROR"}:
            return False
        if "passed" in value:
            return bool(value.get("passed"))
    status = str(value).strip().upper()
    return status in {"PASS", "SUCCESS", "ALLOW", "OK", "TRUE", "1"}


def build_mode_transition_decision(
    *,
    current_mode: str,
    target_mode: str,
    policy: dict[str, Any] | None = None,
    evidence: dict[str, Any] | None = None,
    manual_approval_status: str = "pending",
    actor: str | None = None,
    reason: str | None = None,
) -> dict[str, Any]:
    resolved_policy = resolve_mode_lifecycle_policy(policy)
    normalized_current_mode = normalize_mode(current_mode)
    normalized_target_mode = normalize_mode(target_mode)
    approval_status = str(manual_approval_status or "pending").strip().lower()
    evidence_payload = evidence or {}

    reason_codes: list[str] = []
    matching_transition = _transition_row(
        from_mode=normalized_current_mode,
        to_mode=normalized_target_mode,
        policy=resolved_policy,
    )

    if matching_transition is None and normalized_current_mode != normalized_target_mode:
        emergency_rollback_allowed = bool(
            resolved_policy.get("allow_emergency_rollback_to_paper", True)
        )
        if not (
            emergency_rollback_allowed
            and normalized_target_mode == MODE_PAPER
            and normalized_current_mode in {MODE_TEST, MODE_LIVE}
        ):
            reason_codes.append("illegal_transition")

    required_evidence = []
    manual_approval_required = False
    allowed_approval_statuses = ["approved"]
    if matching_transition is not None:
        required_evidence = [
            str(item).strip()
            for item in matching_transition.get("required_evidence", [])
            if str(item).strip()
        ]
        manual_approval_required = bool(
            matching_transition.get("require_manual_approval", True)
        )
        allowed_approval_statuses = [
            str(item).strip().lower()
            for item in matching_transition.get("allowed_approval_statuses", [])
            if str(item).strip()
        ] or ["approved"]

    missing_evidence = [
        evidence_key for evidence_key in required_evidence if evidence_key not in evidence_payload
    ]
    failing_evidence = [
        evidence_key
        for evidence_key in required_evidence
        if evidence_key in evidence_payload and not _evidence_passes(evidence_payload[evidence_key])
    ]
    if missing_evidence:
        reason_codes.append("required_evidence_missing")
    if failing_evidence:
        reason_codes.append("required_evidence_not_pass")
    if manual_approval_required and approval_status not in allowed_approval_statuses:
        reason_codes.append("manual_approval_not_satisfied")

    transition_name = (
        str(matching_transition.get("id", "")).strip()
        if matching_transition is not None
        else transition_id(normalized_current_mode, normalized_target_mode)
    )
    allowed = not reason_codes
    decision = {
        "schema_version": MODE_LIFECYCLE_DECISION_SCHEMA_VERSION,
        "generated_at": _utc_now_iso(),
        "transition_id": transition_name,
        "current_mode": normalized_current_mode,
        "target_mode": normalized_target_mode,
        "allowed": allowed,
        "reason_codes": reason_codes,
        "required_evidence": required_evidence,
        "missing_evidence": missing_evidence,
        "failing_evidence": failing_evidence,
        "manual_approval_required": manual_approval_required,
        "manual_approval_status": approval_status,
        "allowed_approval_statuses": allowed_approval_statuses,
        "evidence": evidence_payload,
        "actor": actor,
        "reason": reason,
    }
    decision["decision_hash"] = stable_hash(
        {
            "transition_id": decision["transition_id"],
            "current_mode": decision["current_mode"],
            "target_mode": decision["target_mode"],
            "allowed": decision["allowed"],
            "reason_codes": decision["reason_codes"],
            "required_evidence": decision["required_evidence"],
            "missing_evidence": decision["missing_evidence"],
            "failing_evidence": decision["failing_evidence"],
            "manual_approval_required": decision["manual_approval_required"],
            "manual_approval_status": decision["manual_approval_status"],
            "allowed_approval_statuses": decision["allowed_approval_statuses"],
            "evidence": decision["evidence"],
        }
    )
    return decision


def select_test_mode_environment(
    *,
    policy: dict[str, Any] | None = None,
    testnet_parity_supported: bool = True,
) -> dict[str, Any]:
    resolved_policy = resolve_mode_lifecycle_policy(policy)
    test_mode_payload = resolved_policy.get("test_mode_execution")
    if not isinstance(test_mode_payload, dict):
        test_mode_payload = {}
    primary_environment = str(
        test_mode_payload.get("primary_environment", "polygon_amoy_testnet")
    ).strip() or "polygon_amoy_testnet"
    fallback_environment = str(
        test_mode_payload.get("fallback_environment", "mainnet_micro_notional_canary")
    ).strip() or "mainnet_micro_notional_canary"
    fallback_reason_code = str(
        test_mode_payload.get("fallback_reason_code", "testnet_parity_unavailable")
    ).strip() or "testnet_parity_unavailable"

    if testnet_parity_supported:
        return {
            "selected_environment": primary_environment,
            "fallback_used": False,
            "reason_code": "",
            "primary_environment": primary_environment,
            "fallback_environment": fallback_environment,
        }
    return {
        "selected_environment": fallback_environment,
        "fallback_used": True,
        "reason_code": fallback_reason_code,
        "primary_environment": primary_environment,
        "fallback_environment": fallback_environment,
    }
