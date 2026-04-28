from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
SCRIPT_PATH = ROOT_DIR / "scripts" / "run_canary_rollback_guard.py"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from poly_robot.canary_rollback_guard import build_canary_rollback_guard_report  # noqa: E402
from poly_robot.schemas import (  # noqa: E402
    CANARY_ROLLBACK_GUARD_AUDIT_EVENT_SCHEMA_VERSION,
    CANARY_ROLLBACK_GUARD_REPORT_SCHEMA_VERSION,
    CANARY_ROLLBACK_INCIDENT_REPORT_SCHEMA_VERSION,
)


def _enablement_decision_stub(*, decision_status: str = "ALLOW") -> dict:
    return {
        "schema_version": "canary_stage_enablement_decision.v1",
        "decision_status": decision_status,
        "failed_reason_codes": [] if decision_status == "ALLOW" else ["sample_deny_reason"],
        "evidence": {"decision_hash": "enablement_hash_123"},
    }


def _certification_report_stub(
    *,
    overall_status: str = "PASS",
    blockers: list[dict] | None = None,
) -> dict:
    return {
        "schema_version": "canary_rollout_certification_report.v1",
        "overall_status": overall_status,
        "blockers": blockers or [],
        "evidence": {"certification_hash": "certification_hash_123"},
    }


def _rehearsal_report_stub(*, rollback_recommendations: list[dict] | None = None) -> dict:
    return {
        "schema_version": "rollout_rehearsal_report.v1",
        "rollback_recommendations": rollback_recommendations or [],
    }


def _cycle_report_stub(
    *,
    cycle_index: int,
    execution_cost_to_expected_net_ratio: float | None,
    expected_value_after_execution_cost: float | None,
    execution_statuses: list[str] | None = None,
    net_pnl: float | None = 0.0,
    open_notional: float | None = 0.0,
    confirmed_exit_count: int = 1,
    confirmed_exit_ratio: float | None = 1.0,
    expected_edge_capture_ratio: float | None = 1.0,
    ingestion_status: str = "HEALTHY",
    stale_position_ratio: float | None = 0.0,
) -> dict:
    statuses = execution_statuses or ["FILLED"]
    return {
        "schema_version": "test_token_loop_result.v1",
        "run_context": {
            "cycle_index": cycle_index,
            "ingestion_status": ingestion_status,
        },
        "execution_cost_to_expected_net_ratio": execution_cost_to_expected_net_ratio,
        "expected_value_after_execution_cost": expected_value_after_execution_cost,
        "net_pnl": net_pnl,
        "open_notional": open_notional,
        "confirmed_exit_count": confirmed_exit_count,
        "confirmed_exit_ratio": confirmed_exit_ratio,
        "expected_edge_capture_ratio": expected_edge_capture_ratio,
        "ingestion_status": ingestion_status,
        "stale_position_ratio": stale_position_ratio,
        "records": [
            {"execution_result": {"status": status}}
            for status in statuses
        ],
    }


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


class CanaryRollbackGuardTests(unittest.TestCase):
    def test_guard_passes_when_no_triggers_fire(self) -> None:
        guard_report = build_canary_rollback_guard_report(
            canary_enablement_decision=_enablement_decision_stub(decision_status="ALLOW"),
            certification_report=_certification_report_stub(overall_status="PASS"),
            rehearsal_report=_rehearsal_report_stub(),
            cycle_reports=[
                _cycle_report_stub(
                    cycle_index=1,
                    execution_cost_to_expected_net_ratio=0.65,
                    expected_value_after_execution_cost=3.2,
                ),
                _cycle_report_stub(
                    cycle_index=2,
                    execution_cost_to_expected_net_ratio=0.72,
                    expected_value_after_execution_cost=2.4,
                ),
            ],
        )

        self.assertEqual(
            guard_report["schema_version"],
            CANARY_ROLLBACK_GUARD_REPORT_SCHEMA_VERSION,
        )
        self.assertEqual(guard_report["guard_status"], "PASS")
        self.assertEqual(guard_report["triggered_condition_count"], 0)
        incident = guard_report["incident_handoff"]
        self.assertEqual(
            incident["schema_version"],
            CANARY_ROLLBACK_INCIDENT_REPORT_SCHEMA_VERSION,
        )
        self.assertEqual(incident["incident_status"], "NONE")
        self.assertEqual(incident["required_emergency_actions"], [])

    def test_guard_fails_when_enablement_decision_is_denied(self) -> None:
        guard_report = build_canary_rollback_guard_report(
            canary_enablement_decision=_enablement_decision_stub(decision_status="DENY"),
            certification_report=_certification_report_stub(overall_status="PASS"),
            rehearsal_report=_rehearsal_report_stub(),
            cycle_reports=[
                _cycle_report_stub(
                    cycle_index=1,
                    execution_cost_to_expected_net_ratio=0.5,
                    expected_value_after_execution_cost=1.2,
                )
            ],
        )

        self.assertEqual(guard_report["guard_status"], "FAIL")
        trigger_ids = {row["id"] for row in guard_report["triggered_conditions"]}
        self.assertIn("enablement_decision_denied", trigger_ids)
        incident = guard_report["incident_handoff"]
        self.assertEqual(incident["incident_status"], "OPEN")
        self.assertIn("stop_canary_rollout_progression", incident["required_emergency_actions"])
        self.assertEqual(incident["responsible_authority"], "runtime_operator_on_call")

    def test_guard_fails_on_consecutive_execution_cost_ratio_breach(self) -> None:
        guard_report = build_canary_rollback_guard_report(
            canary_enablement_decision=_enablement_decision_stub(decision_status="ALLOW"),
            certification_report=_certification_report_stub(overall_status="PASS"),
            rehearsal_report=_rehearsal_report_stub(),
            cycle_reports=[
                _cycle_report_stub(
                    cycle_index=1,
                    execution_cost_to_expected_net_ratio=1.12,
                    expected_value_after_execution_cost=0.8,
                ),
                _cycle_report_stub(
                    cycle_index=2,
                    execution_cost_to_expected_net_ratio=1.17,
                    expected_value_after_execution_cost=0.6,
                ),
                _cycle_report_stub(
                    cycle_index=3,
                    execution_cost_to_expected_net_ratio=1.23,
                    expected_value_after_execution_cost=0.4,
                ),
            ],
        )

        self.assertEqual(guard_report["guard_status"], "FAIL")
        trigger_ids = {row["id"] for row in guard_report["triggered_conditions"]}
        self.assertIn("execution_cost_ratio_breach_consecutive", trigger_ids)
        telemetry_summary = guard_report["telemetry_summary"]
        self.assertEqual(
            telemetry_summary["max_execution_cost_ratio_consecutive_breaches"], 3
        )

    def test_guard_fails_on_consecutive_negative_realized_pnl(self) -> None:
        guard_report = build_canary_rollback_guard_report(
            canary_enablement_decision=_enablement_decision_stub(decision_status="ALLOW"),
            certification_report=_certification_report_stub(overall_status="PASS"),
            rehearsal_report=_rehearsal_report_stub(),
            cycle_reports=[
                _cycle_report_stub(
                    cycle_index=1,
                    execution_cost_to_expected_net_ratio=0.4,
                    expected_value_after_execution_cost=0.5,
                    net_pnl=-0.11,
                    open_notional=0.0,
                    confirmed_exit_count=1,
                ),
                _cycle_report_stub(
                    cycle_index=2,
                    execution_cost_to_expected_net_ratio=0.5,
                    expected_value_after_execution_cost=0.3,
                    net_pnl=-0.09,
                    open_notional=0.0,
                    confirmed_exit_count=1,
                ),
                _cycle_report_stub(
                    cycle_index=3,
                    execution_cost_to_expected_net_ratio=0.45,
                    expected_value_after_execution_cost=0.4,
                    net_pnl=-0.07,
                    open_notional=0.0,
                    confirmed_exit_count=1,
                ),
            ],
        )

        self.assertEqual(guard_report["guard_status"], "FAIL")
        trigger_ids = {row["id"] for row in guard_report["triggered_conditions"]}
        self.assertIn("negative_realized_pnl_consecutive", trigger_ids)
        telemetry_summary = guard_report["telemetry_summary"]
        self.assertEqual(
            telemetry_summary["max_negative_realized_pnl_consecutive_breaches"], 3
        )

    def test_guard_fails_on_persistent_open_notional_without_confirmed_exits(self) -> None:
        guard_report = build_canary_rollback_guard_report(
            canary_enablement_decision=_enablement_decision_stub(decision_status="ALLOW"),
            certification_report=_certification_report_stub(overall_status="PASS"),
            rehearsal_report=_rehearsal_report_stub(),
            cycle_reports=[
                _cycle_report_stub(
                    cycle_index=1,
                    execution_cost_to_expected_net_ratio=0.4,
                    expected_value_after_execution_cost=0.5,
                    net_pnl=0.02,
                    open_notional=55.0,
                    confirmed_exit_count=0,
                ),
                _cycle_report_stub(
                    cycle_index=2,
                    execution_cost_to_expected_net_ratio=0.45,
                    expected_value_after_execution_cost=0.4,
                    net_pnl=0.01,
                    open_notional=53.0,
                    confirmed_exit_count=0,
                ),
                _cycle_report_stub(
                    cycle_index=3,
                    execution_cost_to_expected_net_ratio=0.5,
                    expected_value_after_execution_cost=0.3,
                    net_pnl=0.0,
                    open_notional=51.0,
                    confirmed_exit_count=0,
                ),
            ],
        )

        self.assertEqual(guard_report["guard_status"], "FAIL")
        trigger_ids = {row["id"] for row in guard_report["triggered_conditions"]}
        self.assertIn("open_notional_without_confirmed_exits_consecutive", trigger_ids)
        telemetry_summary = guard_report["telemetry_summary"]
        self.assertEqual(
            telemetry_summary[
                "max_open_notional_without_confirmed_exits_consecutive_breaches"
            ],
            3,
        )

    def test_guard_fails_on_rolling_realized_pnl_floor_breach(self) -> None:
        guard_report = build_canary_rollback_guard_report(
            canary_enablement_decision=_enablement_decision_stub(decision_status="ALLOW"),
            certification_report=_certification_report_stub(overall_status="PASS"),
            rehearsal_report=_rehearsal_report_stub(),
            policy={
                "thresholds": {
                    "minimum_rolling_realized_pnl": 0.0,
                    "rolling_realized_pnl_window_cycles": 3,
                }
            },
            cycle_reports=[
                _cycle_report_stub(
                    cycle_index=1,
                    execution_cost_to_expected_net_ratio=0.4,
                    expected_value_after_execution_cost=0.5,
                    net_pnl=-0.12,
                ),
                _cycle_report_stub(
                    cycle_index=2,
                    execution_cost_to_expected_net_ratio=0.45,
                    expected_value_after_execution_cost=0.4,
                    net_pnl=-0.08,
                ),
                _cycle_report_stub(
                    cycle_index=3,
                    execution_cost_to_expected_net_ratio=0.5,
                    expected_value_after_execution_cost=0.3,
                    net_pnl=-0.06,
                ),
            ],
        )

        self.assertEqual(guard_report["guard_status"], "FAIL")
        trigger_ids = {row["id"] for row in guard_report["triggered_conditions"]}
        self.assertIn("rolling_realized_pnl_floor_breach", trigger_ids)
        telemetry_summary = guard_report["telemetry_summary"]
        self.assertEqual(telemetry_summary["rolling_realized_pnl_window_cycle_count"], 3)
        self.assertEqual(telemetry_summary["rolling_realized_pnl"], -0.26)

    def test_guard_fails_on_consecutive_confirmed_exit_ratio_breach(self) -> None:
        guard_report = build_canary_rollback_guard_report(
            canary_enablement_decision=_enablement_decision_stub(decision_status="ALLOW"),
            certification_report=_certification_report_stub(overall_status="PASS"),
            rehearsal_report=_rehearsal_report_stub(),
            cycle_reports=[
                _cycle_report_stub(
                    cycle_index=1,
                    execution_cost_to_expected_net_ratio=0.4,
                    expected_value_after_execution_cost=0.5,
                    confirmed_exit_ratio=0.4,
                    stale_position_ratio=0.1,
                ),
                _cycle_report_stub(
                    cycle_index=2,
                    execution_cost_to_expected_net_ratio=0.45,
                    expected_value_after_execution_cost=0.4,
                    confirmed_exit_ratio=0.45,
                    stale_position_ratio=0.1,
                ),
                _cycle_report_stub(
                    cycle_index=3,
                    execution_cost_to_expected_net_ratio=0.5,
                    expected_value_after_execution_cost=0.3,
                    confirmed_exit_ratio=0.48,
                    stale_position_ratio=0.1,
                ),
            ],
        )

        self.assertEqual(guard_report["guard_status"], "FAIL")
        trigger_ids = {row["id"] for row in guard_report["triggered_conditions"]}
        self.assertIn("confirmed_exit_ratio_breach_consecutive", trigger_ids)
        telemetry_summary = guard_report["telemetry_summary"]
        self.assertEqual(
            telemetry_summary[
                "max_confirmed_exit_ratio_breach_consecutive_breaches"
            ],
            3,
        )

    def test_guard_fails_on_consecutive_edge_realization_ratio_breach(self) -> None:
        guard_report = build_canary_rollback_guard_report(
            canary_enablement_decision=_enablement_decision_stub(decision_status="ALLOW"),
            certification_report=_certification_report_stub(overall_status="PASS"),
            rehearsal_report=_rehearsal_report_stub(),
            policy={
                "thresholds": {
                    "minimum_edge_realization_ratio": 0.6,
                    "edge_realization_ratio_breach_consecutive_cycles": 3,
                }
            },
            cycle_reports=[
                _cycle_report_stub(
                    cycle_index=1,
                    execution_cost_to_expected_net_ratio=0.4,
                    expected_value_after_execution_cost=0.5,
                    expected_edge_capture_ratio=0.45,
                ),
                _cycle_report_stub(
                    cycle_index=2,
                    execution_cost_to_expected_net_ratio=0.45,
                    expected_value_after_execution_cost=0.4,
                    expected_edge_capture_ratio=0.5,
                ),
                _cycle_report_stub(
                    cycle_index=3,
                    execution_cost_to_expected_net_ratio=0.5,
                    expected_value_after_execution_cost=0.3,
                    expected_edge_capture_ratio=0.55,
                ),
            ],
        )

        self.assertEqual(guard_report["guard_status"], "FAIL")
        trigger_ids = {row["id"] for row in guard_report["triggered_conditions"]}
        self.assertIn("edge_realization_ratio_breach_consecutive", trigger_ids)
        telemetry_summary = guard_report["telemetry_summary"]
        self.assertEqual(
            telemetry_summary["max_edge_realization_ratio_breach_consecutive_breaches"],
            3,
        )

    def test_guard_fails_on_ingestion_degraded_ratio_window_breach(self) -> None:
        guard_report = build_canary_rollback_guard_report(
            canary_enablement_decision=_enablement_decision_stub(decision_status="ALLOW"),
            certification_report=_certification_report_stub(overall_status="PASS"),
            rehearsal_report=_rehearsal_report_stub(),
            policy={
                "thresholds": {
                    "max_ingestion_degraded_cycle_ratio": 0.5,
                    "ingestion_degraded_ratio_window_cycles": 4,
                }
            },
            cycle_reports=[
                _cycle_report_stub(
                    cycle_index=1,
                    execution_cost_to_expected_net_ratio=0.4,
                    expected_value_after_execution_cost=0.5,
                    ingestion_status="DEGRADED",
                ),
                _cycle_report_stub(
                    cycle_index=2,
                    execution_cost_to_expected_net_ratio=0.45,
                    expected_value_after_execution_cost=0.4,
                    ingestion_status="DEGRADED",
                ),
                _cycle_report_stub(
                    cycle_index=3,
                    execution_cost_to_expected_net_ratio=0.5,
                    expected_value_after_execution_cost=0.3,
                    ingestion_status="HEALTHY",
                ),
                _cycle_report_stub(
                    cycle_index=4,
                    execution_cost_to_expected_net_ratio=0.48,
                    expected_value_after_execution_cost=0.25,
                    ingestion_status="DEGRADED",
                ),
            ],
        )

        self.assertEqual(guard_report["guard_status"], "FAIL")
        trigger_ids = {row["id"] for row in guard_report["triggered_conditions"]}
        self.assertIn("ingestion_degraded_ratio_breach_window", trigger_ids)
        telemetry_summary = guard_report["telemetry_summary"]
        self.assertEqual(
            telemetry_summary["ingestion_degraded_ratio_window_cycle_count"],
            4,
        )
        self.assertEqual(telemetry_summary["ingestion_degraded_cycle_count"], 3)
        self.assertEqual(telemetry_summary["ingestion_degraded_cycle_ratio"], 0.75)

    def test_guard_fails_on_consecutive_stale_position_ratio_breach(self) -> None:
        guard_report = build_canary_rollback_guard_report(
            canary_enablement_decision=_enablement_decision_stub(decision_status="ALLOW"),
            certification_report=_certification_report_stub(overall_status="PASS"),
            rehearsal_report=_rehearsal_report_stub(),
            cycle_reports=[
                _cycle_report_stub(
                    cycle_index=1,
                    execution_cost_to_expected_net_ratio=0.4,
                    expected_value_after_execution_cost=0.5,
                    confirmed_exit_ratio=0.7,
                    stale_position_ratio=0.4,
                ),
                _cycle_report_stub(
                    cycle_index=2,
                    execution_cost_to_expected_net_ratio=0.45,
                    expected_value_after_execution_cost=0.4,
                    confirmed_exit_ratio=0.8,
                    stale_position_ratio=0.42,
                ),
                _cycle_report_stub(
                    cycle_index=3,
                    execution_cost_to_expected_net_ratio=0.5,
                    expected_value_after_execution_cost=0.3,
                    confirmed_exit_ratio=0.75,
                    stale_position_ratio=0.39,
                ),
            ],
        )

        self.assertEqual(guard_report["guard_status"], "FAIL")
        trigger_ids = {row["id"] for row in guard_report["triggered_conditions"]}
        self.assertIn("stale_position_ratio_breach_consecutive", trigger_ids)
        telemetry_summary = guard_report["telemetry_summary"]
        self.assertEqual(
            telemetry_summary[
                "max_stale_position_ratio_breach_consecutive_breaches"
            ],
            3,
        )

    def test_runner_writes_guard_incident_and_audit_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            enablement_path = root / "enablement.json"
            certification_path = root / "certification.json"
            rehearsal_path = root / "rehearsal.json"
            policy_path = root / "policy.json"
            cycle_dir = root / "cycles"
            cycle_dir.mkdir(parents=True, exist_ok=True)
            guard_output = root / "guard_report.json"
            incident_output = root / "incident_report.json"
            audit_output = root / "guard_audit.jsonl"

            enablement_path.write_text(
                json.dumps(_enablement_decision_stub(decision_status="ALLOW"), indent=2) + "\n",
                encoding="utf-8",
            )
            certification_path.write_text(
                json.dumps(_certification_report_stub(overall_status="PASS"), indent=2) + "\n",
                encoding="utf-8",
            )
            rehearsal_path.write_text(
                json.dumps(_rehearsal_report_stub(), indent=2) + "\n",
                encoding="utf-8",
            )
            policy_path.write_text(
                json.dumps(
                    {
                        "thresholds": {
                            "max_execution_cost_to_expected_net_ratio": 1.0,
                            "execution_cost_ratio_consecutive_cycles": 2,
                            "minimum_expected_value_after_execution_cost": 0.0,
                            "negative_expected_value_consecutive_cycles": 3,
                        }
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            (cycle_dir / "cycle_001.json").write_text(
                json.dumps(
                    _cycle_report_stub(
                        cycle_index=1,
                        execution_cost_to_expected_net_ratio=1.11,
                        expected_value_after_execution_cost=0.7,
                    ),
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            (cycle_dir / "cycle_002.json").write_text(
                json.dumps(
                    _cycle_report_stub(
                        cycle_index=2,
                        execution_cost_to_expected_net_ratio=1.16,
                        expected_value_after_execution_cost=0.5,
                    ),
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--enablement-decision",
                    str(enablement_path),
                    "--certification-report",
                    str(certification_path),
                    "--rehearsal-report",
                    str(rehearsal_path),
                    "--cycle-report-dir",
                    str(cycle_dir),
                    "--policy-config",
                    str(policy_path),
                    "--guard-output",
                    str(guard_output),
                    "--incident-output",
                    str(incident_output),
                    "--audit-output",
                    str(audit_output),
                    "--actor",
                    "runtime_operator_on_call",
                    "--reason",
                    "f3-regression-test",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            guard_report = _read_json(guard_output)
            incident_report = _read_json(incident_output)
            audit_rows = _read_jsonl(audit_output)

            self.assertEqual(guard_report["guard_status"], "FAIL")
            self.assertEqual(incident_report["incident_status"], "OPEN")
            self.assertEqual(len(audit_rows), 1)
            self.assertEqual(
                audit_rows[0]["schema_version"],
                CANARY_ROLLBACK_GUARD_AUDIT_EVENT_SCHEMA_VERSION,
            )
            self.assertEqual(audit_rows[0]["guard_status"], "FAIL")
            self.assertEqual(audit_rows[0]["incident_status"], "OPEN")


if __name__ == "__main__":
    unittest.main()
