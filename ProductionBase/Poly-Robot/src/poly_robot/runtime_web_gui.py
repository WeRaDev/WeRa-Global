from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable
import json
import os
import tempfile
import threading

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
        self._mutation_lock = threading.RLock()

    def load_control_state(self) -> dict[str, Any]:
        with self._mutation_lock:
            if not self.control_state_path.exists():
                return _default_control_state()
            payload = _read_json(self.control_state_path)
            if (
                payload.get("schema_version")
                != RUNTIME_OPERATOR_CONTROL_STATE_SCHEMA_VERSION
            ):
                raise ValueError("Operator control state schema version mismatch")
            return payload

    def _mutate_state(
        self,
        *,
        action: str,
        actor: str,
        details: dict[str, Any],
        mutate_state: Callable[[dict[str, Any]], None],
    ) -> dict[str, Any]:
        with self._mutation_lock:
            state = self.load_control_state()
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

    def annotate(self, *, actor: str, note: str) -> dict[str, Any]:
        cleaned_note = note.strip()
        if not cleaned_note:
            raise ValueError("note must not be empty")

        def _apply(state: dict[str, Any]) -> None:
            state["last_annotation"] = cleaned_note

        return self._mutate_state(
            action="incident_annotation",
            actor=actor,
            details={"note": cleaned_note},
            mutate_state=_apply,
        )

    def list_audit_events(
        self,
        *,
        limit: int = 100,
        action: str | None = None,
        actor: str | None = None,
    ) -> list[dict[str, Any]]:
        if limit <= 0:
            raise ValueError("limit must be > 0")
        with self._mutation_lock:
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
        return filtered[-limit:]


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

        fill_rate = RuntimeDashboardService._ratio(
            RuntimeDashboardService._to_float(filled_trade_count),
            RuntimeDashboardService._to_float(risk_allowed_count),
        )
        average_execution_cost_per_fill = RuntimeDashboardService._ratio(
            total_execution_cost,
            RuntimeDashboardService._to_float(filled_trade_count),
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
        }

    @staticmethod
    def _as_positive_int(value: Any, *, field_name: str) -> int:
        try:
            parsed = int(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{field_name} must be an integer") from exc
        if parsed <= 0:
            raise ValueError(f"{field_name} must be > 0")
        return parsed

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
            by_cycle_index[cycle_index] = {
                "cycle_index": cycle_index,
                "timestamp": row.get("timestamp"),
                "selected_scenario": details.get("selected_scenario"),
                "control_version": details.get("control_version"),
                "events": details.get("events"),
                "risk_allowed_count": details.get("risk_allowed_count"),
                "filled_trade_count": details.get("filled_trade_count"),
                "exit_candidate_count": details.get("exit_candidate_count"),
                "confirmed_exit_count": details.get("confirmed_exit_count"),
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
                    "exit_candidate_count": RuntimeDashboardService._delta(
                        previous.get("exit_candidate_count"),
                        entry.get("exit_candidate_count"),
                    ),
                    "confirmed_exit_count": RuntimeDashboardService._delta(
                        previous.get("confirmed_exit_count"),
                        entry.get("confirmed_exit_count"),
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
        limit_value = self._as_positive_int(limit, field_name="incident_limit")
        journal_rows = self._load_journal()
        return self._build_incident_feed_payload(
            journal_rows,
            limit=limit_value,
            cursor=cursor,
        )

    def build_cycle_comparison(self, *, window: int = 10) -> dict[str, Any]:
        window_value = self._as_positive_int(window, field_name="comparison_window")
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
    ) -> dict[str, Any]:
        events_limit = self._as_positive_int(
            recent_events_limit, field_name="recent_events_limit"
        )
        audit_limit = self._as_positive_int(
            recent_audit_limit, field_name="recent_audit_limit"
        )
        incident_limit_value = self._as_positive_int(
            incident_limit, field_name="incident_limit"
        )
        comparison_window_value = self._as_positive_int(
            comparison_window,
            field_name="comparison_window",
        )

        supervisor_state = self._load_state()
        journal_rows = self._load_journal()
        event_counts = self._summarize_event_counts(journal_rows)
        worker_activity = self._summarize_worker_activity(journal_rows)
        control_state = self.control_manager.load_control_state()
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
        cycle_comparison = self._build_cycle_comparison_payload(
            journal_rows,
            window=comparison_window_value,
        )

        return {
            "schema_version": RUNTIME_SUPERVISOR_DASHBOARD_SCHEMA_VERSION,
            "generated_at": _utc_now_iso(),
            "supervisor_state": supervisor_state,
            "control_state": control_state,
            "event_counts": event_counts,
            "worker_activity": worker_activity,
            "loop_metrics": loop_metrics,
            "financial_metrics": financial_metrics,
            "recent_journal_events": journal_rows[-events_limit:],
            "recent_operator_actions": audit_events,
            "incident_feed": incident_feed,
            "cycle_comparison": cycle_comparison,
        }
