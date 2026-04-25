from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from poly_robot.llm_policy import (  # noqa: E402
    CalibrationPolicy,
    CalibrationStatus,
    CalibrationThresholds,
    is_calibration_proven,
    load_calibration_policy,
    merge_confidence,
    resolve_effective_mode,
)


CALIBRATION_POLICY_PATH = ROOT_DIR / "config" / "calibration" / "llm_reliability.v1.json"


class LLMPolicyTests(unittest.TestCase):
    def test_unproven_policy_forces_advisory_mode(self) -> None:
        policy = load_calibration_policy(CALIBRATION_POLICY_PATH)
        self.assertFalse(is_calibration_proven(policy))
        self.assertEqual(resolve_effective_mode("isotonic", policy), "advisory_only")

    def test_merge_confidence_uses_base_when_unproven(self) -> None:
        policy = load_calibration_policy(CALIBRATION_POLICY_PATH)
        confidence, used, mode, reason = merge_confidence(
            base_confidence=0.8,
            llm_confidence=0.95,
            requested_mode="isotonic",
            policy=policy,
        )
        self.assertAlmostEqual(confidence, 0.8, places=6)
        self.assertFalse(used)
        self.assertEqual(mode, "advisory_only")
        self.assertEqual(reason, "calibration_not_proven")

    def test_merge_confidence_uses_calibrated_mode_when_proven(self) -> None:
        policy = CalibrationPolicy(
            thresholds=CalibrationThresholds(
                min_samples=1000,
                max_brier_score=0.2,
                max_expected_calibration_error=0.05,
            ),
            status=CalibrationStatus(
                proven=True,
                sample_count=2000,
                brier_score=0.12,
                expected_calibration_error=0.02,
                last_evaluated_at="2026-04-25T13:10:00Z",
            ),
        )

        confidence, used, mode, reason = merge_confidence(
            base_confidence=0.7,
            llm_confidence=0.9,
            requested_mode="isotonic",
            policy=policy,
        )
        self.assertTrue(used)
        self.assertEqual(mode, "isotonic")
        self.assertEqual(reason, "calibrated_merge")
        self.assertGreater(confidence, 0.7)


if __name__ == "__main__":
    unittest.main()
