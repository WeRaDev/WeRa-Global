from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, Protocol
from .schemas import EVENT_SCHEMA_VERSION


@dataclass(frozen=True)
class MarketEvent:
    event_id: str
    timestamp: str
    market_id: str
    question: str
    midpoint: float
    estimated_probability: float
    bids_depth_usd: float
    asks_depth_usd: float
    liquidity_usd: float
    hours_to_resolution: float
    check_signals: dict[str, bool] = field(default_factory=dict)
    base_confidence: float = 0.0
    llm_confidence: float | None = None
    consensus_buy_votes: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)
    schema_version: str = EVENT_SCHEMA_VERSION

    @property
    def price_gap(self) -> float:
        return abs(self.estimated_probability - self.midpoint)
    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "event_id": self.event_id,
            "timestamp": self.timestamp,
            "market_id": self.market_id,
            "question": self.question,
            "midpoint": self.midpoint,
            "estimated_probability": self.estimated_probability,
            "bids_depth_usd": self.bids_depth_usd,
            "asks_depth_usd": self.asks_depth_usd,
            "liquidity_usd": self.liquidity_usd,
            "hours_to_resolution": self.hours_to_resolution,
            "check_signals": self.check_signals,
            "base_confidence": self.base_confidence,
            "llm_confidence": self.llm_confidence,
            "consensus_buy_votes": self.consensus_buy_votes,
            "metadata": self.metadata,
        }

    @staticmethod
    def from_dict(payload: dict[str, Any]) -> "MarketEvent":
        required_keys = [
            "schema_version",
            "event_id",
            "timestamp",
            "market_id",
            "question",
            "midpoint",
            "estimated_probability",
            "bids_depth_usd",
            "asks_depth_usd",
            "liquidity_usd",
            "hours_to_resolution",
        ]
        missing = [key for key in required_keys if key not in payload]
        if missing:
            raise ValueError(f"MarketEvent payload missing keys: {missing}")
        if payload["schema_version"] != EVENT_SCHEMA_VERSION:
            raise ValueError(
                f"Unsupported event schema_version {payload['schema_version']!r}; "
                f"expected {EVENT_SCHEMA_VERSION!r}."
            )

        return MarketEvent(
            event_id=str(payload["event_id"]),
            timestamp=str(payload["timestamp"]),
            market_id=str(payload["market_id"]),
            question=str(payload["question"]),
            midpoint=float(payload["midpoint"]),
            estimated_probability=float(payload["estimated_probability"]),
            bids_depth_usd=float(payload["bids_depth_usd"]),
            asks_depth_usd=float(payload["asks_depth_usd"]),
            liquidity_usd=float(payload["liquidity_usd"]),
            hours_to_resolution=float(payload["hours_to_resolution"]),
            check_signals=dict(payload.get("check_signals", {})),
            base_confidence=float(payload.get("base_confidence", 0.0)),
            llm_confidence=(
                float(payload["llm_confidence"])
                if payload.get("llm_confidence") is not None
                else None
            ),
            consensus_buy_votes=int(payload.get("consensus_buy_votes", 0)),
            metadata=dict(payload.get("metadata", {})),
            schema_version=str(payload["schema_version"]),
        )


@dataclass
class PortfolioState:
    bankroll: float
    day_start_equity: float
    current_equity: float
    open_notional: float = 0.0
    open_positions: int = 0
    market_notional: dict[str, float] = field(default_factory=dict)

    @property
    def daily_drawdown_fraction(self) -> float:
        if self.day_start_equity <= 0:
            return 0.0
        drawdown = max(0.0, self.day_start_equity - self.current_equity)
        return drawdown / self.day_start_equity

    @property
    def total_exposure_fraction(self) -> float:
        if self.bankroll <= 0:
            return 0.0
        return self.open_notional / self.bankroll

    def market_exposure_fraction(self, market_id: str) -> float:
        if self.bankroll <= 0:
            return 0.0
        return self.market_notional.get(market_id, 0.0) / self.bankroll

    def register_approved_trade(self, market_id: str, notional: float) -> None:
        self.open_notional += notional
        self.open_positions += 1
        self.market_notional[market_id] = self.market_notional.get(market_id, 0.0) + notional

    def clone(self) -> "PortfolioState":
        return PortfolioState(
            bankroll=self.bankroll,
            day_start_equity=self.day_start_equity,
            current_equity=self.current_equity,
            open_notional=self.open_notional,
            open_positions=self.open_positions,
            market_notional=dict(self.market_notional),
        )


@dataclass(frozen=True)
class StrategyDecision:
    action: Literal["BUY", "HOLD"]
    win_probability: float
    confidence: float
    checks_passed: int
    consensus_buy_votes: int
    llm_effective_mode: str
    llm_used_for_probability: bool
    reasons: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RiskDecision:
    allowed: bool
    approved_notional: float
    approved_fraction: float
    kill_switch: bool
    reasons: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ReplayRecord:
    event_id: str
    timestamp: str
    market_id: str
    strategy_decision: StrategyDecision
    risk_decision: RiskDecision


@dataclass(frozen=True)
class ReplayRun:
    records: list[ReplayRecord]
    final_portfolio: PortfolioState

    @property
    def allowed_trade_count(self) -> int:
        return sum(1 for record in self.records if record.risk_decision.allowed)


class StrategyModule(Protocol):
    def evaluate(self, event: MarketEvent, portfolio: PortfolioState) -> StrategyDecision:
        ...


class RiskModule(Protocol):
    def evaluate(
        self, event: MarketEvent, decision: StrategyDecision, portfolio: PortfolioState
    ) -> RiskDecision:
        ...
