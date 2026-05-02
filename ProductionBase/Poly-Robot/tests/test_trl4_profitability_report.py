from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT_DIR / "scripts" / "run_trl4_profitability_report.py"
GATE_CONFIG_PATH = (
    ROOT_DIR / "config" / "certification" / "trl4_24h_profitability_gate.v1.json"
)


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    serialized_rows = [json.dumps(row, sort_keys=True) for row in rows]
    path.write_text("\n".join(serialized_rows) + "\n", encoding="utf-8")


def _journal_row(
    *,
    timestamp: str,
    cycle_index: int,
    expected_value_after_execution_cost: float | None,
    expected_net_edge_value_on_fills: float | None,
    net_pnl: float | None,
) -> dict:
    return {
        "schema_version": "runtime_supervisor_event.v1",
        "timestamp": timestamp,
        "event_type": "worker_heartbeat",
        "payload": {
            "worker_name": "test_token_loop",
            "stage": "cycle_completed",
            "cycle_index": cycle_index,
            "attempt_number": 1,
            "details": {
                "cycle_index": cycle_index,
                "expected_value_after_execution_cost": (
                    expected_value_after_execution_cost
                ),
                "expected_net_edge_value_on_fills": (
                    expected_net_edge_value_on_fills
                ),
                "net_pnl": net_pnl,
            },
        },
    }


class Trl4ProfitabilityReportScriptTests(unittest.TestCase):
    def test_report_passes_with_24h_runtime_and_positive_expected_profitability(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            journal_path = root / "runtime_journal.jsonl"
            output_path = root / "trl4_report.json"
            state_path = root / "runtime_state.json"
            state_path.write_text(
                json.dumps({"cycle_index": 2, "status": "SUCCESS"}) + "\n",
                encoding="utf-8",
            )

            _write_jsonl(
                journal_path,
                [
                    _journal_row(
                        timestamp="2026-01-01T00:00:00.000Z",
                        cycle_index=1,
                        expected_value_after_execution_cost=5.0,
                        expected_net_edge_value_on_fills=5.2,
                        net_pnl=-0.3,
                    ),
                    _journal_row(
                        timestamp="2026-01-02T00:00:00.000Z",
                        cycle_index=2,
                        expected_value_after_execution_cost=4.8,
                        expected_net_edge_value_on_fills=5.1,
                        net_pnl=-0.4,
                    ),
                ],
            )

            command = [
                sys.executable,
                str(SCRIPT_PATH),
                "--journal-path",
                str(journal_path),
                "--state-path",
                str(state_path),
                "--gate-config",
                str(GATE_CONFIG_PATH),
                "--output",
                str(output_path),
            ]
            result = subprocess.run(
                command, capture_output=True, text=True, check=False
            )
            self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
            report = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(report["overall_status"], "PASS")
            self.assertEqual(report["runtime"]["cycle_count"], 2)
            self.assertEqual(report["runtime"]["runtime_duration_hours"], 24.0)
            self.assertEqual(report["runtime"]["runtime_duration_hours_wall_clock"], 24.0)
            self.assertEqual(report["runtime"]["runtime_duration_hours_cycle_based"], 2.0)
            self.assertEqual(report["runtime"]["runtime_hours_per_cycle"], 1.0)

    def test_report_uses_cycle_based_runtime_when_wall_clock_is_short(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            journal_path = root / "runtime_journal.jsonl"
            output_path = root / "trl4_report.json"
            state_path = root / "runtime_state.json"
            state_path.write_text(
                json.dumps({"cycle_index": 2, "status": "SUCCESS"}) + "\n",
                encoding="utf-8",
            )

            _write_jsonl(
                journal_path,
                [
                    _journal_row(
                        timestamp="2026-01-01T00:00:00.000Z",
                        cycle_index=1,
                        expected_value_after_execution_cost=1.0,
                        expected_net_edge_value_on_fills=1.0,
                        net_pnl=-0.1,
                    ),
                    _journal_row(
                        timestamp="2026-01-01T00:00:01.000Z",
                        cycle_index=2,
                        expected_value_after_execution_cost=1.0,
                        expected_net_edge_value_on_fills=1.0,
                        net_pnl=-0.2,
                    ),
                ],
            )

            command = [
                sys.executable,
                str(SCRIPT_PATH),
                "--journal-path",
                str(journal_path),
                "--state-path",
                str(state_path),
                "--gate-config",
                str(GATE_CONFIG_PATH),
                "--runtime-hours-per-cycle",
                "12",
                "--output",
                str(output_path),
            ]
            result = subprocess.run(
                command, capture_output=True, text=True, check=False
            )
            self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
            report = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(report["overall_status"], "PASS")
            self.assertEqual(report["runtime"]["runtime_hours_per_cycle"], 12.0)
            self.assertEqual(report["runtime"]["runtime_duration_hours_cycle_based"], 24.0)
            self.assertEqual(report["runtime"]["runtime_duration_hours"], 24.0)

    def test_report_fails_when_latest_expected_profitability_is_negative(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            journal_path = root / "runtime_journal.jsonl"
            output_path = root / "trl4_report.json"

            _write_jsonl(
                journal_path,
                [
                    _journal_row(
                        timestamp="2026-01-01T00:00:00.000Z",
                        cycle_index=1,
                        expected_value_after_execution_cost=3.0,
                        expected_net_edge_value_on_fills=3.2,
                        net_pnl=0.1,
                    ),
                    _journal_row(
                        timestamp="2026-01-02T00:00:00.000Z",
                        cycle_index=2,
                        expected_value_after_execution_cost=-0.5,
                        expected_net_edge_value_on_fills=2.8,
                        net_pnl=0.2,
                    ),
                ],
            )

            command = [
                sys.executable,
                str(SCRIPT_PATH),
                "--journal-path",
                str(journal_path),
                "--gate-config",
                str(GATE_CONFIG_PATH),
                "--output",
                str(output_path),
            ]
            result = subprocess.run(
                command, capture_output=True, text=True, check=False
            )
            self.assertNotEqual(
                result.returncode, 0, msg=result.stderr or result.stdout
            )
            report = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(report["overall_status"], "FAIL")
            incident_codes = {
                incident["code"] for incident in report.get("incidents", [])
            }
            self.assertIn(
                "criterion_failed:expected_value_after_execution_cost",
                incident_codes,
            )


if __name__ == "__main__":
    unittest.main()
