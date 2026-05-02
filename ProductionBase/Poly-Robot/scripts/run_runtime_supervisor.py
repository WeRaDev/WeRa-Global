#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from poly_robot.contracts import MarketEvent, PortfolioState  # noqa: E402
from poly_robot.agent_operator import AgentOperator, ClaudeApiClient  # noqa: E402
from poly_robot.integration_adapters import (  # noqa: E402
    HardenedExecutionAdapter,
    HistoricalIngestionAdapter,
    LivePolymarketIngestionAdapter,
    PolymarketClobExecutionAdapter,
)
from poly_robot.llm_policy import load_calibration_policy  # noqa: E402
from poly_robot.mode_lifecycle import (  # noqa: E402
    build_mode_transition_decision,
    normalize_mode as normalize_lifecycle_mode,
    resolve_mode_lifecycle_policy,
    select_test_mode_environment,
)
from poly_robot.paper_execution import PaperExecutionAdapter  # noqa: E402
from poly_robot.reproducibility import hash_events, stable_hash  # noqa: E402
from poly_robot.risk_engine import RiskEngine  # noqa: E402
from poly_robot.runtime_supervisor import RuntimeSupervisor, WorkerSpec  # noqa: E402
from poly_robot.runtime_web_gui import OperatorControlManager  # noqa: E402
from poly_robot.scenario_pack import (  # noqa: E402
    ReplayScenario,
    apply_scenario_to_events,
    load_scenario_pack,
)
from poly_robot.strategy_baseline import BaselineStrategy  # noqa: E402
from poly_robot.test_token_loop import TestTokenLoop, serialize_test_token_loop_run  # noqa: E402
EXECUTION_MODE_BY_LIFECYCLE_MODE = {
    "paper": "paper",
    "test": "test_polymarket_clob",
    "live": "live_polymarket_clob",
}
LIFECYCLE_MODE_BY_EXECUTION_MODE = {
    value: key for key, value in EXECUTION_MODE_BY_LIFECYCLE_MODE.items()
}


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _shift_iso_timestamp_for_cycle(timestamp: str, *, cycle_index: int) -> str:
    if cycle_index <= 1:
        return timestamp
    raw = str(timestamp or "").strip()
    if not raw:
        return timestamp
    normalized = raw[:-1] + "+00:00" if raw.endswith("Z") else raw
    try:
        dt = datetime.fromisoformat(normalized)
    except ValueError:
        return timestamp
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    shifted = dt.astimezone(UTC) + timedelta(hours=(cycle_index - 1))
    return shifted.isoformat().replace("+00:00", "Z")


def _offset_events_for_cycle(
    events: list[MarketEvent], *, cycle_index: int
) -> list[MarketEvent]:
    if cycle_index <= 1:
        return events
    shifted_events: list[MarketEvent] = []
    for event in events:
        payload = event.to_dict()
        payload["timestamp"] = _shift_iso_timestamp_for_cycle(
            str(payload.get("timestamp", event.timestamp)),
            cycle_index=cycle_index,
        )
        shifted_events.append(MarketEvent.from_dict(payload))
    return shifted_events


def _prepare_sorted_historical_events(events_path: Path) -> Path:
    lines = events_path.read_text(encoding="utf-8").splitlines()
    records: list[tuple[str, str, int, dict[str, Any]]] = []
    for index, raw_line in enumerate(lines):
        line = raw_line.strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            return events_path
        timestamp = str(payload.get("timestamp", ""))
        event_id = str(payload.get("event_id", ""))
        records.append((timestamp, event_id, index, payload))

    if not records:
        return events_path

    sorted_records = sorted(records, key=lambda row: (row[0], row[1], row[2]))
    already_sorted = all(
        left[:3] == right[:3]
        for left, right in zip(records, sorted_records, strict=False)
    )
    if already_sorted:
        return events_path

    output_dir = Path("/tmp/poly_robot_preprocessed_events")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{events_path.stem}.sorted.jsonl"
    serialized = [
        json.dumps(payload, separators=(",", ":"))
        for _, _, _, payload in sorted_records
    ]
    output_path.write_text("\n".join(serialized) + "\n", encoding="utf-8")
    return output_path


def _load_profile_payload(profile_path: Path) -> tuple[dict, dict]:
    payload = _load_json(profile_path)
    values = payload.get("values")
    if not isinstance(values, dict):
        raise ValueError(f"Profile values must be an object in {profile_path}")
    return payload, values


def _resolve_rollout_stage(
    rollout_payload: dict,
    *,
    requested_stage: str | None,
) -> tuple[str, dict]:
    rollout_stages = rollout_payload.get("rollout_stages")
    if not isinstance(rollout_stages, list):
        raise ValueError("Rollout config must include rollout_stages list")
    stage_by_name: dict[str, dict] = {}
    for row in rollout_stages:
        if not isinstance(row, dict):
            continue
        stage_name = str(row.get("stage", "")).strip()
        if stage_name:
            stage_by_name[stage_name] = row
    if not stage_by_name:
        raise ValueError("Rollout config has no valid rollout stages")
    if requested_stage is not None:
        normalized_requested = requested_stage.strip()
        selected = stage_by_name.get(normalized_requested)
        if selected is None:
            available = ", ".join(sorted(stage_by_name))
            raise ValueError(
                "Unknown rollout stage "
                f"{normalized_requested!r}. Available: {available}"
            )
        return normalized_requested, selected
    for stage_name, stage_config in stage_by_name.items():
        if bool(stage_config.get("enabled", False)):
            return stage_name, stage_config
    fallback_stage_name = next(iter(stage_by_name))
    return fallback_stage_name, stage_by_name[fallback_stage_name]


def _extract_wallet_convergence_count(value: object) -> float | None:
    if isinstance(value, dict):
        for key in (
            "target_wallet_count",
            "wallet_count",
            "convergence_count",
            "count",
        ):
            if key in value:
                return _extract_wallet_convergence_count(value[key])
        return None
    try:
        count = float(value)
    except (TypeError, ValueError):
        return None
    if count < 0:
        return None
    return count


def _load_wallet_convergence_payload(path: Path) -> dict[str, float]:
    if not path.exists():
        return {}
    payload = _load_json(path)
    source: object = payload
    if isinstance(payload, dict):
        if isinstance(payload.get("markets"), dict):
            source = payload["markets"]
        elif isinstance(payload.get("markets"), list):
            source = payload["markets"]

    normalized: dict[str, float] = {}
    if isinstance(source, dict):
        for market_id, raw_count in source.items():
            market_key = str(market_id).strip()
            if not market_key:
                continue
            count = _extract_wallet_convergence_count(raw_count)
            if count is None:
                continue
            normalized[market_key] = count
        return normalized

    if isinstance(source, list):
        for row in source:
            if not isinstance(row, dict):
                continue
            market_key = str(
                row.get("market_id") or row.get("marketId") or row.get("id") or ""
            ).strip()
            if not market_key:
                continue
            count = _extract_wallet_convergence_count(row)
            if count is None:
                continue
            normalized[market_key] = count
        return normalized

    return {}


def _as_optional_positive_float(value: object) -> float | None:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    if parsed <= 0:
        return None
    return parsed


def _as_optional_positive_int(value: object) -> int | None:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return None
    if parsed <= 0:
        return None
    return parsed


def _normalize_agent_operator_mode(value: object) -> str:
    mode = str(value or "advisory").strip().lower()
    if mode not in {"advisory", "strategy"}:
        return "advisory"
    return mode


def _normalize_mode_transition_approval_status(value: object) -> str:
    status = str(value or "pending").strip().lower()
    if status not in {"pending", "approved", "rejected"}:
        return "pending"
    return status


def _execution_mode_for_lifecycle_mode(mode: object) -> str:
    normalized_mode = normalize_lifecycle_mode(mode)
    return EXECUTION_MODE_BY_LIFECYCLE_MODE.get(normalized_mode, "paper")


def _lifecycle_mode_for_execution_mode(mode: object) -> str:
    normalized_mode = str(mode or "paper").strip().lower()
    return LIFECYCLE_MODE_BY_EXECUTION_MODE.get(normalized_mode, "paper")


def _secret_max_age_days_from_seconds(secret_max_age_seconds: float) -> int:
    return max(1, math.ceil(secret_max_age_seconds / 86_400))

def _resolve_l1_auth_guard(
    *,
    operation: str,
    context: str | None,
    operator_actor: str,
    control_manager: OperatorControlManager,
    control_state_path: Path,
    ignore_operator_controls: bool,
) -> dict[str, object]:
    normalized_operation = str(operation or "none").strip().lower() or "none"
    normalized_context = str(context or "").strip().lower()
    requested = normalized_operation != "none"
    summary: dict[str, object] = {
        "requested": requested,
        "operation": normalized_operation,
        "context": normalized_context or None,
        "operator_actor": str(operator_actor).strip(),
        "control_state_available": False,
        "restart_requested": False,
        "kill_switch_active": False,
        "cancel_all_requested": False,
        "allowed": False,
        "status": "not_requested",
        "reason_codes": [],
    }
    if not requested:
        return summary

    reason_codes: list[str] = []
    if normalized_context not in {"startup", "restart", "emergency"}:
        reason_codes.append("l1_auth_context_missing_or_invalid")

    if str(operator_actor).strip().lower() != "operator":
        reason_codes.append("l1_auth_operator_actor_not_authorized")

    control_state_available = bool(
        not ignore_operator_controls and control_state_path.exists()
    )
    summary["control_state_available"] = control_state_available
    if control_state_available:
        try:
            control_state = control_manager.load_control_state()
        except Exception:
            reason_codes.append("l1_auth_control_state_unreadable")
        else:
            restart_requested = bool(control_state.get("restart_requested", False))
            kill_switch_active = bool(control_state.get("kill_switch_active", False))
            cancel_all_requested = bool(control_state.get("cancel_all_requested", False))
            summary["restart_requested"] = restart_requested
            summary["kill_switch_active"] = kill_switch_active
            summary["cancel_all_requested"] = cancel_all_requested

    if normalized_context == "restart":
        if ignore_operator_controls:
            reason_codes.append("l1_auth_restart_requires_operator_controls")
        elif not control_state_available:
            reason_codes.append("l1_auth_control_state_unavailable")
        elif not bool(summary["restart_requested"]):
            reason_codes.append("l1_auth_restart_not_requested")
    elif normalized_context == "emergency":
        if ignore_operator_controls:
            reason_codes.append("l1_auth_emergency_requires_operator_controls")
        elif not control_state_available:
            reason_codes.append("l1_auth_control_state_unavailable")
        elif not (
            bool(summary["kill_switch_active"])
            or bool(summary["cancel_all_requested"])
        ):
            reason_codes.append("l1_auth_emergency_not_active")

    summary["reason_codes"] = reason_codes
    summary["allowed"] = not reason_codes
    summary["status"] = "allowed" if not reason_codes else "denied"
    return summary



def _run_live_credential_preflight(
    *,
    execution_adapter: PolymarketClobExecutionAdapter,
    rollout_stage_name: str,
    stage_enabled: bool,
    real_order_submission: bool,
    allow_real_trading: bool,
    l1_auth_guard: dict[str, object],
) -> dict[str, object]:
    preflight_required = (
        stage_enabled
        and real_order_submission
        and allow_real_trading
    )
    preflight_summary: dict[str, object] = {
        "required": preflight_required,
        "rollout_stage": rollout_stage_name,
        "stage_enabled": stage_enabled,
        "real_order_submission": real_order_submission,
        "allow_real_trading": allow_real_trading,
        "required_env_vars": list(execution_adapter.required_env_vars),
        "max_secret_age_days": execution_adapter.max_secret_age_days,
        "preferred_secret_sources": list(execution_adapter.preferred_secret_sources),
        "enforce_auth_healthcheck": execution_adapter.enforce_auth_healthcheck,
        "allow_l1_auth_requests": execution_adapter.allow_l1_auth_requests,
        "l1_auth_guard": dict(l1_auth_guard),
        "auth_healthcheck": {
            "required": execution_adapter.enforce_auth_healthcheck,
            "status": "skipped",
            "reason": "auth_healthcheck_not_required",
        },
        "status": "skipped",
    }
    l1_auth_requested = bool(l1_auth_guard.get("requested", False))
    l1_auth_allowed = bool(l1_auth_guard.get("allowed", False))
    if l1_auth_requested and not l1_auth_allowed:
        raise ValueError(
            "Live credential preflight failed: "
            "reasons=['l1_auth_policy_violation'] "
            f"l1_auth_guard={l1_auth_guard}"
        )
    if not preflight_required:
        preflight_summary["skip_reason"] = (
            "live_trading_not_enabled_for_stage_or_flags"
        )
        if l1_auth_requested and l1_auth_allowed:
            preflight_summary["status"] = "passed"
        return preflight_summary

    missing_env_vars = execution_adapter._missing_required_env_vars()
    if missing_env_vars:
        raise ValueError(
            "Live credential preflight failed: "
            "missing_polymarket_credentials "
            f"missing_env_vars={missing_env_vars}"
        )

    secret_reasons, secret_metadata = execution_adapter._validate_secret_controls()
    if secret_reasons:
        preflight_details = {
            "secret_source_metadata_missing": secret_metadata.get(
                "secret_source_metadata_missing", []
            ),
            "secret_rotation_metadata_missing": secret_metadata.get(
                "secret_rotation_metadata_missing", []
            ),
            "stale_secrets": secret_metadata.get("stale_secrets", []),
            "plaintext_secret_source_disallowed": secret_metadata.get(
                "plaintext_secret_source_disallowed", []
            ),
            "invalid_secret_sources": secret_metadata.get(
                "invalid_secret_sources", []
            ),
            "max_secret_age_days": secret_metadata.get("max_secret_age_days"),
            "preferred_secret_sources": secret_metadata.get(
                "preferred_secret_sources", []
            ),
        }
        raise ValueError(
            "Live credential preflight failed: "
            f"reasons={secret_reasons} details={preflight_details}"
        )
    if execution_adapter.enforce_auth_healthcheck:
        auth_reasons, auth_metadata = execution_adapter.run_auth_healthcheck(
            force=True
        )
        preflight_summary["auth_healthcheck"] = auth_metadata
        if auth_reasons:
            raise ValueError(
                "Live credential preflight failed: "
                "reasons=['auth_healthcheck_failed'] "
                f"auth_reasons={auth_reasons} details={auth_metadata}"
            )

    preflight_summary["status"] = "passed"
    return preflight_summary


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run Poly-Robot test-token loop under C1 runtime supervision "
            "(heartbeat, bounded retries, and restart-safe state snapshots)."
        )
    )
    parser.add_argument(
        "--events",
        type=Path,
        required=False,
        help=(
            "Path to replay event JSONL file (required when "
            "--ingestion-mode=historical_jsonl)."
        ),
    )
    parser.add_argument(
        "--profile",
        type=Path,
        default=ROOT_DIR
        / "config"
        / "parameters"
        / "profiles"
        / "mvp_test_token.v1.json",
        help="Path to parameter profile JSON.",
    )
    parser.add_argument(
        "--calibration-policy",
        type=Path,
        default=ROOT_DIR / "config" / "calibration" / "llm_reliability.v1.json",
        help="Path to calibration reliability policy JSON.",
    )
    parser.add_argument(
        "--scenario-pack",
        type=Path,
        default=ROOT_DIR / "config" / "replay" / "scenario_pack.v1.json",
        help="Path to replay scenario pack JSON.",
    )
    parser.add_argument(
        "--scenario",
        type=str,
        required=False,
        help="Scenario name from scenario pack; defaults to scenario-pack default.",
    )
    parser.add_argument(
        "--bankroll",
        type=float,
        default=1000.0,
        help="Initial bankroll used in replay simulation.",
    )
    parser.add_argument(
        "--cycles",
        type=int,
        default=3,
        help="Number of supervision cycles to execute.",
    )
    parser.add_argument(
        "--cycle-interval-seconds",
        type=float,
        default=0.0,
        help=(
            "Optional delay between cycles to support real-time ingestion pacing."
        ),
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=2,
        help="Maximum number of retries per worker after initial failure.",
    )
    parser.add_argument(
        "--retry-backoff-seconds",
        type=float,
        default=1.0,
        help="Base retry backoff in seconds (exponential per attempt).",
    )
    parser.add_argument(
        "--heartbeat-timeout-seconds",
        type=float,
        default=30.0,
        help="Maximum allowed time since last heartbeat before marking worker failed.",
    )
    parser.add_argument(
        "--continue-on-failure",
        action="store_true",
        help="Continue through all requested cycles even if a cycle fails.",
    )
    parser.add_argument(
        "--journal-path",
        type=Path,
        default=ROOT_DIR / "runtime" / "runtime_journal.jsonl",
        help="JSONL path for runtime journal events.",
    )
    parser.add_argument(
        "--state-path",
        type=Path,
        default=ROOT_DIR / "runtime" / "runtime_state.json",
        help="JSON path for latest runtime snapshot state.",
    )
    parser.add_argument(
        "--cycle-output-dir",
        type=Path,
        required=False,
        help="Optional directory to persist per-cycle test-token loop outputs.",
    )
    parser.add_argument(
        "--control-state-path",
        type=Path,
        default=ROOT_DIR / "runtime" / "operator_control_state.json",
        help="Path to persisted operator control state JSON.",
    )
    parser.add_argument(
        "--control-audit-path",
        type=Path,
        default=ROOT_DIR / "runtime" / "operator_action_audit.jsonl",
        help="Path to operator action audit JSONL log.",
    )
    parser.add_argument(
        "--agent-operator-learning-state-path",
        type=Path,
        required=False,
        help=(
            "Optional path to AgentOperator learning state JSON. "
            "Defaults to sibling of --control-state-path when omitted."
        ),
    )
    parser.add_argument(
        "--agent-operator-learning-audit-path",
        type=Path,
        required=False,
        help=(
            "Optional path to AgentOperator learning audit JSONL log. "
            "Defaults to sibling of --control-state-path when omitted."
        ),
    )
    parser.add_argument(
        "--operator-control-actor",
        type=str,
        default="runtime_supervisor",
        help="Actor identity used when runtime acknowledges control actions.",
    )
    parser.add_argument(
        "--ignore-operator-controls",
        action="store_true",
        help="Ignore operator control state and run using CLI scenario only.",
    )
    parser.add_argument(
        "--ingestion-mode",
        type=str,
        choices=["historical_jsonl", "live_polymarket"],
        default="historical_jsonl",
        help="Select ingestion source mode.",
    )
    parser.add_argument(
        "--live-source-url",
        type=str,
        default=(
            "https://gamma-api.polymarket.com/markets"
            "?active=true&closed=false&limit=50"
        ),
        help="Polymarket Gamma source URL used in live ingestion mode.",
    )
    parser.add_argument(
        "--live-max-markets",
        type=int,
        default=10,
        help="Maximum number of live markets to convert into cycle events.",
    )
    parser.add_argument(
        "--live-min-volume-24h",
        type=float,
        default=0.0,
        help="Minimum 24h volume required for a live market to be ingested.",
    )
    parser.add_argument(
        "--live-wallet-convergence-path",
        type=Path,
        required=False,
        help=(
            "Optional JSON path providing wallet convergence counts keyed by "
            "market ID for live whale-signal enrichment."
        ),
    )
    parser.add_argument(
        "--live-wallet-convergence-threshold",
        type=float,
        default=3.0,
        help=(
            "Minimum wallet convergence count required to trigger the live "
            "whale check."
        ),
    )
    parser.add_argument(
        "--disable-live-freshness-filter",
        action="store_true",
        help=(
            "Disable live-event freshness filtering that skips previously "
            "seen event IDs across cycles."
        ),
    )
    parser.add_argument(
        "--state-refresh-stale-threshold-cycles",
        type=int,
        default=6,
        help=(
            "Number of consecutive state-refresh cycles with open positions "
            "before markets are flagged as stale."
        ),
    )
    parser.add_argument(
        "--ingestion-degraded-entry-suppress-threshold-cycles",
        type=int,
        default=3,
        help=(
            "Number of consecutive DEGRADED ingestion cycles that triggers "
            "new-entry suppression."
        ),
    )
    parser.add_argument(
        "--ingestion-max-retries",
        type=int,
        default=1,
        help="Maximum retries for ingestion file read failures/timeouts.",
    )
    parser.add_argument(
        "--ingestion-retry-backoff-seconds",
        type=float,
        default=0.25,
        help="Base retry backoff for ingestion retries.",
    )
    parser.add_argument(
        "--ingestion-timeout-seconds",
        type=float,
        default=5.0,
        help="Maximum ingestion wall-clock budget in seconds.",
    )
    parser.add_argument(
        "--ingestion-max-invalid-rows",
        type=int,
        default=0,
        help="Maximum tolerated invalid event rows before ingestion fails.",
    )
    parser.add_argument(
        "--execution-mode",
        type=str,
        choices=["paper", "test_polymarket_clob", "live_polymarket_clob"],
        required=False,
        help=(
            "Execution adapter mode; defaults to rollout config "
            "default_execution_mode when omitted."
        ),
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
        "--mode-lifecycle-mode",
        type=str,
        choices=["paper", "test", "live"],
        required=False,
        help=(
            "Optional lifecycle mode override. When omitted, defaults to "
            "the policy default mode or the resolved execution mode mapping."
        ),
    )
    parser.add_argument(
        "--disable-testnet-parity",
        action="store_true",
        help=(
            "Force test-mode execution to use fallback environment semantics "
            "instead of testnet parity."
        ),
    )
    parser.add_argument(
        "--live-rollout-config",
        type=Path,
        default=ROOT_DIR / "config" / "integration" / "live_trade_rollout.v1.json",
        help="Path to live-trading rollout controls JSON.",
    )
    parser.add_argument(
        "--polymarket-clob-config",
        type=Path,
        default=ROOT_DIR / "config" / "integration" / "polymarket_clob_live.v1.json",
        help="Path to Polymarket CLOB integration JSON.",
    )
    parser.add_argument(
        "--live-rollout-stage",
        type=str,
        required=False,
        help=(
            "Optional rollout stage override for test_polymarket_clob/live_polymarket_clob "
            "execution mode."
        ),
    )
    parser.add_argument(
        "--execution-adapter-audit-path",
        type=Path,
        required=False,
        help=(
            "Optional JSONL path where execution adapter order lifecycle "
            "events are appended."
        ),
    )
    parser.add_argument(
        "--pre-trade-balance-check-enabled",
        action="store_true",
        help="Require per-intent balance checks before live order submission.",
    )
    parser.add_argument(
        "--pre-trade-allowance-check-enabled",
        action="store_true",
        help="Require per-intent allowance checks before live order submission.",
    )
    parser.add_argument(
        "--require-market-token-id",
        action="store_true",
        help="Require token_id metadata on each execution intent.",
    )
    parser.add_argument(
        "--require-market-tick-size",
        action="store_true",
        help="Require tick_size metadata on each execution intent.",
    )
    parser.add_argument(
        "--require-market-neg-risk",
        action="store_true",
        help="Require neg_risk metadata on each execution intent.",
    )
    parser.add_argument(
        "--max-order-notional-usd",
        type=float,
        required=False,
        help=(
            "Optional per-order notional cap in USD for live execution."
        ),
    )
    parser.add_argument(
        "--max-daily-notional-usd",
        type=float,
        required=False,
        help=(
            "Optional cumulative daily notional cap in USD for live execution."
        ),
    )
    parser.add_argument(
        "--max-open-orders",
        type=int,
        required=False,
        help="Optional cap on concurrently open live orders.",
    )
    parser.add_argument(
        "--reconciliation-heartbeat-timeout-seconds",
        type=float,
        required=False,
        help=(
            "Optional timeout in seconds for user-channel heartbeat "
            "freshness checks."
        ),
    )
    parser.add_argument(
        "--enforce-user-channel-heartbeat",
        action="store_true",
        help="Require fresh user-channel heartbeat before submitting orders.",
    )
    parser.add_argument(
        "--enforce-user-channel-ack",
        action="store_true",
        help="Require user-channel acknowledgement after order submission.",
    )
    parser.add_argument(
        "--allowed-secret-sources",
        nargs="+",
        required=False,
        help=(
            "Optional list of allowed secret source identifiers "
            "(e.g. vault, keychain)."
        ),
    )
    parser.add_argument(
        "--secret-max-age-seconds",
        type=float,
        required=False,
        help="Optional maximum allowed age in seconds for loaded credentials.",
    )
    parser.add_argument(
        "--allow-real-trading",
        action="store_true",
        help=(
            "Explicitly allow live-trading execution mode after rollout and "
            "credential gates are satisfied."
        ),
    )
    parser.add_argument(
        "--l1-auth-operation",
        type=str,
        choices=["none", "derive_api_key", "create_api_key"],
        default="none",
        help=(
            "Optional L1 auth operation intent. Restricted to operator-controlled "
            "startup/restart/emergency contexts."
        ),
    )
    parser.add_argument(
        "--l1-auth-context",
        type=str,
        choices=["startup", "restart", "emergency"],
        required=False,
        help=(
            "Context for --l1-auth-operation. restart/emergency require "
            "operator-control state evidence."
        ),
    )
    parser.add_argument(
        "--execution-gateway-max-retries",
        type=int,
        default=1,
        help="Maximum retries for execution gateway failures/timeouts.",
    )
    parser.add_argument(
        "--execution-gateway-retry-backoff-seconds",
        type=float,
        default=0.25,
        help="Base retry backoff for execution gateway retries.",
    )
    parser.add_argument(
        "--execution-gateway-timeout-seconds",
        type=float,
        default=2.0,
        help="Execution gateway timeout budget in seconds.",
    )
    parser.add_argument(
        "--agent-operator-enabled",
        action="store_true",
        help=(
            "Enable parallel AgentOperator advisory inference for profitability "
            "guidance per cycle."
        ),
    )
    parser.add_argument(
        "--agent-operator-model",
        type=str,
        default="claude-sonnet-4-6",
        help="Claude advisory model identifier used by AgentOperator inference.",
    )
    parser.add_argument(
        "--agent-operator-strategy-model",
        type=str,
        default="claude-opus-4-7",
        help=(
            "Claude strategy model identifier used by AgentOperator when mode=strategy."
        ),
    )
    parser.add_argument(
        "--agent-operator-endpoint-url",
        type=str,
        default="https://api.anthropic.com/v1/messages",
        help="Claude API endpoint URL used by AgentOperator.",
    )
    parser.add_argument(
        "--agent-operator-api-key-env",
        type=str,
        default="ANTHROPIC_API_KEY",
        help="Environment variable name containing Claude API key.",
    )
    parser.add_argument(
        "--agent-operator-timeout-seconds",
        type=float,
        default=8.0,
        help="Timeout budget for AgentOperator inference request.",
    )
    parser.add_argument(
        "--agent-operator-max-output-tokens",
        type=int,
        default=500,
        help="Maximum tokens requested for AgentOperator response.",
    )
    parser.add_argument(
        "--agent-operator-temperature",
        type=float,
        default=0.1,
        help="Sampling temperature for AgentOperator inference.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    if args.cycle_interval_seconds < 0:
        raise ValueError("--cycle-interval-seconds must be >= 0")
    if args.live_wallet_convergence_threshold <= 0:
        raise ValueError("--live-wallet-convergence-threshold must be > 0")
    if args.state_refresh_stale_threshold_cycles <= 0:
        raise ValueError("--state-refresh-stale-threshold-cycles must be > 0")
    if args.ingestion_degraded_entry_suppress_threshold_cycles <= 0:
        raise ValueError(
            "--ingestion-degraded-entry-suppress-threshold-cycles must be > 0"
        )
    if args.agent_operator_timeout_seconds <= 0:
        raise ValueError("--agent-operator-timeout-seconds must be > 0")
    if args.agent_operator_max_output_tokens <= 0:
        raise ValueError("--agent-operator-max-output-tokens must be > 0")
    if args.agent_operator_temperature < 0:
        raise ValueError("--agent-operator-temperature must be >= 0")
    if args.ingestion_mode == "historical_jsonl" and args.events is None:
        raise ValueError(
            "--events is required when --ingestion-mode=historical_jsonl"
        )
    if args.ingestion_mode == "historical_jsonl" and args.events is not None:
        args.events = _prepare_sorted_historical_events(args.events)
    profile_payload, parameters = _load_profile_payload(args.profile)
    calibration_policy_payload = _load_json(args.calibration_policy)
    calibration_policy = load_calibration_policy(args.calibration_policy)
    scenario_pack = None
    default_scenario = None
    if args.ingestion_mode == "historical_jsonl":
        scenario_pack = load_scenario_pack(args.scenario_pack)
        default_scenario = scenario_pack.get_scenario(args.scenario)
    control_default_scenario_name = (
        default_scenario.name
        if default_scenario is not None
        else "live_polymarket"
    )

    historical_ingestion = None
    events: list[MarketEvent] = []
    live_ingestion_adapter: LivePolymarketIngestionAdapter | None = None
    if args.ingestion_mode == "historical_jsonl":
        ingestion_adapter = HistoricalIngestionAdapter(
            max_retry_attempts=args.ingestion_max_retries,
            retry_backoff_seconds=args.ingestion_retry_backoff_seconds,
            max_invalid_rows=args.ingestion_max_invalid_rows,
            deduplicate_event_ids=True,
            fail_on_monotonic_violation=False,
        )
        historical_ingestion = ingestion_adapter.load_jsonl(
            args.events,
            timeout_seconds=args.ingestion_timeout_seconds,
        )
        if historical_ingestion.status == "FAILED":
            raise ValueError(
                "Ingestion adapter failed: "
                "reasons="
                f"{list(historical_ingestion.reasons)} "
                f"metadata={historical_ingestion.metadata}"
            )
        events = historical_ingestion.events
    else:
        wallet_convergence_loader = None
        if args.live_wallet_convergence_path is not None:
            wallet_convergence_path = args.live_wallet_convergence_path

            def wallet_convergence_loader() -> dict[str, float]:
                return _load_wallet_convergence_payload(wallet_convergence_path)
        live_ingestion_adapter = LivePolymarketIngestionAdapter(
            source_url=args.live_source_url,
            max_markets=args.live_max_markets,
            min_volume_24h=args.live_min_volume_24h,
            max_retry_attempts=args.ingestion_max_retries,
            retry_backoff_seconds=args.ingestion_retry_backoff_seconds,
            max_invalid_rows=args.ingestion_max_invalid_rows,
            deduplicate_event_ids=True,
            whale_signal_wallet_threshold=args.live_wallet_convergence_threshold,
            wallet_convergence_loader=wallet_convergence_loader,
        )
    mode_lifecycle_policy_payload = resolve_mode_lifecycle_policy(None)
    if args.mode_lifecycle_policy.exists():
        raw_mode_lifecycle_policy_payload = _load_json(args.mode_lifecycle_policy)
        if not isinstance(raw_mode_lifecycle_policy_payload, dict):
            raise ValueError(
                "Mode lifecycle policy must be a JSON object "
                f"({args.mode_lifecycle_policy})"
            )
        mode_lifecycle_policy_payload = resolve_mode_lifecycle_policy(
            raw_mode_lifecycle_policy_payload
        )
    mode_lifecycle_policy_hash = stable_hash(mode_lifecycle_policy_payload)
    mode_lifecycle_default_mode = normalize_lifecycle_mode(
        mode_lifecycle_policy_payload.get("default_mode", "paper")
    )

    control_manager = OperatorControlManager(
        control_state_path=args.control_state_path,
        audit_path=args.control_audit_path,
        mode_lifecycle_policy_path=args.mode_lifecycle_policy,
        agent_operator_learning_state_path=args.agent_operator_learning_state_path,
        agent_operator_learning_audit_path=args.agent_operator_learning_audit_path,
    )

    strategy = BaselineStrategy(parameters, calibration_policy)
    risk = RiskEngine(parameters)
    rollout_payload = _load_json(args.live_rollout_config)
    rollout_default_execution_mode = str(
        rollout_payload.get(
            "default_execution_mode",
            _execution_mode_for_lifecycle_mode(mode_lifecycle_default_mode),
        )
    ).strip().lower() or _execution_mode_for_lifecycle_mode(mode_lifecycle_default_mode)
    if rollout_default_execution_mode not in LIFECYCLE_MODE_BY_EXECUTION_MODE:
        rollout_default_execution_mode = _execution_mode_for_lifecycle_mode(
            mode_lifecycle_default_mode
        )

    execution_mode_override = str(args.execution_mode or "").strip().lower() or None
    lifecycle_mode_override = (
        normalize_lifecycle_mode(args.mode_lifecycle_mode)
        if args.mode_lifecycle_mode is not None
        else None
    )
    if (
        execution_mode_override is not None
        and lifecycle_mode_override is not None
        and _lifecycle_mode_for_execution_mode(execution_mode_override)
        != lifecycle_mode_override
    ):
        raise ValueError(
            "Execution mode override does not match lifecycle mode override "
            f"(execution_mode={execution_mode_override!r}, "
            f"lifecycle_mode={lifecycle_mode_override!r})"
        )

    if execution_mode_override is not None:
        resolved_execution_mode = execution_mode_override
        resolved_lifecycle_mode = _lifecycle_mode_for_execution_mode(
            resolved_execution_mode
        )
    elif lifecycle_mode_override is not None:
        resolved_lifecycle_mode = lifecycle_mode_override
        resolved_execution_mode = _execution_mode_for_lifecycle_mode(
            resolved_lifecycle_mode
        )
    else:
        resolved_execution_mode = rollout_default_execution_mode
        resolved_lifecycle_mode = _lifecycle_mode_for_execution_mode(
            resolved_execution_mode
        )
    l1_auth_guard = _resolve_l1_auth_guard(
        operation=args.l1_auth_operation,
        context=args.l1_auth_context,
        operator_actor=args.operator_control_actor,
        control_manager=control_manager,
        control_state_path=args.control_state_path,
        ignore_operator_controls=bool(args.ignore_operator_controls),
    )
    if bool(l1_auth_guard.get("requested", False)) and not bool(
        l1_auth_guard.get("allowed", False)
    ):
        raise ValueError(
            "L1 auth operation denied by runtime policy: "
            f"operation={l1_auth_guard.get('operation')} "
            f"context={l1_auth_guard.get('context')} "
            f"reason_codes={l1_auth_guard.get('reason_codes', [])}"
        )

    execution_context: dict[str, object]
    if resolved_execution_mode == "paper":
        execution_adapter = PaperExecutionAdapter(parameters)
        execution_context = {
            "mode": "paper",
            "lifecycle_mode": resolved_lifecycle_mode,
            "mode_lifecycle_policy_path": str(args.mode_lifecycle_policy),
            "mode_lifecycle_policy_hash": mode_lifecycle_policy_hash,
            "rollout_config_path": str(args.live_rollout_config),
            "rollout_stage": "paper",
            "rollout_stage_enabled": True,
            "real_order_submission": False,
            "allow_real_trading": False,
            "required_env_vars": [],
            "clob_base_url": None,
            "clob_config_path": None,
            "test_mode_environment": None,
            "test_mode_environment_fallback_used": False,
            "test_mode_environment_reason_code": "",
            "l1_auth_guard": dict(l1_auth_guard),
            "credential_preflight": {
                "required": False,
                "status": "skipped",
                "skip_reason": "paper_execution_mode",
            },
        }
    else:
        clob_config_payload = _load_json(args.polymarket_clob_config)
        endpoints = clob_config_payload.get("endpoints")
        if not isinstance(endpoints, dict):
            raise ValueError(
                "Polymarket CLOB config must include endpoints object "
                f"({args.polymarket_clob_config})"
            )
        clob_base_url = str(endpoints.get("clob_rest_base_url", "")).strip()
        if not clob_base_url:
            raise ValueError(
                "Polymarket CLOB config must include endpoints.clob_rest_base_url"
            )
        default_rollout_stage_override = (
            "canary_live"
            if resolved_execution_mode == "test_polymarket_clob"
            else None
        )
        rollout_stage_name, rollout_stage_payload = _resolve_rollout_stage(
            rollout_payload,
            requested_stage=args.live_rollout_stage or default_rollout_stage_override,
        )
        global_guards = rollout_payload.get("global_guards")
        secrets_policy = rollout_payload.get("secrets_policy")
        order_rules = clob_config_payload.get("order_rules")
        required_env_vars: tuple[str, ...] = ()
        allow_plaintext_secrets = False
        preferred_secret_sources: tuple[str, ...] = ()
        secret_max_age_days = 90
        if isinstance(secrets_policy, dict):
            raw_required_env_vars = secrets_policy.get("required_env_vars")
            if isinstance(raw_required_env_vars, list):
                required_env_vars = tuple(
                    env_var
                    for env_var in (
                        str(raw_name).strip() for raw_name in raw_required_env_vars
                    )
                    if env_var
                )
            allow_plaintext_secrets = bool(
                secrets_policy.get("allow_plaintext_secrets", False)
            )
            raw_preferred_sources = secrets_policy.get("preferred_secret_sources")
            if isinstance(raw_preferred_sources, list):
                preferred_secret_sources = tuple(
                    source
                    for source in (
                        str(raw_source).strip().lower()
                        for raw_source in raw_preferred_sources
                    )
                    if source
                )
            raw_secret_max_age_days = secrets_policy.get("max_secret_age_days")
            parsed_secret_max_age_days = _as_optional_positive_int(
                raw_secret_max_age_days
            )
            if parsed_secret_max_age_days is not None:
                secret_max_age_days = parsed_secret_max_age_days
        if args.allowed_secret_sources:
            preferred_secret_sources = tuple(
                source
                for source in (
                    str(raw_source).strip().lower()
                    for raw_source in args.allowed_secret_sources
                )
                if source
            )
        parsed_secret_max_age_seconds = _as_optional_positive_float(
            args.secret_max_age_seconds
        )
        if parsed_secret_max_age_seconds is not None:
            secret_max_age_days = _secret_max_age_days_from_seconds(
                parsed_secret_max_age_seconds
            )

        required_market_metadata_from_order_rules: set[str] = set()
        default_user_channel_staleness_seconds: float | None = None
        if isinstance(order_rules, dict):
            raw_required_market_metadata = order_rules.get("required_market_metadata")
            if isinstance(raw_required_market_metadata, list):
                required_market_metadata_from_order_rules = {
                    metadata_key
                    for metadata_key in (
                        str(raw_key).strip().lower()
                        for raw_key in raw_required_market_metadata
                    )
                    if metadata_key
                }
            user_channel_heartbeat = order_rules.get("user_channel_heartbeat")
            if isinstance(user_channel_heartbeat, dict):
                ping_interval_seconds = _as_optional_positive_float(
                    user_channel_heartbeat.get("ping_interval_seconds")
                )
                if ping_interval_seconds is not None:
                    default_user_channel_staleness_seconds = (
                        ping_interval_seconds * 3.0
                    )

        stage_enabled = bool(rollout_stage_payload.get("enabled", False))
        real_order_submission = bool(
            rollout_stage_payload.get("real_order_submission", False)
        )
        require_pretrade_balance_checks = bool(
            rollout_stage_payload.get("require_pretrade_balance_checks", False)
        )
        require_user_channel_trade_ack = bool(
            rollout_stage_payload.get("require_user_channel_trade_ack", False)
        )
        require_kill_switch = bool(
            rollout_stage_payload.get("require_kill_switch", False)
        )
        enforce_auth_healthcheck = bool(
            rollout_stage_payload.get("enforce_auth_healthcheck", False)
        )
        enable_geoblock_check = bool(
            rollout_stage_payload.get("enable_geoblock_check", False)
        )
        geoblock_url = str(rollout_stage_payload.get("geoblock_url", "")).strip()
        auth_healthcheck_timeout_seconds = (
            _as_optional_positive_float(
                rollout_stage_payload.get("auth_healthcheck_timeout_seconds")
            )
            or 2.0
        )
        auth_healthcheck_ttl_seconds = (
            _as_optional_positive_float(
                rollout_stage_payload.get("auth_healthcheck_ttl_seconds")
            )
            or 30.0
        )
        auth_healthcheck_max_time_skew_seconds = (
            _as_optional_positive_float(
                rollout_stage_payload.get(
                    "auth_healthcheck_max_time_skew_seconds"
                )
            )
            or 30.0
        )
        if isinstance(global_guards, dict):
            if bool(
                global_guards.get("require_pretrade_balance_and_allowance_checks", False)
            ):
                require_pretrade_balance_checks = True
            if bool(global_guards.get("require_user_channel_trade_ack", False)):
                require_user_channel_trade_ack = True
            if bool(global_guards.get("require_kill_switch", False)):
                require_kill_switch = True
            if bool(global_guards.get("disable_live_trading_on_auth_failure", False)):
                enforce_auth_healthcheck = True
            if bool(global_guards.get("enable_geoblock_check", False)) or bool(
                global_guards.get("require_geoblock_precheck", False)
            ):
                enable_geoblock_check = True
            global_geoblock_url = str(global_guards.get("geoblock_url", "")).strip()
            if global_geoblock_url:
                geoblock_url = global_geoblock_url
            parsed_global_auth_healthcheck_timeout_seconds = (
                _as_optional_positive_float(
                    global_guards.get("auth_healthcheck_timeout_seconds")
                )
            )
            if parsed_global_auth_healthcheck_timeout_seconds is not None:
                auth_healthcheck_timeout_seconds = (
                    parsed_global_auth_healthcheck_timeout_seconds
                )
            parsed_global_auth_healthcheck_ttl_seconds = (
                _as_optional_positive_float(
                    global_guards.get("auth_healthcheck_ttl_seconds")
                )
            )
            if parsed_global_auth_healthcheck_ttl_seconds is not None:
                auth_healthcheck_ttl_seconds = (
                    parsed_global_auth_healthcheck_ttl_seconds
                )
            parsed_global_auth_healthcheck_max_time_skew_seconds = (
                _as_optional_positive_float(
                    global_guards.get(
                        "auth_healthcheck_max_time_skew_seconds"
                    )
                )
            )
            if parsed_global_auth_healthcheck_max_time_skew_seconds is not None:
                auth_healthcheck_max_time_skew_seconds = (
                    parsed_global_auth_healthcheck_max_time_skew_seconds
                )
        if not geoblock_url:
            geoblock_url = "https://polymarket.com/api/geoblock"
        if args.pre_trade_balance_check_enabled or args.pre_trade_allowance_check_enabled:
            require_pretrade_balance_checks = True
        if args.enforce_user_channel_ack:
            require_user_channel_trade_ack = True
        if args.enforce_user_channel_heartbeat:
            require_user_channel_trade_ack = True

        required_market_metadata = set(required_market_metadata_from_order_rules)
        if bool(rollout_stage_payload.get("require_market_token_id", False)):
            required_market_metadata.add("token_id")
        if bool(rollout_stage_payload.get("require_market_tick_size", False)):
            required_market_metadata.add("tick_size")
        if bool(rollout_stage_payload.get("require_market_neg_risk", False)):
            required_market_metadata.add("neg_risk")
        if args.require_market_token_id:
            required_market_metadata.add("token_id")
        if args.require_market_tick_size:
            required_market_metadata.add("tick_size")
        if args.require_market_neg_risk:
            required_market_metadata.add("neg_risk")
        ordered_required_market_metadata = tuple(
            metadata_key
            for metadata_key in ("token_id", "tick_size", "neg_risk")
            if metadata_key in required_market_metadata
        )

        max_order_notional_usd = _as_optional_positive_float(args.max_order_notional_usd)
        if max_order_notional_usd is None:
            max_order_notional_usd = _as_optional_positive_float(
                rollout_stage_payload.get("max_order_notional_usd")
            )
        max_daily_notional_usd = _as_optional_positive_float(args.max_daily_notional_usd)
        if max_daily_notional_usd is None:
            max_daily_notional_usd = _as_optional_positive_float(
                rollout_stage_payload.get("max_daily_notional_usd")
            )
        max_open_orders = _as_optional_positive_int(args.max_open_orders)
        if max_open_orders is None:
            max_open_orders = _as_optional_positive_int(
                rollout_stage_payload.get("max_open_orders")
            )

        user_channel_max_staleness_seconds = _as_optional_positive_float(
            args.reconciliation_heartbeat_timeout_seconds
        )
        if user_channel_max_staleness_seconds is None:
            user_channel_max_staleness_seconds = _as_optional_positive_float(
                rollout_stage_payload.get("user_channel_max_staleness_seconds")
            )
        if user_channel_max_staleness_seconds is None:
            user_channel_max_staleness_seconds = (
                default_user_channel_staleness_seconds or 30.0
            )

        execution_adapter_audit_path = args.execution_adapter_audit_path
        if execution_adapter_audit_path is None:
            raw_stage_audit_path = rollout_stage_payload.get("execution_audit_path")
            raw_global_audit_path = rollout_payload.get("execution_audit_path")
            raw_audit_path = (
                raw_stage_audit_path
                if isinstance(raw_stage_audit_path, str)
                else raw_global_audit_path
            )
            if isinstance(raw_audit_path, str) and raw_audit_path.strip():
                execution_adapter_audit_path = Path(raw_audit_path.strip())

        test_mode_environment = (
            select_test_mode_environment(
                policy=mode_lifecycle_policy_payload,
                testnet_parity_supported=not bool(args.disable_testnet_parity),
            )
            if resolved_execution_mode == "test_polymarket_clob"
            else {
                "selected_environment": "",
                "fallback_used": False,
                "reason_code": "",
                "primary_environment": "",
                "fallback_environment": "",
            }
        )

        execution_adapter = PolymarketClobExecutionAdapter(
            clob_base_url=clob_base_url,
            rollout_stage=rollout_stage_name,
            stage_enabled=stage_enabled,
            real_order_submission=real_order_submission,
            allow_real_trading=bool(args.allow_real_trading),
            required_env_vars=required_env_vars,
            max_order_notional_usd=max_order_notional_usd,
            max_daily_notional_usd=max_daily_notional_usd,
            max_open_orders=max_open_orders,
            required_market_metadata=ordered_required_market_metadata,
            require_pretrade_balance_checks=require_pretrade_balance_checks,
            require_user_channel_trade_ack=require_user_channel_trade_ack,
            require_kill_switch=require_kill_switch,
            allow_plaintext_secrets=allow_plaintext_secrets,
            preferred_secret_sources=preferred_secret_sources,
            max_secret_age_days=secret_max_age_days,
            user_channel_max_staleness_seconds=user_channel_max_staleness_seconds,
            enforce_auth_healthcheck=enforce_auth_healthcheck,
            enable_geoblock_check=enable_geoblock_check,
            geoblock_url=geoblock_url,
            auth_healthcheck_timeout_seconds=auth_healthcheck_timeout_seconds,
            auth_healthcheck_ttl_seconds=auth_healthcheck_ttl_seconds,
            auth_healthcheck_max_time_skew_seconds=(
                auth_healthcheck_max_time_skew_seconds
            ),
            allow_l1_auth_requests=bool(l1_auth_guard.get("allowed", False)),
            audit_log_path=execution_adapter_audit_path,
        )
        credential_preflight = _run_live_credential_preflight(
            execution_adapter=execution_adapter,
            rollout_stage_name=rollout_stage_name,
            stage_enabled=stage_enabled,
            real_order_submission=real_order_submission,
            allow_real_trading=bool(args.allow_real_trading),
            l1_auth_guard=l1_auth_guard,
        )
        execution_context = {
            "mode": resolved_execution_mode,
            "lifecycle_mode": resolved_lifecycle_mode,
            "mode_lifecycle_policy_path": str(args.mode_lifecycle_policy),
            "mode_lifecycle_policy_hash": mode_lifecycle_policy_hash,
            "rollout_config_path": str(args.live_rollout_config),
            "rollout_stage": rollout_stage_name,
            "rollout_stage_enabled": stage_enabled,
            "real_order_submission": real_order_submission,
            "allow_real_trading": bool(args.allow_real_trading),
            "required_env_vars": list(required_env_vars),
            "clob_base_url": clob_base_url,
            "clob_config_path": str(args.polymarket_clob_config),
            "max_order_notional_usd": max_order_notional_usd,
            "max_daily_notional_usd": max_daily_notional_usd,
            "max_open_orders": max_open_orders,
            "required_market_metadata": list(ordered_required_market_metadata),
            "require_pretrade_balance_checks": require_pretrade_balance_checks,
            "require_user_channel_trade_ack": require_user_channel_trade_ack,
            "require_kill_switch": require_kill_switch,
            "enforce_auth_healthcheck": enforce_auth_healthcheck,
            "enable_geoblock_check": enable_geoblock_check,
            "geoblock_url": geoblock_url,
            "auth_healthcheck_timeout_seconds": auth_healthcheck_timeout_seconds,
            "auth_healthcheck_ttl_seconds": auth_healthcheck_ttl_seconds,
            "auth_healthcheck_max_time_skew_seconds": (
                auth_healthcheck_max_time_skew_seconds
            ),
            "allow_plaintext_secrets": allow_plaintext_secrets,
            "preferred_secret_sources": list(preferred_secret_sources),
            "max_secret_age_days": secret_max_age_days,
            "user_channel_max_staleness_seconds": user_channel_max_staleness_seconds,
            "test_mode_environment": test_mode_environment.get("selected_environment"),
            "test_mode_environment_fallback_used": bool(
                test_mode_environment.get("fallback_used", False)
            ),
            "test_mode_environment_reason_code": str(
                test_mode_environment.get("reason_code", "")
            ),
            "test_mode_environment_primary": test_mode_environment.get(
                "primary_environment"
            ),
            "test_mode_environment_fallback": test_mode_environment.get(
                "fallback_environment"
            ),
            "l1_auth_guard": dict(l1_auth_guard),
            "execution_adapter_audit_path": (
                str(execution_adapter_audit_path)
                if execution_adapter_audit_path is not None
                else None
            ),
            "credential_preflight": credential_preflight,
        }
    execution = HardenedExecutionAdapter(
        execution_adapter,
        gateway_max_retry_attempts=args.execution_gateway_max_retries,
        gateway_retry_backoff_seconds=args.execution_gateway_retry_backoff_seconds,
        gateway_timeout_seconds=args.execution_gateway_timeout_seconds,
    )
    strategy_model = (
        str(args.agent_operator_strategy_model).strip() or args.agent_operator_model
    )
    agent_operators_by_mode: dict[str, AgentOperator] = {
        "advisory": AgentOperator(
            client=ClaudeApiClient(
                model=args.agent_operator_model,
                endpoint_url=args.agent_operator_endpoint_url,
                api_key_env=args.agent_operator_api_key_env,
                max_output_tokens=args.agent_operator_max_output_tokens,
                temperature=args.agent_operator_temperature,
            ),
            timeout_seconds=args.agent_operator_timeout_seconds,
            enabled=True,
        ),
        "strategy": AgentOperator(
            client=ClaudeApiClient(
                model=strategy_model,
                endpoint_url=args.agent_operator_endpoint_url,
                api_key_env=args.agent_operator_api_key_env,
                max_output_tokens=args.agent_operator_max_output_tokens,
                temperature=args.agent_operator_temperature,
            ),
            timeout_seconds=args.agent_operator_timeout_seconds,
            enabled=True,
        ),
    }
    loop = TestTokenLoop(strategy, risk, execution, parameters)
    profile_hash = stable_hash(profile_payload)
    calibration_policy_hash = stable_hash(calibration_policy_payload)
    scenario_cache: dict[str, tuple[ReplayScenario, list[MarketEvent], str, str]] = {}
    stop_flags = {"restart_requested": False}
    current_cycle = {"index": 0}
    portfolio_state = PortfolioState(
        bankroll=args.bankroll,
        day_start_equity=args.bankroll,
        current_equity=args.bankroll,
    )
    open_positions_state: dict[str, object] = {}
    seen_live_event_ids: set[str] = set()
    state_refresh_streak_by_market: dict[str, int] = {}
    ingestion_degraded_streak = 0

    def _resolve_scenario_run_inputs(
        scenario_name: str,
    ) -> tuple[ReplayScenario, list[MarketEvent], str, str]:
        if scenario_pack is None or default_scenario is None:
            raise ValueError("scenario_pack_unavailable")
        normalized = scenario_name.strip() or default_scenario.name
        cached = scenario_cache.get(normalized)
        if cached is not None:
            return cached

        scenario = scenario_pack.get_scenario(normalized)
        events_for_run = apply_scenario_to_events(events, scenario)
        events_hash = hash_events(events_for_run)
        scenario_hash = stable_hash(scenario.to_dict())
        cached_payload = (scenario, events_for_run, events_hash, scenario_hash)
        scenario_cache[normalized] = cached_payload
        return cached_payload

    def _read_operator_control_state() -> dict:
        default_agent_operator_enabled = bool(args.agent_operator_enabled)
        default_agent_operator_mode = "advisory"
        default_agent_operator_strategy_auto_apply = True
        default_mode_current = resolved_lifecycle_mode
        default_mode_target = resolved_lifecycle_mode
        if args.ignore_operator_controls or not args.control_state_path.exists():
            return {
                "paused": False,
                "restart_requested": False,
                "kill_switch_active": False,
                "cancel_all_requested": False,
                "selected_scenario": control_default_scenario_name,
                "control_version": 0,
                "agent_operator_enabled": default_agent_operator_enabled,
                "agent_operators_running": default_agent_operator_enabled,
                "agent_operator_mode": default_agent_operator_mode,
                "agent_operator_strategy_auto_apply": (
                    default_agent_operator_strategy_auto_apply
                ),
                "agent_operator_active_candidate_id": "",
                "agent_operator_active_candidate_scenario": "",
                "agent_operator_candidate_previous_scenario": "",
                "agent_operator_candidate_last_action": "",
                "agent_operator_candidate_last_action_at": "",
                "mode_current": default_mode_current,
                "mode_target": default_mode_target,
                "mode_transition_approval_status": "pending",
                "mode_transition_evidence": {},
                "mode_transition_last_decision": {},
                "mode_transition_last_decision_at": "",
                "mode_transition_last_transition_at": "",
                "mode_transition_last_actor": "",
                "mode_transition_last_reason": "",
                "mode_transition_last_action": "",
            }

        control_state = control_manager.load_control_state()
        selected_scenario = str(control_state.get("selected_scenario", "")).strip()
        if not selected_scenario:
            control_state["selected_scenario"] = control_default_scenario_name
        if "kill_switch_active" not in control_state:
            control_state["kill_switch_active"] = False
        if "cancel_all_requested" not in control_state:
            control_state["cancel_all_requested"] = False
        if "agent_operator_enabled" not in control_state:
            control_state["agent_operator_enabled"] = default_agent_operator_enabled
        if "agent_operators_running" not in control_state:
            control_state["agent_operators_running"] = bool(
                control_state.get(
                    "agent_operator_enabled",
                    default_agent_operator_enabled,
                )
            )
        if "agent_operator_mode" not in control_state:
            control_state["agent_operator_mode"] = default_agent_operator_mode
        if "agent_operator_strategy_auto_apply" not in control_state:
            control_state["agent_operator_strategy_auto_apply"] = (
                default_agent_operator_strategy_auto_apply
            )
        if "agent_operator_active_candidate_id" not in control_state:
            control_state["agent_operator_active_candidate_id"] = ""
        if "agent_operator_active_candidate_scenario" not in control_state:
            control_state["agent_operator_active_candidate_scenario"] = ""
        if "agent_operator_candidate_previous_scenario" not in control_state:
            control_state["agent_operator_candidate_previous_scenario"] = ""
        if "agent_operator_candidate_last_action" not in control_state:
            control_state["agent_operator_candidate_last_action"] = ""
        if "agent_operator_candidate_last_action_at" not in control_state:
            control_state["agent_operator_candidate_last_action_at"] = ""
        control_state["agent_operator_mode"] = _normalize_agent_operator_mode(
            control_state.get("agent_operator_mode")
        )
        agent_operator_enabled_state = bool(
            control_state.get("agent_operator_enabled", False)
        )
        control_state["agent_operators_running"] = bool(
            control_state.get("agent_operators_running", False)
            or agent_operator_enabled_state
        )
        control_state["agent_operator_enabled"] = bool(
            control_state["agent_operators_running"]
        )
        control_state["agent_operator_strategy_auto_apply"] = bool(
            control_state.get("agent_operator_strategy_auto_apply", True)
        )
        control_state["agent_operator_active_candidate_id"] = str(
            control_state.get("agent_operator_active_candidate_id", "")
        ).strip()
        control_state["agent_operator_active_candidate_scenario"] = str(
            control_state.get("agent_operator_active_candidate_scenario", "")
        ).strip()
        control_state["agent_operator_candidate_previous_scenario"] = str(
            control_state.get("agent_operator_candidate_previous_scenario", "")
        ).strip()
        control_state["agent_operator_candidate_last_action"] = str(
            control_state.get("agent_operator_candidate_last_action", "")
        ).strip()
        control_state["agent_operator_candidate_last_action_at"] = str(
            control_state.get("agent_operator_candidate_last_action_at", "")
        ).strip()
        control_state["mode_current"] = normalize_lifecycle_mode(
            control_state.get("mode_current", default_mode_current)
        )
        control_state["mode_target"] = normalize_lifecycle_mode(
            control_state.get("mode_target", control_state["mode_current"])
        )
        control_state["mode_transition_approval_status"] = (
            _normalize_mode_transition_approval_status(
                control_state.get("mode_transition_approval_status", "pending")
            )
        )
        mode_transition_evidence = control_state.get("mode_transition_evidence")
        if not isinstance(mode_transition_evidence, dict):
            mode_transition_evidence = {}
        control_state["mode_transition_evidence"] = mode_transition_evidence
        if not isinstance(control_state.get("mode_transition_last_decision"), dict):
            control_state["mode_transition_last_decision"] = {}
        if "mode_transition_last_decision_at" not in control_state:
            control_state["mode_transition_last_decision_at"] = ""
        if "mode_transition_last_transition_at" not in control_state:
            control_state["mode_transition_last_transition_at"] = ""
        if "mode_transition_last_actor" not in control_state:
            control_state["mode_transition_last_actor"] = ""
        if "mode_transition_last_reason" not in control_state:
            control_state["mode_transition_last_reason"] = ""
        if "mode_transition_last_action" not in control_state:
            control_state["mode_transition_last_action"] = ""
        return control_state

    if args.cycle_output_dir:
        args.cycle_output_dir.mkdir(parents=True, exist_ok=True)
    def _agent_operator_skipped_result(reason: str, *, mode: str) -> dict:
        operator = agent_operators_by_mode.get(mode)
        if operator is None:
            return {
                "status": "DISABLED",
                "reason": reason,
                "provider": "none",
                "model": "none",
                "mode": mode,
                "generated_at": datetime.now(UTC).isoformat(timespec="milliseconds"),
                "summary": "",
                "profitability_hypothesis": "",
                "risk_posture": "neutral",
                "confidence": None,
                "recommended_actions": [],
                "scenario_hint": "",
            }
        return {
            "status": "SKIPPED",
            "reason": reason,
            "provider": operator.client.provider,
            "model": operator.client.model,
            "mode": mode,
            "generated_at": datetime.now(UTC).isoformat(timespec="milliseconds"),
            "summary": "",
            "profitability_hypothesis": "",
            "risk_posture": "neutral",
            "confidence": None,
            "recommended_actions": [],
            "scenario_hint": "",
        }

    def _agent_operators_skipped(reason: str) -> dict[str, dict[str, Any]]:
        return {
            "supervisor": _agent_operator_skipped_result(
                reason,
                mode="advisory",
            ),
            "strategist": _agent_operator_skipped_result(
                reason,
                mode="strategy",
            ),
        }

    def _run_test_token_cycle(heartbeat) -> dict:
        nonlocal portfolio_state, open_positions_state, seen_live_event_ids, state_refresh_streak_by_market, ingestion_degraded_streak
        cycle_index = current_cycle["index"] if current_cycle["index"] > 0 else 1
        control_state = _read_operator_control_state()
        selected_scenario_name = str(
            control_state.get("selected_scenario", control_default_scenario_name)
        ).strip()
        if not selected_scenario_name:
            selected_scenario_name = control_default_scenario_name
        control_version = int(control_state.get("control_version", 0))
        paused = bool(control_state.get("paused", False))
        restart_requested = bool(control_state.get("restart_requested", False))
        kill_switch_active = bool(control_state.get("kill_switch_active", False))
        cancel_all_requested = bool(control_state.get("cancel_all_requested", False))
        agent_operators_running = bool(
            control_state.get(
                "agent_operators_running",
                control_state.get("agent_operator_enabled", False),
            )
        )
        agent_operator_enabled = agent_operators_running
        agent_operator_mode = _normalize_agent_operator_mode(
            control_state.get("agent_operator_mode", "advisory")
        )
        agent_operator_strategy_auto_apply = bool(
            control_state.get("agent_operator_strategy_auto_apply", True)
        )
        agent_operator_active_candidate_id = str(
            control_state.get("agent_operator_active_candidate_id", "")
        ).strip()
        agent_operator_active_candidate_scenario = str(
            control_state.get("agent_operator_active_candidate_scenario", "")
        ).strip()
        mode_current = normalize_lifecycle_mode(
            control_state.get("mode_current", resolved_lifecycle_mode)
        )
        mode_target = normalize_lifecycle_mode(
            control_state.get("mode_target", mode_current)
        )
        mode_transition_approval_status = _normalize_mode_transition_approval_status(
            control_state.get("mode_transition_approval_status", "pending")
        )
        raw_mode_transition_evidence = control_state.get("mode_transition_evidence")
        mode_transition_evidence = (
            dict(raw_mode_transition_evidence)
            if isinstance(raw_mode_transition_evidence, dict)
            else {}
        )
        mode_transition_decision = build_mode_transition_decision(
            current_mode=mode_current,
            target_mode=mode_target,
            policy=mode_lifecycle_policy_payload,
            evidence=mode_transition_evidence,
            manual_approval_status=mode_transition_approval_status,
            actor=args.operator_control_actor,
            reason="runtime_supervisor_cycle_gate",
        )
        mode_transition_allowed = bool(mode_transition_decision.get("allowed", False))
        mode_transition_reason_codes = [
            str(reason_code).strip()
            for reason_code in mode_transition_decision.get("reason_codes", [])
            if str(reason_code).strip()
        ]
        mode_transition_decision_hash = str(
            mode_transition_decision.get("decision_hash", "")
        )
        mode_effective = mode_target if mode_transition_allowed else mode_current
        expected_execution_mode = _execution_mode_for_lifecycle_mode(mode_effective)
        execution_mode_matches_lifecycle = (
            expected_execution_mode == resolved_execution_mode
        )
        mode_lifecycle_metadata = {
            "mode_lifecycle_current_mode": mode_current,
            "mode_lifecycle_target_mode": mode_target,
            "mode_lifecycle_transition_allowed": mode_transition_allowed,
            "mode_lifecycle_transition_reason_codes": mode_transition_reason_codes,
            "mode_lifecycle_decision_hash": mode_transition_decision_hash,
            "mode_lifecycle_approval_status": mode_transition_approval_status,
            "mode_lifecycle_effective_mode": mode_effective,
            "mode_lifecycle_expected_execution_mode": expected_execution_mode,
            "mode_lifecycle_execution_mode": resolved_execution_mode,
            "mode_lifecycle_execution_mode_matches": execution_mode_matches_lifecycle,
            "mode_lifecycle_policy_hash": mode_lifecycle_policy_hash,
            "mode_lifecycle_policy_path": str(args.mode_lifecycle_policy),
            "mode_lifecycle_decision": mode_transition_decision,
        }
        heartbeat(
            "cycle_started",
            {
                "cycle_index": cycle_index,
                "selected_scenario": selected_scenario_name,
                "control_version": control_version,
                "paused": paused,
                "restart_requested": restart_requested,
                "kill_switch_active": kill_switch_active,
                "cancel_all_requested": cancel_all_requested,
                "agent_operator_enabled": agent_operator_enabled,
                "agent_operators_running": agent_operators_running,
                "agent_operator_mode": agent_operator_mode,
                "agent_operator_strategy_auto_apply": (
                    agent_operator_strategy_auto_apply
                ),
                "agent_operator_active_candidate_id": (
                    agent_operator_active_candidate_id
                ),
                "agent_operator_active_candidate_scenario": (
                    agent_operator_active_candidate_scenario
                ),
                "mode_current": mode_current,
                "mode_target": mode_target,
                "mode_transition_approval_status": mode_transition_approval_status,
                "mode_transition_allowed": mode_transition_allowed,
                "mode_transition_reason_codes": mode_transition_reason_codes,
                "mode_transition_decision_hash": mode_transition_decision_hash,
                "mode_effective": mode_effective,
                "expected_execution_mode": expected_execution_mode,
                "execution_mode": resolved_execution_mode,
                "execution_mode_matches_lifecycle": execution_mode_matches_lifecycle,
            },
        )

        if restart_requested:
            if not args.ignore_operator_controls and args.control_state_path.exists():
                control_manager.acknowledge_restart(
                    actor=args.operator_control_actor,
                    note=f"acknowledged_before_cycle_{cycle_index}",
                )
            stop_flags["restart_requested"] = True
            agent_operator_result = _agent_operator_skipped_result(
                "restart_requested",
                mode=agent_operator_mode,
            )
            heartbeat(
                "control_restart_acknowledged",
                {
                    "cycle_index": cycle_index,
                    "control_version": control_version,
                    "selected_scenario": selected_scenario_name,
                },
            )
            return {
                "cycle_index": cycle_index,
                "cycle_status": "RESTART_REQUESTED",
                "selected_scenario": selected_scenario_name,
                "control_version": control_version,
                "kill_switch_active": kill_switch_active,
                "cancel_all_requested": cancel_all_requested,
                "events": 0,
                "risk_allowed_count": 0,
                "filled_trade_count": 0,
                "partial_fill_count": 0,
                "exit_candidate_count": 0,
                "confirmed_exit_count": 0,
                "forced_exit_count": 0,
                "confirmed_exit_ratio": None,
                "confirmed_exit_latency_hours": None,
                "median_position_age_hours": None,
                "stale_position_count": 0,
                "stale_position_ratio": 0.0,
                "raw_probability_mean": None,
                "calibrated_probability_mean": None,
                "probability_drift_mean": None,
                "probability_drift_abs_mean": None,
                "probability_drift_max_abs": None,
                "weighted_check_agreement_mean": None,
                "calibration_applied_ratio": 0.0,
                "total_execution_cost": 0.0,
                "total_fees_paid": 0.0,
                "total_slippage_cost": 0.0,
                "attributed_trade_count": 0,
                "expected_gross_edge_value": 0.0,
                "expected_net_edge_value": 0.0,
                "expected_net_edge_value_on_fills": 0.0,
                "expected_value_after_execution_cost": 0.0,
                "average_expected_gross_edge_bps": None,
                "average_expected_net_edge_bps": None,
                "expected_edge_capture_ratio": None,
                "execution_cost_to_expected_net_ratio": None,
                "bankroll": portfolio_state.bankroll,
                "day_start_equity": portfolio_state.day_start_equity,
                "current_equity": portfolio_state.current_equity,
                "net_pnl": round(
                    portfolio_state.current_equity - portfolio_state.day_start_equity,
                    4,
                ),
                "open_notional": portfolio_state.open_notional,
                "open_positions": portfolio_state.open_positions,
                "total_exposure_fraction": round(
                    portfolio_state.total_exposure_fraction, 6
                ),
                "daily_drawdown_fraction": round(
                    portfolio_state.daily_drawdown_fraction, 6
                ),
                "result_hash": None,
                "agent_operator": agent_operator_result,
                "agent_operators_running": agent_operators_running,
                "agent_operators": _agent_operators_skipped("restart_requested"),
                "agent_operator_status": agent_operator_result["status"],
                "agent_operator_mode": agent_operator_mode,
                "agent_operator_provider": agent_operator_result["provider"],
                "agent_operator_model": agent_operator_result["model"],
                "agent_operator_strategy_scenario_applied": False,
                "agent_operator_strategy_scenario_hint": "",
                "agent_operator_strategy_scenario_rejected_reason": "",
                **mode_lifecycle_metadata,
            }

        if paused:
            agent_operator_result = _agent_operator_skipped_result(
                "paused",
                mode=agent_operator_mode,
            )
            heartbeat(
                "control_pause_gate",
                {
                    "cycle_index": cycle_index,
                    "control_version": control_version,
                    "selected_scenario": selected_scenario_name,
                },
            )
            return {
                "cycle_index": cycle_index,
                "cycle_status": "PAUSED",
                "selected_scenario": selected_scenario_name,
                "control_version": control_version,
                "kill_switch_active": kill_switch_active,
                "cancel_all_requested": cancel_all_requested,
                "events": 0,
                "risk_allowed_count": 0,
                "filled_trade_count": 0,
                "partial_fill_count": 0,
                "exit_candidate_count": 0,
                "confirmed_exit_count": 0,
                "forced_exit_count": 0,
                "confirmed_exit_ratio": None,
                "confirmed_exit_latency_hours": None,
                "median_position_age_hours": None,
                "stale_position_count": 0,
                "stale_position_ratio": 0.0,
                "raw_probability_mean": None,
                "calibrated_probability_mean": None,
                "probability_drift_mean": None,
                "probability_drift_abs_mean": None,
                "probability_drift_max_abs": None,
                "weighted_check_agreement_mean": None,
                "calibration_applied_ratio": 0.0,
                "total_execution_cost": 0.0,
                "total_fees_paid": 0.0,
                "total_slippage_cost": 0.0,
                "attributed_trade_count": 0,
                "expected_gross_edge_value": 0.0,
                "expected_net_edge_value": 0.0,
                "expected_net_edge_value_on_fills": 0.0,
                "expected_value_after_execution_cost": 0.0,
                "average_expected_gross_edge_bps": None,
                "average_expected_net_edge_bps": None,
                "expected_edge_capture_ratio": None,
                "execution_cost_to_expected_net_ratio": None,
                "bankroll": portfolio_state.bankroll,
                "day_start_equity": portfolio_state.day_start_equity,
                "current_equity": portfolio_state.current_equity,
                "net_pnl": round(
                    portfolio_state.current_equity - portfolio_state.day_start_equity,
                    4,
                ),
                "open_notional": portfolio_state.open_notional,
                "open_positions": portfolio_state.open_positions,
                "total_exposure_fraction": round(
                    portfolio_state.total_exposure_fraction, 6
                ),
                "daily_drawdown_fraction": round(
                    portfolio_state.daily_drawdown_fraction, 6
                ),
                "result_hash": None,
                "agent_operator": agent_operator_result,
                "agent_operators_running": agent_operators_running,
                "agent_operators": _agent_operators_skipped("paused"),
                "agent_operator_status": agent_operator_result["status"],
                "agent_operator_mode": agent_operator_mode,
                "agent_operator_provider": agent_operator_result["provider"],
                "agent_operator_model": agent_operator_result["model"],
                "agent_operator_strategy_scenario_applied": False,
                "agent_operator_strategy_scenario_hint": "",
                "agent_operator_strategy_scenario_rejected_reason": "",
                **mode_lifecycle_metadata,
            }
        if not execution_mode_matches_lifecycle:
            mismatch_reason = "mode_lifecycle_execution_mode_mismatch"
            agent_operator_result = _agent_operator_skipped_result(
                mismatch_reason,
                mode=agent_operator_mode,
            )
            heartbeat(
                "mode_lifecycle_execution_mode_mismatch",
                {
                    "cycle_index": cycle_index,
                    "control_version": control_version,
                    "mode_current": mode_current,
                    "mode_target": mode_target,
                    "mode_effective": mode_effective,
                    "mode_transition_allowed": mode_transition_allowed,
                    "expected_execution_mode": expected_execution_mode,
                    "execution_mode": resolved_execution_mode,
                    "mode_transition_reason_codes": mode_transition_reason_codes,
                    "mode_transition_decision_hash": mode_transition_decision_hash,
                },
            )
            return {
                "cycle_index": cycle_index,
                "cycle_status": "MODE_LIFECYCLE_EXECUTION_MODE_MISMATCH",
                "selected_scenario": selected_scenario_name,
                "control_version": control_version,
                "kill_switch_active": kill_switch_active,
                "cancel_all_requested": cancel_all_requested,
                "events": 0,
                "risk_allowed_count": 0,
                "filled_trade_count": 0,
                "partial_fill_count": 0,
                "exit_candidate_count": 0,
                "confirmed_exit_count": 0,
                "forced_exit_count": 0,
                "confirmed_exit_ratio": None,
                "confirmed_exit_latency_hours": None,
                "median_position_age_hours": None,
                "stale_position_count": 0,
                "stale_position_ratio": 0.0,
                "raw_probability_mean": None,
                "calibrated_probability_mean": None,
                "probability_drift_mean": None,
                "probability_drift_abs_mean": None,
                "probability_drift_max_abs": None,
                "weighted_check_agreement_mean": None,
                "calibration_applied_ratio": 0.0,
                "total_execution_cost": 0.0,
                "total_fees_paid": 0.0,
                "total_slippage_cost": 0.0,
                "attributed_trade_count": 0,
                "expected_gross_edge_value": 0.0,
                "expected_net_edge_value": 0.0,
                "expected_net_edge_value_on_fills": 0.0,
                "expected_value_after_execution_cost": 0.0,
                "average_expected_gross_edge_bps": None,
                "average_expected_net_edge_bps": None,
                "expected_edge_capture_ratio": None,
                "execution_cost_to_expected_net_ratio": None,
                "bankroll": portfolio_state.bankroll,
                "day_start_equity": portfolio_state.day_start_equity,
                "current_equity": portfolio_state.current_equity,
                "net_pnl": round(
                    portfolio_state.current_equity - portfolio_state.day_start_equity,
                    4,
                ),
                "open_notional": portfolio_state.open_notional,
                "open_positions": portfolio_state.open_positions,
                "total_exposure_fraction": round(
                    portfolio_state.total_exposure_fraction, 6
                ),
                "daily_drawdown_fraction": round(
                    portfolio_state.daily_drawdown_fraction, 6
                ),
                "result_hash": None,
                "agent_operator": agent_operator_result,
                "agent_operators_running": agent_operators_running,
                "agent_operators": _agent_operators_skipped(mismatch_reason),
                "agent_operator_status": agent_operator_result["status"],
                "agent_operator_mode": agent_operator_mode,
                "agent_operator_provider": agent_operator_result["provider"],
                "agent_operator_model": agent_operator_result["model"],
                "agent_operator_strategy_scenario_applied": False,
                "agent_operator_strategy_scenario_hint": "",
                "agent_operator_strategy_scenario_rejected_reason": "",
                **mode_lifecycle_metadata,
            }

        cancel_all_summary: dict[str, object] | None = None
        cancel_all_acknowledged = False
        if kill_switch_active:
            cancel_all_summary = execution.cancel_all_open_orders(
                reason="kill_switch_active"
            )
            heartbeat(
                "control_kill_switch_gate",
                {
                    "cycle_index": cycle_index,
                    "control_version": control_version,
                    "cancelled_order_count": int(
                        cancel_all_summary.get("cancelled_order_count", 0)
                    ),
                    "cancelled_notional": float(
                        cancel_all_summary.get("cancelled_notional", 0.0)
                    ),
                },
            )
        if cancel_all_requested:
            if cancel_all_summary is None:
                cancel_all_summary = execution.cancel_all_open_orders(
                    reason="operator_cancel_all_requested"
                )
            acknowledge_cancel_all = getattr(
                control_manager, "acknowledge_cancel_all", None
            )
            if (
                not args.ignore_operator_controls
                and args.control_state_path.exists()
                and callable(acknowledge_cancel_all)
            ):
                acknowledge_cancel_all(
                    actor=args.operator_control_actor,
                    note=f"acknowledged_before_cycle_{cycle_index}",
                )
                cancel_all_acknowledged = True
            heartbeat(
                "control_cancel_all_applied",
                {
                    "cycle_index": cycle_index,
                    "control_version": control_version,
                    "cancel_all_acknowledged": cancel_all_acknowledged,
                    "cancelled_order_count": int(
                        cancel_all_summary.get("cancelled_order_count", 0)
                    ),
                    "cancelled_notional": float(
                        cancel_all_summary.get("cancelled_notional", 0.0)
                    ),
                },
            )
        freshness_filter_enabled = (
            args.ingestion_mode == "live_polymarket"
            and not args.disable_live_freshness_filter
        )
        freshness_skipped_event_ids = 0
        freshness_committed_event_ids: list[str] = []
        state_refresh_applied = False
        state_refresh_event_count = 0
        state_refresh_market_ids: list[str] = []
        state_refresh_streak_snapshot: dict[str, int] = {}
        state_refresh_max_streak = 0
        stale_open_position_market_ids: list[str] = []
        no_new_events_since_last_cycle = False

        if args.ingestion_mode == "historical_jsonl":
            scenario_name_in_use = selected_scenario_name
            try:
                scenario, events_for_run, events_hash, scenario_hash = (
                    _resolve_scenario_run_inputs(scenario_name_in_use)
                )
            except ValueError:
                scenario_name_in_use = default_scenario.name
                heartbeat(
                    "control_invalid_scenario_fallback",
                    {
                        "cycle_index": cycle_index,
                        "requested_scenario": selected_scenario_name,
                        "fallback_scenario": scenario_name_in_use,
                    },
                )
                scenario, events_for_run, events_hash, scenario_hash = (
                    _resolve_scenario_run_inputs(scenario_name_in_use)
                )
            run_scenario_name = scenario.name
            events_for_run = _offset_events_for_cycle(
                events_for_run,
                cycle_index=cycle_index,
            )
            if historical_ingestion is None:
                raise ValueError("historical ingestion state is unavailable")
            cycle_ingestion = historical_ingestion
        else:
            scenario_name_in_use = "live_polymarket"
            run_scenario_name = "live_polymarket"
            if selected_scenario_name != scenario_name_in_use:
                heartbeat(
                    "control_scenario_ignored_for_live_mode",
                    {
                        "cycle_index": cycle_index,
                        "requested_scenario": selected_scenario_name,
                        "applied_scenario": scenario_name_in_use,
                    },
                )
            if live_ingestion_adapter is None:
                raise ValueError("live ingestion adapter is unavailable")
            cycle_ingestion = live_ingestion_adapter.load_markets(
                timeout_seconds=args.ingestion_timeout_seconds,
            )
            if cycle_ingestion.status == "FAILED":
                raise ValueError(
                    "Ingestion adapter failed: "
                    f"reasons={list(cycle_ingestion.reasons)} "
                    f"metadata={cycle_ingestion.metadata}"
                )
            events_for_run = cycle_ingestion.events
            if freshness_filter_enabled:
                fresh_events: list[MarketEvent] = []
                for event in events_for_run:
                    if event.event_id in seen_live_event_ids:
                        continue
                    fresh_events.append(event)
                    freshness_committed_event_ids.append(event.event_id)
                freshness_skipped_event_ids = len(events_for_run) - len(fresh_events)
                events_for_run = fresh_events
                if freshness_skipped_event_ids > 0:
                    heartbeat(
                        "live_freshness_filter_applied",
                        {
                            "cycle_index": cycle_index,
                            "skipped_seen_event_ids": freshness_skipped_event_ids,
                            "fresh_event_ids": len(events_for_run),
                            "seen_event_ids_before_cycle": len(seen_live_event_ids),
                        },
                    )
            no_new_events_since_last_cycle = (
                freshness_filter_enabled
                and not events_for_run
                and bool(cycle_ingestion.events)
            )
            if (
                no_new_events_since_last_cycle
                and open_positions_state
            ):
                open_position_market_ids = set(open_positions_state.keys())
                state_refresh_events: list[MarketEvent] = []
                for event in cycle_ingestion.events:
                    if event.market_id not in open_position_market_ids:
                        continue
                    event_payload = event.to_dict()
                    event_metadata = dict(event_payload.get("metadata", {}))
                    event_metadata["state_refresh_event"] = True
                    event_metadata["state_refresh_reason"] = (
                        "no_new_events_since_last_cycle"
                    )
                    event_metadata["suppress_new_entries"] = True
                    event_payload["metadata"] = event_metadata
                    state_refresh_events.append(MarketEvent.from_dict(event_payload))
                if state_refresh_events:
                    events_for_run = state_refresh_events
                    state_refresh_applied = True
                    state_refresh_event_count = len(state_refresh_events)
                    state_refresh_market_ids = sorted(
                        {
                            event.market_id
                            for event in state_refresh_events
                        }
                    )
                    heartbeat(
                        "live_state_refresh_applied",
                        {
                            "cycle_index": cycle_index,
                            "state_refresh_event_count": state_refresh_event_count,
                            "open_position_market_count": len(
                                open_position_market_ids
                            ),
                            "state_refresh_market_ids": state_refresh_market_ids,
                            "seen_event_ids_before_cycle": len(
                                seen_live_event_ids
                            ),
                        },
                    )
            events_hash = hash_events(events_for_run)
            scenario_hash = stable_hash(
                {
                    "ingestion_mode": args.ingestion_mode,
                    "live_source_url": args.live_source_url,
                    "live_max_markets": args.live_max_markets,
                    "live_min_volume_24h": args.live_min_volume_24h,
                    "live_wallet_convergence_path": str(
                        args.live_wallet_convergence_path
                    )
                    if args.live_wallet_convergence_path is not None
                    else None,
                    "live_wallet_convergence_threshold": (
                        args.live_wallet_convergence_threshold
                    ),
                }
            )
            if args.ingestion_mode == "live_polymarket":
                open_position_market_ids_sorted = sorted(open_positions_state.keys())
                if state_refresh_applied and state_refresh_market_ids:
                    refreshed_market_ids = set(state_refresh_market_ids)
                    for market_id in open_position_market_ids_sorted:
                        if market_id in refreshed_market_ids:
                            state_refresh_streak_by_market[market_id] = (
                                state_refresh_streak_by_market.get(market_id, 0) + 1
                            )
                        else:
                            state_refresh_streak_by_market.pop(market_id, None)
                else:
                    for market_id in open_position_market_ids_sorted:
                        state_refresh_streak_by_market.pop(market_id, None)
                current_open_market_ids = set(open_position_market_ids_sorted)
                for market_id in list(state_refresh_streak_by_market):
                    if market_id not in current_open_market_ids:
                        state_refresh_streak_by_market.pop(market_id, None)
                state_refresh_streak_snapshot = {
                    market_id: int(state_refresh_streak_by_market[market_id])
                    for market_id in open_position_market_ids_sorted
                    if state_refresh_streak_by_market.get(market_id, 0) > 0
                }
                if state_refresh_streak_snapshot:
                    state_refresh_max_streak = max(state_refresh_streak_snapshot.values())
                stale_open_position_market_ids = sorted(
                    market_id
                    for market_id, streak in state_refresh_streak_snapshot.items()
                    if streak >= args.state_refresh_stale_threshold_cycles
                )
        effective_ingestion_status = cycle_ingestion.status
        effective_ingestion_reasons = list(cycle_ingestion.reasons)
        effective_ingestion_metadata = dict(cycle_ingestion.metadata)
        effective_ingestion_metadata["live_freshness_filter_enabled"] = (
            freshness_filter_enabled
        )
        effective_ingestion_metadata["seen_event_ids_before_cycle"] = len(
            seen_live_event_ids
        )
        effective_ingestion_metadata["skipped_seen_event_ids"] = (
            freshness_skipped_event_ids
        )
        effective_ingestion_metadata["fresh_event_ids"] = len(events_for_run)
        effective_ingestion_metadata["seen_event_ids_after_cycle"] = (
            len(seen_live_event_ids) + len(freshness_committed_event_ids)
        )
        effective_ingestion_metadata["state_refresh_applied"] = state_refresh_applied
        effective_ingestion_metadata["state_refresh_event_count"] = (
            state_refresh_event_count
        )
        effective_ingestion_metadata["state_refresh_market_ids"] = (
            state_refresh_market_ids
        )
        effective_ingestion_metadata["state_refresh_streak_by_market"] = (
            state_refresh_streak_snapshot
        )
        effective_ingestion_metadata["state_refresh_max_streak"] = (
            state_refresh_max_streak
        )
        effective_ingestion_metadata["state_refresh_stale_threshold_cycles"] = (
            args.state_refresh_stale_threshold_cycles
        )
        effective_ingestion_metadata["stale_open_position_market_ids"] = (
            stale_open_position_market_ids
        )
        if freshness_filter_enabled and freshness_skipped_event_ids > 0:
            effective_ingestion_reasons.append("seen_event_ids_skipped")
            if effective_ingestion_status == "OK":
                effective_ingestion_status = "DEGRADED"
        if state_refresh_applied:
            effective_ingestion_reasons.append("state_refresh_from_seen_events")
            if effective_ingestion_status == "OK":
                effective_ingestion_status = "DEGRADED"
        if no_new_events_since_last_cycle:
            effective_ingestion_reasons.append("no_new_events_since_last_cycle")
            if effective_ingestion_status == "OK":
                effective_ingestion_status = "DEGRADED"
        if stale_open_position_market_ids:
            effective_ingestion_reasons.append("stale_open_positions_under_state_refresh")
            if effective_ingestion_status == "OK":
                effective_ingestion_status = "DEGRADED"
        effective_ingestion_reasons = list(dict.fromkeys(effective_ingestion_reasons))
        if effective_ingestion_status == "DEGRADED":
            ingestion_degraded_streak += 1
        else:
            ingestion_degraded_streak = 0
        ingestion_degraded_entry_suppressed = (
            ingestion_degraded_streak
            >= args.ingestion_degraded_entry_suppress_threshold_cycles
        )
        if ingestion_degraded_entry_suppressed:
            effective_ingestion_reasons.append(
                "entry_suppressed_due_consecutive_ingestion_degraded"
            )
            heartbeat(
                "ingestion_degraded_entry_suppression_applied",
                {
                    "cycle_index": cycle_index,
                    "ingestion_degraded_streak": ingestion_degraded_streak,
                    "ingestion_degraded_entry_suppress_threshold_cycles": (
                        args.ingestion_degraded_entry_suppress_threshold_cycles
                    ),
                    "ingestion_status": effective_ingestion_status,
                },
            )
        effective_ingestion_reasons = list(dict.fromkeys(effective_ingestion_reasons))
        effective_ingestion_metadata["ingestion_degraded_streak"] = (
            ingestion_degraded_streak
        )
        effective_ingestion_metadata[
            "ingestion_degraded_entry_suppress_threshold_cycles"
        ] = args.ingestion_degraded_entry_suppress_threshold_cycles
        effective_ingestion_metadata["ingestion_degraded_entry_suppressed"] = (
            ingestion_degraded_entry_suppressed
        )

        execution_scope = f"cycle:{cycle_index}"
        scoped_events: list[MarketEvent] = []
        for event in events_for_run:
            event_payload = event.to_dict()
            event_metadata = dict(event_payload.get("metadata", {}))
            event_metadata["execution_scope"] = execution_scope
            event_metadata["cycle_index"] = cycle_index
            event_metadata["kill_switch_active"] = kill_switch_active
            event_metadata["cancel_all_requested"] = cancel_all_requested
            event_metadata["ingestion_degraded_streak"] = ingestion_degraded_streak
            event_metadata[
                "ingestion_degraded_entry_suppressed"
            ] = ingestion_degraded_entry_suppressed
            if ingestion_degraded_entry_suppressed:
                event_metadata["suppress_new_entries"] = True
            if cancel_all_summary is not None:
                event_metadata["cancel_all_summary"] = cancel_all_summary
            event_payload["metadata"] = event_metadata
            scoped_events.append(MarketEvent.from_dict(event_payload))
        events_for_run = scoped_events

        cycle_start_open_notional = round(portfolio_state.open_notional, 4)
        cycle_start_open_positions = portfolio_state.open_positions
        run = loop.run(
            events_for_run,
            portfolio_state,
            initial_open_positions=open_positions_state,
        )
        available_scenarios = (
            sorted(scenario_pack.scenarios.keys()) if scenario_pack is not None else []
        )
        strategy_scenario_hint = ""
        strategy_scenario_applied = False
        strategy_scenario_rejected_reason = ""
        base_agent_operator_cycle_context = {
            "cycle_index": cycle_index,
            "scenario_name": run_scenario_name,
            "ingestion_mode": args.ingestion_mode,
            "ingestion_status": effective_ingestion_status,
            "ingestion_reasons": effective_ingestion_reasons,
            "ingestion_degraded_streak": ingestion_degraded_streak,
            "risk_allowed_count": run.risk_allowed_count,
            "filled_trade_count": run.filled_trade_count,
            "partial_fill_count": run.partial_fill_count,
            "exit_candidate_count": run.exit_candidate_count,
            "confirmed_exit_count": run.confirmed_exit_count,
            "forced_exit_count": run.forced_exit_count,
            "expected_gross_edge_value": run.expected_gross_edge_value,
            "expected_net_edge_value": run.expected_net_edge_value,
            "expected_net_edge_value_on_fills": run.expected_net_edge_value_on_fills,
            "expected_value_after_execution_cost": run.expected_value_after_execution_cost,
            "total_execution_cost": run.total_execution_cost,
            "total_fees_paid": run.total_fees_paid,
            "total_slippage_cost": run.total_slippage_cost,
            "execution_cost_to_expected_net_ratio": (
                run.execution_cost_to_expected_net_ratio
            ),
            "portfolio": {
                "bankroll": run.final_portfolio.bankroll,
                "day_start_equity": run.final_portfolio.day_start_equity,
                "current_equity": run.final_portfolio.current_equity,
                "net_pnl": (
                    run.final_portfolio.current_equity
                    - run.final_portfolio.day_start_equity
                ),
                "open_notional": run.final_portfolio.open_notional,
                "open_positions": run.final_portfolio.open_positions,
                "total_exposure_fraction": run.final_portfolio.total_exposure_fraction,
                "daily_drawdown_fraction": run.final_portfolio.daily_drawdown_fraction,
            },
            "operator_controls": {
                "kill_switch_active": kill_switch_active,
                "cancel_all_requested": cancel_all_requested,
                "cancel_all_acknowledged": cancel_all_acknowledged,
            },
            "available_scenarios": available_scenarios,
        }
        role_modes = {
            "supervisor": "advisory",
            "strategist": "strategy",
        }
        agent_operators = _agent_operators_skipped(
            "agent_operators_stopped_by_control"
        )
        if agent_operators_running:
            for role_name, role_mode in role_modes.items():
                active_agent_operator = agent_operators_by_mode.get(role_mode)
                if active_agent_operator is None:
                    agent_operators[role_name] = _agent_operator_skipped_result(
                        "agent_operator_mode_not_configured",
                        mode=role_mode,
                    )
                    continue
                agent_operators[role_name] = active_agent_operator.infer(
                    cycle_context={
                        **base_agent_operator_cycle_context,
                        "agent_operator_role": role_name,
                        "agent_operator_mode": role_mode,
                    }
                )
        else:
            agent_operators = _agent_operators_skipped(
                "agent_operators_stopped_by_control"
            )
        legacy_role_name = "strategist" if agent_operator_mode == "strategy" else "supervisor"
        agent_operator_result = dict(
            agent_operators.get(
                legacy_role_name,
                _agent_operator_skipped_result(
                    "agent_operator_mode_not_configured",
                    mode=agent_operator_mode,
                ),
            )
        )
        final_portfolio = run.final_portfolio
        cycle_net_pnl = round(
            final_portfolio.current_equity - final_portfolio.day_start_equity,
            4,
        )
        agent_operator_learning_recommendation: dict[str, Any] | None = None
        agent_operator_learning_candidate: dict[str, Any] | None = None
        agent_operator_learning_record_error = ""
        agent_operator_outcome_attribution: dict[str, Any] = {
            "attributed_count": 0,
            "attributed_recommendation_ids": [],
        }
        agent_operator_outcome_attribution_error = ""
        strategy_scenario_candidate_id = ""

        strategy_scenario_hint = str(agent_operator_result.get("scenario_hint", "")).strip()
        if agent_operator_result.get("status") == "OK":
            try:
                learning_record = control_manager.record_agent_operator_recommendation(
                    cycle_index=cycle_index,
                    scenario_name=run_scenario_name,
                    mode=agent_operator_mode,
                    recommendation=agent_operator_result,
                    baseline_net_pnl=cycle_net_pnl,
                    baseline_expected_value_after_execution_cost=(
                        run.expected_value_after_execution_cost
                    ),
                )
            except Exception as error:  # pragma: no cover - fail-open safety path
                agent_operator_learning_record_error = str(error)
                heartbeat(
                    "agent_operator_learning_record_failed",
                    {
                        "cycle_index": cycle_index,
                        "agent_operator_mode": agent_operator_mode,
                        "error": agent_operator_learning_record_error,
                    },
                )
            else:
                recommendation_payload = learning_record.get("recommendation")
                if isinstance(recommendation_payload, dict):
                    agent_operator_learning_recommendation = recommendation_payload
                candidate_payload = learning_record.get("candidate")
                if isinstance(candidate_payload, dict):
                    agent_operator_learning_candidate = candidate_payload
                    candidate_scenario_hint = str(
                        candidate_payload.get("scenario_name", "")
                    ).strip()
                    if candidate_scenario_hint:
                        strategy_scenario_hint = candidate_scenario_hint
                heartbeat(
                    "agent_operator_learning_recorded",
                    {
                        "cycle_index": cycle_index,
                        "agent_operator_mode": agent_operator_mode,
                        "recommendation_id": str(
                            (
                                agent_operator_learning_recommendation or {}
                            ).get("recommendation_id", "")
                        ).strip(),
                        "candidate_id": str(
                            (
                                agent_operator_learning_candidate or {}
                            ).get("candidate_id", "")
                        ).strip(),
                    },
                )
        if (
            agent_operator_enabled
            and agent_operator_mode == "strategy"
            and agent_operator_result.get("status") == "OK"
            and strategy_scenario_hint
        ):
            if args.ingestion_mode != "historical_jsonl":
                strategy_scenario_rejected_reason = (
                    "strategy_scenario_hint_unsupported_for_live_mode"
                )
            elif not agent_operator_strategy_auto_apply:
                strategy_scenario_rejected_reason = "strategy_auto_apply_disabled"
            else:
                candidate_id_to_apply = str(
                    (agent_operator_learning_candidate or {}).get("candidate_id", "")
                ).strip()
                scenario_to_apply = str(
                    (agent_operator_learning_candidate or {}).get(
                        "scenario_name",
                        strategy_scenario_hint,
                    )
                ).strip() or strategy_scenario_hint
                try:
                    _resolve_scenario_run_inputs(scenario_to_apply)
                except ValueError:
                    strategy_scenario_rejected_reason = (
                        "invalid_strategy_scenario_hint"
                    )
                else:
                    if scenario_to_apply != selected_scenario_name:
                        if args.ignore_operator_controls:
                            strategy_scenario_rejected_reason = (
                                "operator_controls_ignored"
                            )
                        elif not candidate_id_to_apply:
                            strategy_scenario_rejected_reason = (
                                "strategy_candidate_missing"
                            )
                        else:
                            control_manager.apply_agent_operator_candidate(
                                actor=args.operator_control_actor,
                                candidate_id=candidate_id_to_apply,
                                reason=(
                                    f"strategy_auto_apply_cycle_{cycle_index}"
                                ),
                            )
                            strategy_scenario_applied = True
                            strategy_scenario_candidate_id = candidate_id_to_apply
                            heartbeat(
                                "agent_operator_strategy_candidate_applied",
                                {
                                    "cycle_index": cycle_index,
                                    "selected_scenario": selected_scenario_name,
                                    "strategy_scenario_hint": scenario_to_apply,
                                    "candidate_id": candidate_id_to_apply,
                                },
                            )
        try:
            agent_operator_outcome_attribution = (
                control_manager.attribute_agent_operator_outcomes(
                    current_cycle_index=cycle_index,
                    current_net_pnl=cycle_net_pnl,
                    current_expected_value_after_execution_cost=(
                        run.expected_value_after_execution_cost
                    ),
                )
            )
        except Exception as error:  # pragma: no cover - fail-open safety path
            agent_operator_outcome_attribution_error = str(error)
            heartbeat(
                "agent_operator_learning_outcome_attribution_failed",
                {
                    "cycle_index": cycle_index,
                    "error": agent_operator_outcome_attribution_error,
                },
            )
        else:
            attributed_count = int(
                agent_operator_outcome_attribution.get("attributed_count", 0) or 0
            )
            if attributed_count > 0:
                heartbeat(
                    "agent_operator_learning_outcomes_attributed",
                    {
                        "cycle_index": cycle_index,
                        "attributed_count": attributed_count,
                        "attributed_recommendation_ids": list(
                            agent_operator_outcome_attribution.get(
                                "attributed_recommendation_ids",
                                [],
                            )
                        ),
                    },
                )
        if strategy_scenario_rejected_reason:
            heartbeat(
                "agent_operator_strategy_scenario_rejected",
                {
                    "cycle_index": cycle_index,
                    "selected_scenario": selected_scenario_name,
                    "strategy_scenario_hint": strategy_scenario_hint,
                    "reason": strategy_scenario_rejected_reason,
                },
            )
        input_fingerprint = stable_hash(
            {
                "events_hash": events_hash,
                "profile_hash": profile_hash,
                "calibration_policy_hash": calibration_policy_hash,
                "scenario_hash": scenario_hash,
                "bankroll": args.bankroll,
            }
        )
        result_payload = serialize_test_token_loop_run(
            run,
            run_context={
                "scenario_name": run_scenario_name,
                "scenario_pack": str(args.scenario_pack)
                if args.ingestion_mode == "historical_jsonl"
                else None,
                "input_events_path": str(args.events) if args.events else None,
                "profile_path": str(args.profile),
                "calibration_policy_path": str(args.calibration_policy),
                "cycle_index": cycle_index,
                "control_version": control_version,
                "ingestion_mode": args.ingestion_mode,
                "ingestion_source": {
                    "source_url": args.live_source_url
                    if args.ingestion_mode == "live_polymarket"
                    else None,
                    "max_markets": args.live_max_markets
                    if args.ingestion_mode == "live_polymarket"
                    else None,
                    "min_volume_24h": args.live_min_volume_24h
                    if args.ingestion_mode == "live_polymarket"
                    else None,
                    "wallet_convergence_path": str(args.live_wallet_convergence_path)
                    if (
                        args.ingestion_mode == "live_polymarket"
                        and args.live_wallet_convergence_path is not None
                    )
                    else None,
                    "wallet_convergence_threshold": (
                        args.live_wallet_convergence_threshold
                        if args.ingestion_mode == "live_polymarket"
                        else None
                    ),
                },
                "exit_module": {
                    "target_capture_ratio": float(
                        parameters["exit.target_capture_ratio"]
                    ),
                    "volume_spike_multiplier": float(
                        parameters["exit.volume_spike_multiplier"]
                    ),
                    "stale_hours": float(parameters["exit.stale_hours"]),
                    "stale_price_change_threshold": float(
                        parameters["exit.stale_price_change_threshold"]
                    ),
                    "inventory_aging_derisk_hours": float(
                        parameters.get(
                            "exit.inventory_aging_derisk_hours",
                            float(parameters["exit.stale_hours"]) * 0.75,
                        )
                    ),
                    "max_holding_hours": float(
                        parameters.get(
                            "exit.max_holding_hours",
                            float(parameters["exit.stale_hours"]),
                        )
                    ),
                    "confirmation_threshold": 2,
                },
                "ingestion_status": effective_ingestion_status,
                "ingestion_reasons": effective_ingestion_reasons,
                "ingestion_metadata": effective_ingestion_metadata,
                "execution_gateway": {
                    "max_retries": args.execution_gateway_max_retries,
                    "retry_backoff_seconds": args.execution_gateway_retry_backoff_seconds,
                    "timeout_seconds": args.execution_gateway_timeout_seconds,
                },
                "operator_controls": {
                    "kill_switch_active": kill_switch_active,
                    "cancel_all_requested": cancel_all_requested,
                    "cancel_all_acknowledged": cancel_all_acknowledged,
                    "cancel_all_summary": cancel_all_summary,
                    "agent_operator_strategy_auto_apply": (
                        agent_operator_strategy_auto_apply
                    ),
                    "agent_operator_active_candidate_id": (
                        agent_operator_active_candidate_id
                    ),
                    "agent_operator_active_candidate_scenario": (
                        agent_operator_active_candidate_scenario
                    ),
                },
                "agent_operator": agent_operator_result,
                "agent_operators_running": agent_operators_running,
                "agent_operators": agent_operators,
                "agent_operator_mode": agent_operator_mode,
                "agent_operator_strategy_auto_apply": (
                    agent_operator_strategy_auto_apply
                ),
                "agent_operator_strategy_scenario_applied": (
                    strategy_scenario_applied
                ),
                "agent_operator_strategy_scenario_hint": strategy_scenario_hint,
                "agent_operator_strategy_candidate_id": (
                    strategy_scenario_candidate_id
                ),
                "agent_operator_strategy_scenario_rejected_reason": (
                    strategy_scenario_rejected_reason
                ),
                "agent_operator_learning_recommendation": (
                    agent_operator_learning_recommendation
                ),
                "agent_operator_learning_candidate": (
                    agent_operator_learning_candidate
                ),
                "agent_operator_learning_record_error": (
                    agent_operator_learning_record_error
                ),
                "agent_operator_learning_outcome_attribution": (
                    agent_operator_outcome_attribution
                ),
                "agent_operator_learning_outcome_attribution_error": (
                    agent_operator_outcome_attribution_error
                ),
                "execution": dict(execution_context),
                "mode_lifecycle": dict(mode_lifecycle_metadata),
                "stateful_cycle": {
                    "execution_scope": execution_scope,
                    "starting_open_notional": cycle_start_open_notional,
                    "starting_open_positions": cycle_start_open_positions,
                },
            },
        )
        result_hash = stable_hash(
            {
                "records": result_payload["records"],
                "final_portfolio": result_payload["final_portfolio"],
                "risk_allowed_count": result_payload["risk_allowed_count"],
                "filled_trade_count": result_payload["filled_trade_count"],
                "partial_fill_count": result_payload["partial_fill_count"],
                "exit_candidate_count": result_payload["exit_candidate_count"],
                "confirmed_exit_count": result_payload["confirmed_exit_count"],
                "forced_exit_count": result_payload["forced_exit_count"],
                "confirmed_exit_ratio": result_payload["confirmed_exit_ratio"],
                "confirmed_exit_latency_hours": result_payload[
                    "confirmed_exit_latency_hours"
                ],
                "median_position_age_hours": result_payload["median_position_age_hours"],
                "stale_position_count": result_payload["stale_position_count"],
                "stale_position_ratio": result_payload["stale_position_ratio"],
                "raw_probability_mean": result_payload["raw_probability_mean"],
                "calibrated_probability_mean": result_payload[
                    "calibrated_probability_mean"
                ],
                "probability_drift_mean": result_payload["probability_drift_mean"],
                "probability_drift_abs_mean": result_payload[
                    "probability_drift_abs_mean"
                ],
                "probability_drift_max_abs": result_payload[
                    "probability_drift_max_abs"
                ],
                "weighted_check_agreement_mean": result_payload[
                    "weighted_check_agreement_mean"
                ],
                "calibration_applied_ratio": result_payload[
                    "calibration_applied_ratio"
                ],
                "total_execution_cost": result_payload["total_execution_cost"],
                "attributed_trade_count": result_payload["attributed_trade_count"],
                "expected_gross_edge_value": result_payload[
                    "expected_gross_edge_value"
                ],
                "expected_net_edge_value": result_payload["expected_net_edge_value"],
                "expected_net_edge_value_on_fills": result_payload[
                    "expected_net_edge_value_on_fills"
                ],
                "expected_value_after_execution_cost": result_payload[
                    "expected_value_after_execution_cost"
                ],
                "average_expected_gross_edge_bps": result_payload[
                    "average_expected_gross_edge_bps"
                ],
                "average_expected_net_edge_bps": result_payload[
                    "average_expected_net_edge_bps"
                ],
                "expected_edge_capture_ratio": result_payload[
                    "expected_edge_capture_ratio"
                ],
                "execution_cost_to_expected_net_ratio": result_payload[
                    "execution_cost_to_expected_net_ratio"
                ],
                "input_fingerprint": input_fingerprint,
                "cycle_index": cycle_index,
            }
        )
        result_payload["reproducibility"] = {
            "input_fingerprint": input_fingerprint,
            "events_hash": events_hash,
            "profile_hash": profile_hash,
            "calibration_policy_hash": calibration_policy_hash,
            "scenario_hash": scenario_hash,
            "result_hash": result_hash,
            "cycle_index": cycle_index,
        }
        final_portfolio = run.final_portfolio
        net_pnl = round(
            final_portfolio.current_equity - final_portfolio.day_start_equity, 4
        )
        total_exposure_fraction = round(final_portfolio.total_exposure_fraction, 6)
        daily_drawdown_fraction = round(final_portfolio.daily_drawdown_fraction, 6)

        if args.cycle_output_dir:
            output_path = args.cycle_output_dir / f"cycle_{cycle_index:03d}.json"
            output_path.write_text(
                json.dumps(result_payload, indent=2) + "\n", encoding="utf-8"
            )

        heartbeat(
            "cycle_completed",
            {
                "cycle_index": cycle_index,
                "selected_scenario": scenario_name_in_use,
                "control_version": control_version,
                "kill_switch_active": kill_switch_active,
                "cancel_all_requested": cancel_all_requested,
                "cancel_all_acknowledged": cancel_all_acknowledged,
                "cancelled_order_count": int(
                    (cancel_all_summary or {}).get("cancelled_order_count", 0)
                ),
                "mode_lifecycle_current_mode": mode_current,
                "mode_lifecycle_target_mode": mode_target,
                "mode_lifecycle_effective_mode": mode_effective,
                "mode_lifecycle_transition_allowed": mode_transition_allowed,
                "mode_lifecycle_transition_reason_codes": mode_transition_reason_codes,
                "mode_lifecycle_decision_hash": mode_transition_decision_hash,
                "mode_lifecycle_approval_status": mode_transition_approval_status,
                "mode_lifecycle_expected_execution_mode": expected_execution_mode,
                "mode_lifecycle_execution_mode": resolved_execution_mode,
                "mode_lifecycle_execution_mode_matches": execution_mode_matches_lifecycle,
                "events": len(run.records),
                "risk_allowed_count": run.risk_allowed_count,
                "filled_trade_count": run.filled_trade_count,
                "exit_candidate_count": run.exit_candidate_count,
                "confirmed_exit_count": run.confirmed_exit_count,
                "forced_exit_count": run.forced_exit_count,
                "confirmed_exit_ratio": run.confirmed_exit_ratio,
                "confirmed_exit_latency_hours": run.confirmed_exit_latency_hours,
                "median_position_age_hours": run.median_position_age_hours,
                "stale_position_count": run.stale_position_count,
                "stale_position_ratio": run.stale_position_ratio,
                "raw_probability_mean": run.raw_probability_mean,
                "calibrated_probability_mean": run.calibrated_probability_mean,
                "probability_drift_mean": run.probability_drift_mean,
                "probability_drift_abs_mean": run.probability_drift_abs_mean,
                "probability_drift_max_abs": run.probability_drift_max_abs,
                "weighted_check_agreement_mean": run.weighted_check_agreement_mean,
                "calibration_applied_ratio": run.calibration_applied_ratio,
                "total_execution_cost": run.total_execution_cost,
                "total_fees_paid": run.total_fees_paid,
                "total_slippage_cost": run.total_slippage_cost,
                "attributed_trade_count": run.attributed_trade_count,
                "expected_gross_edge_value": run.expected_gross_edge_value,
                "expected_net_edge_value": run.expected_net_edge_value,
                "expected_net_edge_value_on_fills": (
                    run.expected_net_edge_value_on_fills
                ),
                "expected_value_after_execution_cost": (
                    run.expected_value_after_execution_cost
                ),
                "average_expected_gross_edge_bps": (
                    run.average_expected_gross_edge_bps
                ),
                "average_expected_net_edge_bps": run.average_expected_net_edge_bps,
                "expected_edge_capture_ratio": run.expected_edge_capture_ratio,
                "execution_cost_to_expected_net_ratio": (
                    run.execution_cost_to_expected_net_ratio
                ),
                "net_pnl": net_pnl,
                "current_equity": final_portfolio.current_equity,
                "open_notional": final_portfolio.open_notional,
                "open_positions": final_portfolio.open_positions,
                "total_exposure_fraction": total_exposure_fraction,
                "daily_drawdown_fraction": daily_drawdown_fraction,
                "result_hash_prefix": result_hash[:12],
                "agent_operator_status": agent_operator_result.get("status"),
                "agent_operator_mode": agent_operator_mode,
                "agent_operator_provider": agent_operator_result.get("provider"),
                "agent_operator_model": agent_operator_result.get("model"),
                "agent_operators_running": agent_operators_running,
                "agent_operators": agent_operators,
                "agent_operator_risk_posture": agent_operator_result.get(
                    "risk_posture"
                ),
                "agent_operator_confidence": agent_operator_result.get("confidence"),
                "agent_operator_strategy_auto_apply": (
                    agent_operator_strategy_auto_apply
                ),
                "agent_operator_active_candidate_id": (
                    agent_operator_active_candidate_id
                ),
                "agent_operator_active_candidate_scenario": (
                    agent_operator_active_candidate_scenario
                ),
                "agent_operator_strategy_scenario_applied": (
                    strategy_scenario_applied
                ),
                "agent_operator_strategy_scenario_hint": strategy_scenario_hint,
                "agent_operator_strategy_scenario_rejected_reason": (
                    strategy_scenario_rejected_reason
                ),
                "agent_operator_learning_recommendation_id": str(
                    (agent_operator_learning_recommendation or {}).get(
                        "recommendation_id",
                        "",
                    )
                ).strip(),
                "agent_operator_learning_candidate_id": str(
                    (agent_operator_learning_candidate or {}).get(
                        "candidate_id",
                        "",
                    )
                ).strip(),
                "agent_operator_learning_record_error": (
                    agent_operator_learning_record_error
                ),
                "agent_operator_learning_outcomes_attributed_count": int(
                    agent_operator_outcome_attribution.get("attributed_count", 0)
                    or 0
                ),
                "agent_operator_learning_outcome_attribution_error": (
                    agent_operator_outcome_attribution_error
                ),
                "ingestion_status": effective_ingestion_status,
                "ingestion_reasons": effective_ingestion_reasons,
                "ingestion_degraded_streak": ingestion_degraded_streak,
                "ingestion_degraded_entry_suppressed": (
                    ingestion_degraded_entry_suppressed
                ),
                "state_refresh_applied": state_refresh_applied,
                "state_refresh_event_count": state_refresh_event_count,
                "state_refresh_market_ids": state_refresh_market_ids,
                "state_refresh_max_streak": state_refresh_max_streak,
                "stale_open_position_market_ids": stale_open_position_market_ids,
            },
        )
        portfolio_state = run.final_portfolio.clone()
        open_positions_state = dict(run.final_open_positions)
        if args.ingestion_mode == "live_polymarket":
            final_open_market_ids = set(open_positions_state.keys())
            for market_id in list(state_refresh_streak_by_market):
                if market_id not in final_open_market_ids:
                    state_refresh_streak_by_market.pop(market_id, None)
        if freshness_filter_enabled and freshness_committed_event_ids:
            seen_live_event_ids.update(freshness_committed_event_ids)
        return {
            "cycle_index": cycle_index,
            "cycle_status": "EXECUTED",
            "selected_scenario": scenario_name_in_use,
            "control_version": control_version,
            "kill_switch_active": kill_switch_active,
            "cancel_all_requested": cancel_all_requested,
            "cancel_all_acknowledged": cancel_all_acknowledged,
            "cancelled_order_count": int(
                (cancel_all_summary or {}).get("cancelled_order_count", 0)
            ),
            "events": len(run.records),
            "risk_allowed_count": run.risk_allowed_count,
            "filled_trade_count": run.filled_trade_count,
            "partial_fill_count": run.partial_fill_count,
            "exit_candidate_count": run.exit_candidate_count,
            "confirmed_exit_count": run.confirmed_exit_count,
            "forced_exit_count": run.forced_exit_count,
            "confirmed_exit_ratio": run.confirmed_exit_ratio,
            "confirmed_exit_latency_hours": run.confirmed_exit_latency_hours,
            "median_position_age_hours": run.median_position_age_hours,
            "stale_position_count": run.stale_position_count,
            "stale_position_ratio": run.stale_position_ratio,
            "raw_probability_mean": run.raw_probability_mean,
            "calibrated_probability_mean": run.calibrated_probability_mean,
            "probability_drift_mean": run.probability_drift_mean,
            "probability_drift_abs_mean": run.probability_drift_abs_mean,
            "probability_drift_max_abs": run.probability_drift_max_abs,
            "weighted_check_agreement_mean": run.weighted_check_agreement_mean,
            "calibration_applied_ratio": run.calibration_applied_ratio,
            "total_execution_cost": run.total_execution_cost,
            "total_fees_paid": run.total_fees_paid,
            "total_slippage_cost": run.total_slippage_cost,
            "attributed_trade_count": run.attributed_trade_count,
            "expected_gross_edge_value": run.expected_gross_edge_value,
            "expected_net_edge_value": run.expected_net_edge_value,
            "expected_net_edge_value_on_fills": run.expected_net_edge_value_on_fills,
            "expected_value_after_execution_cost": (
                run.expected_value_after_execution_cost
            ),
            "average_expected_gross_edge_bps": run.average_expected_gross_edge_bps,
            "average_expected_net_edge_bps": run.average_expected_net_edge_bps,
            "expected_edge_capture_ratio": run.expected_edge_capture_ratio,
            "execution_cost_to_expected_net_ratio": (
                run.execution_cost_to_expected_net_ratio
            ),
            "bankroll": final_portfolio.bankroll,
            "day_start_equity": final_portfolio.day_start_equity,
            "current_equity": final_portfolio.current_equity,
            "net_pnl": net_pnl,
            "open_notional": final_portfolio.open_notional,
            "open_positions": final_portfolio.open_positions,
            "total_exposure_fraction": total_exposure_fraction,
            "daily_drawdown_fraction": daily_drawdown_fraction,
            "result_hash": result_hash,
            "agent_operator": agent_operator_result,
            "agent_operators_running": agent_operators_running,
            "agent_operators": agent_operators,
            "agent_operator_status": agent_operator_result.get("status"),
            "agent_operator_mode": agent_operator_mode,
            "agent_operator_provider": agent_operator_result.get("provider"),
            "agent_operator_model": agent_operator_result.get("model"),
            "agent_operator_risk_posture": agent_operator_result.get(
                "risk_posture"
            ),
            "agent_operator_confidence": agent_operator_result.get("confidence"),
            "agent_operator_strategy_auto_apply": (
                agent_operator_strategy_auto_apply
            ),
            "agent_operator_active_candidate_id": agent_operator_active_candidate_id,
            "agent_operator_active_candidate_scenario": (
                agent_operator_active_candidate_scenario
            ),
            "agent_operator_strategy_scenario_applied": strategy_scenario_applied,
            "agent_operator_strategy_scenario_hint": strategy_scenario_hint,
            "agent_operator_strategy_candidate_id": strategy_scenario_candidate_id,
            "agent_operator_strategy_scenario_rejected_reason": (
                strategy_scenario_rejected_reason
            ),
            "agent_operator_learning_recommendation": (
                agent_operator_learning_recommendation
            ),
            "agent_operator_learning_candidate": agent_operator_learning_candidate,
            "agent_operator_learning_record_error": (
                agent_operator_learning_record_error
            ),
            "agent_operator_learning_outcome_attribution": (
                agent_operator_outcome_attribution
            ),
            "agent_operator_learning_outcome_attribution_error": (
                agent_operator_outcome_attribution_error
            ),
            "ingestion_status": effective_ingestion_status,
            "ingestion_reasons": effective_ingestion_reasons,
            "ingestion_degraded_streak": ingestion_degraded_streak,
            "ingestion_degraded_entry_suppressed": (
                ingestion_degraded_entry_suppressed
            ),
            "state_refresh_applied": state_refresh_applied,
            "state_refresh_event_count": state_refresh_event_count,
            "state_refresh_market_ids": state_refresh_market_ids,
            "state_refresh_max_streak": state_refresh_max_streak,
            "stale_open_position_market_ids": stale_open_position_market_ids,
            **mode_lifecycle_metadata,
        }

    worker = WorkerSpec(
        name="test_token_loop",
        run=_run_test_token_cycle,
        max_retries=args.max_retries,
        retry_backoff_seconds=args.retry_backoff_seconds,
        heartbeat_timeout_seconds=args.heartbeat_timeout_seconds,
    )
    supervisor = RuntimeSupervisor(
        journal_path=args.journal_path,
        state_path=args.state_path,
    )
    snapshots: list[dict] = []
    for cycle_index in range(1, args.cycles + 1):
        current_cycle["index"] = cycle_index
        snapshot = supervisor.run_cycle([worker], cycle_index=cycle_index)
        snapshots.append(snapshot)
        if stop_flags["restart_requested"]:
            break
        if not args.continue_on_failure and snapshot["status"] == "FAILED":
            break
        if cycle_index < args.cycles and args.cycle_interval_seconds > 0:
            time.sleep(args.cycle_interval_seconds)

    overall_status = (
        "SUCCESS"
        if snapshots and all(s["status"] == "SUCCESS" for s in snapshots)
        else "FAILED"
    )
    summary = {
        "schema_version": "runtime_supervisor_state.v1",
        "generated_at": datetime.now(UTC).isoformat(timespec="milliseconds"),
        "cycles_requested": args.cycles,
        "cycles_completed": len(snapshots),
        "overall_status": overall_status,
        "last_snapshot": snapshots[-1] if snapshots else None,
        "stopped_by_control_restart": stop_flags["restart_requested"],
    }
    last_snapshot = summary.get("last_snapshot") or {}
    failed_workers = last_snapshot.get("failed_workers", [])
    print(
        "Runtime supervision complete: "
        f"cycles_requested={summary['cycles_requested']} "
        f"cycles_completed={summary['cycles_completed']} "
        f"overall_status={summary['overall_status']} "
        f"stopped_by_control_restart={summary['stopped_by_control_restart']} "
        f"failed_workers={len(failed_workers)} "
        f"ingestion_mode={args.ingestion_mode} "
        f"execution_mode={execution_context['mode']} "
        f"state_path={args.state_path} "
        f"journal_path={args.journal_path}"
    )
    return 0 if overall_status == "SUCCESS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
