"""MemPalace-inspired memory store for agent observations (ADR-004).

JSON-backed storage with Palace/Wing/Room/Drawer hierarchy:
- Palace: the entire memory store
- Wings: one per pool type (alpha, risk_advisory, etc.)
- Rooms: one per cycle_id within a wing
- Drawers: individual agent observations within a room
"""
from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="milliseconds")


@dataclass(frozen=True)
class Observation:
    agent_id: str
    cycle_id: str
    pool_type: str
    timestamp: str
    payload: dict[str, Any] = field(default_factory=dict)


class MemoryStore:
    """JSON-backed structured memory for agent observations."""

    def __init__(self) -> None:
        # wing -> cycle_id -> list of observations
        self._wings: dict[str, dict[str, list[Observation]]] = defaultdict(
            lambda: defaultdict(list)
        )

    def write_observation(
        self,
        *,
        agent_id: str,
        cycle_id: str,
        pool_type: str,
        payload: dict[str, Any] | None = None,
    ) -> Observation:
        obs = Observation(
            agent_id=agent_id,
            cycle_id=cycle_id,
            pool_type=pool_type,
            timestamp=_utc_now_iso(),
            payload=payload or {},
        )
        self._wings[pool_type][cycle_id].append(obs)
        return obs

    def read_history(
        self, agent_id: str, *, window_cycles: int = 10
    ) -> list[Observation]:
        results: list[Observation] = []
        for wing in self._wings.values():
            for observations in wing.values():
                for obs in observations:
                    if obs.agent_id == agent_id:
                        results.append(obs)
        results.sort(key=lambda o: o.timestamp, reverse=True)
        seen_cycles: set[str] = set()
        filtered: list[Observation] = []
        for obs in results:
            seen_cycles.add(obs.cycle_id)
            if len(seen_cycles) > window_cycles:
                break
            filtered.append(obs)
        return list(reversed(filtered))

    def read_cycle(self, cycle_id: str) -> list[Observation]:
        results: list[Observation] = []
        for wing in self._wings.values():
            results.extend(wing.get(cycle_id, []))
        return sorted(results, key=lambda o: (o.pool_type, o.agent_id))

    def query(
        self,
        *,
        pool_type: str | None = None,
        agent_id: str | None = None,
        limit: int = 100,
    ) -> list[Observation]:
        results: list[Observation] = []
        wings = (
            {pool_type: self._wings[pool_type]}
            if pool_type and pool_type in self._wings
            else dict(self._wings)
        )
        for wing in wings.values():
            for observations in wing.values():
                for obs in observations:
                    if agent_id is not None and obs.agent_id != agent_id:
                        continue
                    results.append(obs)
        results.sort(key=lambda o: o.timestamp, reverse=True)
        return results[:limit]

    @property
    def cycle_count(self) -> int:
        cycles: set[str] = set()
        for wing in self._wings.values():
            cycles.update(wing.keys())
        return len(cycles)

    @property
    def observation_count(self) -> int:
        total = 0
        for wing in self._wings.values():
            for observations in wing.values():
                total += len(observations)
        return total

    def save(self, path: Path) -> None:
        serialized: dict[str, Any] = {}
        for pool_type, wing in self._wings.items():
            serialized[pool_type] = {
                cycle_id: [asdict(obs) for obs in observations]
                for cycle_id, observations in wing.items()
            }
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(serialized, indent=2) + "\n", encoding="utf-8")

    @staticmethod
    def load(path: Path) -> MemoryStore:
        store = MemoryStore()
        if not path.exists():
            return store
        raw = json.loads(path.read_text(encoding="utf-8"))
        for pool_type, wing_data in raw.items():
            for cycle_id, observations in wing_data.items():
                for obs_data in observations:
                    store._wings[pool_type][cycle_id].append(
                        Observation(
                            agent_id=obs_data["agent_id"],
                            cycle_id=obs_data["cycle_id"],
                            pool_type=obs_data["pool_type"],
                            timestamp=obs_data["timestamp"],
                            payload=obs_data.get("payload", {}),
                        )
                    )
        return store
