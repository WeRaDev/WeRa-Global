"""Operator (Supervision Layer) for Poly-Robot.

Human-facing web GUI, CLI dashboards, control surfaces, runtime
supervision, and lifecycle gate evaluation.

Modules in this layer:
- runtime_web_gui -- web dashboard and control API
- runtime_supervisor -- cycle supervision, heartbeat, journal
- mode_lifecycle -- paper/test/live mode promotion
- canary_enablement -- stage enablement approval workflow
- canary_readiness -- readiness certification evaluation
- canary_rollback_guard -- rollback trigger and incident handoff
- stress_certification -- stress campaign certification evaluator
"""

from poly_robot.canary_enablement import (  # noqa: F401
    build_canary_stage_enablement_decision,
)
from poly_robot.canary_readiness import (  # noqa: F401
    build_canary_readiness_report,
)
from poly_robot.canary_rollback_guard import (  # noqa: F401
    build_canary_rollback_guard_report,
)
from poly_robot.runtime_supervisor import (  # noqa: F401
    RuntimeSupervisor,
    WorkerSpec,
)
from poly_robot.runtime_web_gui import (  # noqa: F401
    OperatorControlManager,
    RuntimeDashboardService,
)
from poly_robot.stress_certification import (  # noqa: F401
    build_stress_certification_report,
)
