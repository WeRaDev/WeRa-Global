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
- `src/poly_robot/`: governance, replay, strategy, risk, and policy modules.
- `tests/`: governance + replay + strategy/risk/LLM policy unit tests.
- `tasks/`: task backlogs and sprint-ready items.
- `skills/`: project-specific Warp agent skills.

## Current maturity
- Stage: incubation / project bootstrap.
- Implementation status: scaffold only, no production modules yet.
- Next milestone: define MVP architecture and initial simulation workflow.

## Phase-1 MVP implementation status
Parameter governance structure is now in place for MVP planning and test-token operation:
- Canonical catalog with ownership, type/range constraints, mutability, and change-control metadata.
- Test-token profile (`mvp_test_token`) with explicit frozen baseline.
- Formal requirements spec with explicit definitions for strategy variables.
- Validation CLI and automated tests to enforce governance + advisory-only LLM policy before runtime.
- Replay-first harness and risk-first execution contract are implemented before any execution adapter.

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
