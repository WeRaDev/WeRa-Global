from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
SCRIPT_PATH = ROOT_DIR / "scripts" / "run_mode_promotion_gate.py"
POLICY_PATH = ROOT_DIR / "config" / "integration" / "mode_lifecycle_policy.v1.json"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from poly_robot.schemas import (  # noqa: E402
    MODE_PROMOTION_GATE_AUDIT_EVENT_SCHEMA_VERSION,
    MODE_PROMOTION_GATE_REPORT_SCHEMA_VERSION,
)


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


class ModePromotionGateScriptTests(unittest.TestCase):
    def test_paper_to_test_allows_when_required_evidence_and_approval_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            milestone_report_path = root / "milestone_c_sequence_summary.json"
            trl4_report_path = root / "trl4_report.json"
            output_path = root / "mode_promotion_gate_report.json"
            audit_path = root / "mode_promotion_audit.jsonl"

            _write_json(
                milestone_report_path,
                {
                    "schema_version": "milestone_c_sequence_report.v1",
                    "overall_status": "PASS",
                    "summary_hash": "abc123",
                },
            )
            _write_json(
                trl4_report_path,
                {
                    "schema_version": "trl4_profitability_report.v1",
                    "overall_status": "PASS",
                },
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--mode-lifecycle-policy",
                    str(POLICY_PATH),
                    "--current-mode",
                    "paper",
                    "--target-mode",
                    "test",
                    "--manual-approval-status",
                    "approved",
                    "--milestone-c-sequence-report",
                    str(milestone_report_path),
                    "--trl4-profitability-report",
                    str(trl4_report_path),
                    "--output",
                    str(output_path),
                    "--audit-output",
                    str(audit_path),
                    "--actor",
                    "test_runner",
                    "--reason",
                    "paper_to_test_gate_validation",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
            report = _read_json(output_path)
            self.assertEqual(
                report["schema_version"],
                MODE_PROMOTION_GATE_REPORT_SCHEMA_VERSION,
            )
            self.assertEqual(report["decision_status"], "ALLOW")
            self.assertTrue(report["promotion_allowed"])
            self.assertTrue(report["decision"]["allowed"])
            self.assertEqual(report["missing_evidence"], [])
            self.assertEqual(report["failing_evidence"], [])
            self.assertEqual(report["reason_codes"], [])
            self.assertTrue(report["evidence_inputs"]["milestone_c_sequence"]["passed"])
            self.assertTrue(report["evidence_inputs"]["trl4_profitability"]["passed"])

            audit_rows = _read_jsonl(audit_path)
            self.assertEqual(len(audit_rows), 1)
            audit_event = audit_rows[0]
            self.assertEqual(
                audit_event["schema_version"],
                MODE_PROMOTION_GATE_AUDIT_EVENT_SCHEMA_VERSION,
            )
            self.assertEqual(audit_event["decision_status"], "ALLOW")
            self.assertTrue(audit_event["promotion_allowed"])

    def test_test_to_live_denies_when_required_evidence_missing_or_failed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            canary_report_path = root / "canary_lifecycle_gate_report.json"
            test_mode_profitability_report_path = (
                root / "test_mode_profitability_report.json"
            )
            output_path = root / "mode_promotion_gate_report.json"
            audit_path = root / "mode_promotion_audit.jsonl"

            _write_json(
                canary_report_path,
                {
                    "schema_version": "canary_lifecycle_gate_report.v1",
                    "overall_status": "FAIL",
                    "statuses": {"enablement_decision_status": "DENY"},
                },
            )
            self.assertFalse(test_mode_profitability_report_path.exists())

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--mode-lifecycle-policy",
                    str(POLICY_PATH),
                    "--current-mode",
                    "test",
                    "--target-mode",
                    "live",
                    "--manual-approval-status",
                    "approved",
                    "--canary-lifecycle-gate-report",
                    str(canary_report_path),
                    "--test-mode-profitability-report",
                    str(test_mode_profitability_report_path),
                    "--output",
                    str(output_path),
                    "--audit-output",
                    str(audit_path),
                    "--actor",
                    "test_runner",
                    "--reason",
                    "test_to_live_gate_validation",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            report = _read_json(output_path)
            self.assertEqual(
                report["schema_version"],
                MODE_PROMOTION_GATE_REPORT_SCHEMA_VERSION,
            )
            self.assertEqual(report["decision_status"], "DENY")
            self.assertFalse(report["promotion_allowed"])
            self.assertFalse(report["decision"]["allowed"])
            self.assertIn("required_evidence_missing", report["reason_codes"])
            self.assertIn("required_evidence_not_pass", report["reason_codes"])
            self.assertIn("test_mode_profitability", report["missing_evidence"])
            self.assertIn("canary_lifecycle_gate", report["failing_evidence"])

            audit_rows = _read_jsonl(audit_path)
            self.assertEqual(len(audit_rows), 1)
            audit_event = audit_rows[0]
            self.assertEqual(audit_event["decision_status"], "DENY")
            self.assertFalse(audit_event["promotion_allowed"])


if __name__ == "__main__":
    unittest.main()
