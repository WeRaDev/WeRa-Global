from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable, Protocol

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
        self, events: Iterable[MarketEvent], initial_portfolio: PortfolioState
    ) -> TestTokenLoopRun:
        ordered_events = sorted(
            events, key=lambda event: (event.timestamp, event.event_id)
        )
        portfolio = initial_portfolio.clone()
        records: list[TestTokenLoopRecord] = []
        open_positions: dict[str, PositionSnapshot] = {}

        for event in ordered_events:
            position = open_positions.get(event.market_id)
            exit_decision = self.exit_module.evaluate(event=event, position=position)
            strategy_decision = self.strategy.evaluate(event, portfolio)
            risk_decision = self.risk.evaluate(event, strategy_decision, portfolio)
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
                    event=event,
                    risk_decision=risk_decision,
                    parameters=self.parameters,
                )
                execution_result = self.execution.execute(event=event, intent=intent)
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
                            event,
                            filled_notional=execution_result.filled_notional,
                        )
                    else:
                        open_positions[event.market_id] = (
                            tracked_position.register_fill(
                                event,
                                filled_notional=execution_result.filled_notional,
                            )
                        )
            else:
                execution_result = self.execution.skip(
                    event=event, risk_decision=risk_decision
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

        return TestTokenLoopRun(records=records, final_portfolio=portfolio)


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
        "risk_allowed_count": run.risk_allowed_count,
        "filled_trade_count": run.filled_trade_count,
        "partial_fill_count": run.partial_fill_count,
        "exit_candidate_count": run.exit_candidate_count,
        "confirmed_exit_count": run.confirmed_exit_count,
        "total_fees_paid": run.total_fees_paid,
        "total_slippage_cost": run.total_slippage_cost,
        "total_execution_cost": run.total_execution_cost,
    }
    if run_context is not None:
        payload["run_context"] = run_context
    if reproducibility is not None:
        payload["reproducibility"] = reproducibility
    return payload
