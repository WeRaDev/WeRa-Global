"""Stable shared interface layer for Poly-Robot.

Re-exports data contracts, schema constants, and reproducibility utilities
that are consumed by both the Operator (supervision) and Orchestrator
(strategy/risk/execution) layers.

Existing ``from poly_robot.contracts import ...`` paths remain valid.
New code should prefer ``from poly_robot.shared import ...``.
"""

from poly_robot.contracts import (  # noqa: F401
    MarketEvent,
    PortfolioState,
    RiskDecision,
    RiskModule,
    StrategyDecision,
    StrategyModule,
)
from poly_robot.reproducibility import stable_hash  # noqa: F401
from poly_robot.schemas import (  # noqa: F401
    STRESS_CERTIFICATION_REPORT_SCHEMA_VERSION,
)
