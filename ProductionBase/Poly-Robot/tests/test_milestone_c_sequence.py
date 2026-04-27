from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT_DIR = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT_DIR / "scripts" / "run_milestone_c_sequence.py"
PROFILE_PATH = (
    ROOT_DIR / "config" / "parameters" / "profiles" / "mvp_test_token.v1.json"
)
CALIBRATION_POLICY_PATH = ROOT_DIR / "config" / "calibration" / "llm_reliability.v1.json"
SCENARIO_PACK_PATH = ROOT_DIR / "config" / "replay" / "scenario_pack.v1.json"
REPLAY_FIXTURE_PATH = ROOT_DIR / "tests" / "fixtures" / "replay_events.jsonl"


def _load_sequence_script_module():
    module_spec = importlib.util.spec_from_file_location(
        "run_milestone_c_sequence", SCRIPT_PATH
    )
    if module_spec is None or module_spec.loader is None:
        raise AssertionError("Unable to load run_milestone_c_sequence.py module")
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


def _arg_value(command: list[str], flag: str) -> str:
    index = command.index(flag)
    return command[index + 1]


class MilestoneCSequenceScriptTests(unittest.TestCase):
    def test_sequence_runner_executes_all_phases_and_writes_summary(self) -> None:
        module = _load_sequence_script_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            output_root = root / "outputs"
            phase_config_path = root / "phase_config.json"
            phase_config_path.write_text(
                json.dumps(
                    {
                        "schema_version": "milestone_c_sequence.v1",
                        "intervals_per_hour": 1,
                        "phases": [
                            {"phase_name": "phase_12h", "duration_hours": 12},
                            {"phase_name": "phase_24h", "duration_hours": 24},
                        ],
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            def fake_run(
                command: list[str], *, capture_output: bool, text: bool, check: bool
            ):
                self.assertTrue(capture_output)
                self.assertTrue(text)
                self.assertFalse(check)
                invoked_script = Path(command[1]).name

                if invoked_script == "run_runtime_soak.py":
                    summary_path = Path(_arg_value(command, "--summary-path"))
                    summary_path.parent.mkdir(parents=True, exist_ok=True)
                    summary_path.write_text(
                        json.dumps(
                            {
                                "overall_status": "SUCCESS",
                                "intervals_completed": int(
                                    _arg_value(command, "--intervals")
                                ),
                            }
                        )
                        + "\n",
                        encoding="utf-8",
                    )
                    health_path = Path(_arg_value(command, "--health-snapshot-path"))
                    health_path.parent.mkdir(parents=True, exist_ok=True)
                    health_path.write_text("", encoding="utf-8")
                    return subprocess.CompletedProcess(
                        command,
                        0,
                        stdout="soak_ok",
                        stderr="",
                    )

                if invoked_script == "run_stress_certification.py":
                    matrix_path = Path(_arg_value(command, "--matrix-output"))
                    matrix_path.parent.mkdir(parents=True, exist_ok=True)
                    matrix_path.write_text(
                        json.dumps({"aggregate": {"scenario_count": 4}}) + "\n",
                        encoding="utf-8",
                    )
                    output_path = Path(_arg_value(command, "--output"))
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    output_path.write_text(
                        json.dumps({"certification": {"overall_status": "PASS"}})
                        + "\n",
                        encoding="utf-8",
                    )
                    return subprocess.CompletedProcess(
                        command,
                        0,
                        stdout="cert_ok",
                        stderr="",
                    )

                raise AssertionError(f"Unexpected script invocation: {invoked_script}")

            argv = [
                "--events",
                str(REPLAY_FIXTURE_PATH),
                "--profile",
                str(PROFILE_PATH),
                "--calibration-policy",
                str(CALIBRATION_POLICY_PATH),
                "--scenario-pack",
                str(SCENARIO_PACK_PATH),
                "--phase-config",
                str(phase_config_path),
                "--output-root",
                str(output_root),
            ]
            with patch.object(module.subprocess, "run", side_effect=fake_run):
                exit_code = module.main(argv)

            self.assertEqual(exit_code, 0)
            summary = json.loads(
                (output_root / "milestone_c_sequence_summary.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(summary["overall_status"], "PASS")
            self.assertEqual(summary["planned_phase_count"], 2)
            self.assertEqual(summary["completed_phase_count"], 2)
            self.assertEqual(
                [phase["intervals"] for phase in summary["phase_reports"]],
                [12, 24],
            )
            self.assertTrue(
                all(phase["status"] == "PASS" for phase in summary["phase_reports"])
            )

    def test_sequence_runner_stops_on_first_failed_phase_by_default(self) -> None:
        module = _load_sequence_script_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            output_root = root / "outputs"
            phase_config_path = root / "phase_config.json"
            phase_config_path.write_text(
                json.dumps(
                    {
                        "schema_version": "milestone_c_sequence.v1",
                        "intervals_per_hour": 1,
                        "phases": [
                            {"phase_name": "phase_12h", "duration_hours": 12},
                            {"phase_name": "phase_24h", "duration_hours": 24},
                        ],
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            phase_invocations: list[str] = []
            certification_invocations = 0

            def fake_run(
                command: list[str], *, capture_output: bool, text: bool, check: bool
            ):
                nonlocal certification_invocations
                self.assertTrue(capture_output)
                self.assertTrue(text)
                self.assertFalse(check)
                invoked_script = Path(command[1]).name

                if invoked_script == "run_runtime_soak.py":
                    phase_name = Path(_arg_value(command, "--summary-path")).parent.name
                    phase_invocations.append(phase_name)
                    summary_path = Path(_arg_value(command, "--summary-path"))
                    summary_path.parent.mkdir(parents=True, exist_ok=True)
                    summary_path.write_text(
                        json.dumps({"overall_status": "SUCCESS"}) + "\n",
                        encoding="utf-8",
                    )
                    return subprocess.CompletedProcess(
                        command,
                        0,
                        stdout="soak_ok",
                        stderr="",
                    )

                if invoked_script == "run_stress_certification.py":
                    phase_name = Path(_arg_value(command, "--output")).parent.name
                    phase_invocations.append(phase_name)
                    certification_invocations += 1
                    matrix_path = Path(_arg_value(command, "--matrix-output"))
                    matrix_path.parent.mkdir(parents=True, exist_ok=True)
                    matrix_path.write_text(
                        json.dumps({"aggregate": {"scenario_count": 4}}) + "\n",
                        encoding="utf-8",
                    )
                    output_path = Path(_arg_value(command, "--output"))
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    output_path.write_text(
                        json.dumps({"certification": {"overall_status": "FAIL"}})
                        + "\n",
                        encoding="utf-8",
                    )
                    return subprocess.CompletedProcess(
                        command,
                        1,
                        stdout="cert_failed",
                        stderr="",
                    )

                raise AssertionError(f"Unexpected script invocation: {invoked_script}")

            argv = [
                "--events",
                str(REPLAY_FIXTURE_PATH),
                "--profile",
                str(PROFILE_PATH),
                "--calibration-policy",
                str(CALIBRATION_POLICY_PATH),
                "--scenario-pack",
                str(SCENARIO_PACK_PATH),
                "--phase-config",
                str(phase_config_path),
                "--output-root",
                str(output_root),
            ]
            with patch.object(module.subprocess, "run", side_effect=fake_run):
                exit_code = module.main(argv)

            self.assertEqual(exit_code, 1)
            self.assertEqual(certification_invocations, 1)
            summary = json.loads(
                (output_root / "milestone_c_sequence_summary.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(summary["overall_status"], "FAIL")
            self.assertEqual(summary["planned_phase_count"], 2)
            self.assertEqual(summary["completed_phase_count"], 1)
            self.assertEqual(len(summary["phase_reports"]), 1)
            self.assertEqual(summary["phase_reports"][0]["phase_name"], "phase_12h")
            self.assertEqual(summary["phase_reports"][0]["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
