from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any
import json

from .schemas import (
    RUNTIME_OPERATOR_ACTION_SCHEMA_VERSION,
    RUNTIME_OPERATOR_CONTROL_STATE_SCHEMA_VERSION,
    RUNTIME_SUPERVISOR_DASHBOARD_SCHEMA_VERSION,
    RUNTIME_SUPERVISOR_JOURNAL_EVENT_SCHEMA_VERSION,
    RUNTIME_SUPERVISOR_STATE_SCHEMA_VERSION,
)


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="milliseconds")


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []

    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rows.append(json.loads(line))
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
        "selected_scenario": "baseline",
        "last_annotation": "",
    }


class OperatorControlManager:
    def __init__(self, *, control_state_path: Path, audit_path: Path) -> None:
        self.control_state_path = control_state_path
        self.audit_path = audit_path

    def load_control_state(self) -> dict[str, Any]:
        if not self.control_state_path.exists():
            return _default_control_state()
        payload = _read_json(self.control_state_path)
        if payload.get("schema_version") != RUNTIME_OPERATOR_CONTROL_STATE_SCHEMA_VERSION:
            raise ValueError("Operator control state schema version mismatch")
        return payload

    def _mutate_state(
        self,
        *,
        action: str,
        actor: str,
        details: dict[str, Any],
    ) -> dict[str, Any]:
        state = self.load_control_state()
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

    def set_paused(self, *, paused: bool, actor: str, reason: str = "") -> dict[str, Any]:
        state = self.load_control_state()
        state["paused"] = paused
        if reason:
            state["pause_reason"] = reason
        _write_json(self.control_state_path, state)
        return self._mutate_state(
            action="pause" if paused else "resume",
            actor=actor,
            details={"paused": paused, "reason": reason},
        )

    def request_restart(self, *, actor: str, reason: str = "") -> dict[str, Any]:
        state = self.load_control_state()
        state["restart_requested"] = True
        if reason:
            state["restart_reason"] = reason
        _write_json(self.control_state_path, state)
        return self._mutate_state(
            action="graceful_restart_requested",
            actor=actor,
            details={"reason": reason},
        )

    def acknowledge_restart(self, *, actor: str, note: str = "") -> dict[str, Any]:
        state = self.load_control_state()
        state["restart_requested"] = False
        if note:
            state["restart_ack_note"] = note
        _write_json(self.control_state_path, state)
        return self._mutate_state(
            action="graceful_restart_acknowledged",
            actor=actor,
            details={"note": note},
        )

    def set_scenario(self, *, actor: str, scenario_name: str) -> dict[str, Any]:
        if not scenario_name.strip():
            raise ValueError("scenario_name must not be empty")
        state = self.load_control_state()
        state["selected_scenario"] = scenario_name.strip()
        _write_json(self.control_state_path, state)
        return self._mutate_state(
            action="scenario_selected",
            actor=actor,
            details={"selected_scenario": scenario_name.strip()},
        )

    def annotate(self, *, actor: str, note: str) -> dict[str, Any]:
        cleaned_note = note.strip()
        if not cleaned_note:
            raise ValueError("note must not be empty")
        state = self.load_control_state()
        state["last_annotation"] = cleaned_note
        _write_json(self.control_state_path, state)
        return self._mutate_state(
            action="incident_annotation",
            actor=actor,
            details={"note": cleaned_note},
        )

    def list_audit_events(self, *, limit: int = 100) -> list[dict[str, Any]]:
        if limit <= 0:
            raise ValueError("limit must be > 0")
        rows = _read_jsonl(self.audit_path)
        return rows[-limit:]


class RuntimeDashboardService:
    def __init__(
        self,
        *,
        state_path: Path,
        journal_path: Path,
        control_manager: OperatorControlManager,
    ) -> None:
        self.state_path = state_path
        self.journal_path = journal_path
        self.control_manager = control_manager

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
            if row.get("schema_version") != RUNTIME_SUPERVISOR_JOURNAL_EVENT_SCHEMA_VERSION:
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
    def _summarize_worker_activity(journal_rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
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
    def _extract_loop_metrics(supervisor_state: dict[str, Any] | None) -> dict[str, Any]:
        if not supervisor_state:
            return {}
        metrics: dict[str, Any] = {}
        worker_results = supervisor_state.get("worker_results")
        if not isinstance(worker_results, list):
            return metrics

        for worker_result in worker_results:
            worker_name = worker_result.get("worker_name")
            last_metadata = worker_result.get("last_metadata") or {}
            if worker_name == "test_token_loop" and isinstance(last_metadata, dict):
                metrics = {
                    "events": last_metadata.get("events"),
                    "risk_allowed_count": last_metadata.get("risk_allowed_count"),
                    "filled_trade_count": last_metadata.get("filled_trade_count"),
                    "partial_fill_count": last_metadata.get("partial_fill_count"),
                    "exit_candidate_count": last_metadata.get("exit_candidate_count"),
                    "confirmed_exit_count": last_metadata.get("confirmed_exit_count"),
                    "total_execution_cost": last_metadata.get("total_execution_cost"),
                    "result_hash": last_metadata.get("result_hash"),
                }
                break
        return metrics

    def build_dashboard_payload(
        self,
        *,
        recent_events_limit: int = 200,
        recent_audit_limit: int = 100,
    ) -> dict[str, Any]:
        if recent_events_limit <= 0:
            raise ValueError("recent_events_limit must be > 0")
        if recent_audit_limit <= 0:
            raise ValueError("recent_audit_limit must be > 0")

        supervisor_state = self._load_state()
        journal_rows = self._load_journal()
        event_counts = self._summarize_event_counts(journal_rows)
        worker_activity = self._summarize_worker_activity(journal_rows)
        control_state = self.control_manager.load_control_state()
        audit_events = self.control_manager.list_audit_events(limit=recent_audit_limit)
        loop_metrics = self._extract_loop_metrics(supervisor_state)

        return {
            "schema_version": RUNTIME_SUPERVISOR_DASHBOARD_SCHEMA_VERSION,
            "generated_at": _utc_now_iso(),
            "supervisor_state": supervisor_state,
            "control_state": control_state,
            "event_counts": event_counts,
            "worker_activity": worker_activity,
            "loop_metrics": loop_metrics,
            "recent_journal_events": journal_rows[-recent_events_limit:],
            "recent_operator_actions": audit_events,
        }
