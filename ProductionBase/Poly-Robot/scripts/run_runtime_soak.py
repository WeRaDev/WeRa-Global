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

from poly_robot.runtime_web_gui import OperatorControlManager  # noqa: E402
from poly_robot.scenario_pack import load_scenario_pack  # noqa: E402
from poly_robot.schemas import RUNTIME_SOAK_HEALTH_SNAPSHOT_SCHEMA_VERSION  # noqa: E402


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="milliseconds")


def _parse_interval_set(raw: str) -> set[int]:
    values = {chunk.strip() for chunk in raw.split(",") if chunk.strip()}
    if not values:
        return set()
    parsed: set[int] = set()
    for value in values:
        interval = int(value)
        if interval <= 0:
            raise ValueError("drill intervals must be positive integers")
        parsed.add(interval)
    return parsed


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def _append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True))
        handle.write("\n")


def _tail(text: str, *, max_chars: int = 3000) -> str:
    cleaned = text.strip()
    if len(cleaned) <= max_chars:
        return cleaned
    return cleaned[-max_chars:]


def _state_mtime(path: Path) -> float | None:
    if not path.exists():
        return None
    return path.stat().st_mtime


def _load_state_if_updated(
    path: Path, *, before_mtime: float | None
) -> dict[str, Any] | None:
    if not path.exists():
        return None
    current_mtime = path.stat().st_mtime
    if before_mtime is not None and current_mtime == before_mtime:
        return None
    return _load_json(path)


def _build_delayed_events_fixture(
    *,
    source_path: Path,
    target_path: Path,
    execution_latency_ms: int,
) -> Path:
    rows = _load_jsonl(source_path)
    transformed_rows: list[str] = []
    for row in rows:
        metadata = dict(row.get("metadata", {}))
        metadata["execution_latency_ms"] = execution_latency_ms
        row["metadata"] = metadata
        transformed_rows.append(json.dumps(row, sort_keys=True))
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text("\n".join(transformed_rows) + "\n", encoding="utf-8")
    return target_path


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run deterministic soak orchestration for Poly-Robot runtime supervision with "
            "scenario rotation, health snapshots, and recovery drills."
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
        "--scenario-rotation",
        type=str,
        default="",
        help=(
            "Comma-separated scenario names used for interval rotation. "
            "Defaults to scenario-pack order."
        ),
    )
    parser.add_argument(
        "--intervals",
        type=int,
        default=12,
        help="Number of soak intervals (each interval runs one supervised cycle).",
    )
    parser.add_argument(
        "--bankroll",
        type=float,
        default=1000.0,
        help="Initial bankroll used in replay simulation.",
    )
    parser.add_argument(
        "--state-path",
        type=Path,
        default=ROOT_DIR / "runtime" / "runtime_state.json",
        help="Path to runtime supervisor state snapshot JSON.",
    )
    parser.add_argument(
        "--journal-path",
        type=Path,
        default=ROOT_DIR / "runtime" / "runtime_journal.jsonl",
        help="Path to runtime supervisor JSONL journal.",
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
        "--health-snapshot-path",
        type=Path,
        default=ROOT_DIR / "runtime" / "soak_health_snapshots.jsonl",
        help="Path to append interval health snapshots as JSONL.",
    )
    parser.add_argument(
        "--summary-path",
        type=Path,
        default=ROOT_DIR / "runtime" / "soak_summary.json",
        help="Path to persist soak summary JSON.",
    )
    parser.add_argument(
        "--cycle-output-dir",
        type=Path,
        required=False,
        help="Optional directory to persist per-interval supervisor cycle reports.",
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
        "--operator-control-actor",
        type=str,
        default="runtime_soak_orchestrator",
        help="Actor identity used when soak runner creates drill control actions.",
    )
    parser.add_argument(
        "--ignore-operator-controls",
        action="store_true",
        help="Ignore operator control state and run using CLI scenario only.",
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
        "--drill-restart-intervals",
        type=str,
        default="2",
        help="Comma-separated interval indexes for intentional restart drill injection.",
    )
    parser.add_argument(
        "--drill-data-unavailable-intervals",
        type=str,
        default="3",
        help="Comma-separated interval indexes for temporary data unavailability drill.",
    )
    parser.add_argument(
        "--drill-delayed-execution-intervals",
        type=str,
        default="4",
        help="Comma-separated interval indexes for delayed execution response drill.",
    )
    parser.add_argument(
        "--drill-delayed-execution-ms",
        type=int,
        default=500000,
        help="Synthetic execution latency (ms) used during delayed execution drill intervals.",
    )
    parser.add_argument(
        "--continue-on-unexpected-failure",
        action="store_true",
        help="Continue running intervals after unexpected failures.",
    )
    return parser


def _build_supervisor_command(
    *,
    args: argparse.Namespace,
    events_path: Path,
    scenario_name: str,
    interval_output_dir: Path | None,
) -> list[str]:
    command = [
        sys.executable,
        str(RUNTIME_SUPERVISOR_SCRIPT),
        "--events",
        str(events_path),
        "--profile",
        str(args.profile),
        "--calibration-policy",
        str(args.calibration_policy),
        "--scenario-pack",
        str(args.scenario_pack),
        "--scenario",
        scenario_name,
        "--bankroll",
        str(args.bankroll),
        "--cycles",
        "1",
        "--max-retries",
        str(args.max_retries),
        "--retry-backoff-seconds",
        str(args.retry_backoff_seconds),
        "--heartbeat-timeout-seconds",
        str(args.heartbeat_timeout_seconds),
        "--state-path",
        str(args.state_path),
        "--journal-path",
        str(args.journal_path),
        "--control-state-path",
        str(args.control_state_path),
        "--control-audit-path",
        str(args.control_audit_path),
        "--operator-control-actor",
        args.operator_control_actor,
        "--ingestion-max-retries",
        str(args.ingestion_max_retries),
        "--ingestion-retry-backoff-seconds",
        str(args.ingestion_retry_backoff_seconds),
        "--ingestion-timeout-seconds",
        str(args.ingestion_timeout_seconds),
        "--ingestion-max-invalid-rows",
        str(args.ingestion_max_invalid_rows),
        "--execution-gateway-max-retries",
        str(args.execution_gateway_max_retries),
        "--execution-gateway-retry-backoff-seconds",
        str(args.execution_gateway_retry_backoff_seconds),
        "--execution-gateway-timeout-seconds",
        str(args.execution_gateway_timeout_seconds),
    ]
    if args.ignore_operator_controls:
        command.append("--ignore-operator-controls")
    if interval_output_dir is not None:
        command.extend(["--cycle-output-dir", str(interval_output_dir)])
    return command


def _extract_worker_loop_metadata(
    state_snapshot: dict[str, Any] | None,
) -> dict[str, Any]:
    if not state_snapshot:
        return {}
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


def _build_rotation(arg_rotation: str, available_scenarios: list[str]) -> list[str]:
    if arg_rotation.strip():
        parsed = [chunk.strip() for chunk in arg_rotation.split(",") if chunk.strip()]
        if not parsed:
            raise ValueError("--scenario-rotation is empty after parsing")
        return parsed
    return available_scenarios


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    if args.intervals <= 0:
        raise ValueError("--intervals must be > 0")
    if args.drill_delayed_execution_ms <= 0:
        raise ValueError("--drill-delayed-execution-ms must be > 0")

    restart_drill_intervals = _parse_interval_set(args.drill_restart_intervals)
    data_unavailable_drill_intervals = _parse_interval_set(
        args.drill_data_unavailable_intervals
    )
    delayed_execution_drill_intervals = _parse_interval_set(
        args.drill_delayed_execution_intervals
    )
    if args.ignore_operator_controls and restart_drill_intervals:
        raise ValueError(
            "Restart drills require operator controls; remove --ignore-operator-controls."
        )

    scenario_pack = load_scenario_pack(args.scenario_pack)
    available_scenarios = list(scenario_pack.scenarios.keys())
    scenario_rotation = _build_rotation(args.scenario_rotation, available_scenarios)
    for scenario_name in scenario_rotation:
        scenario_pack.get_scenario(scenario_name)

    args.health_snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    args.health_snapshot_path.write_text("", encoding="utf-8")
    args.summary_path.parent.mkdir(parents=True, exist_ok=True)
    args.state_path.parent.mkdir(parents=True, exist_ok=True)
    args.journal_path.parent.mkdir(parents=True, exist_ok=True)
    args.control_state_path.parent.mkdir(parents=True, exist_ok=True)
    args.control_audit_path.parent.mkdir(parents=True, exist_ok=True)

    drill_data_dir = args.health_snapshot_path.parent / "soak_drill_inputs"
    drill_data_dir.mkdir(parents=True, exist_ok=True)

    if args.cycle_output_dir:
        args.cycle_output_dir.mkdir(parents=True, exist_ok=True)

    control_manager = OperatorControlManager(
        control_state_path=args.control_state_path,
        audit_path=args.control_audit_path,
    )

    snapshots: list[dict[str, Any]] = []
    for interval_index in range(1, args.intervals + 1):
        scenario_name = scenario_rotation[(interval_index - 1) % len(scenario_rotation)]
        drill_labels: list[str] = []
        expected_failure = False
        events_path = args.events

        if interval_index in delayed_execution_drill_intervals:
            drill_labels.append("delayed_execution_response")
            events_path = _build_delayed_events_fixture(
                source_path=args.events,
                target_path=drill_data_dir
                / f"delayed_execution_interval_{interval_index:03d}.jsonl",
                execution_latency_ms=args.drill_delayed_execution_ms,
            )

        if interval_index in data_unavailable_drill_intervals:
            drill_labels.append("temporary_data_unavailability")
            expected_failure = True
            events_path = (
                drill_data_dir / f"missing_source_interval_{interval_index:03d}.jsonl"
            )

        if interval_index in restart_drill_intervals:
            drill_labels.append("intentional_restart")
            control_manager.request_restart(
                actor=args.operator_control_actor,
                reason=f"soak_drill_interval_{interval_index}",
            )

        interval_output_dir = (
            (args.cycle_output_dir / f"interval_{interval_index:03d}")
            if args.cycle_output_dir
            else None
        )
        if interval_output_dir is not None:
            interval_output_dir.mkdir(parents=True, exist_ok=True)

        command = _build_supervisor_command(
            args=args,
            events_path=events_path,
            scenario_name=scenario_name,
            interval_output_dir=interval_output_dir,
        )
        state_mtime_before = _state_mtime(args.state_path)
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        state_snapshot = _load_state_if_updated(
            args.state_path, before_mtime=state_mtime_before
        )
        worker_metadata = _extract_worker_loop_metadata(state_snapshot)
        supervisor_state_status = (
            state_snapshot.get("status") if isinstance(state_snapshot, dict) else None
        )
        supervisor_failed = supervisor_state_status == "FAILED"
        command_failed = result.returncode != 0

        if expected_failure:
            if command_failed or supervisor_failed:
                interval_status = "DRILL_EXPECTED_FAILURE"
            else:
                interval_status = "DRILL_UNEXPECTED_SUCCESS"
        else:
            interval_status = (
                "FAILED" if command_failed or supervisor_failed else "SUCCESS"
            )

        snapshot = {
            "schema_version": RUNTIME_SOAK_HEALTH_SNAPSHOT_SCHEMA_VERSION,
            "timestamp": _utc_now_iso(),
            "interval_index": interval_index,
            "scenario_name": scenario_name,
            "drills": drill_labels,
            "expected_failure": expected_failure,
            "interval_status": interval_status,
            "command_exit_code": result.returncode,
            "command_stdout_tail": _tail(result.stdout),
            "command_stderr_tail": _tail(result.stderr),
            "supervisor_state_status": supervisor_state_status,
            "worker_last_metadata": worker_metadata,
            "events_path": str(events_path),
        }
        snapshots.append(snapshot)
        _append_jsonl(args.health_snapshot_path, snapshot)
        if (
            interval_status in ("FAILED", "DRILL_UNEXPECTED_SUCCESS")
            and not args.continue_on_unexpected_failure
        ):
            break

    def _has_success_after(interval_index: int) -> bool:
        for snapshot in snapshots:
            if snapshot["interval_index"] <= interval_index:
                continue
            if snapshot["interval_status"] == "SUCCESS":
                return True
        return False

    recovery_checks: list[dict[str, Any]] = []
    for snapshot in snapshots:
        interval_index = int(snapshot["interval_index"])
        drills = snapshot.get("drills", [])
        for drill in drills:
            if drill not in (
                "intentional_restart",
                "temporary_data_unavailability",
                "delayed_execution_response",
            ):
                continue
            recovery_checks.append(
                {
                    "interval_index": interval_index,
                    "drill": drill,
                    "recovered_after_interval": _has_success_after(interval_index),
                }
            )

    has_unexpected_failure = any(
        snapshot["interval_status"] == "FAILED" for snapshot in snapshots
    )
    has_drill_unexpected_success = any(
        snapshot["interval_status"] == "DRILL_UNEXPECTED_SUCCESS"
        for snapshot in snapshots
    )
    has_failed_recovery_check = any(
        not check["recovered_after_interval"] for check in recovery_checks
    )
    overall_status = (
        "FAILED"
        if has_unexpected_failure
        or has_drill_unexpected_success
        or has_failed_recovery_check
        else "SUCCESS"
    )

    summary = {
        "schema_version": "runtime_soak_summary.v1",
        "generated_at": _utc_now_iso(),
        "intervals_requested": args.intervals,
        "intervals_completed": len(snapshots),
        "overall_status": overall_status,
        "scenario_rotation": scenario_rotation,
        "drill_configuration": {
            "restart_intervals": sorted(restart_drill_intervals),
            "data_unavailable_intervals": sorted(data_unavailable_drill_intervals),
            "delayed_execution_intervals": sorted(delayed_execution_drill_intervals),
            "delayed_execution_ms": args.drill_delayed_execution_ms,
        },
        "health_snapshot_path": str(args.health_snapshot_path),
        "recovery_checks": recovery_checks,
        "interval_status_counts": {
            "success": sum(1 for s in snapshots if s["interval_status"] == "SUCCESS"),
            "drill_expected_failure": sum(
                1 for s in snapshots if s["interval_status"] == "DRILL_EXPECTED_FAILURE"
            ),
            "drill_unexpected_success": sum(
                1
                for s in snapshots
                if s["interval_status"] == "DRILL_UNEXPECTED_SUCCESS"
            ),
            "failed": sum(1 for s in snapshots if s["interval_status"] == "FAILED"),
        },
    }
    args.summary_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    print(
        "Runtime soak complete: "
        f"intervals_requested={summary['intervals_requested']} "
        f"intervals_completed={summary['intervals_completed']} "
        f"overall_status={summary['overall_status']} "
        f"health_snapshot_path={args.health_snapshot_path} "
        f"summary_path={args.summary_path}"
    )
    return 0 if overall_status == "SUCCESS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
