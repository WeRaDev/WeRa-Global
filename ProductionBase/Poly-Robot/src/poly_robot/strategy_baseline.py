from __future__ import annotations

from typing import Any

from .contracts import MarketEvent, PortfolioState, StrategyDecision, StrategyModule
from .llm_policy import CalibrationPolicy, merge_confidence
from .probability_oracle import resolve_probability


REQUIRED_CHECKS = ("base_rate", "news", "whale", "disposition")
DEFAULT_CHECK_WEIGHTS = {
    "base_rate": 1.1,
    "news": 0.9,
    "whale": 1.2,
    "disposition": 0.8,
}


def _to_positive_weight(value: Any, *, default: float) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return default
    if parsed <= 0:
        return default
    return parsed


def _resolve_check_weights(event: MarketEvent) -> dict[str, float]:
    raw_weights = event.metadata.get("check_reliability_weights")
    weights: dict[str, float] = {}
    for check_name in REQUIRED_CHECKS:
        default_weight = DEFAULT_CHECK_WEIGHTS[check_name]
        configured_weight = None
        if isinstance(raw_weights, dict):
            configured_weight = raw_weights.get(check_name)
        weights[check_name] = _to_positive_weight(
            configured_weight,
            default=default_weight,
        )
    return weights


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
        min_gap = float(self.parameters["scanner.min_price_gap"])
        min_depth = float(self.parameters["scanner.min_side_depth_usd"])
        min_liquidity = float(self.parameters["scanner.min_market_liquidity_usd"])
        min_hours = float(self.parameters["scanner.min_hours_to_resolution"])
        max_hours = float(self.parameters["scanner.max_hours_to_resolution"])
        min_checks_agreement = int(self.parameters["brain.min_checks_agreement"])
        min_thesis_confidence = float(self.parameters["brain.min_thesis_confidence"])
        requested_llm_mode = str(self.parameters["brain.llm_probability_calibration"])

        check_signals = {
            check_name: bool(event.check_signals.get(check_name, False))
            for check_name in REQUIRED_CHECKS
        }
        check_weights = _resolve_check_weights(event)
        checks_passed = sum(
            1 for check_name in REQUIRED_CHECKS if check_signals[check_name]
        )
        total_check_weight = sum(check_weights.values())
        weighted_support = sum(
            check_weights[check_name]
            for check_name in REQUIRED_CHECKS
            if check_signals[check_name]
        )
        weighted_check_agreement = (
            weighted_support / total_check_weight if total_check_weight > 0 else 0.0
        )
        min_weighted_agreement = min(
            1.0,
            max(0.0, min_checks_agreement / max(1, len(REQUIRED_CHECKS))),
        )
        minimum_raw_checks_required = max(1, min_checks_agreement - 1)
        weighted_consensus_votes = (
            2
            if (
                checks_passed >= min_checks_agreement
                and weighted_check_agreement >= min_weighted_agreement
            )
            else 1
        )
        probability_oracle = resolve_probability(
            estimated_probability=event.estimated_probability,
            midpoint=event.midpoint,
            requested_mode=requested_llm_mode,
            policy=self.calibration_policy,
        )
        strategy_metadata = {
            "raw_estimated_probability": round(probability_oracle.raw_probability, 6),
            "calibrated_probability": round(probability_oracle.probability, 6),
            "probability_drift": probability_oracle.drift,
            "probability_drift_abs": probability_oracle.drift_abs,
            "probability_oracle_source": probability_oracle.source,
            "probability_oracle_effective_mode": probability_oracle.effective_mode,
            "probability_oracle_applied": (
                probability_oracle.source != "heuristic_fallback"
            ),
            "probability_oracle_calibration_proven": (
                probability_oracle.calibration_proven
            ),
            "probability_oracle_reliability_score": (
                probability_oracle.reliability_score
            ),
            "weighted_check_agreement": round(weighted_check_agreement, 6),
            "weighted_check_threshold": round(min_weighted_agreement, 6),
            "minimum_raw_checks_required": minimum_raw_checks_required,
            "weighted_consensus_votes": weighted_consensus_votes,
            "check_weights": {
                check_name: round(check_weights[check_name], 6)
                for check_name in REQUIRED_CHECKS
            },
        }

        pre_entry_reasons: list[str] = []
        if probability_oracle.probability <= event.midpoint:
            pre_entry_reasons.append("non_positive_edge")
        if event.price_gap < min_gap:
            pre_entry_reasons.append("price_gap_below_threshold")
        if min(event.bids_depth_usd, event.asks_depth_usd) < min_depth:
            pre_entry_reasons.append("insufficient_orderbook_depth")
        if event.liquidity_usd < min_liquidity:
            pre_entry_reasons.append("insufficient_market_liquidity")
        if event.hours_to_resolution < min_hours:
            pre_entry_reasons.append("resolution_too_close")
        if event.hours_to_resolution > max_hours:
            pre_entry_reasons.append("resolution_too_far")
        if pre_entry_reasons:
            return StrategyDecision(
                action="HOLD",
                win_probability=probability_oracle.probability,
                confidence=max(min(event.base_confidence, 1.0), 0.0),
                checks_passed=0,
                consensus_buy_votes=weighted_consensus_votes,
                llm_effective_mode="advisory_only",
                llm_used_for_probability=False,
                reasons=tuple(pre_entry_reasons),
                metadata={
                    **strategy_metadata,
                    "llm_reason": "pre_entry_filters_failed",
                    "pre_entry_reasons": tuple(pre_entry_reasons),
                },
            )

        weighted_gate_reasons: list[str] = []
        if checks_passed < minimum_raw_checks_required:
            weighted_gate_reasons.append("insufficient_check_agreement")
        if weighted_check_agreement < min_weighted_agreement:
            weighted_gate_reasons.append("insufficient_weighted_check_agreement")
        if weighted_gate_reasons:
            return StrategyDecision(
                action="HOLD",
                win_probability=probability_oracle.probability,
                confidence=max(min(event.base_confidence, 1.0), 0.0),
                checks_passed=checks_passed,
                consensus_buy_votes=weighted_consensus_votes,
                llm_effective_mode="advisory_only",
                llm_used_for_probability=False,
                reasons=tuple(weighted_gate_reasons),
                metadata={
                    **strategy_metadata,
                    "llm_reason": "weighted_consensus_gate_blocked",
                },
            )

        final_confidence, llm_used, effective_mode, llm_reason = merge_confidence(
            base_confidence=event.base_confidence,
            llm_confidence=event.llm_confidence,
            requested_mode=requested_llm_mode,
            policy=self.calibration_policy,
        )
        if final_confidence < min_thesis_confidence:
            return StrategyDecision(
                action="HOLD",
                win_probability=probability_oracle.probability,
                confidence=final_confidence,
                checks_passed=checks_passed,
                consensus_buy_votes=weighted_consensus_votes,
                llm_effective_mode=effective_mode,
                llm_used_for_probability=llm_used,
                reasons=("confidence_below_threshold",),
                metadata={
                    **strategy_metadata,
                    "llm_reason": llm_reason,
                },
            )

        return StrategyDecision(
            action="BUY",
            win_probability=probability_oracle.probability,
            confidence=final_confidence,
            checks_passed=checks_passed,
            consensus_buy_votes=weighted_consensus_votes,
            llm_effective_mode=effective_mode,
            llm_used_for_probability=llm_used,
            reasons=("entry_candidate",),
            metadata={
                **strategy_metadata,
                "llm_reason": llm_reason,
            },
        )
