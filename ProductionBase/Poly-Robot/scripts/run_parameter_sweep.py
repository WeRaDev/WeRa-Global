#!/usr/bin/env python3
"""Parameter sweep runner for Poly-Robot configuration optimization.

Varies configurable parameters across a matrix of values, runs the
scenario matrix for each configuration, and emits a ranked comparison
report ordering configurations by expected value and trade cadence.
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
from datetime import UTC, datetime
from itertools import product
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from poly_robot.shared.reproducibility import stable_hash  # noqa: E402


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="milliseconds")


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


DEFAULT_SWEEP_AXES = {
    "risk.max_portfolio_exposure_fraction": [0.4, 0.5, 0.6],
    "exit.target_capture_ratio": [0.6, 0.7, 0.85],
    "exit.stale_hours": [12, 16, 24],
}


def _build_configurations(
    base_profile: dict[str, Any],
    sweep_axes: dict[str, list[Any]],
) -> list[dict[str, Any]]:
    """Generate all combinations from sweep axes applied to base profile."""
    axis_keys = list(sweep_axes.keys())
    axis_values = [sweep_axes[key] for key in axis_keys]
    configs: list[dict[str, Any]] = []

    for combination in product(*axis_values):
        profile = copy.deepcopy(base_profile)
        values = profile.get("values", {})
        overrides: dict[str, Any] = {}
        for key, value in zip(axis_keys, combination):
            values[key] = value
            overrides[key] = value
        config_id = stable_hash(overrides)[:12]
        configs.append({
            "config_id": config_id,
            "overrides": overrides,
            "profile": profile,
        })

    return configs


def _run_scenario_matrix_for_config(
    config: dict[str, Any],
    *,
    events_path: Path,
    calibration_policy_path: Path,
    scenario_pack_path: Path,
    base_events: list | None = None,
    scenario_pack: Any | None = None,
    calibration_policy_payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run scenario matrix in-process for a single configuration."""
    from poly_robot.llm_policy import load_calibration_policy
    from poly_robot.replay_harness import load_events_from_jsonl
    from poly_robot.scenario_matrix import build_scenario_matrix_report
    from poly_robot.scenario_pack import load_scenario_pack

    profile = config["profile"]
    profile_values = profile.get("values", {})

    if base_events is None:
        base_events = load_events_from_jsonl(events_path)
    if calibration_policy_payload is None:
        calibration_policy_payload = _load_json(calibration_policy_path)
    if scenario_pack is None:
        scenario_pack = load_scenario_pack(scenario_pack_path)

    calibration_policy = load_calibration_policy(calibration_policy_path)

    return build_scenario_matrix_report(
        base_events=base_events,
        parameters=profile_values,
        calibration_policy=calibration_policy,
        profile_payload=profile,
        calibration_policy_payload=calibration_policy_payload,
        scenario_pack=scenario_pack,
        scenario_pack_path=str(scenario_pack_path),
        events_path=str(events_path),
        profile_path="<sweep-generated>",
        calibration_policy_path=str(calibration_policy_path),
        bankroll=1000.0,
    )


def _extract_metrics(matrix_result: dict[str, Any]) -> dict[str, Any]:
    """Extract key comparison metrics from a scenario matrix result."""
    outcomes = matrix_result.get("outcomes", [])
    total_trades = sum(int(o.get("allowed_trade_count", 0)) for o in outcomes)
    zero_trade_count = sum(1 for o in outcomes if int(o.get("allowed_trade_count", 0)) == 0)
    max_notional = max(
        (float(o.get("open_notional", 0.0)) for o in outcomes),
        default=0.0,
    )
    return {
        "scenario_count": len(outcomes),
        "total_trades": total_trades,
        "zero_trade_scenarios": zero_trade_count,
        "max_open_notional": round(max_notional, 2),
        "trades_per_scenario": round(total_trades / max(1, len(outcomes)), 2),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run parameter sweep across configuration matrix"
    )
    parser.add_argument(
        "--events", type=Path, required=True, help="Replay events JSONL path"
    )
    parser.add_argument(
        "--profile", type=Path, required=True, help="Base parameter profile JSON"
    )
    parser.add_argument(
        "--calibration-policy", type=Path, required=True, help="Calibration policy JSON"
    )
    parser.add_argument(
        "--scenario-pack", type=Path, required=True, help="Scenario pack JSON"
    )
    parser.add_argument(
        "--sweep-config",
        type=Path,
        required=False,
        help="Optional JSON file with sweep axes (keys -> list of values). Defaults to built-in axes.",
    )
    parser.add_argument(
        "--output", type=Path, required=True, help="Output comparison report JSON"
    )
    args = parser.parse_args(argv)

    base_profile = _load_json(args.profile)
    sweep_axes = DEFAULT_SWEEP_AXES
    if args.sweep_config and args.sweep_config.exists():
        sweep_axes = _load_json(args.sweep_config)

    configurations = _build_configurations(base_profile, sweep_axes)
    print(
        f"Sweep: {len(configurations)} configurations from "
        f"{len(sweep_axes)} axes"
    )

    results: list[dict[str, Any]] = []
    for idx, config in enumerate(configurations):
        try:
            matrix_result = _run_scenario_matrix_for_config(
                config,
                events_path=args.events,
                calibration_policy_path=args.calibration_policy,
                scenario_pack_path=args.scenario_pack,
            )
            metrics = _extract_metrics(matrix_result)
            results.append({
                "config_id": config["config_id"],
                "overrides": config["overrides"],
                "metrics": metrics,
                "status": "OK",
            })
        except Exception as exc:
            results.append({
                "config_id": config["config_id"],
                "overrides": config["overrides"],
                "metrics": None,
                "status": f"ERROR: {exc}",
            })
        if (idx + 1) % 5 == 0 or idx == len(configurations) - 1:
            print(f"  completed {idx + 1}/{len(configurations)}")

    # Rank by total_trades descending (cadence), then trades_per_scenario
    ranked = sorted(
        [r for r in results if r["status"] == "OK"],
        key=lambda r: (
            -(r["metrics"]["total_trades"]),
            -(r["metrics"]["trades_per_scenario"]),
        ),
    )

    report = {
        "schema_version": "parameter_sweep_report.v1",
        "generated_at": _utc_now_iso(),
        "sweep_axes": sweep_axes,
        "configuration_count": len(configurations),
        "successful_count": len(ranked),
        "failed_count": len(results) - len(ranked),
        "ranking": ranked,
        "best_config": ranked[0] if ranked else None,
        "baseline_config": next(
            (r for r in results if r["config_id"] == configurations[0]["config_id"]),
            None,
        ),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    best = ranked[0] if ranked else None
    best_trades = best["metrics"]["total_trades"] if best else 0
    print(
        f"Sweep complete: configs={len(configurations)} "
        f"best_trades={best_trades} "
        f"output={args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
