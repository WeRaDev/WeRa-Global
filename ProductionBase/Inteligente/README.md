# Inteligente
Inteligente (`www.inteligente.site`) is a consultancy project of **Inteligente Razão — Unipessoal LDA** (Lisboa, Portugal). It runs two product lines, each with one or more named consultancy services:

- **Human Center**: human-facilitated AI-adoption services.
  - **Shrinking AI** (B2B, researched): a diagnostic service for SMEs, independent professionals, and AI-frustrated consultants/freelancers in Western Europe and the Nordics. Positioned as a "human interaction quality layer" between generic self-serve AI tools and slow/expensive enterprise strategy consulting. Delivery flow: free 15-minute empathy call -> paid structured session using the **RCGFC framework** (Role, Context, Goal, Format, Constraints) -> a 2-hour deliverable (AI-ready problem statement + instruction set) -> optional referral to Automation Center. Core value message: "we will help you get better results for the same money and keep your people happy."
  - **Empowering Human** (B2C/B2B, hypothesis-stage, not yet researched): discovery of the most suitable AI applications for business and personal use. Absorbs the intent of the earlier "Career Development" concept; kept strictly separate from Shrinking AI in navigation, tone, and calls-to-action.
- **Automation Center**: a build-and-implement automation service (n8n/Make/Zapier + LLM APIs) for back-office workflows, gated by a proprietary, evidence-graded discovery-and-ROI methodology (deliverable-first interview, evidence grading A-E, Stop/Measure/Prototype/Pilot screening decisions) rather than a generic sales quote. Its partner-led Financial Automation Discovery Pilot was formally initiated in Sept 2026; the first session and results are not yet confirmed. Broad target: any professional-services firm or solo consultant needing back-office automation.
  - **Financial Automation** (B2B, researched, first named service): workflow automation specialized for the financial industry (financial-advisory firms, investment-fund-adjacent solo consultants), documented pricing from market benchmarks. Additional Automation Center services may be added later for other industries.

Non-goals: open-ended "AI transformation" consulting, unsupervised financial/legal actions, unauthorized account automation, automated tax-return filing, or promising a guaranteed ROI from a discovery conversation alone.

## Quick start
This repository is currently docs/consultancy-stage: no product/automation code has landed yet.
```bash
cd "ProductionBase/Inteligente"
ls KnowledgeBase        # business-model-canvas-shaped knowledgebase
ls Resources/Documents/Research   # desk research, competitive analysis, and pricing benchmarks
```
When automation delivery code is introduced (e.g. for Financial Automation implementation engagements), it will land under a new `src/` (or `automations/`) directory, documented by an ADR in `docs/adr/`.

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
- **Shrinking AI's paid-session price is €50/60-min**, established from the first 2 real paid engagements (Sept 2026) — treat as an introductory rate pending elasticity testing; see `KnowledgeBase/kb-revenue-streams/docs/model/07-revenue-streams.md`.
- **The existing live Odoo chatbot on Frank still implements only generic livechat and lead-routing; it is not the governed Discovery Pilot.** The pilot is planned on Odoo Online, with the Financial partner as customer and the Operations partner as validator. It may use only aggregated metrics from the Financial partner’s own firm after written authorization and cloud/privacy review—no credentials, raw client records, or third-party confidential data. Odoo Online is cloud-hosted, not local-only. Odoo’s documented channel-rule behavior gives an AI Agent priority over a scripted chatbot when both are assigned, so escalation-only GPT-4o invocation, exact context sent, and transcript/provider retention must be verified before automated handoff; otherwise the founder triggers the analyst on one minimized question/answer at a time. The next stages are a local Odoo/local-model MVP on Frank after pilot validation, then the first paying customer’s dedicated account/agent on the SolarSeed TRL5 host after readiness/isolation checks. See `KnowledgeBase/kb-solution/docs/strategy/03-automation-center-solution.md` and `docs/adr/0001-financial-automation-discovery-pilot.md`.
- **Empowering Human has no commissioned research yet** — its current-state content is hypothesis-stage only.
- No lead-qualification gate or booking page exists yet for Shrinking AI, and no proof assets (target: 10+ completed sessions, 3 case write-ups, consent evidence pack) have been produced yet for any service.
- No signed client contracts exist yet for any service.
- Legal entity is confirmed (see above); the Portuguese commercial-registry/VAT number is confirmed as **PT514477580** — see `KnowledgeBase/kb-governance/docs/legal/11-legal-structure.md`.
- Human Center's services (Shrinking AI, Empowering Human) and Automation Center's services (Financial Automation) must remain strictly separated in all navigation, tone, and CTAs to avoid brand collision.
- Financial Automation's benchmark pricing is real market pricing, not yet client-tested; it must not be conflated with Shrinking AI's real but separately-priced €50/60-min session price.
- Any client automation touching financial/legal/consequential actions requires explicit human approval, audit logging, and EU data residency where applicable; Financial Automation clients with regulated or confidential data require the compliance/data-owner discovery route before any pilot.

## Contribution and ownership
- Product owner: Mike Ananyin.
- Delivery model: weekly sprint cadence; pull-request based review for all non-trivial changes, per umbrella `WARP.md`.
