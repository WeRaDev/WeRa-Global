# WeRa-Global
Unified umbrella repository for WeRa Global.

## Repository structure
- `KnowledgeBase/` — canonical project knowledge, strategy, legal, architecture, and financial documentation.
- `ProductionBase/` — software production repositories mounted as independent git projects.

## ProductionBase projects
- `ProductionBase/SolarSeed-v3`
- `ProductionBase/FilantropiaSolar`
- `ProductionBase/FreeDoo`
- `ProductionBase/wera-contracts`
- `ProductionBase/SolarSim`
- `ProductionBase/Bild`
- `ProductionBase/Poly-Robot`

## Working model
- Use this repository as the single onboarding and navigation entry point.
- Keep `KnowledgeBase/` versioned directly in this umbrella repository.
- Keep each `ProductionBase/*` project independent, with dedicated instructions and CI.
- Update `ProductionBase/repos.yaml` whenever project remotes, branches, or ownership change.
- Poly-Robot is now migrated to an independent delegated repository and tracked here as submodule path `ProductionBase/Poly-Robot`.

## Development quality framework
- `AGENTS.md` — canonical provider-agnostic behavioral guardrails for coding agents.
- `SOUL.md` — umbrella constitutional layer for service posture, non-coercion, and crisis behavior.
- `CLAUDE.md` — compatibility shim that delegates to `AGENTS.md` for tools expecting legacy filename conventions.
- `WARP.md` — umbrella governance, delivery process, and repository policy baseline.
- `CONTRIBUTING.md` — contribution workflow, quality requirements, and documentation update rules.
- `skills/` — reusable operational skills used across WeRa Global and inherited by `ProductionBase/*` repositories.
- `skills/registry.yaml` — canonical index and recommended skill execution flow.
- `skills/evals/evals.json` — baseline prompts for periodic skill quality review.
- `docs/adr/` — architecture decision record system and templates.
- `docs/trl4-sync-automation.md` — continuous local→TRL4 Gitea synchronization runbook.
- `tasks/` — backlog, sprint template, and weekly execution workspace.

## Development kickoff
Start project development in this order:
1. Read `README.md`, `WARP.md`, `AGENTS.md`, `SOUL.md`, and `CONTRIBUTING.md`.
2. Pick or define scope in `tasks/backlog.md`.
3. If the change affects architecture, create an ADR from `docs/adr/0000-adr-template.md`.
4. Execute work using the skill flow in `skills/registry.yaml`.
5. Validate with repository-native checks and update relevant docs.

## ProductionBase baseline bootstrap
Use `ProductionBase/BOOTSTRAP.md` to align each `ProductionBase/*` repository with the umbrella baseline (`AGENTS.md`, `SOUL.md`, `docs/adr/`, `tasks/`, `skills/`).

## Clone
Use recursive clone to pull all production repositories:

```bash
git clone --recurse-submodules http://127.0.0.1:3000/wera-global/WeRa-Global.git
```
