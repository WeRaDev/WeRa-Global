from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
SCRIPT_PATH = ROOT_DIR / "scripts" / "run_canary_lifecycle_gate.py"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from poly_robot.schemas import CANARY_LIFECYCLE_GATE_REPORT_SCHEMA_VERSION  # noqa: E402


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _rehearsal_report_stub() -> dict:
    return {
        "schema_version": "rollout_rehearsal_report.v1",
        "summary": {
            "overall_status": "SUCCESS",
            "scenario_count": 4,
            "failed_scenarios": 0,
            "failed_command_bundles": 0,
            "failed_bundle_commands": 0,
            "rollback_recommendation_count": 0,
        },
        "blocking_metadata": {
            "has_blocking_failures": False,
            "blocking_reasons": [],
        },
        "scenario_results": [
            {"id": "baseline_control_path", "status": "PASS"},
            {"id": "kill_switch_gate", "status": "PASS"},
            {"id": "cancel_all_gate", "status": "PASS"},
            {"id": "restart_acknowledgement_gate", "status": "PASS"},
        ],
        "rollback_recommendations": [],
    }


def _cycle_report_stub(*, cycle_index: int) -> dict:
    return {
        "schema_version": "test_token_loop_result.v1",
        "run_context": {
            "cycle_index": cycle_index,
            "ingestion_status": "HEALTHY",
        },
        "execution_cost_to_expected_net_ratio": 0.62,
        "expected_value_after_execution_cost": 0.48,
        "net_pnl": 0.11,
        "open_notional": 0.0,
        "confirmed_exit_count": 1,
        "confirmed_exit_ratio": 1.0,
        "expected_edge_capture_ratio": 0.84,
        "ingestion_status": "HEALTHY",
        "stale_position_ratio": 0.0,
        "records": [{"execution_result": {"status": "FILLED"}}],
    }


def _copy_json(source_path: Path, target_path: Path) -> None:
    payload = _read_json(source_path)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


class CanaryLifecycleGateScriptTests(unittest.TestCase):
    def test_pending_approval_path_denies_enablement_and_opens_incident(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            rehearsal_path = root / "rehearsal.json"
            criteria_path = root / "criteria.json"
            approval_path = root / "approval_record.json"
            rollout_config_path = root / "rollout_config.json"
            policy_path = root / "rollback_policy.json"
            cycle_dir = root / "cycles"
            cycle_dir.mkdir(parents=True, exist_ok=True)
            certification_output = root / "certification.json"
            decision_output = root / "decision.json"
            enablement_audit_output = root / "enablement_audit.jsonl"
            guard_output = root / "guard.json"
            incident_output = root / "incident.json"
            guard_audit_output = root / "guard_audit.jsonl"
            summary_output = root / "summary.json"

            rehearsal_path.write_text(
                json.dumps(_rehearsal_report_stub(), indent=2) + "\n",
                encoding="utf-8",
            )
            _copy_json(
                ROOT_DIR
                / "config"
                / "integration"
                / "canary_promotion_criteria.v1.json",
                criteria_path,
            )
            _copy_json(
                ROOT_DIR
                / "config"
                / "integration"
                / "canary_approval_record_template.v1.json",
                approval_path,
            )
            _copy_json(
                ROOT_DIR / "config" / "integration" / "live_trade_rollout.v1.json",
                rollout_config_path,
            )
            _copy_json(
                ROOT_DIR
                / "config"
                / "integration"
                / "canary_rollback_policy.v1.json",
                policy_path,
            )
            for index in range(1, 4):
                (cycle_dir / f"cycle_{index:03d}.json").write_text(
                    json.dumps(_cycle_report_stub(cycle_index=index), indent=2) + "\n",
                    encoding="utf-8",
                )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--rehearsal-report",
                    str(rehearsal_path),
                    "--criteria-config",
                    str(criteria_path),
                    "--approval-record",
                    str(approval_path),
                    "--rollout-config",
                    str(rollout_config_path),
                    "--policy-config",
                    str(policy_path),
                    "--cycle-report-dir",
                    str(cycle_dir),
                    "--cycle-report-pattern",
                    "cycle_*.json",
                    "--approval-status",
                    "pending",
                    "--approval-actor",
                    "release_manager",
                    "--certification-output",
                    str(certification_output),
                    "--decision-output",
                    str(decision_output),
                    "--enablement-audit-output",
                    str(enablement_audit_output),
                    "--guard-output",
                    str(guard_output),
                    "--incident-output",
                    str(incident_output),
                    "--guard-audit-output",
                    str(guard_audit_output),
                    "--summary-output",
                    str(summary_output),
                    "--reason",
                    "pending-approval-test",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            certification_report = _read_json(certification_output)
            decision_report = _read_json(decision_output)
            guard_report = _read_json(guard_output)
            incident_report = _read_json(incident_output)
            summary_report = _read_json(summary_output)

            self.assertEqual(certification_report["overall_status"], "PASS")
            self.assertEqual(decision_report["decision_status"], "DENY")
            self.assertEqual(guard_report["guard_status"], "FAIL")
            self.assertEqual(incident_report["incident_status"], "OPEN")
            self.assertEqual(
                summary_report["schema_version"],
                CANARY_LIFECYCLE_GATE_REPORT_SCHEMA_VERSION,
            )
            self.assertEqual(summary_report["overall_status"], "FAIL")
            self.assertEqual(
                summary_report["statuses"]["enablement_decision_status"],
                "DENY",
            )
            self.assertIn(
                "enablement_decision_denied",
                summary_report["triggered_condition_ids"],
            )

    def test_auto_approval_path_allows_enablement_and_passes_guard(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            rehearsal_path = root / "rehearsal.json"
            criteria_path = root / "criteria.json"
            approval_path = root / "approval_record.json"
            rollout_config_path = root / "rollout_config.json"
            policy_path = root / "rollback_policy.json"
            cycle_dir = root / "cycles"
            cycle_dir.mkdir(parents=True, exist_ok=True)
            certification_output = root / "certification.json"
            decision_output = root / "decision.json"
            enablement_audit_output = root / "enablement_audit.jsonl"
            guard_output = root / "guard.json"
            incident_output = root / "incident.json"
            guard_audit_output = root / "guard_audit.jsonl"
            summary_output = root / "summary.json"

            rehearsal_path.write_text(
                json.dumps(_rehearsal_report_stub(), indent=2) + "\n",
                encoding="utf-8",
            )
            _copy_json(
                ROOT_DIR
                / "config"
                / "integration"
                / "canary_promotion_criteria.v1.json",
                criteria_path,
            )
            _copy_json(
                ROOT_DIR
                / "config"
                / "integration"
                / "canary_approval_record_template.v1.json",
                approval_path,
            )
            _copy_json(
                ROOT_DIR / "config" / "integration" / "live_trade_rollout.v1.json",
                rollout_config_path,
            )
            _copy_json(
                ROOT_DIR
                / "config"
                / "integration"
                / "canary_rollback_policy.v1.json",
                policy_path,
            )
            for index in range(1, 4):
                (cycle_dir / f"cycle_{index:03d}.json").write_text(
                    json.dumps(_cycle_report_stub(cycle_index=index), indent=2) + "\n",
                    encoding="utf-8",
                )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--rehearsal-report",
                    str(rehearsal_path),
                    "--criteria-config",
                    str(criteria_path),
                    "--approval-record",
                    str(approval_path),
                    "--rollout-config",
                    str(rollout_config_path),
                    "--policy-config",
                    str(policy_path),
                    "--cycle-report-dir",
                    str(cycle_dir),
                    "--cycle-report-pattern",
                    "cycle_*.json",
                    "--approval-status",
                    "approved",
                    "--approval-actor",
                    "release_manager",
                    "--auto-approve-required-approvers",
                    "--certification-output",
                    str(certification_output),
                    "--decision-output",
                    str(decision_output),
                    "--enablement-audit-output",
                    str(enablement_audit_output),
                    "--guard-output",
                    str(guard_output),
                    "--incident-output",
                    str(incident_output),
                    "--guard-audit-output",
                    str(guard_audit_output),
                    "--summary-output",
                    str(summary_output),
                    "--reason",
                    "auto-approval-test",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(
                result.returncode,
                0,
                msg=result.stderr or result.stdout,
            )
            certification_report = _read_json(certification_output)
            decision_report = _read_json(decision_output)
            guard_report = _read_json(guard_output)
            incident_report = _read_json(incident_output)
            summary_report = _read_json(summary_output)

            self.assertEqual(certification_report["overall_status"], "PASS")
            self.assertEqual(decision_report["decision_status"], "ALLOW")
            self.assertEqual(guard_report["guard_status"], "PASS")
            self.assertEqual(incident_report["incident_status"], "NONE")
            self.assertEqual(summary_report["overall_status"], "PASS")
            self.assertEqual(
                summary_report["statuses"]["enablement_decision_status"],
                "ALLOW",
            )
            self.assertEqual(summary_report["triggered_condition_ids"], [])
            self.assertTrue(summary_report["promotion_allowed"])

    def test_lifecycle_runner_uses_numeric_cycle_order_for_max_cycle_reports(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            rehearsal_path = root / "rehearsal.json"
            criteria_path = root / "criteria.json"
            approval_path = root / "approval_record.json"
            rollout_config_path = root / "rollout_config.json"
            policy_path = root / "rollback_policy.json"
            cycle_dir = root / "cycles"
            cycle_dir.mkdir(parents=True, exist_ok=True)
            certification_output = root / "certification.json"
            decision_output = root / "decision.json"
            enablement_audit_output = root / "enablement_audit.jsonl"
            guard_output = root / "guard.json"
            incident_output = root / "incident.json"
            guard_audit_output = root / "guard_audit.jsonl"
            summary_output = root / "summary.json"

            rehearsal_path.write_text(
                json.dumps(_rehearsal_report_stub(), indent=2) + "\n",
                encoding="utf-8",
            )
            _copy_json(
                ROOT_DIR
                / "config"
                / "integration"
                / "canary_promotion_criteria.v1.json",
                criteria_path,
            )
            _copy_json(
                ROOT_DIR
                / "config"
                / "integration"
                / "canary_approval_record_template.v1.json",
                approval_path,
            )
            _copy_json(
                ROOT_DIR / "config" / "integration" / "live_trade_rollout.v1.json",
                rollout_config_path,
            )
            _copy_json(
                ROOT_DIR
                / "config"
                / "integration"
                / "canary_rollback_policy.v1.json",
                policy_path,
            )
            for cycle_index in (2, 10, 11):
                (cycle_dir / f"cycle_{cycle_index}.json").write_text(
                    json.dumps(_cycle_report_stub(cycle_index=cycle_index), indent=2)
                    + "\n",
                    encoding="utf-8",
                )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--rehearsal-report",
                    str(rehearsal_path),
                    "--criteria-config",
                    str(criteria_path),
                    "--approval-record",
                    str(approval_path),
                    "--rollout-config",
                    str(rollout_config_path),
                    "--policy-config",
                    str(policy_path),
                    "--cycle-report-dir",
                    str(cycle_dir),
                    "--cycle-report-pattern",
                    "cycle_*.json",
                    "--max-cycle-reports",
                    "2",
                    "--approval-status",
                    "approved",
                    "--approval-actor",
                    "release_manager",
                    "--auto-approve-required-approvers",
                    "--certification-output",
                    str(certification_output),
                    "--decision-output",
                    str(decision_output),
                    "--enablement-audit-output",
                    str(enablement_audit_output),
                    "--guard-output",
                    str(guard_output),
                    "--incident-output",
                    str(incident_output),
                    "--guard-audit-output",
                    str(guard_audit_output),
                    "--summary-output",
                    str(summary_output),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
            summary_report = _read_json(summary_output)
            loaded_cycle_files = [
                Path(path).name for path in summary_report.get("cycle_report_paths", [])
            ]
            self.assertEqual(loaded_cycle_files, ["cycle_10.json", "cycle_11.json"])


if __name__ == "__main__":
    unittest.main()
