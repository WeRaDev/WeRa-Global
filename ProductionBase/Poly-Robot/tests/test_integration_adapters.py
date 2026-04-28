from __future__ import annotations

import json
import socket
import sys
import tempfile
import unittest
from urllib.error import URLError
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from poly_robot.contracts import MarketEvent, RiskDecision  # noqa: E402
from poly_robot.integration_adapters import (  # noqa: E402
    ExecutionGatewayAdapter,
    HistoricalIngestionAdapter,
    LivePolymarketIngestionAdapter,
    PolymarketClobExecutionAdapter,
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


def _build_event(
    event_id: str = "evt-1", *, metadata: dict[str, object] | None = None
) -> MarketEvent:
    payload = _event_payload(event_id=event_id, timestamp="2026-01-01T00:00:00Z")
    if metadata is not None:
        payload["metadata"] = dict(metadata)
    return MarketEvent.from_dict(payload)


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

class LivePolymarketIngestionAdapterTests(unittest.TestCase):
    def test_normalizes_live_market_payload(self) -> None:
        payload = [
            {
                "id": "540816",
                "question": "Russia-Ukraine Ceasefire before GTA VI?",
                "updatedAt": "2026-04-26T14:55:01Z",
                "endDate": "2026-07-31T12:00:00Z",
                "liquidity": "47182.9661",
                "outcomePrices": "[\"0.525\", \"0.475\"]",
                "volume24hr": 5007.46185,
                "oneWeekPriceChange": 0.02,
            }
        ]
        adapter = LivePolymarketIngestionAdapter(
            source_url="https://example.test/markets",
            max_markets=5,
            min_volume_24h=0.0,
            max_retry_attempts=0,
            max_invalid_rows=0,
            fetch_json_fn=lambda _url, _timeout: payload,
        )

        batch = adapter.load_markets(timeout_seconds=1.0)

        self.assertEqual(batch.status, "OK")
        self.assertEqual(len(batch.events), 1)
        event = batch.events[0]
        self.assertTrue(event.event_id.startswith("540816:"))
        self.assertEqual(event.market_id, "540816")
        self.assertGreater(event.estimated_probability, event.midpoint)
        self.assertEqual(event.metadata["source"], "polymarket_gamma")
        self.assertEqual(
            event.metadata["probability_estimator_version"], "live_structured.v2"
        )
        self.assertIn(
            "weekly_change_component", event.metadata["probability_components"]
        )
        self.assertIn(
            "signal_agreement", event.metadata["probability_features"]
        )
        expected_raw_probability = round(
            event.midpoint + sum(event.metadata["probability_components"].values()),
            6,
        )
        self.assertAlmostEqual(
            event.metadata["raw_estimated_probability"],
            expected_raw_probability,
            places=6,
        )
        self.assertEqual(batch.metadata["selected_rows"], 1)

    def test_degraded_when_invalid_rows_are_within_budget(self) -> None:
        payload = [
            {"id": "missing-prices"},
            {
                "id": "540817",
                "question": "New Rihanna Album before GTA VI?",
                "updatedAt": "2026-04-26T14:56:01Z",
                "endDate": "2026-07-31T12:00:00Z",
                "outcomePrices": "[\"0.655\", \"0.345\"]",
                "liquidity": "30872.6836",
                "volume24hr": 374.250312,
                "oneWeekPriceChange": -0.01,
            },
        ]
        adapter = LivePolymarketIngestionAdapter(
            source_url="https://example.test/markets",
            max_markets=5,
            min_volume_24h=0.0,
            max_retry_attempts=0,
            max_invalid_rows=1,
            fetch_json_fn=lambda _url, _timeout: payload,
        )

        batch = adapter.load_markets(timeout_seconds=1.0)

        self.assertEqual(batch.status, "DEGRADED")
        self.assertEqual(len(batch.events), 1)
        self.assertIn("invalid_rows_skipped", batch.reasons)
        self.assertEqual(batch.metadata["invalid_rows"], 1)

    def test_retries_after_source_unavailable_then_succeeds(self) -> None:
        state = {"calls": 0}

        def fetch(_url: str, _timeout: float):
            state["calls"] += 1
            if state["calls"] == 1:
                raise OSError("temporary network issue")
            return [
                {
                    "id": "540818",
                    "question": "New Frank Ocean Album before GTA VI?",
                    "updatedAt": "2026-04-26T14:57:01Z",
                    "endDate": "2026-07-31T12:00:00Z",
                    "outcomePrices": "[\"0.321\", \"0.679\"]",
                    "liquidity": "61234.1",
                    "volume24hr": 1820.0,
                    "oneWeekPriceChange": 0.05,
                }
            ]

        adapter = LivePolymarketIngestionAdapter(
            source_url="https://example.test/markets",
            max_markets=5,
            min_volume_24h=0.0,
            max_retry_attempts=1,
            retry_backoff_seconds=0.0,
            max_invalid_rows=0,
            sleep_fn=lambda _seconds: None,
            fetch_json_fn=fetch,
        )

        batch = adapter.load_markets(timeout_seconds=1.0)

        self.assertEqual(state["calls"], 2)
        self.assertEqual(batch.status, "OK")
        self.assertEqual(len(batch.events), 1)

    def test_degraded_when_all_rows_filtered_out(self) -> None:
        payload = [
            {
                "id": "540821",
                "question": "Will test data be filtered out?",
                "updatedAt": "2026-04-26T14:58:01Z",
                "endDate": "2026-07-31T12:00:00Z",
                "outcomePrices": "[\"0.52\", \"0.48\"]",
                "liquidity": "1000.0",
                "volume24hr": 25.0,
                "oneWeekPriceChange": 0.01,
            }
        ]
        adapter = LivePolymarketIngestionAdapter(
            source_url="https://example.test/markets",
            max_markets=5,
            min_volume_24h=100.0,
            max_retry_attempts=0,
            max_invalid_rows=0,
            fetch_json_fn=lambda _url, _timeout: payload,
        )

        batch = adapter.load_markets(timeout_seconds=1.0)

        self.assertEqual(batch.status, "DEGRADED")
        self.assertEqual(batch.events, [])
        self.assertIn("no_markets_after_filters", batch.reasons)

    def test_classifies_urlerror_timeout_as_ingestion_timeout(self) -> None:
        def fetch(_url: str, _timeout: float):
            raise URLError(socket.timeout("timed out"))

        adapter = LivePolymarketIngestionAdapter(
            source_url="https://example.test/markets",
            max_markets=5,
            min_volume_24h=0.0,
            max_retry_attempts=0,
            max_invalid_rows=0,
            fetch_json_fn=fetch,
        )

        batch = adapter.load_markets(timeout_seconds=1.0)

        self.assertEqual(batch.status, "FAILED")
        self.assertEqual(batch.reasons, ("ingestion_timeout",))

    def test_wallet_convergence_can_trigger_whale_signal_without_liquidity(self) -> None:
        payload = [
            {
                "id": "540822",
                "question": "Can wallet convergence drive whale signal?",
                "updatedAt": "2026-04-26T15:10:01Z",
                "endDate": "2026-07-31T12:00:00Z",
                "outcomePrices": "[\"0.45\", \"0.55\"]",
                "liquidity": "1200.0",
                "volume24hr": 420.0,
                "oneWeekPriceChange": 0.02,
            }
        ]
        adapter = LivePolymarketIngestionAdapter(
            source_url="https://example.test/markets",
            max_markets=5,
            min_volume_24h=0.0,
            max_retry_attempts=0,
            max_invalid_rows=0,
            whale_signal_wallet_threshold=3.0,
            wallet_convergence_loader=lambda: {"540822": 4.0},
            fetch_json_fn=lambda _url, _timeout: payload,
        )

        batch = adapter.load_markets(timeout_seconds=1.0)

        self.assertEqual(batch.status, "OK")
        self.assertEqual(len(batch.events), 1)
        event = batch.events[0]
        self.assertTrue(event.check_signals["whale"])
        self.assertTrue(event.metadata["wallet_convergence_signal"])
        self.assertFalse(event.metadata["liquidity_whale_signal"])
        self.assertEqual(event.metadata["wallet_convergence_count"], 4.0)
        self.assertGreater(
            event.metadata["probability_features"]["wallet_convergence_score"], 0.0
        )
        self.assertGreater(
            event.metadata["probability_components"]["wallet_convergence_component"],
            0.0,
        )

    def test_degraded_when_wallet_convergence_loader_fails(self) -> None:
        payload = [
            {
                "id": "540823",
                "question": "Will loader failures degrade safely?",
                "updatedAt": "2026-04-26T15:11:01Z",
                "endDate": "2026-07-31T12:00:00Z",
                "outcomePrices": "[\"0.55\", \"0.45\"]",
                "liquidity": "42000.0",
                "volume24hr": 600.0,
                "oneWeekPriceChange": 0.03,
            }
        ]

        def failing_loader() -> dict[str, float]:
            raise OSError("wallet source unavailable")

        adapter = LivePolymarketIngestionAdapter(
            source_url="https://example.test/markets",
            max_markets=5,
            min_volume_24h=0.0,
            max_retry_attempts=0,
            max_invalid_rows=0,
            wallet_convergence_loader=failing_loader,
            fetch_json_fn=lambda _url, _timeout: payload,
        )

        batch = adapter.load_markets(timeout_seconds=1.0)

        self.assertEqual(batch.status, "DEGRADED")
        self.assertIn("wallet_signal_unavailable", batch.reasons)
        self.assertEqual(batch.metadata["wallet_signal_loader_error"], "OSError")

    def test_domain_wallet_convergence_can_drive_domain_basket_signal(self) -> None:
        payload = [
            {
                "id": "540824",
                "question": "Will domain convergence raise basket confidence?",
                "updatedAt": "2026-04-26T15:12:01Z",
                "endDate": "2026-07-31T12:00:00Z",
                "category": "Politics",
                "outcomePrices": "[\"0.49\", \"0.51\"]",
                "liquidity": "1800.0",
                "volume24hr": 380.0,
                "oneWeekPriceChange": 0.01,
            }
        ]
        adapter = LivePolymarketIngestionAdapter(
            source_url="https://example.test/markets",
            max_markets=5,
            min_volume_24h=0.0,
            max_retry_attempts=0,
            max_invalid_rows=0,
            whale_signal_wallet_threshold=3.0,
            wallet_convergence_loader=lambda: {
                "domains": {"politics": 4.0}
            },
            fetch_json_fn=lambda _url, _timeout: payload,
        )

        batch = adapter.load_markets(timeout_seconds=1.0)

        self.assertEqual(batch.status, "OK")
        self.assertEqual(batch.metadata["wallet_signal_domains"], 1)
        event = batch.events[0]
        self.assertEqual(event.metadata["domain_key"], "politics")
        self.assertEqual(event.metadata["domain_wallet_convergence_count"], 4.0)
        self.assertGreater(
            event.metadata["probability_components"]["domain_basket_component"],
            0.0,
        )

    def test_marks_complement_arb_candidate_when_constraints_pass(self) -> None:
        payload = [
            {
                "id": "540825",
                "question": "Is complement arbitrage feasible in paper mode?",
                "updatedAt": "2026-04-26T15:13:01Z",
                "endDate": "2026-07-31T12:00:00Z",
                "outcomePrices": "[\"0.45\", \"0.45\"]",
                "bestBid": "0.45",
                "bestAsk": "0.46",
                "tickSize": "0.01",
                "tokenId": "tok-540825",
                "availableBalanceUsd": 100.0,
                "allowanceUsd": 100.0,
                "liquidity": "2200.0",
                "volume24hr": 510.0,
                "oneWeekPriceChange": 0.02,
            }
        ]
        adapter = LivePolymarketIngestionAdapter(
            source_url="https://example.test/markets",
            max_markets=5,
            min_volume_24h=0.0,
            max_retry_attempts=0,
            max_invalid_rows=0,
            fetch_json_fn=lambda _url, _timeout: payload,
        )

        batch = adapter.load_markets(timeout_seconds=1.0)

        self.assertEqual(batch.status, "OK")
        event = batch.events[0]
        self.assertTrue(event.metadata["complement_arb_candidate"])
        self.assertTrue(event.metadata["complement_arb_signal"]["candidate"])
        self.assertEqual(
            event.metadata["complement_arb_signal"]["rejection_reasons"], []
        )

    def test_assigns_domain_allocation_budgets_to_selected_events(self) -> None:
        payload = [
            {
                "id": "540826",
                "question": "Will crypto market keep momentum?",
                "updatedAt": "2026-04-26T15:14:01Z",
                "endDate": "2026-07-31T12:00:00Z",
                "category": "Crypto",
                "outcomePrices": "[\"0.62\", \"0.38\"]",
                "liquidity": "2800.0",
                "volume24hr": 900.0,
                "oneWeekPriceChange": 0.03,
            },
            {
                "id": "540827",
                "question": "Will politics market reverse this week?",
                "updatedAt": "2026-04-26T15:15:01Z",
                "endDate": "2026-07-31T12:00:00Z",
                "category": "Politics",
                "outcomePrices": "[\"0.41\", \"0.59\"]",
                "liquidity": "2600.0",
                "volume24hr": 850.0,
                "oneWeekPriceChange": -0.01,
            },
        ]
        adapter = LivePolymarketIngestionAdapter(
            source_url="https://example.test/markets",
            max_markets=5,
            min_volume_24h=0.0,
            max_retry_attempts=0,
            max_invalid_rows=0,
            fetch_json_fn=lambda _url, _timeout: payload,
        )

        batch = adapter.load_markets(timeout_seconds=1.0)

        self.assertEqual(batch.status, "OK")
        allocation = batch.metadata["domain_budget_allocation"]
        self.assertIn("crypto", allocation)
        self.assertIn("politics", allocation)
        self.assertAlmostEqual(sum(allocation.values()), 1.0, places=5)
        for event in batch.events:
            self.assertIn("domain_allocation_budget", event.metadata)
            self.assertGreater(event.metadata["domain_allocation_budget"], 0.0)

class PolymarketClobExecutionAdapterTests(unittest.TestCase):
    def _build_adapter(
        self,
        *,
        stage_enabled: bool = True,
        real_order_submission: bool = True,
        allow_real_trading: bool = True,
        required_env_vars: tuple[str, ...] = (),
        require_pretrade_balance_checks: bool = False,
        require_user_channel_trade_ack: bool = False,
        require_kill_switch: bool = False,
        allow_plaintext_secrets: bool = True,
        environment: dict[str, str] | None = None,
    ) -> PolymarketClobExecutionAdapter:
        return PolymarketClobExecutionAdapter(
            clob_base_url="https://clob.polymarket.com",
            rollout_stage="canary_live",
            stage_enabled=stage_enabled,
            real_order_submission=real_order_submission,
            allow_real_trading=allow_real_trading,
            required_env_vars=required_env_vars,
            require_pretrade_balance_checks=require_pretrade_balance_checks,
            require_user_channel_trade_ack=require_user_channel_trade_ack,
            require_kill_switch=require_kill_switch,
            allow_plaintext_secrets=allow_plaintext_secrets,
            environment=environment,
        )

    def test_rejects_when_stage_disabled(self) -> None:
        adapter = self._build_adapter(
            stage_enabled=False,
            real_order_submission=True,
            allow_real_trading=True,
            required_env_vars=(),
            environment={},
        )
        result = adapter.execute(
            event=_build_event(metadata={"token_id": "1234"}),
            intent=_build_intent(),
        )

        self.assertEqual(result.status, "REJECTED")
        self.assertEqual(
            result.reasons,
            ("live_trading_disabled_by_rollout_stage",),
        )

    def test_rejects_when_required_credentials_are_missing(self) -> None:
        adapter = self._build_adapter(
            required_env_vars=("POLYMARKET_API_KEY", "POLYMARKET_API_SECRET"),
            environment={"POLYMARKET_API_KEY": "key-present"},
        )
        result = adapter.execute(
            event=_build_event(metadata={"token_id": "1234"}),
            intent=_build_intent(),
        )

        self.assertEqual(result.status, "REJECTED")
        self.assertEqual(result.reasons, ("missing_polymarket_credentials",))
        self.assertEqual(
            result.metadata["missing_env_vars"],
            ["POLYMARKET_API_SECRET"],
        )

    def test_rejects_when_secret_source_metadata_missing(self) -> None:
        adapter = self._build_adapter(
            required_env_vars=("POLYMARKET_API_KEY",),
            environment={"POLYMARKET_API_KEY": "key-present"},
        )
        result = adapter.execute(
            event=_build_event(metadata={"token_id": "1234"}),
            intent=_build_intent(),
        )

        self.assertEqual(result.status, "REJECTED")
        self.assertEqual(result.reasons, ("secret_source_metadata_missing",))

    def test_rejects_when_token_id_is_missing(self) -> None:
        adapter = self._build_adapter(required_env_vars=(), environment={})
        result = adapter.execute(event=_build_event(metadata={}), intent=_build_intent())

        self.assertEqual(result.status, "REJECTED")
        self.assertEqual(result.reasons, ("token_id_missing_for_execution",))

    def test_fills_order_when_gates_pass(self) -> None:
        adapter = self._build_adapter(
            required_env_vars=("POLYMARKET_API_KEY",),
            environment={
                "POLYMARKET_API_KEY": "key-present",
                "POLYMARKET_API_KEY_SOURCE": "vault",
                "POLYMARKET_API_KEY_LAST_ROTATED_AT": "2099-01-01T00:00:00Z",
            },
        )
        result = adapter.execute(
            event=_build_event(metadata={"token_id": "9876"}),
            intent=_build_intent(),
        )

        self.assertEqual(result.status, "FILLED")
        self.assertEqual(result.reasons, ("clob_order_filled",))
        self.assertEqual(result.filled_notional, 100.0)
        self.assertEqual(result.metadata["token_id"], "9876")

    def test_rejects_when_kill_switch_is_active(self) -> None:
        adapter = self._build_adapter(
            require_kill_switch=True,
            required_env_vars=("POLYMARKET_API_KEY",),
            environment={
                "POLYMARKET_API_KEY": "key-present",
                "POLYMARKET_API_KEY_SOURCE": "vault",
                "POLYMARKET_API_KEY_LAST_ROTATED_AT": "2026-01-01T00:00:00Z",
            },
        )
        result = adapter.execute(
            event=_build_event(metadata={"token_id": "9876", "kill_switch_active": True}),
            intent=_build_intent(),
        )

        self.assertEqual(result.status, "REJECTED")
        self.assertEqual(result.reasons, ("kill_switch_active",))

    def test_rejects_when_cancel_all_requested(self) -> None:
        adapter = self._build_adapter(
            required_env_vars=("POLYMARKET_API_KEY",),
            environment={
                "POLYMARKET_API_KEY": "key-present",
                "POLYMARKET_API_KEY_SOURCE": "vault",
                "POLYMARKET_API_KEY_LAST_ROTATED_AT": "2026-01-01T00:00:00Z",
            },
        )
        result = adapter.execute(
            event=_build_event(
                metadata={"token_id": "9876", "cancel_all_requested": True}
            ),
            intent=_build_intent(),
        )

        self.assertEqual(result.status, "REJECTED")
        self.assertEqual(result.reasons, ("cancel_all_requested",))

    def test_skip_maps_risk_reasons(self) -> None:
        adapter = self._build_adapter(
            stage_enabled=True,
            real_order_submission=False,
            allow_real_trading=False,
            required_env_vars=(),
            environment={},
        )
        risk_decision = RiskDecision(
            allowed=False,
            approved_notional=0.0,
            approved_fraction=0.0,
            kill_switch=False,
            reasons=("daily_loss_limit_exceeded",),
        )
        result = adapter.skip(event=_build_event(), risk_decision=risk_decision)

        self.assertEqual(result.status, "SKIPPED")
        self.assertEqual(result.reasons, ("risk:daily_loss_limit_exceeded",))


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
