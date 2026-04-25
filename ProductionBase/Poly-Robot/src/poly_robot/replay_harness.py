from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Iterable

from .contracts import (
    MarketEvent,
    PortfolioState,
    ReplayRecord,
    ReplayRun,
    RiskModule,
    StrategyModule,
)
from .schemas import REPLAY_RESULT_SCHEMA_VERSION


def load_events_from_jsonl(path: Path) -> list[MarketEvent]:
    events: list[MarketEvent] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line:
                continue
            payload = json.loads(line)
            try:
                event = MarketEvent.from_dict(payload)
            except ValueError as exc:
                raise ValueError(f"Invalid event at line {line_number}: {exc}") from exc
            events.append(event)
    return events


class ReplayHarness:
    def __init__(self, strategy: StrategyModule, risk: RiskModule):
        self.strategy = strategy
        self.risk = risk

    def run(self, events: Iterable[MarketEvent], initial_portfolio: PortfolioState) -> ReplayRun:
        ordered_events = sorted(events, key=lambda event: (event.timestamp, event.event_id))
        portfolio = initial_portfolio.clone()
        records: list[ReplayRecord] = []

        for event in ordered_events:
            strategy_decision = self.strategy.evaluate(event, portfolio)
            risk_decision = self.risk.evaluate(event, strategy_decision, portfolio)

            if risk_decision.allowed and risk_decision.approved_notional > 0:
                portfolio.register_approved_trade(event.market_id, risk_decision.approved_notional)

            records.append(
                ReplayRecord(
                    event_id=event.event_id,
                    timestamp=event.timestamp,
                    market_id=event.market_id,
                    strategy_decision=strategy_decision,
                    risk_decision=risk_decision,
                )
            )

        return ReplayRun(records=records, final_portfolio=portfolio)


def serialize_replay_run(
    run: ReplayRun, *, run_context: dict | None = None, reproducibility: dict | None = None
) -> dict:
    payload = {
        "schema_version": REPLAY_RESULT_SCHEMA_VERSION,
        "records": [asdict(record) for record in run.records],
        "final_portfolio": asdict(run.final_portfolio),
        "allowed_trade_count": run.allowed_trade_count,
    }
    if run_context is not None:
        payload["run_context"] = run_context
    if reproducibility is not None:
        payload["reproducibility"] = reproducibility
    return payload
