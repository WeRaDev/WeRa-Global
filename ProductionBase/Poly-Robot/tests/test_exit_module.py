from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
PROFILE_PATH = (
    ROOT_DIR / "config" / "parameters" / "profiles" / "mvp_test_token.v1.json"
)

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from poly_robot.contracts import MarketEvent  # noqa: E402
from poly_robot.exit_module import ExitModule, PositionSnapshot  # noqa: E402


def _load_profile_values() -> dict:
    payload = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    return payload["values"]


def _build_event(
    *,
    event_id: str,
    timestamp: str,
    midpoint: float,
    estimated_probability: float,
    volume_usd: float,
) -> MarketEvent:
    return MarketEvent.from_dict(
        {
            "schema_version": "replay_event.v1",
            "event_id": event_id,
            "timestamp": timestamp,
            "market_id": "mkt-1",
            "question": "Will trigger tests pass?",
            "midpoint": midpoint,
            "estimated_probability": estimated_probability,
            "bids_depth_usd": 2500.0,
            "asks_depth_usd": 2600.0,
            "liquidity_usd": 120000.0,
            "hours_to_resolution": 48.0,
            "check_signals": {},
            "base_confidence": 0.8,
            "llm_confidence": 0.9,
            "consensus_buy_votes": 2,
            "metadata": {"volume_usd": volume_usd},
        }
    )


class ExitModuleTests(unittest.TestCase):
    def test_confirms_exit_when_target_capture_and_volume_spike_align(self) -> None:
        parameters = _load_profile_values()
        module = ExitModule(parameters)
        entry_event = _build_event(
            event_id="evt-entry",
            timestamp="2026-01-01T00:00:00Z",
            midpoint=0.45,
            estimated_probability=0.70,
            volume_usd=1000.0,
        )
        position = PositionSnapshot.from_fill(entry_event, filled_notional=100.0)

        check_event = _build_event(
            event_id="evt-check",
            timestamp="2026-01-01T02:00:00Z",
            midpoint=0.67,
            estimated_probability=0.72,
            volume_usd=3600.0,
        )
        decision = module.evaluate(event=check_event, position=position)

        self.assertTrue(decision.should_exit)
        self.assertEqual(decision.trigger_count, 2)
        self.assertIn("target_capture_ratio_reached", decision.reasons)
        self.assertIn("abnormal_volume_spike_detected", decision.reasons)
        self.assertIn("exit_multi_trigger_confirmed", decision.reasons)
        self.assertTrue(decision.metadata["triggers"]["target_capture"])
        self.assertTrue(decision.metadata["triggers"]["abnormal_volume"])

    def test_marks_single_trigger_as_unconfirmed(self) -> None:
        parameters = _load_profile_values()
        module = ExitModule(parameters)
        entry_event = _build_event(
            event_id="evt-entry",
            timestamp="2026-01-01T00:00:00Z",
            midpoint=0.45,
            estimated_probability=0.70,
            volume_usd=1000.0,
        )
        position = PositionSnapshot.from_fill(entry_event, filled_notional=80.0)

        check_event = _build_event(
            event_id="evt-stale",
            timestamp="2026-01-02T06:00:00Z",
            midpoint=0.454,
            estimated_probability=0.69,
            volume_usd=1100.0,
        )
        decision = module.evaluate(event=check_event, position=position)

        self.assertFalse(decision.should_exit)
        self.assertEqual(decision.trigger_count, 1)
        self.assertIn("stale_thesis_detected", decision.reasons)
        self.assertIn("exit_multi_trigger_unconfirmed", decision.reasons)
        self.assertTrue(decision.metadata["triggers"]["stale_thesis"])


if __name__ == "__main__":
    unittest.main()
