from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from poly_robot.schemas import STRESS_CERTIFICATION_REPORT_SCHEMA_VERSION  # noqa: E402
from poly_robot.stress_certification import build_stress_certification_report  # noqa: E402


def _matrix_report_stub() -> dict:
    return {
        "schema_version": "replay_scenario_matrix.v1",
        "report_hash": "matrix-hash-123",
        "aggregate": {
            "scenario_count": 4,
            "total_allowed_trades": 3,
            "max_open_notional": 220.0,
            "zero_trade_scenarios": ["volatile_skew"],
        },
    }


def _soak_summary_stub(*, recovery_ok: bool = True) -> dict:
    return {
        "schema_version": "runtime_soak_summary.v1",
        "overall_status": "SUCCESS",
        "interval_status_counts": {
            "success": 4,
            "drill_expected_failure": 1,
            "drill_unexpected_success": 0,
            "failed": 0,
        },
        "recovery_checks": [
            {
                "interval_index": 2,
                "drill": "intentional_restart",
                "recovered_after_interval": recovery_ok,
            }
        ],
    }


class StressCertificationTests(unittest.TestCase):
    def test_passes_with_healthy_matrix_and_soak(self) -> None:
        report = build_stress_certification_report(
            matrix_report=_matrix_report_stub(),
            soak_summary=_soak_summary_stub(recovery_ok=True),
        )

        self.assertEqual(
            report["schema_version"], STRESS_CERTIFICATION_REPORT_SCHEMA_VERSION
        )
        self.assertEqual(report["overall_status"], "PASS")
        self.assertEqual(report["incidents"], [])
        self.assertTrue(all(item["passed"] for item in report["criteria"]))

    def test_fails_when_soak_summary_is_missing(self) -> None:
        report = build_stress_certification_report(
            matrix_report=_matrix_report_stub(),
            soak_summary=None,
        )

        self.assertEqual(report["overall_status"], "FAIL")
        codes = {incident["code"] for incident in report["incidents"]}
        self.assertIn("criterion_failed:soak_summary_present", codes)

    def test_fails_when_recovery_checks_report_unrecovered_interval(self) -> None:
        report = build_stress_certification_report(
            matrix_report=_matrix_report_stub(),
            soak_summary=_soak_summary_stub(recovery_ok=False),
        )

        self.assertEqual(report["overall_status"], "FAIL")
        codes = {incident["code"] for incident in report["incidents"]}
        self.assertIn("criterion_failed:soak_recovery_failures", codes)


if __name__ == "__main__":
    unittest.main()
