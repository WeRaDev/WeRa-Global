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
