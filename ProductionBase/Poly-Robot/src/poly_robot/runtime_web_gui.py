from __future__ import annotations
from contextlib import contextmanager

from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Iterator
import fcntl
import json
import os
import tempfile
import threading
from .agent_operator_learning import AgentOperatorLearningStore

from .mode_lifecycle import (
    build_mode_transition_decision,
    normalize_mode,
    resolve_mode_lifecycle_policy,
)
from .schemas import (
    RUNTIME_OPERATOR_ACTION_SCHEMA_VERSION,
    RUNTIME_OPERATOR_CONTROL_STATE_SCHEMA_VERSION,
    RUNTIME_SUPERVISOR_DASHBOARD_SCHEMA_VERSION,
    RUNTIME_SUPERVISOR_JOURNAL_EVENT_SCHEMA_VERSION,
    RUNTIME_SUPERVISOR_STATE_SCHEMA_VERSION,
)
KPI_SHADOW_POLICY_SCHEMA_VERSION = "kpi_shadow_policy.v1"
MAX_DASHBOARD_RECENT_EVENTS_LIMIT = 5000
MAX_DASHBOARD_RECENT_AUDIT_LIMIT = 2000
MAX_DASHBOARD_INCIDENT_LIMIT = 2000
MAX_DASHBOARD_COMPARISON_WINDOW = 1000
MAX_DASHBOARD_KPI_WINDOW = 1000


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="milliseconds")


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    temp_file_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            delete=False,
            prefix=f".{path.name}.",
            suffix=".tmp",
        ) as handle:
            handle.write(serialized)
            temp_file_path = Path(handle.name)
        if temp_file_path is None:
            raise RuntimeError("Failed to create temporary control-state file.")
        os.replace(temp_file_path, path)
    finally:
        if temp_file_path is not None and temp_file_path.exists():
            temp_file_path.unlink()


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []

    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def _append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True))
        handle.write("\n")


def _default_control_state() -> dict[str, Any]:
    now = _utc_now_iso()
    return {
        "schema_version": RUNTIME_OPERATOR_CONTROL_STATE_SCHEMA_VERSION,
        "updated_at": now,
        "control_version": 0,
        "paused": False,
        "restart_requested": False,
        "kill_switch_active": False,
        "cancel_all_requested": False,
        "selected_scenario": "baseline",
        "agent_operator_enabled": False,
        "agent_operators_running": False,
        "agent_operator_mode": "advisory",
        "agent_operator_strategy_auto_apply": True,
        "agent_operator_active_candidate_id": "",
        "agent_operator_active_candidate_scenario": "",
        "agent_operator_candidate_previous_scenario": "",
        "agent_operator_candidate_last_action": "",
        "agent_operator_candidate_last_action_at": "",
        "mode_current": "paper",
        "mode_target": "paper",
        "mode_transition_approval_status": "pending",
        "mode_transition_evidence": {},
        "mode_transition_last_decision": {},
        "mode_transition_last_decision_at": "",
        "mode_transition_last_transition_at": "",
        "mode_transition_last_actor": "",
        "mode_transition_last_reason": "",
        "mode_transition_last_action": "",
        "last_annotation": "",
    }


def _default_kpi_shadow_policy() -> dict[str, Any]:
    return {
        "schema_version": KPI_SHADOW_POLICY_SCHEMA_VERSION,
        "updated_at": "2026-04-27T00:00:00Z",
        "mode": "shadow",
        "default_window": 10,
        "minimum_sample_size": 2,
        "kpis": [
            {
                "kpi_id": "fill_rate",
                "label": "Fill Rate",
                "domain": "execution_quality",
                "source": "financial_metrics.fill_rate",
                "cycle_field": "fill_rate",
                "unit": "ratio",
                "direction": "higher_is_better",
                "warning_below": 0.35,
                "critical_below": 0.20,
            },
            {
                "kpi_id": "partial_fill_rate",
                "label": "Partial Fill Rate",
                "domain": "execution_quality",
                "source": "kpi_derived.partial_fill_rate",
                "cycle_field": "partial_fill_rate",
                "unit": "ratio",
                "direction": "lower_is_better",
                "warning_above": 0.50,
                "critical_above": 0.75,
            },
            {
                "kpi_id": "average_execution_cost_per_fill",
                "label": "Average Execution Cost Per Fill",
                "domain": "execution_quality",
                "source": "financial_metrics.average_execution_cost_per_fill",
                "cycle_field": "average_execution_cost_per_fill",
                "unit": "usd",
                "direction": "lower_is_better",
                "warning_above": 0.75,
                "critical_above": 1.25,
            },
            {
                "kpi_id": "expected_edge_capture_ratio",
                "label": "Expected Edge Capture Ratio",
                "domain": "execution_quality",
                "source": "financial_metrics.expected_edge_capture_ratio",
                "cycle_field": "expected_edge_capture_ratio",
                "unit": "ratio",
                "direction": "higher_is_better",
                "warning_below": 0.65,
                "critical_below": 0.50,
            },
            {
                "kpi_id": "execution_cost_to_expected_net_ratio",
                "label": "Execution Cost to Expected Net Ratio",
                "domain": "execution_quality",
                "source": "financial_metrics.execution_cost_to_expected_net_ratio",
                "cycle_field": "execution_cost_to_expected_net_ratio",
                "unit": "ratio",
                "direction": "lower_is_better",
                "warning_above": 0.80,
                "critical_above": 1.00,
            },
            {
                "kpi_id": "expected_value_after_execution_cost",
                "label": "Expected Value After Execution Cost",
                "domain": "forecast_quality",
                "source": "financial_metrics.expected_value_after_execution_cost",
                "cycle_field": "expected_value_after_execution_cost",
                "unit": "usd",
                "direction": "higher_is_better",
                "warning_below": 0.00,
                "critical_below": -0.05,
            },
            {
                "kpi_id": "calibration_applied_ratio",
                "label": "Calibration Applied Ratio",
                "domain": "calibration_reliability",
                "source": "loop_metrics.calibration_applied_ratio",
                "cycle_field": "calibration_applied_ratio",
                "unit": "ratio",
                "direction": "higher_is_better",
                "warning_below": 0.60,
                "critical_below": 0.40,
            },
            {
                "kpi_id": "weighted_check_agreement_mean",
                "label": "Weighted Check Agreement Mean",
                "domain": "calibration_reliability",
                "source": "loop_metrics.weighted_check_agreement_mean",
                "cycle_field": "weighted_check_agreement_mean",
                "unit": "ratio",
                "direction": "higher_is_better",
                "warning_below": 0.55,
                "critical_below": 0.45,
            },
            {
                "kpi_id": "probability_drift_abs_mean",
                "label": "Probability Drift Absolute Mean",
                "domain": "calibration_reliability",
                "source": "loop_metrics.probability_drift_abs_mean",
                "cycle_field": "probability_drift_abs_mean",
                "unit": "ratio",
                "direction": "lower_is_better",
                "warning_above": 0.08,
                "critical_above": 0.12,
            },
            {
                "kpi_id": "probability_drift_max_abs",
                "label": "Probability Drift Max Absolute",
                "domain": "calibration_reliability",
                "source": "loop_metrics.probability_drift_max_abs",
                "cycle_field": "probability_drift_max_abs",
                "unit": "ratio",
                "direction": "lower_is_better",
                "warning_above": 0.18,
                "critical_above": 0.25,
            },
            {
                "kpi_id": "net_pnl",
                "label": "Net PnL",
                "domain": "risk_and_capital",
                "source": "financial_metrics.net_pnl",
                "cycle_field": "net_pnl",
                "unit": "usd",
                "direction": "higher_is_better",
                "warning_below": -0.25,
                "critical_below": -0.75,
            },
            {
                "kpi_id": "daily_drawdown_fraction",
                "label": "Daily Drawdown Fraction",
                "domain": "risk_and_capital",
                "source": "financial_metrics.daily_drawdown_fraction",
                "cycle_field": "daily_drawdown_fraction",
                "unit": "ratio",
                "direction": "lower_is_better",
                "warning_above": 0.04,
                "critical_above": 0.08,
            },
            {
                "kpi_id": "total_exposure_fraction",
                "label": "Total Exposure Fraction",
                "domain": "risk_and_capital",
                "source": "financial_metrics.total_exposure_fraction",
                "cycle_field": "total_exposure_fraction",
                "unit": "ratio",
                "direction": "lower_is_better",
                "warning_above": 0.50,
                "critical_above": 0.65,
            },
            {
                "kpi_id": "test_token_loop_retry_count",
                "label": "Test Token Loop Retry Count",
                "domain": "operational_reliability",
                "source": "kpi_derived.test_token_loop_retry_count",
                "unit": "count",
                "direction": "lower_is_better",
                "warning_above": 1.0,
                "critical_above": 3.0,
            },
            {
                "kpi_id": "incident_density_per_cycle",
                "label": "Incident Density Per Cycle",
                "domain": "operational_reliability",
                "source": "kpi_derived.incident_density_per_cycle",
                "unit": "incidents_per_cycle",
                "direction": "lower_is_better",
                "warning_above": 0.40,
                "critical_above": 0.80,
            },
        ],
    }


class OperatorControlManager:
    def __init__(
        self,
        *,
        control_state_path: Path,
        audit_path: Path,
        mode_lifecycle_policy_path: Path | None = None,
        agent_operator_learning_state_path: Path | None = None,
        agent_operator_learning_audit_path: Path | None = None,
    ) -> None:
        self.control_state_path = control_state_path
        self.audit_path = audit_path
        self.mode_lifecycle_policy_path = mode_lifecycle_policy_path
        self.lock_path = self.control_state_path.with_name(
            f"{self.control_state_path.name}.lock"
        )
        self._mutation_lock = threading.RLock()
        resolved_learning_state_path = (
            agent_operator_learning_state_path
            if agent_operator_learning_state_path is not None
            else self.control_state_path.with_name("agent_operator_learning_state.json")
        )
        resolved_learning_audit_path = (
            agent_operator_learning_audit_path
            if agent_operator_learning_audit_path is not None
            else self.control_state_path.with_name("agent_operator_learning_audit.jsonl")
        )
        self.agent_operator_learning_store = AgentOperatorLearningStore(
            state_path=resolved_learning_state_path,
            event_log_path=resolved_learning_audit_path,
        )

    @contextmanager
    def _interprocess_lock(self) -> Iterator[None]:
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        with self.lock_path.open("a+", encoding="utf-8") as lock_handle:
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)

    def _load_control_state_unlocked(self) -> dict[str, Any]:
        if not self.control_state_path.exists():
            return _default_control_state()
        payload = _read_json(self.control_state_path)
        if payload.get("schema_version") != RUNTIME_OPERATOR_CONTROL_STATE_SCHEMA_VERSION:
            raise ValueError("Operator control state schema version mismatch")
        baseline = _default_control_state()
        baseline.update(payload)
        return baseline

    def load_control_state(self) -> dict[str, Any]:
        with self._mutation_lock:
            with self._interprocess_lock():
                return self._load_control_state_unlocked()

    def _load_mode_lifecycle_policy(self) -> dict[str, Any]:
        if self.mode_lifecycle_policy_path is None:
            return resolve_mode_lifecycle_policy(None)
        if not self.mode_lifecycle_policy_path.exists():
            return resolve_mode_lifecycle_policy(None)
        payload = _read_json(self.mode_lifecycle_policy_path)
        if not isinstance(payload, dict):
            return resolve_mode_lifecycle_policy(None)
        return resolve_mode_lifecycle_policy(payload)

    def _mutate_state(
        self,
        *,
        action: str,
        actor: str,
        details: dict[str, Any],
        mutate_state: Callable[[dict[str, Any]], None],
    ) -> dict[str, Any]:
        with self._mutation_lock:
            with self._interprocess_lock():
                state = self._load_control_state_unlocked()
                mutate_state(state)
                next_version = int(state.get("control_version", 0)) + 1
                updated_at = _utc_now_iso()
                state["control_version"] = next_version
                state["updated_at"] = updated_at
                state["schema_version"] = RUNTIME_OPERATOR_CONTROL_STATE_SCHEMA_VERSION
                _write_json(self.control_state_path, state)
                _append_jsonl(
                    self.audit_path,
                    {
                        "schema_version": RUNTIME_OPERATOR_ACTION_SCHEMA_VERSION,
                        "timestamp": updated_at,
                        "action_sequence": next_version,
                        "action": action,
                        "actor": actor,
                        "details": details,
                        "control_state_version": state["control_version"],
                    },
                )
                return state

    def set_paused(
        self, *, paused: bool, actor: str, reason: str = ""
    ) -> dict[str, Any]:
        def _apply(state: dict[str, Any]) -> None:
            state["paused"] = paused
            if reason:
                state["pause_reason"] = reason

        return self._mutate_state(
            action="pause" if paused else "resume",
            actor=actor,
            details={"paused": paused, "reason": reason},
            mutate_state=_apply,
        )

    def request_restart(self, *, actor: str, reason: str = "") -> dict[str, Any]:
        def _apply(state: dict[str, Any]) -> None:
            state["restart_requested"] = True
            if reason:
                state["restart_reason"] = reason

        return self._mutate_state(
            action="graceful_restart_requested",
            actor=actor,
            details={"reason": reason},
            mutate_state=_apply,
        )

    def set_kill_switch(
        self, *, active: bool, actor: str, reason: str = ""
    ) -> dict[str, Any]:
        def _apply(state: dict[str, Any]) -> None:
            state["kill_switch_active"] = active
            if active:
                state["cancel_all_requested"] = True
            if reason:
                state["kill_switch_reason"] = reason

        return self._mutate_state(
            action="kill_switch_enabled" if active else "kill_switch_disabled",
            actor=actor,
            details={"kill_switch_active": active, "reason": reason},
            mutate_state=_apply,
        )

    def request_cancel_all(self, *, actor: str, reason: str = "") -> dict[str, Any]:
        def _apply(state: dict[str, Any]) -> None:
            state["cancel_all_requested"] = True
            if reason:
                state["cancel_all_reason"] = reason

        return self._mutate_state(
            action="cancel_all_requested",
            actor=actor,
            details={"reason": reason},
            mutate_state=_apply,
        )

    def acknowledge_cancel_all(self, *, actor: str, note: str = "") -> dict[str, Any]:
        def _apply(state: dict[str, Any]) -> None:
            state["cancel_all_requested"] = False
            if note:
                state["cancel_all_ack_note"] = note

        return self._mutate_state(
            action="cancel_all_acknowledged",
            actor=actor,
            details={"note": note},
            mutate_state=_apply,
        )

    def acknowledge_restart(self, *, actor: str, note: str = "") -> dict[str, Any]:
        def _apply(state: dict[str, Any]) -> None:
            state["restart_requested"] = False
            if note:
                state["restart_ack_note"] = note

        return self._mutate_state(
            action="graceful_restart_acknowledged",
            actor=actor,
            details={"note": note},
            mutate_state=_apply,
        )

    def set_scenario(self, *, actor: str, scenario_name: str) -> dict[str, Any]:
        if not scenario_name.strip():
            raise ValueError("scenario_name must not be empty")
        cleaned_scenario_name = scenario_name.strip()

        def _apply(state: dict[str, Any]) -> None:
            state["selected_scenario"] = cleaned_scenario_name

        return self._mutate_state(
            action="scenario_selected",
            actor=actor,
            details={"selected_scenario": cleaned_scenario_name},
            mutate_state=_apply,
        )

    def set_agent_operator_config(
        self,
        *,
        actor: str,
        enabled: bool | None = None,
        mode: str | None = None,
        strategy_auto_apply: bool | None = None,
        reason: str = "",
    ) -> dict[str, Any]:
        if enabled is None and mode is None and strategy_auto_apply is None:
            raise ValueError("enabled, mode, or strategy_auto_apply must be provided")
        normalized_mode: str | None = None
        if mode is not None:
            normalized_mode = str(mode).strip().lower()
            if normalized_mode not in {"advisory", "strategy"}:
                raise ValueError("mode must be advisory or strategy")
        normalized_reason = reason.strip()

        def _apply(state: dict[str, Any]) -> None:
            if enabled is not None:
                state["agent_operator_enabled"] = bool(enabled)
                state["agent_operators_running"] = bool(enabled)
            if normalized_mode is not None:
                state["agent_operator_mode"] = normalized_mode
            if strategy_auto_apply is not None:
                state["agent_operator_strategy_auto_apply"] = bool(
                    strategy_auto_apply
                )
            if normalized_reason:
                state["agent_operator_reason"] = normalized_reason

        details: dict[str, Any] = {}
        if enabled is not None:
            details["agent_operator_enabled"] = bool(enabled)
        if normalized_mode is not None:
            details["agent_operator_mode"] = normalized_mode
        if strategy_auto_apply is not None:
            details["agent_operator_strategy_auto_apply"] = bool(strategy_auto_apply)
        if normalized_reason:
            details["reason"] = normalized_reason

        return self._mutate_state(
            action="agent_operator_config_updated",
            actor=actor,
            details=details,
            mutate_state=_apply,
        )

    def start_agent_operators(self, *, actor: str, reason: str = "") -> dict[str, Any]:
        normalized_reason = reason.strip()
        def _apply(state: dict[str, Any]) -> None:
            state["agent_operator_enabled"] = True
            state["agent_operators_running"] = True
            if normalized_reason:
                state["agent_operator_reason"] = normalized_reason
        details: dict[str, Any] = {
            "agent_operator_enabled": True,
            "agent_operators_running": True,
        }
        if normalized_reason:
            details["reason"] = normalized_reason
        return self._mutate_state(
            action="agent_operators_started",
            actor=actor,
            details=details,
            mutate_state=_apply,
        )

    def stop_agent_operators(self, *, actor: str, reason: str = "") -> dict[str, Any]:
        normalized_reason = reason.strip()
        def _apply(state: dict[str, Any]) -> None:
            state["agent_operator_enabled"] = False
            state["agent_operators_running"] = False
            if normalized_reason:
                state["agent_operator_reason"] = normalized_reason
        details: dict[str, Any] = {
            "agent_operator_enabled": False,
            "agent_operators_running": False,
        }
        if normalized_reason:
            details["reason"] = normalized_reason
        return self._mutate_state(
            action="agent_operators_stopped",
            actor=actor,
            details=details,
            mutate_state=_apply,
        )

    def set_mode_transition(
        self,
        *,
        actor: str,
        target_mode: str,
        reason: str = "",
        approval_status: str | None = None,
        evidence: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        normalized_target_mode = normalize_mode(target_mode)
        normalized_reason = reason.strip()
        normalized_approval_status: str | None = None
        if approval_status is not None:
            normalized_approval_status = str(approval_status).strip().lower() or None
            if normalized_approval_status not in {"pending", "approved", "rejected"}:
                raise ValueError("approval_status must be pending, approved, or rejected")
        if evidence is not None and not isinstance(evidence, dict):
            raise ValueError("evidence must be an object")
        evidence_updates = dict(evidence or {})
        lifecycle_policy = self._load_mode_lifecycle_policy()

        def _apply(state: dict[str, Any]) -> None:
            current_mode = normalize_mode(state.get("mode_current"))
            existing_evidence = state.get("mode_transition_evidence")
            merged_evidence = (
                dict(existing_evidence) if isinstance(existing_evidence, dict) else {}
            )
            merged_evidence.update(evidence_updates)
            effective_approval_status = normalized_approval_status
            if effective_approval_status is None:
                effective_approval_status = str(
                    state.get("mode_transition_approval_status", "pending")
                ).strip().lower() or "pending"
            state["mode_target"] = normalized_target_mode
            state["mode_transition_evidence"] = merged_evidence
            state["mode_transition_approval_status"] = effective_approval_status
            decision = build_mode_transition_decision(
                current_mode=current_mode,
                target_mode=normalized_target_mode,
                policy=lifecycle_policy,
                evidence=merged_evidence,
                manual_approval_status=effective_approval_status,
                actor=actor,
                reason=normalized_reason or None,
            )
            decision_timestamp = str(decision.get("generated_at", "")).strip()
            state["mode_transition_last_decision"] = decision
            state["mode_transition_last_decision_at"] = decision_timestamp
            state["mode_transition_last_actor"] = actor
            state["mode_transition_last_action"] = (
                "applied" if decision.get("allowed") else "blocked"
            )
            if normalized_reason:
                state["mode_transition_last_reason"] = normalized_reason
            if decision.get("allowed"):
                state["mode_current"] = normalized_target_mode
                state["mode_target"] = normalized_target_mode
                state["mode_transition_last_transition_at"] = decision_timestamp

        return self._mutate_state(
            action="mode_transition_requested",
            actor=actor,
            details={
                "target_mode": normalized_target_mode,
                "reason": normalized_reason,
                "approval_status": normalized_approval_status,
                "evidence_keys": sorted(str(key) for key in evidence_updates.keys()),
            },
            mutate_state=_apply,
        )

    def record_agent_operator_recommendation(
        self,
        *,
        cycle_index: int,
        scenario_name: str,
        mode: str,
        recommendation: dict[str, Any],
        baseline_net_pnl: float | None,
        baseline_expected_value_after_execution_cost: float | None,
    ) -> dict[str, Any]:
        return self.agent_operator_learning_store.record_recommendation(
            cycle_index=cycle_index,
            scenario_name=scenario_name,
            mode=mode,
            recommendation=recommendation,
            baseline_net_pnl=baseline_net_pnl,
            baseline_expected_value_after_execution_cost=(
                baseline_expected_value_after_execution_cost
            ),
        )

    def attribute_agent_operator_outcomes(
        self,
        *,
        current_cycle_index: int,
        current_net_pnl: float | None,
        current_expected_value_after_execution_cost: float | None,
    ) -> dict[str, Any]:
        return self.agent_operator_learning_store.attribute_outcomes(
            current_cycle_index=current_cycle_index,
            current_net_pnl=current_net_pnl,
            current_expected_value_after_execution_cost=(
                current_expected_value_after_execution_cost
            ),
        )

    def get_agent_operator_learning_payload(
        self,
        *,
        candidate_limit: int = 20,
        recommendation_limit: int = 20,
    ) -> dict[str, Any]:
        return self.agent_operator_learning_store.build_dashboard_payload(
            candidate_limit=candidate_limit,
            recommendation_limit=recommendation_limit,
        )

    def apply_agent_operator_candidate(
        self,
        *,
        actor: str,
        candidate_id: str,
        reason: str = "",
    ) -> dict[str, Any]:
        candidate = self.agent_operator_learning_store.apply_candidate(
            candidate_id=candidate_id,
            actor=actor,
            reason=reason,
        )
        candidate_id_value = str(candidate.get("candidate_id", "")).strip()
        scenario_name = str(candidate.get("scenario_name", "")).strip()
        if not scenario_name:
            raise ValueError("candidate scenario_name is empty")
        candidate_action_at = _utc_now_iso()

        def _apply(state: dict[str, Any]) -> None:
            previous_scenario = str(state.get("selected_scenario", "")).strip()
            state["agent_operator_candidate_previous_scenario"] = previous_scenario
            state["selected_scenario"] = scenario_name
            state["agent_operator_active_candidate_id"] = candidate_id_value
            state["agent_operator_active_candidate_scenario"] = scenario_name
            state["agent_operator_candidate_last_action"] = "applied"
            state["agent_operator_candidate_last_action_at"] = candidate_action_at

        return self._mutate_state(
            action="agent_operator_candidate_applied",
            actor=actor,
            details={
                "candidate_id": candidate_id_value,
                "scenario_name": scenario_name,
                "reason": reason,
            },
            mutate_state=_apply,
        )

    def revert_agent_operator_candidate(
        self,
        *,
        actor: str,
        candidate_id: str = "",
        reason: str = "",
    ) -> dict[str, Any]:
        current_state = self.load_control_state()
        resolved_candidate_id = str(candidate_id or "").strip() or str(
            current_state.get("agent_operator_active_candidate_id", "")
        ).strip()
        if not resolved_candidate_id:
            raise ValueError("candidate_id must not be empty")
        candidate = self.agent_operator_learning_store.revert_candidate(
            candidate_id=resolved_candidate_id,
            actor=actor,
            reason=reason,
        )
        candidate_action_at = _utc_now_iso()
        restored_scenario = str(
            current_state.get("agent_operator_candidate_previous_scenario", "")
        ).strip()

        def _apply(state: dict[str, Any]) -> None:
            active_candidate_id = str(
                state.get("agent_operator_active_candidate_id", "")
            ).strip()
            if active_candidate_id == resolved_candidate_id:
                if restored_scenario:
                    state["selected_scenario"] = restored_scenario
                state["agent_operator_active_candidate_id"] = ""
                state["agent_operator_active_candidate_scenario"] = ""
                state["agent_operator_candidate_previous_scenario"] = ""
            state["agent_operator_candidate_last_action"] = "reverted"
            state["agent_operator_candidate_last_action_at"] = candidate_action_at

        return self._mutate_state(
            action="agent_operator_candidate_reverted",
            actor=actor,
            details={
                "candidate_id": str(candidate.get("candidate_id", "")).strip(),
                "restored_scenario": restored_scenario,
                "reason": reason,
            },
            mutate_state=_apply,
        )

    def annotate(self, *, actor: str, note: str, reason: str = "") -> dict[str, Any]:
        cleaned_note = note.strip()
        if not cleaned_note:
            raise ValueError("note must not be empty")
        cleaned_reason = reason.strip()

        def _apply(state: dict[str, Any]) -> None:
            state["last_annotation"] = cleaned_note
            if cleaned_reason:
                state["last_annotation_reason"] = cleaned_reason

        details: dict[str, Any] = {"note": cleaned_note}
        if cleaned_reason:
            details["reason"] = cleaned_reason

        return self._mutate_state(
            action="incident_annotation",
            actor=actor,
            details=details,
            mutate_state=_apply,
        )

    def list_audit_events(
        self,
        *,
        limit: int = 100,
        action: str | None = None,
        actor: str | None = None,
    ) -> list[dict[str, Any]]:
        limit_value = RuntimeDashboardService._as_positive_int(
            limit,
            field_name="limit",
            max_value=MAX_DASHBOARD_RECENT_AUDIT_LIMIT,
        )
        with self._mutation_lock:
            with self._interprocess_lock():
                rows = _read_jsonl(self.audit_path)
        filtered = rows
        if action and action.strip():
            expected_action = action.strip()
            filtered = [
                row
                for row in filtered
                if str(row.get("action", "")).strip() == expected_action
            ]
        if actor and actor.strip():
            expected_actor = actor.strip()
            filtered = [
                row
                for row in filtered
                if str(row.get("actor", "")).strip() == expected_actor
            ]
        return filtered[-limit_value:]


class RuntimeDashboardService:
    def __init__(
        self,
        *,
        state_path: Path,
        journal_path: Path,
        control_manager: OperatorControlManager,
        kpi_shadow_policy_path: Path | None = None,
    ) -> None:
        self.state_path = state_path
        self.journal_path = journal_path
        self.control_manager = control_manager
        self.kpi_shadow_policy_path = kpi_shadow_policy_path

    def _load_state(self) -> dict[str, Any] | None:
        if not self.state_path.exists():
            return None
        state = _read_json(self.state_path)
        if state.get("schema_version") != RUNTIME_SUPERVISOR_STATE_SCHEMA_VERSION:
            raise ValueError("Runtime supervisor state schema version mismatch")
        return state

    def _load_journal(self) -> list[dict[str, Any]]:
        rows = _read_jsonl(self.journal_path)
        for row in rows:
            if (
                row.get("schema_version")
                != RUNTIME_SUPERVISOR_JOURNAL_EVENT_SCHEMA_VERSION
            ):
                raise ValueError("Runtime supervisor journal schema version mismatch")
        return rows

    @staticmethod
    def _summarize_event_counts(journal_rows: list[dict[str, Any]]) -> dict[str, int]:
        event_counts: dict[str, int] = {}
        for row in journal_rows:
            event_type = str(row.get("event_type", "unknown"))
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
        return event_counts

    @staticmethod
    def _summarize_worker_activity(
        journal_rows: list[dict[str, Any]],
    ) -> dict[str, dict[str, Any]]:
        by_worker: dict[str, dict[str, Any]] = {}
        for row in journal_rows:
            payload = row.get("payload") or {}
            worker_name = payload.get("worker_name")
            if not worker_name:
                continue
            worker = by_worker.setdefault(
                worker_name,
                {
                    "heartbeat_count": 0,
                    "retry_count": 0,
                    "last_heartbeat_timestamp": None,
                    "last_attempt_status": None,
                    "last_failure_reason": None,
                },
            )
            event_type = row.get("event_type")
            if event_type == "worker_heartbeat":
                worker["heartbeat_count"] += 1
                worker["last_heartbeat_timestamp"] = row.get("timestamp")
            elif event_type == "worker_retry_scheduled":
                worker["retry_count"] += 1
            elif event_type == "worker_attempt_completed":
                worker["last_attempt_status"] = payload.get("status")
                worker["last_failure_reason"] = payload.get("failure_reason")
        return by_worker

    @staticmethod
    def _extract_test_token_loop_metadata(
        supervisor_state: dict[str, Any] | None,
    ) -> dict[str, Any]:
        if not supervisor_state:
            return {}
        worker_results = supervisor_state.get("worker_results")
        if not isinstance(worker_results, list):
            return {}
        for worker_result in worker_results:
            if worker_result.get("worker_name") != "test_token_loop":
                continue
            last_metadata = worker_result.get("last_metadata") or {}
            if isinstance(last_metadata, dict):
                return last_metadata
        return {}

    @staticmethod
    def _to_float(value: Any) -> float | None:
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _to_int(value: Any) -> int | None:
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _round_float(value: float | None, *, digits: int) -> float | None:
        if value is None:
            return None
        return round(value, digits)

    @staticmethod
    def _ratio(numerator: float | None, denominator: float | None) -> float | None:
        if numerator is None or denominator is None:
            return None
        if denominator <= 0:
            return None
        return numerator / denominator

    @staticmethod
    def _ratio_with_zero_for_empty_series(
        numerator: float | None, denominator: float | None
    ) -> float | None:
        if numerator is None or denominator is None:
            return None
        if denominator <= 0:
            if abs(numerator) <= 1e-12:
                return 0.0
            return None
        return numerator / denominator

    @staticmethod
    def _normalize_position_rows(rows: Any) -> list[dict[str, Any]]:
        if not isinstance(rows, list):
            return []
        normalized: list[dict[str, Any]] = []
        for row in rows:
            if not isinstance(row, dict):
                continue
            normalized.append(dict(row))
        return normalized

    @staticmethod
    def _extract_position_book(
        supervisor_state: dict[str, Any] | None,
    ) -> dict[str, Any]:
        last_metadata = RuntimeDashboardService._extract_test_token_loop_metadata(
            supervisor_state
        )
        open_positions_detail = RuntimeDashboardService._normalize_position_rows(
            last_metadata.get("open_positions_detail")
        )
        closed_positions_recent = RuntimeDashboardService._normalize_position_rows(
            last_metadata.get("closed_positions_recent")
        )
        return {
            "open_positions": open_positions_detail,
            "closed_positions_recent": closed_positions_recent,
            "open_count": len(open_positions_detail),
            "closed_recent_count": len(closed_positions_recent),
            "verification_links_available": (
                sum(
                    1
                    for row in open_positions_detail + closed_positions_recent
                    if str(row.get("verification_url", "")).strip()
                )
            ),
        }

    @staticmethod
    def _build_game_overview(
        *,
        financial_metrics: dict[str, Any],
        loop_metrics: dict[str, Any],
        position_book: dict[str, Any],
        control_state: dict[str, Any],
    ) -> dict[str, Any]:
        net_pnl = RuntimeDashboardService._to_float(financial_metrics.get("net_pnl"))
        expected_value_after_cost = RuntimeDashboardService._to_float(
            loop_metrics.get("expected_value_after_execution_cost")
        )
        fill_rate = RuntimeDashboardService._to_float(financial_metrics.get("fill_rate"))
        return {
            "phase": (
                "green"
                if (net_pnl is not None and net_pnl >= 0)
                else "amber"
                if (
                    expected_value_after_cost is not None
                    and expected_value_after_cost >= 0
                )
                else "red"
            ),
            "scoreboard": {
                "net_pnl": financial_metrics.get("net_pnl"),
                "equity": financial_metrics.get("current_equity"),
                "expected_value_after_execution_cost": (
                    loop_metrics.get("expected_value_after_execution_cost")
                ),
                "fill_rate": financial_metrics.get("fill_rate"),
                "open_positions": position_book.get("open_count"),
            },
            "quick_controls": {
                "paused": bool(control_state.get("paused", False)),
                "kill_switch_active": bool(
                    control_state.get("kill_switch_active", False)
                ),
                "cancel_all_requested": bool(
                    control_state.get("cancel_all_requested", False)
                ),
            },
            "status_flags": {
                "profitable": bool(net_pnl is not None and net_pnl >= 0),
                "edge_positive": bool(
                    expected_value_after_cost is not None
                    and expected_value_after_cost >= 0
                ),
                "fills_active": bool(fill_rate is not None and fill_rate > 0),
            },
        }

    @staticmethod
    def _extract_loop_metrics(
        supervisor_state: dict[str, Any] | None,
    ) -> dict[str, Any]:
        last_metadata = RuntimeDashboardService._extract_test_token_loop_metadata(
            supervisor_state
        )
        if not last_metadata:
            return {}
        return {
            "events": last_metadata.get("events"),
            "risk_allowed_count": last_metadata.get("risk_allowed_count"),
            "filled_trade_count": last_metadata.get("filled_trade_count"),
            "partial_fill_count": last_metadata.get("partial_fill_count"),
            "exit_candidate_count": last_metadata.get("exit_candidate_count"),
            "confirmed_exit_count": last_metadata.get("confirmed_exit_count"),
            "total_execution_cost": last_metadata.get("total_execution_cost"),
            "attributed_trade_count": last_metadata.get("attributed_trade_count"),
            "expected_gross_edge_value": last_metadata.get(
                "expected_gross_edge_value"
            ),
            "expected_net_edge_value": last_metadata.get("expected_net_edge_value"),
            "expected_net_edge_value_on_fills": last_metadata.get(
                "expected_net_edge_value_on_fills"
            ),
            "expected_value_after_execution_cost": last_metadata.get(
                "expected_value_after_execution_cost"
            ),
            "average_expected_gross_edge_bps": last_metadata.get(
                "average_expected_gross_edge_bps"
            ),
            "average_expected_net_edge_bps": last_metadata.get(
                "average_expected_net_edge_bps"
            ),
            "expected_edge_capture_ratio": last_metadata.get(
                "expected_edge_capture_ratio"
            ),
            "execution_cost_to_expected_net_ratio": last_metadata.get(
                "execution_cost_to_expected_net_ratio"
            ),
            "raw_probability_mean": last_metadata.get("raw_probability_mean"),
            "calibrated_probability_mean": last_metadata.get(
                "calibrated_probability_mean"
            ),
            "probability_drift_mean": last_metadata.get("probability_drift_mean"),
            "probability_drift_abs_mean": last_metadata.get(
                "probability_drift_abs_mean"
            ),
            "probability_drift_max_abs": last_metadata.get("probability_drift_max_abs"),
            "weighted_check_agreement_mean": last_metadata.get(
                "weighted_check_agreement_mean"
            ),
            "calibration_applied_ratio": last_metadata.get(
                "calibration_applied_ratio"
            ),
            "agent_operator_status": last_metadata.get("agent_operator_status"),
            "agent_operator_mode": last_metadata.get("agent_operator_mode"),
            "agent_operator_provider": last_metadata.get("agent_operator_provider"),
            "agent_operator_model": last_metadata.get("agent_operator_model"),
            "agent_operator_risk_posture": last_metadata.get(
                "agent_operator_risk_posture"
            ),
            "agent_operator_confidence": last_metadata.get("agent_operator_confidence"),
            "agent_operator_strategy_scenario_applied": last_metadata.get(
                "agent_operator_strategy_scenario_applied"
            ),
            "agent_operator_strategy_scenario_hint": last_metadata.get(
                "agent_operator_strategy_scenario_hint"
            ),
            "agent_operator_strategy_scenario_rejected_reason": last_metadata.get(
                "agent_operator_strategy_scenario_rejected_reason"
            ),
            "agent_operators_running": last_metadata.get("agent_operators_running"),
            "agent_operators": last_metadata.get("agent_operators"),
            "open_positions_detail": last_metadata.get("open_positions_detail"),
            "closed_positions_recent": last_metadata.get("closed_positions_recent"),
            "mode_lifecycle_current_mode": last_metadata.get(
                "mode_lifecycle_current_mode"
            ),
            "mode_lifecycle_target_mode": last_metadata.get(
                "mode_lifecycle_target_mode"
            ),
            "mode_lifecycle_transition_allowed": last_metadata.get(
                "mode_lifecycle_transition_allowed"
            ),
            "mode_lifecycle_transition_reason_codes": last_metadata.get(
                "mode_lifecycle_transition_reason_codes"
            ),
            "mode_lifecycle_decision_hash": last_metadata.get(
                "mode_lifecycle_decision_hash"
            ),
            "result_hash": last_metadata.get("result_hash"),
        }

    @staticmethod
    def _extract_financial_metrics(
        supervisor_state: dict[str, Any] | None,
        loop_metrics: dict[str, Any],
    ) -> dict[str, Any]:
        last_metadata = RuntimeDashboardService._extract_test_token_loop_metadata(
            supervisor_state
        )
        if not last_metadata:
            return {}

        bankroll = RuntimeDashboardService._to_float(last_metadata.get("bankroll"))
        day_start_equity = RuntimeDashboardService._to_float(
            last_metadata.get("day_start_equity")
        )
        current_equity = RuntimeDashboardService._to_float(
            last_metadata.get("current_equity")
        )
        if day_start_equity is None and bankroll is not None:
            day_start_equity = bankroll
        if current_equity is None and day_start_equity is not None:
            current_equity = day_start_equity

        total_execution_cost = RuntimeDashboardService._to_float(
            last_metadata.get("total_execution_cost")
        )
        if total_execution_cost is None:
            total_execution_cost = RuntimeDashboardService._to_float(
                loop_metrics.get("total_execution_cost")
            )

        total_fees_paid = RuntimeDashboardService._to_float(
            last_metadata.get("total_fees_paid")
        )
        total_slippage_cost = RuntimeDashboardService._to_float(
            last_metadata.get("total_slippage_cost")
        )
        open_notional = RuntimeDashboardService._to_float(
            last_metadata.get("open_notional")
        )
        open_positions = RuntimeDashboardService._to_int(
            last_metadata.get("open_positions")
        )
        risk_allowed_count = RuntimeDashboardService._to_int(
            loop_metrics.get("risk_allowed_count")
        )
        filled_trade_count = RuntimeDashboardService._to_int(
            loop_metrics.get("filled_trade_count")
        )
        partial_fill_count = RuntimeDashboardService._to_int(
            loop_metrics.get("partial_fill_count")
        )
        attributed_trade_count = RuntimeDashboardService._to_int(
            last_metadata.get("attributed_trade_count")
        )
        if attributed_trade_count is None:
            attributed_trade_count = RuntimeDashboardService._to_int(
                loop_metrics.get("attributed_trade_count")
            )

        net_pnl = RuntimeDashboardService._to_float(last_metadata.get("net_pnl"))
        if (
            net_pnl is None
            and day_start_equity is not None
            and current_equity is not None
        ):
            net_pnl = current_equity - day_start_equity

        total_exposure_fraction = RuntimeDashboardService._to_float(
            last_metadata.get("total_exposure_fraction")
        )
        if total_exposure_fraction is None:
            total_exposure_fraction = RuntimeDashboardService._ratio(
                open_notional, bankroll
            )

        daily_drawdown_fraction = RuntimeDashboardService._to_float(
            last_metadata.get("daily_drawdown_fraction")
        )
        if (
            daily_drawdown_fraction is None
            and day_start_equity is not None
            and current_equity is not None
            and day_start_equity > 0
        ):
            drawdown = max(0.0, day_start_equity - current_equity)
            daily_drawdown_fraction = drawdown / day_start_equity

        fill_rate = RuntimeDashboardService._ratio_with_zero_for_empty_series(
            RuntimeDashboardService._to_float(filled_trade_count),
            RuntimeDashboardService._to_float(risk_allowed_count),
        )
        average_execution_cost_per_fill = (
            RuntimeDashboardService._ratio_with_zero_for_empty_series(
            total_execution_cost,
            RuntimeDashboardService._to_float(filled_trade_count),
            )
        )
        expected_gross_edge_value = RuntimeDashboardService._to_float(
            last_metadata.get("expected_gross_edge_value")
        )
        if expected_gross_edge_value is None:
            expected_gross_edge_value = RuntimeDashboardService._to_float(
                loop_metrics.get("expected_gross_edge_value")
            )
        expected_net_edge_value = RuntimeDashboardService._to_float(
            last_metadata.get("expected_net_edge_value")
        )
        if expected_net_edge_value is None:
            expected_net_edge_value = RuntimeDashboardService._to_float(
                loop_metrics.get("expected_net_edge_value")
            )
        expected_net_edge_value_on_fills = RuntimeDashboardService._to_float(
            last_metadata.get("expected_net_edge_value_on_fills")
        )
        if expected_net_edge_value_on_fills is None:
            expected_net_edge_value_on_fills = RuntimeDashboardService._to_float(
                loop_metrics.get("expected_net_edge_value_on_fills")
            )
        expected_value_after_execution_cost = RuntimeDashboardService._to_float(
            last_metadata.get("expected_value_after_execution_cost")
        )
        if (
            expected_value_after_execution_cost is None
            and expected_net_edge_value_on_fills is not None
            and total_execution_cost is not None
        ):
            expected_value_after_execution_cost = (
                expected_net_edge_value_on_fills - total_execution_cost
            )
        average_expected_gross_edge_bps = RuntimeDashboardService._to_float(
            last_metadata.get("average_expected_gross_edge_bps")
        )
        if average_expected_gross_edge_bps is None:
            average_expected_gross_edge_bps = RuntimeDashboardService._to_float(
                loop_metrics.get("average_expected_gross_edge_bps")
            )
        average_expected_net_edge_bps = RuntimeDashboardService._to_float(
            last_metadata.get("average_expected_net_edge_bps")
        )
        if average_expected_net_edge_bps is None:
            average_expected_net_edge_bps = RuntimeDashboardService._to_float(
                loop_metrics.get("average_expected_net_edge_bps")
            )
        expected_edge_capture_ratio = RuntimeDashboardService._to_float(
            last_metadata.get("expected_edge_capture_ratio")
        )
        if expected_edge_capture_ratio is None:
            expected_edge_capture_ratio = (
                RuntimeDashboardService._ratio_with_zero_for_empty_series(
                expected_net_edge_value_on_fills,
                expected_net_edge_value,
                )
            )
        execution_cost_to_expected_net_ratio = RuntimeDashboardService._to_float(
            last_metadata.get("execution_cost_to_expected_net_ratio")
        )
        if execution_cost_to_expected_net_ratio is None:
            execution_cost_to_expected_net_ratio = (
                RuntimeDashboardService._ratio_with_zero_for_empty_series(
                total_execution_cost,
                expected_net_edge_value_on_fills,
                )
            )

        return {
            "bankroll": RuntimeDashboardService._round_float(bankroll, digits=4),
            "day_start_equity": RuntimeDashboardService._round_float(
                day_start_equity, digits=4
            ),
            "current_equity": RuntimeDashboardService._round_float(
                current_equity, digits=4
            ),
            "net_pnl": RuntimeDashboardService._round_float(net_pnl, digits=4),
            "open_notional": RuntimeDashboardService._round_float(
                open_notional, digits=4
            ),
            "open_positions": open_positions,
            "total_exposure_fraction": RuntimeDashboardService._round_float(
                total_exposure_fraction, digits=6
            ),
            "daily_drawdown_fraction": RuntimeDashboardService._round_float(
                daily_drawdown_fraction, digits=6
            ),
            "risk_allowed_count": risk_allowed_count,
            "filled_trade_count": filled_trade_count,
            "partial_fill_count": partial_fill_count,
            "attributed_trade_count": attributed_trade_count,
            "fill_rate": RuntimeDashboardService._round_float(fill_rate, digits=6),
            "total_fees_paid": RuntimeDashboardService._round_float(
                total_fees_paid, digits=4
            ),
            "total_slippage_cost": RuntimeDashboardService._round_float(
                total_slippage_cost, digits=4
            ),
            "total_execution_cost": RuntimeDashboardService._round_float(
                total_execution_cost, digits=4
            ),
            "average_execution_cost_per_fill": RuntimeDashboardService._round_float(
                average_execution_cost_per_fill, digits=4
            ),
            "expected_gross_edge_value": RuntimeDashboardService._round_float(
                expected_gross_edge_value, digits=4
            ),
            "expected_net_edge_value": RuntimeDashboardService._round_float(
                expected_net_edge_value, digits=4
            ),
            "expected_net_edge_value_on_fills": RuntimeDashboardService._round_float(
                expected_net_edge_value_on_fills, digits=4
            ),
            "expected_value_after_execution_cost": RuntimeDashboardService._round_float(
                expected_value_after_execution_cost, digits=4
            ),
            "average_expected_gross_edge_bps": RuntimeDashboardService._round_float(
                average_expected_gross_edge_bps, digits=2
            ),
            "average_expected_net_edge_bps": RuntimeDashboardService._round_float(
                average_expected_net_edge_bps, digits=2
            ),
            "expected_edge_capture_ratio": RuntimeDashboardService._round_float(
                expected_edge_capture_ratio, digits=6
            ),
            "execution_cost_to_expected_net_ratio": RuntimeDashboardService._round_float(
                execution_cost_to_expected_net_ratio, digits=6
            ),
        }

    @staticmethod
    def _as_positive_int(
        value: Any, *, field_name: str, max_value: int | None = None
    ) -> int:
        try:
            parsed = int(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{field_name} must be an integer") from exc
        if parsed <= 0:
            raise ValueError(f"{field_name} must be > 0")
        if max_value is not None and parsed > max_value:
            raise ValueError(f"{field_name} must be <= {max_value}")
        return parsed

    @staticmethod
    def _normalize_optional_filter(value: Any) -> str | None:
        if value is None:
            return None
        cleaned = str(value).strip()
        if not cleaned:
            return None
        return cleaned

    @staticmethod
    def _normalize_kpi_status_filter(value: Any) -> str | None:
        cleaned = RuntimeDashboardService._normalize_optional_filter(value)
        if cleaned is None:
            return None
        allowed_statuses = {"ok", "warning", "critical", "insufficient_data"}
        if cleaned not in allowed_statuses:
            raise ValueError(
                "kpi_status must be one of ok, warning, critical, insufficient_data"
            )
        return cleaned

    @staticmethod
    def _normalize_kpi_definitions(raw_kpis: Any) -> list[dict[str, Any]]:
        if not isinstance(raw_kpis, list):
            return []
        normalized: list[dict[str, Any]] = []
        seen_ids: set[str] = set()
        for item in raw_kpis:
            if not isinstance(item, dict):
                continue
            kpi_id = str(item.get("kpi_id", "")).strip()
            source = str(item.get("source", "")).strip()
            if not kpi_id or not source or kpi_id in seen_ids:
                continue
            seen_ids.add(kpi_id)
            direction = str(item.get("direction", "higher_is_better")).strip()
            if direction not in {"higher_is_better", "lower_is_better"}:
                direction = "higher_is_better"
            normalized_item = dict(item)
            normalized_item["kpi_id"] = kpi_id
            normalized_item["source"] = source
            normalized_item["label"] = (
                str(item.get("label", "")).strip() or kpi_id.replace("_", " ").title()
            )
            normalized_item["domain"] = (
                str(item.get("domain", "")).strip() or "uncategorized"
            )
            normalized_item["direction"] = direction
            cycle_field = RuntimeDashboardService._normalize_optional_filter(
                item.get("cycle_field")
            )
            if cycle_field is not None:
                normalized_item["cycle_field"] = cycle_field
            else:
                normalized_item.pop("cycle_field", None)
            unit = RuntimeDashboardService._normalize_optional_filter(item.get("unit"))
            if unit is not None:
                normalized_item["unit"] = unit
            threshold_keys = (
                "warning_below",
                "critical_below",
                "warning_above",
                "critical_above",
            )
            for threshold_key in threshold_keys:
                threshold_value = RuntimeDashboardService._to_float(
                    item.get(threshold_key)
                )
                if threshold_value is None:
                    normalized_item.pop(threshold_key, None)
                    continue
                normalized_item[threshold_key] = threshold_value
            normalized.append(normalized_item)
        return normalized

    def _load_kpi_shadow_policy(self) -> dict[str, Any]:
        default_policy = json.loads(json.dumps(_default_kpi_shadow_policy()))
        if self.kpi_shadow_policy_path is None:
            return default_policy
        if not self.kpi_shadow_policy_path.exists():
            return default_policy

        payload = _read_json(self.kpi_shadow_policy_path)
        if payload.get("schema_version") != KPI_SHADOW_POLICY_SCHEMA_VERSION:
            raise ValueError("KPI shadow policy schema version mismatch")

        default_window = RuntimeDashboardService._to_int(payload.get("default_window"))
        if default_window is not None and default_window > 0:
            default_policy["default_window"] = default_window
        minimum_sample_size = RuntimeDashboardService._to_int(
            payload.get("minimum_sample_size")
        )
        if minimum_sample_size is not None and minimum_sample_size > 0:
            default_policy["minimum_sample_size"] = minimum_sample_size
        mode = RuntimeDashboardService._normalize_optional_filter(payload.get("mode"))
        if mode is not None:
            default_policy["mode"] = mode
        updated_at = RuntimeDashboardService._normalize_optional_filter(
            payload.get("updated_at")
        )
        if updated_at is not None:
            default_policy["updated_at"] = updated_at

        normalized_kpis = RuntimeDashboardService._normalize_kpi_definitions(
            payload.get("kpis")
        )
        if normalized_kpis:
            default_policy["kpis"] = normalized_kpis
        return default_policy

    @staticmethod
    def _lookup_nested_value(source: str, context: dict[str, Any]) -> Any:
        current: Any = context
        for segment in source.split("."):
            if not isinstance(current, dict):
                return None
            current = current.get(segment)
            if current is None:
                return None
        return current

    @staticmethod
    def _extract_kpi_series(
        cycle_summaries: list[dict[str, Any]],
        *,
        cycle_field: str | None,
        window: int,
    ) -> list[dict[str, Any]]:
        if cycle_field is None:
            return []
        values: list[dict[str, Any]] = []
        for cycle_summary in cycle_summaries[-window:]:
            value = RuntimeDashboardService._to_float(cycle_summary.get(cycle_field))
            if value is None:
                continue
            values.append(
                {
                    "cycle_index": cycle_summary.get("cycle_index"),
                    "timestamp": cycle_summary.get("timestamp"),
                    "value": round(value, 6),
                }
            )
        return values

    @staticmethod
    def _evaluate_kpi_status(
        *,
        value: float | None,
        sample_count: int,
        minimum_sample_size: int,
        definition: dict[str, Any],
    ) -> tuple[str, str]:
        if value is None:
            return ("insufficient_data", "latest_value_missing")
        if sample_count < minimum_sample_size:
            return ("insufficient_data", "minimum_sample_size_not_met")

        direction = str(definition.get("direction", "higher_is_better"))
        warning_below = RuntimeDashboardService._to_float(definition.get("warning_below"))
        critical_below = RuntimeDashboardService._to_float(
            definition.get("critical_below")
        )
        warning_above = RuntimeDashboardService._to_float(definition.get("warning_above"))
        critical_above = RuntimeDashboardService._to_float(
            definition.get("critical_above")
        )

        if direction == "higher_is_better":
            if critical_below is not None and value <= critical_below:
                return ("critical", "critical_below_threshold")
            if warning_below is not None and value <= warning_below:
                return ("warning", "warning_below_threshold")
        else:
            if critical_above is not None and value >= critical_above:
                return ("critical", "critical_above_threshold")
            if warning_above is not None and value >= warning_above:
                return ("warning", "warning_above_threshold")
        return ("ok", "within_threshold")

    @staticmethod
    def _derive_kpi_metrics(
        *,
        financial_metrics: dict[str, Any],
        worker_activity: dict[str, dict[str, Any]],
        incident_feed: dict[str, Any],
        cycle_summaries: list[dict[str, Any]],
    ) -> dict[str, Any]:
        partial_fill_rate = RuntimeDashboardService._ratio_with_zero_for_empty_series(
            RuntimeDashboardService._to_float(financial_metrics.get("partial_fill_count")),
            RuntimeDashboardService._to_float(financial_metrics.get("filled_trade_count")),
        )
        test_token_loop_retry_count = RuntimeDashboardService._to_float(
            (worker_activity.get("test_token_loop") or {}).get("retry_count")
        )
        total_cycles = len(cycle_summaries)
        total_incidents = RuntimeDashboardService._to_float(
            (incident_feed.get("paging") or {}).get("total_incidents")
        )
        incident_density_per_cycle = RuntimeDashboardService._ratio(
            total_incidents,
            RuntimeDashboardService._to_float(total_cycles),
        )
        return {
            "partial_fill_rate": RuntimeDashboardService._round_float(
                partial_fill_rate,
                digits=6,
            ),
            "test_token_loop_retry_count": RuntimeDashboardService._round_float(
                test_token_loop_retry_count,
                digits=4,
            ),
            "incident_density_per_cycle": RuntimeDashboardService._round_float(
                incident_density_per_cycle,
                digits=6,
            ),
            "incident_total_count": RuntimeDashboardService._to_int(total_incidents),
        }

    @staticmethod
    def _build_kpi_shadow_payload(
        *,
        policy: dict[str, Any],
        financial_metrics: dict[str, Any],
        loop_metrics: dict[str, Any],
        worker_activity: dict[str, dict[str, Any]],
        incident_feed: dict[str, Any],
        cycle_summaries: list[dict[str, Any]],
        window: int,
        kpi_domain: str | None,
        kpi_status: str | None,
    ) -> dict[str, Any]:
        minimum_sample_size = RuntimeDashboardService._to_int(
            policy.get("minimum_sample_size")
        )
        if minimum_sample_size is None or minimum_sample_size <= 0:
            minimum_sample_size = 1
        derived_metrics = RuntimeDashboardService._derive_kpi_metrics(
            financial_metrics=financial_metrics,
            worker_activity=worker_activity,
            incident_feed=incident_feed,
            cycle_summaries=cycle_summaries,
        )
        context: dict[str, Any] = {
            "financial_metrics": financial_metrics,
            "loop_metrics": loop_metrics,
            "worker_activity": worker_activity,
            "kpi_derived": derived_metrics,
        }
        items: list[dict[str, Any]] = []
        available_domains: set[str] = set()
        for definition in policy.get("kpis", []):
            if not isinstance(definition, dict):
                continue
            domain = str(definition.get("domain", "uncategorized")).strip()
            if not domain:
                domain = "uncategorized"
            available_domains.add(domain)
            if kpi_domain is not None and domain != kpi_domain:
                continue
            source = str(definition.get("source", "")).strip()
            if not source:
                continue
            cycle_field = RuntimeDashboardService._normalize_optional_filter(
                definition.get("cycle_field")
            )
            series = RuntimeDashboardService._extract_kpi_series(
                cycle_summaries,
                cycle_field=cycle_field,
                window=window,
            )
            latest_value = RuntimeDashboardService._to_float(
                RuntimeDashboardService._lookup_nested_value(source, context)
            )
            if latest_value is None and series:
                latest_value = RuntimeDashboardService._to_float(series[-1].get("value"))
            previous_value = None
            if len(series) >= 2:
                previous_value = RuntimeDashboardService._to_float(series[-2].get("value"))
            delta_value = None
            if latest_value is not None and previous_value is not None:
                delta_value = round(latest_value - previous_value, 6)
            sample_count = len(series)
            if sample_count == 0 and latest_value is not None:
                sample_count = 1
            status, status_reason = RuntimeDashboardService._evaluate_kpi_status(
                value=latest_value,
                sample_count=sample_count,
                minimum_sample_size=minimum_sample_size,
                definition=definition,
            )
            if kpi_status is not None and status != kpi_status:
                continue

            threshold_keys = (
                "warning_below",
                "critical_below",
                "warning_above",
                "critical_above",
            )
            thresholds: dict[str, float] = {}
            for threshold_key in threshold_keys:
                threshold_value = RuntimeDashboardService._to_float(
                    definition.get(threshold_key)
                )
                if threshold_value is None:
                    continue
                thresholds[threshold_key] = round(threshold_value, 6)

            items.append(
                {
                    "kpi_id": definition.get("kpi_id"),
                    "label": definition.get("label"),
                    "domain": domain,
                    "unit": definition.get("unit"),
                    "direction": definition.get("direction"),
                    "source": source,
                    "mode": "shadow",
                    "shadow_only": True,
                    "status": status,
                    "status_reason": status_reason,
                    "sample_count": sample_count,
                    "minimum_sample_size": minimum_sample_size,
                    "window": window,
                    "latest_value": RuntimeDashboardService._round_float(
                        latest_value,
                        digits=6,
                    ),
                    "previous_value": RuntimeDashboardService._round_float(
                        previous_value,
                        digits=6,
                    ),
                    "delta": RuntimeDashboardService._round_float(
                        delta_value,
                        digits=6,
                    ),
                    "latest_cycle_index": (
                        series[-1].get("cycle_index") if series else None
                    ),
                    "thresholds": thresholds,
                    "series": series,
                }
            )

        items.sort(key=lambda item: (str(item.get("domain")), str(item.get("kpi_id"))))
        status_counts = {
            "ok": 0,
            "warning": 0,
            "critical": 0,
            "insufficient_data": 0,
        }
        domain_counts: dict[str, dict[str, Any]] = {}
        for item in items:
            status = str(item.get("status"))
            if status in status_counts:
                status_counts[status] += 1
            domain = str(item.get("domain"))
            domain_summary = domain_counts.setdefault(
                domain,
                {
                    "total": 0,
                    "status_counts": {
                        "ok": 0,
                        "warning": 0,
                        "critical": 0,
                        "insufficient_data": 0,
                    },
                },
            )
            domain_summary["total"] += 1
            if status in domain_summary["status_counts"]:
                domain_summary["status_counts"][status] += 1

        return {
            "mode": str(policy.get("mode", "shadow")),
            "policy": {
                "schema_version": policy.get("schema_version"),
                "updated_at": policy.get("updated_at"),
                "minimum_sample_size": minimum_sample_size,
                "default_window": policy.get("default_window"),
                "configured_kpi_count": len(policy.get("kpis", [])),
            },
            "filters": {
                "window": window,
                "domain": kpi_domain,
                "status": kpi_status,
                "available_domains": sorted(available_domains),
                "available_statuses": [
                    "ok",
                    "warning",
                    "critical",
                    "insufficient_data",
                ],
            },
            "summary": {
                "total_kpis": len(items),
                "status_counts": status_counts,
                "domain_counts": domain_counts,
                "total_cycles_available": len(cycle_summaries),
            },
            "derived_metrics": derived_metrics,
            "items": items,
        }

    @staticmethod
    def _incident_from_journal_row(
        row: dict[str, Any], *, sequence: int
    ) -> dict[str, Any] | None:
        event_type = str(row.get("event_type", "unknown"))
        payload = row.get("payload") or {}
        timestamp = row.get("timestamp")

        if event_type == "worker_retry_scheduled":
            worker_name = str(payload.get("worker_name", "worker"))
            next_attempt = payload.get("next_attempt_number")
            summary = (
                f"Retry scheduled for {worker_name} (next_attempt={next_attempt})."
            )
            severity = "warning"
        elif (
            event_type == "worker_attempt_completed"
            and str(payload.get("status")) == "FAILED"
        ):
            worker_name = str(payload.get("worker_name", "worker"))
            failure_reason = str(payload.get("failure_reason", "unknown_failure"))
            summary = f"Worker attempt failed: {worker_name} ({failure_reason})."
            severity = "error"
        elif event_type == "cycle_completed" and str(payload.get("status")) == "FAILED":
            cycle_index = payload.get("cycle_index")
            summary = f"Cycle completed in FAILED state (cycle_index={cycle_index})."
            severity = "error"
        elif event_type == "control_invalid_scenario_fallback":
            requested = payload.get("requested_scenario")
            fallback = payload.get("fallback_scenario")
            summary = f"Invalid scenario fallback applied: {requested} -> {fallback}."
            severity = "warning"
        elif event_type == "control_restart_acknowledged":
            cycle_index = payload.get("cycle_index")
            summary = f"Restart request acknowledged before cycle execution (cycle_index={cycle_index})."
            severity = "info"
        elif (
            event_type == "worker_heartbeat"
            and payload.get("worker_name") == "test_token_loop"
            and payload.get("stage") == "cycle_completed"
        ):
            details = payload.get("details") or {}
            cycle_index = details.get("cycle_index", payload.get("cycle_index"))
            expected_value_after_execution_cost = RuntimeDashboardService._to_float(
                details.get("expected_value_after_execution_cost")
            )
            execution_cost_to_expected_net_ratio = RuntimeDashboardService._to_float(
                details.get("execution_cost_to_expected_net_ratio")
            )
            open_positions = RuntimeDashboardService._to_int(
                details.get("open_positions")
            )
            events = RuntimeDashboardService._to_int(details.get("events"))
            state_refresh_applied = bool(details.get("state_refresh_applied"))
            state_refresh_event_count = RuntimeDashboardService._to_int(
                details.get("state_refresh_event_count")
            )
            state_refresh_max_streak = RuntimeDashboardService._to_int(
                details.get("state_refresh_max_streak")
            )
            stale_open_position_market_ids_raw = details.get(
                "stale_open_position_market_ids"
            )
            stale_open_position_market_ids: list[str] = []
            if isinstance(stale_open_position_market_ids_raw, list):
                for market_id in stale_open_position_market_ids_raw:
                    market_id_text = str(market_id).strip()
                    if market_id_text:
                        stale_open_position_market_ids.append(market_id_text)
            open_positions_value = open_positions or 0
            healthy_ingestion_zero_risk_alert = bool(
                details.get("healthy_ingestion_zero_risk_alert")
            )
            healthy_ingestion_zero_risk_streak = RuntimeDashboardService._to_int(
                details.get("healthy_ingestion_zero_risk_streak")
            )
            near_cap_zero_fill_alert = bool(details.get("near_cap_zero_fill_alert"))
            near_cap_zero_fill_streak = RuntimeDashboardService._to_int(
                details.get("near_cap_zero_fill_streak")
            )
            near_cap_exposure_threshold_fraction = (
                RuntimeDashboardService._to_float(
                    details.get("near_cap_exposure_threshold_fraction")
                )
            )
            total_exposure_fraction = RuntimeDashboardService._to_float(
                details.get("total_exposure_fraction")
            )
            filled_trade_count = RuntimeDashboardService._to_int(
                details.get("filled_trade_count")
            )
            ingestion_status = str(details.get("ingestion_status") or "")
            risk_allowed_count = RuntimeDashboardService._to_int(
                details.get("risk_allowed_count")
            )
            if healthy_ingestion_zero_risk_alert:
                summary = (
                    "Ingestion remained healthy while risk approvals were "
                    "continuously zero "
                    f"(cycle_index={cycle_index}, "
                    f"streak={healthy_ingestion_zero_risk_streak or 0}, "
                    f"ingestion_status={ingestion_status or 'unknown'}, "
                    f"risk_allowed_count={risk_allowed_count or 0})."
                )
                severity = "warning"
            elif near_cap_zero_fill_alert:
                summary = (
                    "Near-cap exposure persisted with zero fills across "
                    "consecutive cycles "
                    f"(cycle_index={cycle_index}, "
                    f"streak={near_cap_zero_fill_streak or 0}, "
                    f"total_exposure_fraction={total_exposure_fraction or 0:.4f}, "
                    "threshold="
                    f"{near_cap_exposure_threshold_fraction or 0:.4f}, "
                    f"filled_trade_count={filled_trade_count or 0})."
                )
                severity = "warning"
            elif (
                expected_value_after_execution_cost is not None
                and expected_value_after_execution_cost < 0
            ):
                summary = (
                    "Negative expected value after execution costs detected "
                    f"(cycle_index={cycle_index}, "
                    f"value={expected_value_after_execution_cost:.4f})."
                )
                severity = "warning"
            elif (
                execution_cost_to_expected_net_ratio is not None
                and execution_cost_to_expected_net_ratio > 1.0
            ):
                summary = (
                    "Execution cost exceeded expected net edge "
                    f"(cycle_index={cycle_index}, "
                    f"ratio={execution_cost_to_expected_net_ratio:.4f})."
                )
                severity = "warning"
            elif stale_open_position_market_ids and open_positions_value > 0:
                stale_market_preview = ", ".join(stale_open_position_market_ids[:3])
                if len(stale_open_position_market_ids) > 3:
                    stale_market_preview = f"{stale_market_preview}, ..."
                summary = (
                    "State refresh replay has persisted across consecutive cycles "
                    "while open positions remain "
                    f"(cycle_index={cycle_index}, "
                    f"open_positions={open_positions_value}, "
                    f"max_streak={state_refresh_max_streak or 0}, "
                    f"stale_markets={stale_market_preview})."
                )
                severity = "error"
            elif state_refresh_applied and open_positions_value > 0:
                summary = (
                    "No fresh live events were available while open positions remained; "
                    "state refresh replay was applied "
                    f"(cycle_index={cycle_index}, "
                    f"open_positions={open_positions_value}, "
                    f"state_refresh_events={state_refresh_event_count or 0})."
                )
                severity = "warning"
            elif events == 0 and open_positions_value > 0:
                summary = (
                    "Cycle processed zero events while open positions remained "
                    f"(cycle_index={cycle_index}, "
                    f"open_positions={open_positions_value})."
                )
                severity = "warning"
            else:
                return None
        else:
            return None

        return {
            "incident_id": f"{sequence}:{event_type}",
            "incident_sequence": sequence,
            "timestamp": timestamp,
            "event_type": event_type,
            "severity": severity,
            "summary": summary,
            "payload": payload,
        }

    @staticmethod
    def _build_incident_feed_payload(
        journal_rows: list[dict[str, Any]],
        *,
        limit: int,
        cursor: Any,
    ) -> dict[str, Any]:
        incident_rows: list[dict[str, Any]] = []
        for sequence, row in enumerate(journal_rows, start=1):
            incident = RuntimeDashboardService._incident_from_journal_row(
                row, sequence=sequence
            )
            if incident is not None:
                incident_rows.append(incident)

        upper_bound = len(incident_rows)
        normalized_cursor: str | None = None
        if cursor is not None:
            normalized_cursor = str(cursor).strip() or None
        if normalized_cursor is not None:
            try:
                upper_bound = min(upper_bound, max(0, int(normalized_cursor)))
            except ValueError as exc:
                raise ValueError("incident_cursor must be an integer") from exc

        start_index = max(0, upper_bound - limit)
        page_items = incident_rows[start_index:upper_bound]
        next_cursor = str(start_index) if start_index > 0 else None

        return {
            "items": page_items,
            "paging": {
                "limit": limit,
                "cursor": normalized_cursor,
                "next_cursor": next_cursor,
                "total_incidents": len(incident_rows),
            },
        }

    @staticmethod
    def _extract_cycle_summaries_from_journal(
        journal_rows: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        by_cycle_index: dict[int, dict[str, Any]] = {}
        for row in journal_rows:
            if row.get("event_type") != "worker_heartbeat":
                continue
            payload = row.get("payload") or {}
            if payload.get("worker_name") != "test_token_loop":
                continue
            if payload.get("stage") != "cycle_completed":
                continue
            details = payload.get("details") or {}
            raw_cycle_index = details.get("cycle_index", payload.get("cycle_index"))
            if raw_cycle_index is None:
                continue
            try:
                cycle_index = int(raw_cycle_index)
            except (TypeError, ValueError):
                continue
            risk_allowed_count = RuntimeDashboardService._to_int(
                details.get("risk_allowed_count")
            )
            filled_trade_count = RuntimeDashboardService._to_int(
                details.get("filled_trade_count")
            )
            partial_fill_count = RuntimeDashboardService._to_int(
                details.get("partial_fill_count")
            )
            total_execution_cost = RuntimeDashboardService._to_float(
                details.get("total_execution_cost")
            )
            total_fees_paid = RuntimeDashboardService._to_float(
                details.get("total_fees_paid")
            )
            total_slippage_cost = RuntimeDashboardService._to_float(
                details.get("total_slippage_cost")
            )
            current_equity = RuntimeDashboardService._to_float(
                details.get("current_equity")
            )
            open_notional = RuntimeDashboardService._to_float(details.get("open_notional"))
            total_exposure_fraction = RuntimeDashboardService._to_float(
                details.get("total_exposure_fraction")
            )
            daily_drawdown_fraction = RuntimeDashboardService._to_float(
                details.get("daily_drawdown_fraction")
            )
            fill_rate = RuntimeDashboardService._ratio_with_zero_for_empty_series(
                RuntimeDashboardService._to_float(filled_trade_count),
                RuntimeDashboardService._to_float(risk_allowed_count),
            )
            partial_fill_rate = RuntimeDashboardService._ratio_with_zero_for_empty_series(
                RuntimeDashboardService._to_float(partial_fill_count),
                RuntimeDashboardService._to_float(filled_trade_count),
            )
            average_execution_cost_per_fill = (
                RuntimeDashboardService._ratio_with_zero_for_empty_series(
                total_execution_cost,
                RuntimeDashboardService._to_float(filled_trade_count),
                )
            )
            expected_net_edge_value = RuntimeDashboardService._to_float(
                details.get("expected_net_edge_value")
            )
            expected_net_edge_value_on_fills = RuntimeDashboardService._to_float(
                details.get("expected_net_edge_value_on_fills")
            )
            expected_edge_capture_ratio = RuntimeDashboardService._to_float(
                details.get("expected_edge_capture_ratio")
            )
            if expected_edge_capture_ratio is None:
                expected_edge_capture_ratio = (
                    RuntimeDashboardService._ratio_with_zero_for_empty_series(
                        expected_net_edge_value_on_fills,
                        expected_net_edge_value,
                    )
                )
            execution_cost_to_expected_net_ratio = RuntimeDashboardService._to_float(
                details.get("execution_cost_to_expected_net_ratio")
            )
            if execution_cost_to_expected_net_ratio is None:
                execution_cost_to_expected_net_ratio = (
                    RuntimeDashboardService._ratio_with_zero_for_empty_series(
                        total_execution_cost,
                        expected_net_edge_value_on_fills,
                    )
                )
            raw_probability_mean = RuntimeDashboardService._to_float(
                details.get("raw_probability_mean")
            )
            calibrated_probability_mean = RuntimeDashboardService._to_float(
                details.get("calibrated_probability_mean")
            )
            probability_drift_mean = RuntimeDashboardService._to_float(
                details.get("probability_drift_mean")
            )
            probability_drift_abs_mean = RuntimeDashboardService._to_float(
                details.get("probability_drift_abs_mean")
            )
            probability_drift_max_abs = RuntimeDashboardService._to_float(
                details.get("probability_drift_max_abs")
            )
            weighted_check_agreement_mean = RuntimeDashboardService._to_float(
                details.get("weighted_check_agreement_mean")
            )
            calibration_applied_ratio = RuntimeDashboardService._to_float(
                details.get("calibration_applied_ratio")
            )
            by_cycle_index[cycle_index] = {
                "cycle_index": cycle_index,
                "timestamp": row.get("timestamp"),
                "selected_scenario": details.get("selected_scenario"),
                "control_version": details.get("control_version"),
                "events": details.get("events"),
                "risk_allowed_count": risk_allowed_count,
                "filled_trade_count": filled_trade_count,
                "partial_fill_count": partial_fill_count,
                "exit_candidate_count": details.get("exit_candidate_count"),
                "confirmed_exit_count": details.get("confirmed_exit_count"),
                "total_execution_cost": total_execution_cost,
                "total_fees_paid": total_fees_paid,
                "total_slippage_cost": total_slippage_cost,
                "net_pnl": details.get("net_pnl"),
                "current_equity": current_equity,
                "open_notional": open_notional,
                "open_positions": details.get("open_positions"),
                "total_exposure_fraction": total_exposure_fraction,
                "daily_drawdown_fraction": daily_drawdown_fraction,
                "attributed_trade_count": details.get("attributed_trade_count"),
                "fill_rate": RuntimeDashboardService._round_float(fill_rate, digits=6),
                "partial_fill_rate": RuntimeDashboardService._round_float(
                    partial_fill_rate,
                    digits=6,
                ),
                "expected_net_edge_value_on_fills": RuntimeDashboardService._round_float(
                    expected_net_edge_value_on_fills,
                    digits=4,
                ),
                "average_execution_cost_per_fill": RuntimeDashboardService._round_float(
                    average_execution_cost_per_fill,
                    digits=4,
                ),
                "expected_gross_edge_value": details.get("expected_gross_edge_value"),
                "expected_net_edge_value": RuntimeDashboardService._round_float(
                    expected_net_edge_value,
                    digits=4,
                ),
                "expected_value_after_execution_cost": details.get(
                    "expected_value_after_execution_cost"
                ),
                "expected_edge_capture_ratio": RuntimeDashboardService._round_float(
                    expected_edge_capture_ratio,
                    digits=6,
                ),
                "execution_cost_to_expected_net_ratio": (
                    RuntimeDashboardService._round_float(
                        execution_cost_to_expected_net_ratio,
                        digits=6,
                    )
                ),
                "raw_probability_mean": RuntimeDashboardService._round_float(
                    raw_probability_mean,
                    digits=6,
                ),
                "calibrated_probability_mean": RuntimeDashboardService._round_float(
                    calibrated_probability_mean,
                    digits=6,
                ),
                "probability_drift_mean": RuntimeDashboardService._round_float(
                    probability_drift_mean,
                    digits=6,
                ),
                "probability_drift_abs_mean": RuntimeDashboardService._round_float(
                    probability_drift_abs_mean,
                    digits=6,
                ),
                "probability_drift_max_abs": RuntimeDashboardService._round_float(
                    probability_drift_max_abs,
                    digits=6,
                ),
                "weighted_check_agreement_mean": RuntimeDashboardService._round_float(
                    weighted_check_agreement_mean,
                    digits=6,
                ),
                "calibration_applied_ratio": RuntimeDashboardService._round_float(
                    calibration_applied_ratio,
                    digits=6,
                ),
                "result_hash_prefix": details.get("result_hash_prefix"),
            }
        return [by_cycle_index[index] for index in sorted(by_cycle_index.keys())]

    @staticmethod
    def _delta(previous_value: Any, current_value: Any) -> int | None:
        try:
            previous_int = int(previous_value)
            current_int = int(current_value)
        except (TypeError, ValueError):
            return None
        return current_int - previous_int

    @staticmethod
    def _delta_float(
        previous_value: Any, current_value: Any, *, digits: int = 6
    ) -> float | None:
        try:
            previous_float = float(previous_value)
            current_float = float(current_value)
        except (TypeError, ValueError):
            return None
        return round(current_float - previous_float, digits)

    @staticmethod
    def _build_cycle_comparison_payload(
        journal_rows: list[dict[str, Any]],
        *,
        window: int,
    ) -> dict[str, Any]:
        cycle_summaries = RuntimeDashboardService._extract_cycle_summaries_from_journal(
            journal_rows
        )
        windowed = cycle_summaries[-window:]
        comparison_items: list[dict[str, Any]] = []

        previous: dict[str, Any] | None = None
        for entry in windowed:
            enriched = dict(entry)
            if previous is None:
                enriched["delta"] = None
            else:
                enriched["delta"] = {
                    "events": RuntimeDashboardService._delta(
                        previous.get("events"), entry.get("events")
                    ),
                    "risk_allowed_count": RuntimeDashboardService._delta(
                        previous.get("risk_allowed_count"),
                        entry.get("risk_allowed_count"),
                    ),
                    "filled_trade_count": RuntimeDashboardService._delta(
                        previous.get("filled_trade_count"),
                        entry.get("filled_trade_count"),
                    ),
                    "partial_fill_count": RuntimeDashboardService._delta(
                        previous.get("partial_fill_count"),
                        entry.get("partial_fill_count"),
                    ),
                    "exit_candidate_count": RuntimeDashboardService._delta(
                        previous.get("exit_candidate_count"),
                        entry.get("exit_candidate_count"),
                    ),
                    "confirmed_exit_count": RuntimeDashboardService._delta(
                        previous.get("confirmed_exit_count"),
                        entry.get("confirmed_exit_count"),
                    ),
                    "total_execution_cost": RuntimeDashboardService._delta_float(
                        previous.get("total_execution_cost"),
                        entry.get("total_execution_cost"),
                        digits=4,
                    ),
                    "net_pnl": RuntimeDashboardService._delta_float(
                        previous.get("net_pnl"),
                        entry.get("net_pnl"),
                        digits=4,
                    ),
                    "attributed_trade_count": RuntimeDashboardService._delta(
                        previous.get("attributed_trade_count"),
                        entry.get("attributed_trade_count"),
                    ),
                    "fill_rate": RuntimeDashboardService._delta_float(
                        previous.get("fill_rate"),
                        entry.get("fill_rate"),
                        digits=6,
                    ),
                    "partial_fill_rate": RuntimeDashboardService._delta_float(
                        previous.get("partial_fill_rate"),
                        entry.get("partial_fill_rate"),
                        digits=6,
                    ),
                    "average_execution_cost_per_fill": (
                        RuntimeDashboardService._delta_float(
                            previous.get("average_execution_cost_per_fill"),
                            entry.get("average_execution_cost_per_fill"),
                            digits=4,
                        )
                    ),
                    "daily_drawdown_fraction": RuntimeDashboardService._delta_float(
                        previous.get("daily_drawdown_fraction"),
                        entry.get("daily_drawdown_fraction"),
                        digits=6,
                    ),
                    "total_exposure_fraction": RuntimeDashboardService._delta_float(
                        previous.get("total_exposure_fraction"),
                        entry.get("total_exposure_fraction"),
                        digits=6,
                    ),
                    "expected_gross_edge_value": (
                        RuntimeDashboardService._delta_float(
                            previous.get("expected_gross_edge_value"),
                            entry.get("expected_gross_edge_value"),
                            digits=4,
                        )
                    ),
                    "expected_net_edge_value": RuntimeDashboardService._delta_float(
                        previous.get("expected_net_edge_value"),
                        entry.get("expected_net_edge_value"),
                        digits=4,
                    ),
                    "expected_net_edge_value_on_fills": (
                        RuntimeDashboardService._delta_float(
                            previous.get("expected_net_edge_value_on_fills"),
                            entry.get("expected_net_edge_value_on_fills"),
                            digits=4,
                        )
                    ),
                    "expected_value_after_execution_cost": (
                        RuntimeDashboardService._delta_float(
                            previous.get("expected_value_after_execution_cost"),
                            entry.get("expected_value_after_execution_cost"),
                            digits=4,
                        )
                    ),
                    "expected_edge_capture_ratio": (
                        RuntimeDashboardService._delta_float(
                            previous.get("expected_edge_capture_ratio"),
                            entry.get("expected_edge_capture_ratio"),
                            digits=6,
                        )
                    ),
                    "execution_cost_to_expected_net_ratio": (
                        RuntimeDashboardService._delta_float(
                            previous.get("execution_cost_to_expected_net_ratio"),
                            entry.get("execution_cost_to_expected_net_ratio"),
                            digits=6,
                        )
                    ),
                    "raw_probability_mean": RuntimeDashboardService._delta_float(
                        previous.get("raw_probability_mean"),
                        entry.get("raw_probability_mean"),
                        digits=6,
                    ),
                    "calibrated_probability_mean": (
                        RuntimeDashboardService._delta_float(
                            previous.get("calibrated_probability_mean"),
                            entry.get("calibrated_probability_mean"),
                            digits=6,
                        )
                    ),
                    "probability_drift_mean": RuntimeDashboardService._delta_float(
                        previous.get("probability_drift_mean"),
                        entry.get("probability_drift_mean"),
                        digits=6,
                    ),
                    "probability_drift_abs_mean": (
                        RuntimeDashboardService._delta_float(
                            previous.get("probability_drift_abs_mean"),
                            entry.get("probability_drift_abs_mean"),
                            digits=6,
                        )
                    ),
                    "probability_drift_max_abs": RuntimeDashboardService._delta_float(
                        previous.get("probability_drift_max_abs"),
                        entry.get("probability_drift_max_abs"),
                        digits=6,
                    ),
                    "weighted_check_agreement_mean": (
                        RuntimeDashboardService._delta_float(
                            previous.get("weighted_check_agreement_mean"),
                            entry.get("weighted_check_agreement_mean"),
                            digits=6,
                        )
                    ),
                    "calibration_applied_ratio": RuntimeDashboardService._delta_float(
                        previous.get("calibration_applied_ratio"),
                        entry.get("calibration_applied_ratio"),
                        digits=6,
                    ),
                }
            comparison_items.append(enriched)
            previous = entry

        return {
            "window": window,
            "total_cycles": len(cycle_summaries),
            "items": comparison_items,
        }

    def build_incident_feed(
        self, *, limit: int = 50, cursor: Any = None
    ) -> dict[str, Any]:
        limit_value = self._as_positive_int(
            limit,
            field_name="incident_limit",
            max_value=MAX_DASHBOARD_INCIDENT_LIMIT,
        )
        journal_rows = self._load_journal()
        return self._build_incident_feed_payload(
            journal_rows,
            limit=limit_value,
            cursor=cursor,
        )

    def build_cycle_comparison(self, *, window: int = 10) -> dict[str, Any]:
        window_value = self._as_positive_int(
            window,
            field_name="comparison_window",
            max_value=MAX_DASHBOARD_COMPARISON_WINDOW,
        )
        journal_rows = self._load_journal()
        return self._build_cycle_comparison_payload(
            journal_rows,
            window=window_value,
        )

    def build_dashboard_payload(
        self,
        *,
        recent_events_limit: int = 200,
        recent_audit_limit: int = 100,
        audit_action: str | None = None,
        audit_actor: str | None = None,
        incident_limit: int = 50,
        incident_cursor: Any = None,
        comparison_window: int = 10,
        kpi_window: Any = None,
        kpi_domain: Any = None,
        kpi_status: Any = None,
    ) -> dict[str, Any]:
        events_limit = self._as_positive_int(
            recent_events_limit,
            field_name="recent_events_limit",
            max_value=MAX_DASHBOARD_RECENT_EVENTS_LIMIT,
        )
        audit_limit = self._as_positive_int(
            recent_audit_limit,
            field_name="recent_audit_limit",
            max_value=MAX_DASHBOARD_RECENT_AUDIT_LIMIT,
        )
        incident_limit_value = self._as_positive_int(
            incident_limit,
            field_name="incident_limit",
            max_value=MAX_DASHBOARD_INCIDENT_LIMIT,
        )
        comparison_window_value = self._as_positive_int(
            comparison_window,
            field_name="comparison_window",
            max_value=MAX_DASHBOARD_COMPARISON_WINDOW,
        )
        kpi_shadow_policy = self._load_kpi_shadow_policy()
        policy_default_window = self._to_int(kpi_shadow_policy.get("default_window"))
        if policy_default_window is None or policy_default_window <= 0:
            policy_default_window = comparison_window_value
        if policy_default_window > MAX_DASHBOARD_KPI_WINDOW:
            policy_default_window = MAX_DASHBOARD_KPI_WINDOW
        if kpi_window is None:
            kpi_window_value = policy_default_window
        else:
            kpi_window_value = self._as_positive_int(
                kpi_window,
                field_name="kpi_window",
                max_value=MAX_DASHBOARD_KPI_WINDOW,
            )
        kpi_domain_value = self._normalize_optional_filter(kpi_domain)
        kpi_status_value = self._normalize_kpi_status_filter(kpi_status)

        supervisor_state = self._load_state()
        journal_rows = self._load_journal()
        event_counts = self._summarize_event_counts(journal_rows)
        worker_activity = self._summarize_worker_activity(journal_rows)
        control_state = self.control_manager.load_control_state()
        agent_operator_learning = self.control_manager.get_agent_operator_learning_payload()
        audit_events = self.control_manager.list_audit_events(
            limit=audit_limit,
            action=audit_action,
            actor=audit_actor,
        )
        loop_metrics = self._extract_loop_metrics(supervisor_state)
        financial_metrics = self._extract_financial_metrics(
            supervisor_state,
            loop_metrics,
        )
        incident_feed = self._build_incident_feed_payload(
            journal_rows,
            limit=incident_limit_value,
            cursor=incident_cursor,
        )
        cycle_summaries = self._extract_cycle_summaries_from_journal(journal_rows)
        cycle_comparison = self._build_cycle_comparison_payload(
            journal_rows,
            window=comparison_window_value,
        )
        kpi_shadow = self._build_kpi_shadow_payload(
            policy=kpi_shadow_policy,
            financial_metrics=financial_metrics,
            loop_metrics=loop_metrics,
            worker_activity=worker_activity,
            incident_feed=incident_feed,
            cycle_summaries=cycle_summaries,
            window=kpi_window_value,
            kpi_domain=kpi_domain_value,
            kpi_status=kpi_status_value,
        )
        mode_lifecycle = {
            "current_mode": control_state.get("mode_current"),
            "target_mode": control_state.get("mode_target"),
            "approval_status": control_state.get("mode_transition_approval_status"),
            "evidence": control_state.get("mode_transition_evidence"),
            "last_decision": control_state.get("mode_transition_last_decision"),
            "last_decision_at": control_state.get("mode_transition_last_decision_at"),
            "last_transition_at": control_state.get(
                "mode_transition_last_transition_at"
            ),
            "last_actor": control_state.get("mode_transition_last_actor"),
            "last_action": control_state.get("mode_transition_last_action"),
            "last_reason": control_state.get("mode_transition_last_reason"),
            "runtime_current_mode": loop_metrics.get("mode_lifecycle_current_mode"),
            "runtime_target_mode": loop_metrics.get("mode_lifecycle_target_mode"),
            "runtime_transition_allowed": loop_metrics.get(
                "mode_lifecycle_transition_allowed"
            ),
            "runtime_transition_reason_codes": loop_metrics.get(
                "mode_lifecycle_transition_reason_codes"
            ),
            "runtime_decision_hash": loop_metrics.get("mode_lifecycle_decision_hash"),
        }
        position_book = self._extract_position_book(supervisor_state)
        game_overview = self._build_game_overview(
            financial_metrics=financial_metrics,
            loop_metrics=loop_metrics,
            position_book=position_book,
            control_state=control_state,
        )

        return {
            "schema_version": RUNTIME_SUPERVISOR_DASHBOARD_SCHEMA_VERSION,
            "generated_at": _utc_now_iso(),
            "supervisor_state": supervisor_state,
            "control_state": control_state,
            "mode_lifecycle": mode_lifecycle,
            "event_counts": event_counts,
            "worker_activity": worker_activity,
            "loop_metrics": loop_metrics,
            "financial_metrics": financial_metrics,
            "agent_operator_learning": agent_operator_learning,
            "recent_journal_events": journal_rows[-events_limit:],
            "recent_operator_actions": audit_events,
            "incident_feed": incident_feed,
            "cycle_comparison": cycle_comparison,
            "kpi_shadow": kpi_shadow,
            "position_book": position_book,
            "game_overview": game_overview,
        }
