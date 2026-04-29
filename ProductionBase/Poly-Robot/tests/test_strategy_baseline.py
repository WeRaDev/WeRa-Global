from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from poly_robot.contracts import MarketEvent, PortfolioState  # noqa: E402
from poly_robot.llm_policy import (  # noqa: E402
    CalibrationPolicy,
    CalibrationStatus,
    CalibrationThresholds,
)
from poly_robot.strategy_baseline import BaselineStrategy  # noqa: E402


PROFILE_PATH = (
    ROOT_DIR / "config" / "parameters" / "profiles" / "mvp_test_token.v1.json"
)


def _load_parameters() -> dict:
    return json.loads(PROFILE_PATH.read_text(encoding="utf-8"))["values"]


def _build_event(
    *,
    event_id: str,
    midpoint: float,
    estimated_probability: float,
    check_signals: dict[str, bool],
    base_confidence: float = 0.9,
    llm_confidence: float | None = 0.9,
    metadata: dict | None = None,
) -> MarketEvent:
    return MarketEvent(
        event_id=event_id,
        timestamp="2026-01-01T00:00:00Z",
        market_id="mkt-1",
        question="Test market",
        midpoint=midpoint,
        estimated_probability=estimated_probability,
        bids_depth_usd=3000.0,
        asks_depth_usd=3000.0,
        liquidity_usd=120000.0,
        hours_to_resolution=36.0,
        check_signals=check_signals,
        base_confidence=base_confidence,
        llm_confidence=llm_confidence,
        consensus_buy_votes=2,
        metadata=dict(metadata or {}),
    )


def _proven_policy() -> CalibrationPolicy:
    return CalibrationPolicy(
        thresholds=CalibrationThresholds(
            min_samples=1000,
            max_brier_score=0.2,
            max_expected_calibration_error=0.05,
        ),
        status=CalibrationStatus(
            proven=True,
            sample_count=2400,
            brier_score=0.1,
            expected_calibration_error=0.02,
            last_evaluated_at="2026-04-28T00:00:00Z",
        ),
    )


class BaselineStrategyTests(unittest.TestCase):
    def test_weighted_consensus_blocks_when_weighted_agreement_is_too_low(self) -> None:
        parameters = _load_parameters()
        strategy = BaselineStrategy(parameters, calibration_policy=None)
        event = _build_event(
            event_id="evt-low-weighted-consensus",
            midpoint=0.6,
            estimated_probability=0.76,
            check_signals={
                "base_rate": False,
                "news": True,
                "whale": False,
                "disposition": True,
            },
        )

        decision = strategy.evaluate(
            event,
            PortfolioState(
                bankroll=1000.0,
                day_start_equity=1000.0,
                current_equity=1000.0,
            ),
        )

        self.assertEqual(decision.action, "HOLD")
        self.assertEqual(
            decision.reasons,
            ("insufficient_weighted_check_agreement",),
        )
        self.assertEqual(decision.consensus_buy_votes, 1)
        self.assertEqual(decision.checks_passed, 2)
        self.assertAlmostEqual(
            decision.metadata["weighted_check_agreement"],
            0.425,
            places=6,
        )
        self.assertAlmostEqual(
            decision.metadata["weighted_check_threshold"],
            0.75,
            places=6,
        )
        self.assertEqual(decision.metadata["minimum_raw_checks_required"], 2)

    def test_weighted_consensus_uses_reliability_weights_for_gate(self) -> None:
        parameters = _load_parameters()
        strategy = BaselineStrategy(parameters, calibration_policy=None)
        event = _build_event(
            event_id="evt-weighted-pass",
            midpoint=0.6,
            estimated_probability=0.76,
            check_signals={
                "base_rate": True,
                "news": False,
                "whale": True,
                "disposition": False,
            },
            metadata={
                "check_reliability_weights": {
                    "base_rate": 5.0,
                    "news": 0.1,
                    "whale": 5.0,
                    "disposition": 0.1,
                }
            },
        )

        decision = strategy.evaluate(
            event,
            PortfolioState(
                bankroll=1000.0,
                day_start_equity=1000.0,
                current_equity=1000.0,
            ),
        )

        self.assertEqual(decision.action, "BUY")
        self.assertEqual(decision.reasons, ("entry_candidate",))
        self.assertEqual(decision.checks_passed, 2)
        self.assertEqual(decision.consensus_buy_votes, 1)
        self.assertGreater(decision.metadata["weighted_check_agreement"], 0.95)
        self.assertEqual(
            decision.metadata["check_weights"],
            {
                "base_rate": 5.0,
                "news": 0.1,
                "whale": 5.0,
                "disposition": 0.1,
            },
        )

    def test_strategy_emits_probability_oracle_metadata_for_calibrated_mode(
        self,
    ) -> None:
        parameters = _load_parameters()
        parameters["brain.llm_probability_calibration"] = "isotonic"
        strategy = BaselineStrategy(parameters, calibration_policy=_proven_policy())
        event = _build_event(
            event_id="evt-calibrated-buy",
            midpoint=0.55,
            estimated_probability=0.76,
            check_signals={
                "base_rate": True,
                "news": True,
                "whale": True,
                "disposition": False,
            },
            base_confidence=0.8,
            llm_confidence=0.9,
        )

        decision = strategy.evaluate(
            event,
            PortfolioState(
                bankroll=1000.0,
                day_start_equity=1000.0,
                current_equity=1000.0,
            ),
        )

        self.assertEqual(decision.action, "BUY")
        self.assertEqual(decision.llm_effective_mode, "isotonic")
        self.assertTrue(decision.llm_used_for_probability)
        self.assertEqual(decision.consensus_buy_votes, 2)
        self.assertEqual(decision.metadata["probability_oracle_source"], "calibrated_isotonic")
        self.assertEqual(decision.metadata["probability_oracle_effective_mode"], "isotonic")
        self.assertTrue(decision.metadata["probability_oracle_applied"])
        self.assertTrue(decision.metadata["probability_oracle_calibration_proven"])
        self.assertGreater(
            decision.metadata["calibrated_probability"],
            decision.metadata["raw_estimated_probability"],
        )
        self.assertGreater(decision.metadata["probability_oracle_reliability_score"], 0.0)
        self.assertEqual(decision.metadata["weighted_consensus_votes"], 2)


if __name__ == "__main__":
    unittest.main()
