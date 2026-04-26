from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from .contracts import MarketEvent, PortfolioState
from .llm_policy import CalibrationPolicy
from .replay_harness import ReplayHarness
from .reproducibility import hash_events, stable_hash
from .risk_engine import RiskEngine
from .scenario_pack import ScenarioPack, apply_scenario_to_events
from .schemas import SCENARIO_MATRIX_REPORT_SCHEMA_VERSION
from .strategy_baseline import BaselineStrategy


def _execute_single_scenario(
    *,
    events: list[MarketEvent],
    parameters: dict[str, Any],
    calibration_policy: CalibrationPolicy | None,
    profile_payload: dict[str, Any],
    calibration_policy_payload: dict[str, Any],
    scenario_name: str,
    scenario_pack_path: str,
    events_path: str,
    profile_path: str,
    calibration_policy_path: str,
    bankroll: float,
) -> dict[str, Any]:
    strategy = BaselineStrategy(parameters, calibration_policy)
    risk = RiskEngine(parameters)
    harness = ReplayHarness(strategy, risk)

    events_hash = hash_events(events)
    profile_hash = stable_hash(profile_payload)
    calibration_policy_hash = stable_hash(calibration_policy_payload)
    input_fingerprint = stable_hash(
        {
            "events_hash": events_hash,
            "profile_hash": profile_hash,
            "calibration_policy_hash": calibration_policy_hash,
            "scenario_name": scenario_name,
            "bankroll": bankroll,
        }
    )

    run = harness.run(
        events,
        PortfolioState(
            bankroll=bankroll,
            day_start_equity=bankroll,
            current_equity=bankroll,
        ),
    )

    result_hash = stable_hash(
        {
            "scenario_name": scenario_name,
            "records": [
                {
                    "event_id": record.event_id,
                    "timestamp": record.timestamp,
                    "market_id": record.market_id,
                    "strategy_action": record.strategy_decision.action,
                    "risk_allowed": record.risk_decision.allowed,
                    "approved_notional": record.risk_decision.approved_notional,
                }
                for record in run.records
            ],
            "final_portfolio": {
                "open_positions": run.final_portfolio.open_positions,
                "open_notional": run.final_portfolio.open_notional,
            },
            "allowed_trade_count": run.allowed_trade_count,
            "input_fingerprint": input_fingerprint,
        }
    )

    return {
        "scenario_name": scenario_name,
        "allowed_trade_count": run.allowed_trade_count,
        "open_positions": run.final_portfolio.open_positions,
        "open_notional": run.final_portfolio.open_notional,
        "context": {
            "scenario_pack": scenario_pack_path,
            "events": events_path,
            "profile": profile_path,
            "calibration_policy": calibration_policy_path,
        },
        "reproducibility": {
            "input_fingerprint": input_fingerprint,
            "events_hash": events_hash,
            "profile_hash": profile_hash,
            "calibration_policy_hash": calibration_policy_hash,
            "result_hash": result_hash,
        },
    }


def build_scenario_matrix_report(
    *,
    base_events: list[MarketEvent],
    parameters: dict[str, Any],
    calibration_policy: CalibrationPolicy | None,
    profile_payload: dict[str, Any],
    calibration_policy_payload: dict[str, Any],
    scenario_pack: ScenarioPack,
    scenario_pack_path: str,
    events_path: str,
    profile_path: str,
    calibration_policy_path: str,
    bankroll: float,
    scenario_names: list[str] | None = None,
) -> dict[str, Any]:
    selected_scenarios = scenario_names or sorted(scenario_pack.scenarios.keys())
    outcomes: list[dict[str, Any]] = []

    for name in selected_scenarios:
        scenario = scenario_pack.get_scenario(name)
        transformed_events = apply_scenario_to_events(base_events, scenario)
        outcomes.append(
            _execute_single_scenario(
                events=transformed_events,
                parameters=parameters,
                calibration_policy=calibration_policy,
                profile_payload=profile_payload,
                calibration_policy_payload=calibration_policy_payload,
                scenario_name=name,
                scenario_pack_path=scenario_pack_path,
                events_path=events_path,
                profile_path=profile_path,
                calibration_policy_path=calibration_policy_path,
                bankroll=bankroll,
            )
        )

    aggregate = {
        "scenario_count": len(outcomes),
        "total_allowed_trades": sum(
            outcome["allowed_trade_count"] for outcome in outcomes
        ),
        "max_open_notional": max(
            (outcome["open_notional"] for outcome in outcomes), default=0.0
        ),
        "min_open_notional": min(
            (outcome["open_notional"] for outcome in outcomes), default=0.0
        ),
        "zero_trade_scenarios": [
            outcome["scenario_name"]
            for outcome in outcomes
            if outcome["allowed_trade_count"] == 0
        ],
    }

    report_hash = stable_hash(
        {
            "selected_scenarios": selected_scenarios,
            "outcomes": outcomes,
            "aggregate": aggregate,
            "scenario_pack": scenario_pack_path,
            "events": events_path,
            "profile": profile_path,
            "calibration_policy": calibration_policy_path,
        }
    )

    return {
        "schema_version": SCENARIO_MATRIX_REPORT_SCHEMA_VERSION,
        "generated_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "selected_scenarios": selected_scenarios,
        "outcomes": outcomes,
        "aggregate": aggregate,
        "report_hash": report_hash,
    }
