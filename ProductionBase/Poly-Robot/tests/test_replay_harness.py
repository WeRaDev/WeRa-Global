from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from poly_robot.contracts import PortfolioState  # noqa: E402
from poly_robot.llm_policy import load_calibration_policy  # noqa: E402
from poly_robot.replay_harness import (  # noqa: E402
    ReplayHarness,
    load_events_from_jsonl,
    serialize_replay_run,
)
from poly_robot.risk_engine import RiskEngine  # noqa: E402
from poly_robot.strategy_baseline import BaselineStrategy  # noqa: E402
from poly_robot.schemas import REPLAY_RESULT_SCHEMA_VERSION  # noqa: E402


PROFILE_PATH = (
    ROOT_DIR / "config" / "parameters" / "profiles" / "mvp_test_token.v1.json"
)
CALIBRATION_POLICY_PATH = (
    ROOT_DIR / "config" / "calibration" / "llm_reliability.v1.json"
)
REPLAY_FIXTURE_PATH = ROOT_DIR / "tests" / "fixtures" / "replay_events.jsonl"


def _load_parameters() -> dict:
    payload = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    return payload["values"]


class ReplayHarnessTests(unittest.TestCase):
    def test_replay_is_deterministic_and_uses_risk_contract(self) -> None:
        parameters = _load_parameters()
        calibration_policy = load_calibration_policy(CALIBRATION_POLICY_PATH)
        strategy = BaselineStrategy(parameters, calibration_policy)
        risk = RiskEngine(parameters)
        harness = ReplayHarness(strategy, risk)

        events = load_events_from_jsonl(REPLAY_FIXTURE_PATH)
        run = harness.run(
            events,
            PortfolioState(
                bankroll=1000.0,
                day_start_equity=1000.0,
                current_equity=1000.0,
            ),
        )

        self.assertEqual(
            [record.event_id for record in run.records], ["evt-1", "evt-2"]
        )
        self.assertEqual(run.records[0].strategy_decision.action, "HOLD")
        self.assertEqual(run.records[1].strategy_decision.action, "BUY")
        self.assertTrue(run.records[1].risk_decision.allowed)
        self.assertFalse(run.records[1].strategy_decision.llm_used_for_probability)
        self.assertEqual(
            run.records[1].strategy_decision.llm_effective_mode, "advisory_only"
        )
        self.assertEqual(run.final_portfolio.open_positions, 1)
        self.assertEqual(
            serialize_replay_run(run)["schema_version"], REPLAY_RESULT_SCHEMA_VERSION
        )


if __name__ == "__main__":
    unittest.main()
