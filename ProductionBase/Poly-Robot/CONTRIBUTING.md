# Contributing to Poly-Robot

## Branching and pull requests
- Default branch: `main`.
- Use short-lived topic branches (`feat/*`, `fix/*`, `chore/*`).
- Keep pull requests focused and include concrete verification steps.

## Definition of Ready
A task is ready only when it has:
- Problem statement and scope/non-scope
- Acceptance criteria
- Dependencies and assumptions
- Validation plan

## Definition of Done
A task is done only when:
- Implementation is complete and reviewed
- Relevant tests for changed scope pass
- Lint/type checks pass
- Documentation and operational notes are updated

## Baseline checks
- Lint:
  - `ruff check src/poly_robot tests scripts`
- Governance validation:
  - `python3 scripts/validate_parameters.py --catalog config/parameters/catalog.v1.json --profile config/parameters/profiles/mvp_test_token.v1.json --baseline config/parameters/baselines/mvp_test_token.freeze.v1.json --calibration-policy config/calibration/llm_reliability.v1.json`
- Unit test suite:
  - `PYTHONPATH=src python3 -m unittest discover -s tests -p "test_*.py"`
- Security regression checks:
  - `PYTHONPATH=src python3 -m unittest tests.test_integration_adapters tests.test_llm_policy tests.test_parameter_governance`
- Security static analysis:
  - `bandit -q -r src/poly_robot scripts -s B404,B603,B310,B105`
- Type check:
  - `python3 scripts/run_typecheck.py`
- UX regression checks:
  - `PYTHONPATH=src python3 -m unittest tests.test_runtime_web_gui tests.test_runtime_supervisor_controls tests.test_runtime_supervisor_live`
- D3 rollout rehearsal protocol:
  - `python3 scripts/run_rollout_rehearsal.py --protocol-config config/integration/live_rollout_rehearsal.v1.json --work-dir runtime/rollout_rehearsal --output-path runtime/rollout_rehearsal_report.json`
  - Treat non-zero `summary.failed_command_bundles` or `summary.failed_bundle_commands` in `runtime/rollout_rehearsal_report.json` as rollout-blocking and resolve before promotion.
- E3 canary readiness certification:
  - `python3 scripts/run_canary_readiness_certification.py --rehearsal-report runtime/rollout_rehearsal_report.json --criteria-config config/integration/canary_promotion_criteria.v1.json --approval-status pending --output runtime/canary_rollout_certification_report.json`
  - Treat `overall_status=FAIL` in `runtime/canary_rollout_certification_report.json` as canary-promotion blocking.
  - CI gate sequence is mandatory: rehearsal report gate first, then canary readiness certification gate.
- F2 canary stage enablement approval gate:
  - `python3 scripts/run_canary_stage_enablement.py --certification-report runtime/canary_rollout_certification_report.json --approval-record config/integration/canary_approval_record_template.v1.json --rollout-config config/integration/live_trade_rollout.v1.json --requested-stage canary_live --decision-output runtime/canary_stage_enablement_decision.json --audit-output runtime/canary_stage_enablement_audit.jsonl --actor release_manager --reason "phase-f2-gate-evaluation"`
  - Treat `decision_status=DENY` in `runtime/canary_stage_enablement_decision.json` as rollout-blocking.
  - Treat missing append-only audit evidence in `runtime/canary_stage_enablement_audit.jsonl` as policy non-compliance for promotion actions.
- F3 canary rollback guard:
  - `python3 scripts/run_canary_rollback_guard.py --enablement-decision runtime/canary_stage_enablement_decision.json --certification-report runtime/canary_rollout_certification_report.json --rehearsal-report runtime/rollout_rehearsal_report.json --cycle-report-dir runtime/rollout_rehearsal --cycle-report-pattern "**/cycle_*.json" --policy-config config/integration/canary_rollback_policy.v1.json --guard-output runtime/canary_rollback_guard_report.json --incident-output runtime/canary_rollback_incident_report.json --audit-output runtime/canary_rollback_guard_audit.jsonl --actor runtime_operator_on_call --reason "phase-f3-gate-evaluation" || true`
  - Treat `guard_status=FAIL` in `runtime/canary_rollback_guard_report.json` as mandatory rollback/hold signal.
  - Treat `incident_handoff.incident_status=OPEN` in `runtime/canary_rollback_incident_report.json` as required handoff event with emergency action ownership.
  - Treat missing append-only guard evidence in `runtime/canary_rollback_guard_audit.jsonl` as policy non-compliance for rollback enforcement.
- F4 canary lifecycle gate:
  - `python3 scripts/run_canary_lifecycle_gate.py --rehearsal-report runtime/rollout_rehearsal_report.json --criteria-config config/integration/canary_promotion_criteria.v1.json --approval-record config/integration/canary_approval_record_template.v1.json --rollout-config config/integration/live_trade_rollout.v1.json --policy-config config/integration/canary_rollback_policy.v1.json --cycle-report-dir runtime/rollout_rehearsal --cycle-report-pattern "**/cycle_*.json" --requested-stage canary_live --approval-status pending --certification-output runtime/canary_rollout_certification_report.json --decision-output runtime/canary_stage_enablement_decision.json --enablement-audit-output runtime/canary_stage_enablement_audit.jsonl --guard-output runtime/canary_rollback_guard_report.json --incident-output runtime/canary_rollback_incident_report.json --guard-audit-output runtime/canary_rollback_guard_audit.jsonl --summary-output runtime/canary_lifecycle_gate_report.json --decision-actor release_manager --guard-actor runtime_operator_on_call --reason "phase-f4-lifecycle-gate-evaluation" || true`
  - Treat `overall_status=FAIL` in `runtime/canary_lifecycle_gate_report.json` as rollout-blocking for promotion attempts.
  - Promotion-ready lifecycle validation should run with `--approval-status approved --auto-approve-required-approvers` and must return `overall_status=PASS`.
- Docker deployment sanity:
  - `docker compose config --quiet`
  - `docker compose build runtime-gui`

If a command is not yet available, add it in the same pull request that introduces the related tooling.

## Security
- Never include real credentials, API tokens, hardware access keys, or private telemetry in commits.
- Use least-privilege and explicit approval for any operation that can affect physical systems.
- For live CLOB startup (`--execution-mode live_polymarket_clob` + enabled real-order rollout stage + `--allow-real-trading`), credential preflight is mandatory.
- For each required credential (`POLYMARKET_PRIVATE_KEY`, `POLYMARKET_FUNDER_ADDRESS`, `POLYMARKET_API_KEY`, `POLYMARKET_API_SECRET`, `POLYMARKET_API_PASSPHRASE`), provide:
  - `<ENV_VAR>`
  - `<ENV_VAR>_SOURCE` (must be one of configured preferred sources)
  - `<ENV_VAR>_LAST_ROTATED_AT` (UTC ISO8601 timestamp)
- `config/integration/live_trade_rollout.v1.json` `secrets_policy.max_secret_age_days` defines rotation SLO (currently `30` days); stale credentials are startup-blocking.
- Use non-interactive secret loading patterns and never echo secret values:
  - `export POLYMARKET_API_KEY="$(secret_manager read --key polymarket/api_key)"`
  - `export POLYMARKET_API_KEY_SOURCE="vault"`
  - `export POLYMARKET_API_KEY_LAST_ROTATED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"`
- Treat startup failures containing `Live credential preflight failed` as blocking incidents and resolve by rotating/reloading credentials plus metadata refresh before retry.
- Treat non-empty `rollback_recommendations` in `runtime/rollout_rehearsal_report.json` as rollout-blocking incidents; resolve trigger conditions and rerun D3 rehearsal before advancing rollout stage.
- Canary enablement approval boundary:
  - Promotion owner: `release_manager`.
  - Required approvers: `release_manager` and `runtime_operator_on_call`.
  - Rollback authority: `runtime_operator_on_call` and `incident_commander`.
  - Keep approval entries in `config/integration/canary_approval_record_template.v1.json` as `pending` until explicit sign-off is recorded for each required approver.
  - Do not enable `canary_live` stage unless `runtime/canary_stage_enablement_decision.json` reports `decision_status=ALLOW`.
  - Preserve `runtime/canary_stage_enablement_audit.jsonl` as append-only evidence for every promotion attempt (allowed or denied).
- F3 rollback incident handoff boundary:
  - Use `config/integration/canary_rollback_policy.v1.json` as the source of truth for trigger thresholds, emergency actions, and authority mapping.
  - Keep `runtime/canary_rollback_incident_report.json` synchronized with `runtime/canary_rollback_guard_report.json` for every guard evaluation.
  - Any `incident_status=OPEN` requires explicit handoff to `runtime_operator_on_call` (primary), escalation to `incident_commander`, and release-hold acknowledgement by `release_manager`.
  - Preserve `runtime/canary_rollback_guard_audit.jsonl` as append-only evidence for every guard run, including PASS and FAIL outcomes.
