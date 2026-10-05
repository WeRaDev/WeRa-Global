# Inteligente
Inteligente (`www.inteligente.site`) is a consultancy project of **Inteligente Razão — Unipessoal LDA** (Lisboa, Portugal). It runs two product lines, each with one or more named consultancy services:

- **Human Center**: human-facilitated AI-adoption services.
  - **Shrinking AI** (B2B, researched): a diagnostic service for SMEs, independent professionals, and AI-frustrated consultants/freelancers in Western Europe and the Nordics. Positioned as a "human interaction quality layer" between generic self-serve AI tools and slow/expensive enterprise strategy consulting. Delivery flow: free 15-minute empathy call -> paid structured session using the **RCGFC framework** (Role, Context, Goal, Format, Constraints) -> a 2-hour deliverable (AI-ready problem statement + instruction set) -> optional referral to Automation Center. Core value message: "we will help you get better results for the same money and keep your people happy."
  - **Expanding Human** (individuals and organizations, hypothesis-stage): explores where AI may support a person's or organization's goals, problems, or ambitions. One founder-reported €50/60-minute paid observation is recorded; it does not establish a standard price, validated audience, or repeatable method. The earlier "Career Development" concept is not a separate service.
- **Automation Center**: a build-and-implement automation service (n8n/Make/Zapier + LLM APIs) for back-office workflows, gated by a proprietary, evidence-graded discovery-and-ROI methodology (deliverable-first interview, evidence grading A-E, Stop/Measure/Prototype/Pilot screening decisions) rather than a generic sales quote. **Consultancy Automation** is the planned internal-first use case to automate Inteligente's own consultancy operations and measure efficiency/outcomes; workflow, baseline, and hosting are not yet selected. The partner-led Financial Automation Discovery Pilot was formally initiated in Sept 2026 but is deferred, not cancelled, until internal validation and all existing safety/data-flow gates pass; no first session or result is confirmed. Broad target: any professional-services firm or solo consultant needing back-office automation.
  - **Financial Automation** (B2B, researched, first named external service): workflow automation specialized for the financial industry (financial-advisory firms, investment-fund-adjacent solo consultants), documented pricing from market benchmarks. Additional Automation Center services may be added later for other industries.

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
- **Financial Automation Discovery Pilot status:** The external partner pilot was formally initiated but is deferred, not cancelled, until Consultancy Automation is validated and the existing safety, actionable-human-notification, privacy, and data-flow gates pass. No partner session or result is confirmed. The founder confirmed that the authorized external-pilot database runs on Odoo Online. A separate draft chatbot (bot 4) was configured and synthetically tested, then archived/inactivated after sensitive-input, legal/tax/investment-advice, and guaranteed-ROI stop tests failed; keep it out of live use until the hard stops, data handling, and actionable human notification are verified. The handoff separately records an always-enabled Human Center `/discovery-interview` route assigned to Agent 5, with CRM Create/Get Lead tools available; public reachability, runtime behavior, and CRM side effects are unaudited. Do not conflate that route or archived bot 4 with the generic chatbot previously documented as hosted on Frank; the relationship between the public site, Odoo Online database, and Frank remains unresolved. Region, provider/runtime, API-key mode, context, and retention are not established by the hosting confirmation. The Odoo Online → Frank → SolarSeed sequence applies only to the future external path; no host is selected for Consultancy Automation. See `KnowledgeBase/kb-solution/docs/strategy/03-automation-center-solution.md`, `docs/adr/0001-financial-automation-discovery-pilot.md`, `docs/adr/0002-consultancy-automation-internal-first.md`, and task handoffs in `tasks/`.
- **Expanding Human has no commissioned research or validated audience/method yet.** One €50/60-minute paid follow-up is recorded as a founder-reported observation, not a standard offer or validated market signal.
- No lead-qualification gate or booking page exists yet for Shrinking AI, and no proof assets (target: 10+ completed sessions, 3 case write-ups, consent evidence pack) have been produced yet for any service.
- No signed Automation Center client engagement has been reported. Human Center has two initial paid Shrinking AI sessions and one separate paid Expanding Human follow-up, with no validated repeatable delivery or measured downstream business impact.
- Legal entity is confirmed (see above); the Portuguese commercial-registry/VAT number is confirmed as **PT514477580** — see `KnowledgeBase/kb-governance/docs/legal/11-legal-structure.md`.
- Keep Human Center and Automation Center distinct in primary navigation, tone, and CTAs; refer clients between them by need in either direction without treating the referral strategy as conversion evidence.
- Financial Automation's benchmark pricing is real market pricing, not yet client-tested; it must not be conflated with Shrinking AI's real but separately-priced €50/60-min session price.
- Any client automation touching financial/legal/consequential actions requires explicit human approval, audit logging, and EU data residency where applicable; Financial Automation clients with regulated or confidential data require the compliance/data-owner discovery route before any pilot.

## Contribution and ownership
- Product owner: Mike Ananyin.
- Delivery model: weekly sprint cadence; pull-request based review for all non-trivial changes, per umbrella `WARP.md`.
