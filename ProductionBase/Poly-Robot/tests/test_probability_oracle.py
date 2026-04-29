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
)
from poly_robot.probability_oracle import (  # noqa: E402
    calibration_reliability_score,
    resolve_probability,
)


def _proven_policy(
    *,
    sample_count: int = 2000,
    brier_score: float = 0.1,
    expected_calibration_error: float = 0.02,
) -> CalibrationPolicy:
    return CalibrationPolicy(
        thresholds=CalibrationThresholds(
            min_samples=1000,
            max_brier_score=0.2,
            max_expected_calibration_error=0.05,
        ),
        status=CalibrationStatus(
            proven=True,
            sample_count=sample_count,
            brier_score=brier_score,
            expected_calibration_error=expected_calibration_error,
            last_evaluated_at="2026-04-28T00:00:00Z",
        ),
    )


class ProbabilityOracleTests(unittest.TestCase):
    def test_unproven_policy_uses_heuristic_fallback(self) -> None:
        policy = CalibrationPolicy(
            thresholds=CalibrationThresholds(
                min_samples=1000,
                max_brier_score=0.2,
                max_expected_calibration_error=0.05,
            ),
            status=CalibrationStatus(
                proven=False,
                sample_count=500,
                brier_score=0.25,
                expected_calibration_error=0.08,
                last_evaluated_at="2026-04-28T00:00:00Z",
            ),
        )

        result = resolve_probability(
            estimated_probability=0.73,
            midpoint=0.5,
            requested_mode="isotonic",
            policy=policy,
        )

        self.assertEqual(result.effective_mode, "advisory_only")
        self.assertEqual(result.source, "heuristic_fallback")
        self.assertFalse(result.calibration_proven)
        self.assertAlmostEqual(result.raw_probability, 0.73, places=6)
        self.assertAlmostEqual(result.probability, 0.73, places=6)
        self.assertAlmostEqual(result.drift, 0.0, places=6)
        self.assertAlmostEqual(result.drift_abs, 0.0, places=6)

    def test_isotonic_mode_applies_calibration_and_reports_reliability(self) -> None:
        policy = _proven_policy()
        score = calibration_reliability_score(policy)

        result = resolve_probability(
            estimated_probability=0.62,
            midpoint=0.5,
            requested_mode="isotonic",
            policy=policy,
        )

        self.assertAlmostEqual(score, 0.8, places=6)
        self.assertEqual(result.effective_mode, "isotonic")
        self.assertEqual(result.source, "calibrated_isotonic")
        self.assertTrue(result.calibration_proven)
        self.assertGreater(result.probability, result.raw_probability)
        self.assertAlmostEqual(
            result.drift,
            round(result.probability - result.raw_probability, 6),
            places=6,
        )
        self.assertEqual(result.reliability_score, round(score, 6))

    def test_platt_mode_clamps_extreme_probability_inputs(self) -> None:
        policy = _proven_policy(
            sample_count=3000,
            brier_score=0.0,
            expected_calibration_error=0.0,
        )

        result = resolve_probability(
            estimated_probability=5.0,
            midpoint=0.6,
            requested_mode="platt",
            policy=policy,
        )

        self.assertEqual(result.effective_mode, "platt")
        self.assertEqual(result.source, "calibrated_platt")
        self.assertTrue(result.calibration_proven)
        self.assertEqual(result.raw_probability, 0.999)
        self.assertGreaterEqual(result.probability, 0.001)
        self.assertLessEqual(result.probability, 0.999)
        self.assertEqual(result.reliability_score, 1.0)


if __name__ == "__main__":
    unittest.main()
