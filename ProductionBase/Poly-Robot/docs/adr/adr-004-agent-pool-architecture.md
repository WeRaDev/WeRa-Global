# ADR-004: Agent Pool Architecture

**Status**: Draft
**Date**: 2026-05-05
**Context**: ADR-002 Phase 3 preparation

## Problem

The current AgentOperator is a single advisory/strategy agent backed by one LLM client (Claude API or OpenFang). As Poly-Robot evolves toward multi-agent orchestration, the system needs:

- A registry of heterogeneous agent types (alpha signal, risk advisory, execution timing, meta-learning)
- Defined lifecycle states for each agent (idle, active, cooldown, disabled)
- A structured memory interface so agents can read cycle history and write observations
- A coordination layer that weights and combines agent outputs

## Decision

Introduce an Agent Pool Architecture with four components:

### 1. Pool Registry
- Agents register with a typed descriptor: `agent_id`, `pool_type`, `capabilities`, `priority`
- Pool types: `alpha` (signal generation), `risk_advisory` (risk commentary), `execution_timing` (order timing), `meta` (self-improvement)
- Registry is configuration-driven (`config/agents/pool_registry.v1.json`)

### 2. Agent Lifecycle
States: `REGISTERED -> IDLE -> ACTIVE -> COOLDOWN -> IDLE` (or `DISABLED`)
- `REGISTERED`: agent descriptor accepted, not yet initialized
- `IDLE`: ready to receive cycle context
- `ACTIVE`: processing current cycle, producing output
- `COOLDOWN`: post-cycle recovery (rate limiting, reflection)
- `DISABLED`: manually or automatically disabled (policy violation, repeated failures)

Transitions are logged as append-only lifecycle events.

### 3. Memory Interface (Spirit-inspired)
From ADR-002 MemPalace mapping:
- **Palace**: runtime memory store (JSON-backed initially, upgradeable to database)
- **Wings**: one per pool type, containing agent-specific history
- **Rooms**: one per cycle, containing all agent outputs for that cycle
- **Drawers**: individual agent observations within a room

Interface contract:
- `write_observation(agent_id, cycle_id, observation)`: append to agent's wing
- `read_history(agent_id, window_cycles)`: retrieve recent observations
- `read_cycle(cycle_id)`: retrieve all agent outputs for a cycle
- `query(filter)`: search across wings with temporal and agent-type filters

### 4. Coordination Layer
- Replaces flat confidence with weighted combination of pool outputs
- Initial implementation: simple priority-weighted average (no Bayesian inference)
- Phase 4 (RxInfer) upgrades to factor-graph belief propagation

## Consequences

- Enables multi-agent experimentation without restructuring the decision loop
- Memory interface is the prerequisite for agent self-improvement (Phase 4)
- Pool registry makes agent management operational (add/remove/disable via config)
- Initial implementation is JSON file-backed; database upgrade is Phase 4+
- AgentOperator becomes one agent in the `alpha` pool

## Implementation plan
1. Define pool registry schema and create `config/agents/pool_registry.v1.json`
2. Implement `AgentPool` class with lifecycle state machine and event logging
3. Implement `MemoryStore` with Palace/Wing/Room/Drawer structure (JSON-backed)
4. Create `PoolCoordinator` that queries active agents, collects outputs, and produces weighted decisions
5. Migrate existing `AgentOperator` to register as an `alpha` pool agent
6. Add tests for lifecycle transitions, memory read/write, and coordination
