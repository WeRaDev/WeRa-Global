from __future__ import annotations

from typing import Any

from .contracts import (
    MarketEvent,
    PortfolioState,
    RiskDecision,
    RiskModule,
    StrategyDecision,
)

def _coerce_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    return str(value).strip().lower() in {"1", "true", "yes", "on"}

def _coerce_float(value: Any, *, default: float = 0.0) -> float:
    if value is None:
        return default
    if isinstance(value, str) and not value.strip():
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def kelly_fraction(*, p_win: float, market_price: float) -> float:
    if market_price <= 0 or market_price >= 1:
        return 0.0
    p = max(min(p_win, 0.999), 0.001)
    q = 1 - p
    b = (1 / market_price) - 1
    if b <= 0:
        return 0.0
    return (p * b - q) / b

def estimate_expected_slippage_bps(
    *, event: MarketEvent, notional: float, max_slippage_bps: int
) -> int:
    if notional <= 0 or max_slippage_bps <= 0:
        return 0
    available_depth = max(1.0, min(event.bids_depth_usd, event.asks_depth_usd))
    depth_utilization = min(1.0, notional / available_depth)
    estimated_bps = int(round(max_slippage_bps * depth_utilization))
    if estimated_bps <= 0 and depth_utilization > 0:
        return 1
    return max(0, min(max_slippage_bps, estimated_bps))


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
        if _coerce_bool(event.metadata.get("suppress_new_entries")):
            state_refresh_event = _coerce_bool(event.metadata.get("state_refresh_event"))
            ingestion_degraded_entry_suppressed = _coerce_bool(
                event.metadata.get("ingestion_degraded_entry_suppressed")
            )
            inventory_aging_derisk_active = _coerce_bool(
                event.metadata.get("inventory_aging_derisk_active")
            )
            if state_refresh_event:
                suppression_reason = "entry_suppressed_for_state_refresh"
            elif ingestion_degraded_entry_suppressed:
                suppression_reason = "entry_suppressed_for_ingestion_degradation"
            elif inventory_aging_derisk_active:
                suppression_reason = "entry_suppressed_for_inventory_aging"
            else:
                suppression_reason = "entry_suppressed_by_runtime_gate"
            return RiskDecision(
                allowed=False,
                approved_notional=0.0,
                approved_fraction=0.0,
                kill_switch=False,
                reasons=(suppression_reason,),
                metadata={
                    "state_refresh_event": state_refresh_event,
                    "ingestion_degraded_entry_suppressed": (
                        ingestion_degraded_entry_suppressed
                    ),
                    "ingestion_degraded_streak": int(
                        event.metadata.get("ingestion_degraded_streak", 0) or 0
                    ),
                    "inventory_aging_derisk_active": inventory_aging_derisk_active,
                },
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

        max_market_exposure = float(
            self.parameters["risk.max_market_exposure_fraction"]
        )
        current_market_exposure = portfolio.market_exposure_fraction(event.market_id)
        if current_market_exposure >= max_market_exposure:
            return RiskDecision(
                allowed=False,
                approved_notional=0.0,
                approved_fraction=0.0,
                kill_switch=False,
                reasons=("market_exposure_limit_reached",),
            )

        max_portfolio_exposure = float(
            self.parameters["risk.max_portfolio_exposure_fraction"]
        )
        current_total_exposure = portfolio.total_exposure_fraction
        if current_total_exposure >= max_portfolio_exposure:
            return RiskDecision(
                allowed=False,
                approved_notional=0.0,
                approved_fraction=0.0,
                kill_switch=False,
                reasons=("portfolio_exposure_limit_reached",),
            )
        domain_key = str(event.metadata.get("domain_key") or "general").strip() or "general"
        raw_domain_budget = event.metadata.get("domain_allocation_budget")
        domain_allocation_budget: float | None
        if raw_domain_budget is None:
            domain_allocation_budget = None
        else:
            domain_allocation_budget = min(
                1.0,
                max(0.0, _coerce_float(raw_domain_budget, default=0.0)),
            )
        max_domain_exposure = _coerce_float(
            self.parameters.get(
                "risk.max_domain_exposure_fraction",
                max_portfolio_exposure,
            ),
            default=max_portfolio_exposure,
        )
        if max_domain_exposure <= 0:
            max_domain_exposure = max_portfolio_exposure
        domain_open_notional = max(
            0.0,
            _coerce_float(
                event.metadata.get("domain_open_notional_usd"),
                default=0.0,
            ),
        )
        current_domain_exposure = (
            domain_open_notional / portfolio.bankroll
            if portfolio.bankroll > 0
            else 0.0
        )
        if current_domain_exposure >= max_domain_exposure:
            return RiskDecision(
                allowed=False,
                approved_notional=0.0,
                approved_fraction=0.0,
                kill_switch=False,
                reasons=("domain_exposure_limit_reached",),
                metadata={
                    "domain_key": domain_key,
                    "max_domain_exposure_fraction": max_domain_exposure,
                    "current_domain_exposure_fraction": current_domain_exposure,
                },
            )
        remaining_domain_fraction = max(
            0.0,
            max_domain_exposure - current_domain_exposure,
        )

        f_star = kelly_fraction(
            p_win=decision.win_probability, market_price=event.midpoint
        )
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
            approved_fraction *= float(
                self.parameters["execution.single_vote_size_factor"]
            )
            reasons.append("single_vote_reduced_size")
        else:
            return RiskDecision(
                allowed=False,
                approved_notional=0.0,
                approved_fraction=0.0,
                kill_switch=False,
                reasons=("insufficient_consensus_votes",),
            )

        domain_budget_scale = 1.0
        if domain_allocation_budget is not None:
            domain_min_budget_threshold = max(
                0.0,
                _coerce_float(
                    self.parameters.get("risk.domain_min_budget_threshold", 0.01),
                    default=0.01,
                ),
            )
            if domain_allocation_budget < domain_min_budget_threshold:
                return RiskDecision(
                    allowed=False,
                    approved_notional=0.0,
                    approved_fraction=0.0,
                    kill_switch=False,
                    reasons=("domain_budget_exhausted",),
                    metadata={
                        "domain_key": domain_key,
                        "domain_allocation_budget": domain_allocation_budget,
                        "domain_min_budget_threshold": (
                            domain_min_budget_threshold
                        ),
                    },
                )
            domain_min_allocation_scale = min(
                1.0,
                max(
                    0.0,
                    _coerce_float(
                        self.parameters.get(
                            "risk.domain_min_allocation_scale",
                            0.35,
                        ),
                        default=0.35,
                    ),
                ),
            )
            domain_budget_scale = domain_min_allocation_scale + (
                (1.0 - domain_min_allocation_scale)
                * domain_allocation_budget
            )
            if domain_budget_scale < 1.0:
                approved_fraction *= domain_budget_scale
                reasons.append("domain_budget_scaled_size")
        remaining_portfolio_fraction = max(
            0.0,
            max_portfolio_exposure - current_total_exposure,
        )
        remaining_market_fraction = max(
            0.0,
            max_market_exposure - current_market_exposure,
        )
        approved_fraction = min(
            approved_fraction,
            remaining_portfolio_fraction,
            remaining_market_fraction,
            remaining_domain_fraction,
        )

        if approved_fraction <= 0:
            return RiskDecision(
                allowed=False,
                approved_notional=0.0,
                approved_fraction=0.0,
                kill_switch=False,
                reasons=("no_remaining_risk_capacity",),
            )

        gross_edge_fraction = max(0.0, decision.win_probability - event.midpoint)
        max_slippage_bps = int(self.parameters["execution.max_slippage_bps"])
        fee_rate_bps = max(0, int(self.parameters.get("ops.fee_rate_bps", 0)))
        preliminary_notional = round(portfolio.bankroll * approved_fraction, 2)
        expected_slippage_bps = estimate_expected_slippage_bps(
            event=event,
            notional=preliminary_notional,
            max_slippage_bps=max_slippage_bps,
        )
        total_expected_cost_bps = fee_rate_bps + expected_slippage_bps
        total_expected_cost_fraction = total_expected_cost_bps / 10_000
        net_edge_fraction = gross_edge_fraction - total_expected_cost_fraction
        if net_edge_fraction <= 0:
            failure_reasons = list(reasons)
            failure_reasons.append("non_positive_net_edge_after_costs")
            return RiskDecision(
                allowed=False,
                approved_notional=0.0,
                approved_fraction=0.0,
                kill_switch=False,
                reasons=tuple(dict.fromkeys(failure_reasons)),
                metadata={
                    "max_slippage_bps": max_slippage_bps,
                    "expected_slippage_bps": expected_slippage_bps,
                    "fee_rate_bps": fee_rate_bps,
                    "gross_edge_bps": round(gross_edge_fraction * 10_000, 2),
                    "net_edge_bps": round(net_edge_fraction * 10_000, 2),
                    "domain_key": domain_key,
                    "domain_allocation_budget": domain_allocation_budget,
                    "domain_budget_scale": round(domain_budget_scale, 6),
                    "max_domain_exposure_fraction": max_domain_exposure,
                    "current_domain_exposure_fraction": (
                        current_domain_exposure
                    ),
                    "remaining_domain_exposure_fraction": (
                        remaining_domain_fraction
                    ),
                },
            )

        if gross_edge_fraction > 0:
            net_edge_scale = min(
                1.0, max(0.0, net_edge_fraction / gross_edge_fraction)
            )
            if net_edge_scale < 1.0:
                approved_fraction *= net_edge_scale
                reasons.append("net_edge_size_scaled")

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
            metadata={
                "max_slippage_bps": max_slippage_bps,
                "expected_slippage_bps": expected_slippage_bps,
                "fee_rate_bps": fee_rate_bps,
                "gross_edge_bps": round(gross_edge_fraction * 10_000, 2),
                "net_edge_bps": round(net_edge_fraction * 10_000, 2),
                "domain_key": domain_key,
                "domain_allocation_budget": domain_allocation_budget,
                "domain_budget_scale": round(domain_budget_scale, 6),
                "max_domain_exposure_fraction": max_domain_exposure,
                "current_domain_exposure_fraction": current_domain_exposure,
                "remaining_domain_exposure_fraction": (
                    remaining_domain_fraction
                ),
            },
        )
