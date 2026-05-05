"""Data provider abstraction for Poly-Robot (ADR-002 Phase 2).

Defines a typed protocol for market data ingestion that decouples the
orchestrator from specific data source implementations. Concrete providers
wrap existing adapters and can be composed or swapped without changing
the decision loop.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from .integration_adapters import (
    HistoricalIngestionAdapter,
    IngestionBatch,
    LivePolymarketIngestionAdapter,
)
from .shared.contracts import MarketEvent


@runtime_checkable
class DataProvider(Protocol):
    """Protocol for market data providers.

    Each provider must expose a source identifier and implement
    the ``fetch`` method to produce an ``IngestionBatch`` of
    ``MarketEvent`` instances.
    """

    @property
    def source_id(self) -> str:
        """Short identifier for the data source (e.g. 'polymarket', 'manifold')."""
        ...

    def fetch(self, **kwargs: Any) -> IngestionBatch:
        """Fetch the next batch of market events.

        Keyword arguments are provider-specific (e.g. path for historical,
        URL/filters for live).
        """
        ...


@dataclass
class PolymarketHistoricalProvider:
    """DataProvider wrapping HistoricalIngestionAdapter for replay fixtures."""

    events_path: Path
    adapter: HistoricalIngestionAdapter = field(
        default_factory=HistoricalIngestionAdapter
    )
    timeout_seconds: float | None = None

    @property
    def source_id(self) -> str:
        return "polymarket_historical"

    def fetch(self, **kwargs: Any) -> IngestionBatch:
        path = kwargs.get("path", self.events_path)
        if isinstance(path, str):
            path = Path(path)
        return self.adapter.load_jsonl(
            path, timeout_seconds=self.timeout_seconds
        )


@dataclass
class ManifoldMarketsProvider:
    """Synthetic DataProvider producing MarketEvent from Manifold Markets schema.

    Validates the DataProvider abstraction with a non-Polymarket source.
    Converts Manifold-style market data (probability, volume, liquidity)
    into the canonical MarketEvent format used by the orchestrator.
    """

    api_url: str = "https://api.manifold.markets/v0/markets"
    max_markets: int = 20
    timeout_seconds: float = 15.0

    @property
    def source_id(self) -> str:
        return "manifold_markets"

    def fetch(self, **kwargs: Any) -> IngestionBatch:
        """Fetch markets from Manifold Markets API and convert to MarketEvent."""
        import json as _json
        from datetime import UTC, datetime
        from urllib.error import URLError
        from urllib.request import Request, urlopen

        url = kwargs.get("api_url", self.api_url)
        limit = kwargs.get("max_markets", self.max_markets)
        timeout = kwargs.get("timeout_seconds", self.timeout_seconds)
        request_url = f"{url}?limit={limit}&sort=most-popular"

        try:
            req = Request(request_url, headers={"Accept": "application/json"})
            with urlopen(req, timeout=timeout) as resp:
                raw = _json.loads(resp.read().decode("utf-8"))
        except (URLError, TimeoutError, OSError) as exc:
            return IngestionBatch(
                status="FAILED",
                events=[],
                reasons=("manifold_api_unavailable",),
                metadata={"error": str(exc), "url": request_url},
            )

        if not isinstance(raw, list):
            return IngestionBatch(
                status="FAILED",
                events=[],
                reasons=("manifold_unexpected_response_format",),
            )

        from .shared.schemas import EVENT_SCHEMA_VERSION

        now_iso = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
        events = []
        for market in raw:
            if not isinstance(market, dict):
                continue
            prob = market.get("probability")
            if prob is None or not isinstance(prob, (int, float)):
                continue
            market_id = str(market.get("id", "")).strip()
            if not market_id:
                continue
            volume = float(market.get("volume", 0) or 0)
            liquidity = float(market.get("totalLiquidity", 0) or 0)
            close_time = market.get("closeTime")
            hours_to_res = 48.0
            if isinstance(close_time, (int, float)) and close_time > 0:
                remaining_ms = close_time - datetime.now(UTC).timestamp() * 1000
                hours_to_res = max(1.0, remaining_ms / 3_600_000)

            midpoint = max(0.01, min(0.99, float(prob)))
            est_prob = max(0.01, min(0.99, midpoint + 0.02))
            depth = max(100.0, liquidity * 0.005)

            events.append(MarketEvent(
                event_id=f"manifold-{market_id}",
                timestamp=now_iso,
                market_id=f"manifold:{market_id}",
                question=str(market.get("question", ""))[:256],
                midpoint=round(midpoint, 6),
                estimated_probability=round(est_prob, 6),
                bids_depth_usd=round(depth, 2),
                asks_depth_usd=round(depth, 2),
                liquidity_usd=round(liquidity, 2),
                hours_to_resolution=round(hours_to_res, 1),
                check_signals={},
                base_confidence=0.55,
                consensus_buy_votes=1,
                metadata={"source": "manifold_markets", "volume_usd": round(volume, 2)},
                schema_version=EVENT_SCHEMA_VERSION,
            ))

        if not events:
            return IngestionBatch(
                status="DEGRADED",
                events=[],
                reasons=("no_markets_after_conversion",),
                metadata={"raw_market_count": len(raw)},
            )

        return IngestionBatch(
            status="OK",
            events=events,
            metadata={"raw_market_count": len(raw), "converted_count": len(events)},
        )


@dataclass
class PolymarketLiveProvider:
    """DataProvider wrapping LivePolymarketIngestionAdapter for real-time data."""

    source_url: str = "https://gamma-api.polymarket.com/markets?active=true&closed=false&limit=50"
    max_markets: int = 10
    min_volume_24h: float = 300.0
    timeout_seconds: float = 30.0

    @property
    def source_id(self) -> str:
        return "polymarket_live"

    def fetch(self, **kwargs: Any) -> IngestionBatch:
        adapter = LivePolymarketIngestionAdapter(
            source_url=kwargs.get("source_url", self.source_url),
            max_markets=kwargs.get("max_markets", self.max_markets),
            min_volume_24h=kwargs.get("min_volume_24h", self.min_volume_24h),
            timeout_seconds=kwargs.get("timeout_seconds", self.timeout_seconds),
        )
        return adapter.fetch()
