#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from poly_robot.contracts import PortfolioState  # noqa: E402
from poly_robot.integration_adapters import (  # noqa: E402
    HardenedExecutionAdapter,
    HistoricalIngestionAdapter,
)
from poly_robot.llm_policy import load_calibration_policy  # noqa: E402
from poly_robot.paper_execution import PaperExecutionAdapter  # noqa: E402
from poly_robot.reproducibility import hash_events, stable_hash  # noqa: E402
from poly_robot.risk_engine import RiskEngine  # noqa: E402
from poly_robot.scenario_pack import apply_scenario_to_events, load_scenario_pack  # noqa: E402
from poly_robot.strategy_baseline import BaselineStrategy  # noqa: E402
from poly_robot.test_token_loop import (  # noqa: E402
    TestTokenLoop,
    serialize_test_token_loop_run,
)


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_profile_payload(profile_path: Path) -> tuple[dict, dict]:
    payload = _load_json(profile_path)
    values = payload.get("values")
    if not isinstance(values, dict):
        raise ValueError(f"Profile values must be an object in {profile_path}")
    return payload, values


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run Poly-Robot end-to-end test-token loop "
            "(strategy -> risk -> paper execution) with reproducible output."
        )
    )
    parser.add_argument(
        "--events", type=Path, required=True, help="Path to replay event JSONL file."
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
        "--output",
        type=Path,
        required=False,
        help="Optional path to save end-to-end loop result JSON.",
    )
    parser.add_argument(
        "--ingestion-max-retries",
        type=int,
        default=1,
        help="Maximum number of retries for ingestion file read failures/timeouts.",
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
    profile_payload, parameters = _load_profile_payload(args.profile)
    calibration_policy_payload = _load_json(args.calibration_policy)
    calibration_policy = load_calibration_policy(args.calibration_policy)
    scenario_pack = load_scenario_pack(args.scenario_pack)
    scenario = scenario_pack.get_scenario(args.scenario)
    ingestion_adapter = HistoricalIngestionAdapter(
        max_retry_attempts=args.ingestion_max_retries,
        retry_backoff_seconds=args.ingestion_retry_backoff_seconds,
        max_invalid_rows=args.ingestion_max_invalid_rows,
        deduplicate_event_ids=True,
        fail_on_monotonic_violation=False,
    )
    ingestion = ingestion_adapter.load_jsonl(
        args.events,
        timeout_seconds=args.ingestion_timeout_seconds,
    )
    if ingestion.status == "FAILED":
        raise ValueError(
            "Ingestion adapter failed: "
            f"reasons={list(ingestion.reasons)} metadata={ingestion.metadata}"
        )

    events = ingestion.events
    events_for_run = apply_scenario_to_events(events, scenario)

    strategy = BaselineStrategy(parameters, calibration_policy)
    risk = RiskEngine(parameters)
    execution = HardenedExecutionAdapter(
        PaperExecutionAdapter(parameters),
        gateway_max_retry_attempts=args.execution_gateway_max_retries,
        gateway_retry_backoff_seconds=args.execution_gateway_retry_backoff_seconds,
        gateway_timeout_seconds=args.execution_gateway_timeout_seconds,
    )
    loop = TestTokenLoop(strategy, risk, execution, parameters)

    run = loop.run(
        events_for_run,
        PortfolioState(
            bankroll=args.bankroll,
            day_start_equity=args.bankroll,
            current_equity=args.bankroll,
        ),
    )

    events_hash = hash_events(events_for_run)
    profile_hash = stable_hash(profile_payload)
    calibration_policy_hash = stable_hash(calibration_policy_payload)
    scenario_hash = stable_hash(scenario.to_dict())
    input_fingerprint = stable_hash(
        {
            "events_hash": events_hash,
            "profile_hash": profile_hash,
            "calibration_policy_hash": calibration_policy_hash,
            "scenario_hash": scenario_hash,
            "bankroll": args.bankroll,
        }
    )

    run_context = {
        "scenario_name": scenario.name,
        "scenario_pack": str(args.scenario_pack),
        "input_events_path": str(args.events),
        "profile_path": str(args.profile),
        "calibration_policy_path": str(args.calibration_policy),
        "exit_module": {
            "target_capture_ratio": float(parameters["exit.target_capture_ratio"]),
            "volume_spike_multiplier": float(
                parameters["exit.volume_spike_multiplier"]
            ),
            "stale_hours": float(parameters["exit.stale_hours"]),
            "stale_price_change_threshold": float(
                parameters["exit.stale_price_change_threshold"]
            ),
            "confirmation_threshold": 2,
        },
        "ingestion_status": ingestion.status,
        "ingestion_reasons": list(ingestion.reasons),
        "ingestion_metadata": ingestion.metadata,
        "execution_gateway": {
            "max_retries": args.execution_gateway_max_retries,
            "retry_backoff_seconds": args.execution_gateway_retry_backoff_seconds,
            "timeout_seconds": args.execution_gateway_timeout_seconds,
        },
    }
    result_payload = serialize_test_token_loop_run(run, run_context=run_context)
    result_hash = stable_hash(
        {
            "records": result_payload["records"],
            "final_portfolio": result_payload["final_portfolio"],
            "risk_allowed_count": result_payload["risk_allowed_count"],
            "filled_trade_count": result_payload["filled_trade_count"],
            "partial_fill_count": result_payload["partial_fill_count"],
            "exit_candidate_count": result_payload["exit_candidate_count"],
            "confirmed_exit_count": result_payload["confirmed_exit_count"],
            "total_fees_paid": result_payload["total_fees_paid"],
            "total_slippage_cost": result_payload["total_slippage_cost"],
            "total_execution_cost": result_payload["total_execution_cost"],
            "attributed_trade_count": result_payload["attributed_trade_count"],
            "expected_gross_edge_value": result_payload["expected_gross_edge_value"],
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
        }
    )
    result_payload["reproducibility"] = {
        "input_fingerprint": input_fingerprint,
        "events_hash": events_hash,
        "profile_hash": profile_hash,
        "calibration_policy_hash": calibration_policy_hash,
        "scenario_hash": scenario_hash,
        "result_hash": result_hash,
    }

    if args.output:
        args.output.write_text(
            json.dumps(result_payload, indent=2) + "\n", encoding="utf-8"
        )

    edge_capture_display = (
        f"{run.expected_edge_capture_ratio:.4f}"
        if run.expected_edge_capture_ratio is not None
        else "n/a"
    )
    expected_net_ratio_display = (
        f"{run.execution_cost_to_expected_net_ratio:.4f}"
        if run.execution_cost_to_expected_net_ratio is not None
        else "n/a"
    )

    print(
        "Test-token loop complete: "
        f"events={len(run.records)} "
        f"risk_allowed={run.risk_allowed_count} "
        f"filled_trades={run.filled_trade_count} "
        f"partial_fills={run.partial_fill_count} "
        f"exit_candidates={run.exit_candidate_count} "
        f"confirmed_exits={run.confirmed_exit_count} "
        f"fees={run.total_fees_paid:.4f} "
        f"slippage_cost={run.total_slippage_cost:.4f} "
        f"execution_cost={run.total_execution_cost:.4f} "
        f"expected_gross_edge={run.expected_gross_edge_value:.4f} "
        f"expected_net_edge={run.expected_net_edge_value_on_fills:.4f} "
        f"expected_value_after_cost={run.expected_value_after_execution_cost:.4f} "
        f"edge_capture={edge_capture_display} "
        f"cost_to_expected_net={expected_net_ratio_display} "
        f"open_positions={run.final_portfolio.open_positions} "
        f"open_notional={run.final_portfolio.open_notional:.2f} "
        f"result_hash={result_hash[:12]}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
