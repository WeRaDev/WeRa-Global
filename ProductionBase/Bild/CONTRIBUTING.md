# Contributing to Bild

## Branching and pull requests
- Default branch: `main`.
- Use short-lived topic branches (`feat/*`, `fix/*`, `chore/*`).
- Keep pull requests focused and include verification steps.

## Definition of Ready
A task is ready only when it has:
- Problem statement and scope/non-scope
- Acceptance criteria
- Dependency list
- Validation plan

## Definition of Done
A task is done only when:
- Implementation is complete and reviewed
- Tests for changed scope pass
- Lint/type checks pass
- Documentation and operational notes are updated

## Required checks (to be finalized in Sprint 1)
- Lint: `ruff check .`
- Format: `ruff format --check .`
- Type check: `mypy .`
- Tests: `pytest`

If a command is not yet available, add it in the same pull request that introduces the tooling.

## Security and compliance
- Never include real client credentials, session artifacts, or private project files in commits.
- All pilot-client data handling must follow signed DPA terms and least-privilege access.

