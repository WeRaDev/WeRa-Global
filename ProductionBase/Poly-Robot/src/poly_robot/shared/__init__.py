"""Stable shared interface layer for Poly-Robot.

Contains the canonical copies of data contracts, schema constants, and
reproducibility utilities consumed by both the Operator (supervision)
and Orchestrator (strategy/risk/execution) layers.

Existing ``from poly_robot.contracts import ...`` paths remain valid
via backward-compatible shims at the original locations.
"""

from .contracts import (  # noqa: F401
    MarketEvent,
    PortfolioState,
    ReplayRecord,
    ReplayRun,
    RiskDecision,
    RiskModule,
    StrategyDecision,
    StrategyModule,
)
from .reproducibility import (  # noqa: F401
    hash_events,
    stable_hash,
    stable_json_dumps,
)
from .schemas import (  # noqa: F401
    STRESS_CERTIFICATION_REPORT_SCHEMA_VERSION,
)
