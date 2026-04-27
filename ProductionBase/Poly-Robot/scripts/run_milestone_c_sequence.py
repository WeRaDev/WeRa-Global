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
RUNTIME_SOAK_SCRIPT = ROOT_DIR / "scripts" / "run_runtime_soak.py"
STRESS_CERTIFICATION_SCRIPT = ROOT_DIR / "scripts" / "run_stress_certification.py"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from poly_robot.reproducibility import stable_hash  # noqa: E402


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="milliseconds")


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _tail(text: str, *, max_chars: int = 3000) -> str:
    cleaned = text.strip()
    if len(cleaned) <= max_chars:
        return cleaned
    return cleaned[-max_chars:]


def _resolve_repo_path(raw_path: str) -> Path:
    parsed = Path(raw_path)
    if parsed.is_absolute():
        return parsed
    return ROOT_DIR / parsed


def _load_phase_sequence(
    path: Path,
) -> tuple[int, list[dict[str, Any]]]:
    payload = _load_json(path)
    intervals_per_hour = int(payload.get("intervals_per_hour", 1))
    if intervals_per_hour <= 0:
        raise ValueError("intervals_per_hour must be > 0")

    raw_phases = payload.get("phases")
    if not isinstance(raw_phases, list) or not raw_phases:
        raise ValueError("phase sequence must define a non-empty phases list")

    normalized_phases: list[dict[str, Any]] = []
    for index, raw_phase in enumerate(raw_phases):
        if not isinstance(raw_phase, dict):
            raise ValueError(f"phase entry at index {index} must be an object")
        phase_name = str(raw_phase.get("phase_name", "")).strip()
        if not phase_name:
            raise ValueError(f"phase_name missing at index {index}")
        duration_hours = int(raw_phase.get("duration_hours", 0))
        if duration_hours <= 0:
            raise ValueError(f"duration_hours for phase {phase_name} must be > 0")
        thresholds_path_raw = raw_phase.get("thresholds_path")
        thresholds_path = (
            _resolve_repo_path(str(thresholds_path_raw))
            if thresholds_path_raw is not None and str(thresholds_path_raw).strip()
            else None
        )
        scenarios = (
            str(raw_phase.get("scenarios")).strip()
            if raw_phase.get("scenarios") is not None
            else None
        )
        normalized_phases.append(
            {
                "phase_name": phase_name,
                "duration_hours": duration_hours,
                "thresholds_path": thresholds_path,
                "scenarios": scenarios or None,
            }
        )

    return intervals_per_hour, normalized_phases


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run staged Milestone C campaigns by executing runtime soak and stress "
            "certification in sequence (for example 12h -> 24h -> 48h)."
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
        "--phase-config",
        type=Path,
        default=ROOT_DIR / "config" / "certification" / "milestone_c_sequence.v1.json",
        help="Path to Milestone C phased soak/certification sequence config JSON.",
    )
    parser.add_argument(
        "--intervals-per-hour",
        type=int,
        required=False,
        help=(
            "Optional override for intervals per hour used to convert phase "
            "durations into soak intervals."
        ),
    )
    parser.add_argument(
        "--scenario-rotation",
        type=str,
        default="",
        help=(
            "Optional comma-separated scenario rotation passed to soak runner. "
            "Defaults to scenario-pack order."
        ),
    )
    parser.add_argument(
        "--scenarios",
        type=str,
        required=False,
        help=(
            "Optional comma-separated scenarios passed to stress certification. "
            "Defaults to all scenarios."
        ),
    )
    parser.add_argument(
        "--certification-thresholds",
        type=Path,
        required=False,
        help=(
            "Optional global thresholds JSON used for all phases unless "
            "phase-specific thresholds are configured."
        ),
    )
    parser.add_argument(
        "--bankroll",
        type=float,
        default=1000.0,
        help="Initial bankroll used in replay simulation.",
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
        help="Synthetic execution latency (ms) used during delayed execution drills.",
    )
    parser.add_argument(
        "--continue-on-unexpected-failure",
        action="store_true",
        help="Continue soak intervals after unexpected failures within a phase.",
    )
    parser.add_argument(
        "--continue-on-phase-failure",
        action="store_true",
        help="Continue running subsequent phases after a failed phase.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=ROOT_DIR / "runtime" / "milestone_c_sequence",
        help="Directory where per-phase and sequence summary artifacts are written.",
    )
    return parser


def _build_soak_command(
    *,
    args: argparse.Namespace,
    intervals: int,
    phase_dir: Path,
) -> list[str]:
    command = [
        sys.executable,
        str(RUNTIME_SOAK_SCRIPT),
        "--events",
        str(args.events),
        "--profile",
        str(args.profile),
        "--calibration-policy",
        str(args.calibration_policy),
        "--scenario-pack",
        str(args.scenario_pack),
        "--intervals",
        str(intervals),
        "--bankroll",
        str(args.bankroll),
        "--max-retries",
        str(args.max_retries),
        "--retry-backoff-seconds",
        str(args.retry_backoff_seconds),
        "--heartbeat-timeout-seconds",
        str(args.heartbeat_timeout_seconds),
        "--drill-restart-intervals",
        args.drill_restart_intervals,
        "--drill-data-unavailable-intervals",
        args.drill_data_unavailable_intervals,
        "--drill-delayed-execution-intervals",
        args.drill_delayed_execution_intervals,
        "--drill-delayed-execution-ms",
        str(args.drill_delayed_execution_ms),
        "--state-path",
        str(phase_dir / "runtime_state.json"),
        "--journal-path",
        str(phase_dir / "runtime_journal.jsonl"),
        "--control-state-path",
        str(phase_dir / "operator_control_state.json"),
        "--control-audit-path",
        str(phase_dir / "operator_action_audit.jsonl"),
        "--health-snapshot-path",
        str(phase_dir / "soak_health_snapshots.jsonl"),
        "--summary-path",
        str(phase_dir / "soak_summary.json"),
        "--cycle-output-dir",
        str(phase_dir / "cycles"),
    ]
    if args.scenario_rotation.strip():
        command.extend(["--scenario-rotation", args.scenario_rotation])
    if args.continue_on_unexpected_failure:
        command.append("--continue-on-unexpected-failure")
    return command


def _build_certification_command(
    *,
    args: argparse.Namespace,
    phase_dir: Path,
    thresholds_path: Path | None,
    phase_scenarios: str | None,
) -> list[str]:
    command = [
        sys.executable,
        str(STRESS_CERTIFICATION_SCRIPT),
        "--events",
        str(args.events),
        "--profile",
        str(args.profile),
        "--calibration-policy",
        str(args.calibration_policy),
        "--scenario-pack",
        str(args.scenario_pack),
        "--bankroll",
        str(args.bankroll),
        "--soak-summary",
        str(phase_dir / "soak_summary.json"),
        "--matrix-output",
        str(phase_dir / "stress_matrix_report.json"),
        "--output",
        str(phase_dir / "stress_campaign_certification.json"),
    ]
    selected_scenarios = phase_scenarios or args.scenarios
    if selected_scenarios and selected_scenarios.strip():
        command.extend(["--scenarios", selected_scenarios.strip()])
    if thresholds_path is not None:
        command.extend(["--thresholds", str(thresholds_path)])
    return command


def _safe_load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return _load_json(path)


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    config_intervals_per_hour, phases = _load_phase_sequence(args.phase_config)
    intervals_per_hour = args.intervals_per_hour or config_intervals_per_hour
    if intervals_per_hour <= 0:
        raise ValueError("--intervals-per-hour must be > 0")

    global_thresholds_path = (
        _resolve_repo_path(str(args.certification_thresholds))
        if args.certification_thresholds is not None
        else None
    )
    args.output_root.mkdir(parents=True, exist_ok=True)

    phase_reports: list[dict[str, Any]] = []
    for phase in phases:
        phase_name = str(phase["phase_name"])
        duration_hours = int(phase["duration_hours"])
        phase_intervals = duration_hours * intervals_per_hour
        phase_dir = args.output_root / phase_name
        phase_dir.mkdir(parents=True, exist_ok=True)

        soak_command = _build_soak_command(
            args=args,
            intervals=phase_intervals,
            phase_dir=phase_dir,
        )
        soak_result = subprocess.run(
            soak_command,
            capture_output=True,
            text=True,
            check=False,
        )
        soak_summary_path = phase_dir / "soak_summary.json"
        soak_summary = _safe_load_json(soak_summary_path) or {}
        soak_overall_status = str(soak_summary.get("overall_status", "UNKNOWN"))

        phase_thresholds_path = phase.get("thresholds_path") or global_thresholds_path
        certification_command = _build_certification_command(
            args=args,
            phase_dir=phase_dir,
            thresholds_path=phase_thresholds_path,
            phase_scenarios=phase.get("scenarios"),
        )
        certification_result = subprocess.run(
            certification_command,
            capture_output=True,
            text=True,
            check=False,
        )

        certification_report_path = phase_dir / "stress_campaign_certification.json"
        certification_report = _safe_load_json(certification_report_path) or {}
        certification_payload = certification_report.get("certification")
        if isinstance(certification_payload, dict):
            certification_status = str(
                certification_payload.get("overall_status", "UNKNOWN")
            )
        else:
            certification_status = "UNKNOWN"

        phase_status = (
            "PASS"
            if soak_result.returncode == 0
            and certification_result.returncode == 0
            and soak_overall_status == "SUCCESS"
            and certification_status == "PASS"
            else "FAIL"
        )
        phase_report = {
            "phase_name": phase_name,
            "duration_hours": duration_hours,
            "intervals": phase_intervals,
            "status": phase_status,
            "soak_return_code": soak_result.returncode,
            "soak_overall_status": soak_overall_status,
            "soak_summary_path": str(soak_summary_path),
            "soak_stdout_tail": _tail(soak_result.stdout),
            "soak_stderr_tail": _tail(soak_result.stderr),
            "certification_return_code": certification_result.returncode,
            "certification_status": certification_status,
            "certification_report_path": str(certification_report_path),
            "certification_stdout_tail": _tail(certification_result.stdout),
            "certification_stderr_tail": _tail(certification_result.stderr),
            "matrix_report_path": str(phase_dir / "stress_matrix_report.json"),
            "thresholds_path": (
                str(phase_thresholds_path) if phase_thresholds_path else None
            ),
        }
        phase_reports.append(phase_report)

        if phase_status == "FAIL" and not args.continue_on_phase_failure:
            break

    all_planned_phases_passed = (
        len(phase_reports) == len(phases)
        and all(report["status"] == "PASS" for report in phase_reports)
    )
    overall_status = "PASS" if all_planned_phases_passed else "FAIL"

    summary = {
        "schema_version": "milestone_c_sequence_report.v1",
        "generated_at": _utc_now_iso(),
        "phase_config_path": str(args.phase_config),
        "intervals_per_hour": intervals_per_hour,
        "planned_phase_count": len(phases),
        "completed_phase_count": len(phase_reports),
        "overall_status": overall_status,
        "phase_reports": phase_reports,
        "output_root": str(args.output_root),
    }
    summary["summary_hash"] = stable_hash(
        {
            "phase_config_path": summary["phase_config_path"],
            "intervals_per_hour": summary["intervals_per_hour"],
            "planned_phase_count": summary["planned_phase_count"],
            "completed_phase_count": summary["completed_phase_count"],
            "overall_status": summary["overall_status"],
            "phase_reports": summary["phase_reports"],
        }
    )

    summary_path = args.output_root / "milestone_c_sequence_summary.json"
    summary_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(
        "Milestone C sequence complete: "
        f"planned_phases={summary['planned_phase_count']} "
        f"completed_phases={summary['completed_phase_count']} "
        f"overall_status={summary['overall_status']} "
        f"summary_path={summary_path}"
    )
    return 0 if overall_status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
