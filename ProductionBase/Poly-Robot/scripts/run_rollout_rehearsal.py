#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
RUNTIME_SUPERVISOR_SCRIPT = ROOT_DIR / "scripts" / "run_runtime_supervisor.py"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from poly_robot.schemas import (  # noqa: E402
    ROLLOUT_REHEARSAL_REPORT_SCHEMA_VERSION,
    RUNTIME_OPERATOR_CONTROL_STATE_SCHEMA_VERSION,
)


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="milliseconds")


def _tail(value: str, *, max_chars: int = 3000) -> str:
    cleaned = value.strip()
    if len(cleaned) <= max_chars:
        return cleaned
    return cleaned[-max_chars:]


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _extract_worker_loop_metadata(state_snapshot: dict[str, Any]) -> dict[str, Any]:
    worker_results = state_snapshot.get("worker_results")
    if not isinstance(worker_results, list):
        return {}
    for worker_result in worker_results:
        if worker_result.get("worker_name") != "test_token_loop":
            continue
        metadata = worker_result.get("last_metadata")
        if isinstance(metadata, dict):
            return metadata
    return {}


def _extract_heartbeat_stages(journal_rows: list[dict[str, Any]]) -> list[str]:
    stages: set[str] = set()
    for row in journal_rows:
        if row.get("event_type") != "worker_heartbeat":
            continue
        payload = row.get("payload")
        if not isinstance(payload, dict):
            continue
        stage = str(payload.get("stage", "")).strip()
        if stage:
            stages.add(stage)
    return sorted(stages)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run D3 rollout rehearsal drills through runtime supervisor control paths "
            "and produce deterministic evidence plus rollback recommendations."
        )
    )
    parser.add_argument(
        "--events",
        type=Path,
        default=ROOT_DIR / "tests" / "fixtures" / "replay_events.jsonl",
        help="Path to replay events fixture used for deterministic control drills.",
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
        help="Path to calibration policy JSON.",
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
        default="baseline",
        help="Scenario name used for all rehearsal drills.",
    )
    parser.add_argument(
        "--protocol-config",
        type=Path,
        default=ROOT_DIR / "config" / "integration" / "live_rollout_rehearsal.v1.json",
        help="Path to D3 rollout rehearsal protocol configuration JSON.",
    )
    parser.add_argument(
        "--work-dir",
        type=Path,
        default=ROOT_DIR / "runtime" / "rollout_rehearsal",
        help="Directory for per-scenario rehearsal runtime artifacts.",
    )
    parser.add_argument(
        "--output-path",
        type=Path,
        default=ROOT_DIR / "runtime" / "rollout_rehearsal_report.json",
        help="Output path for rollout rehearsal summary report.",
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=0,
        help="Maximum retries for runtime supervisor worker.",
    )
    parser.add_argument(
        "--retry-backoff-seconds",
        type=float,
        default=0.0,
        help="Retry backoff for runtime supervisor worker.",
    )
    parser.add_argument(
        "--ingestion-max-retries",
        type=int,
        default=0,
        help="Ingestion retry count for deterministic drills.",
    )
    parser.add_argument(
        "--ingestion-retry-backoff-seconds",
        type=float,
        default=0.0,
        help="Ingestion retry backoff for deterministic drills.",
    )
    parser.add_argument(
        "--execution-gateway-max-retries",
        type=int,
        default=0,
        help="Execution gateway retry count for deterministic drills.",
    )
    parser.add_argument(
        "--execution-gateway-retry-backoff-seconds",
        type=float,
        default=0.0,
        help="Execution gateway retry backoff for deterministic drills.",
    )
    parser.add_argument(
        "--operator-control-actor",
        type=str,
        default="rollout_rehearsal_runner",
        help="Actor identity used for rehearsal control acknowledgements.",
    )
    return parser


def _build_control_state(
    *,
    scenario_name: str,
    scenario_id: str,
    control_version: int,
    overrides: dict[str, Any],
) -> dict[str, Any]:
    control_state = {
        "schema_version": RUNTIME_OPERATOR_CONTROL_STATE_SCHEMA_VERSION,
        "updated_at": _utc_now_iso(),
        "control_version": control_version,
        "paused": False,
        "restart_requested": False,
        "kill_switch_active": False,
        "cancel_all_requested": False,
        "selected_scenario": scenario_name,
        "last_annotation": f"rollout_rehearsal:{scenario_id}",
    }
    for key in (
        "paused",
        "restart_requested",
        "kill_switch_active",
        "cancel_all_requested",
    ):
        if key in overrides:
            control_state[key] = bool(overrides[key])
    return control_state


def _build_supervisor_command(
    *,
    args: argparse.Namespace,
    state_path: Path,
    journal_path: Path,
    control_state_path: Path,
    control_audit_path: Path,
    cycle_output_dir: Path,
) -> list[str]:
    return [
        sys.executable,
        str(RUNTIME_SUPERVISOR_SCRIPT),
        "--events",
        str(args.events),
        "--profile",
        str(args.profile),
        "--calibration-policy",
        str(args.calibration_policy),
        "--scenario-pack",
        str(args.scenario_pack),
        "--scenario",
        args.scenario,
        "--cycles",
        "1",
        "--max-retries",
        str(args.max_retries),
        "--retry-backoff-seconds",
        str(args.retry_backoff_seconds),
        "--ingestion-max-retries",
        str(args.ingestion_max_retries),
        "--ingestion-retry-backoff-seconds",
        str(args.ingestion_retry_backoff_seconds),
        "--execution-gateway-max-retries",
        str(args.execution_gateway_max_retries),
        "--execution-gateway-retry-backoff-seconds",
        str(args.execution_gateway_retry_backoff_seconds),
        "--state-path",
        str(state_path),
        "--journal-path",
        str(journal_path),
        "--control-state-path",
        str(control_state_path),
        "--control-audit-path",
        str(control_audit_path),
        "--operator-control-actor",
        args.operator_control_actor,
        "--cycle-output-dir",
        str(cycle_output_dir),
    ]


def _append_check(
    checks: list[dict[str, Any]],
    *,
    name: str,
    expected: Any,
    actual: Any,
) -> None:
    checks.append(
        {
            "name": name,
            "expected": expected,
            "actual": actual,
            "passed": actual == expected,
        }
    )


def _evaluate_expected_checks(
    *,
    expected: dict[str, Any],
    command_exit_code: int,
    worker_metadata: dict[str, Any],
    heartbeat_stages: list[str],
    updated_control_state: dict[str, Any],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    expected_exit_code = int(expected.get("command_exit_code", 0))
    _append_check(
        checks,
        name="command_exit_code",
        expected=expected_exit_code,
        actual=command_exit_code,
    )
    if "cycle_status" in expected:
        _append_check(
            checks,
            name="cycle_status",
            expected=expected["cycle_status"],
            actual=worker_metadata.get("cycle_status"),
        )
    if "kill_switch_active" in expected:
        _append_check(
            checks,
            name="kill_switch_active",
            expected=bool(expected["kill_switch_active"]),
            actual=bool(worker_metadata.get("kill_switch_active", False)),
        )
    if "cancel_all_requested" in expected:
        _append_check(
            checks,
            name="cancel_all_requested",
            expected=bool(expected["cancel_all_requested"]),
            actual=bool(worker_metadata.get("cancel_all_requested", False)),
        )
    if "cancel_all_acknowledged" in expected:
        _append_check(
            checks,
            name="cancel_all_acknowledged",
            expected=bool(expected["cancel_all_acknowledged"]),
            actual=bool(worker_metadata.get("cancel_all_acknowledged", False)),
        )
    if "heartbeat_stage" in expected:
        heartbeat_stage = str(expected["heartbeat_stage"]).strip()
        _append_check(
            checks,
            name=f"heartbeat_stage:{heartbeat_stage}",
            expected=True,
            actual=heartbeat_stage in heartbeat_stages,
        )
    if "restart_acknowledged" in expected:
        restart_acknowledged = not bool(
            updated_control_state.get("restart_requested", False)
        )
        _append_check(
            checks,
            name="restart_acknowledged",
            expected=bool(expected["restart_acknowledged"]),
            actual=restart_acknowledged,
        )
    return checks


def _run_drill_scenario(
    *,
    args: argparse.Namespace,
    scenario_config: dict[str, Any],
    control_version: int,
) -> dict[str, Any]:
    scenario_id = str(scenario_config.get("id", "")).strip()
    if not scenario_id:
        raise ValueError("drill_scenarios entries must include non-empty id")
    scenario_dir = args.work_dir / scenario_id
    state_path = scenario_dir / "runtime_state.json"
    journal_path = scenario_dir / "runtime_journal.jsonl"
    control_state_path = scenario_dir / "operator_control_state.json"
    control_audit_path = scenario_dir / "operator_action_audit.jsonl"
    cycle_output_dir = scenario_dir / "cycles"
    cycle_output_dir.mkdir(parents=True, exist_ok=True)

    control_state = _build_control_state(
        scenario_name=args.scenario,
        scenario_id=scenario_id,
        control_version=control_version,
        overrides=dict(scenario_config.get("control_state_overrides", {})),
    )
    _write_json(control_state_path, control_state)

    command = _build_supervisor_command(
        args=args,
        state_path=state_path,
        journal_path=journal_path,
        control_state_path=control_state_path,
        control_audit_path=control_audit_path,
        cycle_output_dir=cycle_output_dir,
    )
    result = subprocess.run(command, capture_output=True, text=True, check=False)

    state_snapshot = _load_json(state_path) if state_path.exists() else {}
    worker_metadata = _extract_worker_loop_metadata(state_snapshot)
    journal_rows = _load_jsonl(journal_path)
    heartbeat_stages = _extract_heartbeat_stages(journal_rows)
    updated_control_state = _load_json(control_state_path)
    expected = dict(scenario_config.get("expected", {}))

    checks = _evaluate_expected_checks(
        expected=expected,
        command_exit_code=result.returncode,
        worker_metadata=worker_metadata,
        heartbeat_stages=heartbeat_stages,
        updated_control_state=updated_control_state,
    )
    failed_checks = [check["name"] for check in checks if not check["passed"]]
    scenario_status = "PASS" if not failed_checks else "FAIL"

    return {
        "id": scenario_id,
        "description": str(scenario_config.get("description", "")),
        "status": scenario_status,
        "checks": checks,
        "failed_checks": failed_checks,
        "command_exit_code": result.returncode,
        "command_stdout_tail": _tail(result.stdout),
        "command_stderr_tail": _tail(result.stderr),
        "worker_last_metadata": worker_metadata,
        "heartbeat_stages": heartbeat_stages,
        "artifact_paths": {
            "state_path": str(state_path),
            "journal_path": str(journal_path),
            "control_state_path": str(control_state_path),
            "control_audit_path": str(control_audit_path),
            "cycle_output_dir": str(cycle_output_dir),
        },
    }


def _scenario_result_by_id(
    scenario_results: list[dict[str, Any]], scenario_id: str
) -> dict[str, Any] | None:
    for scenario_result in scenario_results:
        if scenario_result.get("id") == scenario_id:
            return scenario_result
    return None


def _build_rollback_recommendations(
    *,
    scenario_results: list[dict[str, Any]],
    rollback_matrix: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    recommendations: list[dict[str, Any]] = []
    for row in rollback_matrix:
        trigger = str(row.get("trigger", "")).strip()
        if not trigger:
            continue
        triggered_by: list[str] = []
        if trigger == "live_credential_preflight_failed":
            for scenario_result in scenario_results:
                combined_output = "\n".join(
                    [
                        str(scenario_result.get("command_stdout_tail", "")),
                        str(scenario_result.get("command_stderr_tail", "")),
                    ]
                )
                if "Live credential preflight failed" in combined_output:
                    triggered_by.append(str(scenario_result.get("id", "")))
        elif trigger == "kill_switch_gate_missing":
            result = _scenario_result_by_id(scenario_results, "kill_switch_gate")
            if result and result.get("status") != "PASS":
                triggered_by.append("kill_switch_gate")
        elif trigger == "cancel_all_not_acknowledged":
            result = _scenario_result_by_id(scenario_results, "cancel_all_gate")
            if result and result.get("status") != "PASS":
                triggered_by.append("cancel_all_gate")
        elif trigger == "restart_recovery_not_acknowledged":
            result = _scenario_result_by_id(
                scenario_results, "restart_acknowledgement_gate"
            )
            if result and result.get("status") != "PASS":
                triggered_by.append("restart_acknowledgement_gate")
        if not triggered_by:
            continue
        recommendations.append(
            {
                "trigger": trigger,
                "condition": str(row.get("condition", "")),
                "severity": str(row.get("severity", "unknown")),
                "required_actions": list(row.get("required_actions", [])),
                "triggered_by": triggered_by,
            }
        )
    return recommendations


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    protocol_config = _load_json(args.protocol_config)
    drill_scenarios = protocol_config.get("drill_scenarios")
    if not isinstance(drill_scenarios, list) or not drill_scenarios:
        raise ValueError("Protocol config must define non-empty drill_scenarios list")
    rollback_matrix = protocol_config.get("rollback_decision_matrix")
    if not isinstance(rollback_matrix, list):
        raise ValueError("Protocol config must define rollback_decision_matrix list")

    args.work_dir.mkdir(parents=True, exist_ok=True)
    args.output_path.parent.mkdir(parents=True, exist_ok=True)

    scenario_results: list[dict[str, Any]] = []
    for index, scenario_config in enumerate(drill_scenarios, start=1):
        if not isinstance(scenario_config, dict):
            raise ValueError("Each drill_scenarios item must be an object")
        scenario_result = _run_drill_scenario(
            args=args,
            scenario_config=scenario_config,
            control_version=index,
        )
        scenario_results.append(scenario_result)

    rollback_recommendations = _build_rollback_recommendations(
        scenario_results=scenario_results,
        rollback_matrix=rollback_matrix,
    )
    failed_scenarios = [row for row in scenario_results if row.get("status") != "PASS"]
    overall_status = "SUCCESS" if not failed_scenarios else "FAILED"

    report = {
        "schema_version": ROLLOUT_REHEARSAL_REPORT_SCHEMA_VERSION,
        "generated_at": _utc_now_iso(),
        "protocol_config_path": str(args.protocol_config),
        "protocol_config_version": protocol_config.get("config_version"),
        "scenario_name": args.scenario,
        "precheck_commands": list(protocol_config.get("precheck_commands", [])),
        "postcheck_commands": list(protocol_config.get("postcheck_commands", [])),
        "scenario_results": scenario_results,
        "summary": {
            "overall_status": overall_status,
            "scenario_count": len(scenario_results),
            "passed_scenarios": len(scenario_results) - len(failed_scenarios),
            "failed_scenarios": len(failed_scenarios),
            "rollback_recommendation_count": len(rollback_recommendations),
        },
        "rollback_recommendations": rollback_recommendations,
    }
    _write_json(args.output_path, report)

    print(
        "Rollout rehearsal complete: "
        f"overall_status={overall_status} "
        f"scenario_count={len(scenario_results)} "
        f"failed_scenarios={len(failed_scenarios)} "
        f"rollback_recommendations={len(rollback_recommendations)} "
        f"output_path={args.output_path}"
    )
    return 0 if overall_status == "SUCCESS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
