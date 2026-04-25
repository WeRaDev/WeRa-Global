from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Sequence
import json
import time

from .schemas import (
    RUNTIME_SUPERVISOR_JOURNAL_EVENT_SCHEMA_VERSION,
    RUNTIME_SUPERVISOR_STATE_SCHEMA_VERSION,
)


HeartbeatEmitter = Callable[[str, dict[str, Any] | None], None]
WorkerHandler = Callable[[HeartbeatEmitter], dict[str, Any] | None]


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="milliseconds")


@dataclass(frozen=True)
class WorkerSpec:
    name: str
    run: WorkerHandler
    max_retries: int = 2
    retry_backoff_seconds: float = 1.0
    heartbeat_timeout_seconds: float = 30.0

    def __post_init__(self) -> None:
        if self.max_retries < 0:
            raise ValueError("max_retries must be >= 0")
        if self.retry_backoff_seconds < 0:
            raise ValueError("retry_backoff_seconds must be >= 0")
        if self.heartbeat_timeout_seconds <= 0:
            raise ValueError("heartbeat_timeout_seconds must be > 0")


@dataclass
class WorkerAttempt:
    attempt_number: int
    status: str
    failure_reason: str | None
    duration_seconds: float
    heartbeat_count: int
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkerRunResult:
    worker_name: str
    status: str
    attempts: list[WorkerAttempt]
    final_failure_reason: str | None
    last_metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def attempt_count(self) -> int:
        return len(self.attempts)

    @property
    def retry_count(self) -> int:
        return max(0, self.attempt_count - 1)

    def as_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["attempt_count"] = self.attempt_count
        payload["retry_count"] = self.retry_count
        return payload


class RunJournal:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, event_type: str, payload: dict[str, Any] | None = None) -> None:
        entry = {
            "schema_version": RUNTIME_SUPERVISOR_JOURNAL_EVENT_SCHEMA_VERSION,
            "timestamp": _utc_now_iso(),
            "event_type": event_type,
            "payload": payload or {},
        }
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, sort_keys=True))
            handle.write("\n")


class StateSnapshotStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, snapshot: dict[str, Any]) -> None:
        with self.path.open("w", encoding="utf-8") as handle:
            json.dump(snapshot, handle, indent=2, sort_keys=True)


class RuntimeSupervisor:
    def __init__(
        self,
        *,
        journal_path: Path,
        state_path: Path,
        sleep_fn: Callable[[float], None] | None = None,
        monotonic_fn: Callable[[], float] | None = None,
    ) -> None:
        self._journal = RunJournal(journal_path)
        self._state_store = StateSnapshotStore(state_path)
        self._sleep_fn = sleep_fn or time.sleep
        self._monotonic_fn = monotonic_fn or time.monotonic

    def _run_worker_once(
        self,
        worker: WorkerSpec,
        *,
        cycle_index: int,
        attempt_number: int,
    ) -> WorkerAttempt:
        started = self._monotonic_fn()
        heartbeat_count = 0
        last_heartbeat_time: float | None = None
        metadata: dict[str, Any] = {}
        failure_reason: str | None = None

        self._journal.append(
            "worker_attempt_started",
            {
                "cycle_index": cycle_index,
                "worker_name": worker.name,
                "attempt_number": attempt_number,
            },
        )

        def emit_heartbeat(stage: str, details: dict[str, Any] | None = None) -> None:
            nonlocal heartbeat_count, last_heartbeat_time
            heartbeat_count += 1
            last_heartbeat_time = self._monotonic_fn()
            payload = {
                "cycle_index": cycle_index,
                "worker_name": worker.name,
                "attempt_number": attempt_number,
                "stage": stage,
            }
            if details:
                payload["details"] = details
            self._journal.append("worker_heartbeat", payload)

        try:
            run_metadata = worker.run(emit_heartbeat)
            if isinstance(run_metadata, dict):
                metadata = run_metadata
            elif run_metadata is not None:
                metadata = {"result": run_metadata}
        except Exception as exc:  # pragma: no cover - exception text is non-deterministic
            failure_reason = f"exception:{exc.__class__.__name__}:{exc}"
        else:
            if heartbeat_count == 0:
                failure_reason = "missing_heartbeat"
            elif last_heartbeat_time is not None:
                heartbeat_age = self._monotonic_fn() - last_heartbeat_time
                if heartbeat_age > worker.heartbeat_timeout_seconds:
                    failure_reason = f"stale_heartbeat:{heartbeat_age:.3f}s"

        status = "SUCCESS" if failure_reason is None else "FAILED"
        duration_seconds = round(self._monotonic_fn() - started, 6)
        attempt = WorkerAttempt(
            attempt_number=attempt_number,
            status=status,
            failure_reason=failure_reason,
            duration_seconds=duration_seconds,
            heartbeat_count=heartbeat_count,
            metadata=metadata,
        )
        self._journal.append(
            "worker_attempt_completed",
            {
                "cycle_index": cycle_index,
                "worker_name": worker.name,
                "attempt_number": attempt_number,
                "status": status,
                "failure_reason": failure_reason,
                "heartbeat_count": heartbeat_count,
                "duration_seconds": duration_seconds,
            },
        )
        return attempt

    def _run_worker_with_retries(self, worker: WorkerSpec, *, cycle_index: int) -> WorkerRunResult:
        attempts: list[WorkerAttempt] = []
        final_failure_reason: str | None = None
        last_metadata: dict[str, Any] = {}
        max_attempts = worker.max_retries + 1

        for attempt_number in range(1, max_attempts + 1):
            attempt = self._run_worker_once(worker, cycle_index=cycle_index, attempt_number=attempt_number)
            attempts.append(attempt)
            last_metadata = attempt.metadata
            if attempt.status == "SUCCESS":
                final_failure_reason = None
                break

            final_failure_reason = attempt.failure_reason
            if attempt_number < max_attempts:
                backoff_seconds = round(
                    worker.retry_backoff_seconds * (2 ** (attempt_number - 1)),
                    6,
                )
                self._journal.append(
                    "worker_retry_scheduled",
                    {
                        "cycle_index": cycle_index,
                        "worker_name": worker.name,
                        "attempt_number": attempt_number,
                        "next_attempt_number": attempt_number + 1,
                        "backoff_seconds": backoff_seconds,
                    },
                )
                self._sleep_fn(backoff_seconds)

        status = "SUCCESS" if attempts and attempts[-1].status == "SUCCESS" else "FAILED"
        return WorkerRunResult(
            worker_name=worker.name,
            status=status,
            attempts=attempts,
            final_failure_reason=final_failure_reason,
            last_metadata=last_metadata,
        )

    def run_cycle(self, worker_specs: Sequence[WorkerSpec], *, cycle_index: int) -> dict[str, Any]:
        if not worker_specs:
            raise ValueError("worker_specs must not be empty")

        self._journal.append(
            "cycle_started",
            {"cycle_index": cycle_index, "worker_count": len(worker_specs)},
        )

        results = [self._run_worker_with_retries(worker, cycle_index=cycle_index) for worker in worker_specs]
        failed_workers = [result.worker_name for result in results if result.status == "FAILED"]
        cycle_status = "SUCCESS" if not failed_workers else "FAILED"
        snapshot = {
            "schema_version": RUNTIME_SUPERVISOR_STATE_SCHEMA_VERSION,
            "generated_at": _utc_now_iso(),
            "cycle_index": cycle_index,
            "status": cycle_status,
            "worker_count": len(worker_specs),
            "failed_workers": failed_workers,
            "worker_results": [result.as_dict() for result in results],
        }
        self._state_store.write(snapshot)

        self._journal.append(
            "cycle_completed",
            {
                "cycle_index": cycle_index,
                "status": cycle_status,
                "failed_workers": failed_workers,
            },
        )
        return snapshot

    def run(
        self,
        worker_specs: Sequence[WorkerSpec],
        *,
        cycles: int = 1,
        stop_on_failure: bool = True,
    ) -> dict[str, Any]:
        if cycles <= 0:
            raise ValueError("cycles must be >= 1")

        snapshots: list[dict[str, Any]] = []
        for cycle_index in range(1, cycles + 1):
            snapshot = self.run_cycle(worker_specs, cycle_index=cycle_index)
            snapshots.append(snapshot)
            if stop_on_failure and snapshot["status"] == "FAILED":
                break

        overall_status = "SUCCESS" if snapshots and all(s["status"] == "SUCCESS" for s in snapshots) else "FAILED"
        return {
            "schema_version": RUNTIME_SUPERVISOR_STATE_SCHEMA_VERSION,
            "generated_at": _utc_now_iso(),
            "cycles_requested": cycles,
            "cycles_completed": len(snapshots),
            "overall_status": overall_status,
            "last_snapshot": snapshots[-1] if snapshots else None,
        }
