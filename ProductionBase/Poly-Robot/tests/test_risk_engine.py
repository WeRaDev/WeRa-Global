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


PROFILE_PATH = (
    ROOT_DIR / "config" / "parameters" / "profiles" / "mvp_test_token.v1.json"
)


def _load_parameters() -> dict:
    payload = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    return payload["values"]


def _build_event(*, metadata: dict | None = None) -> MarketEvent:
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
        metadata=dict(metadata or {}),
    )


def _build_decision(
    consensus_votes: int,
    *,
    action: Literal["BUY", "HOLD"] = "BUY",
    win_probability: float = 0.82,
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
        single_result = self.engine.evaluate(
            self.event, single_vote_decision, portfolio
        )

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

    def test_denies_when_entries_are_suppressed_for_ingestion_degradation(self) -> None:
        event = _build_event(
            metadata={
                "suppress_new_entries": True,
                "ingestion_degraded_entry_suppressed": True,
                "ingestion_degraded_streak": 3,
            }
        )
        portfolio = PortfolioState(
            bankroll=1000.0,
            day_start_equity=1000.0,
            current_equity=1000.0,
        )
        decision = _build_decision(consensus_votes=2)
        result = self.engine.evaluate(event, decision, portfolio)

        self.assertFalse(result.allowed)
        self.assertIn("entry_suppressed_for_ingestion_degradation", result.reasons)
        self.assertFalse(result.metadata["state_refresh_event"])
        self.assertTrue(result.metadata["ingestion_degraded_entry_suppressed"])
        self.assertEqual(result.metadata["ingestion_degraded_streak"], 3)

    def test_denies_when_entries_are_suppressed_for_inventory_aging(self) -> None:
        event = _build_event(
            metadata={
                "suppress_new_entries": True,
                "inventory_aging_derisk_active": True,
            }
        )
        portfolio = PortfolioState(
            bankroll=1000.0,
            day_start_equity=1000.0,
            current_equity=1000.0,
        )
        decision = _build_decision(consensus_votes=2)
        result = self.engine.evaluate(event, decision, portfolio)

        self.assertFalse(result.allowed)
        self.assertIn("entry_suppressed_for_inventory_aging", result.reasons)
        self.assertFalse(result.metadata["state_refresh_event"])
        self.assertFalse(result.metadata["ingestion_degraded_entry_suppressed"])
        self.assertTrue(result.metadata["inventory_aging_derisk_active"])

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

    def test_denies_when_net_edge_after_costs_is_non_positive(self) -> None:
        portfolio = PortfolioState(
            bankroll=1000.0,
            day_start_equity=1000.0,
            current_equity=1000.0,
        )
        decision = _build_decision(consensus_votes=2, win_probability=0.651)
        result = self.engine.evaluate(self.event, decision, portfolio)

        self.assertFalse(result.allowed)
        self.assertIn("non_positive_net_edge_after_costs", result.reasons)
        self.assertGreater(result.metadata["fee_rate_bps"], 0)

    def test_scales_size_when_expected_costs_reduce_edge(self) -> None:
        low_cost_parameters = dict(self.parameters)
        low_cost_parameters["ops.fee_rate_bps"] = 0
        low_cost_parameters["execution.max_slippage_bps"] = 0
        low_cost_engine = RiskEngine(low_cost_parameters)

        portfolio = PortfolioState(
            bankroll=1000.0,
            day_start_equity=1000.0,
            current_equity=1000.0,
        )
        decision = _build_decision(consensus_votes=2, win_probability=0.68)
        low_cost_result = low_cost_engine.evaluate(self.event, decision, portfolio)
        cost_aware_result = self.engine.evaluate(self.event, decision, portfolio)

        self.assertTrue(low_cost_result.allowed)
        self.assertTrue(cost_aware_result.allowed)
        self.assertIn("net_edge_size_scaled", cost_aware_result.reasons)
        self.assertLess(
            cost_aware_result.approved_notional, low_cost_result.approved_notional
        )
    def test_scales_size_when_domain_budget_is_low(self) -> None:
        portfolio = PortfolioState(
            bankroll=1000.0,
            day_start_equity=1000.0,
            current_equity=1000.0,
        )
        decision = _build_decision(consensus_votes=2, win_probability=0.78)
        full_budget_event = _build_event(
            metadata={
                "domain_key": "crypto",
                "domain_allocation_budget": 1.0,
            }
        )
        low_budget_event = _build_event(
            metadata={
                "domain_key": "crypto",
                "domain_allocation_budget": 0.2,
            }
        )

        full_budget_result = self.engine.evaluate(
            full_budget_event, decision, portfolio
        )
        low_budget_result = self.engine.evaluate(
            low_budget_event, decision, portfolio
        )

        self.assertTrue(full_budget_result.allowed)
        self.assertTrue(low_budget_result.allowed)
        self.assertIn("domain_budget_scaled_size", low_budget_result.reasons)
        self.assertLess(
            low_budget_result.approved_notional, full_budget_result.approved_notional
        )
        self.assertLess(low_budget_result.metadata["domain_budget_scale"], 1.0)

    def test_denies_when_domain_budget_is_exhausted(self) -> None:
        portfolio = PortfolioState(
            bankroll=1000.0,
            day_start_equity=1000.0,
            current_equity=1000.0,
        )
        decision = _build_decision(consensus_votes=2)
        event = _build_event(
            metadata={
                "domain_key": "sports",
                "domain_allocation_budget": 0.0,
            }
        )
        result = self.engine.evaluate(event, decision, portfolio)

        self.assertFalse(result.allowed)
        self.assertIn("domain_budget_exhausted", result.reasons)
        self.assertEqual(result.metadata["domain_key"], "sports")

    def test_denies_when_domain_exposure_limit_is_reached(self) -> None:
        constrained_parameters = dict(self.parameters)
        constrained_parameters["risk.max_domain_exposure_fraction"] = 0.2
        constrained_engine = RiskEngine(constrained_parameters)
        portfolio = PortfolioState(
            bankroll=1000.0,
            day_start_equity=1000.0,
            current_equity=1000.0,
        )
        decision = _build_decision(consensus_votes=2)
        event = _build_event(
            metadata={
                "domain_key": "politics",
                "domain_open_notional_usd": 220.0,
                "domain_allocation_budget": 1.0,
            }
        )
        result = constrained_engine.evaluate(event, decision, portfolio)

        self.assertFalse(result.allowed)
        self.assertIn("domain_exposure_limit_reached", result.reasons)
        self.assertEqual(result.metadata["domain_key"], "politics")


if __name__ == "__main__":
    unittest.main()
