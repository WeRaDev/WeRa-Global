# WeRa-Global Umbrella Rules

## Scope
This repository is the umbrella for:
- `KnowledgeBase/`
- `ProductionBase/`

## Governance
- `KnowledgeBase/` is the canonical business and technical context source.
- `ProductionBase/` contains independent sub-project repositories.
- Any new production project must be added to `ProductionBase/repos.yaml`.

## Change policy
- Do not add heavy archival or customer raw data into umbrella history.
- Keep `_Archive/`, `Customers/`, and `Old_documents/` outside canonical tracking.
- Prefer project-local changes inside the corresponding `ProductionBase/*` repository.

## Operational baseline
Each `ProductionBase/*` repository should include:
- `README.md`
- `WARP.md`
- `CONTRIBUTING.md`
- `.gitea/workflows/`
