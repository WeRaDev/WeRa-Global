# Poly-Robot
Poly-Robot is an incubation-stage WeRa Global sub-project focused on modular robotics workflows and multi-agent orchestration.

## Scope (initial)
- Define project architecture and operating constraints for robotics control logic.
- Establish delivery workflow, quality baseline, and documentation structure.
- Prepare a safe path toward simulation-first development before hardware coupling.

## Project structure
- `README.md`: project context and onboarding.
- `WARP.md`: project-specific agent operating rules and guardrails.
- `CONTRIBUTING.md`: contribution standards and definition of done.
- `.gitea/workflows/`: CI baseline checks.
- `config/parameters/`: Phase-1 parameter governance catalog, profiles, and freeze baselines.
- `config/calibration/`: LLM calibration status and reliability threshold policy.
- `config/replay/`: replay scenario-pack definitions for deterministic stress transforms.
- `docs/requirements/`: formal MVP requirements and strategy-variable definitions.
- `scripts/validate_parameters.py`: governance validation entrypoint.
- `scripts/run_replay_harness.py`: deterministic replay runner for strategy+risk contract validation.
- `scripts/run_scenario_matrix.py`: multi-scenario replay runner producing stress-report JSON.
- `scripts/run_test_token_loop.py`: end-to-end test-token loop runner (strategy -> risk -> paper execution).
- `scripts/run_runtime_supervisor.py`: C1 runtime supervision runner (heartbeat/retries/snapshot journal).
- `scripts/run_runtime_soak.py`: deterministic soak orchestration runner with drill injection and interval health snapshots.
- `scripts/run_stress_certification.py`: stress campaign + certification artifact runner for thresholded pass/fail decisions.
- `scripts/run_runtime_gui.py`: web operator console for runtime state/journal visibility, audited controls, incident navigation, and run-to-run comparison.
- `src/poly_robot/`: governance, replay, strategy, risk, execution, and policy modules.
- `src/poly_robot/integration_adapters.py`: hardened ingestion + execution gateway adapters for bounded retries/timeouts/degraded mode.
- `src/poly_robot/exit_module.py`: multi-trigger exit engine for target-capture, volume-spike, and stale-thesis confirmations.
- `src/poly_robot/stress_certification.py`: certification evaluator that scores scenario-matrix and soak evidence against explicit gates.
- `tests/`: governance + replay + strategy/risk + execution + loop integration unit tests.
- `tasks/`: task backlogs and sprint-ready items.
- `skills/`: project-specific Warp agent skills.

## Current maturity
- Stage: incubation with active MVP execution-track development.
- Implementation status: deterministic replay + risk controls + scenario matrix + paper execution loop + runtime reliability supervision + stress certification.
- Next milestone: complete longer-duration soak certification envelopes and external interface hardening.

## Phase-1 MVP implementation status
Parameter governance structure is now in place for MVP planning and test-token operation:
- Canonical catalog with ownership, type/range constraints, mutability, and change-control metadata.
- Test-token profile (`mvp_test_token`) with explicit frozen baseline.
- Formal requirements spec with explicit definitions for strategy variables.
- Validation CLI and automated tests to enforce governance + advisory-only LLM policy before runtime.
- Replay-first harness and risk-first execution contract are implemented.

## Milestone B execution-track status
- Deterministic paper execution adapter is available with auditable order outcomes (`FILLED`, `PARTIALLY_FILLED`, `REJECTED`, `EXPIRED`, `SKIPPED`).
- Execution lifecycle now includes submit/cancel/replace transitions, retry backoff behavior, TTL expiry handling, and partial-fill simulation.
- Fee/slippage accounting is tracked per fill and aggregated into loop reports and portfolio state.
- End-to-end loop runs strategy, risk gating, and paper execution in a single reproducible pipeline with execution telemetry and reproducibility fingerprints.

## Milestone C1 runtime reliability status
- Runtime supervisor foundation is implemented with bounded retries, exponential retry backoff, and heartbeat timeout enforcement.
- Supervisor now emits append-only runtime journal events and writes restart-safe latest-state snapshots per cycle.
- C1 runner executes the test-token loop under supervision for multi-cycle soak-style validation.
- Web GUI operator console foundation now exposes supervisor/journal parity, loop metrics, and role-bounded audited control actions.
- Runtime supervisor now consumes operator control state for pause/resume, graceful restart acknowledgement, and scenario-selection enforcement per cycle.

## Milestone C2 integration hardening status
- Ingestion path now runs through a hardened adapter with schema validation, bounded retries, timeout budgeting, deduplication, and explicit degraded/failed outcomes.
- Execution path now runs through a bounded execution gateway with idempotency-key caching, timeout enforcement, retry caps, and degraded reject behavior on persistent failures.
- Test-token loop and runtime supervisor runners are wired to these adapters with configuration surfaced via CLI flags.

## Milestone C3 exit and soak orchestration status
- Exit decisions are now first-class runtime outputs with multi-trigger confirmation across target capture, abnormal volume spikes, and stale-thesis detection.
- Loop records now include reason-coded exit telemetry and aggregate exit counters (`exit_candidate_count`, `confirmed_exit_count`) for supervisor/dashboard parity.
- A dedicated soak orchestration runner now rotates scenarios by interval and records append-only health snapshots for each interval execution.
- Deterministic recovery drills are now built into soak runs: intentional restart requests, temporary data unavailability, and delayed execution-response injections.

## Milestone C4 stress certification status
- Stress campaign execution now supports a certification builder that evaluates scenario-matrix and soak artifacts against explicit pass/fail thresholds.
- Certification outputs include criterion-level decisions, incident summaries for failed gates, and reproducibility-linked evidence hashes.

## Milestone C5 operator console hardening status
- Dashboard now supports operator-facing action-history filtering by actor and action for rapid control-intent audit review.
- Incident feed supports cursor-based navigation for historical incident triage during soak operations.
- Run-to-run cycle comparison now exposes configurable windows with per-cycle deltas across key loop metrics (`events`, `risk_allowed_count`, `filled_trade_count`, `exit_candidate_count`, `confirmed_exit_count`).
- Runtime GUI includes filter controls and incident navigation actions (`Apply Filters`, `Reset Filters`, `Newer Incidents`, `Older Incidents`) so the hardened backend observability paths are directly accessible from the console.

Run validation:
```bash
python3 scripts/validate_parameters.py \
  --catalog config/parameters/catalog.v1.json \
  --profile config/parameters/profiles/mvp_test_token.v1.json \
  --baseline config/parameters/baselines/mvp_test_token.freeze.v1.json \
  --calibration-policy config/calibration/llm_reliability.v1.json
```

Run deterministic replay harness:
```bash
python3 scripts/run_replay_harness.py \
  --events tests/fixtures/replay_events.jsonl \
  --profile config/parameters/profiles/mvp_test_token.v1.json \
  --calibration-policy config/calibration/llm_reliability.v1.json \
  --scenario-pack config/replay/scenario_pack.v1.json \
  --scenario liquidity_crunch
```

Run scenario matrix report:
```bash
python3 scripts/run_scenario_matrix.py \
  --events tests/fixtures/replay_events.jsonl \
  --profile config/parameters/profiles/mvp_test_token.v1.json \
  --calibration-policy config/calibration/llm_reliability.v1.json \
  --scenario-pack config/replay/scenario_pack.v1.json \
  --output replay_stress_report.json
```

Run end-to-end test-token loop:
```bash
python3 scripts/run_test_token_loop.py \
  --events tests/fixtures/replay_events.jsonl \
  --profile config/parameters/profiles/mvp_test_token.v1.json \
  --calibration-policy config/calibration/llm_reliability.v1.json \
  --scenario-pack config/replay/scenario_pack.v1.json \
  --scenario baseline \
  --output test_token_loop_report.json
```

Run C1 runtime supervisor:
```bash
python3 scripts/run_runtime_supervisor.py \
  --events tests/fixtures/replay_events.jsonl \
  --profile config/parameters/profiles/mvp_test_token.v1.json \
  --calibration-policy config/calibration/llm_reliability.v1.json \
  --scenario-pack config/replay/scenario_pack.v1.json \
  --scenario baseline \
  --cycles 3 \
  --control-state-path runtime/operator_control_state.json \
  --control-audit-path runtime/operator_action_audit.jsonl \
  --cycle-output-dir runtime/cycles
```

Run runtime web GUI:
```bash
python3 scripts/run_runtime_gui.py \
  --state-path runtime/runtime_state.json \
  --journal-path runtime/runtime_journal.jsonl \
  --control-state-path runtime/operator_control_state.json \
  --audit-path runtime/operator_action_audit.jsonl \
  --host 127.0.0.1 \
  --port 8765
```
GUI operator guide (financial dashboard + controls):
1. Start runtime supervision so the GUI has fresh cycle state:
```bash
python3 scripts/run_runtime_supervisor.py \
  --events tests/fixtures/replay_events.jsonl \
  --profile config/parameters/profiles/mvp_test_token.v1.json \
  --calibration-policy config/calibration/llm_reliability.v1.json \
  --scenario-pack config/replay/scenario_pack.v1.json \
  --scenario baseline \
  --cycles 3 \
  --control-state-path runtime/operator_control_state.json \
  --control-audit-path runtime/operator_action_audit.jsonl \
  --cycle-output-dir runtime/cycles
```
2. Run the GUI and open `http://127.0.0.1:8765` in a browser.
3. Use **Financial Dashboard** to monitor:
   - `current_equity`, `net_pnl`, and `day_start_equity`
   - `open_notional`, `open_positions`, and `total_exposure_fraction`
   - `total_fees_paid`, `total_slippage_cost`, `total_execution_cost`, and `fill_rate`
4. Use **Operator Controls** to control Poly-Robot runtime:
   - `Pause`: blocks new cycle execution but keeps runtime alive
   - `Resume`: removes pause gate and continues processing
   - `Graceful Restart`: requests supervisor restart acknowledgement before next cycle
   - `Set Scenario`: changes scenario used by the next cycle
   - `Annotate Incident`: appends an audited operator note
5. If GUI is started without `--operator-token`, controls are read-only and POST control actions return 403.

Operator token configuration (Docker Compose runtime-gui):
1. Set a strong operator token in your shell before startup:
```bash
export POLY_ROBOT_OPERATOR_TOKEN="replace-with-strong-token"
```
2. Rebuild/restart dashboard service so compose injects the token:
```bash
docker compose up -d --build runtime-gui
```
3. Verify token-required mode in logs:
```bash
docker compose logs --tail=20 runtime-gui
```
Expected startup line includes `control_mode=token_required`.
4. Control API calls must include `X-Operator-Token`; otherwise requests return 403:
```bash
curl -X POST http://127.0.0.1:8765/api/control/pause \
  -H "Content-Type: application/json" \
  -H "X-Operator-Token: $POLY_ROBOT_OPERATOR_TOKEN" \
  -d '{"actor":"operator","reason":"manual_pause"}'

curl -X POST http://127.0.0.1:8765/api/control/resume \
  -H "Content-Type: application/json" \
  -H "X-Operator-Token: $POLY_ROBOT_OPERATOR_TOKEN" \
  -d '{"actor":"operator","reason":"manual_resume"}'
```

Runtime GUI API examples for hardened operator views:
```bash
curl "http://127.0.0.1:8765/api/dashboard?audit_actor=operator&audit_action=incident_annotation&incident_limit=20&comparison_window=15"
curl "http://127.0.0.1:8765/api/incidents?limit=25&cursor=50"
curl "http://127.0.0.1:8765/api/comparison?window=12"
```
Docker deployment (local):
```bash
docker compose config --quiet
docker compose build runtime-gui
docker compose up -d runtime-gui
curl http://127.0.0.1:8765/healthz
```

Run the supervisor in Docker (optional):
```bash
docker compose --profile runner run --rm runtime-supervisor
```

Stop local Docker services:
```bash
docker compose down
```

Run deterministic runtime soak orchestration:
```bash
python3 scripts/run_runtime_soak.py \
  --events tests/fixtures/replay_events.jsonl \
  --profile config/parameters/profiles/mvp_test_token.v1.json \
  --calibration-policy config/calibration/llm_reliability.v1.json \
  --scenario-pack config/replay/scenario_pack.v1.json \
  --scenario-rotation baseline,liquidity_crunch,latency_spike \
  --intervals 6 \
  --drill-restart-intervals 2 \
  --drill-data-unavailable-intervals 3 \
  --drill-delayed-execution-intervals 4 \
  --health-snapshot-path runtime/soak_health_snapshots.jsonl \
  --summary-path runtime/soak_summary.json
```

Run stress campaign certification:
```bash
python3 scripts/run_stress_certification.py \
  --events tests/fixtures/replay_events.jsonl \
  --profile config/parameters/profiles/mvp_test_token.v1.json \
  --calibration-policy config/calibration/llm_reliability.v1.json \
  --scenario-pack config/replay/scenario_pack.v1.json \
  --soak-summary runtime/soak_summary.json \
  --matrix-output runtime/stress_matrix_report.json \
  --output runtime/stress_campaign_certification.json
```
