from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT_DIR / "scripts" / "run_runtime_soak.py"
PROFILE_PATH = (
    ROOT_DIR / "config" / "parameters" / "profiles" / "mvp_test_token.v1.json"
)
CALIBRATION_POLICY_PATH = (
    ROOT_DIR / "config" / "calibration" / "llm_reliability.v1.json"
)
SCENARIO_PACK_PATH = ROOT_DIR / "config" / "replay" / "scenario_pack.v1.json"
REPLAY_FIXTURE_PATH = ROOT_DIR / "tests" / "fixtures" / "replay_events.jsonl"


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


class RuntimeSoakIntegrationTests(unittest.TestCase):
    def test_soak_runner_rotates_scenarios_and_records_recovery_drills(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            health_path = root / "soak_health.jsonl"
            summary_path = root / "soak_summary.json"
            state_path = root / "runtime_state.json"
            journal_path = root / "runtime_journal.jsonl"
            control_state_path = root / "operator_control_state.json"
            control_audit_path = root / "operator_action_audit.jsonl"

            command = [
                sys.executable,
                str(SCRIPT_PATH),
                "--events",
                str(REPLAY_FIXTURE_PATH),
                "--profile",
                str(PROFILE_PATH),
                "--calibration-policy",
                str(CALIBRATION_POLICY_PATH),
                "--scenario-pack",
                str(SCENARIO_PACK_PATH),
                "--scenario-rotation",
                "baseline,liquidity_crunch,latency_spike",
                "--intervals",
                "5",
                "--max-retries",
                "0",
                "--retry-backoff-seconds",
                "0",
                "--ingestion-max-retries",
                "0",
                "--ingestion-retry-backoff-seconds",
                "0",
                "--execution-gateway-max-retries",
                "0",
                "--execution-gateway-retry-backoff-seconds",
                "0",
                "--drill-restart-intervals",
                "2",
                "--drill-data-unavailable-intervals",
                "3",
                "--drill-delayed-execution-intervals",
                "4",
                "--drill-delayed-execution-ms",
                "500000",
                "--state-path",
                str(state_path),
                "--journal-path",
                str(journal_path),
                "--control-state-path",
                str(control_state_path),
                "--control-audit-path",
                str(control_audit_path),
                "--health-snapshot-path",
                str(health_path),
                "--summary-path",
                str(summary_path),
                "--cycle-output-dir",
                str(root / "cycles"),
            ]
            result = subprocess.run(
                command, capture_output=True, text=True, check=False
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
            summary = _read_json(summary_path)
            health_rows = _read_jsonl(health_path)

            self.assertEqual(summary["overall_status"], "SUCCESS")
            self.assertEqual(summary["intervals_completed"], 5)
            self.assertEqual(len(health_rows), 5)

            restart_row = health_rows[1]
            self.assertIn("intentional_restart", restart_row["drills"])
            self.assertEqual(restart_row["interval_status"], "SUCCESS")
            self.assertEqual(
                restart_row["worker_last_metadata"].get("cycle_status"),
                "RESTART_REQUESTED",
            )

            data_row = health_rows[2]
            self.assertIn("temporary_data_unavailability", data_row["drills"])
            self.assertEqual(data_row["interval_status"], "DRILL_EXPECTED_FAILURE")
            self.assertNotEqual(data_row["command_exit_code"], 0)

            delayed_row = health_rows[3]
            self.assertIn("delayed_execution_response", delayed_row["drills"])
            self.assertEqual(delayed_row["interval_status"], "SUCCESS")
            self.assertEqual(
                delayed_row["worker_last_metadata"].get("filled_trade_count"),
                0,
            )

            recovery_checks = summary["recovery_checks"]
            self.assertTrue(recovery_checks)
            self.assertTrue(
                all(check["recovered_after_interval"] for check in recovery_checks)
            )

    def test_soak_runner_fails_when_expected_drill_failure_succeeds(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            health_path = root / "soak_health.jsonl"
            summary_path = root / "soak_summary.json"
            state_path = root / "runtime_state.json"
            journal_path = root / "runtime_journal.jsonl"
            control_state_path = root / "operator_control_state.json"
            control_audit_path = root / "operator_action_audit.jsonl"
            drill_dir = root / "soak_drill_inputs"
            drill_dir.mkdir(parents=True, exist_ok=True)
            (drill_dir / "missing_source_interval_001.jsonl").write_text(
                REPLAY_FIXTURE_PATH.read_text(encoding="utf-8"),
                encoding="utf-8",
            )

            command = [
                sys.executable,
                str(SCRIPT_PATH),
                "--events",
                str(REPLAY_FIXTURE_PATH),
                "--profile",
                str(PROFILE_PATH),
                "--calibration-policy",
                str(CALIBRATION_POLICY_PATH),
                "--scenario-pack",
                str(SCENARIO_PACK_PATH),
                "--scenario-rotation",
                "baseline",
                "--intervals",
                "3",
                "--max-retries",
                "0",
                "--retry-backoff-seconds",
                "0",
                "--ingestion-max-retries",
                "0",
                "--ingestion-retry-backoff-seconds",
                "0",
                "--execution-gateway-max-retries",
                "0",
                "--execution-gateway-retry-backoff-seconds",
                "0",
                "--drill-restart-intervals",
                "",
                "--drill-data-unavailable-intervals",
                "1",
                "--drill-delayed-execution-intervals",
                "",
                "--drill-delayed-execution-ms",
                "500000",
                "--state-path",
                str(state_path),
                "--journal-path",
                str(journal_path),
                "--control-state-path",
                str(control_state_path),
                "--control-audit-path",
                str(control_audit_path),
                "--health-snapshot-path",
                str(health_path),
                "--summary-path",
                str(summary_path),
            ]
            result = subprocess.run(
                command, capture_output=True, text=True, check=False
            )

            self.assertNotEqual(
                result.returncode, 0, msg=result.stderr or result.stdout
            )
            summary = _read_json(summary_path)
            health_rows = _read_jsonl(health_path)
            self.assertEqual(summary["overall_status"], "FAILED")
            self.assertEqual(summary["intervals_completed"], 1)
            self.assertEqual(
                summary["interval_status_counts"]["drill_unexpected_success"],
                1,
            )
            self.assertEqual(
                health_rows[0]["interval_status"], "DRILL_UNEXPECTED_SUCCESS"
            )


if __name__ == "__main__":
    unittest.main()
