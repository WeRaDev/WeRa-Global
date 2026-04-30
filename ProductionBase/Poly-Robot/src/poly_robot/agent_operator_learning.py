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

from .schemas import (
    AGENT_OPERATOR_LEARNING_EVENT_SCHEMA_VERSION,
    AGENT_OPERATOR_LEARNING_STATE_SCHEMA_VERSION,
)

MAX_RECOMMENDATION_HISTORY = 500
MAX_CANDIDATE_HISTORY = 500


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="milliseconds")


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    temp_path: Path | None = None
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
            temp_path = Path(handle.name)
        if temp_path is None:
            raise RuntimeError("Failed to create temporary learning-state file.")
        os.replace(temp_path, path)
    finally:
        if temp_path is not None and temp_path.exists():
            temp_path.unlink()


def _append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True))
        handle.write("\n")


def _as_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _as_int(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _trim_text(value: Any, *, max_length: int) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return f"{text[: max_length - 3]}..."


def _normalize_mode(value: Any) -> str:
    mode = str(value or "advisory").strip().lower()
    if mode not in {"advisory", "strategy"}:
        return "advisory"
    return mode


def _normalize_scenario_name(value: Any) -> str:
    scenario_name = _trim_text(value, max_length=128)
    if not scenario_name:
        return ""
    cleaned = "".join(
        character
        for character in scenario_name
        if character.isalnum() or character in {"_", "-", "."}
    ).strip()
    return cleaned


def _normalize_actions(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    normalized: list[str] = []
    for item in value:
        action = _trim_text(item, max_length=160)
        if not action:
            continue
        normalized.append(action)
        if len(normalized) >= 8:
            break
    return normalized


def _default_metrics() -> dict[str, Any]:
    return {
        "recommendation_count": 0,
        "attributed_count": 0,
        "positive_outcome_count": 0,
        "negative_outcome_count": 0,
        "neutral_outcome_count": 0,
        "outcome_win_rate": 0.0,
        "average_outcome_net_pnl_delta": None,
        "average_outcome_expected_value_delta": None,
    }


def _default_state() -> dict[str, Any]:
    return {
        "schema_version": AGENT_OPERATOR_LEARNING_STATE_SCHEMA_VERSION,
        "updated_at": _utc_now_iso(),
        "recommendation_sequence": 0,
        "candidate_sequence": 0,
        "active_candidate_id": "",
        "recommendations": [],
        "candidates": [],
        "metrics": _default_metrics(),
    }


def _normalize_state(payload: dict[str, Any] | None) -> dict[str, Any]:
    normalized = _default_state()
    if isinstance(payload, dict):
        normalized.update(payload)
    normalized["schema_version"] = AGENT_OPERATOR_LEARNING_STATE_SCHEMA_VERSION
    recommendation_sequence = _as_int(normalized.get("recommendation_sequence"))
    normalized["recommendation_sequence"] = max(0, recommendation_sequence or 0)
    candidate_sequence = _as_int(normalized.get("candidate_sequence"))
    normalized["candidate_sequence"] = max(0, candidate_sequence or 0)
    if not isinstance(normalized.get("recommendations"), list):
        normalized["recommendations"] = []
    if not isinstance(normalized.get("candidates"), list):
        normalized["candidates"] = []
    if not isinstance(normalized.get("metrics"), dict):
        normalized["metrics"] = _default_metrics()
    else:
        metrics = _default_metrics()
        metrics.update(normalized["metrics"])
        normalized["metrics"] = metrics
    normalized["active_candidate_id"] = str(
        normalized.get("active_candidate_id", "")
    ).strip()
    normalized["updated_at"] = _trim_text(
        normalized.get("updated_at", ""), max_length=64
    ) or _utc_now_iso()
    return normalized


class AgentOperatorLearningStore:
    def __init__(
        self,
        *,
        state_path: Path,
        event_log_path: Path,
        outcome_delay_cycles: int = 1,
        max_recommendation_history: int = MAX_RECOMMENDATION_HISTORY,
        max_candidate_history: int = MAX_CANDIDATE_HISTORY,
    ) -> None:
        if outcome_delay_cycles <= 0:
            raise ValueError("outcome_delay_cycles must be > 0")
        if max_recommendation_history <= 0:
            raise ValueError("max_recommendation_history must be > 0")
        if max_candidate_history <= 0:
            raise ValueError("max_candidate_history must be > 0")
        self.state_path = state_path
        self.event_log_path = event_log_path
        self.outcome_delay_cycles = outcome_delay_cycles
        self.max_recommendation_history = max_recommendation_history
        self.max_candidate_history = max_candidate_history
        self.lock_path = self.state_path.with_name(f"{self.state_path.name}.lock")
        self._mutation_lock = threading.RLock()

    @contextmanager
    def _interprocess_lock(self) -> Iterator[None]:
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        with self.lock_path.open("a+", encoding="utf-8") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    def _load_state_unlocked(self) -> dict[str, Any]:
        if not self.state_path.exists():
            return _default_state()
        payload = _read_json(self.state_path)
        if payload.get("schema_version") != AGENT_OPERATOR_LEARNING_STATE_SCHEMA_VERSION:
            raise ValueError("AgentOperator learning state schema version mismatch")
        return _normalize_state(payload)

    def load_state(self) -> dict[str, Any]:
        with self._mutation_lock:
            with self._interprocess_lock():
                return self._load_state_unlocked()

    def _log_event_unlocked(self, *, action: str, details: dict[str, Any]) -> None:
        _append_jsonl(
            self.event_log_path,
            {
                "schema_version": AGENT_OPERATOR_LEARNING_EVENT_SCHEMA_VERSION,
                "timestamp": _utc_now_iso(),
                "action": action,
                "details": details,
            },
        )

    @staticmethod
    def _recompute_metrics(state: dict[str, Any]) -> None:
        recommendations_raw = state.get("recommendations")
        recommendations = (
            recommendations_raw if isinstance(recommendations_raw, list) else []
        )
        attributed = [
            row
            for row in recommendations
            if isinstance(row, dict) and str(row.get("status")) == "attributed"
        ]
        positive = 0
        negative = 0
        neutral = 0
        net_pnl_deltas: list[float] = []
        expected_value_deltas: list[float] = []
        for row in attributed:
            net_delta = _as_float(row.get("outcome_net_pnl_delta"))
            if net_delta is not None:
                net_pnl_deltas.append(net_delta)
            expected_delta = _as_float(row.get("outcome_expected_value_delta"))
            if expected_delta is not None:
                expected_value_deltas.append(expected_delta)
            label = str(row.get("outcome_label", "")).strip().lower()
            if label == "positive":
                positive += 1
            elif label == "negative":
                negative += 1
            else:
                neutral += 1

        attributed_count = len(attributed)
        win_rate = 0.0
        if attributed_count > 0:
            win_rate = round(positive / attributed_count, 6)
        metrics = {
            "recommendation_count": len(recommendations),
            "attributed_count": attributed_count,
            "positive_outcome_count": positive,
            "negative_outcome_count": negative,
            "neutral_outcome_count": neutral,
            "outcome_win_rate": win_rate,
            "average_outcome_net_pnl_delta": (
                round(sum(net_pnl_deltas) / len(net_pnl_deltas), 6)
                if net_pnl_deltas
                else None
            ),
            "average_outcome_expected_value_delta": (
                round(sum(expected_value_deltas) / len(expected_value_deltas), 6)
                if expected_value_deltas
                else None
            ),
        }
        state["metrics"] = metrics

    def _trim_history(self, state: dict[str, Any]) -> None:
        recommendations_raw = state.get("recommendations")
        if isinstance(recommendations_raw, list):
            state["recommendations"] = recommendations_raw[-self.max_recommendation_history :]
        else:
            state["recommendations"] = []
        candidates_raw = state.get("candidates")
        if isinstance(candidates_raw, list):
            state["candidates"] = candidates_raw[-self.max_candidate_history :]
        else:
            state["candidates"] = []

    def _mutate_state(
        self,
        *,
        action: str,
        details: dict[str, Any],
        mutate_state: Callable[[dict[str, Any]], None],
    ) -> dict[str, Any]:
        with self._mutation_lock:
            with self._interprocess_lock():
                state = self._load_state_unlocked()
                mutate_state(state)
                self._trim_history(state)
                self._recompute_metrics(state)
                state["updated_at"] = _utc_now_iso()
                state["schema_version"] = AGENT_OPERATOR_LEARNING_STATE_SCHEMA_VERSION
                _write_json(self.state_path, state)
                self._log_event_unlocked(action=action, details=details)
                return state

    def record_recommendation(
        self,
        *,
        cycle_index: int,
        scenario_name: str,
        mode: str,
        recommendation: dict[str, Any],
        baseline_net_pnl: float | None,
        baseline_expected_value_after_execution_cost: float | None,
    ) -> dict[str, Any]:
        cycle_index_value = _as_int(cycle_index)
        if cycle_index_value is None or cycle_index_value <= 0:
            raise ValueError("cycle_index must be > 0")
        recommendation_status = str(recommendation.get("status", "")).strip().upper()
        if recommendation_status != "OK":
            raise ValueError("recommendation status must be OK")
        recommendation_mode = _normalize_mode(mode)
        scenario_name_value = _normalize_scenario_name(scenario_name)
        recommendation_result: dict[str, Any] = {}

        def _apply(state: dict[str, Any]) -> None:
            recommendation_sequence = int(state.get("recommendation_sequence", 0)) + 1
            recommendation_id = f"rec-{recommendation_sequence:06d}"
            recommendation_entry = {
                "recommendation_id": recommendation_id,
                "sequence": recommendation_sequence,
                "cycle_index": cycle_index_value,
                "scenario_name": scenario_name_value,
                "mode": recommendation_mode,
                "generated_at": _trim_text(
                    recommendation.get("generated_at", ""), max_length=64
                )
                or _utc_now_iso(),
                "summary": _trim_text(recommendation.get("summary", ""), max_length=512),
                "profitability_hypothesis": _trim_text(
                    recommendation.get("profitability_hypothesis", ""),
                    max_length=512,
                ),
                "risk_posture": _trim_text(
                    recommendation.get("risk_posture", "neutral"), max_length=32
                )
                or "neutral",
                "confidence": _as_float(recommendation.get("confidence")),
                "recommended_actions": _normalize_actions(
                    recommendation.get("recommended_actions")
                ),
                "scenario_hint": _normalize_scenario_name(
                    recommendation.get("scenario_hint")
                ),
                "status": "pending_outcome",
                "outcome_due_cycle_index": (
                    cycle_index_value + self.outcome_delay_cycles
                ),
                "baseline_net_pnl": _as_float(baseline_net_pnl),
                "baseline_expected_value_after_execution_cost": _as_float(
                    baseline_expected_value_after_execution_cost
                ),
                "outcome_cycle_index": None,
                "outcome_attributed_at": "",
                "outcome_net_pnl_delta": None,
                "outcome_expected_value_delta": None,
                "outcome_label": "",
            }
            state["recommendation_sequence"] = recommendation_sequence
            recommendations_raw = state.get("recommendations")
            recommendations = (
                recommendations_raw if isinstance(recommendations_raw, list) else []
            )
            recommendations.append(recommendation_entry)
            state["recommendations"] = recommendations
            recommendation_result["recommendation"] = recommendation_entry

            candidate_entry: dict[str, Any] | None = None
            scenario_hint = recommendation_entry.get("scenario_hint", "")
            if recommendation_mode == "strategy" and scenario_hint:
                candidate_sequence = int(state.get("candidate_sequence", 0)) + 1
                candidate_id = f"cand-{candidate_sequence:06d}"
                candidate_entry = {
                    "candidate_id": candidate_id,
                    "sequence": candidate_sequence,
                    "source_recommendation_id": recommendation_id,
                    "source_cycle_index": cycle_index_value,
                    "scenario_name": scenario_hint,
                    "status": "pending",
                    "created_at": _utc_now_iso(),
                    "updated_at": _utc_now_iso(),
                    "applied_at": "",
                    "applied_by": "",
                    "apply_reason": "",
                    "reverted_at": "",
                    "reverted_by": "",
                    "revert_reason": "",
                }
                state["candidate_sequence"] = candidate_sequence
                candidates_raw = state.get("candidates")
                candidates = candidates_raw if isinstance(candidates_raw, list) else []
                candidates.append(candidate_entry)
                state["candidates"] = candidates
            recommendation_result["candidate"] = candidate_entry

        details = {
            "cycle_index": cycle_index_value,
            "mode": recommendation_mode,
            "scenario_name": scenario_name_value,
        }
        self._mutate_state(
            action="recommendation_recorded",
            details=details,
            mutate_state=_apply,
        )
        return recommendation_result

    def attribute_outcomes(
        self,
        *,
        current_cycle_index: int,
        current_net_pnl: float | None,
        current_expected_value_after_execution_cost: float | None,
    ) -> dict[str, Any]:
        cycle_index_value = _as_int(current_cycle_index)
        if cycle_index_value is None or cycle_index_value <= 0:
            raise ValueError("current_cycle_index must be > 0")
        current_net_pnl_value = _as_float(current_net_pnl)
        current_expected_value = _as_float(current_expected_value_after_execution_cost)
        result = {"attributed_count": 0, "attributed_recommendation_ids": []}

        def _apply(state: dict[str, Any]) -> None:
            recommendations_raw = state.get("recommendations")
            recommendations = (
                recommendations_raw if isinstance(recommendations_raw, list) else []
            )
            attributed_ids: list[str] = []
            attributed_count = 0
            attributed_at = _utc_now_iso()
            for row in recommendations:
                if not isinstance(row, dict):
                    continue
                if str(row.get("status", "")).strip() != "pending_outcome":
                    continue
                outcome_due_cycle_index = _as_int(row.get("outcome_due_cycle_index"))
                if outcome_due_cycle_index is None or outcome_due_cycle_index > cycle_index_value:
                    continue
                baseline_net_pnl = _as_float(row.get("baseline_net_pnl"))
                net_pnl_delta = None
                if baseline_net_pnl is not None and current_net_pnl_value is not None:
                    net_pnl_delta = round(current_net_pnl_value - baseline_net_pnl, 6)
                baseline_expected_value = _as_float(
                    row.get("baseline_expected_value_after_execution_cost")
                )
                expected_value_delta = None
                if (
                    baseline_expected_value is not None
                    and current_expected_value is not None
                ):
                    expected_value_delta = round(
                        current_expected_value - baseline_expected_value, 6
                    )
                outcome_label = "neutral"
                if net_pnl_delta is not None:
                    if net_pnl_delta > 0:
                        outcome_label = "positive"
                    elif net_pnl_delta < 0:
                        outcome_label = "negative"
                row["status"] = "attributed"
                row["outcome_cycle_index"] = cycle_index_value
                row["outcome_attributed_at"] = attributed_at
                row["outcome_net_pnl_delta"] = net_pnl_delta
                row["outcome_expected_value_delta"] = expected_value_delta
                row["outcome_label"] = outcome_label
                recommendation_id = str(row.get("recommendation_id", "")).strip()
                if recommendation_id:
                    attributed_ids.append(recommendation_id)
                attributed_count += 1
            result["attributed_count"] = attributed_count
            result["attributed_recommendation_ids"] = attributed_ids

        self._mutate_state(
            action="recommendation_outcomes_attributed",
            details={
                "current_cycle_index": cycle_index_value,
                "current_net_pnl": current_net_pnl_value,
                "current_expected_value_after_execution_cost": current_expected_value,
            },
            mutate_state=_apply,
        )
        return result

    def apply_candidate(
        self, *, candidate_id: str, actor: str, reason: str = ""
    ) -> dict[str, Any]:
        candidate_id_value = _trim_text(candidate_id, max_length=64)
        if not candidate_id_value:
            raise ValueError("candidate_id must not be empty")
        actor_value = _trim_text(actor, max_length=80) or "operator"
        reason_value = _trim_text(reason, max_length=256)
        result: dict[str, Any] = {}

        def _apply(state: dict[str, Any]) -> None:
            candidates_raw = state.get("candidates")
            candidates = candidates_raw if isinstance(candidates_raw, list) else []
            selected_index = None
            for index, candidate in enumerate(candidates):
                if not isinstance(candidate, dict):
                    continue
                if str(candidate.get("candidate_id", "")).strip() == candidate_id_value:
                    selected_index = index
                    break
            if selected_index is None:
                raise ValueError(f"candidate_id not found: {candidate_id_value}")
            selected_candidate = candidates[selected_index]
            if str(selected_candidate.get("status", "")).strip() == "reverted":
                raise ValueError("candidate has been reverted and cannot be re-applied")
            updated_at = _utc_now_iso()
            active_candidate_id = str(state.get("active_candidate_id", "")).strip()
            if active_candidate_id and active_candidate_id != candidate_id_value:
                for candidate in candidates:
                    if not isinstance(candidate, dict):
                        continue
                    if str(candidate.get("candidate_id", "")).strip() != active_candidate_id:
                        continue
                    candidate["status"] = "superseded"
                    candidate["updated_at"] = updated_at
                    break
            selected_candidate["status"] = "active"
            selected_candidate["updated_at"] = updated_at
            selected_candidate["applied_at"] = updated_at
            selected_candidate["applied_by"] = actor_value
            selected_candidate["apply_reason"] = reason_value
            state["active_candidate_id"] = candidate_id_value
            result.update(selected_candidate)

        self._mutate_state(
            action="candidate_applied",
            details={
                "candidate_id": candidate_id_value,
                "actor": actor_value,
                "reason": reason_value,
            },
            mutate_state=_apply,
        )
        return result

    def revert_candidate(
        self, *, candidate_id: str, actor: str, reason: str = ""
    ) -> dict[str, Any]:
        actor_value = _trim_text(actor, max_length=80) or "operator"
        reason_value = _trim_text(reason, max_length=256)
        candidate_id_value = _trim_text(candidate_id, max_length=64)
        result: dict[str, Any] = {}

        def _apply(state: dict[str, Any]) -> None:
            nonlocal candidate_id_value
            candidates_raw = state.get("candidates")
            candidates = candidates_raw if isinstance(candidates_raw, list) else []
            active_candidate_id = str(state.get("active_candidate_id", "")).strip()
            if not candidate_id_value:
                candidate_id_value = active_candidate_id
            if not candidate_id_value:
                raise ValueError("candidate_id must not be empty")
            selected_index = None
            for index, candidate in enumerate(candidates):
                if not isinstance(candidate, dict):
                    continue
                if str(candidate.get("candidate_id", "")).strip() == candidate_id_value:
                    selected_index = index
                    break
            if selected_index is None:
                raise ValueError(f"candidate_id not found: {candidate_id_value}")
            selected_candidate = candidates[selected_index]
            updated_at = _utc_now_iso()
            selected_candidate["status"] = "reverted"
            selected_candidate["updated_at"] = updated_at
            selected_candidate["reverted_at"] = updated_at
            selected_candidate["reverted_by"] = actor_value
            selected_candidate["revert_reason"] = reason_value
            if active_candidate_id == candidate_id_value:
                state["active_candidate_id"] = ""
            result.update(selected_candidate)

        self._mutate_state(
            action="candidate_reverted",
            details={
                "candidate_id": candidate_id_value,
                "actor": actor_value,
                "reason": reason_value,
            },
            mutate_state=_apply,
        )
        return result

    def list_candidates(self, *, limit: int = 20) -> list[dict[str, Any]]:
        payload = self.build_dashboard_payload(candidate_limit=limit, recommendation_limit=1)
        candidates = payload.get("candidates")
        if isinstance(candidates, list):
            return candidates
        return []

    def build_dashboard_payload(
        self,
        *,
        candidate_limit: int = 20,
        recommendation_limit: int = 20,
    ) -> dict[str, Any]:
        if candidate_limit <= 0:
            raise ValueError("candidate_limit must be > 0")
        if recommendation_limit <= 0:
            raise ValueError("recommendation_limit must be > 0")
        state = self.load_state()
        candidates_raw = state.get("candidates")
        recommendations_raw = state.get("recommendations")
        candidates = candidates_raw if isinstance(candidates_raw, list) else []
        recommendations = (
            recommendations_raw if isinstance(recommendations_raw, list) else []
        )
        candidate_status_counts = {
            "pending": 0,
            "active": 0,
            "superseded": 0,
            "reverted": 0,
        }
        for row in candidates:
            if not isinstance(row, dict):
                continue
            status = str(row.get("status", "")).strip().lower()
            if status in candidate_status_counts:
                candidate_status_counts[status] += 1
        return {
            "schema_version": AGENT_OPERATOR_LEARNING_STATE_SCHEMA_VERSION,
            "updated_at": state.get("updated_at"),
            "active_candidate_id": state.get("active_candidate_id"),
            "recommendation_sequence": state.get("recommendation_sequence"),
            "candidate_sequence": state.get("candidate_sequence"),
            "metrics": state.get("metrics"),
            "candidate_status_counts": candidate_status_counts,
            "candidates": candidates[-candidate_limit:],
            "recent_recommendations": recommendations[-recommendation_limit:],
        }
