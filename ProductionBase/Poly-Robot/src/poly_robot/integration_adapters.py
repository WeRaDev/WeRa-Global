from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Literal
import json
import time

from .contracts import MarketEvent
from .paper_execution import ExecutionIntent, ExecutionResult


IngestionStatus = Literal["OK", "DEGRADED", "FAILED"]


@dataclass(frozen=True)
class IngestionBatch:
    status: IngestionStatus
    events: list[MarketEvent]
    reasons: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


class HistoricalIngestionAdapter:
    def __init__(
        self,
        *,
        max_retry_attempts: int = 1,
        retry_backoff_seconds: float = 0.25,
        max_invalid_rows: int = 0,
        deduplicate_event_ids: bool = True,
        fail_on_monotonic_violation: bool = True,
        sleep_fn: Callable[[float], None] | None = None,
        monotonic_fn: Callable[[], float] | None = None,
    ) -> None:
        if max_retry_attempts < 0:
            raise ValueError("max_retry_attempts must be >= 0")
        if retry_backoff_seconds < 0:
            raise ValueError("retry_backoff_seconds must be >= 0")
        if max_invalid_rows < 0:
            raise ValueError("max_invalid_rows must be >= 0")
        self.max_retry_attempts = max_retry_attempts
        self.retry_backoff_seconds = retry_backoff_seconds
        self.max_invalid_rows = max_invalid_rows
        self.deduplicate_event_ids = deduplicate_event_ids
        self.fail_on_monotonic_violation = fail_on_monotonic_violation
        self._sleep_fn = sleep_fn or time.sleep
        self._monotonic_fn = monotonic_fn or time.monotonic

    def _load_once(self, path: Path, *, timeout_seconds: float | None, attempt_number: int) -> IngestionBatch:
        if timeout_seconds is not None and timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be > 0 when provided")

        started = self._monotonic_fn()
        events: list[MarketEvent] = []
        seen_event_ids: set[str] = set()
        total_rows = 0
        invalid_rows = 0
        duplicate_rows = 0
        monotonic_violations = 0
        previous_timestamp: str | None = None

        try:
            with path.open("r", encoding="utf-8") as handle:
                for line_number, raw_line in enumerate(handle, start=1):
                    total_rows += 1
                    if timeout_seconds is not None and (self._monotonic_fn() - started) > timeout_seconds:
                        raise TimeoutError("ingestion_timeout")

                    line = raw_line.strip()
                    if not line:
                        continue
                    try:
                        payload = json.loads(line)
                        event = MarketEvent.from_dict(payload)
                    except Exception:
                        invalid_rows += 1
                        if invalid_rows > self.max_invalid_rows:
                            return IngestionBatch(
                                status="FAILED",
                                events=[],
                                reasons=("invalid_row_budget_exceeded",),
                                metadata={
                                    "attempt_number": attempt_number,
                                    "line_number": line_number,
                                    "total_rows": total_rows,
                                    "invalid_rows": invalid_rows,
                                    "max_invalid_rows": self.max_invalid_rows,
                                },
                            )
                        continue

                    if previous_timestamp is not None and event.timestamp < previous_timestamp:
                        monotonic_violations += 1
                        if self.fail_on_monotonic_violation:
                            return IngestionBatch(
                                status="FAILED",
                                events=[],
                                reasons=("non_monotonic_timestamp",),
                                metadata={
                                    "attempt_number": attempt_number,
                                    "line_number": line_number,
                                    "previous_timestamp": previous_timestamp,
                                    "current_timestamp": event.timestamp,
                                    "total_rows": total_rows,
                                },
                            )

                    if previous_timestamp is None:
                        previous_timestamp = event.timestamp
                    else:
                        previous_timestamp = max(previous_timestamp, event.timestamp)
                    if self.deduplicate_event_ids and event.event_id in seen_event_ids:
                        duplicate_rows += 1
                        continue

                    seen_event_ids.add(event.event_id)
                    events.append(event)
        except OSError:
            return IngestionBatch(
                status="FAILED",
                events=[],
                reasons=("source_unavailable",),
                metadata={
                    "attempt_number": attempt_number,
                    "path": str(path),
                },
            )
        except TimeoutError:
            return IngestionBatch(
                status="FAILED",
                events=[],
                reasons=("ingestion_timeout",),
                metadata={
                    "attempt_number": attempt_number,
                    "path": str(path),
                    "timeout_seconds": timeout_seconds,
                },
            )

        reasons: list[str] = []
        status: IngestionStatus = "OK"
        if invalid_rows > 0:
            reasons.append("invalid_rows_skipped")
            status = "DEGRADED"
        if duplicate_rows > 0:
            reasons.append("duplicate_rows_skipped")
            status = "DEGRADED"
        if monotonic_violations > 0:
            reasons.append("non_monotonic_rows_detected")
            status = "DEGRADED"

        return IngestionBatch(
            status=status,
            events=events,
            reasons=tuple(reasons),
            metadata={
                "attempt_number": attempt_number,
                "total_rows": total_rows,
                "valid_rows": len(events),
                "invalid_rows": invalid_rows,
                "duplicate_rows": duplicate_rows,
                "monotonic_violations": monotonic_violations,
                "deduplicate_event_ids": self.deduplicate_event_ids,
                "fail_on_monotonic_violation": self.fail_on_monotonic_violation,
            },
        )

    def load_jsonl(self, path: Path, *, timeout_seconds: float | None = None) -> IngestionBatch:
        max_attempts = self.max_retry_attempts + 1
        last_failure: IngestionBatch | None = None
        for attempt_number in range(1, max_attempts + 1):
            outcome = self._load_once(path, timeout_seconds=timeout_seconds, attempt_number=attempt_number)
            if outcome.status != "FAILED":
                return outcome

            last_failure = outcome
            if outcome.reasons and outcome.reasons[0] in (
                "invalid_row_budget_exceeded",
                "non_monotonic_timestamp",
            ):
                return outcome

            if attempt_number < max_attempts:
                backoff_seconds = self.retry_backoff_seconds * (2 ** (attempt_number - 1))
                self._sleep_fn(backoff_seconds)

        return last_failure or IngestionBatch(
            status="FAILED",
            events=[],
            reasons=("ingestion_failed",),
            metadata={"path": str(path)},
        )


def _clone_execution_result(
    result: ExecutionResult,
    *,
    gateway_metadata: dict[str, Any],
    extra_reasons: tuple[str, ...] = (),
) -> ExecutionResult:
    metadata = dict(result.metadata)
    metadata["execution_gateway"] = gateway_metadata
    reasons = tuple(dict.fromkeys(result.reasons + extra_reasons))
    return ExecutionResult(
        status=result.status,
        requested_notional=result.requested_notional,
        filled_notional=result.filled_notional,
        reference_price=result.reference_price,
        fill_price=result.fill_price,
        slippage_bps=result.slippage_bps,
        fee_paid=result.fee_paid,
        slippage_cost=result.slippage_cost,
        total_execution_cost=result.total_execution_cost,
        reasons=reasons,
        metadata=metadata,
    )


class ExecutionGatewayAdapter:
    def __init__(
        self,
        *,
        execute_fn: Callable[..., ExecutionResult],
        max_retry_attempts: int = 1,
        retry_backoff_seconds: float = 0.25,
        timeout_seconds: float = 2.0,
        sleep_fn: Callable[[float], None] | None = None,
        monotonic_fn: Callable[[], float] | None = None,
    ) -> None:
        if max_retry_attempts < 0:
            raise ValueError("max_retry_attempts must be >= 0")
        if retry_backoff_seconds < 0:
            raise ValueError("retry_backoff_seconds must be >= 0")
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be > 0")
        self.execute_fn = execute_fn
        self.max_retry_attempts = max_retry_attempts
        self.retry_backoff_seconds = retry_backoff_seconds
        self.timeout_seconds = timeout_seconds
        self._sleep_fn = sleep_fn or time.sleep
        self._monotonic_fn = monotonic_fn or time.monotonic
        self._idempotency_cache: dict[str, ExecutionResult] = {}

    def _degraded_result(
        self,
        *,
        intent: ExecutionIntent,
        idempotency_key: str,
        attempt_count: int,
        failure_reason: str,
    ) -> ExecutionResult:
        return ExecutionResult(
            status="REJECTED",
            requested_notional=float(intent.requested_notional),
            filled_notional=0.0,
            reference_price=float(intent.reference_price),
            fill_price=None,
            slippage_bps=0,
            reasons=("execution_gateway_degraded", failure_reason),
            metadata={
                "execution_gateway": {
                    "attempt_count": attempt_count,
                    "max_attempts": self.max_retry_attempts + 1,
                    "timeout_seconds": self.timeout_seconds,
                    "idempotency_key": idempotency_key,
                    "degraded_mode": True,
                }
            },
        )

    def execute(self, *, event: MarketEvent, intent: ExecutionIntent, idempotency_key: str) -> ExecutionResult:
        if not idempotency_key.strip():
            raise ValueError("idempotency_key must not be empty")
        if idempotency_key in self._idempotency_cache:
            return self._idempotency_cache[idempotency_key]

        max_attempts = self.max_retry_attempts + 1
        last_failure_reason = "execution_gateway_unknown"
        for attempt_number in range(1, max_attempts + 1):
            started = self._monotonic_fn()
            try:
                raw_result = self.execute_fn(event=event, intent=intent)
                elapsed = self._monotonic_fn() - started
                if elapsed > self.timeout_seconds:
                    raise TimeoutError("execution_gateway_timeout")
                result = _clone_execution_result(
                    raw_result,
                    gateway_metadata={
                        "attempt_count": attempt_number,
                        "max_attempts": max_attempts,
                        "timeout_seconds": self.timeout_seconds,
                        "idempotency_key": idempotency_key,
                        "degraded_mode": False,
                    },
                )
                self._idempotency_cache[idempotency_key] = result
                return result
            except TimeoutError:
                last_failure_reason = "execution_gateway_timeout"
            except Exception as exc:  # pragma: no cover - exception message text may vary
                last_failure_reason = f"execution_gateway_error:{exc.__class__.__name__}"

            if attempt_number < max_attempts:
                backoff_seconds = self.retry_backoff_seconds * (2 ** (attempt_number - 1))
                self._sleep_fn(backoff_seconds)

        degraded = self._degraded_result(
            intent=intent,
            idempotency_key=idempotency_key,
            attempt_count=max_attempts,
            failure_reason=last_failure_reason,
        )
        self._idempotency_cache[idempotency_key] = degraded
        return degraded


class HardenedExecutionAdapter:
    def __init__(
        self,
        execution_adapter: Any,
        *,
        gateway_max_retry_attempts: int = 1,
        gateway_retry_backoff_seconds: float = 0.25,
        gateway_timeout_seconds: float = 2.0,
    ) -> None:
        self.execution_adapter = execution_adapter
        self.gateway = ExecutionGatewayAdapter(
            execute_fn=execution_adapter.execute,
            max_retry_attempts=gateway_max_retry_attempts,
            retry_backoff_seconds=gateway_retry_backoff_seconds,
            timeout_seconds=gateway_timeout_seconds,
        )

    def skip(self, **kwargs: Any) -> ExecutionResult:
        return self.execution_adapter.skip(**kwargs)

    def execute(self, *, event: MarketEvent, intent: ExecutionIntent) -> ExecutionResult:
        idempotency_key = f"{intent.intent_id}:{event.timestamp}:{intent.requested_notional:.4f}"
        return self.gateway.execute(
            event=event,
            intent=intent,
            idempotency_key=idempotency_key,
        )
