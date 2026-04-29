"""Poly-Robot source package."""

from .contracts import (  # noqa: F401
    MarketEvent,
    PortfolioState,
    ReplayRecord,
    ReplayRun,
    RiskDecision,
    StrategyDecision,
)
from .exit_module import ExitDecision, ExitModule, PositionSnapshot  # noqa: F401
from .integration_adapters import (  # noqa: F401
    ExecutionGatewayAdapter,
    HardenedExecutionAdapter,
    HistoricalIngestionAdapter,
    IngestionBatch,
    LivePolymarketIngestionAdapter,
    PolymarketClobExecutionAdapter,
)
from .schemas import (  # noqa: F401
    CANARY_APPROVAL_RECORD_SCHEMA_VERSION,
    CANARY_ROLLBACK_GUARD_AUDIT_EVENT_SCHEMA_VERSION,
    CANARY_ROLLBACK_GUARD_REPORT_SCHEMA_VERSION,
    CANARY_ROLLBACK_INCIDENT_REPORT_SCHEMA_VERSION,
    CANARY_ROLLOUT_CERTIFICATION_REPORT_SCHEMA_VERSION,
    CANARY_STAGE_ENABLEMENT_AUDIT_EVENT_SCHEMA_VERSION,
    CANARY_STAGE_ENABLEMENT_DECISION_SCHEMA_VERSION,
    EVENT_SCHEMA_VERSION,
    REPLAY_RESULT_SCHEMA_VERSION,
    RUNTIME_OPERATOR_ACTION_SCHEMA_VERSION,
    RUNTIME_OPERATOR_CONTROL_STATE_SCHEMA_VERSION,
    RUNTIME_SOAK_HEALTH_SNAPSHOT_SCHEMA_VERSION,
    RUNTIME_SUPERVISOR_DASHBOARD_SCHEMA_VERSION,
    RUNTIME_SUPERVISOR_JOURNAL_EVENT_SCHEMA_VERSION,
    RUNTIME_SUPERVISOR_STATE_SCHEMA_VERSION,
    SCENARIO_PACK_SCHEMA_VERSION,
    STRESS_CAMPAIGN_REPORT_SCHEMA_VERSION,
    STRESS_CERTIFICATION_REPORT_SCHEMA_VERSION,
    TEST_TOKEN_LOOP_RESULT_SCHEMA_VERSION,
)
from .runtime_supervisor import RuntimeSupervisor, WorkerSpec  # noqa: F401
from .runtime_web_gui import OperatorControlManager, RuntimeDashboardService  # noqa: F401
