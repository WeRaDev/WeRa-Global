from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
SCRIPT_PATH = ROOT_DIR / "scripts" / "run_canary_stage_enablement.py"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from poly_robot.canary_enablement import build_canary_stage_enablement_decision  # noqa: E402
from poly_robot.schemas import (  # noqa: E402
    CANARY_STAGE_ENABLEMENT_AUDIT_EVENT_SCHEMA_VERSION,
    CANARY_STAGE_ENABLEMENT_DECISION_SCHEMA_VERSION,
)


def _certification_report_stub(
    *,
    overall_status: str = "PASS",
    blockers: list[dict] | None = None,
) -> dict:
    return {
        "schema_version": "canary_rollout_certification_report.v1",
        "overall_status": overall_status,
        "readiness_score": 98.4,
        "blockers": blockers or [],
        "promotion_decision": {
            "manual_approval_required": True,
            "promotion_owner": "release_manager",
            "required_approvers": ["release_manager", "runtime_operator_on_call"],
            "rollback_authority": ["runtime_operator_on_call", "incident_commander"],
        },
        "evidence": {"certification_hash": "cert_hash_123"},
    }


def _approval_record_stub(
    *,
    approvals: list[dict],
) -> dict:
    return {
        "schema_version": "canary_approval_record.v1",
        "record_id": "approval-record-001",
        "requested_by": "release_manager",
        "requested_stage": "canary_live",
        "required_approvers": ["release_manager", "runtime_operator_on_call"],
        "approvals": approvals,
    }


def _rollout_config_stub() -> dict:
    return {
        "rollout_stages": [
            {
                "stage": "paper",
                "enabled": True,
                "real_order_submission": False,
            },
            {
                "stage": "canary_live",
                "enabled": False,
                "real_order_submission": True,
                "max_order_notional_usd": 50,
                "max_daily_notional_usd": 500,
                "max_open_orders": 3,
            },
        ],
        "emergency_actions": [
            "disable_new_orders",
            "cancel_all_open_orders",
            "switch_to_paper_mode",
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


class CanaryEnablementTests(unittest.TestCase):
    def test_missing_required_approver_denies_stage_enablement(self) -> None:
        decision = build_canary_stage_enablement_decision(
            certification_report=_certification_report_stub(),
            approval_record=_approval_record_stub(
                approvals=[{"actor": "release_manager", "decision": "approved"}]
            ),
            rollout_config=_rollout_config_stub(),
            requested_stage="canary_live",
        )

        self.assertEqual(
            decision["schema_version"],
            CANARY_STAGE_ENABLEMENT_DECISION_SCHEMA_VERSION,
        )
        self.assertEqual(decision["decision_status"], "DENY")
        self.assertFalse(decision["canary_stage_enablement_allowed"])
        self.assertIn("required_approver_missing", decision["failed_reason_codes"])
        self.assertIn("required_approver_not_approved", decision["failed_reason_codes"])
        self.assertEqual(
            decision["approval_state"]["missing_required_approvers"],
            ["runtime_operator_on_call"],
        )

    def test_certification_blockers_deny_stage_enablement(self) -> None:
        decision = build_canary_stage_enablement_decision(
            certification_report=_certification_report_stub(
                overall_status="FAIL",
                blockers=[
                    {
                        "code": "unresolved_rollback_trigger:kill_switch_gate_missing",
                        "severity": "critical",
                    }
                ],
            ),
            approval_record=_approval_record_stub(
                approvals=[
                    {"actor": "release_manager", "decision": "approved"},
                    {"actor": "runtime_operator_on_call", "decision": "approved"},
                ]
            ),
            rollout_config=_rollout_config_stub(),
            requested_stage="canary_live",
        )

        self.assertEqual(decision["decision_status"], "DENY")
        self.assertIn("certification_not_pass", decision["failed_reason_codes"])
        self.assertIn(
            "certification_blockers_present",
            decision["failed_reason_codes"],
        )

    def test_passed_certification_and_complete_approvals_allow_stage_enablement(self) -> None:
        decision = build_canary_stage_enablement_decision(
            certification_report=_certification_report_stub(),
            approval_record=_approval_record_stub(
                approvals=[
                    {"actor": "release_manager", "decision": "approved"},
                    {"actor": "runtime_operator_on_call", "decision": "approved"},
                ]
            ),
            rollout_config=_rollout_config_stub(),
            requested_stage="canary_live",
        )

        self.assertEqual(decision["decision_status"], "ALLOW")
        self.assertTrue(decision["canary_stage_enablement_allowed"])
        self.assertEqual(decision["failed_reason_codes"], [])
        self.assertTrue(decision["evidence"]["certification_hash"])
        self.assertTrue(decision["evidence"]["approval_record_hash"])
        self.assertTrue(decision["evidence"]["decision_hash"])

    def test_runner_appends_audit_events_for_each_decision(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            certification_path = root / "certification.json"
            approval_path = root / "approval_record.json"
            rollout_config_path = root / "rollout_config.json"
            decision_output = root / "decision.json"
            audit_output = root / "audit.jsonl"

            certification_path.write_text(
                json.dumps(_certification_report_stub(), indent=2) + "\n",
                encoding="utf-8",
            )
            rollout_config_path.write_text(
                json.dumps(_rollout_config_stub(), indent=2) + "\n",
                encoding="utf-8",
            )

            approval_path.write_text(
                json.dumps(
                    _approval_record_stub(
                        approvals=[
                            {"actor": "release_manager", "decision": "approved"},
                            {
                                "actor": "runtime_operator_on_call",
                                "decision": "approved",
                            },
                        ]
                    ),
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            allow_result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--certification-report",
                    str(certification_path),
                    "--approval-record",
                    str(approval_path),
                    "--rollout-config",
                    str(rollout_config_path),
                    "--decision-output",
                    str(decision_output),
                    "--audit-output",
                    str(audit_output),
                    "--actor",
                    "release_manager",
                    "--reason",
                    "promotion-approved",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(
                allow_result.returncode,
                0,
                msg=allow_result.stderr or allow_result.stdout,
            )
            allow_decision = _read_json(decision_output)
            self.assertEqual(allow_decision["decision_status"], "ALLOW")

            approval_path.write_text(
                json.dumps(
                    _approval_record_stub(
                        approvals=[{"actor": "release_manager", "decision": "approved"}]
                    ),
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            deny_result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--certification-report",
                    str(certification_path),
                    "--approval-record",
                    str(approval_path),
                    "--rollout-config",
                    str(rollout_config_path),
                    "--decision-output",
                    str(decision_output),
                    "--audit-output",
                    str(audit_output),
                    "--actor",
                    "release_manager",
                    "--reason",
                    "promotion-denied-missing-approver",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(deny_result.returncode, 0)
            deny_decision = _read_json(decision_output)
            self.assertEqual(deny_decision["decision_status"], "DENY")

            audit_rows = _read_jsonl(audit_output)
            self.assertEqual(len(audit_rows), 2)
            self.assertEqual(audit_rows[0]["decision_status"], "ALLOW")
            self.assertEqual(audit_rows[1]["decision_status"], "DENY")
            self.assertEqual(
                audit_rows[0]["schema_version"],
                CANARY_STAGE_ENABLEMENT_AUDIT_EVENT_SCHEMA_VERSION,
            )
            self.assertEqual(
                audit_rows[1]["schema_version"],
                CANARY_STAGE_ENABLEMENT_AUDIT_EVENT_SCHEMA_VERSION,
            )
            self.assertTrue(audit_rows[0]["decision_hash"])
            self.assertTrue(audit_rows[1]["decision_hash"])


if __name__ == "__main__":
    unittest.main()
