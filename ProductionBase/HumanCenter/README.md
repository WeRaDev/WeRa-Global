# Human Center
Human Center (`www.inteligente.site`) is a consultancy project of **Inteligente Razão — Unipessoal LDA** (Lisboa, Portugal). It runs three distinct, strictly-separated product lines:
- **Product 1 — "Shrinking AI" (B2B, researched)**: a human-facilitated AI-adoption diagnostic service for SMEs, independent professionals, and AI-frustrated consultants/freelancers in Western Europe and the Nordics. Positioned as a "human interaction quality layer" between generic self-serve AI tools and slow/expensive enterprise strategy consulting. Delivery flow: free 15-minute empathy call -> paid structured session using the **RCGFC framework** (Role, Context, Goal, Format, Constraints) -> a 2-hour deliverable (AI-ready problem statement + instruction set) -> optional referral to Automation Center. Core value message: "we will help you get better results for the same money and keep your people happy."
- **Product 2 — "Career Development" (B2C, not yet researched)**: kept strictly separate from Products 1 and 3 in navigation, tone, and calls-to-action to avoid brand collision.
- **Product 3 — "Automation Center" (B2B, researched, standalone)**: a build-and-implement automation service (n8n/Make/Zapier + LLM APIs) for back-office workflows (email, accounting/bookkeeping/document automation), for any professional-services firm or solo consultant, including investment-fund-adjacent and financial-advisory clients. Gated by a proprietary, evidence-graded discovery-and-ROI methodology (role-routed interview, evidence grading A-E, Stop/Measure/Prototype/Pilot screening decisions) rather than a generic sales quote. Has its own documented, market-benchmark-derived pricing (see `KnowledgeBase/kb-revenue-streams/docs/model/07-revenue-streams.md`).

Non-goals: open-ended "AI transformation" consulting, unsupervised financial/legal actions, unauthorized account automation, automated tax-return filing, or promising a guaranteed ROI from a discovery conversation alone.

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
- **Shrinking AI's paid-session price is undocumented anywhere** — the highest-priority pricing gap for Product 1; see `KnowledgeBase/kb-revenue-streams/docs/model/07-revenue-streams.md`.
- **Automation Center's discovery-and-ROI chatbot has not been built or tested** — the methodology is fully designed but currently must be run manually.
- No lead-qualification gate or booking page exists yet for Shrinking AI, and no proof assets (target: 10+ completed sessions, 3 case write-ups, consent evidence pack) have been produced yet for either product.
- No signed client contracts exist yet for any product.
- Legal entity is confirmed (see above); the Portuguese commercial-registry/VAT number is still unconfirmed — see `KnowledgeBase/kb-governance/docs/legal/11-legal-structure.md`.
- Products 1, 2, and 3 must remain strictly separated in all navigation, tone, and CTAs to avoid brand collision.
- Automation Center's benchmark pricing is real market pricing, not yet client-tested; it must not be conflated with Shrinking AI's still-undocumented session price.
- Any client automation touching financial/legal/consequential actions requires explicit human approval, audit logging, and EU data residency where applicable; Automation Center clients with regulated or confidential data require the compliance/data-owner discovery route before any pilot.

## Contribution and ownership
- Product owner: Mike Ananyin.
- Delivery model: weekly sprint cadence; pull-request based review for all non-trivial changes, per umbrella `WARP.md`.
