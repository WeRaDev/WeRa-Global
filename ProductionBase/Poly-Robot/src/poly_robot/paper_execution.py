from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from .contracts import MarketEvent, RiskDecision


ExecutionStatus = Literal[
    "SKIPPED", "REJECTED", "EXPIRED", "PARTIALLY_FILLED", "FILLED"
]


@dataclass(frozen=True)
class ExecutionIntent:
    intent_id: str
    event_id: str
    timestamp: str
    market_id: str
    side: Literal["BUY"]
    requested_notional: float
    reference_price: float
    max_slippage_bps: int
    ttl_seconds: int
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ExecutionResult:
    status: ExecutionStatus
    requested_notional: float
    filled_notional: float
    reference_price: float
    fill_price: float | None
    slippage_bps: int
    fee_paid: float = 0.0
    slippage_cost: float = 0.0
    total_execution_cost: float = 0.0
    reasons: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_filled(self) -> bool:
        return self.filled_notional > 0


def _clamp_price(value: float) -> float:
    return min(max(value, 0.001), 0.999)


def _lifecycle_event(state: str, **details: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {"state": state}
    payload.update(details)
    return payload


def build_execution_intent(
    *, event: MarketEvent, risk_decision: RiskDecision, parameters: dict[str, Any]
) -> ExecutionIntent:
    if not risk_decision.allowed or risk_decision.approved_notional <= 0:
        raise ValueError(
            "Execution intent requires an allowed risk decision with positive notional."
        )

    return ExecutionIntent(
        intent_id=f"{event.event_id}:BUY",
        event_id=event.event_id,
        timestamp=event.timestamp,
        market_id=event.market_id,
        side="BUY",
        requested_notional=float(risk_decision.approved_notional),
        reference_price=float(event.midpoint),
        max_slippage_bps=int(parameters["execution.max_slippage_bps"]),
        ttl_seconds=int(parameters["execution.order_ttl_seconds"]),
        metadata={
            "approved_fraction": risk_decision.approved_fraction,
            "risk_reasons": list(risk_decision.reasons),
        },
    )


class PaperExecutionAdapter:
    def __init__(self, parameters: dict[str, Any], *, depth_fill_ratio: float = 0.8):
        self.parameters = parameters
        self.depth_fill_ratio = min(max(depth_fill_ratio, 0.1), 1.0)
        self.max_retry_attempts = max(
            0, int(parameters.get("ops.max_api_retry_attempts", 0))
        )
        self.retry_backoff_seconds = max(
            0.0, float(parameters.get("ops.retry_backoff_seconds", 0.0))
        )
        self.fee_rate_bps = max(0, int(parameters.get("ops.fee_rate_bps", 0)))

    def skip(
        self, *, event: MarketEvent, risk_decision: RiskDecision
    ) -> ExecutionResult:
        reasons = risk_decision.reasons or ("risk_denied",)
        return ExecutionResult(
            status="SKIPPED",
            requested_notional=float(risk_decision.approved_notional),
            filled_notional=0.0,
            reference_price=float(event.midpoint),
            fill_price=None,
            slippage_bps=0,
            reasons=tuple(f"risk:{reason}" for reason in reasons),
            metadata={
                "risk_allowed": risk_decision.allowed,
                "lifecycle": [
                    _lifecycle_event(
                        "SKIPPED",
                        reason=(
                            risk_decision.reasons[0]
                            if risk_decision.reasons
                            else "risk_denied"
                        ),
                    )
                ],
            },
        )

    def execute(
        self, *, event: MarketEvent, intent: ExecutionIntent
    ) -> ExecutionResult:
        lifecycle = [
            _lifecycle_event(
                "SUBMITTED", attempt=0, requested_notional=intent.requested_notional
            )
        ]
        if intent.requested_notional <= 0:
            lifecycle.append(
                _lifecycle_event("REJECTED", reason="invalid_requested_notional")
            )
            return ExecutionResult(
                status="REJECTED",
                requested_notional=float(intent.requested_notional),
                filled_notional=0.0,
                reference_price=float(intent.reference_price),
                fill_price=None,
                slippage_bps=0,
                reasons=("invalid_requested_notional",),
                metadata={"lifecycle": lifecycle},
            )

        base_latency_ms = self._extract_latency_ms(event)
        ttl_ms = max(int(intent.ttl_seconds), 1) * 1000
        if base_latency_ms > ttl_ms:
            lifecycle.append(
                _lifecycle_event(
                    "EXPIRED",
                    reason="order_ttl_exceeded",
                    latency_ms=base_latency_ms,
                    ttl_ms=ttl_ms,
                )
            )
            return ExecutionResult(
                status="EXPIRED",
                requested_notional=float(intent.requested_notional),
                filled_notional=0.0,
                reference_price=float(intent.reference_price),
                fill_price=None,
                slippage_bps=0,
                reasons=("order_ttl_exceeded",),
                metadata={
                    "latency_ms": base_latency_ms,
                    "ttl_ms": ttl_ms,
                    "lifecycle": lifecycle,
                },
            )
        replace_factor = float(self.parameters["execution.single_vote_size_factor"])
        active_notional = round(float(intent.requested_notional), 2)
        attempt = 0

        while True:
            retry_delay_ms = int(round(attempt * self.retry_backoff_seconds * 1000))
            effective_latency_ms = base_latency_ms + retry_delay_ms
            if effective_latency_ms > ttl_ms:
                lifecycle.append(
                    _lifecycle_event(
                        "EXPIRED",
                        attempt=attempt,
                        reason="order_ttl_exceeded",
                        latency_ms=effective_latency_ms,
                        ttl_ms=ttl_ms,
                    )
                )
                return ExecutionResult(
                    status="EXPIRED",
                    requested_notional=float(intent.requested_notional),
                    filled_notional=0.0,
                    reference_price=float(intent.reference_price),
                    fill_price=None,
                    slippage_bps=0,
                    reasons=("order_ttl_exceeded",),
                    metadata={
                        "latency_ms": effective_latency_ms,
                        "ttl_ms": ttl_ms,
                        "replace_count": attempt,
                        "lifecycle": lifecycle,
                    },
                )

            slippage_bps = self._estimate_slippage_bps(event, active_notional)
            if slippage_bps <= intent.max_slippage_bps:
                return self._finalize_fill(
                    event=event,
                    intent=intent,
                    active_notional=active_notional,
                    slippage_bps=slippage_bps,
                    attempt=attempt,
                    effective_latency_ms=effective_latency_ms,
                    ttl_ms=ttl_ms,
                    lifecycle=lifecycle,
                )

            lifecycle.append(
                _lifecycle_event(
                    "CANCELLED",
                    attempt=attempt,
                    reason="slippage_limit_breached",
                    requested_notional=active_notional,
                    estimated_slippage_bps=slippage_bps,
                    max_slippage_bps=intent.max_slippage_bps,
                )
            )
            if attempt >= self.max_retry_attempts:
                lifecycle.append(
                    _lifecycle_event(
                        "REJECTED",
                        attempt=attempt,
                        reason="slippage_limit_breached_after_retries",
                    )
                )
                return ExecutionResult(
                    status="REJECTED",
                    requested_notional=float(intent.requested_notional),
                    filled_notional=0.0,
                    reference_price=float(intent.reference_price),
                    fill_price=None,
                    slippage_bps=slippage_bps,
                    reasons=("slippage_limit_breached_after_retries",),
                    metadata={
                        "max_slippage_bps": intent.max_slippage_bps,
                        "replace_count": attempt,
                        "max_retry_attempts": self.max_retry_attempts,
                        "lifecycle": lifecycle,
                    },
                )

            replacement_notional = round(active_notional * replace_factor, 2)
            if replacement_notional <= 0 or replacement_notional >= active_notional:
                lifecycle.append(
                    _lifecycle_event(
                        "REJECTED",
                        attempt=attempt,
                        reason="invalid_replace_notional",
                        replace_factor=replace_factor,
                    )
                )
                return ExecutionResult(
                    status="REJECTED",
                    requested_notional=float(intent.requested_notional),
                    filled_notional=0.0,
                    reference_price=float(intent.reference_price),
                    fill_price=None,
                    slippage_bps=slippage_bps,
                    reasons=("invalid_replace_notional",),
                    metadata={
                        "replace_count": attempt,
                        "replace_factor": replace_factor,
                        "lifecycle": lifecycle,
                    },
                )

            attempt += 1
            active_notional = replacement_notional
            lifecycle.append(
                _lifecycle_event(
                    "REPLACED",
                    attempt=attempt,
                    replacement_notional=active_notional,
                    retry_backoff_seconds=self.retry_backoff_seconds,
                )
            )

    def _finalize_fill(
        self,
        *,
        event: MarketEvent,
        intent: ExecutionIntent,
        active_notional: float,
        slippage_bps: int,
        attempt: int,
        effective_latency_ms: int,
        ttl_ms: int,
        lifecycle: list[dict[str, Any]],
    ) -> ExecutionResult:
        fill_capacity_notional = max(
            0.0,
            min(event.bids_depth_usd, event.asks_depth_usd) * self.depth_fill_ratio,
        )
        filled_notional = round(min(active_notional, fill_capacity_notional), 2)
        if filled_notional <= 0:
            lifecycle.append(
                _lifecycle_event("REJECTED", reason="no_fill_capacity", attempt=attempt)
            )
            return ExecutionResult(
                status="REJECTED",
                requested_notional=float(intent.requested_notional),
                filled_notional=0.0,
                reference_price=float(intent.reference_price),
                fill_price=None,
                slippage_bps=slippage_bps,
                reasons=("no_fill_capacity",),
                metadata={
                    "latency_ms": effective_latency_ms,
                    "ttl_ms": ttl_ms,
                    "fill_capacity_notional": round(fill_capacity_notional, 2),
                    "replace_count": attempt,
                    "lifecycle": lifecycle,
                },
            )

        partial_by_replace = active_notional < intent.requested_notional
        partial_by_depth = filled_notional < active_notional

        status: ExecutionStatus = "FILLED"
        reasons = ["paper_fill_simulated"]
        if partial_by_replace or partial_by_depth:
            status = "PARTIALLY_FILLED"
            if partial_by_replace:
                reasons.insert(0, "cancel_replace_size_reduction")
            if partial_by_depth:
                reasons.insert(0, "partial_fill_depth_limited")

        fill_price = _clamp_price(intent.reference_price + (slippage_bps / 10_000))
        fee_paid = round(filled_notional * (self.fee_rate_bps / 10_000), 4)
        slippage_cost = round(filled_notional * (slippage_bps / 10_000), 4)
        total_execution_cost = round(fee_paid + slippage_cost, 4)

        lifecycle.append(
            _lifecycle_event(
                status,
                attempt=attempt,
                target_notional=active_notional,
                filled_notional=filled_notional,
                fill_price=fill_price,
                slippage_bps=slippage_bps,
                fee_paid=fee_paid,
                slippage_cost=slippage_cost,
            )
        )

        return ExecutionResult(
            status=status,
            requested_notional=float(intent.requested_notional),
            filled_notional=filled_notional,
            reference_price=float(intent.reference_price),
            fill_price=fill_price,
            slippage_bps=slippage_bps,
            fee_paid=fee_paid,
            slippage_cost=slippage_cost,
            total_execution_cost=total_execution_cost,
            reasons=tuple(dict.fromkeys(reasons)),
            metadata={
                "latency_ms": effective_latency_ms,
                "ttl_ms": ttl_ms,
                "fill_capacity_notional": round(fill_capacity_notional, 2),
                "depth_fill_ratio": self.depth_fill_ratio,
                "replace_count": attempt,
                "executed_target_notional": active_notional,
                "max_retry_attempts": self.max_retry_attempts,
                "retry_backoff_seconds": self.retry_backoff_seconds,
                "fee_rate_bps": self.fee_rate_bps,
                "lifecycle": lifecycle,
            },
        )

    @staticmethod
    def _extract_latency_ms(event: MarketEvent) -> int:
        raw = event.metadata.get(
            "execution_latency_ms",
            event.metadata.get("scenario_latency_ms", 0),
        )
        try:
            return max(0, int(raw))
        except (TypeError, ValueError):
            return 0

    @staticmethod
    def _estimate_slippage_bps(event: MarketEvent, requested_notional: float) -> int:
        min_depth = max(min(event.bids_depth_usd, event.asks_depth_usd), 1.0)
        liquidity = max(event.liquidity_usd, 1.0)
        slippage_multiplier = PaperExecutionAdapter._extract_slippage_multiplier(event)

        depth_impact_bps = (requested_notional / min_depth) * 40.0
        liquidity_impact_bps = (requested_notional / liquidity) * 20.0
        return max(
            0,
            int(round((depth_impact_bps + liquidity_impact_bps) * slippage_multiplier)),
        )

    @staticmethod
    def _extract_slippage_multiplier(event: MarketEvent) -> float:
        raw = event.metadata.get("execution_slippage_multiplier", 1.0)
        try:
            return max(0.0, float(raw))
        except (TypeError, ValueError):
            return 1.0
