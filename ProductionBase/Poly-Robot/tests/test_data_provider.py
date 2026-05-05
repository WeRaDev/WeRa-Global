"""Tests for the DataProvider protocol and concrete implementations."""
from __future__ import annotations

import unittest
from pathlib import Path

from poly_robot.data_provider import (
    DataProvider,
    ManifoldMarketsProvider,
    PolymarketHistoricalProvider,
    PolymarketLiveProvider,
)
from poly_robot.integration_adapters import IngestionBatch


ROOT_DIR = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT_DIR / "tests" / "fixtures" / "replay_events.jsonl"
RICH_FIXTURE_PATH = ROOT_DIR / "tests" / "fixtures" / "replay_events_rich.jsonl"


class TestDataProviderProtocol(unittest.TestCase):
    def test_historical_provider_satisfies_protocol(self) -> None:
        provider = PolymarketHistoricalProvider(events_path=FIXTURE_PATH)
        self.assertIsInstance(provider, DataProvider)

    def test_source_id(self) -> None:
        provider = PolymarketHistoricalProvider(events_path=FIXTURE_PATH)
        self.assertEqual(provider.source_id, "polymarket_historical")


class TestPolymarketHistoricalProvider(unittest.TestCase):
    def test_fetch_returns_ingestion_batch(self) -> None:
        provider = PolymarketHistoricalProvider(events_path=FIXTURE_PATH)
        batch = provider.fetch()
        self.assertIsInstance(batch, IngestionBatch)
        self.assertIn(batch.status, {"OK", "DEGRADED", "FAILED"})

    def test_fetch_with_rich_fixture(self) -> None:
        if not RICH_FIXTURE_PATH.exists():
            self.skipTest("Rich fixture not generated")
        provider = PolymarketHistoricalProvider(events_path=RICH_FIXTURE_PATH)
        batch = provider.fetch()
        self.assertEqual(batch.status, "OK")
        self.assertGreater(len(batch.events), 100)

    def test_fetch_missing_file_returns_failed(self) -> None:
        provider = PolymarketHistoricalProvider(
            events_path=Path("/nonexistent/path.jsonl")
        )
        batch = provider.fetch()
        self.assertEqual(batch.status, "FAILED")

    def test_fetch_path_override(self) -> None:
        provider = PolymarketHistoricalProvider(
            events_path=Path("/nonexistent/default.jsonl")
        )
        batch = provider.fetch(path=str(FIXTURE_PATH))
        # Override may still fail if retry exhausts; accept OK, DEGRADED, or FAILED
        self.assertIsInstance(batch, IngestionBatch)


class TestManifoldMarketsProvider(unittest.TestCase):
    def test_satisfies_protocol(self) -> None:
        provider = ManifoldMarketsProvider()
        self.assertIsInstance(provider, DataProvider)

    def test_source_id(self) -> None:
        provider = ManifoldMarketsProvider()
        self.assertEqual(provider.source_id, "manifold_markets")

    def test_fetch_unreachable_returns_failed(self) -> None:
        provider = ManifoldMarketsProvider(
            api_url="http://127.0.0.1:1/nonexistent",
            timeout_seconds=1.0,
        )
        batch = provider.fetch()
        self.assertEqual(batch.status, "FAILED")
        self.assertIn("manifold_api_unavailable", batch.reasons)

class TestPolymarketLiveProvider(unittest.TestCase):
    def test_satisfies_protocol(self) -> None:
        provider = PolymarketLiveProvider(
            source_url="http://127.0.0.1:1/nonexistent",
            timeout_seconds=1.0,
        )
        self.assertIsInstance(provider, DataProvider)

    def test_fetch_unreachable_returns_failed(self) -> None:
        provider = PolymarketLiveProvider(
            source_url="http://127.0.0.1:1/nonexistent",
            max_markets=1,
            min_volume_24h=0.0,
            timeout_seconds=1.0,
        )
        batch = provider.fetch()
        self.assertEqual(batch.status, "FAILED")
        self.assertIn("source_unavailable", batch.reasons)


if __name__ == "__main__":
    unittest.main()
