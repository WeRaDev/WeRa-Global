# Human Center
Human Center is an AI-automation consultancy (site: `www.inteligente.site`) that designs and delivers narrowly-scoped, high-trust AI-driven business-process automations for SMEs and independent professionals — for example email triage/drafting/follow-up, and document/receipt/bookkeeping handoff automation. Non-goals: open-ended "AI transformation" consulting, unsupervised financial/legal actions, unauthorized account automation, or automated tax-return filing.

## Quick start
This repository is currently docs/consultancy-stage: no product/automation code has landed yet.
```bash
cd "ProductionBase/HumanCenter"
ls KnowledgeBase        # business-model-canvas-shaped knowledgebase
ls Resources/Documents/Research   # desk research and pricing benchmarks
```
When automation delivery code is introduced, it will land under a new `src/` (or `automations/`) directory, documented by an ADR in `docs/adr/`.

## Project structure
- `KnowledgeBase/`: business-model-canvas-shaped knowledgebase (`kb-*` domain folders), mirroring the umbrella `KnowledgeBase/` structure.
- `Resources/Documents/Research/`: existing desk research, pricing benchmarks, and problem-framing analysis (canonical evidence source; not duplicated elsewhere).
- `docs/adr/`: architecture/business decision records.
- `tasks/`: sprint-ready work items.
- `skills/`: project-specific agent skills.
- `.gitea/workflows/`: CI pipelines (baseline + knowledgebase structure checks).
- `AGENTS.md` / `WARP.md` / `SOUL.md`: agent instructions, governance, and constitutional layer.

## Core workflows
- Baseline check (CI): verifies required files/folders exist (see `.gitea/workflows/ci.yml`).
- Knowledgebase structure check (CI): verifies every `KnowledgeBase/kb-*` folder has a `README.md`.
- Build/test/lint: not yet applicable (no code); this section will be updated once automation delivery code is added.

## Constraints and known limits
- No signed client contracts or validated cost model yet; pricing in `KnowledgeBase/kb-revenue-streams/` is market-benchmark-derived, not yet Human-Center-specific.
- Legal entity linkage (candidate: `INTELIGENTE RAZÃO - UNIPESSOAL LDA`) is unverified — see `KnowledgeBase/kb-governance/docs/legal/11-legal-structure.md`.
- Any client automation touching financial/legal/consequential actions requires explicit human approval, audit logging, and EU data residency where applicable.

## Contribution and ownership
- Product owner: Mike Ananyin.
- Delivery model: weekly sprint cadence; pull-request based review for all non-trivial changes, per umbrella `WARP.md`.
