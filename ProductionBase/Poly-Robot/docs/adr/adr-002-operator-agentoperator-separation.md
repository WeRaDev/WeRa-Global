# ADR-002: Operator / AgentOperator Separation

**Status**: Accepted
**Date**: 2026-05-05
**Context**: Poly-Robot architecture upgrade plan

## Decision

Separate Poly-Robot into two distinct layers:

1. **Operator (Supervision Layer)** -- human-facing web+CLI dashboard with OpenBB-inspired TET data pipeline and gamified controls.
2. **AgentOperator (Orchestration Layer)** -- multi-agent runtime with MemPalace-inspired structured memory (Spirit), reactive Bayesian orchestration (RxInfer patterns), and FinRL-X weight-centric strategy composition.

## Motivation

The current monolithic runtime couples human supervision, agent orchestration, strategy, risk, execution, and data ingestion into a single supervisor cycle. This blocks:

- Independent evolution of the dashboard vs. agent runtime
- Pluggable data sources (multiple prediction markets)
- Multi-agent orchestration with memory and self-improvement
- Gamified operator experience

## Key External References Studied

- **OpenBB Platform** (github.com/OpenBB-finance/OpenBB): TET pipeline, provider extension model, REST API + Python + CLI
- **AgenticTrading** (github.com/Open-Finance-Lab/AgenticTrading): DAG planner, agent pools, memory agent, MCP/A2A protocols
- **FinRL-X** (github.com/AI4Finance-Foundation/FinRL-Trading): Weight-centric architecture, DRL agents, walk-forward evaluation
- **MemPalace** (github.com/MemPalace/mempalace): Palace/Wing/Room/Drawer structured memory, knowledge graph with validity windows, 96.6% R@5 recall
- **ReactiveBayes/RxInfer** (github.com/ReactiveBayes): Factor graph inference, reactive message passing, RxEnvironments for agents
- **SolarSeed-v3 Spirit**: Heartbeat-based meta-agent (observe-only), M0-M3 upgrade path from Python to Julia/RxInfer.jl

## Polymarket-trading Audit Finding

The `Polymarket-trading/` folder is NOT ready for paper/test/live modes. It contains standalone CLI utilities (market fetcher, on-chain approval, position redemption) with:

- Zero tests for wrapper scripts
- No mode lifecycle awareness (hardcoded mainnet chain_id=137)
- No integration with runtime supervisor or credential preflight
- Duplicate vendored py_clob_client code
- Mixed language comments and emoji in non-UI output

Integration plan: absorb CLOB client into the data provider layer during Phase 2.

## Spirit-as-Memory-Agent

The SolarSeed-v3 Spirit meta-agent maps to Poly-Robot's Memory Agent:

- **MemPalace metaphor**: Palace=runtime memory, Wings=agent pools, Rooms=cycle contexts, Drawers=individual decisions
- **Verbatim storage**: Raw cycle traces preserved, no summarization
- **Knowledge graph**: Temporal entity-relationship graph for strategy performance profiles
- **Agent diaries**: Each agent pool gets its own wing with diary
- **MCP tools**: Memory exposed to OpenFang agents via tool interface

## Reactive Bayesian Orchestration

From ReactiveBayes/RxInfer and SolarSeed Spirit upgrade path:

- **Factor graph model**: Cycle as probabilistic graphical model, agents as factor nodes
- **Belief propagation**: Bayesian weighting of alpha agent signals (replaces flat confidence)
- **Reactive streams**: Event-driven cycle updates instead of batch execution
- **RxInfer sidecar**: M2 milestone -- Python orchestrator feeds observations, Julia sidecar computes posteriors

## Phases

1. Structural separation + Polymarket-trading cleanup
2. Data Platform + Polymarket integration
3. Agent Pool Architecture + Spirit Memory
4. Bayesian Orchestration + Self-Improvement
5. Gamification, Multi-Market, Full Reactive Orchestration

## Phase 1 Module Boundary (Sprint W20)

### Shared interface layer (`src/poly_robot/shared/`)
Stable data contracts consumed by both Operator and Orchestrator layers:
- `contracts.py` -- MarketEvent, StrategyDecision, RiskDecision, PortfolioState, etc.
- `schemas.py` -- schema version constants
- `reproducibility.py` -- stable_hash and fingerprinting utilities

### Operator layer (supervision, human-facing)
Modules that serve the human operator via web GUI, CLI dashboards, and control surfaces:
- `runtime_web_gui.py` -- web dashboard and control API
- `runtime_supervisor.py` -- cycle supervision, heartbeat, journal, control state
- `mode_lifecycle.py` -- paper/test/live mode promotion decisions
- `canary_enablement.py` -- stage enablement approval workflow
- `canary_readiness.py` -- readiness certification evaluation
- `canary_rollback_guard.py` -- rollback trigger and incident handoff
- `stress_certification.py` -- stress campaign certification evaluator

### Orchestrator layer (strategy, risk, execution, agents)
Modules that implement the trading decision loop and agent coordination:
- `strategy_baseline.py` -- entry signal generation
- `risk_engine.py` -- sizing, exposure caps, cost-aware gating
- `paper_execution.py` -- paper execution adapter
- `exit_module.py` -- multi-trigger exit logic
- `test_token_loop.py` -- end-to-end loop orchestration
- `integration_adapters.py` -- ingestion and execution gateway adapters
- `agent_operator.py` -- AgentOperator advisory/strategy modes
- `agent_operator_learning.py` -- agent learning and improvement
- `probability_oracle.py` -- probability estimation
- `scenario_pack.py` -- scenario transform definitions
- `replay_harness.py` -- deterministic replay execution
- `scenario_matrix.py` -- multi-scenario replay runner

### Governance layer (cross-cutting)
- `parameter_governance.py` -- catalog/profile validation
- `llm_policy.py` -- LLM calibration policy enforcement

### Migration approach
1. Create `src/poly_robot/shared/__init__.py` that re-exports from `contracts`, `schemas`, `reproducibility`.
2. All existing imports (`from .contracts import ...`) continue to work unchanged.
3. New code prefers `from poly_robot.shared import ...`.
4. Full physical move of files into `operator/` and `orchestrator/` subdirectories deferred to Sprint W21 (Phase 1 completion) to keep the change set reviewable.

## Consequences

- Backward compatible: Phase 1 is pure refactoring, all CI gates pass
- `contracts.py` data models remain the stable interface contract
- OpenFang integration becomes one agent in the registry
- MemPalace patterns adopted conceptually (MIT), not as code dependency
- RxInfer sidecar is Phase 4+; Python approximations used earlier
