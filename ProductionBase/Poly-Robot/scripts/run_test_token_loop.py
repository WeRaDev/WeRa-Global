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
from poly_robot.llm_policy import load_calibration_policy  # noqa: E402
from poly_robot.paper_execution import PaperExecutionAdapter  # noqa: E402
from poly_robot.replay_harness import load_events_from_jsonl  # noqa: E402
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
    parser.add_argument("--events", type=Path, required=True, help="Path to replay event JSONL file.")
    parser.add_argument(
        "--profile",
        type=Path,
        default=ROOT_DIR / "config" / "parameters" / "profiles" / "mvp_test_token.v1.json",
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
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    profile_payload, parameters = _load_profile_payload(args.profile)
    calibration_policy_payload = _load_json(args.calibration_policy)
    calibration_policy = load_calibration_policy(args.calibration_policy)
    scenario_pack = load_scenario_pack(args.scenario_pack)
    scenario = scenario_pack.get_scenario(args.scenario)
    events = load_events_from_jsonl(args.events)
    events_for_run = apply_scenario_to_events(events, scenario)

    strategy = BaselineStrategy(parameters, calibration_policy)
    risk = RiskEngine(parameters)
    execution = PaperExecutionAdapter(parameters)
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
    }
    result_payload = serialize_test_token_loop_run(run, run_context=run_context)
    result_hash = stable_hash(
        {
            "records": result_payload["records"],
            "final_portfolio": result_payload["final_portfolio"],
            "risk_allowed_count": result_payload["risk_allowed_count"],
            "filled_trade_count": result_payload["filled_trade_count"],
            "partial_fill_count": result_payload["partial_fill_count"],
            "total_fees_paid": result_payload["total_fees_paid"],
            "total_slippage_cost": result_payload["total_slippage_cost"],
            "total_execution_cost": result_payload["total_execution_cost"],
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
        args.output.write_text(json.dumps(result_payload, indent=2) + "\n", encoding="utf-8")

    print(
        "Test-token loop complete: "
        f"events={len(run.records)} "
        f"risk_allowed={run.risk_allowed_count} "
        f"filled_trades={run.filled_trade_count} "
        f"partial_fills={run.partial_fill_count} "
        f"fees={run.total_fees_paid:.4f} "
        f"slippage_cost={run.total_slippage_cost:.4f} "
        f"execution_cost={run.total_execution_cost:.4f} "
        f"open_positions={run.final_portfolio.open_positions} "
        f"open_notional={run.final_portfolio.open_notional:.2f} "
        f"result_hash={result_hash[:12]}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
