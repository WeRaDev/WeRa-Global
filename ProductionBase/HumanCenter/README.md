# Human Center
Human Center (`www.inteligente.site`) is a consultancy project of **Inteligente Razão — Unipessoal LDA** (Lisboa, Portugal). It runs two distinct, strictly-separated product lines:
- **Product 1 — "Shrinking AI" (B2B, primary, researched)**: a human-facilitated AI-adoption service for SMEs, independent professionals, and AI-frustrated consultants/freelancers in Western Europe and the Nordics. Positioned as a "human interaction quality layer" between generic self-serve AI tools and slow/expensive enterprise strategy consulting. Delivery flow: free 15-minute empathy call -> paid structured session using the **RCGFC framework** (Role, Context, Goal, Format, Constraints) -> a 2-hour deliverable (AI-ready problem statement + instruction set) -> optional retainer/implementation support. Core value message: "we will help you get better results for the same money and keep your people happy."
- **Product 2 — "Career Development" (B2C, not yet researched)**: kept strictly separate from Product 1 in navigation, tone, and calls-to-action to avoid brand collision.

Non-goals: open-ended "AI transformation" consulting, unsupervised financial/legal actions, unauthorized account automation, or automated tax-return filing.

## Quick start
This repository is currently docs/consultancy-stage: no product/automation code has landed yet.
```bash
cd "ProductionBase/HumanCenter"
ls KnowledgeBase        # business-model-canvas-shaped knowledgebase
ls Resources/Documents/Research   # desk research, competitive analysis, and pricing benchmarks
```
When automation delivery code is introduced (e.g. for optional implementation-support engagements), it will land under a new `src/` (or `automations/`) directory, documented by an ADR in `docs/adr/`.

## Project structure
- `KnowledgeBase/`: business-model-canvas-shaped knowledgebase (`kb-*` domain folders), mirroring the umbrella `KnowledgeBase/` structure.
- `Resources/Documents/Research/`: existing desk research, competitive analysis, and pricing benchmarks (canonical evidence source; not duplicated elsewhere).
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
- **Shrinking AI's paid-session price is undocumented anywhere** — the highest-priority pricing gap; see `KnowledgeBase/kb-revenue-streams/docs/model/07-revenue-streams.md`.
- No lead-qualification gate or booking page exists yet, and no proof assets (target: 10+ completed sessions, 3 case write-ups, consent evidence pack) have been produced yet.
- No signed client contracts exist yet.
- Legal entity is confirmed (see above); the Portuguese commercial-registry/VAT number is still unconfirmed — see `KnowledgeBase/kb-governance/docs/legal/11-legal-structure.md`.
- Product 1 and Product 2 must remain strictly separated in all navigation, tone, and CTAs to avoid brand collision.
- Any client automation touching financial/legal/consequential actions requires explicit human approval, audit logging, and EU data residency where applicable.

## Contribution and ownership
- Product owner: Mike Ananyin.
- Delivery model: weekly sprint cadence; pull-request based review for all non-trivial changes, per umbrella `WARP.md`.
