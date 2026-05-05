"""Pool Supervisor Adapter -- wires Agent Pool into the supervisor cycle.

Wraps RuntimeSupervisor to add per-cycle agent pool telemetry:
- Activates registered agents before each cycle
- Records agent observations in MemoryStore after each cycle
- Combines agent outputs via PoolCoordinator
- Persists memory to disk after each cycle
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

from .agent_pool import AgentPool, AgentState
from .memory_store import MemoryStore
from .pool_coordinator import AgentOutput, CoordinatedDecision, PoolCoordinator
from .runtime_supervisor import RuntimeSupervisor, WorkerSpec


class PoolSupervisorAdapter:
    """Extends RuntimeSupervisor with Agent Pool telemetry."""

    def __init__(
        self,
        *,
        supervisor: RuntimeSupervisor,
        pool: AgentPool,
        memory: MemoryStore,
        memory_path: Path | None = None,
    ) -> None:
        self._supervisor = supervisor
        self._pool = pool
        self._coordinator = PoolCoordinator(pool)
        self._memory = memory
        self._memory_path = memory_path
        self._cycle_decisions: list[CoordinatedDecision] = []

    def run(
        self,
        worker_specs: Sequence[WorkerSpec],
        *,
        cycles: int = 1,
        stop_on_failure: bool = True,
    ) -> dict[str, Any]:
        """Run supervisor cycles with pool telemetry hooks."""
        if cycles <= 0:
            raise ValueError("cycles must be >= 1")

        # Activate all registered agents
        for descriptor in list(self._pool._agents.values()):
            state = self._pool.get_state(descriptor.agent_id)
            if state == AgentState.REGISTERED:
                self._pool.activate(descriptor.agent_id, reason="supervisor_start")
            elif state == AgentState.COOLDOWN:
                self._pool.ready(descriptor.agent_id, reason="supervisor_start")

        snapshots: list[dict[str, Any]] = []
        for cycle_index in range(1, cycles + 1):
            snapshot = self._supervisor.run_cycle(
                worker_specs, cycle_index=cycle_index
            )

            # Post-cycle pool telemetry
            self._record_cycle_telemetry(cycle_index, snapshot)

            snapshots.append(snapshot)
            if stop_on_failure and snapshot["status"] == "FAILED":
                break

        # Persist memory
        if self._memory_path:
            self._memory.save(self._memory_path)

        overall_status = (
            "SUCCESS"
            if snapshots and all(s["status"] == "SUCCESS" for s in snapshots)
            else "FAILED"
        )
        return {
            "cycles_completed": len(snapshots),
            "overall_status": overall_status,
            "pool_decisions": len(self._cycle_decisions),
            "memory_observations": self._memory.observation_count,
            "memory_cycles": self._memory.cycle_count,
        }

    def _record_cycle_telemetry(
        self, cycle_index: int, snapshot: dict[str, Any]
    ) -> None:
        """Record agent observations and coordinated decision for a cycle."""
        cycle_id = f"cycle_{cycle_index}"

        # Collect outputs from active alpha agents
        outputs: list[AgentOutput] = []
        for descriptor in self._pool.active_agents(pool_type="alpha"):
            # In advisory mode, agents produce ABSTAIN until wired to real backends
            outputs.append(
                AgentOutput(
                    agent_id=descriptor.agent_id,
                    pool_type=descriptor.pool_type,
                    priority=descriptor.priority,
                    action="ABSTAIN",
                    confidence=0.0,
                    metadata={"cycle_index": cycle_index, "mode": "shadow"},
                )
            )

        # Combine and record
        decision = self._coordinator.combine(outputs, pool_type="alpha")
        self._cycle_decisions.append(decision)

        # Write observations to memory
        for output in outputs:
            self._memory.write_observation(
                agent_id=output.agent_id,
                cycle_id=cycle_id,
                pool_type=output.pool_type,
                payload={
                    "action": output.action,
                    "confidence": output.confidence,
                    "decision_action": decision.action,
                    "decision_confidence": decision.weighted_confidence,
                    "cycle_status": snapshot.get("status", "UNKNOWN"),
                },
            )

        # Transition agents through cooldown cycle
        for descriptor in self._pool.active_agents(pool_type="alpha"):
            state = self._pool.get_state(descriptor.agent_id)
            if state == AgentState.ACTIVE:
                self._pool.complete_cycle(descriptor.agent_id, reason="cycle_end")
                self._pool.ready(descriptor.agent_id, reason="next_cycle")

    @property
    def decisions(self) -> list[CoordinatedDecision]:
        return list(self._cycle_decisions)

    @property
    def memory(self) -> MemoryStore:
        return self._memory
