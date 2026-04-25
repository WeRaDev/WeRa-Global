from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
SCRIPT_PATH = ROOT_DIR / "scripts" / "run_runtime_supervisor.py"
PROFILE_PATH = ROOT_DIR / "config" / "parameters" / "profiles" / "mvp_test_token.v1.json"
CALIBRATION_POLICY_PATH = ROOT_DIR / "config" / "calibration" / "llm_reliability.v1.json"
SCENARIO_PACK_PATH = ROOT_DIR / "config" / "replay" / "scenario_pack.v1.json"
REPLAY_FIXTURE_PATH = ROOT_DIR / "tests" / "fixtures" / "replay_events.jsonl"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from poly_robot.schemas import (  # noqa: E402
    RUNTIME_OPERATOR_CONTROL_STATE_SCHEMA_VERSION,
    RUNTIME_SUPERVISOR_STATE_SCHEMA_VERSION,
)


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


class RuntimeSupervisorControlIntegrationTests(unittest.TestCase):
    def _run_supervisor(
        self,
        *,
        temp_root: Path,
        control_state_payload: dict,
        cycles: int,
        scenario: str = "baseline",
        cycle_output: bool = False,
    ) -> tuple[subprocess.CompletedProcess[str], Path, Path, Path, Path]:
        state_path = temp_root / "runtime_state.json"
        journal_path = temp_root / "runtime_journal.jsonl"
        control_state_path = temp_root / "operator_control_state.json"
        audit_path = temp_root / "operator_action_audit.jsonl"
        _write_json(control_state_path, control_state_payload)

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
            "--scenario",
            scenario,
            "--cycles",
            str(cycles),
            "--max-retries",
            "0",
            "--retry-backoff-seconds",
            "0",
            "--state-path",
            str(state_path),
            "--journal-path",
            str(journal_path),
            "--control-state-path",
            str(control_state_path),
            "--control-audit-path",
            str(audit_path),
        ]
        if cycle_output:
            command.extend(["--cycle-output-dir", str(temp_root / "cycles")])

        result = subprocess.run(command, capture_output=True, text=True, check=False)
        return result, state_path, journal_path, control_state_path, audit_path

    def test_pause_control_skips_cycle_execution(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            control_state = {
                "schema_version": RUNTIME_OPERATOR_CONTROL_STATE_SCHEMA_VERSION,
                "updated_at": "2026-01-01T00:00:00Z",
                "control_version": 5,
                "paused": True,
                "restart_requested": False,
                "selected_scenario": "baseline",
                "last_annotation": "",
            }
            result, state_path, journal_path, _, _ = self._run_supervisor(
                temp_root=root,
                control_state_payload=control_state,
                cycles=2,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
            state = _read_json(state_path)
            self.assertEqual(state["schema_version"], RUNTIME_SUPERVISOR_STATE_SCHEMA_VERSION)
            self.assertEqual(state["cycle_index"], 2)
            metadata = state["worker_results"][0]["last_metadata"]
            self.assertEqual(metadata["cycle_status"], "PAUSED")
            self.assertEqual(metadata["events"], 0)
            stages = {
                (row.get("payload") or {}).get("stage")
                for row in _read_jsonl(journal_path)
                if row.get("event_type") == "worker_heartbeat"
            }
            self.assertIn("control_pause_gate", stages)

    def test_restart_request_is_acknowledged_and_stops_early(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            control_state = {
                "schema_version": RUNTIME_OPERATOR_CONTROL_STATE_SCHEMA_VERSION,
                "updated_at": "2026-01-01T00:00:00Z",
                "control_version": 3,
                "paused": False,
                "restart_requested": True,
                "selected_scenario": "baseline",
                "last_annotation": "",
            }
            result, state_path, _, control_state_path, audit_path = self._run_supervisor(
                temp_root=root,
                control_state_payload=control_state,
                cycles=3,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
            self.assertIn("stopped_by_control_restart=True", result.stdout)
            state = _read_json(state_path)
            self.assertEqual(state["cycle_index"], 1)
            metadata = state["worker_results"][0]["last_metadata"]
            self.assertEqual(metadata["cycle_status"], "RESTART_REQUESTED")

            updated_control_state = _read_json(control_state_path)
            self.assertFalse(updated_control_state["restart_requested"])
            audit_events = _read_jsonl(audit_path)
            self.assertTrue(audit_events)
            self.assertEqual(audit_events[-1]["action"], "graceful_restart_acknowledged")

    def test_selected_scenario_from_control_state_is_used_for_cycle(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            control_state = {
                "schema_version": RUNTIME_OPERATOR_CONTROL_STATE_SCHEMA_VERSION,
                "updated_at": "2026-01-01T00:00:00Z",
                "control_version": 8,
                "paused": False,
                "restart_requested": False,
                "selected_scenario": "liquidity_crunch",
                "last_annotation": "",
            }
            result, state_path, _, _, _ = self._run_supervisor(
                temp_root=root,
                control_state_payload=control_state,
                cycles=1,
                cycle_output=True,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
            state = _read_json(state_path)
            metadata = state["worker_results"][0]["last_metadata"]
            self.assertEqual(metadata["cycle_status"], "EXECUTED")
            self.assertEqual(metadata["selected_scenario"], "liquidity_crunch")

            cycle_report = _read_json(root / "cycles" / "cycle_001.json")
            self.assertEqual(cycle_report["run_context"]["scenario_name"], "liquidity_crunch")


if __name__ == "__main__":
    unittest.main()
