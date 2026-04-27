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
  - `PYTHONPATH=src python3 -m mypy src/poly_robot`
- UX regression checks:
  - `PYTHONPATH=src python3 -m unittest tests.test_runtime_web_gui tests.test_runtime_supervisor_controls tests.test_runtime_supervisor_live`
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
