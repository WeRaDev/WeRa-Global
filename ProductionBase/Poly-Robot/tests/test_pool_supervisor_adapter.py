"""Tests for PoolSupervisorAdapter: pool telemetry wired into supervisor."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from poly_robot.agent_pool import AgentDescriptor, AgentPool
from poly_robot.memory_store import MemoryStore
from poly_robot.pool_supervisor_adapter import PoolSupervisorAdapter
from poly_robot.runtime_supervisor import RuntimeSupervisor, WorkerSpec


def _noop_sleep(seconds: float) -> None:
    pass


_CLOCK = 0.0


def _fake_monotonic() -> float:
    global _CLOCK
    _CLOCK += 0.01
    return _CLOCK


def _make_worker(name: str = "test_worker") -> WorkerSpec:
    def handler(emit):
        emit("cycle_completed", {"risk_allowed_count": 1, "filled_trade_count": 1})
        return {"status": "ok"}
    return WorkerSpec(name=name, run=handler, max_retries=0, heartbeat_timeout_seconds=60)


class TestPoolSupervisorAdapter(unittest.TestCase):
    def setUp(self) -> None:
        global _CLOCK
        _CLOCK = 0.0

    def _make_adapter(self) -> PoolSupervisorAdapter:
        tmp = Path(tempfile.mkdtemp())
        supervisor = RuntimeSupervisor(
            journal_path=tmp / "journal.jsonl",
            state_path=tmp / "state.json",
            sleep_fn=_noop_sleep,
            monotonic_fn=_fake_monotonic,
        )
        pool = AgentPool()
        pool.register(AgentDescriptor(
            agent_id="test-alpha", pool_type="alpha", priority=10
        ))
        memory = MemoryStore()
        return PoolSupervisorAdapter(
            supervisor=supervisor,
            pool=pool,
            memory=memory,
            memory_path=tmp / "memory.json",
        )

    def test_run_records_observations(self) -> None:
        adapter = self._make_adapter()
        result = adapter.run([_make_worker()], cycles=3)
        self.assertEqual(result["overall_status"], "SUCCESS")
        self.assertEqual(result["cycles_completed"], 3)
        self.assertEqual(result["pool_decisions"], 3)
        self.assertGreater(result["memory_observations"], 0)
        self.assertEqual(result["memory_cycles"], 3)

    def test_memory_persisted(self) -> None:
        adapter = self._make_adapter()
        adapter.run([_make_worker()], cycles=2)
        # Memory should have been saved
        self.assertGreater(adapter.memory.observation_count, 0)

    def test_decisions_are_hold_in_shadow_mode(self) -> None:
        adapter = self._make_adapter()
        adapter.run([_make_worker()], cycles=1)
        decisions = adapter.decisions
        self.assertEqual(len(decisions), 1)
        # Shadow mode agents ABSTAIN -> coordinator returns HOLD
        self.assertEqual(decisions[0].action, "HOLD")

    def test_single_cycle(self) -> None:
        adapter = self._make_adapter()
        result = adapter.run([_make_worker()], cycles=1)
        self.assertEqual(result["cycles_completed"], 1)
        self.assertEqual(result["memory_cycles"], 1)


if __name__ == "__main__":
    unittest.main()
