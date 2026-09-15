# Contributing to Human Center

## Branching and pull requests
- Default branch: `main` (versioned in the `WeRa-Global` umbrella repository; `HumanCenter` is a `native` project per `ProductionBase/repos.yaml`).
- Use short-lived topic branches (`feat/humancenter-*`, `fix/humancenter-*`, `chore/humancenter-*`).
- Keep pull requests focused and include verification steps.

## Definition of Ready
A task is ready only when it has:
- Problem statement and scope/non-scope
- Acceptance criteria
- Dependency list
- Validation plan

## Definition of Done
A task is done only when:
- Implementation (or knowledgebase update) is complete and reviewed
- Baseline and knowledgebase-structure CI checks pass
- Documentation and operational notes are updated
- New/changed `KnowledgeBase/` claims carry an accurate `evidence_status`

## Required checks
- Baseline check: `.gitea/workflows/ci.yml` `baseline-check` job (required files/folders exist).
- Knowledgebase structure check: `.gitea/workflows/ci.yml` `kb-structure-check` job (every `kb-*` folder has a `README.md`).
- Lint/typecheck/tests: to be added in the same pull request that introduces automation delivery code.

## Security and compliance
- Never include real client credentials, session artifacts, or private client files in commits.
- All client data handling must follow signed DPA terms and least-privilege access once client work begins.

## Pull-request review
- Non-trivial pull requests should follow the umbrella `revisor-pr-audit` skill output contract (verdict, severity taxonomy, actionable findings, confidence/depth declaration).
