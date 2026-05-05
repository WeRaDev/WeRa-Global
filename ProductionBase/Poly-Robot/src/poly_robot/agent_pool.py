"""Agent Pool with lifecycle state machine (ADR-004).

Manages a registry of heterogeneous agents with typed descriptors,
lifecycle state transitions, and append-only event logging.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import Any


class AgentState(str, Enum):
    REGISTERED = "REGISTERED"
    IDLE = "IDLE"
    ACTIVE = "ACTIVE"
    COOLDOWN = "COOLDOWN"
    DISABLED = "DISABLED"


VALID_TRANSITIONS: dict[AgentState, set[AgentState]] = {
    AgentState.REGISTERED: {AgentState.IDLE, AgentState.DISABLED},
    AgentState.IDLE: {AgentState.ACTIVE, AgentState.DISABLED},
    AgentState.ACTIVE: {AgentState.COOLDOWN, AgentState.IDLE, AgentState.DISABLED},
    AgentState.COOLDOWN: {AgentState.IDLE, AgentState.DISABLED},
    AgentState.DISABLED: {AgentState.REGISTERED},
}


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="milliseconds")


@dataclass
class AgentDescriptor:
    agent_id: str
    pool_type: str
    capabilities: list[str] = field(default_factory=list)
    priority: int = 0
    backend: str = ""
    enabled: bool = True
    description: str = ""

    @staticmethod
    def from_dict(payload: dict[str, Any]) -> AgentDescriptor:
        return AgentDescriptor(
            agent_id=str(payload.get("agent_id", "")).strip(),
            pool_type=str(payload.get("pool_type", "")).strip(),
            capabilities=[str(c) for c in payload.get("capabilities", [])],
            priority=int(payload.get("priority", 0)),
            backend=str(payload.get("backend", "")).strip(),
            enabled=bool(payload.get("enabled", True)),
            description=str(payload.get("description", "")).strip(),
        )


@dataclass
class LifecycleEvent:
    agent_id: str
    from_state: str
    to_state: str
    timestamp: str
    reason: str = ""


class AgentPool:
    """Manages agent registration, lifecycle, and state queries."""

    def __init__(self) -> None:
        self._agents: dict[str, AgentDescriptor] = {}
        self._states: dict[str, AgentState] = {}
        self._events: list[LifecycleEvent] = []

    def register(self, descriptor: AgentDescriptor) -> None:
        if not descriptor.agent_id:
            raise ValueError("agent_id must not be empty")
        self._agents[descriptor.agent_id] = descriptor
        self._transition(descriptor.agent_id, AgentState.REGISTERED, reason="registered")

    def activate(self, agent_id: str, *, reason: str = "") -> None:
        current = self._states.get(agent_id)
        if current == AgentState.REGISTERED:
            self._transition(agent_id, AgentState.IDLE, reason="auto_init")
        self._transition(agent_id, AgentState.ACTIVE, reason=reason or "activated")

    def complete_cycle(self, agent_id: str, *, reason: str = "") -> None:
        self._transition(agent_id, AgentState.COOLDOWN, reason=reason or "cycle_complete")

    def ready(self, agent_id: str, *, reason: str = "") -> None:
        self._transition(agent_id, AgentState.IDLE, reason=reason or "cooldown_complete")

    def disable(self, agent_id: str, *, reason: str = "") -> None:
        self._transition(agent_id, AgentState.DISABLED, reason=reason or "disabled")

    def get_state(self, agent_id: str) -> AgentState | None:
        return self._states.get(agent_id)

    def get_descriptor(self, agent_id: str) -> AgentDescriptor | None:
        return self._agents.get(agent_id)

    def active_agents(self, *, pool_type: str | None = None) -> list[AgentDescriptor]:
        result = []
        for agent_id, state in self._states.items():
            if state not in {AgentState.IDLE, AgentState.ACTIVE}:
                continue
            descriptor = self._agents.get(agent_id)
            if descriptor is None:
                continue
            if pool_type is not None and descriptor.pool_type != pool_type:
                continue
            result.append(descriptor)
        return sorted(result, key=lambda d: -d.priority)

    @property
    def events(self) -> list[LifecycleEvent]:
        return list(self._events)

    def _transition(self, agent_id: str, to_state: AgentState, *, reason: str) -> None:
        current = self._states.get(agent_id)
        if current is not None:
            allowed = VALID_TRANSITIONS.get(current, set())
            if to_state not in allowed:
                raise ValueError(
                    f"Invalid transition for {agent_id}: {current.value} -> {to_state.value}"
                )
        event = LifecycleEvent(
            agent_id=agent_id,
            from_state=current.value if current else "NONE",
            to_state=to_state.value,
            timestamp=_utc_now_iso(),
            reason=reason,
        )
        self._states[agent_id] = to_state
        self._events.append(event)

    @staticmethod
    def from_registry(path: Path) -> AgentPool:
        payload = json.loads(path.read_text(encoding="utf-8"))
        pool = AgentPool()
        for agent_payload in payload.get("agents", []):
            descriptor = AgentDescriptor.from_dict(agent_payload)
            if descriptor.enabled:
                pool.register(descriptor)
        return pool
