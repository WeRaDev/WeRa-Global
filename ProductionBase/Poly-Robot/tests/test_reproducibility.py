from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from poly_robot.replay_harness import load_events_from_jsonl  # noqa: E402
from poly_robot.reproducibility import hash_events, stable_hash  # noqa: E402
from poly_robot.scenario_pack import (  # noqa: E402
    apply_scenario_to_events,
    load_scenario_pack,
)


REPLAY_FIXTURE_PATH = ROOT_DIR / "tests" / "fixtures" / "replay_events.jsonl"
SCENARIO_PACK_PATH = ROOT_DIR / "config" / "replay" / "scenario_pack.v1.json"


class ReproducibilityTests(unittest.TestCase):
    def test_hash_events_is_order_independent_and_deterministic(self) -> None:
        events = load_events_from_jsonl(REPLAY_FIXTURE_PATH)
        hash_a = hash_events(events)
        hash_b = hash_events(list(reversed(events)))
        self.assertEqual(hash_a, hash_b)

    def test_hash_changes_when_scenario_changes_inputs(self) -> None:
        events = load_events_from_jsonl(REPLAY_FIXTURE_PATH)
        pack = load_scenario_pack(SCENARIO_PACK_PATH)
        baseline_events = apply_scenario_to_events(
            events, pack.get_scenario("baseline")
        )
        stress_events = apply_scenario_to_events(
            events, pack.get_scenario("liquidity_crunch")
        )
        self.assertNotEqual(hash_events(baseline_events), hash_events(stress_events))

    def test_stable_hash_is_deterministic(self) -> None:
        payload = {"b": 2, "a": 1, "nested": {"z": 5, "x": 3}}
        self.assertEqual(stable_hash(payload), stable_hash(payload))


if __name__ == "__main__":
    unittest.main()
