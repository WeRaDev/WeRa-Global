from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from poly_robot.contracts import MarketEvent  # noqa: E402
from poly_robot.integration_adapters import (  # noqa: E402
    ExecutionGatewayAdapter,
    HistoricalIngestionAdapter,
)
from poly_robot.paper_execution import ExecutionIntent, ExecutionResult  # noqa: E402


def _event_payload(event_id: str, timestamp: str) -> dict:
    return {
        "schema_version": "replay_event.v1",
        "event_id": event_id,
        "timestamp": timestamp,
        "market_id": "mkt-1",
        "question": "Will this test pass?",
        "midpoint": 0.62,
        "estimated_probability": 0.78,
        "bids_depth_usd": 1800.0,
        "asks_depth_usd": 1800.0,
        "liquidity_usd": 90000.0,
        "hours_to_resolution": 24.0,
        "check_signals": {},
        "base_confidence": 0.8,
        "llm_confidence": 0.9,
        "consensus_buy_votes": 2,
        "metadata": {},
    }


def _write_jsonl(path: Path, rows: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")


def _build_event(event_id: str = "evt-1") -> MarketEvent:
    return MarketEvent.from_dict(
        _event_payload(event_id=event_id, timestamp="2026-01-01T00:00:00Z")
    )


def _build_intent() -> ExecutionIntent:
    return ExecutionIntent(
        intent_id="evt-1:BUY",
        event_id="evt-1",
        timestamp="2026-01-01T00:00:00Z",
        market_id="mkt-1",
        side="BUY",
        requested_notional=100.0,
        reference_price=0.62,
        max_slippage_bps=50,
        ttl_seconds=300,
        metadata={},
    )


def _success_execution_result() -> ExecutionResult:
    return ExecutionResult(
        status="FILLED",
        requested_notional=100.0,
        filled_notional=100.0,
        reference_price=0.62,
        fill_price=0.625,
        slippage_bps=8,
        fee_paid=0.1,
        slippage_cost=0.08,
        total_execution_cost=0.18,
        reasons=("paper_fill_simulated",),
        metadata={},
    )


class HistoricalIngestionAdapterTests(unittest.TestCase):
    def test_degraded_when_invalid_rows_are_within_budget(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            path = root / "events.jsonl"
            _write_jsonl(
                path,
                [
                    json.dumps(_event_payload("evt-1", "2026-01-01T00:00:00Z")),
                    '{"not":"valid_event"}',
                    json.dumps(_event_payload("evt-2", "2026-01-01T00:01:00Z")),
                ],
            )
            adapter = HistoricalIngestionAdapter(max_invalid_rows=1)
            batch = adapter.load_jsonl(path, timeout_seconds=2.0)

            self.assertEqual(batch.status, "DEGRADED")
            self.assertEqual(len(batch.events), 2)
            self.assertIn("invalid_rows_skipped", batch.reasons)
            self.assertEqual(batch.metadata["invalid_rows"], 1)

    def test_fails_when_invalid_row_budget_is_exceeded(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            path = root / "events.jsonl"
            _write_jsonl(
                path,
                [
                    json.dumps(_event_payload("evt-1", "2026-01-01T00:00:00Z")),
                    '{"not":"valid_event"}',
                ],
            )
            adapter = HistoricalIngestionAdapter(max_invalid_rows=0)
            batch = adapter.load_jsonl(path, timeout_seconds=2.0)

            self.assertEqual(batch.status, "FAILED")
            self.assertEqual(batch.reasons, ("invalid_row_budget_exceeded",))
            self.assertEqual(batch.events, [])

    def test_degraded_when_duplicate_event_ids_are_skipped(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            path = root / "events.jsonl"
            payload = json.dumps(_event_payload("evt-dup", "2026-01-01T00:00:00Z"))
            _write_jsonl(path, [payload, payload])

            adapter = HistoricalIngestionAdapter(
                max_invalid_rows=0, deduplicate_event_ids=True
            )
            batch = adapter.load_jsonl(path, timeout_seconds=2.0)

            self.assertEqual(batch.status, "DEGRADED")
            self.assertEqual(len(batch.events), 1)
            self.assertIn("duplicate_rows_skipped", batch.reasons)
            self.assertEqual(batch.metadata["duplicate_rows"], 1)

    def test_degraded_when_non_monotonic_timestamps_are_detected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            path = root / "events.jsonl"
            _write_jsonl(
                path,
                [
                    json.dumps(_event_payload("evt-1", "2026-01-01T00:00:02Z")),
                    json.dumps(_event_payload("evt-2", "2026-01-01T00:00:01Z")),
                ],
            )
            adapter = HistoricalIngestionAdapter(
                max_invalid_rows=0,
                fail_on_monotonic_violation=False,
            )
            batch = adapter.load_jsonl(path, timeout_seconds=2.0)

            self.assertEqual(batch.status, "DEGRADED")
            self.assertEqual(len(batch.events), 2)
            self.assertIn("non_monotonic_rows_detected", batch.reasons)
            self.assertEqual(batch.metadata["monotonic_violations"], 1)


class ExecutionGatewayAdapterTests(unittest.TestCase):
    def test_retries_and_succeeds(self) -> None:
        state = {"calls": 0}

        def execute_fn(*, event, intent):
            state["calls"] += 1
            if state["calls"] == 1:
                raise RuntimeError("transient")
            return _success_execution_result()

        gateway = ExecutionGatewayAdapter(
            execute_fn=execute_fn,
            max_retry_attempts=1,
            retry_backoff_seconds=0.0,
            timeout_seconds=2.0,
        )
        result = gateway.execute(
            event=_build_event(),
            intent=_build_intent(),
            idempotency_key="idemp-1",
        )

        self.assertEqual(state["calls"], 2)
        self.assertEqual(result.status, "FILLED")
        self.assertEqual(result.metadata["execution_gateway"]["attempt_count"], 2)
        self.assertFalse(result.metadata["execution_gateway"]["degraded_mode"])

    def test_degrades_on_timeout(self) -> None:
        time_values = iter([0.0, 5.0])

        def monotonic() -> float:
            return next(time_values)

        gateway = ExecutionGatewayAdapter(
            execute_fn=lambda **_: _success_execution_result(),
            max_retry_attempts=0,
            retry_backoff_seconds=0.0,
            timeout_seconds=1.0,
            monotonic_fn=monotonic,
        )
        result = gateway.execute(
            event=_build_event(),
            intent=_build_intent(),
            idempotency_key="idemp-timeout",
        )

        self.assertEqual(result.status, "REJECTED")
        self.assertIn("execution_gateway_degraded", result.reasons)
        self.assertIn("execution_gateway_timeout", result.reasons)
        self.assertTrue(result.metadata["execution_gateway"]["degraded_mode"])

    def test_idempotency_cache_prevents_duplicate_execution(self) -> None:
        state = {"calls": 0}

        def execute_fn(*, event, intent):
            state["calls"] += 1
            return _success_execution_result()

        gateway = ExecutionGatewayAdapter(
            execute_fn=execute_fn,
            max_retry_attempts=0,
            retry_backoff_seconds=0.0,
            timeout_seconds=2.0,
        )
        first = gateway.execute(
            event=_build_event(),
            intent=_build_intent(),
            idempotency_key="idemp-cache",
        )
        second = gateway.execute(
            event=_build_event(),
            intent=_build_intent(),
            idempotency_key="idemp-cache",
        )

        self.assertEqual(state["calls"], 1)
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
