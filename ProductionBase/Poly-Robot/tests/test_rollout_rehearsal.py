from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT_DIR / "scripts" / "run_rollout_rehearsal.py"
DEFAULT_PROTOCOL_PATH = (
    ROOT_DIR / "config" / "integration" / "live_rollout_rehearsal.v1.json"
)


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class RolloutRehearsalIntegrationTests(unittest.TestCase):
    def test_rehearsal_runner_produces_success_report_for_default_protocol(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            output_path = root / "rollout_rehearsal_report.json"
            work_dir = root / "work"

            command = [
                sys.executable,
                str(SCRIPT_PATH),
                "--protocol-config",
                str(DEFAULT_PROTOCOL_PATH),
                "--work-dir",
                str(work_dir),
                "--output-path",
                str(output_path),
            ]
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
            report = _read_json(output_path)
            self.assertEqual(report["schema_version"], "rollout_rehearsal_report.v1")
            self.assertEqual(report["summary"]["overall_status"], "SUCCESS")
            self.assertEqual(report["summary"]["failed_scenarios"], 0)
            self.assertEqual(report["rollback_recommendations"], [])
            scenario_ids = {row["id"] for row in report["scenario_results"]}
            self.assertEqual(
                scenario_ids,
                {
                    "baseline_control_path",
                    "kill_switch_gate",
                    "cancel_all_gate",
                    "restart_acknowledgement_gate",
                },
            )
            self.assertTrue(
                all(row["status"] == "PASS" for row in report["scenario_results"])
            )

    def test_rehearsal_runner_emits_rollback_recommendation_when_drill_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            protocol_path = root / "protocol.json"
            protocol = _read_json(DEFAULT_PROTOCOL_PATH)
            for scenario in protocol["drill_scenarios"]:
                if scenario["id"] == "kill_switch_gate":
                    scenario["expected"]["heartbeat_stage"] = "nonexistent_stage"
            protocol_path.write_text(
                json.dumps(protocol, indent=2) + "\n",
                encoding="utf-8",
            )

            output_path = root / "rollout_rehearsal_report.json"
            work_dir = root / "work"
            command = [
                sys.executable,
                str(SCRIPT_PATH),
                "--protocol-config",
                str(protocol_path),
                "--work-dir",
                str(work_dir),
                "--output-path",
                str(output_path),
            ]
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            report = _read_json(output_path)
            self.assertEqual(report["summary"]["overall_status"], "FAILED")
            self.assertGreater(report["summary"]["failed_scenarios"], 0)
            triggers = {row["trigger"] for row in report["rollback_recommendations"]}
            self.assertIn("kill_switch_gate_missing", triggers)


if __name__ == "__main__":
    unittest.main()
