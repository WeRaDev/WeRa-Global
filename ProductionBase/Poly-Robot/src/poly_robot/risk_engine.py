from __future__ import annotations

from typing import Any

from .contracts import MarketEvent, PortfolioState, RiskDecision, RiskModule, StrategyDecision


def kelly_fraction(*, p_win: float, market_price: float) -> float:
    if market_price <= 0 or market_price >= 1:
        return 0.0
    p = max(min(p_win, 0.999), 0.001)
    q = 1 - p
    b = (1 / market_price) - 1
    if b <= 0:
        return 0.0
    return (p * b - q) / b


class RiskEngine(RiskModule):
    def __init__(self, parameters: dict[str, Any]):
        self.parameters = parameters

    def evaluate(
        self, event: MarketEvent, decision: StrategyDecision, portfolio: PortfolioState
    ) -> RiskDecision:
        reasons: list[str] = []

        if decision.action != "BUY":
            return RiskDecision(
                allowed=False,
                approved_notional=0.0,
                approved_fraction=0.0,
                kill_switch=False,
                reasons=("strategy_not_buy",),
            )

        max_daily_drawdown = float(self.parameters["risk.max_daily_drawdown_fraction"])
        if portfolio.daily_drawdown_fraction >= max_daily_drawdown:
            return RiskDecision(
                allowed=False,
                approved_notional=0.0,
                approved_fraction=0.0,
                kill_switch=True,
                reasons=("daily_drawdown_kill_switch",),
            )

        max_concurrent = int(self.parameters["risk.max_concurrent_positions"])
        if portfolio.open_positions >= max_concurrent:
            return RiskDecision(
                allowed=False,
                approved_notional=0.0,
                approved_fraction=0.0,
                kill_switch=False,
                reasons=("max_concurrent_positions_reached",),
            )

        max_market_exposure = float(self.parameters["risk.max_market_exposure_fraction"])
        current_market_exposure = portfolio.market_exposure_fraction(event.market_id)
        if current_market_exposure >= max_market_exposure:
            return RiskDecision(
                allowed=False,
                approved_notional=0.0,
                approved_fraction=0.0,
                kill_switch=False,
                reasons=("market_exposure_limit_reached",),
            )

        max_portfolio_exposure = float(self.parameters["risk.max_portfolio_exposure_fraction"])
        current_total_exposure = portfolio.total_exposure_fraction
        if current_total_exposure >= max_portfolio_exposure:
            return RiskDecision(
                allowed=False,
                approved_notional=0.0,
                approved_fraction=0.0,
                kill_switch=False,
                reasons=("portfolio_exposure_limit_reached",),
            )

        f_star = kelly_fraction(p_win=decision.win_probability, market_price=event.midpoint)
        if f_star <= 0:
            return RiskDecision(
                allowed=False,
                approved_notional=0.0,
                approved_fraction=0.0,
                kill_switch=False,
                reasons=("non_positive_kelly_edge",),
            )

        kelly_cap = float(self.parameters["risk.kelly_cap_fraction"])
        max_position_fraction = float(self.parameters["risk.max_position_fraction"])
        approved_fraction = min(f_star, kelly_cap, max_position_fraction)

        min_consensus_votes = int(self.parameters["execution.min_consensus_buy_votes"])
        if decision.consensus_buy_votes >= min_consensus_votes:
            reasons.append("consensus_full_size")
        elif decision.consensus_buy_votes == 1:
            approved_fraction *= float(self.parameters["execution.single_vote_size_factor"])
            reasons.append("single_vote_reduced_size")
        else:
            return RiskDecision(
                allowed=False,
                approved_notional=0.0,
                approved_fraction=0.0,
                kill_switch=False,
                reasons=("insufficient_consensus_votes",),
            )

        remaining_portfolio_fraction = max(0.0, max_portfolio_exposure - current_total_exposure)
        remaining_market_fraction = max(0.0, max_market_exposure - current_market_exposure)
        approved_fraction = min(approved_fraction, remaining_portfolio_fraction, remaining_market_fraction)

        if approved_fraction <= 0:
            return RiskDecision(
                allowed=False,
                approved_notional=0.0,
                approved_fraction=0.0,
                kill_switch=False,
                reasons=("no_remaining_risk_capacity",),
            )

        approved_notional = round(portfolio.bankroll * approved_fraction, 2)
        if approved_notional <= 0:
            return RiskDecision(
                allowed=False,
                approved_notional=0.0,
                approved_fraction=0.0,
                kill_switch=False,
                reasons=("approved_notional_zero",),
            )

        return RiskDecision(
            allowed=True,
            approved_notional=approved_notional,
            approved_fraction=approved_fraction,
            kill_switch=False,
            reasons=tuple(reasons),
            metadata={"max_slippage_bps": int(self.parameters["execution.max_slippage_bps"])},
        )
