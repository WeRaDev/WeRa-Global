"""Pool Coordinator for multi-agent decision combination (ADR-004).

Queries active agents from the pool, collects their outputs, and
produces a priority-weighted combined decision.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from .agent_pool import AgentPool


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="milliseconds")


@dataclass(frozen=True)
class AgentOutput:
    agent_id: str
    pool_type: str
    priority: int
    action: str  # "BUY", "HOLD", "ABSTAIN"
    confidence: float
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CoordinatedDecision:
    action: str
    weighted_confidence: float
    contributing_agents: int
    abstained_agents: int
    outputs: list[AgentOutput]
    timestamp: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "action": self.action,
            "weighted_confidence": round(self.weighted_confidence, 6),
            "contributing_agents": self.contributing_agents,
            "abstained_agents": self.abstained_agents,
            "outputs": [
                {
                    "agent_id": o.agent_id,
                    "pool_type": o.pool_type,
                    "priority": o.priority,
                    "action": o.action,
                    "confidence": round(o.confidence, 6),
                }
                for o in self.outputs
            ],
            "timestamp": self.timestamp,
        }


class PoolCoordinator:
    """Combines outputs from multiple agents using priority-weighted voting."""

    def __init__(self, pool: AgentPool) -> None:
        self._pool = pool

    def combine(
        self,
        outputs: list[AgentOutput],
        *,
        pool_type: str = "alpha",
    ) -> CoordinatedDecision:
        active = {d.agent_id for d in self._pool.active_agents(pool_type=pool_type)}
        relevant = [o for o in outputs if o.agent_id in active and o.pool_type == pool_type]

        contributing = [o for o in relevant if o.action != "ABSTAIN"]
        abstained = [o for o in relevant if o.action == "ABSTAIN"]

        if not contributing:
            return CoordinatedDecision(
                action="HOLD",
                weighted_confidence=0.0,
                contributing_agents=0,
                abstained_agents=len(abstained),
                outputs=relevant,
                timestamp=_utc_now_iso(),
            )

        total_priority = sum(o.priority for o in contributing) or 1
        weighted_confidence = sum(
            o.confidence * (o.priority / total_priority) for o in contributing
        )

        buy_weight = sum(
            o.priority for o in contributing if o.action == "BUY"
        )
        hold_weight = sum(
            o.priority for o in contributing if o.action == "HOLD"
        )
        action = "BUY" if buy_weight > hold_weight else "HOLD"

        return CoordinatedDecision(
            action=action,
            weighted_confidence=weighted_confidence,
            contributing_agents=len(contributing),
            abstained_agents=len(abstained),
            outputs=relevant,
            timestamp=_utc_now_iso(),
        )
