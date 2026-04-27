#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import UTC, datetime
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from poly_robot.contracts import MarketEvent, PortfolioState  # noqa: E402
from poly_robot.integration_adapters import (  # noqa: E402
    HardenedExecutionAdapter,
    HistoricalIngestionAdapter,
    LivePolymarketIngestionAdapter,
    PolymarketClobExecutionAdapter,
)
from poly_robot.llm_policy import load_calibration_policy  # noqa: E402
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


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


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
        choices=["paper", "live_polymarket_clob"],
        required=False,
        help=(
            "Execution adapter mode; defaults to rollout config "
            "default_execution_mode when omitted."
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
            "Optional rollout stage override for live_polymarket_clob "
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
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    if args.cycle_interval_seconds < 0:
        raise ValueError("--cycle-interval-seconds must be >= 0")
    if args.live_wallet_convergence_threshold <= 0:
        raise ValueError("--live-wallet-convergence-threshold must be > 0")
    if args.ingestion_mode == "historical_jsonl" and args.events is None:
        raise ValueError(
            "--events is required when --ingestion-mode=historical_jsonl"
        )
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
    control_manager = OperatorControlManager(
        control_state_path=args.control_state_path,
        audit_path=args.control_audit_path,
    )

    strategy = BaselineStrategy(parameters, calibration_policy)
    risk = RiskEngine(parameters)
    rollout_payload = _load_json(args.live_rollout_config)
    rollout_default_execution_mode = str(
        rollout_payload.get("default_execution_mode", "paper")
    ).strip() or "paper"
    resolved_execution_mode = str(
        args.execution_mode or rollout_default_execution_mode
    ).strip()
    if resolved_execution_mode not in {"paper", "live_polymarket_clob"}:
        raise ValueError(
            "--execution-mode must be one of paper, live_polymarket_clob "
            f"(resolved={resolved_execution_mode!r})"
        )

    execution_context: dict[str, object]
    if resolved_execution_mode == "paper":
        execution_adapter = PaperExecutionAdapter(parameters)
        execution_context = {
            "mode": "paper",
            "rollout_config_path": str(args.live_rollout_config),
            "rollout_stage": "paper",
            "rollout_stage_enabled": True,
            "real_order_submission": False,
            "allow_real_trading": False,
            "required_env_vars": [],
            "clob_base_url": None,
            "clob_config_path": None,
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
        rollout_stage_name, rollout_stage_payload = _resolve_rollout_stage(
            rollout_payload,
            requested_stage=args.live_rollout_stage,
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
            secret_max_age_days = max(
                1,
                int(parsed_secret_max_age_seconds / 86_400),
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
        if isinstance(global_guards, dict):
            if bool(
                global_guards.get("require_pretrade_balance_and_allowance_checks", False)
            ):
                require_pretrade_balance_checks = True
            if bool(global_guards.get("require_user_channel_trade_ack", False)):
                require_user_channel_trade_ack = True
            if bool(global_guards.get("require_kill_switch", False)):
                require_kill_switch = True
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
            audit_log_path=execution_adapter_audit_path,
        )
        execution_context = {
            "mode": "live_polymarket_clob",
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
            "allow_plaintext_secrets": allow_plaintext_secrets,
            "preferred_secret_sources": list(preferred_secret_sources),
            "max_secret_age_days": secret_max_age_days,
            "user_channel_max_staleness_seconds": user_channel_max_staleness_seconds,
            "execution_adapter_audit_path": (
                str(execution_adapter_audit_path)
                if execution_adapter_audit_path is not None
                else None
            ),
        }
    execution = HardenedExecutionAdapter(
        execution_adapter,
        gateway_max_retry_attempts=args.execution_gateway_max_retries,
        gateway_retry_backoff_seconds=args.execution_gateway_retry_backoff_seconds,
        gateway_timeout_seconds=args.execution_gateway_timeout_seconds,
    )
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
        if args.ignore_operator_controls or not args.control_state_path.exists():
            return {
                "paused": False,
                "restart_requested": False,
                "kill_switch_active": False,
                "cancel_all_requested": False,
                "selected_scenario": control_default_scenario_name,
                "control_version": 0,
            }

        control_state = control_manager.load_control_state()
        selected_scenario = str(control_state.get("selected_scenario", "")).strip()
        if not selected_scenario:
            control_state["selected_scenario"] = control_default_scenario_name
        if "kill_switch_active" not in control_state:
            control_state["kill_switch_active"] = False
        if "cancel_all_requested" not in control_state:
            control_state["cancel_all_requested"] = False
        return control_state

    if args.cycle_output_dir:
        args.cycle_output_dir.mkdir(parents=True, exist_ok=True)

    def _run_test_token_cycle(heartbeat) -> dict:
        nonlocal portfolio_state, open_positions_state, seen_live_event_ids
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
            },
        )

        if restart_requested:
            if not args.ignore_operator_controls and args.control_state_path.exists():
                control_manager.acknowledge_restart(
                    actor=args.operator_control_actor,
                    note=f"acknowledged_before_cycle_{cycle_index}",
                )
            stop_flags["restart_requested"] = True
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
            }

        if paused:
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
        if freshness_filter_enabled and freshness_skipped_event_ids > 0:
            effective_ingestion_reasons.append("seen_event_ids_skipped")
            if effective_ingestion_status == "OK":
                effective_ingestion_status = "DEGRADED"
        if (
            freshness_filter_enabled
            and args.ingestion_mode == "live_polymarket"
            and not events_for_run
            and cycle_ingestion.events
        ):
            effective_ingestion_reasons.append("no_new_events_since_last_cycle")
            if effective_ingestion_status == "OK":
                effective_ingestion_status = "DEGRADED"
        effective_ingestion_reasons = list(dict.fromkeys(effective_ingestion_reasons))

        execution_scope = f"cycle:{cycle_index}"
        scoped_events: list[MarketEvent] = []
        for event in events_for_run:
            event_payload = event.to_dict()
            event_metadata = dict(event_payload.get("metadata", {}))
            event_metadata["execution_scope"] = execution_scope
            event_metadata["cycle_index"] = cycle_index
            event_metadata["kill_switch_active"] = kill_switch_active
            event_metadata["cancel_all_requested"] = cancel_all_requested
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
                },
                "execution": dict(execution_context),
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
                "events": len(run.records),
                "risk_allowed_count": run.risk_allowed_count,
                "filled_trade_count": run.filled_trade_count,
                "exit_candidate_count": run.exit_candidate_count,
                "confirmed_exit_count": run.confirmed_exit_count,
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
            },
        )
        portfolio_state = run.final_portfolio.clone()
        open_positions_state = dict(run.final_open_positions)
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
