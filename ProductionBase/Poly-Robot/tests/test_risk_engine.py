from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from typing import Literal


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from poly_robot.contracts import MarketEvent, PortfolioState, StrategyDecision  # noqa: E402
from poly_robot.risk_engine import RiskEngine  # noqa: E402


PROFILE_PATH = ROOT_DIR / "config" / "parameters" / "profiles" / "mvp_test_token.v1.json"


def _load_parameters() -> dict:
    payload = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    return payload["values"]


def _build_event() -> MarketEvent:
    return MarketEvent(
        event_id="evt-risk-1",
        timestamp="2026-01-01T00:00:00Z",
        market_id="mkt-risk",
        question="Risk test market?",
        midpoint=0.65,
        estimated_probability=0.82,
        bids_depth_usd=2000.0,
        asks_depth_usd=1800.0,
        liquidity_usd=90000.0,
        hours_to_resolution=24,
    )


def _build_decision(
    consensus_votes: int, *, action: Literal["BUY", "HOLD"] = "BUY", win_probability: float = 0.82
) -> StrategyDecision:
    return StrategyDecision(
        action=action,
        win_probability=win_probability,
        confidence=0.8,
        checks_passed=3,
        consensus_buy_votes=consensus_votes,
        llm_effective_mode="advisory_only",
        llm_used_for_probability=False,
        reasons=("entry_candidate",),
    )


class RiskEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.parameters = _load_parameters()
        self.engine = RiskEngine(self.parameters)
        self.event = _build_event()

    def test_allows_buy_when_within_limits(self) -> None:
        portfolio = PortfolioState(
            bankroll=1000.0,
            day_start_equity=1000.0,
            current_equity=980.0,
            open_notional=100.0,
            open_positions=1,
            market_notional={"mkt-other": 100.0},
        )
        decision = _build_decision(consensus_votes=2)
        result = self.engine.evaluate(self.event, decision, portfolio)

        self.assertTrue(result.allowed, result.reasons)
        self.assertGreater(result.approved_notional, 0.0)
        self.assertIn("consensus_full_size", result.reasons)

    def test_reduces_size_on_single_vote(self) -> None:
        portfolio = PortfolioState(
            bankroll=1000.0,
            day_start_equity=1000.0,
            current_equity=1000.0,
        )
        full_vote_decision = _build_decision(consensus_votes=2)
        single_vote_decision = _build_decision(consensus_votes=1)

        full_result = self.engine.evaluate(self.event, full_vote_decision, portfolio)
        single_result = self.engine.evaluate(self.event, single_vote_decision, portfolio)

        self.assertTrue(full_result.allowed)
        self.assertTrue(single_result.allowed)
        self.assertLess(single_result.approved_notional, full_result.approved_notional)
        self.assertIn("single_vote_reduced_size", single_result.reasons)

    def test_kill_switch_on_daily_drawdown(self) -> None:
        portfolio = PortfolioState(
            bankroll=1000.0,
            day_start_equity=1000.0,
            current_equity=900.0,
        )
        decision = _build_decision(consensus_votes=2)
        result = self.engine.evaluate(self.event, decision, portfolio)

        self.assertFalse(result.allowed)
        self.assertTrue(result.kill_switch)
        self.assertIn("daily_drawdown_kill_switch", result.reasons)

    def test_denies_when_strategy_is_not_buy(self) -> None:
        portfolio = PortfolioState(
            bankroll=1000.0,
            day_start_equity=1000.0,
            current_equity=1000.0,
        )
        decision = _build_decision(consensus_votes=2, action="HOLD")
        result = self.engine.evaluate(self.event, decision, portfolio)

        self.assertFalse(result.allowed)
        self.assertIn("strategy_not_buy", result.reasons)

    def test_denies_when_max_concurrent_positions_reached(self) -> None:
        portfolio = PortfolioState(
            bankroll=1000.0,
            day_start_equity=1000.0,
            current_equity=1000.0,
            open_notional=250.0,
            open_positions=6,
            market_notional={"mkt-other": 250.0},
        )
        decision = _build_decision(consensus_votes=2)
        result = self.engine.evaluate(self.event, decision, portfolio)

        self.assertFalse(result.allowed)
        self.assertIn("max_concurrent_positions_reached", result.reasons)

    def test_denies_when_market_exposure_limit_reached(self) -> None:
        portfolio = PortfolioState(
            bankroll=1000.0,
            day_start_equity=1000.0,
            current_equity=1000.0,
            open_notional=250.0,
            open_positions=2,
            market_notional={"mkt-risk": 250.0},
        )
        decision = _build_decision(consensus_votes=2)
        result = self.engine.evaluate(self.event, decision, portfolio)

        self.assertFalse(result.allowed)
        self.assertIn("market_exposure_limit_reached", result.reasons)

    def test_denies_when_portfolio_exposure_limit_reached(self) -> None:
        portfolio = PortfolioState(
            bankroll=1000.0,
            day_start_equity=1000.0,
            current_equity=1000.0,
            open_notional=600.0,
            open_positions=4,
            market_notional={"mkt-other": 300.0, "mkt-alt": 300.0},
        )
        decision = _build_decision(consensus_votes=2)
        result = self.engine.evaluate(self.event, decision, portfolio)

        self.assertFalse(result.allowed)
        self.assertIn("portfolio_exposure_limit_reached", result.reasons)

    def test_denies_when_consensus_votes_insufficient(self) -> None:
        portfolio = PortfolioState(
            bankroll=1000.0,
            day_start_equity=1000.0,
            current_equity=1000.0,
        )
        decision = _build_decision(consensus_votes=0)
        result = self.engine.evaluate(self.event, decision, portfolio)

        self.assertFalse(result.allowed)
        self.assertIn("insufficient_consensus_votes", result.reasons)

    def test_denies_when_kelly_edge_is_non_positive(self) -> None:
        portfolio = PortfolioState(
            bankroll=1000.0,
            day_start_equity=1000.0,
            current_equity=1000.0,
        )
        decision = _build_decision(consensus_votes=2, win_probability=0.40)
        result = self.engine.evaluate(self.event, decision, portfolio)

        self.assertFalse(result.allowed)
        self.assertIn("non_positive_kelly_edge", result.reasons)

    def test_denies_when_approved_notional_rounds_to_zero(self) -> None:
        portfolio = PortfolioState(
            bankroll=0.01,
            day_start_equity=0.01,
            current_equity=0.01,
        )
        decision = _build_decision(consensus_votes=2)
        result = self.engine.evaluate(self.event, decision, portfolio)

        self.assertFalse(result.allowed)
        self.assertIn("approved_notional_zero", result.reasons)


if __name__ == "__main__":
    unittest.main()
