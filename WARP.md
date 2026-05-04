# WeRa Global Master WARP Configuration

## Mission
WeRa Global exists to design and implement the Solar Network State as resilient infrastructure for natural and artificial intelligence.
This master `WARP.md` defines how we govern, build, document, and operate across the entire umbrella repository.

## Repository scope
This repository is the umbrella for:
- `KnowledgeBase/` (canonical business, architecture, legal, and strategy context)
- `ProductionBase/` (independent production repositories)

Out of canonical umbrella tracking:
- `_Archive/`
- `Customers/`
- `Old_documents/`

## Governance model
### Source of truth
- `KnowledgeBase/` is the canonical source for product intent, system vision, and business constraints.
- Implementation truth lives in each `ProductionBase/*` repository.
- If code and documentation conflict, fix both in the same delivery cycle.

### Project registration
- Every production repository must be listed in `ProductionBase/repos.yaml`.
- New projects are not considered active until they have baseline documentation and CI.

### Rule precedence
Rule resolution order:
1. Personal/global Warp rules
2. Umbrella `WARP.md` (this file)
3. Project-level `ProductionBase/<project>/WARP.md`
4. Subdirectory-level rules inside a project

The most specific rule has highest priority.

### Agent instruction standard (provider-agnostic)
- `AGENTS.md` is the canonical instruction file for coding agents.
- Each production repository must include `AGENTS.md` at repository root.
- `CLAUDE.md` is optional and should be a compatibility shim that points to `AGENTS.md` to avoid instruction drift.
- In monorepos, the nearest `AGENTS.md` to the edited path takes precedence.

### Soul constitution standard
- `SOUL.md` is the canonical consciousness/operational constitution layer for agent behavior.
- Umbrella canonical source: `SOUL.md`, derived from `ProductionBase/SolarSeed-v3/christ-soul.md`.
- Each new `ProductionBase/*` project must include a project-level `SOUL.md` that inherits umbrella principles and adds project-specific safety constraints.
- `AGENTS.md` and `WARP.md` in every project must remain consistent with `SOUL.md` and must not weaken its service, safety, and non-coercion principles.

### New project creation gate (umbrella)
A project is not considered initialized under WeRa Global until all baseline files exist and are internally consistent:
- `README.md`
- `WARP.md`
- `AGENTS.md`
- `SOUL.md`
- `CONTRIBUTING.md`
- `.gitea/workflows/`
- `docs/adr/`
- `tasks/`
- `skills/`

## Required baseline for every production repository
Each `ProductionBase/*` repository must include:
- `README.md`
- `WARP.md`
- `AGENTS.md`
- `SOUL.md`
- `CONTRIBUTING.md`
- `.gitea/workflows/`
- `docs/adr/` for architecture decisions
- `tasks/` for sprint-ready work items
- `skills/` for project-specific agent skills

## Documentation standard (Karpathy-inspired, adapted for WeRa)
### README contract
Every production repo `README.md` must include:
1. One-paragraph purpose and non-goals
2. Fastest successful quick start (copy-paste runnable)
3. Project structure map (what can be edited vs. stable zones)
4. Core workflows (build, test, lint, run)
5. Constraints and known limits
6. Contribution path and decision ownership

### Engineering docs
- Keep docs concise, executable, and close to code.
- Prefer small, explicit examples over broad theory.
- Use one decision per ADR file in `docs/adr/`.
- Track interface-level changes in changelogs or release notes.

## Agile operating framework
### Cadence
- Sprint length: 1 week
- Planning: define sprint goal + committed scope
- Mid-sprint review: risk and dependency check
- End-sprint review: demo, retro, and carry-over triage

### Work item lifecycle
`Backlog -> Ready -> In Progress -> Review -> Validated -> Done`

### Definition of Ready (DoR)
A task is Ready only if it has:
- Problem statement
- Scope and non-scope
- Acceptance criteria
- Dependencies identified
- Validation plan (tests/checks)

### Definition of Done (DoD)
A task is Done only if:
- Code is implemented and reviewed
- Tests pass for affected scope
- Lint/type checks pass
- Documentation is updated
- Rollback/operational risk is documented when relevant

## Agentic delivery framework
### Standard execution loop
1. Understand context from `KnowledgeBase/` and local project docs
2. Inspect current implementation and constraints
3. Plan before non-trivial changes
4. Implement in small, reviewable increments
5. Validate with tests and quality gates
6. Update docs and operational notes
7. Capture learnings for future iterations

### Change-size policy
- Small change: direct implementation with clear validation
- Medium/large change: explicit plan first, then implementation
- High-risk change: require ADR update and staged rollout strategy

### Branch and commit conventions
- Branch naming: `feat/<scope>-<slug>`, `fix/<scope>-<slug>`, `chore/<scope>-<slug>`
- Commit style: conventional commits (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`)
- Keep commits atomic and reversible
- Use Gitea pull requests for review and traceability

### Mandatory Gitea commitment identity (WARP-only)
- This policy applies to every Gitea commit, tag, push, and PR update.
- Use only the `WARP` Gitea account for repository commitments; never use personal identities.
- Before commit, set repo-local identity to WARP credentials:
  - `git config user.name "WARP"`
  - `git config user.email "<primary email of the WARP Gitea account>"`
- Before commit/push, verify all of the following:
  - `git config --get user.name` is exactly `WARP`
  - `git config --get user.email` matches the WARP Gitea account email
  - `git remote get-url origin` points to the canonical WeRa Global Gitea namespace (for example, `/wera-global/`)
- Use non-interactive token-based auth for all Gitea push/fetch operations. Load token from secure storage into an environment variable and pass auth via git HTTP header, never interactive prompts.
- If any identity/auth/remote check fails, stop and fix configuration before creating commits or pushing.

## Skill system for agent development
### Purpose
Skills turn repeated workflows into reusable, testable playbooks for both human and AI contributors.

### Skill storage
- Global umbrella skills: `skills/`
- Project skills: `ProductionBase/<project>/skills/`
- Optional skill registry: `skills/registry.yaml` (or project equivalent)

### Skill template
Every skill file must define:
- `name`
- `intent`
- `trigger_conditions`
- `required_inputs`
- `procedure`
- `validation`
- `expected_outputs`
- `failure_modes`
- `handoff_notes`

### Required core skills (minimum set)
1. `repo-orientation`: map structure, commands, and constraints
2. `task-intake`: convert requests into scoped deliverables
3. `implementation-plan`: produce safe execution plans for non-trivial work
4. `quality-gate`: run project tests, linters, and type checks
5. `release-readiness`: verify docs, migration notes, and operational impact
6. `retro-capture`: record outcomes, incidents, and improvements

## Quality and verification policy
- Never merge unvalidated changes.
- Prefer repository-native scripts for test/lint/typecheck.
- If no tests exist, add at least one verification path for changed behavior.
- Failures must be surfaced with exact command and error context.

## Security and reliability guardrails
- Do not commit secrets or sensitive customer data.
- Use least-privilege credentials and scoped tokens.
- Document migration and rollback paths for stateful changes.
- For infra-impacting changes, include pre-check and post-check commands.

## Cross-repository alignment
- Shared standards are defined here; implementation details belong in project `WARP.md` files.
- Project rules may extend this baseline but should not weaken quality or security requirements.
- Cross-project interfaces must be versioned and documented.

## Initialization status and next actions
### Foundation initialized at umbrella level
- `skills/`, `skills/registry.yaml`, and core skills are in place.
- `AGENTS.md` defines canonical provider-agnostic behavioral coding guardrails.
- `CLAUDE.md` is retained as compatibility shim.
- `CONTRIBUTING.md`, `docs/adr/`, and `tasks/` initialize development execution artifacts.

### Current priority actions
1. Apply baseline folders (`docs/adr/`, `tasks/`, `skills/`) across each `ProductionBase/*` repository.
2. Standardize all project `README.md` files to the README contract in this document.
3. Start weekly sprint execution from `tasks/backlog.md` and `tasks/sprint-template.md`.
4. Create project-level ADRs for major architecture and integration decisions.
