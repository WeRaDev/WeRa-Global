from __future__ import annotations

from typing import Any

from .contracts import MarketEvent, PortfolioState, StrategyDecision, StrategyModule
from .llm_policy import CalibrationPolicy, merge_confidence


class BaselineStrategy(StrategyModule):
    def __init__(
        self, parameters: dict[str, Any], calibration_policy: CalibrationPolicy | None
    ):
        self.parameters = parameters
        self.calibration_policy = calibration_policy

    def evaluate(
        self, event: MarketEvent, portfolio: PortfolioState
    ) -> StrategyDecision:
        del portfolio

        reasons: list[str] = []

        min_gap = float(self.parameters["scanner.min_price_gap"])
        min_depth = float(self.parameters["scanner.min_side_depth_usd"])
        min_liquidity = float(self.parameters["scanner.min_market_liquidity_usd"])
        min_hours = float(self.parameters["scanner.min_hours_to_resolution"])
        max_hours = float(self.parameters["scanner.max_hours_to_resolution"])

        if event.estimated_probability <= event.midpoint:
            reasons.append("non_positive_edge")
        if event.price_gap < min_gap:
            reasons.append("price_gap_below_threshold")
        if min(event.bids_depth_usd, event.asks_depth_usd) < min_depth:
            reasons.append("insufficient_orderbook_depth")
        if event.liquidity_usd < min_liquidity:
            reasons.append("insufficient_market_liquidity")
        if event.hours_to_resolution < min_hours:
            reasons.append("resolution_too_close")
        if event.hours_to_resolution > max_hours:
            reasons.append("resolution_too_far")

        if reasons:
            return StrategyDecision(
                action="HOLD",
                win_probability=max(min(event.estimated_probability, 0.999), 0.001),
                confidence=max(min(event.base_confidence, 1.0), 0.0),
                checks_passed=0,
                consensus_buy_votes=event.consensus_buy_votes,
                llm_effective_mode="advisory_only",
                llm_used_for_probability=False,
                reasons=tuple(reasons),
            )

        required_checks = ["base_rate", "news", "whale", "disposition"]
        checks_passed = sum(
            1
            for check in required_checks
            if bool(event.check_signals.get(check, False))
        )
        min_checks_agreement = int(self.parameters["brain.min_checks_agreement"])
        if checks_passed < min_checks_agreement:
            return StrategyDecision(
                action="HOLD",
                win_probability=max(min(event.estimated_probability, 0.999), 0.001),
                confidence=max(min(event.base_confidence, 1.0), 0.0),
                checks_passed=checks_passed,
                consensus_buy_votes=event.consensus_buy_votes,
                llm_effective_mode="advisory_only",
                llm_used_for_probability=False,
                reasons=("insufficient_check_agreement",),
            )

        final_confidence, llm_used, effective_mode, llm_reason = merge_confidence(
            base_confidence=event.base_confidence,
            llm_confidence=event.llm_confidence,
            requested_mode=str(self.parameters["brain.llm_probability_calibration"]),
            policy=self.calibration_policy,
        )

        min_thesis_confidence = float(self.parameters["brain.min_thesis_confidence"])
        if final_confidence < min_thesis_confidence:
            return StrategyDecision(
                action="HOLD",
                win_probability=max(min(event.estimated_probability, 0.999), 0.001),
                confidence=final_confidence,
                checks_passed=checks_passed,
                consensus_buy_votes=event.consensus_buy_votes,
                llm_effective_mode=effective_mode,
                llm_used_for_probability=llm_used,
                reasons=("confidence_below_threshold",),
                metadata={"llm_reason": llm_reason},
            )

        return StrategyDecision(
            action="BUY",
            win_probability=max(min(event.estimated_probability, 0.999), 0.001),
            confidence=final_confidence,
            checks_passed=checks_passed,
            consensus_buy_votes=event.consensus_buy_votes,
            llm_effective_mode=effective_mode,
            llm_used_for_probability=llm_used,
            reasons=("entry_candidate",),
            metadata={"llm_reason": llm_reason},
        )
