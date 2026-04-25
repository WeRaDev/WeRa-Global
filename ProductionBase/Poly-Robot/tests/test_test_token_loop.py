from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from poly_robot.contracts import (  # noqa: E402
    MarketEvent,
    PortfolioState,
    RiskDecision,
    StrategyDecision,
)
from poly_robot.llm_policy import load_calibration_policy  # noqa: E402
from poly_robot.paper_execution import ExecutionResult, PaperExecutionAdapter  # noqa: E402
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


def _build_custom_event(
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
            "question": "Custom loop event",
            "midpoint": midpoint,
            "estimated_probability": estimated_probability,
            "bids_depth_usd": 3000.0,
            "asks_depth_usd": 3000.0,
            "liquidity_usd": 110000.0,
            "hours_to_resolution": 36.0,
            "check_signals": {},
            "base_confidence": 0.9,
            "llm_confidence": 0.9,
            "consensus_buy_votes": 2,
            "metadata": {"volume_usd": volume_usd},
        }
    )


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

    def test_confirmed_exit_closes_position_and_emits_exit_telemetry(self) -> None:
        profile_payload = _load_json(PROFILE_PATH)
        parameters = profile_payload["values"]

        class AlwaysBuyStrategy:
            def evaluate(self, event: MarketEvent, portfolio: PortfolioState) -> StrategyDecision:
                del event, portfolio
                return StrategyDecision(
                    action="BUY",
                    win_probability=0.75,
                    confidence=0.9,
                    checks_passed=4,
                    consensus_buy_votes=2,
                    llm_effective_mode="advisory_only",
                    llm_used_for_probability=False,
                    reasons=("entry_candidate",),
                    metadata={},
                )

        class AlwaysAllowRisk:
            def evaluate(
                self,
                event: MarketEvent,
                decision: StrategyDecision,
                portfolio: PortfolioState,
            ) -> RiskDecision:
                del event, decision, portfolio
                return RiskDecision(
                    allowed=True,
                    approved_notional=100.0,
                    approved_fraction=0.1,
                    kill_switch=False,
                    reasons=("test_allow",),
                    metadata={},
                )

        class DeterministicExecution:
            def execute(self, *, event, intent) -> ExecutionResult:
                return ExecutionResult(
                    status="FILLED",
                    requested_notional=float(intent.requested_notional),
                    filled_notional=float(intent.requested_notional),
                    reference_price=float(event.midpoint),
                    fill_price=float(event.midpoint),
                    slippage_bps=0,
                    fee_paid=0.0,
                    slippage_cost=0.0,
                    total_execution_cost=0.0,
                    reasons=("test_fill",),
                    metadata={},
                )

            def skip(self, *, event, risk_decision) -> ExecutionResult:
                del risk_decision
                return ExecutionResult(
                    status="SKIPPED",
                    requested_notional=0.0,
                    filled_notional=0.0,
                    reference_price=float(event.midpoint),
                    fill_price=None,
                    slippage_bps=0,
                    reasons=("skipped",),
                    metadata={},
                )

        loop = TestTokenLoop(
            strategy=AlwaysBuyStrategy(),
            risk=AlwaysAllowRisk(),
            execution=DeterministicExecution(),
            parameters=parameters,
        )
        run = loop.run(
            [
                _build_custom_event(
                    event_id="evt-entry",
                    timestamp="2026-01-01T00:00:00Z",
                    midpoint=0.45,
                    estimated_probability=0.7,
                    volume_usd=1000.0,
                ),
                _build_custom_event(
                    event_id="evt-exit",
                    timestamp="2026-01-01T03:00:00Z",
                    midpoint=0.67,
                    estimated_probability=0.72,
                    volume_usd=3600.0,
                ),
            ],
            PortfolioState(
                bankroll=1000.0,
                day_start_equity=1000.0,
                current_equity=1000.0,
            ),
        )
        payload = serialize_test_token_loop_run(run)

        self.assertEqual(run.filled_trade_count, 1)
        self.assertEqual(run.confirmed_exit_count, 1)
        self.assertEqual(run.final_portfolio.open_positions, 0)
        self.assertEqual(run.final_portfolio.open_notional, 0.0)
        self.assertEqual(run.records[1].execution_result.status, "SKIPPED")
        self.assertIn("exit_position_closed", run.records[1].execution_result.reasons)
        self.assertTrue(run.records[1].exit_decision.should_exit)
        self.assertEqual(payload["confirmed_exit_count"], 1)
        self.assertEqual(payload["exit_candidate_count"], 1)


if __name__ == "__main__":
    unittest.main()
