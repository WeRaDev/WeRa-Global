from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from statistics import median
from typing import Any, Iterable, Protocol

from .contracts import (
    MarketEvent,
    PortfolioState,
    ReplayRecord,
    RiskDecision,
    RiskModule,
    StrategyModule,
)
from .exit_module import ExitDecision, ExitModule, PositionSnapshot
from .paper_execution import (
    ExecutionIntent,
    ExecutionResult,
    build_execution_intent,
)
from .schemas import TEST_TOKEN_LOOP_RESULT_SCHEMA_VERSION


@dataclass(frozen=True)
class TestTokenLoopRecord:
    event_id: str
    timestamp: str
    market_id: str
    replay_record: ReplayRecord
    execution_result: ExecutionResult
    exit_decision: ExitDecision


@dataclass(frozen=True)
class TestTokenLoopRun:
    records: list[TestTokenLoopRecord]
    final_portfolio: PortfolioState
    final_open_positions: dict[str, PositionSnapshot] = field(default_factory=dict)
    stale_hours_threshold: float = 24.0

    @staticmethod
    def _as_non_negative_float(value: Any) -> float:
        try:
            parsed = float(value)
        except (TypeError, ValueError):
            return 0.0
        return max(0.0, parsed)

    @staticmethod
    def _as_float_or_none(value: Any) -> float | None:
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _parse_iso_timestamp(timestamp: str) -> datetime | None:
        try:
            return datetime.fromisoformat(timestamp.replace("Z", "+00:00")).astimezone(
                UTC
            )
        except ValueError:
            return None

    @classmethod
    def _hours_between(cls, start_timestamp: str, end_timestamp: str) -> float:
        start = cls._parse_iso_timestamp(start_timestamp)
        end = cls._parse_iso_timestamp(end_timestamp)
        if start is None or end is None or end < start:
            return 0.0
        return (end - start).total_seconds() / 3600.0

    def _open_position_age_hours(self) -> list[float]:
        return [
            self._hours_between(position.opened_at, position.last_event_timestamp)
            for position in self.final_open_positions.values()
        ]

    def _profitability_attribution_totals(self) -> dict[str, float]:
        totals = {
            "attributed_trade_count": 0.0,
            "approved_notional": 0.0,
            "filled_notional": 0.0,
            "expected_gross_edge_value": 0.0,
            "expected_net_edge_value": 0.0,
            "expected_net_edge_value_on_fills": 0.0,
            "weighted_gross_edge_bps_numerator": 0.0,
            "weighted_net_edge_bps_numerator": 0.0,
        }
        for record in self.records:
            risk_decision = record.replay_record.risk_decision
            if not risk_decision.allowed or risk_decision.approved_notional <= 0:
                continue
            gross_edge_bps = self._as_float_or_none(
                risk_decision.metadata.get("gross_edge_bps")
            )
            net_edge_bps = self._as_float_or_none(
                risk_decision.metadata.get("net_edge_bps")
            )
            if gross_edge_bps is None or net_edge_bps is None:
                continue
            approved_notional = self._as_non_negative_float(
                risk_decision.approved_notional
            )
            filled_notional = self._as_non_negative_float(
                record.execution_result.filled_notional
            )
            totals["attributed_trade_count"] += 1.0
            totals["approved_notional"] += approved_notional
            totals["filled_notional"] += filled_notional
            totals["expected_gross_edge_value"] += (
                approved_notional * gross_edge_bps / 10_000
            )
            totals["expected_net_edge_value"] += (
                approved_notional * net_edge_bps / 10_000
            )
            totals["expected_net_edge_value_on_fills"] += (
                filled_notional * net_edge_bps / 10_000
            )
            totals["weighted_gross_edge_bps_numerator"] += (
                approved_notional * gross_edge_bps
            )
            totals["weighted_net_edge_bps_numerator"] += (
                approved_notional * net_edge_bps
            )
        return totals

    def _strategy_probability_metrics(self) -> dict[str, float | None]:
        raw_probabilities: list[float] = []
        calibrated_probabilities: list[float] = []
        probability_drifts: list[float] = []
        absolute_probability_drifts: list[float] = []
        weighted_check_scores: list[float] = []
        oracle_applied_count = 0

        for record in self.records:
            metadata = record.replay_record.strategy_decision.metadata
            raw_probability = self._as_float_or_none(
                metadata.get("raw_estimated_probability")
            )
            if raw_probability is not None:
                raw_probabilities.append(raw_probability)
            calibrated_probability = self._as_float_or_none(
                metadata.get("calibrated_probability")
            )
            if calibrated_probability is not None:
                calibrated_probabilities.append(calibrated_probability)
            probability_drift = self._as_float_or_none(metadata.get("probability_drift"))
            if probability_drift is not None:
                probability_drifts.append(probability_drift)
            probability_drift_abs = self._as_float_or_none(
                metadata.get("probability_drift_abs")
            )
            if probability_drift_abs is not None:
                absolute_probability_drifts.append(probability_drift_abs)
            weighted_check_agreement = self._as_float_or_none(
                metadata.get("weighted_check_agreement")
            )
            if weighted_check_agreement is not None:
                weighted_check_scores.append(weighted_check_agreement)
            if bool(metadata.get("probability_oracle_applied", False)):
                oracle_applied_count += 1

        calibrated_probability_mean = (
            round(sum(calibrated_probabilities) / len(calibrated_probabilities), 6)
            if calibrated_probabilities
            else None
        )
        raw_probability_mean = (
            round(sum(raw_probabilities) / len(raw_probabilities), 6)
            if raw_probabilities
            else None
        )
        probability_drift_mean = (
            round(sum(probability_drifts) / len(probability_drifts), 6)
            if probability_drifts
            else None
        )
        probability_drift_abs_mean = (
            round(sum(absolute_probability_drifts) / len(absolute_probability_drifts), 6)
            if absolute_probability_drifts
            else None
        )
        probability_drift_max_abs = (
            round(max(absolute_probability_drifts), 6)
            if absolute_probability_drifts
            else None
        )
        weighted_check_agreement_mean = (
            round(sum(weighted_check_scores) / len(weighted_check_scores), 6)
            if weighted_check_scores
            else None
        )
        calibration_applied_ratio = (
            round(oracle_applied_count / len(self.records), 6)
            if self.records
            else 0.0
        )
        return {
            "calibrated_probability_mean": calibrated_probability_mean,
            "raw_probability_mean": raw_probability_mean,
            "probability_drift_mean": probability_drift_mean,
            "probability_drift_abs_mean": probability_drift_abs_mean,
            "probability_drift_max_abs": probability_drift_max_abs,
            "weighted_check_agreement_mean": weighted_check_agreement_mean,
            "calibration_applied_ratio": calibration_applied_ratio,
        }

    @property
    def risk_allowed_count(self) -> int:
        return sum(
            1 for record in self.records if record.replay_record.risk_decision.allowed
        )

    @property
    def filled_trade_count(self) -> int:
        return sum(1 for record in self.records if record.execution_result.is_filled)

    @property
    def partial_fill_count(self) -> int:
        return sum(
            1
            for record in self.records
            if record.execution_result.status == "PARTIALLY_FILLED"
        )

    @property
    def total_fees_paid(self) -> float:
        return round(
            sum(record.execution_result.fee_paid for record in self.records), 4
        )

    @property
    def total_slippage_cost(self) -> float:
        return round(
            sum(record.execution_result.slippage_cost for record in self.records), 4
        )

    @property
    def total_execution_cost(self) -> float:
        return round(
            sum(
                record.execution_result.total_execution_cost for record in self.records
            ),
            4,
        )

    @property
    def exit_candidate_count(self) -> int:
        return sum(
            1 for record in self.records if record.exit_decision.trigger_count > 0
        )

    @property
    def confirmed_exit_count(self) -> int:
        return sum(1 for record in self.records if record.exit_decision.should_exit)

    @property
    def forced_exit_count(self) -> int:
        return sum(
            1
            for record in self.records
            if record.exit_decision.should_exit
            and bool(record.exit_decision.metadata.get("forced_exit", False))
        )

    @property
    def confirmed_exit_ratio(self) -> float | None:
        if self.exit_candidate_count <= 0:
            return None
        return round(self.confirmed_exit_count / self.exit_candidate_count, 6)

    @property
    def confirmed_exit_latency_hours(self) -> float | None:
        latencies: list[float] = []
        for record in self.records:
            if not record.exit_decision.should_exit:
                continue
            holding_hours = self._as_float_or_none(
                record.exit_decision.metadata.get("holding_hours")
            )
            if holding_hours is None or holding_hours < 0:
                continue
            latencies.append(holding_hours)
        if not latencies:
            return None
        return round(sum(latencies) / len(latencies), 6)

    @property
    def median_position_age_hours(self) -> float | None:
        ages = self._open_position_age_hours()
        if not ages:
            return None
        return round(float(median(ages)), 6)

    @property
    def stale_position_count(self) -> int:
        ages = self._open_position_age_hours()
        return sum(1 for age in ages if age >= self.stale_hours_threshold)

    @property
    def stale_position_ratio(self) -> float:
        ages = self._open_position_age_hours()
        if not ages:
            return 0.0
        return round(self.stale_position_count / len(ages), 6)

    @property
    def calibrated_probability_mean(self) -> float | None:
        return self._strategy_probability_metrics()["calibrated_probability_mean"]

    @property
    def raw_probability_mean(self) -> float | None:
        return self._strategy_probability_metrics()["raw_probability_mean"]

    @property
    def probability_drift_mean(self) -> float | None:
        return self._strategy_probability_metrics()["probability_drift_mean"]

    @property
    def probability_drift_abs_mean(self) -> float | None:
        return self._strategy_probability_metrics()["probability_drift_abs_mean"]

    @property
    def probability_drift_max_abs(self) -> float | None:
        return self._strategy_probability_metrics()["probability_drift_max_abs"]

    @property
    def weighted_check_agreement_mean(self) -> float | None:
        return self._strategy_probability_metrics()["weighted_check_agreement_mean"]

    @property
    def calibration_applied_ratio(self) -> float:
        ratio = self._strategy_probability_metrics()["calibration_applied_ratio"]
        if ratio is None:
            return 0.0
        return ratio

    @property
    def attributed_trade_count(self) -> int:
        totals = self._profitability_attribution_totals()
        return int(totals["attributed_trade_count"])

    @property
    def expected_gross_edge_value(self) -> float:
        totals = self._profitability_attribution_totals()
        return round(totals["expected_gross_edge_value"], 4)

    @property
    def expected_net_edge_value(self) -> float:
        totals = self._profitability_attribution_totals()
        return round(totals["expected_net_edge_value"], 4)

    @property
    def expected_net_edge_value_on_fills(self) -> float:
        totals = self._profitability_attribution_totals()
        return round(totals["expected_net_edge_value_on_fills"], 4)

    @property
    def expected_value_after_execution_cost(self) -> float:
        return round(
            self.expected_net_edge_value_on_fills - self.total_execution_cost,
            4,
        )

    @property
    def average_expected_gross_edge_bps(self) -> float | None:
        totals = self._profitability_attribution_totals()
        approved_notional = totals["approved_notional"]
        if approved_notional <= 0:
            return None
        return round(
            totals["weighted_gross_edge_bps_numerator"] / approved_notional,
            2,
        )

    @property
    def average_expected_net_edge_bps(self) -> float | None:
        totals = self._profitability_attribution_totals()
        approved_notional = totals["approved_notional"]
        if approved_notional <= 0:
            return None
        return round(
            totals["weighted_net_edge_bps_numerator"] / approved_notional,
            2,
        )

    @property
    def expected_edge_capture_ratio(self) -> float | None:
        totals = self._profitability_attribution_totals()
        expected_net_edge_value = totals["expected_net_edge_value"]
        if expected_net_edge_value <= 0:
            return None
        return round(
            totals["expected_net_edge_value_on_fills"] / expected_net_edge_value,
            6,
        )

    @property
    def execution_cost_to_expected_net_ratio(self) -> float | None:
        expected_net_edge_value_on_fills = self.expected_net_edge_value_on_fills
        if expected_net_edge_value_on_fills <= 0:
            return None
        return round(
            self.total_execution_cost / expected_net_edge_value_on_fills,
            6,
        )


class ExecutionAdapter(Protocol):
    def execute(
        self, *, event: MarketEvent, intent: ExecutionIntent
    ) -> ExecutionResult: ...

    def skip(
        self, *, event: MarketEvent, risk_decision: RiskDecision
    ) -> ExecutionResult: ...


def _build_exit_skip_result(
    *,
    event: MarketEvent,
    exit_decision: ExitDecision,
    closed_notional: float,
    closed_position_count: int,
) -> ExecutionResult:
    reason_codes = tuple(
        dict.fromkeys(("exit_position_closed",) + exit_decision.reasons)
    )
    return ExecutionResult(
        status="SKIPPED",
        requested_notional=0.0,
        filled_notional=0.0,
        reference_price=float(event.midpoint),
        fill_price=None,
        slippage_bps=0,
        reasons=reason_codes,
        metadata={
            "exit_closed_notional": round(closed_notional, 4),
            "exit_closed_position_count": closed_position_count,
            "exit_decision": asdict(exit_decision),
            "lifecycle": [{"state": "SKIPPED", "reason": "exit_position_closed"}],
        },
    )


class TestTokenLoop:
    def __init__(
        self,
        strategy: StrategyModule,
        risk: RiskModule,
        execution: ExecutionAdapter,
        parameters: dict,
        *,
        exit_module: ExitModule | None = None,
    ):
        self.strategy = strategy
        self.risk = risk
        self.execution = execution
        self.parameters = parameters
        self.exit_module = exit_module or ExitModule(parameters)

    def run(
        self,
        events: Iterable[MarketEvent],
        initial_portfolio: PortfolioState,
        *,
        initial_open_positions: dict[str, PositionSnapshot] | None = None,
    ) -> TestTokenLoopRun:
        ordered_events = sorted(
            events, key=lambda event: (event.timestamp, event.event_id)
        )
        portfolio = initial_portfolio.clone()
        records: list[TestTokenLoopRecord] = []
        open_positions: dict[str, PositionSnapshot] = dict(initial_open_positions or {})

        for event in ordered_events:
            position = open_positions.get(event.market_id)
            exit_decision = self.exit_module.evaluate(event=event, position=position)
            event_for_decision = event
            if (
                position is not None
                and not exit_decision.should_exit
                and bool(
                    exit_decision.metadata.get("inventory_aging_derisk_active", False)
                )
            ):
                event_payload = event.to_dict()
                event_metadata = dict(event_payload.get("metadata", {}))
                event_metadata["suppress_new_entries"] = True
                event_metadata["inventory_aging_derisk_active"] = True
                event_metadata["inventory_aging_derisk_market_id"] = event.market_id
                event_payload["metadata"] = event_metadata
                event_for_decision = MarketEvent.from_dict(event_payload)
            strategy_decision = self.strategy.evaluate(event_for_decision, portfolio)
            risk_decision = self.risk.evaluate(
                event_for_decision, strategy_decision, portfolio
            )
            replay_record = ReplayRecord(
                event_id=event.event_id,
                timestamp=event.timestamp,
                market_id=event.market_id,
                strategy_decision=strategy_decision,
                risk_decision=risk_decision,
            )
            if exit_decision.should_exit and position is not None:
                market_notional = max(
                    0.0,
                    float(
                        portfolio.market_notional.get(
                            event.market_id, position.open_notional
                        )
                    ),
                )
                closed_notional = round(market_notional, 4)
                closed_position_count = max(1, position.fill_count)
                if closed_notional > 0:
                    portfolio.open_notional = round(
                        max(0.0, portfolio.open_notional - closed_notional),
                        4,
                    )
                    portfolio.open_positions = max(
                        0, portfolio.open_positions - closed_position_count
                    )
                    portfolio.market_notional.pop(event.market_id, None)
                open_positions.pop(event.market_id, None)
                execution_result = _build_exit_skip_result(
                    event=event,
                    exit_decision=exit_decision,
                    closed_notional=closed_notional,
                    closed_position_count=closed_position_count,
                )
            elif risk_decision.allowed and risk_decision.approved_notional > 0:
                intent = build_execution_intent(
                    event=event_for_decision,
                    risk_decision=risk_decision,
                    parameters=self.parameters,
                )
                execution_result = self.execution.execute(
                    event=event_for_decision, intent=intent
                )
                if execution_result.is_filled:
                    portfolio.register_executed_trade(
                        event.market_id,
                        execution_result.filled_notional,
                        fee_paid=execution_result.fee_paid,
                        slippage_cost=execution_result.slippage_cost,
                    )
                    tracked_position = open_positions.get(event.market_id)
                    if tracked_position is None:
                        open_positions[event.market_id] = PositionSnapshot.from_fill(
                            event_for_decision,
                            filled_notional=execution_result.filled_notional,
                        )
                    else:
                        open_positions[event.market_id] = (
                            tracked_position.register_fill(
                                event_for_decision,
                                filled_notional=execution_result.filled_notional,
                            )
                        )
            else:
                execution_result = self.execution.skip(
                    event=event_for_decision, risk_decision=risk_decision
                )

            records.append(
                TestTokenLoopRecord(
                    event_id=event.event_id,
                    timestamp=event.timestamp,
                    market_id=event.market_id,
                    replay_record=replay_record,
                    execution_result=execution_result,
                    exit_decision=exit_decision,
                )
            )

        return TestTokenLoopRun(
            records=records,
            final_portfolio=portfolio,
            final_open_positions=dict(open_positions),
            stale_hours_threshold=float(self.exit_module.stale_hours),
        )


def serialize_test_token_loop_run(
    run: TestTokenLoopRun,
    *,
    run_context: dict | None = None,
    reproducibility: dict | None = None,
) -> dict:
    payload = {
        "schema_version": TEST_TOKEN_LOOP_RESULT_SCHEMA_VERSION,
        "records": [asdict(record) for record in run.records],
        "final_portfolio": asdict(run.final_portfolio),
        "final_open_positions": {
            market_id: asdict(position)
            for market_id, position in run.final_open_positions.items()
        },
        "risk_allowed_count": run.risk_allowed_count,
        "filled_trade_count": run.filled_trade_count,
        "partial_fill_count": run.partial_fill_count,
        "exit_candidate_count": run.exit_candidate_count,
        "confirmed_exit_count": run.confirmed_exit_count,
        "forced_exit_count": run.forced_exit_count,
        "confirmed_exit_ratio": run.confirmed_exit_ratio,
        "confirmed_exit_latency_hours": run.confirmed_exit_latency_hours,
        "median_position_age_hours": run.median_position_age_hours,
        "stale_position_count": run.stale_position_count,
        "stale_position_ratio": run.stale_position_ratio,
        "raw_probability_mean": run.raw_probability_mean,
        "calibrated_probability_mean": run.calibrated_probability_mean,
        "probability_drift_mean": run.probability_drift_mean,
        "probability_drift_abs_mean": run.probability_drift_abs_mean,
        "probability_drift_max_abs": run.probability_drift_max_abs,
        "weighted_check_agreement_mean": run.weighted_check_agreement_mean,
        "calibration_applied_ratio": run.calibration_applied_ratio,
        "total_fees_paid": run.total_fees_paid,
        "total_slippage_cost": run.total_slippage_cost,
        "total_execution_cost": run.total_execution_cost,
        "attributed_trade_count": run.attributed_trade_count,
        "expected_gross_edge_value": run.expected_gross_edge_value,
        "expected_net_edge_value": run.expected_net_edge_value,
        "expected_net_edge_value_on_fills": run.expected_net_edge_value_on_fills,
        "expected_value_after_execution_cost": run.expected_value_after_execution_cost,
        "average_expected_gross_edge_bps": run.average_expected_gross_edge_bps,
        "average_expected_net_edge_bps": run.average_expected_net_edge_bps,
        "expected_edge_capture_ratio": run.expected_edge_capture_ratio,
        "execution_cost_to_expected_net_ratio": run.execution_cost_to_expected_net_ratio,
    }
    if run_context is not None:
        payload["run_context"] = run_context
    if reproducibility is not None:
        payload["reproducibility"] = reproducibility
    return payload
