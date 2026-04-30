# Poly-Robot Economy & Strategy — Unified Specification
## 1) Scope and source of truth
This specification consolidates the implemented economic logic across:
- Strategy: `src/poly_robot/strategy_baseline.py`
- Risk: `src/poly_robot/risk_engine.py`
- Execution: `src/poly_robot/paper_execution.py`, `src/poly_robot/integration_adapters.py`
- Exit: `src/poly_robot/exit_module.py`
- Loop attribution: `src/poly_robot/test_token_loop.py`
- Runtime/reporting: `scripts/run_runtime_supervisor.py`, `scripts/run_trl4_profitability_report.py`, `src/poly_robot/runtime_web_gui.py`
- Governance/config: `config/parameters/catalog.v1.json`, `config/parameters/profiles/mvp_test_token.v1.json`, `config/calibration/llm_reliability.v1.json`, `config/certification/trl4_24h_profitability_gate.v1.json`

## 2) Economic objective (implemented)
Poly-Robot is currently optimized for:
- Expected-edge selection (probability edge over midpoint),
- Cost-aware risk sizing (fees + expected slippage),
- Execution-cost attribution (fee/slippage tracked deterministically),
- Safety-first exposure controls (drawdown/position/exposure limits).

Current implementation is not yet a full realized-PnL engine: equity is reduced by execution costs and does not yet book mark-to-market gains/losses from price movement.

## 3) Active parameter baseline (`mvp_test_token`)
From `config/parameters/profiles/mvp_test_token.v1.json`:
- Entry filters:
  - `scanner.min_price_gap = 0.07`
  - `scanner.min_side_depth_usd = 500.0`
  - `scanner.min_market_liquidity_usd = 50000.0`
  - `scanner.min_hours_to_resolution = 4`
  - `scanner.max_hours_to_resolution = 168`
- Decision confidence:
  - `brain.min_checks_agreement = 3`
  - `brain.min_thesis_confidence = 0.75`
  - `brain.llm_probability_calibration = advisory_only`
- Execution:
  - `execution.min_consensus_buy_votes = 2`
  - `execution.single_vote_size_factor = 0.5`
  - `execution.order_ttl_seconds = 120`
  - `execution.max_slippage_bps = 60`
- Risk:
  - `risk.kelly_cap_fraction = 0.25`
  - `risk.max_position_fraction = 0.15`
  - `risk.max_market_exposure_fraction = 0.25`
  - `risk.max_portfolio_exposure_fraction = 0.6`
  - `risk.max_daily_drawdown_fraction = 0.08`
  - `risk.max_concurrent_positions = 6`
- Exit:
  - `exit.target_capture_ratio = 0.85`
  - `exit.volume_spike_multiplier = 3.0`
  - `exit.stale_hours = 24`
  - `exit.stale_price_change_threshold = 0.02`
- Cost model:
  - `ops.fee_rate_bps = 20`

## 4) Market-event economics
### 4.1 Historical ingestion
`HistoricalIngestionAdapter`:
- Loads JSONL events, validates schema, optional dedupe by `event_id`, optional monotonic timestamp checks.
- Produces `OK`, `DEGRADED`, or `FAILED` with reason-coded metadata.

### 4.2 Live Polymarket ingestion
`LivePolymarketIngestionAdapter` builds each `MarketEvent` with:
- Midpoint extraction from `outcomePrices[0]`, fallback to bid/ask midpoint, fallback to last trade.
- Liquidity transformation:
  - `effective_liquidity = max(raw_liquidity, volume_24h * volume_to_liquidity_multiplier)`
- Signals:
  - `base_rate`: midpoint >= threshold
  - `news`: volume_24h >= threshold
  - `whale`: wallet convergence signal OR liquidity whale signal
  - `disposition`: one-week price change >= 0
- Estimated probability:
  - `estimated_probability = clamp(midpoint + sum(probability_components), 0.001, 0.999)`
  - Components include alpha prior, weekly change, momentum, news volume, liquidity score, wallet convergence, signal agreement, whale presence, disposition.
- Confidence:
  - `base_confidence = clamp(0.55 + 0.1 * checks_passed, 0.001, 0.999)`
- Consensus votes:
  - `consensus_buy_votes = 2 if checks_passed >= 3 else 1`
- Depth payload:
  - `bids_depth_usd = asks_depth_usd = max(500.0, effective_liquidity / 2.0)`

## 5) Strategy logic (`BaselineStrategy`)
Decision sequence:
1. Hard prefilters (any fail => `HOLD`):
   - Positive edge: `estimated_probability > midpoint`
   - Price-gap threshold: `abs(estimated_probability - midpoint) >= scanner.min_price_gap`
   - Depth threshold: `min(bids_depth_usd, asks_depth_usd) >= scanner.min_side_depth_usd`
   - Liquidity threshold: `liquidity_usd >= scanner.min_market_liquidity_usd`
   - Resolution window: `scanner.min_hours_to_resolution <= hours_to_resolution <= scanner.max_hours_to_resolution`
2. Multi-check agreement gate:
   - Checks: `base_rate`, `news`, `whale`, `disposition`
   - Require `checks_passed >= brain.min_checks_agreement`
3. Confidence and LLM-policy gate:
   - `merge_confidence(base_confidence, llm_confidence, requested_mode, calibration_policy)`
   - In current profile (`advisory_only`), LLM does not alter probability usage.
   - Non-advisory modes are only effective when calibration reliability is proven.
   - Require `final_confidence >= brain.min_thesis_confidence`
4. Output:
   - `BUY` with reason `entry_candidate` or `HOLD` with explicit reason codes.

## 6) Risk engine economics
### 6.1 Core sizing formula
Kelly fraction:
- `b = (1 / market_price) - 1`
- `f* = (p * b - q) / b`, where `q = 1 - p`
- Inputs are clamped to safe ranges.

Approved-fraction pipeline:
1. Start with `f*`
2. Cap by:
   - `risk.kelly_cap_fraction`
   - `risk.max_position_fraction`
3. Consensus scaling:
   - If `consensus_buy_votes >= execution.min_consensus_buy_votes`: full-size
   - If `consensus_buy_votes == 1`: multiply by `execution.single_vote_size_factor`
   - Else reject (`insufficient_consensus_votes`)
4. Remaining-capacity caps:
   - Remaining portfolio exposure capacity
   - Remaining market exposure capacity

### 6.2 Hard risk gates (pre-sizing rejects)
- Strategy action not `BUY`
- Daily drawdown kill switch triggered
- Max concurrent positions reached
- Market exposure limit reached
- Portfolio exposure limit reached
- Non-positive Kelly edge

### 6.3 Cost-aware edge gating
Before final approval:
- `gross_edge_fraction = max(0, win_probability - midpoint)`
- Slippage estimate:
  - `depth_utilization = min(1, notional / min_side_depth)`
  - `expected_slippage_bps = round(max_slippage_bps * depth_utilization)`
- Costs:
  - `total_expected_cost_bps = fee_rate_bps + expected_slippage_bps`
  - `net_edge_fraction = gross_edge_fraction - (total_expected_cost_bps / 10000)`
- If `net_edge_fraction <= 0`: reject (`non_positive_net_edge_after_costs`)
- If positive but reduced vs gross edge: scale size by
  - `net_edge_scale = net_edge_fraction / gross_edge_fraction`
  - add reason `net_edge_size_scaled`

Risk metadata includes:
- `gross_edge_bps`, `net_edge_bps`, `expected_slippage_bps`, `fee_rate_bps`

## 7) Execution economics
### 7.1 Paper execution (`PaperExecutionAdapter`)
Execution intent uses risk-approved notional, midpoint reference price, max slippage bps, and TTL.

Slippage model:
- `depth_impact_bps = (requested_notional / min_depth) * 40`
- `liquidity_impact_bps = (requested_notional / liquidity) * 20`
- `slippage_bps = round((depth_impact_bps + liquidity_impact_bps) * slippage_multiplier)`

Lifecycle:
- Reject invalid notional.
- Expire if effective latency exceeds TTL.
- If slippage breaches max:
  - cancel/replace,
  - reduce notional by `execution.single_vote_size_factor`,
  - retry with backoff until retry cap.
- Fill capacity:
  - `fill_capacity_notional = min(bid_depth, ask_depth) * depth_fill_ratio` (default `0.8`)
- Partial-fill conditions:
  - reduced target from cancel/replace and/or depth-limited fill.

Execution cost accounting:
- `fee_paid = filled_notional * fee_rate_bps / 10000`
- `slippage_cost = filled_notional * slippage_bps / 10000`
- `total_execution_cost = fee_paid + slippage_cost`

### 7.2 Live CLOB execution (`PolymarketClobExecutionAdapter`)
Adds operational-economic gates:
- rollout stage enablement + real-trading flag,
- credential presence + secret provenance/age policy checks,
- pretrade balance/allowance checks,
- required market metadata (`token_id`, `tick_size`, `neg_risk` as configured),
- max order notional / max daily notional / max open orders,
- user-channel heartbeat + trade-ack reconciliation.

Submitted order economics:
- Uses metadata-defined fill ratio, slippage bps, fee bps.
- Reconciliation can revise status/fills and proportionally rescale costs.
- Persistently open unreconciled orders return `EXPIRED`.

## 8) Exit strategy economics (`ExitModule`)
Exit triggers on open positions:
1. Target-capture trigger:
   - `expected_move = abs(entry_estimated_probability - entry_midpoint)`
   - `realized_move = abs(current_midpoint - entry_midpoint)`
   - `capture_ratio = realized_move / expected_move`
   - trigger when `capture_ratio >= exit.target_capture_ratio`
2. Abnormal-volume trigger:
   - `volume_multiplier = current_volume / reference_volume`
   - trigger when `volume_multiplier >= exit.volume_spike_multiplier`
3. Stale-thesis trigger:
   - `holding_hours >= exit.stale_hours`
   - and `abs(current_midpoint - entry_midpoint) <= exit.stale_price_change_threshold`

Confirmation rule:
- `should_exit = trigger_count >= confirmation_threshold`
- current default `confirmation_threshold = 2`

When exit is confirmed in loop execution:
- open notional and open positions for that market are reduced/closed,
- exit reason codes and trigger metadata are attached.

## 9) Portfolio accounting semantics (`PortfolioState`)
Tracked state:
- `bankroll`, `day_start_equity`, `current_equity`
- `open_notional`, `open_positions`, `market_notional`
- `cumulative_fees_paid`, `cumulative_slippage_cost`, `cumulative_execution_cost`

Current equity update path:
- On executed fills, equity decreases by `total_execution_cost`.
- Mark-to-market gains/losses are not yet realized in equity.
- Therefore current `net_pnl` is primarily an execution-cost drag indicator in this phase.

## 10) Profitability attribution formulas (`TestTokenLoopRun`)
Attribution includes risk-approved trades with valid edge metadata:
- `expected_gross_edge_value += approved_notional * gross_edge_bps / 10000`
- `expected_net_edge_value += approved_notional * net_edge_bps / 10000`
- `expected_net_edge_value_on_fills += filled_notional * net_edge_bps / 10000`
- `expected_value_after_execution_cost = expected_net_edge_value_on_fills - total_execution_cost`

Weighted edge metrics:
- `average_expected_gross_edge_bps = sum(approved_notional * gross_edge_bps) / sum(approved_notional)`
- `average_expected_net_edge_bps = sum(approved_notional * net_edge_bps) / sum(approved_notional)`

Efficiency ratios:
- `expected_edge_capture_ratio = expected_net_edge_value_on_fills / expected_net_edge_value` (if denominator > 0)
- `execution_cost_to_expected_net_ratio = total_execution_cost / expected_net_edge_value_on_fills` (if denominator > 0)

## 11) Runtime economic observability
Cycle heartbeat and GUI expose:
- fills/partials, execution costs, expected-edge metrics, net_pnl, exposure.

Profitability-drift incidents are raised when:
- `expected_value_after_execution_cost < 0`, or
- `execution_cost_to_expected_net_ratio > 1.0`.

## 12) Stress and certification economics
### Scenario transforms (`scenario_pack`)
Deterministic stressors:
- latency shift,
- depth and liquidity multipliers,
- probability shift,
- midpoint shift.

### Stress certification (`stress_certification`)
Thresholded certification checks include:
- minimum scenario count,
- minimum total allowed trades,
- maximum zero-trade scenarios,
- max open notional envelope,
- soak success and recovery criteria.

### TRL4 profitability gate
`scripts/run_trl4_profitability_report.py` enforces:
- runtime duration >= configured minimum (default 24h),
- profitability metrics present,
- latest `expected_value_after_execution_cost >= minimum`,
- latest `expected_net_edge_value_on_fills >= minimum`,
- net_pnl present (sign optional if gate allows negative).

Current gate (`config/certification/trl4_24h_profitability_gate.v1.json`) is:
- `min_runtime_hours = 24.0`
- `minimum_expected_value_after_execution_cost = 0.0`
- `minimum_expected_net_edge_value_on_fills = 0.0`
- `require_profitability_metrics = true`
- `allow_negative_net_pnl = true`

## 13) Effective strategy behavior (current phase)
- Strict entry quality via edge/depth/liquidity/time filters.
- Cost-adjusted Kelly-style sizing rather than raw Kelly.
- Slippage-bounded execution with cancel/replace and TTL behavior.
- Multi-trigger exit confirmation (2-of-3).
- Expected-value-centric profitability attribution with explicit execution-cost accounting.
- LLM remains economically non-authoritative under advisory-only calibration.
- Replay-first, deterministic, and auditable stress/certification workflow.
