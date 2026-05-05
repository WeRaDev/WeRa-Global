# ProductionBase baseline bootstrap
Use this guide to initialize each `ProductionBase/*` repository to the umbrella baseline.

## Baseline requirements per project
- `README.md`
- `WARP.md`
- `AGENTS.md`
- `SOUL.md`
- `CONTRIBUTING.md`
- `.gitea/workflows/`
- `docs/adr/`
- `tasks/`
- `skills/`

## Registry and VCS alignment
- Every tracked production project must be registered in `ProductionBase/repos.yaml`.
- Set `vcs_mode` to `submodule` when the project is tracked via `.gitmodules`, and to `native` when code is versioned directly in this umbrella repository.
- Set `baseline_policy`:
  - `enforced` for native projects (validated in umbrella CI),
  - `delegated` for submodule projects (validated in the project repository CI).

## Bootstrap sequence
1. Open the target project repository directly.
2. Add required instruction files:
   - `AGENTS.md` (canonical provider-agnostic instructions for agents)
   - `WARP.md` (project governance/safety/process)
   - `SOUL.md` (project constitutional layer inheriting from umbrella `SOUL.md`)
   - Optional `CLAUDE.md` compatibility shim that points to `AGENTS.md`
3. Create missing folders:
   - `docs/adr/`
   - `tasks/`
   - `skills/`
4. Add minimal seed files:
   - `AGENTS.md`
   - `SOUL.md`
   - `docs/adr/0000-adr-template.md`
   - `tasks/README.md`
   - `skills/README.md`
5. Align project `README.md` to the umbrella README contract.
6. Register project-specific workflows and quality checks in `CONTRIBUTING.md`.
7. Include project pull-request review guidance aligned with `revisor-pr-audit` (severity taxonomy + structured review report).

## Migration from CLAUDE.md to AGENTS.md
When a project already has `CLAUDE.md`:
1. Move canonical instructions into `AGENTS.md`.
2. Keep `CLAUDE.md` as a short compatibility shim referencing `AGENTS.md`.
3. Do not maintain two independent instruction documents.

## New project compliance rule
When creating any new `ProductionBase/*` project, initialization is incomplete until:
1. `SOUL.md` is created and explicitly inherits umbrella `SOUL.md`.
2. `AGENTS.md`, `WARP.md`, and `CONTRIBUTING.md` reference and remain consistent with the project `SOUL.md`.
3. The project is registered in `ProductionBase/repos.yaml` with baseline policy and CI in place.
4. Pull-request review workflow is defined and aligned with umbrella `revisor-pr-audit` quality standards.

## Python asyncio enhancement (systemPY)
For Python projects with multiple entrypoints or complex startup/shutdown logic:
- Add `systemPY` and define lifecycle in component `Unit` classes.
- Use lifecycle stages consistently (`on_init`, `pre_startup`, `on_startup`, `on_shutdown`, `post_shutdown`, `on_exit`).
- Compose app behavior from mixins instead of duplicating init/teardown logic per entrypoint.
- Keep shutdown paths explicit and test graceful stop/reload behavior.

## Validation checklist
- Required baseline files and folders exist.
- Project docs match actual build/test/lint workflow.
- First sprint-ready tasks are defined under project `tasks/`.
- At least one ADR seed exists in `docs/adr/`.
