from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from poly_robot.contracts import MarketEvent, RiskDecision  # noqa: E402
from poly_robot.paper_execution import (  # noqa: E402
    PaperExecutionAdapter,
    build_execution_intent,
)


PROFILE_PATH = ROOT_DIR / "config" / "parameters" / "profiles" / "mvp_test_token.v1.json"


def _load_parameters() -> dict:
    payload = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    return payload["values"]


def _build_event(**overrides) -> MarketEvent:
    payload = {
        "schema_version": "replay_event.v1",
        "event_id": "evt-exec-1",
        "timestamp": "2026-01-01T00:00:00Z",
        "market_id": "mkt-exec",
        "question": "Execution test market?",
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
    payload.update(overrides)
    return MarketEvent.from_dict(payload)


def _allowed_risk_decision(notional: float) -> RiskDecision:
    return RiskDecision(
        allowed=True,
        approved_notional=notional,
        approved_fraction=0.1,
        kill_switch=False,
        reasons=("consensus_full_size",),
    )


class PaperExecutionAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.parameters = _load_parameters()
        self.adapter = PaperExecutionAdapter(self.parameters)

    def test_fills_when_slippage_and_ttl_are_within_limits(self) -> None:
        event = _build_event()
        intent = build_execution_intent(
            event=event,
            risk_decision=_allowed_risk_decision(120.0),
            parameters=self.parameters,
        )
        result = self.adapter.execute(event=event, intent=intent)

        self.assertEqual(result.status, "FILLED")
        self.assertEqual(result.filled_notional, intent.requested_notional)
        self.assertLessEqual(result.slippage_bps, intent.max_slippage_bps)
        self.assertGreater(result.fee_paid, 0.0)
        self.assertGreater(result.slippage_cost, 0.0)
        self.assertGreater(result.total_execution_cost, 0.0)

    def test_partial_fill_when_orderbook_capacity_is_limited(self) -> None:
        event = _build_event(bids_depth_usd=100.0, asks_depth_usd=100.0, liquidity_usd=90000.0)
        intent = build_execution_intent(
            event=event,
            risk_decision=_allowed_risk_decision(100.0),
            parameters=self.parameters,
        )
        result = self.adapter.execute(event=event, intent=intent)

        self.assertEqual(result.status, "PARTIALLY_FILLED")
        self.assertEqual(result.filled_notional, 80.0)
        self.assertIn("partial_fill_depth_limited", result.reasons)

    def test_rejects_when_slippage_budget_is_breached(self) -> None:
        event = _build_event(bids_depth_usd=10.0, asks_depth_usd=10.0, liquidity_usd=500.0)
        intent = build_execution_intent(
            event=event,
            risk_decision=_allowed_risk_decision(150.0),
            parameters=self.parameters,
        )
        result = self.adapter.execute(event=event, intent=intent)

        self.assertEqual(result.status, "REJECTED")
        self.assertIn("slippage_limit_breached_after_retries", result.reasons)

    def test_expires_when_latency_exceeds_order_ttl(self) -> None:
        event = _build_event(metadata={"execution_latency_ms": 500_000})
        intent = build_execution_intent(
            event=event,
            risk_decision=_allowed_risk_decision(80.0),
            parameters=self.parameters,
        )
        result = self.adapter.execute(event=event, intent=intent)

        self.assertEqual(result.status, "EXPIRED")
        self.assertIn("order_ttl_exceeded", result.reasons)

    def test_cancel_replace_flow_can_convert_reject_to_partial_fill(self) -> None:
        event = _build_event(bids_depth_usd=100.0, asks_depth_usd=100.0, liquidity_usd=2000.0)
        intent = build_execution_intent(
            event=event,
            risk_decision=_allowed_risk_decision(150.0),
            parameters=self.parameters,
        )
        result = self.adapter.execute(event=event, intent=intent)

        self.assertEqual(result.status, "PARTIALLY_FILLED")
        self.assertEqual(result.filled_notional, 75.0)
        self.assertIn("cancel_replace_size_reduction", result.reasons)
        self.assertEqual(result.metadata["replace_count"], 1)

        lifecycle_states = [entry["state"] for entry in result.metadata["lifecycle"]]
        self.assertIn("CANCELLED", lifecycle_states)
        self.assertIn("REPLACED", lifecycle_states)
        self.assertIn("PARTIALLY_FILLED", lifecycle_states)


if __name__ == "__main__":
    unittest.main()
