from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from poly_robot.replay_harness import load_events_from_jsonl  # noqa: E402
from poly_robot.scenario_pack import (  # noqa: E402
    apply_scenario_to_events,
    load_scenario_pack,
)
from poly_robot.schemas import SCENARIO_PACK_SCHEMA_VERSION  # noqa: E402


REPLAY_FIXTURE_PATH = ROOT_DIR / "tests" / "fixtures" / "replay_events.jsonl"
SCENARIO_PACK_PATH = ROOT_DIR / "config" / "replay" / "scenario_pack.v1.json"


class ScenarioPackTests(unittest.TestCase):
    def test_loads_schema_version_and_default_scenario(self) -> None:
        pack = load_scenario_pack(SCENARIO_PACK_PATH)
        self.assertEqual(pack.schema_version, SCENARIO_PACK_SCHEMA_VERSION)
        self.assertIn(pack.default_scenario, pack.scenarios)

    def test_applies_liquidity_crunch_transform(self) -> None:
        events = load_events_from_jsonl(REPLAY_FIXTURE_PATH)
        pack = load_scenario_pack(SCENARIO_PACK_PATH)
        scenario = pack.get_scenario("liquidity_crunch")
        transformed = apply_scenario_to_events(events, scenario)

        self.assertEqual(len(events), len(transformed))
        self.assertLess(
            transformed[0].bids_depth_usd,
            events[0].bids_depth_usd,
        )
        self.assertLess(
            transformed[0].liquidity_usd,
            events[0].liquidity_usd,
        )
        self.assertEqual(transformed[0].metadata["scenario_name"], "liquidity_crunch")

    def test_applies_latency_shift_transform(self) -> None:
        events = load_events_from_jsonl(REPLAY_FIXTURE_PATH)
        pack = load_scenario_pack(SCENARIO_PACK_PATH)
        scenario = pack.get_scenario("latency_spike")
        transformed = apply_scenario_to_events(events, scenario)

        self.assertNotEqual(transformed[0].timestamp, events[0].timestamp)
        self.assertEqual(transformed[0].metadata["scenario_latency_ms"], 1200)


if __name__ == "__main__":
    unittest.main()
