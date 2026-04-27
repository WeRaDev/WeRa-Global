from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from poly_robot.canary_readiness import build_canary_readiness_report  # noqa: E402
from poly_robot.schemas import (  # noqa: E402
    CANARY_ROLLOUT_CERTIFICATION_REPORT_SCHEMA_VERSION,
)


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


class CanaryReadinessTests(unittest.TestCase):
    def test_clean_rehearsal_report_passes_but_requires_manual_approval_for_enablement(
        self,
    ) -> None:
        report = build_canary_readiness_report(
            rehearsal_report=_rehearsal_report_stub(),
            approval_status="pending",
        )

        self.assertEqual(
            report["schema_version"],
            CANARY_ROLLOUT_CERTIFICATION_REPORT_SCHEMA_VERSION,
        )
        self.assertEqual(report["overall_status"], "PASS")
        self.assertEqual(report["readiness_score"], 100.0)
        self.assertEqual(report["blockers"], [])
        self.assertFalse(report["promotion_decision"]["canary_enablement_allowed"])
        self.assertEqual(report["promotion_decision"]["approval_status"], "pending")

    def test_clean_rehearsal_report_with_approved_status_allows_enablement(self) -> None:
        report = build_canary_readiness_report(
            rehearsal_report=_rehearsal_report_stub(),
            approval_status="approved",
            approval_actor="release_manager",
        )

        self.assertEqual(report["overall_status"], "PASS")
        self.assertTrue(report["promotion_decision"]["canary_enablement_allowed"])
        self.assertEqual(report["promotion_decision"]["approval_status"], "approved")

    def test_critical_rollback_recommendation_is_fail_fast_blocker(self) -> None:
        rehearsal_report = _rehearsal_report_stub()
        rehearsal_report["rollback_recommendations"] = [
            {
                "trigger": "kill_switch_gate_missing",
                "severity": "critical",
                "condition": "kill_switch gate did not pass",
            }
        ]
        rehearsal_report["summary"]["rollback_recommendation_count"] = 1

        report = build_canary_readiness_report(
            rehearsal_report=rehearsal_report,
            approval_status="approved",
        )

        self.assertEqual(report["overall_status"], "FAIL")
        self.assertFalse(report["promotion_decision"]["canary_enablement_allowed"])
        blocker_codes = {row["code"] for row in report["blockers"]}
        self.assertIn(
            "unresolved_rollback_trigger:kill_switch_gate_missing",
            blocker_codes,
        )
        criteria = {
            row["id"]: row for row in report["criteria"] if isinstance(row, dict)
        }
        self.assertFalse(criteria["no_blocking_rollback_recommendations"]["passed"])
        self.assertEqual(
            criteria["no_blocking_rollback_recommendations"]["reason_code"],
            "blocking_rollback_recommendations_present",
        )

    def test_required_control_scenario_failure_blocks_certification(self) -> None:
        rehearsal_report = _rehearsal_report_stub()
        rehearsal_report["scenario_results"][1]["status"] = "FAIL"
        rehearsal_report["summary"]["failed_scenarios"] = 1
        rehearsal_report["summary"]["overall_status"] = "FAILED"
        report = build_canary_readiness_report(
            rehearsal_report=rehearsal_report,
            approval_status="approved",
        )

        self.assertEqual(report["overall_status"], "FAIL")
        criteria = {
            row["id"]: row for row in report["criteria"] if isinstance(row, dict)
        }
        self.assertFalse(criteria["required_control_scenarios_passed"]["passed"])
        self.assertEqual(
            criteria["required_control_scenarios_passed"]["reason_code"],
            "runtime_control_scenario_failed_or_missing",
        )


if __name__ == "__main__":
    unittest.main()
