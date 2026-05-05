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

## Consequences

- Backward compatible: Phase 1 is pure refactoring, all CI gates pass
- `contracts.py` data models remain the stable interface contract
- OpenFang integration becomes one agent in the registry
- MemPalace patterns adopted conceptually (MIT), not as code dependency
- RxInfer sidecar is Phase 4+; Python approximations used earlier
