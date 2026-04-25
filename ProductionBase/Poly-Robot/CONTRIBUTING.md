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

## Baseline checks (to be finalized)
- Lint: `ruff check .`
- Format: `ruff format --check .`
- Type check: `mypy .`
- Tests: `pytest`
- Governance validation:
  - `python3 scripts/validate_parameters.py --catalog config/parameters/catalog.v1.json --profile config/parameters/profiles/mvp_test_token.v1.json --baseline config/parameters/baselines/mvp_test_token.freeze.v1.json --calibration-policy config/calibration/llm_reliability.v1.json`
- Unit tests:
  - `PYTHONPATH=src python3 -m unittest discover -s tests -p "test_*.py"`

If a command is not yet available, add it in the same pull request that introduces the related tooling.

## Security
- Never include real credentials, API tokens, hardware access keys, or private telemetry in commits.
- Use least-privilege and explicit approval for any operation that can affect physical systems.
