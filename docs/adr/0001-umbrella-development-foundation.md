# 0001 - Umbrella development foundation and quality operating model

## Status
Accepted

## Date
2026-04-15

## Context
WeRa Global needed a consistent project initialization baseline to improve development quality, onboarding clarity, and execution efficiency across umbrella and production repositories.
Core governance existed in `WARP.md`, but contributor flow and startup artifacts were incomplete or fragmented.

## Decision
Adopt and operationalize a unified umbrella development foundation consisting of:
- Behavioral guardrails in `CLAUDE.md`
- Skill framework and execution profiles in `skills/`
- Contributor workflow in `CONTRIBUTING.md`
- ADR system in `docs/adr/`
- Task planning cadence in `tasks/`
- Production baseline bootstrap guide in `ProductionBase/BOOTSTRAP.md`

## Alternatives considered
- Keep governance centralized only in `WARP.md` without additional scaffolding.
- Defer contributor and sprint artifacts until per-project implementation begins.
- Maintain process guidance only within subproject repositories.

## Consequences
### Positive
- Faster contributor onboarding with explicit execution flow.
- Reduced ambiguity and overengineering through behavioral guardrails.
- Improved decision traceability via ADRs.
- Better weekly planning discipline with task scaffolding.

### Negative
- Additional documentation maintenance overhead.
- Requires periodic synchronization between umbrella and subproject docs.

## Validation plan
- Confirm all umbrella artifacts are present and referenced from `README.md`.
- Use `tasks/backlog.md` and `tasks/sprint-template.md` for active planning cycles.
- Track major architectural choices with incremental ADRs.

## Follow-up actions
- Apply baseline folder structure to each `ProductionBase/*` repository.
- Standardize project README files to umbrella documentation contract.
- Create project-level ADR seeds in active subprojects.
