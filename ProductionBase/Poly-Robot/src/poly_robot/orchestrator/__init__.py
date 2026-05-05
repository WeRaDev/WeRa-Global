"""Orchestrator (Agent Layer) for Poly-Robot.

Trading decision loop, strategy signal generation, risk sizing,
execution adapters, exit logic, and agent coordination.

Modules in this layer:
- strategy_baseline -- entry signal generation
- risk_engine -- sizing, exposure caps, cost-aware gating
- paper_execution -- paper execution adapter
- exit_module -- multi-trigger exit logic
- test_token_loop -- end-to-end loop orchestration
- integration_adapters -- ingestion and execution gateway adapters
- agent_operator -- AgentOperator advisory/strategy modes
- agent_operator_learning -- agent learning and improvement
- probability_oracle -- probability estimation
- scenario_pack -- scenario transform definitions
- replay_harness -- deterministic replay execution
- scenario_matrix -- multi-scenario replay runner
"""

from poly_robot.agent_operator import AgentOperator  # noqa: F401
from poly_robot.exit_module import ExitDecision, ExitModule, PositionSnapshot  # noqa: F401
from poly_robot.integration_adapters import (  # noqa: F401
    ExecutionGatewayAdapter,
    HardenedExecutionAdapter,
    HistoricalIngestionAdapter,
    LivePolymarketIngestionAdapter,
    PolymarketClobExecutionAdapter,
)
from poly_robot.paper_execution import PaperExecutionAdapter  # noqa: F401
from poly_robot.replay_harness import ReplayHarness  # noqa: F401
from poly_robot.risk_engine import RiskEngine  # noqa: F401
from poly_robot.strategy_baseline import BaselineStrategy  # noqa: F401

# ADR-002 Phase 2: Data provider abstraction
from poly_robot.data_provider import (  # noqa: F401
    DataProvider,
    ManifoldMarketsProvider,
    PolymarketHistoricalProvider,
    PolymarketLiveProvider,
)
