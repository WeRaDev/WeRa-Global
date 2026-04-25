from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from poly_robot.contracts import MarketEvent, PortfolioState  # noqa: E402
from poly_robot.llm_policy import load_calibration_policy  # noqa: E402
from poly_robot.paper_execution import PaperExecutionAdapter  # noqa: E402
from poly_robot.replay_harness import load_events_from_jsonl  # noqa: E402
from poly_robot.risk_engine import RiskEngine  # noqa: E402
from poly_robot.schemas import TEST_TOKEN_LOOP_RESULT_SCHEMA_VERSION  # noqa: E402
from poly_robot.strategy_baseline import BaselineStrategy  # noqa: E402
from poly_robot.test_token_loop import (  # noqa: E402
    TestTokenLoop,
    serialize_test_token_loop_run,
)


PROFILE_PATH = ROOT_DIR / "config" / "parameters" / "profiles" / "mvp_test_token.v1.json"
CALIBRATION_POLICY_PATH = ROOT_DIR / "config" / "calibration" / "llm_reliability.v1.json"
REPLAY_FIXTURE_PATH = ROOT_DIR / "tests" / "fixtures" / "replay_events.jsonl"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class TestTokenLoopTests(unittest.TestCase):
    def test_end_to_end_loop_runs_strategy_risk_and_execution(self) -> None:
        profile_payload = _load_json(PROFILE_PATH)
        parameters = profile_payload["values"]
        calibration_policy = load_calibration_policy(CALIBRATION_POLICY_PATH)
        events = load_events_from_jsonl(REPLAY_FIXTURE_PATH)

        strategy = BaselineStrategy(parameters, calibration_policy)
        risk = RiskEngine(parameters)
        execution = PaperExecutionAdapter(parameters)
        loop = TestTokenLoop(strategy, risk, execution, parameters)

        run = loop.run(
            events,
            PortfolioState(
                bankroll=1000.0,
                day_start_equity=1000.0,
                current_equity=1000.0,
            ),
        )
        payload = serialize_test_token_loop_run(run)

        self.assertEqual([record.event_id for record in run.records], ["evt-1", "evt-2"])
        self.assertEqual(run.records[0].execution_result.status, "SKIPPED")
        self.assertTrue(run.records[1].replay_record.risk_decision.allowed)
        self.assertEqual(run.records[1].execution_result.status, "FILLED")
        self.assertEqual(run.risk_allowed_count, 1)
        self.assertEqual(run.filled_trade_count, 1)
        self.assertEqual(run.partial_fill_count, 0)
        self.assertEqual(run.final_portfolio.open_positions, 1)
        self.assertEqual(
            run.final_portfolio.open_notional,
            run.records[1].execution_result.filled_notional,
        )
        self.assertGreater(run.total_execution_cost, 0.0)
        self.assertAlmostEqual(
            run.final_portfolio.current_equity,
            1000.0 - run.total_execution_cost,
            places=4,
        )
        self.assertEqual(payload["schema_version"], TEST_TOKEN_LOOP_RESULT_SCHEMA_VERSION)
        self.assertEqual(payload["total_execution_cost"], run.total_execution_cost)

    def test_loop_preserves_risk_gate_when_execution_ttl_expires(self) -> None:
        profile_payload = _load_json(PROFILE_PATH)
        parameters = profile_payload["values"]
        calibration_policy = load_calibration_policy(CALIBRATION_POLICY_PATH)
        events = load_events_from_jsonl(REPLAY_FIXTURE_PATH)

        latency_events: list[MarketEvent] = []
        for event in events:
            payload = event.to_dict()
            if event.event_id == "evt-2":
                payload["metadata"] = {"execution_latency_ms": 500_000}
            latency_events.append(MarketEvent.from_dict(payload))

        strategy = BaselineStrategy(parameters, calibration_policy)
        risk = RiskEngine(parameters)
        execution = PaperExecutionAdapter(parameters)
        loop = TestTokenLoop(strategy, risk, execution, parameters)

        run = loop.run(
            latency_events,
            PortfolioState(
                bankroll=1000.0,
                day_start_equity=1000.0,
                current_equity=1000.0,
            ),
        )

        self.assertEqual(run.risk_allowed_count, 1)
        self.assertEqual(run.filled_trade_count, 0)
        self.assertEqual(run.records[1].execution_result.status, "EXPIRED")
        self.assertEqual(run.final_portfolio.open_positions, 0)
        self.assertEqual(run.final_portfolio.open_notional, 0.0)
        self.assertEqual(run.total_execution_cost, 0.0)

    def test_loop_records_replace_path_and_partial_fill(self) -> None:
        profile_payload = _load_json(PROFILE_PATH)
        parameters = profile_payload["values"]
        calibration_policy = load_calibration_policy(CALIBRATION_POLICY_PATH)
        events = load_events_from_jsonl(REPLAY_FIXTURE_PATH)

        replace_events: list[MarketEvent] = []
        for event in events:
            payload = event.to_dict()
            if event.event_id == "evt-2":
                payload["metadata"] = {"execution_slippage_multiplier": 20.0}
            replace_events.append(MarketEvent.from_dict(payload))

        strategy = BaselineStrategy(parameters, calibration_policy)
        risk = RiskEngine(parameters)
        execution = PaperExecutionAdapter(parameters)
        loop = TestTokenLoop(strategy, risk, execution, parameters)
        run = loop.run(
            replace_events,
            PortfolioState(
                bankroll=1000.0,
                day_start_equity=1000.0,
                current_equity=1000.0,
            ),
        )

        self.assertEqual(run.risk_allowed_count, 1)
        self.assertEqual(run.filled_trade_count, 1)
        self.assertEqual(run.partial_fill_count, 1)
        self.assertEqual(run.records[1].execution_result.status, "PARTIALLY_FILLED")
        self.assertIn("cancel_replace_size_reduction", run.records[1].execution_result.reasons)
        self.assertEqual(run.records[1].execution_result.metadata["replace_count"], 1)


if __name__ == "__main__":
    unittest.main()
