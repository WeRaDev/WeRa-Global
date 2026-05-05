# ADR-003: Reliability Gate / Economic-Quality Gate Separation

**Status**: Accepted
**Date**: 2026-05-05
**Context**: Poly-Robot lifecycle gate evolution (Sprint W21)

## Problem

The current TRL4 profitability gate and canary lifecycle gate conflate two independent concerns:

1. **Reliability** -- is the runtime healthy? (ingestion OK, supervisor cycling, no crashes, drills pass, rollback mechanisms verified)
2. **Economic quality** -- is the strategy profitable? (positive EV, positive net edge, acceptable cost ratios, rolling-window PnL trends)

This coupling means:
- A runtime that is perfectly reliable but has weak economics cannot be promoted even for controlled canary observation.
- A strategy with strong economics but flaky ingestion can pass if the latest cycle happens to look good.
- Gate criteria must be set conservatively to avoid either false-pass, making the gate less useful for both purposes.

## Decision

Split the single gate evaluation into two independent gate stages:

### Stage 1: Reliability Gate
Evaluates runtime health, operational safety, and deterministic process integrity.

Criteria:
- Runtime duration meets minimum hours
- Ingestion status stable (no prolonged degradation streaks)
- Supervisor cycling without worker failures
- Soak/stress certification PASS
- Rehearsal protocol SUCCESS with zero blocking rollback recommendations
- Control drills (kill-switch, cancel-all, restart) verified

Pass condition: all reliability criteria met. This gate is required for any mode promotion.

### Stage 2: Economic-Quality Gate
Evaluates strategy profitability and financial metric quality.

Criteria:
- Latest expected_value_after_execution_cost >= configured minimum
- Latest expected_net_edge_value_on_fills >= configured minimum
- Mean expected_value_after_execution_cost across rolling window >= configured minimum
- Net PnL trend (sign and direction over configurable window)
- Execution cost ratio within acceptable bounds

Pass condition: all economic criteria met. This gate is required for `test -> live` promotion but may be advisory-only for `paper -> test` transitions.

### Gate composition
- `paper -> test`: Reliability Gate required, Economic-Quality Gate advisory
- `test -> live`: Both gates required
- Canary promotion: Both gates required, plus approval record sign-off

## Consequences

- Allows controlled canary observation of a reliable but not-yet-profitable system
- Makes it explicit which gate failed and why, improving operator triage
- Enables independent threshold tuning for reliability vs. profitability
- Requires updating `run_trl4_profitability_report.py` and `mode_lifecycle.py` to support split evaluation
- Existing single-gate behavior remains as the default until split is implemented

## Implementation plan
1. Add `gate_mode` field to TRL4 gate config: `combined` (current default), `reliability_only`, `economic_only`
2. Factor criteria in `run_trl4_profitability_report.py` into reliability and economic groups
3. Emit per-group pass/fail in the report alongside overall status
4. Update `mode_lifecycle.py` to consume split gate results for transition-specific requirements
5. Update canary lifecycle gate to enforce both independently
