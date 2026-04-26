from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Literal
import json
import socket
import time
from urllib.error import URLError
from urllib.request import Request, urlopen

from .contracts import MarketEvent
from .schemas import EVENT_SCHEMA_VERSION
from .paper_execution import ExecutionIntent, ExecutionResult


IngestionStatus = Literal["OK", "DEGRADED", "FAILED"]


@dataclass(frozen=True)
class IngestionBatch:
    status: IngestionStatus
    events: list[MarketEvent]
    reasons: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="milliseconds")


def _clamp_probability(value: float) -> float:
    return min(max(value, 0.001), 0.999)


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

    def _load_once(
        self, path: Path, *, timeout_seconds: float | None, attempt_number: int
    ) -> IngestionBatch:
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
                    if (
                        timeout_seconds is not None
                        and (self._monotonic_fn() - started) > timeout_seconds
                    ):
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

                    if (
                        previous_timestamp is not None
                        and event.timestamp < previous_timestamp
                    ):
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

    def load_jsonl(
        self, path: Path, *, timeout_seconds: float | None = None
    ) -> IngestionBatch:
        max_attempts = self.max_retry_attempts + 1
        last_failure: IngestionBatch | None = None
        for attempt_number in range(1, max_attempts + 1):
            outcome = self._load_once(
                path, timeout_seconds=timeout_seconds, attempt_number=attempt_number
            )
            if outcome.status != "FAILED":
                return outcome

            last_failure = outcome
            if outcome.reasons and outcome.reasons[0] in (
                "invalid_row_budget_exceeded",
                "non_monotonic_timestamp",
            ):
                return outcome

            if attempt_number < max_attempts:
                backoff_seconds = self.retry_backoff_seconds * (
                    2 ** (attempt_number - 1)
                )
                self._sleep_fn(backoff_seconds)

        return last_failure or IngestionBatch(
            status="FAILED",
            events=[],
            reasons=("ingestion_failed",),
            metadata={"path": str(path)},
        )


class LivePolymarketIngestionAdapter:
    def __init__(
        self,
        *,
        source_url: str = (
            "https://gamma-api.polymarket.com/markets"
            "?active=true&closed=false&limit=50"
        ),
        max_markets: int = 10,
        min_volume_24h: float = 0.0,
        max_retry_attempts: int = 1,
        retry_backoff_seconds: float = 0.25,
        max_invalid_rows: int = 0,
        deduplicate_event_ids: bool = True,
        volume_to_liquidity_multiplier: float = 20.0,
        max_hours_to_resolution_cap: float = 168.0,
        base_rate_midpoint_threshold: float = 0.5,
        news_signal_volume_24h_threshold: float = 300.0,
        whale_signal_liquidity_threshold: float = 30000.0,
        sleep_fn: Callable[[float], None] | None = None,
        fetch_json_fn: Callable[[str, float], Any] | None = None,
    ) -> None:
        if not source_url.strip():
            raise ValueError("source_url must not be empty")
        if max_markets <= 0:
            raise ValueError("max_markets must be > 0")
        if min_volume_24h < 0:
            raise ValueError("min_volume_24h must be >= 0")
        if max_retry_attempts < 0:
            raise ValueError("max_retry_attempts must be >= 0")
        if retry_backoff_seconds < 0:
            raise ValueError("retry_backoff_seconds must be >= 0")
        if max_invalid_rows < 0:
            raise ValueError("max_invalid_rows must be >= 0")
        if volume_to_liquidity_multiplier <= 0:
            raise ValueError("volume_to_liquidity_multiplier must be > 0")
        if max_hours_to_resolution_cap <= 0:
            raise ValueError("max_hours_to_resolution_cap must be > 0")

        self.source_url = source_url
        self.max_markets = max_markets
        self.min_volume_24h = min_volume_24h
        self.max_retry_attempts = max_retry_attempts
        self.retry_backoff_seconds = retry_backoff_seconds
        self.max_invalid_rows = max_invalid_rows
        self.deduplicate_event_ids = deduplicate_event_ids
        self.volume_to_liquidity_multiplier = volume_to_liquidity_multiplier
        self.max_hours_to_resolution_cap = max_hours_to_resolution_cap
        self.base_rate_midpoint_threshold = base_rate_midpoint_threshold
        self.news_signal_volume_24h_threshold = news_signal_volume_24h_threshold
        self.whale_signal_liquidity_threshold = whale_signal_liquidity_threshold
        self._sleep_fn = sleep_fn or time.sleep
        self._fetch_json_fn = fetch_json_fn or self._default_fetch_json
        self._previous_midpoint_by_market: dict[str, float] = {}

    def _default_fetch_json(self, source_url: str, timeout_seconds: float) -> Any:
        request = Request(
            source_url,
            headers={
                "Accept": "application/json",
                "User-Agent": "poly-robot-live-ingestion/1.0",
            },
        )
        with urlopen(request, timeout=timeout_seconds) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            payload = response.read().decode(charset)
        return json.loads(payload)

    @staticmethod
    def _parse_float(value: Any, *, default: float = 0.0) -> float:
        if value is None:
            return default
        if isinstance(value, str) and not value.strip():
            return default
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _is_timeout_error(exc: BaseException) -> bool:
        if isinstance(exc, (TimeoutError, socket.timeout)):
            return True
        if isinstance(exc, URLError):
            reason = exc.reason
            return isinstance(reason, (TimeoutError, socket.timeout))
        return False

    def _extract_midpoint(self, row: dict[str, Any]) -> float:
        raw_outcome_prices = row.get("outcomePrices")
        if isinstance(raw_outcome_prices, str):
            try:
                parsed_prices = json.loads(raw_outcome_prices)
            except json.JSONDecodeError:
                parsed_prices = []
        elif isinstance(raw_outcome_prices, list):
            parsed_prices = raw_outcome_prices
        else:
            parsed_prices = []

        if parsed_prices:
            return _clamp_probability(self._parse_float(parsed_prices[0], default=0.5))

        best_bid = self._parse_float(row.get("bestBid"))
        best_ask = self._parse_float(row.get("bestAsk"))
        if best_bid > 0 and best_ask > 0:
            return _clamp_probability((best_bid + best_ask) / 2.0)

        last_trade = self._parse_float(row.get("lastTradePrice"), default=-1.0)
        if last_trade >= 0:
            return _clamp_probability(last_trade)

        raise ValueError("midpoint_unavailable")

    @staticmethod
    def _parse_datetime(value: str) -> datetime | None:
        normalized = value.strip()
        if not normalized:
            return None
        if normalized.endswith("Z"):
            normalized = normalized[:-1] + "+00:00"
        try:
            return datetime.fromisoformat(normalized)
        except ValueError:
            return None

    def _normalize_hours_to_resolution(
        self,
        *,
        end_date_value: str,
        reference_timestamp: str,
    ) -> tuple[float, bool]:
        end_date = self._parse_datetime(end_date_value)
        reference_date = self._parse_datetime(reference_timestamp)
        if end_date is None or reference_date is None:
            return 24.0, True

        raw_hours = (end_date - reference_date).total_seconds() / 3600.0
        if raw_hours <= 0:
            return 24.0, True
        if raw_hours > self.max_hours_to_resolution_cap:
            return float(self.max_hours_to_resolution_cap), True
        return raw_hours, False

    def _build_market_event(
        self, row: dict[str, Any], *, fetched_at: str
    ) -> tuple[MarketEvent, float]:
        market_id = str(row.get("id") or row.get("conditionId") or "").strip()
        if not market_id:
            raise ValueError("market_id_missing")

        timestamp = str(row.get("updatedAt") or row.get("createdAt") or fetched_at)
        midpoint = self._extract_midpoint(row)
        one_week_change = self._parse_float(row.get("oneWeekPriceChange"))
        volume_24h = self._parse_float(
            row.get("volume24hr", row.get("volume24hrClob", 0.0))
        )
        raw_liquidity = self._parse_float(
            row.get("liquidityNum", row.get("liquidity", 0.0))
        )
        effective_liquidity = max(
            raw_liquidity, volume_24h * self.volume_to_liquidity_multiplier
        )

        previous_midpoint = self._previous_midpoint_by_market.get(market_id)
        momentum = midpoint - previous_midpoint if previous_midpoint is not None else 0.0
        self._previous_midpoint_by_market[market_id] = midpoint

        signal_bonus = 0.0
        if volume_24h >= self.news_signal_volume_24h_threshold:
            signal_bonus += 0.03
        if effective_liquidity >= self.whale_signal_liquidity_threshold:
            signal_bonus += 0.025
        if one_week_change > 0:
            signal_bonus += 0.02
        if momentum > 0:
            signal_bonus += min(0.05, momentum)

        estimated_probability = _clamp_probability(midpoint + signal_bonus)
        hours_to_resolution, normalized_hours = self._normalize_hours_to_resolution(
            end_date_value=str(row.get("endDate") or ""),
            reference_timestamp=timestamp,
        )

        check_signals = {
            "base_rate": midpoint >= self.base_rate_midpoint_threshold,
            "news": volume_24h >= self.news_signal_volume_24h_threshold,
            "whale": effective_liquidity >= self.whale_signal_liquidity_threshold,
            "disposition": one_week_change >= 0,
        }
        checks_passed = sum(1 for passed in check_signals.values() if passed)
        base_confidence = _clamp_probability(0.55 + (checks_passed * 0.1))
        consensus_buy_votes = 2 if checks_passed >= 3 else 1
        event_id = (
            f"{market_id}:{timestamp}"
            if timestamp
            else f"{market_id}:{fetched_at}"
        )

        payload = {
            "schema_version": EVENT_SCHEMA_VERSION,
            "event_id": event_id,
            "timestamp": timestamp,
            "market_id": market_id,
            "question": str(row.get("question") or row.get("slug") or market_id),
            "midpoint": midpoint,
            "estimated_probability": estimated_probability,
            "bids_depth_usd": max(500.0, effective_liquidity / 2.0),
            "asks_depth_usd": max(500.0, effective_liquidity / 2.0),
            "liquidity_usd": max(1000.0, effective_liquidity),
            "hours_to_resolution": round(hours_to_resolution, 4),
            "check_signals": check_signals,
            "base_confidence": round(base_confidence, 4),
            "llm_confidence": None,
            "consensus_buy_votes": consensus_buy_votes,
            "metadata": {
                "source": "polymarket_gamma",
                "source_url": self.source_url,
                "raw_market_id": row.get("id"),
                "market_slug": row.get("slug"),
                "volume_24h": volume_24h,
                "raw_liquidity": raw_liquidity,
                "effective_liquidity": effective_liquidity,
                "one_week_price_change": one_week_change,
                "momentum": round(momentum, 6),
                "hours_to_resolution_normalized": normalized_hours,
                "fetched_at": fetched_at,
            },
        }
        return MarketEvent.from_dict(payload), volume_24h

    def _load_once(
        self, *, timeout_seconds: float, attempt_number: int
    ) -> IngestionBatch:
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be > 0")

        fetched_at = _utc_now_iso()
        try:
            payload = self._fetch_json_fn(self.source_url, timeout_seconds)
        except (OSError, URLError, TimeoutError) as exc:
            if self._is_timeout_error(exc):
                return IngestionBatch(
                    status="FAILED",
                    events=[],
                    reasons=("ingestion_timeout",),
                    metadata={
                        "attempt_number": attempt_number,
                        "source_url": self.source_url,
                        "timeout_seconds": timeout_seconds,
                    },
                )
            return IngestionBatch(
                status="FAILED",
                events=[],
                reasons=("source_unavailable",),
                metadata={
                    "attempt_number": attempt_number,
                    "source_url": self.source_url,
                },
            )
        except json.JSONDecodeError:
            return IngestionBatch(
                status="FAILED",
                events=[],
                reasons=("invalid_source_payload",),
                metadata={
                    "attempt_number": attempt_number,
                    "source_url": self.source_url,
                },
            )

        if isinstance(payload, list):
            rows = payload
        elif isinstance(payload, dict):
            maybe_rows = payload.get("markets") or payload.get("data")
            if isinstance(maybe_rows, list):
                rows = maybe_rows
            else:
                rows = [payload]
        else:
            return IngestionBatch(
                status="FAILED",
                events=[],
                reasons=("invalid_source_payload",),
                metadata={
                    "attempt_number": attempt_number,
                    "source_url": self.source_url,
                    "payload_type": type(payload).__name__,
                },
            )

        events: list[MarketEvent] = []
        seen_event_ids: set[str] = set()
        invalid_rows = 0
        duplicate_rows = 0
        filtered_rows = 0

        for row_number, row in enumerate(rows, start=1):
            if len(events) >= self.max_markets:
                break
            if not isinstance(row, dict):
                invalid_rows += 1
                if invalid_rows > self.max_invalid_rows:
                    return IngestionBatch(
                        status="FAILED",
                        events=[],
                        reasons=("invalid_row_budget_exceeded",),
                        metadata={
                            "attempt_number": attempt_number,
                            "row_number": row_number,
                            "invalid_rows": invalid_rows,
                            "max_invalid_rows": self.max_invalid_rows,
                        },
                    )
                continue
            try:
                event, volume_24h = self._build_market_event(row, fetched_at=fetched_at)
            except ValueError:
                invalid_rows += 1
                if invalid_rows > self.max_invalid_rows:
                    return IngestionBatch(
                        status="FAILED",
                        events=[],
                        reasons=("invalid_row_budget_exceeded",),
                        metadata={
                            "attempt_number": attempt_number,
                            "row_number": row_number,
                            "invalid_rows": invalid_rows,
                            "max_invalid_rows": self.max_invalid_rows,
                        },
                    )
                continue

            if volume_24h < self.min_volume_24h:
                filtered_rows += 1
                continue

            if self.deduplicate_event_ids and event.event_id in seen_event_ids:
                duplicate_rows += 1
                continue
            seen_event_ids.add(event.event_id)
            events.append(event)

        if not events:
            if filtered_rows > 0:
                return IngestionBatch(
                    status="DEGRADED",
                    events=[],
                    reasons=("no_markets_after_filters",),
                    metadata={
                        "attempt_number": attempt_number,
                        "source_url": self.source_url,
                        "total_rows": len(rows),
                        "invalid_rows": invalid_rows,
                        "filtered_rows": filtered_rows,
                    },
                )
            if not rows:
                return IngestionBatch(
                    status="DEGRADED",
                    events=[],
                    reasons=("source_returned_no_rows",),
                    metadata={
                        "attempt_number": attempt_number,
                        "source_url": self.source_url,
                        "total_rows": len(rows),
                    },
                )
            return IngestionBatch(
                status="FAILED",
                events=[],
                reasons=("no_valid_events",),
                metadata={
                    "attempt_number": attempt_number,
                    "source_url": self.source_url,
                    "total_rows": len(rows),
                    "invalid_rows": invalid_rows,
                    "filtered_rows": filtered_rows,
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
        if filtered_rows > 0:
            reasons.append("rows_filtered_by_volume")
            status = "DEGRADED"

        return IngestionBatch(
            status=status,
            events=events,
            reasons=tuple(reasons),
            metadata={
                "attempt_number": attempt_number,
                "source_url": self.source_url,
                "total_rows": len(rows),
                "selected_rows": len(events),
                "invalid_rows": invalid_rows,
                "duplicate_rows": duplicate_rows,
                "filtered_rows": filtered_rows,
                "max_markets": self.max_markets,
                "min_volume_24h": self.min_volume_24h,
                "fetched_at": fetched_at,
            },
        )

    def load_markets(self, *, timeout_seconds: float = 5.0) -> IngestionBatch:
        max_attempts = self.max_retry_attempts + 1
        last_failure: IngestionBatch | None = None
        for attempt_number in range(1, max_attempts + 1):
            outcome = self._load_once(
                timeout_seconds=timeout_seconds,
                attempt_number=attempt_number,
            )
            if outcome.status != "FAILED":
                return outcome

            last_failure = outcome
            if outcome.reasons and outcome.reasons[0] in (
                "invalid_row_budget_exceeded",
                "invalid_source_payload",
                "no_valid_events",
            ):
                return outcome

            if attempt_number < max_attempts:
                backoff_seconds = self.retry_backoff_seconds * (
                    2 ** (attempt_number - 1)
                )
                self._sleep_fn(backoff_seconds)

        return last_failure or IngestionBatch(
            status="FAILED",
            events=[],
            reasons=("ingestion_failed",),
            metadata={"source_url": self.source_url},
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

    def execute(
        self, *, event: MarketEvent, intent: ExecutionIntent, idempotency_key: str
    ) -> ExecutionResult:
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
            except (
                Exception
            ) as exc:  # pragma: no cover - exception message text may vary
                last_failure_reason = (
                    f"execution_gateway_error:{exc.__class__.__name__}"
                )

            if attempt_number < max_attempts:
                backoff_seconds = self.retry_backoff_seconds * (
                    2 ** (attempt_number - 1)
                )
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

    def execute(
        self, *, event: MarketEvent, intent: ExecutionIntent
    ) -> ExecutionResult:
        idempotency_key = (
            f"{intent.intent_id}:{event.timestamp}:{intent.requested_notional:.4f}"
        )
        return self.gateway.execute(
            event=event,
            intent=intent,
            idempotency_key=idempotency_key,
        )
