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

from poly_robot.llm_policy import load_calibration_policy  # noqa: E402
from poly_robot.replay_harness import load_events_from_jsonl  # noqa: E402
from poly_robot.scenario_matrix import build_scenario_matrix_report  # noqa: E402
from poly_robot.scenario_pack import load_scenario_pack  # noqa: E402


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_profile_payload(profile_path: Path) -> tuple[dict, dict]:
    payload = _load_json(profile_path)
    values = payload.get("values")
    if not isinstance(values, dict):
        raise ValueError(f"Profile values must be an object in {profile_path}")
    return payload, values


def _parse_scenario_list(raw: str | None) -> list[str] | None:
    if raw is None:
        return None
    names = [item.strip() for item in raw.split(",") if item.strip()]
    return names or None


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run replay scenarios as a matrix and emit a reproducibility-linked stress report."
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
        "--scenarios",
        type=str,
        required=False,
        help="Optional comma-separated list of scenarios. Defaults to all scenarios.",
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
        help="Optional file path to persist matrix report JSON.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    profile_payload, parameters = _load_profile_payload(args.profile)
    calibration_policy_payload = _load_json(args.calibration_policy)
    calibration_policy = load_calibration_policy(args.calibration_policy)
    scenario_pack = load_scenario_pack(args.scenario_pack)
    base_events = load_events_from_jsonl(args.events)
    selected_scenarios = _parse_scenario_list(args.scenarios)

    report = build_scenario_matrix_report(
        base_events=base_events,
        parameters=parameters,
        calibration_policy=calibration_policy,
        profile_payload=profile_payload,
        calibration_policy_payload=calibration_policy_payload,
        scenario_pack=scenario_pack,
        scenario_pack_path=str(args.scenario_pack),
        events_path=str(args.events),
        profile_path=str(args.profile),
        calibration_policy_path=str(args.calibration_policy),
        bankroll=args.bankroll,
        scenario_names=selected_scenarios,
    )

    if args.output:
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    aggregate = report["aggregate"]
    print(
        "Scenario matrix complete: "
        f"scenarios={aggregate['scenario_count']} "
        f"total_allowed_trades={aggregate['total_allowed_trades']} "
        f"zero_trade_scenarios={len(aggregate['zero_trade_scenarios'])} "
        f"report_hash={report['report_hash'][:12]}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
