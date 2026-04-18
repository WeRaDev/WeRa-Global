# ProductionBase baseline bootstrap
Use this guide to initialize each `ProductionBase/*` repository to the umbrella baseline.

## Baseline requirements per project
- `README.md`
- `WARP.md`
- `CONTRIBUTING.md`
- `.gitea/workflows/`
- `docs/adr/`
- `tasks/`
- `skills/`

## Bootstrap sequence
1. Open the target project repository directly.
2. Create missing folders:
   - `docs/adr/`
   - `tasks/`
   - `skills/`
3. Add minimal seed files:
   - `docs/adr/0000-adr-template.md`
   - `tasks/README.md`
   - `skills/README.md`
4. Align project `README.md` to the umbrella README contract.
5. Register project-specific workflows and quality checks in `CONTRIBUTING.md`.

## Validation checklist
- Required baseline files and folders exist.
- Project docs match actual build/test/lint workflow.
- First sprint-ready tasks are defined under project `tasks/`.
- At least one ADR seed exists in `docs/adr/`.
