from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from .contracts import MarketEvent
from .schemas import SCENARIO_PACK_SCHEMA_VERSION


@dataclass(frozen=True)
class ReplayScenario:
    name: str
    latency_ms: int = 0
    depth_multiplier: float = 1.0
    liquidity_multiplier: float = 1.0
    probability_shift: float = 0.0
    midpoint_shift: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "latency_ms": self.latency_ms,
            "depth_multiplier": self.depth_multiplier,
            "liquidity_multiplier": self.liquidity_multiplier,
            "probability_shift": self.probability_shift,
            "midpoint_shift": self.midpoint_shift,
        }


@dataclass(frozen=True)
class ScenarioPack:
    schema_version: str
    default_scenario: str
    scenarios: dict[str, ReplayScenario]

    def get_scenario(self, name: str | None = None) -> ReplayScenario:
        scenario_name = name or self.default_scenario
        scenario = self.scenarios.get(scenario_name)
        if scenario is None:
            available = sorted(self.scenarios.keys())
            raise ValueError(
                f"Unknown scenario {scenario_name!r}. Available scenarios: {available}"
            )
        return scenario


def _clamp_probability(value: float) -> float:
    return min(max(value, 0.001), 0.999)


def _shift_timestamp(timestamp: str, latency_ms: int) -> str:
    if latency_ms == 0:
        return timestamp
    parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    shifted = parsed + timedelta(milliseconds=latency_ms)
    return shifted.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _parse_scenario(name: str, payload: dict[str, Any]) -> ReplayScenario:
    return ReplayScenario(
        name=name,
        latency_ms=int(payload.get("latency_ms", 0)),
        depth_multiplier=float(payload.get("depth_multiplier", 1.0)),
        liquidity_multiplier=float(payload.get("liquidity_multiplier", 1.0)),
        probability_shift=float(payload.get("probability_shift", 0.0)),
        midpoint_shift=float(payload.get("midpoint_shift", 0.0)),
    )


def load_scenario_pack(path: Path) -> ScenarioPack:
    payload = json.loads(path.read_text(encoding="utf-8"))
    schema_version = str(payload.get("schema_version", ""))
    if schema_version != SCENARIO_PACK_SCHEMA_VERSION:
        raise ValueError(
            f"Unsupported scenario pack schema version {schema_version!r}; "
            f"expected {SCENARIO_PACK_SCHEMA_VERSION!r}."
        )

    scenarios_payload = payload.get("scenarios")
    if not isinstance(scenarios_payload, dict) or not scenarios_payload:
        raise ValueError("Scenario pack must define a non-empty scenarios object.")

    scenarios: dict[str, ReplayScenario] = {}
    for name, scenario_payload in scenarios_payload.items():
        if not isinstance(scenario_payload, dict):
            raise ValueError(f"Scenario {name!r} must be an object.")
        scenarios[name] = _parse_scenario(name, scenario_payload)

    default_scenario = str(payload.get("default_scenario", "baseline"))
    if default_scenario not in scenarios:
        raise ValueError(
            f"default_scenario {default_scenario!r} is not defined in scenarios."
        )

    return ScenarioPack(
        schema_version=schema_version,
        default_scenario=default_scenario,
        scenarios=scenarios,
    )


def apply_scenario_to_events(
    events: list[MarketEvent], scenario: ReplayScenario
) -> list[MarketEvent]:
    transformed: list[MarketEvent] = []

    for event in events:
        payload = event.to_dict()
        payload["timestamp"] = _shift_timestamp(event.timestamp, scenario.latency_ms)
        payload["bids_depth_usd"] = max(
            0.0, event.bids_depth_usd * scenario.depth_multiplier
        )
        payload["asks_depth_usd"] = max(
            0.0, event.asks_depth_usd * scenario.depth_multiplier
        )
        payload["liquidity_usd"] = max(
            0.0, event.liquidity_usd * scenario.liquidity_multiplier
        )
        payload["estimated_probability"] = _clamp_probability(
            event.estimated_probability + scenario.probability_shift
        )
        payload["midpoint"] = _clamp_probability(
            event.midpoint + scenario.midpoint_shift
        )
        payload["metadata"] = {
            **event.metadata,
            "scenario_name": scenario.name,
            "scenario_latency_ms": scenario.latency_ms,
            "scenario_depth_multiplier": scenario.depth_multiplier,
            "scenario_liquidity_multiplier": scenario.liquidity_multiplier,
            "scenario_probability_shift": scenario.probability_shift,
            "scenario_midpoint_shift": scenario.midpoint_shift,
        }
        transformed.append(MarketEvent.from_dict(payload))

    return transformed
