# Contributing to WeRa Global
This document defines how to contribute across the umbrella repository and its `ProductionBase/*` projects with consistent quality, clarity, and speed.

## Scope
- This repository is the umbrella coordination layer for WeRa Global.
- `KnowledgeBase/` is the canonical context source.
- `ProductionBase/*` repositories are independent implementation projects.

## Required reading before implementation
1. `README.md`
2. `WARP.md`
3. `AGENTS.md`
4. `SOUL.md`
5. Project-level `ProductionBase/<project>/SOUL.md`, `ProductionBase/<project>/AGENTS.md` (if present), and `ProductionBase/<project>/WARP.md` for touched subprojects

## Contribution workflow
1. Define scope in `tasks/backlog.md` or a sprint file.
2. If architecture or policy is affected, create/update an ADR in `docs/adr/`.
3. Execute using the default flow in `skills/registry.yaml`.
4. Validate with repository-native checks for touched code.
5. Update docs and task artifacts in the same change cycle.

## Quality requirements
- Keep changes minimal and traceable to the task objective.
- Surface assumptions and ambiguity before implementation.
- Prefer simplest sufficient solution over speculative abstractions.
- Include explicit verification evidence for completed changes.

## Documentation update rules
- Update `README.md` for onboarding-impacting changes.
- Add or update ADRs for significant architectural decisions.
- Keep `tasks/` current with actual planning and execution state.
- Do not leave process-critical changes undocumented.

## Work in ProductionBase projects
- Treat each `ProductionBase/*` directory as an independent repository.
- Use `ProductionBase/BOOTSTRAP.md` to align project baseline structure (`AGENTS.md`, `SOUL.md`, `docs/adr/`, `tasks/`, `skills/`).
- Follow each project's `CONTRIBUTING.md` and `WARP.md` when editing there.
- For Python asyncio projects with multiple entrypoints, evaluate `systemPY` to standardize startup/shutdown lifecycle and graceful teardown.

## Security and operational hygiene
- Never commit secrets or sensitive raw customer data.
- Use least-privilege credentials and scoped access.
- For stateful or high-impact changes, document rollback path and validation checks.
