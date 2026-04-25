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
- `scripts/run_runtime_gui.py`: web operator console for runtime state/journal visibility and audited controls.
- `src/poly_robot/`: governance, replay, strategy, risk, execution, and policy modules.
- `src/poly_robot/integration_adapters.py`: hardened ingestion + execution gateway adapters for bounded retries/timeouts/degraded mode.
- `src/poly_robot/exit_module.py`: multi-trigger exit engine for target-capture, volume-spike, and stale-thesis confirmations.
- `tests/`: governance + replay + strategy/risk + execution + loop integration unit tests.
- `tasks/`: task backlogs and sprint-ready items.
- `skills/`: project-specific Warp agent skills.

## Current maturity
- Stage: incubation with active MVP execution-track development.
- Implementation status: deterministic replay + risk controls + scenario matrix + paper execution loop.
- Next milestone: extend Milestone C runtime reliability and soak orchestration.

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
