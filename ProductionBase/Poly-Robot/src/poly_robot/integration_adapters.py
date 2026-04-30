from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Literal, Mapping
import base64
import hashlib
import hmac
import json
import math
import os
import socket
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from .contracts import MarketEvent, RiskDecision
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
        whale_signal_wallet_threshold: float = 3.0,
        domain_exploration_weight: float = 0.25,
        complement_arb_min_edge_bps: float = 30.0,
        complement_arb_max_spread_bps: float = 120.0,
        complement_arb_fee_rate_bps: float = 20.0,
        complement_arb_max_tick_size: float = 0.02,
        complement_arb_min_notional_usd: float = 25.0,
        execution_mode: str = "paper",
        complement_arb_paper_mode_only: bool = True,
        wallet_convergence_loader: Callable[[], dict[str, Any]] | None = None,
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
        if whale_signal_wallet_threshold <= 0:
            raise ValueError("whale_signal_wallet_threshold must be > 0")
        if not (0.0 <= domain_exploration_weight <= 1.0):
            raise ValueError("domain_exploration_weight must be between 0 and 1")
        if complement_arb_min_edge_bps < 0:
            raise ValueError("complement_arb_min_edge_bps must be >= 0")
        if complement_arb_max_spread_bps <= 0:
            raise ValueError("complement_arb_max_spread_bps must be > 0")
        if complement_arb_fee_rate_bps < 0:
            raise ValueError("complement_arb_fee_rate_bps must be >= 0")
        if complement_arb_max_tick_size <= 0:
            raise ValueError("complement_arb_max_tick_size must be > 0")
        if complement_arb_min_notional_usd <= 0:
            raise ValueError("complement_arb_min_notional_usd must be > 0")

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
        self.whale_signal_wallet_threshold = whale_signal_wallet_threshold
        self.domain_exploration_weight = domain_exploration_weight
        self.complement_arb_min_edge_bps = complement_arb_min_edge_bps
        self.complement_arb_max_spread_bps = complement_arb_max_spread_bps
        self.complement_arb_fee_rate_bps = complement_arb_fee_rate_bps
        self.complement_arb_max_tick_size = complement_arb_max_tick_size
        self.complement_arb_min_notional_usd = complement_arb_min_notional_usd
        self.execution_mode = execution_mode.strip() or "paper"
        self.complement_arb_paper_mode_only = complement_arb_paper_mode_only
        self._wallet_convergence_loader = wallet_convergence_loader
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

    @classmethod
    def _extract_wallet_convergence_count(cls, value: Any) -> float | None:
        if isinstance(value, dict):
            for key in (
                "target_wallet_count",
                "wallet_count",
                "convergence_count",
                "count",
            ):
                if key in value:
                    return cls._extract_wallet_convergence_count(value[key])
            return None

        parsed = cls._parse_float(value, default=-1.0)
        if parsed < 0:
            return None
        return parsed

    @staticmethod
    def _normalize_domain_key(value: Any) -> str:
        text = str(value or "").strip().lower()
        if not text:
            return ""
        normalized = "".join(
            character if character.isalnum() else "_"
            for character in text
        )
        while "__" in normalized:
            normalized = normalized.replace("__", "_")
        return normalized.strip("_")

    def _resolve_market_domain_key(self, row: dict[str, Any]) -> str:
        for key in (
            "category",
            "categorySlug",
            "marketCategory",
            "groupItemTitle",
            "tag",
        ):
            normalized = self._normalize_domain_key(row.get(key))
            if normalized:
                return normalized

        text = str(row.get("question") or row.get("slug") or "").strip().lower()
        if not text:
            return "general"
        if any(token in text for token in ("election", "president", "senate", "vote")):
            return "politics"
        if any(token in text for token in ("bitcoin", "btc", "eth", "crypto", "solana")):
            return "crypto"
        if any(token in text for token in ("nba", "nfl", "soccer", "mlb", "ufc", "f1")):
            return "sports"
        if any(
            token in text
            for token in ("movie", "album", "music", "award", "celebrity", "tv")
        ):
            return "culture"
        return "general"

    def _load_wallet_convergence_map(
        self,
    ) -> tuple[dict[str, float], dict[str, float], str | None]:
        if self._wallet_convergence_loader is None:
            return {}, {}, None
        try:
            payload = self._wallet_convergence_loader()
        except Exception as exc:  # pragma: no cover - defensive branch
            return {}, {}, exc.__class__.__name__

        if payload is None:
            return {}, {}, None
        if not isinstance(payload, dict):
            return {}, {}, f"invalid_payload:{type(payload).__name__}"

        market_source = payload
        if isinstance(payload.get("markets"), dict):
            market_source = payload["markets"]
        domain_source: dict[str, Any] = {}
        if isinstance(payload.get("domains"), dict):
            domain_source = payload["domains"]

        market_counts: dict[str, float] = {}
        for market_id, raw_count in market_source.items():
            market_key = str(market_id).strip()
            if not market_key:
                continue
            count = self._extract_wallet_convergence_count(raw_count)
            if count is None:
                continue
            market_counts[market_key] = count

        domain_counts: dict[str, float] = {}
        for domain_key, raw_count in domain_source.items():
            normalized_domain = self._normalize_domain_key(domain_key)
            if not normalized_domain:
                continue
            count = self._extract_wallet_convergence_count(raw_count)
            if count is None:
                continue
            domain_counts[normalized_domain] = count
        return market_counts, domain_counts, None

    def _extract_outcome_prices(self, row: dict[str, Any]) -> list[float]:
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
        outcome_prices: list[float] = []
        for raw_value in parsed_prices:
            parsed = self._parse_float(raw_value, default=-1.0)
            if parsed < 0:
                continue
            outcome_prices.append(_clamp_probability(parsed))
        return outcome_prices

    def _extract_midpoint(self, row: dict[str, Any]) -> float:
        outcome_prices = self._extract_outcome_prices(row)
        if outcome_prices:
            return _clamp_probability(outcome_prices[0])

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

    @staticmethod
    def _normalize_positive_feature(value: float, *, saturation: float) -> float:
        if saturation <= 0:
            return 0.0
        bounded = max(0.0, float(value))
        return min(1.0, bounded / saturation)

    def _build_complement_arb_signal(
        self,
        *,
        row: dict[str, Any],
        outcome_prices: list[float],
        tick_size: float,
        token_id: str,
        available_balance_usd: float,
        allowance_usd: float,
    ) -> dict[str, Any]:
        outcome_sum = (
            sum(outcome_prices[:2])
            if len(outcome_prices) >= 2
            else None
        )
        best_bid = self._parse_float(row.get("bestBid"), default=0.0)
        best_ask = self._parse_float(row.get("bestAsk"), default=0.0)
        spread_fraction = 0.0
        if best_bid > 0 and best_ask > 0 and best_ask >= best_bid:
            spread_fraction = best_ask - best_bid
        elif tick_size > 0:
            spread_fraction = tick_size
        spread_bps = round(spread_fraction * 10_000, 2)
        underround_fraction = (
            max(0.0, 1.0 - outcome_sum) if outcome_sum is not None else 0.0
        )
        fee_fraction = self.complement_arb_fee_rate_bps / 10_000
        effective_edge_fraction = (
            underround_fraction - fee_fraction - spread_fraction
        )
        effective_edge_bps = round(effective_edge_fraction * 10_000, 2)
        fast_path_active = (
            self.execution_mode == "paper"
            if self.complement_arb_paper_mode_only
            else True
        )
        constraints: dict[str, bool] = {
            "fast_path_active": fast_path_active,
            "has_token_id": bool(token_id),
            "tick_size_within_limit": (
                tick_size > 0 and tick_size <= self.complement_arb_max_tick_size
            ),
            "spread_within_limit": spread_bps <= self.complement_arb_max_spread_bps,
            "edge_above_threshold": (
                effective_edge_bps >= self.complement_arb_min_edge_bps
            ),
            "balance_sufficient": (
                available_balance_usd < 0
                or available_balance_usd >= self.complement_arb_min_notional_usd
            ),
            "allowance_sufficient": (
                allowance_usd < 0
                or allowance_usd >= self.complement_arb_min_notional_usd
            ),
            "has_dual_outcomes": outcome_sum is not None,
        }
        candidate = all(constraints.values())
        rejection_reasons = [
            key for key, passed in constraints.items() if not passed
        ]
        return {
            "fast_path_active": fast_path_active,
            "candidate": candidate,
            "mode": (
                "paper_only"
                if self.complement_arb_paper_mode_only
                else "all_modes"
            ),
            "outcome_sum": outcome_sum,
            "underround_fraction": round(underround_fraction, 6),
            "estimated_spread_bps": spread_bps,
            "effective_edge_bps": effective_edge_bps,
            "constraints": constraints,
            "rejection_reasons": rejection_reasons,
        }

    def _apply_domain_allocation_budgets(
        self,
        events: list[MarketEvent],
    ) -> tuple[list[MarketEvent], dict[str, float]]:
        if not events:
            return events, {}

        domain_reward_sum: dict[str, float] = {}
        domain_event_count: dict[str, int] = {}
        for event in events:
            metadata = event.metadata
            domain_key = str(metadata.get("domain_key") or "general").strip() or "general"
            reward_signal = self._parse_float(
                metadata.get("domain_bandit_reward_signal"),
                default=0.5,
            )
            reward_signal = min(max(reward_signal, 0.0), 1.0)
            domain_reward_sum[domain_key] = (
                domain_reward_sum.get(domain_key, 0.0) + reward_signal
            )
            domain_event_count[domain_key] = domain_event_count.get(domain_key, 0) + 1

        total_events = max(1, len(events))
        domain_budget_score: dict[str, float] = {}
        for domain_key, count in domain_event_count.items():
            average_reward = domain_reward_sum[domain_key] / max(1, count)
            exploration_bonus = math.sqrt(
                math.log(total_events + 1.0) / (count + 1.0)
            )
            ucb_score = average_reward + (
                self.domain_exploration_weight * exploration_bonus
            )
            domain_budget_score[domain_key] = max(1e-6, ucb_score)
        budget_denominator = sum(domain_budget_score.values())
        if budget_denominator <= 0:
            equal_budget = 1.0 / max(1, len(domain_budget_score))
            domain_budget = {
                key: round(equal_budget, 6) for key in domain_budget_score
            }
        else:
            domain_budget = {
                key: round(score / budget_denominator, 6)
                for key, score in domain_budget_score.items()
            }

        adjusted_events: list[MarketEvent] = []
        for event in events:
            event_payload = event.to_dict()
            event_metadata = dict(event_payload.get("metadata", {}))
            domain_key = str(event_metadata.get("domain_key") or "general").strip() or "general"
            event_metadata["domain_allocation_budget"] = domain_budget.get(domain_key, 0.0)
            event_metadata["domain_bandit_exploration_weight"] = round(
                self.domain_exploration_weight,
                6,
            )
            event_payload["metadata"] = event_metadata
            adjusted_events.append(MarketEvent.from_dict(event_payload))
        return adjusted_events, domain_budget

    def _build_market_event(
        self,
        row: dict[str, Any],
        *,
        fetched_at: str,
        wallet_convergence_by_market: dict[str, float] | None = None,
        wallet_convergence_by_domain: dict[str, float] | None = None,
    ) -> tuple[MarketEvent, float]:
        market_id = str(row.get("id") or row.get("conditionId") or "").strip()
        if not market_id:
            raise ValueError("market_id_missing")
        token_id = str(
            row.get("tokenId") or row.get("token_id") or row.get("clobTokenId") or ""
        ).strip()
        tick_size = self._parse_float(
            row.get("tickSize", row.get("tick_size")),
            default=0.0,
        )
        neg_risk_raw = row.get("negRisk", row.get("neg_risk"))
        neg_risk = bool(neg_risk_raw)
        available_balance_usd = self._parse_float(
            row.get("availableBalanceUsd", row.get("available_balance_usd")),
            default=-1.0,
        )
        allowance_usd = self._parse_float(
            row.get("allowanceUsd", row.get("allowance_usd")),
            default=-1.0,
        )

        timestamp = str(row.get("updatedAt") or row.get("createdAt") or fetched_at)
        outcome_prices = self._extract_outcome_prices(row)
        midpoint = (
            _clamp_probability(outcome_prices[0])
            if outcome_prices
            else self._extract_midpoint(row)
        )
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
        domain_key = self._resolve_market_domain_key(row)
        market_wallet_convergence_count = 0.0
        if wallet_convergence_by_market is not None:
            market_wallet_convergence_count = wallet_convergence_by_market.get(
                market_id, 0.0
            )
        domain_wallet_convergence_count = 0.0
        if wallet_convergence_by_domain is not None:
            domain_wallet_convergence_count = wallet_convergence_by_domain.get(
                domain_key,
                0.0,
            )
        wallet_convergence_count = max(
            market_wallet_convergence_count,
            domain_wallet_convergence_count,
        )
        wallet_whale_signal = (
            wallet_convergence_count >= self.whale_signal_wallet_threshold
        )
        liquidity_whale_signal = (
            effective_liquidity >= self.whale_signal_liquidity_threshold
        )
        whale_signal = wallet_whale_signal or liquidity_whale_signal
        complement_arb_signal = self._build_complement_arb_signal(
            row=row,
            outcome_prices=outcome_prices,
            tick_size=tick_size,
            token_id=token_id,
            available_balance_usd=available_balance_usd,
            allowance_usd=allowance_usd,
        )

        previous_midpoint = self._previous_midpoint_by_market.get(market_id)
        momentum = midpoint - previous_midpoint if previous_midpoint is not None else 0.0
        self._previous_midpoint_by_market[market_id] = midpoint
        check_signals = {
            "base_rate": midpoint >= self.base_rate_midpoint_threshold,
            "news": volume_24h >= self.news_signal_volume_24h_threshold,
            "whale": whale_signal,
            "disposition": one_week_change >= 0,
        }
        checks_passed = sum(1 for passed in check_signals.values() if passed)
        signal_agreement = checks_passed / max(1, len(check_signals))
        normalized_weekly_change = max(-1.0, min(1.0, one_week_change / 0.05))
        normalized_momentum = max(-1.0, min(1.0, momentum / 0.03))
        liquidity_score = self._normalize_positive_feature(
            effective_liquidity,
            saturation=max(self.whale_signal_liquidity_threshold * 2.0, 1.0),
        )
        volume_score = self._normalize_positive_feature(
            volume_24h,
            saturation=max(self.news_signal_volume_24h_threshold * 4.0, 1.0),
        )
        market_wallet_convergence_score = self._normalize_positive_feature(
            market_wallet_convergence_count,
            saturation=max(self.whale_signal_wallet_threshold * 2.0, 1.0),
        )
        domain_wallet_convergence_score = self._normalize_positive_feature(
            domain_wallet_convergence_count,
            saturation=max(self.whale_signal_wallet_threshold * 2.0, 1.0),
        )
        wallet_convergence_score = max(
            market_wallet_convergence_score,
            domain_wallet_convergence_score,
        )
        domain_bandit_reward_signal = min(
            max(
                0.0,
                (0.6 * signal_agreement)
                + (0.4 * domain_wallet_convergence_score),
            ),
            1.0,
        )
        probability_components = {
            "alpha_prior_component": 0.035,
            "weekly_change_component": 0.06 * normalized_weekly_change,
            "momentum_component": 0.03 * normalized_momentum,
            "news_volume_component": 0.02 * (volume_score - 0.25),
            "liquidity_component": 0.02 * (liquidity_score - 0.4),
            "wallet_convergence_component": (
                0.02 * market_wallet_convergence_score
            ),
            "domain_basket_component": (
                0.025 * domain_wallet_convergence_score
            ),
            "signal_agreement_component": 0.04 * (signal_agreement - 0.5),
            "whale_presence_component": 0.015 if whale_signal else -0.005,
            "disposition_component": 0.01 if check_signals["disposition"] else -0.01,
        }
        raw_estimated_probability = midpoint + sum(probability_components.values())
        estimated_probability = _clamp_probability(raw_estimated_probability)
        hours_to_resolution, normalized_hours = self._normalize_hours_to_resolution(
            end_date_value=str(row.get("endDate") or ""),
            reference_timestamp=timestamp,
        )
        base_confidence = _clamp_probability(0.55 + (checks_passed * 0.1))
        consensus_buy_votes = 2 if checks_passed >= 3 else 1
        event_id = (
            f"{market_id}:{timestamp}"
            if timestamp
            else f"{market_id}:{fetched_at}"
        )

        metadata_payload: dict[str, Any] = {
            "source": "polymarket_gamma",
            "source_url": self.source_url,
            "raw_market_id": row.get("id"),
            "market_slug": row.get("slug"),
            "token_id": token_id or None,
            "tick_size": tick_size if tick_size > 0 else None,
            "neg_risk": neg_risk,
            "volume_24h": volume_24h,
            "raw_liquidity": raw_liquidity,
            "effective_liquidity": effective_liquidity,
            "domain_key": domain_key,
            "market_wallet_convergence_count": market_wallet_convergence_count,
            "domain_wallet_convergence_count": domain_wallet_convergence_count,
            "wallet_convergence_count": wallet_convergence_count,
            "wallet_convergence_signal": wallet_whale_signal,
            "domain_wallet_convergence_signal": (
                domain_wallet_convergence_count
                >= self.whale_signal_wallet_threshold
            ),
            "liquidity_whale_signal": liquidity_whale_signal,
            "complement_arb_candidate": bool(
                complement_arb_signal.get("candidate")
            ),
            "complement_arb_signal": complement_arb_signal,
            "outcome_prices": [
                round(price, 6)
                for price in outcome_prices[:4]
            ],
            "one_week_price_change": one_week_change,
            "momentum": round(momentum, 6),
            "normalized_weekly_change": round(normalized_weekly_change, 6),
            "normalized_momentum": round(normalized_momentum, 6),
            "probability_estimator_version": "live_structured.v2",
            "probability_features": {
                "signal_agreement": round(signal_agreement, 6),
                "liquidity_score": round(liquidity_score, 6),
                "volume_score": round(volume_score, 6),
                "market_wallet_convergence_score": round(
                    market_wallet_convergence_score,
                    6,
                ),
                "domain_wallet_convergence_score": round(
                    domain_wallet_convergence_score,
                    6,
                ),
                "wallet_convergence_score": round(
                    wallet_convergence_score, 6
                ),
            },
            "probability_components": {
                key: round(value, 6)
                for key, value in probability_components.items()
            },
            "raw_estimated_probability": round(raw_estimated_probability, 6),
            "legacy_signal_bonus": round(
                max(0.0, estimated_probability - midpoint), 6
            ),
            "domain_bandit_reward_signal": round(
                domain_bandit_reward_signal,
                6,
            ),
            "hours_to_resolution_normalized": normalized_hours,
            "fetched_at": fetched_at,
        }
        payload: dict[str, Any] = {
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
            "metadata": metadata_payload,
        }
        if available_balance_usd >= 0:
            metadata_payload["available_balance_usd"] = available_balance_usd
        if allowance_usd >= 0:
            metadata_payload["allowance_usd"] = allowance_usd
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
        (
            wallet_convergence_by_market,
            wallet_convergence_by_domain,
            wallet_signal_loader_error,
        ) = self._load_wallet_convergence_map()
        wallet_signal_metadata: dict[str, Any] = {
            "wallet_signal_enabled": self._wallet_convergence_loader is not None,
            "wallet_signal_markets": len(wallet_convergence_by_market),
            "wallet_signal_domains": len(wallet_convergence_by_domain),
            "whale_signal_wallet_threshold": self.whale_signal_wallet_threshold,
        }
        if wallet_signal_loader_error is not None:
            wallet_signal_metadata["wallet_signal_loader_error"] = (
                wallet_signal_loader_error
            )

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
                event, volume_24h = self._build_market_event(
                    row,
                    fetched_at=fetched_at,
                    wallet_convergence_by_market=wallet_convergence_by_market,
                    wallet_convergence_by_domain=wallet_convergence_by_domain,
                )
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
        domain_budget_allocation: dict[str, float] = {}
        if events:
            events, domain_budget_allocation = self._apply_domain_allocation_budgets(
                events
            )

        if not events:
            if filtered_rows > 0:
                filtered_reasons = ["no_markets_after_filters"]
                if wallet_signal_loader_error is not None:
                    filtered_reasons.append("wallet_signal_unavailable")
                return IngestionBatch(
                    status="DEGRADED",
                    events=[],
                    reasons=tuple(filtered_reasons),
                    metadata={
                        "attempt_number": attempt_number,
                        "source_url": self.source_url,
                        "total_rows": len(rows),
                        "invalid_rows": invalid_rows,
                        "filtered_rows": filtered_rows,
                        "domain_exploration_weight": self.domain_exploration_weight,
                        **wallet_signal_metadata,
                    },
                )
            if not rows:
                empty_reasons = ["source_returned_no_rows"]
                if wallet_signal_loader_error is not None:
                    empty_reasons.append("wallet_signal_unavailable")
                return IngestionBatch(
                    status="DEGRADED",
                    events=[],
                    reasons=tuple(empty_reasons),
                    metadata={
                        "attempt_number": attempt_number,
                        "source_url": self.source_url,
                        "total_rows": len(rows),
                        "domain_exploration_weight": self.domain_exploration_weight,
                        **wallet_signal_metadata,
                    },
                )
            no_valid_reasons = ["no_valid_events"]
            if wallet_signal_loader_error is not None:
                no_valid_reasons.append("wallet_signal_unavailable")
            return IngestionBatch(
                status="FAILED",
                events=[],
                reasons=tuple(no_valid_reasons),
                metadata={
                    "attempt_number": attempt_number,
                    "source_url": self.source_url,
                    "total_rows": len(rows),
                    "invalid_rows": invalid_rows,
                    "filtered_rows": filtered_rows,
                    "domain_exploration_weight": self.domain_exploration_weight,
                    **wallet_signal_metadata,
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
        if wallet_signal_loader_error is not None:
            reasons.append("wallet_signal_unavailable")
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
                "domain_exploration_weight": self.domain_exploration_weight,
                "domain_budget_allocation": domain_budget_allocation,
                "fetched_at": fetched_at,
                **wallet_signal_metadata,
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

class PolymarketClobExecutionAdapter:
    _L1_AUTH_ENDPOINT_PATHS = frozenset(
        {
            "/auth/api-key",
            "/auth/derive-api-key",
        }
    )
    def __init__(
        self,
        *,
        clob_base_url: str,
        rollout_stage: str,
        stage_enabled: bool,
        real_order_submission: bool,
        allow_real_trading: bool,
        required_env_vars: tuple[str, ...] = (),
        max_order_notional_usd: float | None = None,
        max_daily_notional_usd: float | None = None,
        max_open_orders: int | None = None,
        required_market_metadata: tuple[str, ...] = (),
        require_pretrade_balance_checks: bool = True,
        require_user_channel_trade_ack: bool = True,
        require_kill_switch: bool = True,
        allow_plaintext_secrets: bool = False,
        preferred_secret_sources: tuple[str, ...] = (),
        max_secret_age_days: int = 90,
        user_channel_max_staleness_seconds: float = 30.0,
        user_channel_event_source: Callable[[], list[dict[str, Any]]] | None = None,
        audit_log_path: Path | None = None,
        now_fn: Callable[[], datetime] | None = None,
        environment: Mapping[str, str] | None = None,
        enforce_auth_healthcheck: bool = False,
        enable_geoblock_check: bool = False,
        geoblock_url: str = "https://polymarket.com/api/geoblock",
        auth_healthcheck_timeout_seconds: float = 2.0,
        auth_healthcheck_ttl_seconds: float = 30.0,
        auth_healthcheck_max_time_skew_seconds: float = 30.0,
        allow_l1_auth_requests: bool = False,
        http_json_request_fn: (
            Callable[
                [str, str, dict[str, str], str | None, float],
                tuple[int | None, Any, str | None],
            ]
            | None
        ) = None,
    ) -> None:
        normalized_base_url = clob_base_url.strip()
        if not normalized_base_url:
            raise ValueError("clob_base_url must not be empty")
        normalized_stage = rollout_stage.strip()
        if not normalized_stage:
            raise ValueError("rollout_stage must not be empty")
        self.clob_base_url = normalized_base_url.rstrip("/")
        self.rollout_stage = normalized_stage
        self.stage_enabled = bool(stage_enabled)
        self.real_order_submission = bool(real_order_submission)
        self.allow_real_trading = bool(allow_real_trading)
        self.required_env_vars = tuple(
            var_name.strip() for var_name in required_env_vars if var_name.strip()
        )
        self.max_order_notional_usd = (
            float(max_order_notional_usd)
            if max_order_notional_usd is not None and max_order_notional_usd > 0
            else None
        )
        self.max_daily_notional_usd = (
            float(max_daily_notional_usd)
            if max_daily_notional_usd is not None and max_daily_notional_usd > 0
            else None
        )
        self.max_open_orders = (
            int(max_open_orders)
            if max_open_orders is not None and max_open_orders > 0
            else None
        )
        self.required_market_metadata = tuple(
            key.strip() for key in required_market_metadata if key.strip()
        )
        self.require_pretrade_balance_checks = bool(require_pretrade_balance_checks)
        self.require_user_channel_trade_ack = bool(require_user_channel_trade_ack)
        self.require_kill_switch = bool(require_kill_switch)
        self.allow_plaintext_secrets = bool(allow_plaintext_secrets)
        self.preferred_secret_sources = tuple(
            source.strip().lower()
            for source in preferred_secret_sources
            if source.strip()
        )
        if max_secret_age_days <= 0:
            raise ValueError("max_secret_age_days must be > 0")
        self.max_secret_age_days = int(max_secret_age_days)
        if user_channel_max_staleness_seconds <= 0:
            raise ValueError("user_channel_max_staleness_seconds must be > 0")
        self.user_channel_max_staleness_seconds = float(
            user_channel_max_staleness_seconds
        )
        if auth_healthcheck_timeout_seconds <= 0:
            raise ValueError("auth_healthcheck_timeout_seconds must be > 0")
        if auth_healthcheck_ttl_seconds <= 0:
            raise ValueError("auth_healthcheck_ttl_seconds must be > 0")
        if auth_healthcheck_max_time_skew_seconds <= 0:
            raise ValueError("auth_healthcheck_max_time_skew_seconds must be > 0")
        self.enforce_auth_healthcheck = bool(enforce_auth_healthcheck)
        self.enable_geoblock_check = bool(enable_geoblock_check)
        normalized_geoblock_url = geoblock_url.strip()
        self.geoblock_url = (
            normalized_geoblock_url
            if normalized_geoblock_url
            else "https://polymarket.com/api/geoblock"
        )
        self.auth_healthcheck_timeout_seconds = float(auth_healthcheck_timeout_seconds)
        self.auth_healthcheck_ttl_seconds = float(auth_healthcheck_ttl_seconds)
        self.auth_healthcheck_max_time_skew_seconds = float(
            auth_healthcheck_max_time_skew_seconds
        )
        self.allow_l1_auth_requests = bool(allow_l1_auth_requests)
        self._raw_http_json_request_fn = (
            http_json_request_fn or self._default_http_json_request
        )
        self._http_json_request_fn = self._guarded_http_json_request
        self._user_channel_event_source = user_channel_event_source
        self.audit_log_path = audit_log_path
        self._now_fn = now_fn or (lambda: datetime.now(UTC))
        if environment is None:
            self.environment = dict(os.environ)
        else:
            self.environment = dict(environment)
        self._open_orders: dict[str, dict[str, Any]] = {}
        self._daily_submitted_notional_by_day: dict[str, float] = {}
        self._order_sequence = 0
        self._last_user_channel_heartbeat_at: datetime | None = None
        self._last_auth_healthcheck_at: datetime | None = None
        self._cached_auth_healthcheck: tuple[list[str], dict[str, Any]] | None = None

    @staticmethod
    def _coerce_bool(value: Any) -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value != 0
        return str(value).strip().lower() in {"1", "true", "yes", "on"}

    @staticmethod
    def _parse_datetime(value: str) -> datetime | None:
        normalized = value.strip()
        if not normalized:
            return None
        if normalized.endswith("Z"):
            normalized = normalized[:-1] + "+00:00"
        try:
            parsed = datetime.fromisoformat(normalized)
        except ValueError:
            return None
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=UTC)
        return parsed.astimezone(UTC)

    @staticmethod
    def _clamp_price(value: float) -> float:
        return min(max(value, 0.001), 0.999)

    @staticmethod
    def _normalize_order_status(value: Any) -> str | None:
        normalized = str(value).strip().upper()
        aliases = {
            "SUBMITTED": "OPEN",
            "ACCEPTED": "OPEN",
            "LIVE": "OPEN",
            "OPEN": "OPEN",
            "PARTIALLY_FILLED": "PARTIALLY_FILLED",
            "PARTIAL": "PARTIALLY_FILLED",
            "FILLED": "FILLED",
            "MATCHED": "FILLED",
            "CANCELLED": "CANCELLED",
            "CANCELED": "CANCELLED",
            "REJECTED": "REJECTED",
            "FAILED": "REJECTED",
            "ERROR": "REJECTED",
        }
        return aliases.get(normalized)

    @staticmethod
    def _metadata_float(
        payload: Mapping[str, Any],
        *,
        keys: tuple[str, ...],
        default: float | None = None,
    ) -> float | None:
        for key in keys:
            if key not in payload:
                continue
            try:
                return float(payload[key])
            except (TypeError, ValueError):
                continue
        return default

    def _now(self) -> datetime:
        return self._now_fn()

    def _metadata_bool(
        self,
        *,
        intent: ExecutionIntent,
        event: MarketEvent,
        key: str,
        default: bool = False,
    ) -> bool:
        if key in intent.metadata:
            return self._coerce_bool(intent.metadata[key])
        if key in event.metadata:
            return self._coerce_bool(event.metadata[key])
        return default

    def _daily_bucket(self, timestamp: str) -> str:
        parsed = self._parse_datetime(timestamp)
        if parsed is None:
            return "unknown"
        return parsed.date().isoformat()

    def _current_daily_submitted_notional(self, timestamp: str) -> float:
        bucket = self._daily_bucket(timestamp)
        return float(self._daily_submitted_notional_by_day.get(bucket, 0.0))

    def _record_daily_submitted_notional(self, *, timestamp: str, notional: float) -> None:
        if notional <= 0:
            return
        bucket = self._daily_bucket(timestamp)
        self._daily_submitted_notional_by_day[bucket] = (
            self._current_daily_submitted_notional(timestamp) + float(notional)
        )

    def _next_order_id(self, execution_scope: str) -> str:
        self._order_sequence += 1
        return f"{execution_scope}:clob:{self._order_sequence:08d}"

    def _append_lifecycle(
        self, lifecycle: list[dict[str, Any]], state: str, **details: Any
    ) -> None:
        payload: dict[str, Any] = {"state": state, "timestamp": _utc_now_iso()}
        payload.update(details)
        lifecycle.append(payload)

    def _append_audit_event(self, *, event_type: str, payload: dict[str, Any]) -> None:
        if self.audit_log_path is None:
            return
        self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)
        row = {
            "timestamp": _utc_now_iso(),
            "event_type": event_type,
            "execution_adapter": "polymarket_clob",
            "rollout_stage": self.rollout_stage,
            "payload": payload,
        }
        with self.audit_log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(row, sort_keys=True))
            handle.write("\n")
    @staticmethod
    def _extract_request_path(url: str) -> str:
        try:
            return str(urlparse(url).path or "/").strip()
        except Exception:
            return ""

    def _guarded_http_json_request(
        self,
        url: str,
        method: str,
        headers: dict[str, str],
        serialized_body: str | None,
        timeout_seconds: float,
    ) -> tuple[int | None, Any, str | None]:
        request_path = self._extract_request_path(url)
        if (
            request_path in self._L1_AUTH_ENDPOINT_PATHS
            and not self.allow_l1_auth_requests
        ):
            return None, None, "l1_auth_not_allowed_in_runtime_cycle"
        return self._raw_http_json_request_fn(
            url,
            method,
            headers,
            serialized_body,
            timeout_seconds,
        )

    @staticmethod
    def _default_http_json_request(
        url: str,
        method: str,
        headers: dict[str, str],
        serialized_body: str | None,
        timeout_seconds: float,
    ) -> tuple[int | None, Any, str | None]:
        request = Request(
            url=url,
            headers=headers,
            data=(
                serialized_body.encode("utf-8")
                if serialized_body is not None
                else None
            ),
            method=method.upper(),
        )
        try:
            with urlopen(request, timeout=timeout_seconds) as response:
                status_code = int(getattr(response, "status", response.getcode()))
                charset = response.headers.get_content_charset() or "utf-8"
                raw_payload = response.read().decode(charset, errors="replace")
        except HTTPError as exc:
            status_code = int(exc.code)
            charset = (
                exc.headers.get_content_charset()
                if exc.headers is not None
                else "utf-8"
            ) or "utf-8"
            raw_payload = exc.read().decode(charset, errors="replace")
            try:
                parsed_payload = json.loads(raw_payload)
            except json.JSONDecodeError:
                parsed_payload = raw_payload
            return status_code, parsed_payload, f"http_error:{status_code}"
        except (OSError, TimeoutError, URLError) as exc:
            return None, None, exc.__class__.__name__
        try:
            parsed_payload = json.loads(raw_payload)
        except json.JSONDecodeError:
            parsed_payload = raw_payload
        return status_code, parsed_payload, None

    def _resolve_poly_address(self) -> str | None:
        for env_var in (
            "POLYMARKET_ADDRESS",
            "POLYMARKET_SIGNER_ADDRESS",
            "POLYMARKET_WALLET_ADDRESS",
            "POLYMARKET_FUNDER_ADDRESS",
        ):
            value = str(self.environment.get(env_var, "")).strip()
            if value:
                return value
        private_key = str(self.environment.get("POLYMARKET_PRIVATE_KEY", "")).strip()
        if not private_key:
            return None
        try:  # pragma: no cover - optional dependency may not be installed in tests
            from eth_account import Account  # type: ignore[import-not-found]
        except Exception:  # pragma: no cover - defensive branch
            return None
        try:  # pragma: no cover - optional dependency may not be installed in tests
            return str(Account.from_key(private_key).address)
        except Exception:  # pragma: no cover - defensive branch
            return None

    @staticmethod
    def _decode_polymarket_api_secret(secret: str) -> bytes:
        normalized = secret.strip()
        if not normalized:
            raise ValueError("polymarket_api_secret_missing")
        padding = "=" * (-len(normalized) % 4)
        try:
            return base64.urlsafe_b64decode(normalized + padding)
        except Exception as exc:
            raise ValueError("polymarket_api_secret_invalid_base64") from exc

    def _build_l2_auth_headers(
        self,
        *,
        method: str,
        request_path: str,
        serialized_body: str | None = None,
    ) -> dict[str, str]:
        poly_address = self._resolve_poly_address()
        if not poly_address:
            raise ValueError("polymarket_address_missing")
        api_key = str(self.environment.get("POLYMARKET_API_KEY", "")).strip()
        if not api_key:
            raise ValueError("polymarket_api_key_missing")
        api_passphrase = str(
            self.environment.get("POLYMARKET_API_PASSPHRASE", "")
        ).strip()
        if not api_passphrase:
            raise ValueError("polymarket_api_passphrase_missing")
        api_secret = self._decode_polymarket_api_secret(
            str(self.environment.get("POLYMARKET_API_SECRET", ""))
        )
        timestamp = str(int(self._now().timestamp()))
        signature_payload = (
            f"{timestamp}{method.upper()}{request_path}"
            f"{serialized_body or ''}"
        )
        signature = base64.urlsafe_b64encode(
            hmac.new(
                api_secret,
                signature_payload.encode("utf-8"),
                hashlib.sha256,
            ).digest()
        ).decode("utf-8")
        return {
            "POLY_ADDRESS": poly_address,
            "POLY_SIGNATURE": signature,
            "POLY_TIMESTAMP": timestamp,
            "POLY_API_KEY": api_key,
            "POLY_PASSPHRASE": api_passphrase,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    @staticmethod
    def _extract_server_epoch_seconds(payload: Any) -> float | None:
        if isinstance(payload, dict):
            for key in (
                "timestamp",
                "serverTime",
                "server_time",
                "time",
                "epoch",
            ):
                if key not in payload:
                    continue
                value = payload.get(key)
                if isinstance(value, (int, float)):
                    return float(value)
                if isinstance(value, str):
                    parsed_datetime = PolymarketClobExecutionAdapter._parse_datetime(
                        value
                    )
                    if parsed_datetime is not None:
                        return parsed_datetime.timestamp()
                    try:
                        return float(value)
                    except ValueError:
                        continue
            return None
        if isinstance(payload, (int, float)):
            return float(payload)
        if isinstance(payload, str):
            parsed_datetime = PolymarketClobExecutionAdapter._parse_datetime(payload)
            if parsed_datetime is not None:
                return parsed_datetime.timestamp()
            try:
                return float(payload)
            except ValueError:
                return None
        return None

    @staticmethod
    def _is_geoblocked(payload: Any) -> bool:
        if isinstance(payload, dict):
            for key in (
                "blocked",
                "isBlocked",
                "geoBlocked",
                "geoblocked",
                "restricted",
                "isRestricted",
            ):
                if key in payload:
                    return bool(payload.get(key))
            for key in ("status", "result"):
                marker = str(payload.get(key, "")).strip().lower()
                if marker in {"blocked", "restricted", "denied"}:
                    return True
        return False

    def _run_auth_healthcheck(
        self,
        *,
        force: bool = False,
    ) -> tuple[list[str], dict[str, Any]]:
        metadata: dict[str, Any] = {
            "required": self.enforce_auth_healthcheck,
            "status": "skipped",
            "timeout_seconds": self.auth_healthcheck_timeout_seconds,
            "ttl_seconds": self.auth_healthcheck_ttl_seconds,
            "max_time_skew_seconds": self.auth_healthcheck_max_time_skew_seconds,
            "enable_geoblock_check": self.enable_geoblock_check,
            "geoblock_url": self.geoblock_url,
            "allow_l1_auth_requests": self.allow_l1_auth_requests,
            "cache_hit": False,
        }
        if not self.enforce_auth_healthcheck:
            metadata["skip_reason"] = "auth_healthcheck_not_required"
            return [], metadata

        now = self._now()
        if (
            not force
            and self._last_auth_healthcheck_at is not None
            and self._cached_auth_healthcheck is not None
            and (now - self._last_auth_healthcheck_at).total_seconds()
            <= self.auth_healthcheck_ttl_seconds
        ):
            cached_reasons, cached_metadata = self._cached_auth_healthcheck
            cached_copy = dict(cached_metadata)
            cached_copy["cache_hit"] = True
            return list(cached_reasons), cached_copy

        reasons: list[str] = []
        if self.enable_geoblock_check:
            geoblock_status, geoblock_payload, geoblock_error = (
                self._http_json_request_fn(
                    self.geoblock_url,
                    "GET",
                    {"Accept": "application/json"},
                    None,
                    self.auth_healthcheck_timeout_seconds,
                )
            )
            metadata["geoblock_status_code"] = geoblock_status
            metadata["geoblock_request_error"] = geoblock_error
            if geoblock_error is not None:
                reasons.append("geoblock_check_unavailable")
            elif geoblock_status is None or geoblock_status >= 400:
                reasons.append("geoblock_check_failed")
            else:
                geoblocked = self._is_geoblocked(geoblock_payload)
                metadata["geoblocked"] = geoblocked
                if geoblocked:
                    reasons.append("geoblocked")

        server_time_url = f"{self.clob_base_url}/time"
        time_status, time_payload, time_error = self._http_json_request_fn(
            server_time_url,
            "GET",
            {"Accept": "application/json"},
            None,
            self.auth_healthcheck_timeout_seconds,
        )
        metadata["server_time_status_code"] = time_status
        metadata["server_time_request_error"] = time_error
        if time_error is not None or time_status is None or time_status >= 400:
            reasons.append("clob_server_time_unavailable")
        else:
            server_epoch_seconds = self._extract_server_epoch_seconds(time_payload)
            metadata["server_epoch_seconds"] = server_epoch_seconds
            if server_epoch_seconds is None:
                reasons.append("clob_server_time_invalid")
            else:
                skew_seconds = abs(now.timestamp() - server_epoch_seconds)
                metadata["server_time_skew_seconds"] = round(skew_seconds, 6)
                if skew_seconds > self.auth_healthcheck_max_time_skew_seconds:
                    reasons.append("clob_server_time_skew_exceeded")

        auth_request_path = "/auth/api-keys"
        auth_url = f"{self.clob_base_url}{auth_request_path}"
        try:
            auth_headers = self._build_l2_auth_headers(
                method="GET",
                request_path=auth_request_path,
            )
        except ValueError as exc:
            metadata["l2_auth_header_error"] = str(exc)
            reasons.append(str(exc))
        else:
            auth_status, auth_payload, auth_error = self._http_json_request_fn(
                auth_url,
                "GET",
                auth_headers,
                None,
                self.auth_healthcheck_timeout_seconds,
            )
            metadata["l2_auth_status_code"] = auth_status
            metadata["l2_auth_request_error"] = auth_error
            if auth_error is not None:
                reasons.append("clob_l2_auth_request_failed")
            elif auth_status != 200:
                reasons.append("clob_l2_auth_failed")
            elif isinstance(auth_payload, list):
                metadata["l2_api_key_count"] = len(auth_payload)
            elif isinstance(auth_payload, dict):
                data_rows = auth_payload.get("data")
                if isinstance(data_rows, list):
                    metadata["l2_api_key_count"] = len(data_rows)

        deduped_reasons = list(dict.fromkeys(reasons))
        metadata["status"] = "passed" if not deduped_reasons else "failed"
        metadata["reasons"] = deduped_reasons
        metadata["checked_at"] = _utc_now_iso()
        self._last_auth_healthcheck_at = now
        self._cached_auth_healthcheck = (deduped_reasons, dict(metadata))
        return deduped_reasons, metadata

    def run_auth_healthcheck(
        self,
        *,
        force: bool = False,
    ) -> tuple[list[str], dict[str, Any]]:
        return self._run_auth_healthcheck(force=force)

    def _missing_required_env_vars(self) -> list[str]:
        missing: list[str] = []
        for var_name in self.required_env_vars:
            if not str(self.environment.get(var_name, "")).strip():
                missing.append(var_name)
        return missing

    def _validate_secret_controls(self) -> tuple[list[str], dict[str, Any]]:
        now = self._now()
        source_metadata_missing: list[str] = []
        rotation_metadata_missing: list[str] = []
        stale_secrets: list[str] = []
        disallowed_plaintext_sources: list[str] = []
        invalid_sources: list[str] = []
        secret_provenance: list[dict[str, Any]] = []

        for var_name in self.required_env_vars:
            source_env_var = f"{var_name}_SOURCE"
            source_value = str(self.environment.get(source_env_var, "")).strip().lower()
            rotated_env_var = f"{var_name}_LAST_ROTATED_AT"
            rotated_value = str(self.environment.get(rotated_env_var, "")).strip()
            rotated_at = self._parse_datetime(rotated_value)

            if not source_value:
                source_metadata_missing.append(var_name)
            if not rotated_value or rotated_at is None:
                rotation_metadata_missing.append(var_name)
            elif (now - rotated_at).total_seconds() > (self.max_secret_age_days * 86_400):
                stale_secrets.append(var_name)
            if (
                not self.allow_plaintext_secrets
                and source_value in {"env", "inline", "plaintext"}
            ):
                disallowed_plaintext_sources.append(var_name)
            if self.preferred_secret_sources and source_value:
                if source_value not in self.preferred_secret_sources:
                    invalid_sources.append(var_name)
            secret_provenance.append(
                {
                    "env_var": var_name,
                    "source": source_value or None,
                    "source_env_var": source_env_var,
                    "rotation_env_var": rotated_env_var,
                    "last_rotated_at": rotated_value or None,
                }
            )

        reasons: list[str] = []
        if source_metadata_missing:
            reasons.append("secret_source_metadata_missing")
        if rotation_metadata_missing:
            reasons.append("secret_rotation_metadata_missing")
        if stale_secrets:
            reasons.append("secret_rotation_stale")
        if disallowed_plaintext_sources:
            reasons.append("plaintext_secret_source_disallowed")
        if invalid_sources:
            reasons.append("secret_source_not_allowed")
        return reasons, {
            "secret_provenance": secret_provenance,
            "secret_source_metadata_missing": source_metadata_missing,
            "secret_rotation_metadata_missing": rotation_metadata_missing,
            "stale_secrets": stale_secrets,
            "plaintext_secret_source_disallowed": disallowed_plaintext_sources,
            "invalid_secret_sources": invalid_sources,
            "max_secret_age_days": self.max_secret_age_days,
            "preferred_secret_sources": list(self.preferred_secret_sources),
        }

    def _rejected_result(
        self,
        *,
        intent: ExecutionIntent,
        reason: str,
        metadata: dict[str, Any],
    ) -> ExecutionResult:
        return ExecutionResult(
            status="REJECTED",
            requested_notional=float(intent.requested_notional),
            filled_notional=0.0,
            reference_price=float(intent.reference_price),
            fill_price=None,
            slippage_bps=0,
            reasons=(reason,),
            metadata=metadata,
        )

    def cancel_order(self, *, order_id: str, reason: str) -> dict[str, Any]:
        order = self._open_orders.pop(order_id, None)
        if order is None:
            return {"order_id": order_id, "cancelled": False, "reason": "order_not_found"}
        order["status"] = "CANCELLED"
        order["cancel_reason"] = reason
        order["updated_at"] = _utc_now_iso()
        summary = {
            "order_id": order_id,
            "cancelled": True,
            "reason": reason,
            "remaining_notional": round(float(order["remaining_notional"]), 4),
        }
        self._append_audit_event(event_type="order_cancelled", payload=summary)
        return summary

    def cancel_all_open_orders(self, *, reason: str) -> dict[str, Any]:
        order_ids = list(self._open_orders.keys())
        cancelled_rows = [
            self.cancel_order(order_id=order_id, reason=reason) for order_id in order_ids
        ]
        cancelled_notional = round(
            sum(float(row.get("remaining_notional", 0.0)) for row in cancelled_rows),
            4,
        )
        summary = {
            "cancelled_order_count": len(
                [row for row in cancelled_rows if row.get("cancelled")]
            ),
            "cancelled_notional": cancelled_notional,
            "reason": reason,
            "cancelled_orders": cancelled_rows,
        }
        self._append_audit_event(event_type="cancel_all", payload=summary)
        return summary

    def _run_pretrade_checks(
        self, *, event: MarketEvent, intent: ExecutionIntent
    ) -> tuple[list[str], dict[str, Any]]:
        reasons: list[str] = []
        metadata: dict[str, Any] = {}
        requested_notional = float(intent.requested_notional)
        if requested_notional <= 0:
            reasons.append("invalid_requested_notional")
            return reasons, metadata
        if (
            self.max_order_notional_usd is not None
            and requested_notional > self.max_order_notional_usd
        ):
            reasons.append("max_order_notional_exceeded")
        current_daily_notional = self._current_daily_submitted_notional(intent.timestamp)
        metadata["daily_submitted_notional"] = round(current_daily_notional, 4)
        if (
            self.max_daily_notional_usd is not None
            and (current_daily_notional + requested_notional) > self.max_daily_notional_usd
        ):
            reasons.append("max_daily_notional_exceeded")
        if self.max_open_orders is not None and len(self._open_orders) >= self.max_open_orders:
            reasons.append("max_open_orders_exceeded")
        missing_market_metadata = [
            field for field in self.required_market_metadata if field not in event.metadata
        ]
        if missing_market_metadata:
            reasons.append("required_market_metadata_missing")
            metadata["missing_market_metadata"] = missing_market_metadata
        if self.require_pretrade_balance_checks:
            available_balance = self._metadata_float(
                event.metadata,
                keys=("available_balance_usd", "wallet_balance_usd", "balance_usd"),
            )
            allowance = self._metadata_float(
                event.metadata,
                keys=("allowance_usd", "collateral_allowance_usd", "trade_allowance_usd"),
            )
            metadata["available_balance_usd"] = available_balance
            metadata["allowance_usd"] = allowance
            if available_balance is None:
                reasons.append("pretrade_balance_missing")
            elif available_balance < requested_notional:
                reasons.append("pretrade_balance_insufficient")
            if allowance is None:
                reasons.append("pretrade_allowance_missing")
            elif allowance < requested_notional:
                reasons.append("pretrade_allowance_insufficient")
        return reasons, metadata

    def _load_user_channel_events(
        self, *, inline_events: Any
    ) -> tuple[list[dict[str, Any]], str | None]:
        events: list[dict[str, Any]] = []
        if isinstance(inline_events, list):
            events.extend(row for row in inline_events if isinstance(row, dict))
        source_error: str | None = None
        if self._user_channel_event_source is not None:
            try:
                sourced = self._user_channel_event_source()
            except Exception as exc:  # pragma: no cover - defensive branch
                source_error = f"user_channel_source_error:{exc.__class__.__name__}"
            else:
                if isinstance(sourced, list):
                    events.extend(row for row in sourced if isinstance(row, dict))
        return events, source_error

    def _reconcile_user_channel_events(
        self,
        *,
        current_order_id: str,
        current_filled_notional: float,
        inline_events: Any,
    ) -> dict[str, Any]:
        events, source_error = self._load_user_channel_events(inline_events=inline_events)
        matched_trade_ack_count = 0
        updates_applied = 0
        resolved_status: str | None = None
        resolved_filled_notional = float(current_filled_notional)

        for row in events:
            kind = str(row.get("kind", row.get("event_type", "order_update"))).strip()
            normalized_kind = kind.lower()
            order_id = str(row.get("order_id", "")).strip()
            timestamp = str(row.get("timestamp", "")).strip() or _utc_now_iso()

            if normalized_kind in {"heartbeat", "pong"}:
                heartbeat_at = self._parse_datetime(timestamp)
                self._last_user_channel_heartbeat_at = heartbeat_at or self._now()
                self._append_audit_event(
                    event_type="user_channel_heartbeat",
                    payload={"timestamp": timestamp, "kind": kind},
                )
                continue

            status = self._normalize_order_status(row.get("status"))
            if order_id == current_order_id:
                if normalized_kind in {"trade_ack", "ack", "order_update", "fill"}:
                    matched_trade_ack_count += 1
                if status is not None:
                    resolved_status = status
                filled_override = self._metadata_float(
                    row,
                    keys=("filled_notional", "filled_notional_usd"),
                )
                if filled_override is not None:
                    resolved_filled_notional = max(0.0, filled_override)
            if order_id and order_id in self._open_orders and status is not None:
                order = self._open_orders[order_id]
                requested_notional = float(order["requested_notional"])
                filled_override = self._metadata_float(
                    row,
                    keys=("filled_notional", "filled_notional_usd"),
                    default=float(order["filled_notional"]),
                )
                if filled_override is None:
                    filled_override = float(order["filled_notional"])
                filled_override = max(0.0, min(requested_notional, filled_override))
                order["filled_notional"] = round(filled_override, 4)
                order["remaining_notional"] = round(
                    max(0.0, requested_notional - filled_override), 4
                )
                order["status"] = status
                order["updated_at"] = timestamp
                updates_applied += 1
                if status in {"FILLED", "CANCELLED", "REJECTED"}:
                    self._open_orders.pop(order_id, None)
            self._append_audit_event(
                event_type="user_channel_event",
                payload={
                    "kind": kind,
                    "order_id": order_id,
                    "status": status,
                    "timestamp": timestamp,
                },
            )

        heartbeat_age_seconds: float | None = None
        if self._last_user_channel_heartbeat_at is not None:
            heartbeat_age_seconds = (
                self._now() - self._last_user_channel_heartbeat_at
            ).total_seconds()
            heartbeat_age_seconds = max(0.0, heartbeat_age_seconds)
        heartbeat_stale = heartbeat_age_seconds is None or (
            heartbeat_age_seconds > self.user_channel_max_staleness_seconds
        )
        return {
            "events_processed": len(events),
            "matched_trade_ack_count": matched_trade_ack_count,
            "updates_applied": updates_applied,
            "heartbeat_age_seconds": heartbeat_age_seconds,
            "heartbeat_stale": heartbeat_stale,
            "source_error": source_error,
            "resolved_status": resolved_status,
            "resolved_filled_notional": round(resolved_filled_notional, 4),
        }

    def _simulate_order_submission(
        self,
        *,
        event: MarketEvent,
        intent: ExecutionIntent,
        order_id: str,
        token_id: str,
        execution_scope: str,
        lifecycle: list[dict[str, Any]],
    ) -> dict[str, Any]:
        requested_notional = round(float(intent.requested_notional), 4)
        self._append_lifecycle(
            lifecycle,
            "SUBMITTED",
            order_id=order_id,
            requested_notional=requested_notional,
            execution_scope=execution_scope,
            token_id=token_id,
        )
        ack_status = str(event.metadata.get("clob_ack_status", "accepted")).strip().lower()
        if ack_status != "accepted":
            reject_reason = str(
                event.metadata.get("clob_reject_reason", "clob_order_rejected")
            ).strip() or "clob_order_rejected"
            self._append_lifecycle(
                lifecycle, "REJECTED", order_id=order_id, reason=reject_reason
            )
            self._append_audit_event(
                event_type="order_rejected",
                payload={"order_id": order_id, "reason": reject_reason},
            )
            return {
                "order_id": order_id,
                "status": "REJECTED",
                "reason": reject_reason,
                "filled_notional": 0.0,
                "remaining_notional": requested_notional,
                "fill_price": None,
                "slippage_bps": 0,
                "fee_paid": 0.0,
                "slippage_cost": 0.0,
                "total_execution_cost": 0.0,
            }

        fill_ratio = self._metadata_float(
            event.metadata,
            keys=("clob_fill_ratio",),
            default=1.0,
        )
        if fill_ratio is None:
            fill_ratio = 1.0
        fill_ratio = min(max(fill_ratio, 0.0), 1.0)
        filled_notional = round(requested_notional * fill_ratio, 4)
        remaining_notional = round(max(0.0, requested_notional - filled_notional), 4)
        slippage_bps = int(
            self._metadata_float(event.metadata, keys=("clob_slippage_bps",), default=0.0)
            or 0.0
        )
        fill_price: float | None = self._clamp_price(
            float(intent.reference_price) + (slippage_bps / 10_000)
        )
        fee_rate_bps = max(
            0.0,
            float(
                self._metadata_float(
                    event.metadata,
                    keys=("clob_fee_rate_bps",),
                    default=0.0,
                )
                or 0.0
            ),
        )
        fee_paid = round(filled_notional * (fee_rate_bps / 10_000), 4)
        slippage_cost = round(filled_notional * (slippage_bps / 10_000), 4)
        total_execution_cost = round(fee_paid + slippage_cost, 4)
        order_status = "FILLED"
        if remaining_notional > 0 and filled_notional > 0:
            order_status = "PARTIALLY_FILLED"
        elif filled_notional <= 0:
            order_status = "OPEN"
        if self._coerce_bool(event.metadata.get("clob_force_open_order", False)):
            order_status = "OPEN"
            filled_notional = 0.0
            remaining_notional = requested_notional
            fee_paid = 0.0
            slippage_cost = 0.0
            total_execution_cost = 0.0
            fill_price = None

        self._record_daily_submitted_notional(
            timestamp=intent.timestamp,
            notional=requested_notional,
        )
        order_payload = {
            "order_id": order_id,
            "token_id": token_id,
            "market_id": intent.market_id,
            "execution_scope": execution_scope,
            "requested_notional": requested_notional,
            "filled_notional": filled_notional,
            "remaining_notional": remaining_notional,
            "status": order_status,
            "reference_price": float(intent.reference_price),
            "fill_price": fill_price,
            "slippage_bps": slippage_bps,
            "fee_paid": fee_paid,
            "slippage_cost": slippage_cost,
            "total_execution_cost": total_execution_cost,
            "created_at": _utc_now_iso(),
            "updated_at": _utc_now_iso(),
        }
        if order_status in {"OPEN", "PARTIALLY_FILLED"}:
            self._open_orders[order_id] = dict(order_payload)
        self._append_lifecycle(
            lifecycle,
            order_status,
            order_id=order_id,
            filled_notional=filled_notional,
            remaining_notional=remaining_notional,
            slippage_bps=slippage_bps,
            fee_paid=fee_paid,
            total_execution_cost=total_execution_cost,
        )
        self._append_audit_event(event_type="order_submitted", payload=order_payload)
        return order_payload

    def skip(
        self, *, event: MarketEvent, risk_decision: RiskDecision
    ) -> ExecutionResult:
        del event
        reasons = risk_decision.reasons or ("risk_denied",)
        return ExecutionResult(
            status="SKIPPED",
            requested_notional=float(risk_decision.approved_notional),
            filled_notional=0.0,
            reference_price=0.0,
            fill_price=None,
            slippage_bps=0,
            reasons=tuple(f"risk:{reason}" for reason in reasons),
            metadata={
                "execution_adapter": "polymarket_clob",
                "rollout_stage": self.rollout_stage,
                "risk_allowed": risk_decision.allowed,
                "open_order_count": len(self._open_orders),
            },
        )

    def execute(
        self, *, event: MarketEvent, intent: ExecutionIntent
    ) -> ExecutionResult:
        execution_scope = str(
            intent.metadata.get(
                "execution_scope",
                event.metadata.get("execution_scope", ""),
            )
        ).strip() or "global"
        kill_switch_active = self._metadata_bool(
            intent=intent,
            event=event,
            key="kill_switch_active",
            default=False,
        )
        cancel_all_requested = self._metadata_bool(
            intent=intent,
            event=event,
            key="cancel_all_requested",
            default=False,
        )
        lifecycle: list[dict[str, Any]] = []
        self._append_lifecycle(
            lifecycle,
            "RECEIVED",
            execution_scope=execution_scope,
            requested_notional=float(intent.requested_notional),
        )
        metadata = {
            "execution_adapter": "polymarket_clob",
            "clob_base_url": self.clob_base_url,
            "rollout_stage": self.rollout_stage,
            "stage_enabled": self.stage_enabled,
            "real_order_submission": self.real_order_submission,
            "allow_real_trading": self.allow_real_trading,
            "enforce_auth_healthcheck": self.enforce_auth_healthcheck,
            "enable_geoblock_check": self.enable_geoblock_check,
            "allow_l1_auth_requests": self.allow_l1_auth_requests,
            "auth_healthcheck_timeout_seconds": self.auth_healthcheck_timeout_seconds,
            "auth_healthcheck_ttl_seconds": self.auth_healthcheck_ttl_seconds,
            "auth_healthcheck_max_time_skew_seconds": (
                self.auth_healthcheck_max_time_skew_seconds
            ),
            "required_env_vars": list(self.required_env_vars),
            "required_market_metadata": list(self.required_market_metadata),
            "require_pretrade_balance_checks": self.require_pretrade_balance_checks,
            "require_user_channel_trade_ack": self.require_user_channel_trade_ack,
            "require_kill_switch": self.require_kill_switch,
            "kill_switch_active": kill_switch_active,
            "cancel_all_requested": cancel_all_requested,
            "max_order_notional_usd": self.max_order_notional_usd,
            "max_daily_notional_usd": self.max_daily_notional_usd,
            "max_open_orders": self.max_open_orders,
            "open_order_count": len(self._open_orders),
            "user_channel_max_staleness_seconds": self.user_channel_max_staleness_seconds,
            "lifecycle": lifecycle,
        }
        if not self.stage_enabled:
            self._append_lifecycle(
                lifecycle,
                "REJECTED",
                reason="live_trading_disabled_by_rollout_stage",
            )
            return self._rejected_result(
                intent=intent,
                reason="live_trading_disabled_by_rollout_stage",
                metadata=metadata,
            )
        if not self.real_order_submission:
            self._append_lifecycle(
                lifecycle, "REJECTED", reason="real_order_submission_disabled"
            )
            return self._rejected_result(
                intent=intent,
                reason="real_order_submission_disabled",
                metadata=metadata,
            )
        if not self.allow_real_trading:
            self._append_lifecycle(
                lifecycle, "REJECTED", reason="real_trading_flag_not_enabled"
            )
            return self._rejected_result(
                intent=intent,
                reason="real_trading_flag_not_enabled",
                metadata=metadata,
            )
        if (
            self.require_kill_switch
            and "kill_switch_active" not in intent.metadata
            and "kill_switch_active" not in event.metadata
        ):
            self._append_lifecycle(
                lifecycle, "REJECTED", reason="kill_switch_state_unavailable"
            )
            return self._rejected_result(
                intent=intent,
                reason="kill_switch_state_unavailable",
                metadata=metadata,
            )
        if kill_switch_active:
            cancel_summary = self.cancel_all_open_orders(reason="kill_switch_active")
            metadata["cancel_all_summary"] = cancel_summary
            self._append_lifecycle(
                lifecycle,
                "REJECTED",
                reason="kill_switch_active",
                cancel_all_summary=cancel_summary,
            )
            return self._rejected_result(
                intent=intent,
                reason="kill_switch_active",
                metadata=metadata,
            )
        if cancel_all_requested:
            cancel_summary = self.cancel_all_open_orders(
                reason="operator_cancel_all_requested"
            )
            metadata["cancel_all_summary"] = cancel_summary
            self._append_lifecycle(
                lifecycle,
                "REJECTED",
                reason="cancel_all_requested",
                cancel_all_summary=cancel_summary,
            )
            return self._rejected_result(
                intent=intent,
                reason="cancel_all_requested",
                metadata=metadata,
            )
        missing_env_vars = self._missing_required_env_vars()
        if missing_env_vars:
            metadata_with_missing = dict(metadata)
            metadata_with_missing["missing_env_vars"] = missing_env_vars
            self._append_lifecycle(
                lifecycle,
                "REJECTED",
                reason="missing_polymarket_credentials",
                missing_env_vars=missing_env_vars,
            )
            return self._rejected_result(
                intent=intent,
                reason="missing_polymarket_credentials",
                metadata=metadata_with_missing,
            )
        secret_reasons, secret_metadata = self._validate_secret_controls()
        if secret_reasons:
            metadata_with_secret_controls = dict(metadata)
            metadata_with_secret_controls.update(secret_metadata)
            self._append_lifecycle(
                lifecycle,
                "REJECTED",
                reason=secret_reasons[0],
                secret_controls=secret_metadata,
            )
            return self._rejected_result(
                intent=intent,
                reason=secret_reasons[0],
                metadata=metadata_with_secret_controls,
            )
        auth_reasons, auth_metadata = self._run_auth_healthcheck(force=False)
        metadata_with_auth = dict(metadata)
        metadata_with_auth["auth_healthcheck"] = auth_metadata
        if auth_reasons:
            self._append_lifecycle(
                lifecycle,
                "REJECTED",
                reason=auth_reasons[0],
                auth_healthcheck=auth_metadata,
            )
            return self._rejected_result(
                intent=intent,
                reason=auth_reasons[0],
                metadata=metadata_with_auth,
            )
        metadata = metadata_with_auth
        token_id = str(event.metadata.get("token_id", "")).strip()
        if not token_id:
            self._append_lifecycle(
                lifecycle, "REJECTED", reason="token_id_missing_for_execution"
            )
            return self._rejected_result(
                intent=intent,
                reason="token_id_missing_for_execution",
                metadata=metadata,
            )
        pretrade_reasons, pretrade_checks = self._run_pretrade_checks(
            event=event,
            intent=intent,
        )
        if pretrade_reasons:
            metadata_with_pretrade = dict(metadata)
            metadata_with_pretrade["token_id"] = token_id
            metadata_with_pretrade["pretrade_checks"] = pretrade_checks
            self._append_lifecycle(
                lifecycle,
                "REJECTED",
                reason=pretrade_reasons[0],
                pretrade_checks=pretrade_checks,
            )
            return self._rejected_result(
                intent=intent,
                reason=pretrade_reasons[0],
                metadata=metadata_with_pretrade,
            )
        order_id = self._next_order_id(execution_scope)
        submitted_order = self._simulate_order_submission(
            event=event,
            intent=intent,
            order_id=order_id,
            token_id=token_id,
            execution_scope=execution_scope,
            lifecycle=lifecycle,
        )
        metadata_with_order = dict(metadata)
        metadata_with_order["token_id"] = token_id
        metadata_with_order["order_id"] = order_id
        metadata_with_order["pretrade_checks"] = pretrade_checks
        metadata_with_order["order_submission"] = submitted_order
        if submitted_order["status"] == "REJECTED":
            return self._rejected_result(
                intent=intent,
                reason=str(submitted_order.get("reason", "clob_order_rejected")),
                metadata=metadata_with_order,
            )

        reconciliation = self._reconcile_user_channel_events(
            current_order_id=order_id,
            current_filled_notional=float(submitted_order["filled_notional"]),
            inline_events=event.metadata.get("clob_user_events"),
        )
        metadata_with_order["reconciliation"] = reconciliation
        if reconciliation["source_error"] is not None:
            self._append_lifecycle(
                lifecycle,
                "REJECTED",
                reason="user_channel_source_unavailable",
                source_error=reconciliation["source_error"],
            )
            return self._rejected_result(
                intent=intent,
                reason="user_channel_source_unavailable",
                metadata=metadata_with_order,
            )
        if self.require_user_channel_trade_ack:
            if reconciliation["heartbeat_stale"]:
                self._append_lifecycle(
                    lifecycle,
                    "REJECTED",
                    reason="user_channel_heartbeat_stale",
                    reconciliation=reconciliation,
                )
                return self._rejected_result(
                    intent=intent,
                    reason="user_channel_heartbeat_stale",
                    metadata=metadata_with_order,
                )
            if reconciliation["matched_trade_ack_count"] <= 0:
                self._append_lifecycle(
                    lifecycle,
                    "REJECTED",
                    reason="user_channel_trade_ack_missing",
                    reconciliation=reconciliation,
                )
                self.cancel_order(
                    order_id=order_id,
                    reason="user_channel_trade_ack_missing",
                )
                return self._rejected_result(
                    intent=intent,
                    reason="user_channel_trade_ack_missing",
                    metadata=metadata_with_order,
                )

        resolved_status = reconciliation["resolved_status"] or str(submitted_order["status"])
        resolved_filled_notional = min(
            float(intent.requested_notional),
            max(0.0, float(reconciliation["resolved_filled_notional"])),
        )
        if resolved_status == "FILLED":
            resolved_filled_notional = float(intent.requested_notional)
            self._open_orders.pop(order_id, None)
        elif resolved_status == "PARTIALLY_FILLED":
            remaining = round(
                max(0.0, float(intent.requested_notional) - resolved_filled_notional),
                4,
            )
            if remaining <= 0:
                resolved_status = "FILLED"
                self._open_orders.pop(order_id, None)
            else:
                live_order = self._open_orders.get(order_id)
                if live_order is not None:
                    live_order["filled_notional"] = round(resolved_filled_notional, 4)
                    live_order["remaining_notional"] = remaining
                    live_order["status"] = "PARTIALLY_FILLED"
                    live_order["updated_at"] = _utc_now_iso()
        elif resolved_status in {"CANCELLED", "REJECTED"}:
            self._open_orders.pop(order_id, None)
        elif resolved_status == "OPEN":
            if order_id not in self._open_orders:
                self._open_orders[order_id] = {
                    "order_id": order_id,
                    "token_id": token_id,
                    "market_id": intent.market_id,
                    "execution_scope": execution_scope,
                    "requested_notional": float(intent.requested_notional),
                    "filled_notional": round(resolved_filled_notional, 4),
                    "remaining_notional": round(
                        max(0.0, float(intent.requested_notional) - resolved_filled_notional),
                        4,
                    ),
                    "status": "OPEN",
                    "created_at": _utc_now_iso(),
                    "updated_at": _utc_now_iso(),
                }

        slippage_bps = int(submitted_order["slippage_bps"])
        fill_price = submitted_order["fill_price"] if resolved_filled_notional > 0 else None
        fee_paid = round(
            float(submitted_order["fee_paid"])
            * (
                resolved_filled_notional / float(submitted_order["filled_notional"])
                if float(submitted_order["filled_notional"]) > 0
                else 0.0
            ),
            4,
        )
        slippage_cost = round(
            float(submitted_order["slippage_cost"])
            * (
                resolved_filled_notional / float(submitted_order["filled_notional"])
                if float(submitted_order["filled_notional"]) > 0
                else 0.0
            ),
            4,
        )
        total_execution_cost = round(fee_paid + slippage_cost, 4)
        metadata_with_order["open_order_count"] = len(self._open_orders)
        if resolved_status == "FILLED":
            self._append_lifecycle(
                lifecycle,
                "FILLED",
                order_id=order_id,
                filled_notional=round(resolved_filled_notional, 4),
                total_execution_cost=total_execution_cost,
            )
            return ExecutionResult(
                status="FILLED",
                requested_notional=float(intent.requested_notional),
                filled_notional=round(resolved_filled_notional, 4),
                reference_price=float(intent.reference_price),
                fill_price=fill_price,
                slippage_bps=slippage_bps,
                fee_paid=fee_paid,
                slippage_cost=slippage_cost,
                total_execution_cost=total_execution_cost,
                reasons=("clob_order_filled",),
                metadata=metadata_with_order,
            )
        if resolved_status == "PARTIALLY_FILLED" and resolved_filled_notional > 0:
            self._append_lifecycle(
                lifecycle,
                "PARTIALLY_FILLED",
                order_id=order_id,
                filled_notional=round(resolved_filled_notional, 4),
                remaining_notional=round(
                    max(0.0, float(intent.requested_notional) - resolved_filled_notional),
                    4,
                ),
                total_execution_cost=total_execution_cost,
            )
            return ExecutionResult(
                status="PARTIALLY_FILLED",
                requested_notional=float(intent.requested_notional),
                filled_notional=round(resolved_filled_notional, 4),
                reference_price=float(intent.reference_price),
                fill_price=fill_price,
                slippage_bps=slippage_bps,
                fee_paid=fee_paid,
                slippage_cost=slippage_cost,
                total_execution_cost=total_execution_cost,
                reasons=("clob_partial_fill",),
                metadata=metadata_with_order,
            )
        if resolved_status in {"CANCELLED", "REJECTED"}:
            self._append_lifecycle(
                lifecycle,
                "REJECTED",
                order_id=order_id,
                reason="clob_order_cancelled_or_rejected",
                resolved_status=resolved_status,
            )
            return self._rejected_result(
                intent=intent,
                reason="clob_order_cancelled_or_rejected",
                metadata=metadata_with_order,
            )
        self._append_lifecycle(
            lifecycle,
            "EXPIRED",
            order_id=order_id,
            reason="clob_order_open_pending_reconciliation",
        )
        return ExecutionResult(
            status="EXPIRED",
            requested_notional=float(intent.requested_notional),
            filled_notional=0.0,
            reference_price=float(intent.reference_price),
            fill_price=None,
            slippage_bps=0,
            reasons=("clob_order_open_pending_reconciliation",),
            metadata=metadata_with_order,
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

    def cancel_all_open_orders(self, *, reason: str) -> dict[str, Any]:
        cancel_fn = getattr(self.execution_adapter, "cancel_all_open_orders", None)
        if callable(cancel_fn):
            return cancel_fn(reason=reason)
        return {
            "cancelled_order_count": 0,
            "cancelled_notional": 0.0,
            "reason": reason,
            "supported": False,
        }

    def execute(
        self, *, event: MarketEvent, intent: ExecutionIntent
    ) -> ExecutionResult:
        raw_scope = intent.metadata.get("execution_scope")
        execution_scope = str(raw_scope).strip() if raw_scope is not None else ""
        if not execution_scope:
            execution_scope = "global"
        idempotency_key = (
            f"{execution_scope}:{intent.intent_id}:{event.timestamp}:"
            f"{intent.requested_notional:.4f}"
        )
        return self.gateway.execute(
            event=event,
            intent=intent,
            idempotency_key=idempotency_key,
        )
