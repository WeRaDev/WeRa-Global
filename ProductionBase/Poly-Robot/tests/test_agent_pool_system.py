"""Tests for ADR-004 Agent Pool Architecture: pool, memory, coordinator."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from poly_robot.agent_pool import AgentDescriptor, AgentPool, AgentState
from poly_robot.memory_store import MemoryStore
from poly_robot.pool_coordinator import AgentOutput, PoolCoordinator


ROOT_DIR = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT_DIR / "config" / "agents" / "pool_registry.v1.json"


class TestAgentPoolLifecycle(unittest.TestCase):
    def _make_pool(self) -> AgentPool:
        pool = AgentPool()
        pool.register(AgentDescriptor(
            agent_id="test-agent", pool_type="alpha", priority=10
        ))
        return pool

    def test_register_sets_registered_state(self) -> None:
        pool = self._make_pool()
        self.assertEqual(pool.get_state("test-agent"), AgentState.REGISTERED)

    def test_activate_transitions_to_active(self) -> None:
        pool = self._make_pool()
        pool.activate("test-agent")
        self.assertEqual(pool.get_state("test-agent"), AgentState.ACTIVE)

    def test_full_cycle(self) -> None:
        pool = self._make_pool()
        pool.activate("test-agent")
        pool.complete_cycle("test-agent")
        self.assertEqual(pool.get_state("test-agent"), AgentState.COOLDOWN)
        pool.ready("test-agent")
        self.assertEqual(pool.get_state("test-agent"), AgentState.IDLE)

    def test_disable_from_any_state(self) -> None:
        pool = self._make_pool()
        pool.activate("test-agent")
        pool.disable("test-agent", reason="policy_violation")
        self.assertEqual(pool.get_state("test-agent"), AgentState.DISABLED)

    def test_invalid_transition_raises(self) -> None:
        pool = self._make_pool()
        with self.assertRaises(ValueError):
            pool.complete_cycle("test-agent")  # REGISTERED -> COOLDOWN invalid

    def test_events_are_appended(self) -> None:
        pool = self._make_pool()
        pool.activate("test-agent")
        self.assertGreaterEqual(len(pool.events), 2)

    def test_active_agents_filters_by_pool_type(self) -> None:
        pool = self._make_pool()
        pool.register(AgentDescriptor(agent_id="other", pool_type="meta", priority=5))
        pool.activate("test-agent")
        pool.activate("other")
        alpha = pool.active_agents(pool_type="alpha")
        self.assertEqual(len(alpha), 1)
        self.assertEqual(alpha[0].agent_id, "test-agent")

    def test_from_registry(self) -> None:
        if not REGISTRY_PATH.exists():
            self.skipTest("Registry config not found")
        pool = AgentPool.from_registry(REGISTRY_PATH)
        self.assertGreater(len(pool.events), 0)


class TestMemoryStore(unittest.TestCase):
    def test_write_and_read_cycle(self) -> None:
        store = MemoryStore()
        store.write_observation(
            agent_id="a1", cycle_id="c1", pool_type="alpha",
            payload={"action": "BUY", "confidence": 0.8},
        )
        cycle = store.read_cycle("c1")
        self.assertEqual(len(cycle), 1)
        self.assertEqual(cycle[0].agent_id, "a1")

    def test_read_history_windowed(self) -> None:
        store = MemoryStore()
        for i in range(5):
            store.write_observation(
                agent_id="a1", cycle_id=f"c{i}", pool_type="alpha",
            )
        history = store.read_history("a1", window_cycles=3)
        cycles = {o.cycle_id for o in history}
        self.assertLessEqual(len(cycles), 3)

    def test_query_filters(self) -> None:
        store = MemoryStore()
        store.write_observation(agent_id="a1", cycle_id="c1", pool_type="alpha")
        store.write_observation(agent_id="a2", cycle_id="c1", pool_type="meta")
        alpha = store.query(pool_type="alpha")
        self.assertEqual(len(alpha), 1)

    def test_save_and_load(self) -> None:
        store = MemoryStore()
        store.write_observation(agent_id="a1", cycle_id="c1", pool_type="alpha")
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = Path(f.name)
        store.save(path)
        loaded = MemoryStore.load(path)
        self.assertEqual(loaded.observation_count, 1)
        path.unlink(missing_ok=True)

    def test_counts(self) -> None:
        store = MemoryStore()
        store.write_observation(agent_id="a1", cycle_id="c1", pool_type="alpha")
        store.write_observation(agent_id="a1", cycle_id="c2", pool_type="alpha")
        self.assertEqual(store.cycle_count, 2)
        self.assertEqual(store.observation_count, 2)


class TestPoolCoordinator(unittest.TestCase):
    def _make_pool_and_coordinator(self) -> tuple[AgentPool, PoolCoordinator]:
        pool = AgentPool()
        pool.register(AgentDescriptor(agent_id="a1", pool_type="alpha", priority=10))
        pool.register(AgentDescriptor(agent_id="a2", pool_type="alpha", priority=5))
        pool.activate("a1")
        pool.activate("a2")
        return pool, PoolCoordinator(pool)

    def test_combine_buy_majority(self) -> None:
        pool, coord = self._make_pool_and_coordinator()
        outputs = [
            AgentOutput(agent_id="a1", pool_type="alpha", priority=10, action="BUY", confidence=0.9),
            AgentOutput(agent_id="a2", pool_type="alpha", priority=5, action="HOLD", confidence=0.6),
        ]
        decision = coord.combine(outputs)
        self.assertEqual(decision.action, "BUY")
        self.assertEqual(decision.contributing_agents, 2)

    def test_combine_all_abstain(self) -> None:
        pool, coord = self._make_pool_and_coordinator()
        outputs = [
            AgentOutput(agent_id="a1", pool_type="alpha", priority=10, action="ABSTAIN", confidence=0.0),
        ]
        decision = coord.combine(outputs)
        self.assertEqual(decision.action, "HOLD")
        self.assertEqual(decision.abstained_agents, 1)

    def test_combine_empty(self) -> None:
        pool, coord = self._make_pool_and_coordinator()
        decision = coord.combine([])
        self.assertEqual(decision.action, "HOLD")
        self.assertEqual(decision.contributing_agents, 0)

    def test_weighted_confidence(self) -> None:
        pool, coord = self._make_pool_and_coordinator()
        outputs = [
            AgentOutput(agent_id="a1", pool_type="alpha", priority=10, action="BUY", confidence=0.9),
            AgentOutput(agent_id="a2", pool_type="alpha", priority=10, action="BUY", confidence=0.5),
        ]
        decision = coord.combine(outputs)
        self.assertAlmostEqual(decision.weighted_confidence, 0.7, places=2)


if __name__ == "__main__":
    unittest.main()
