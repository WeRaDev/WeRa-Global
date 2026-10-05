# Inteligente — Knowledgebase
Machine- and human-readable reference for the Inteligente consultancy, structured as a Business-Model-Canvas-shaped set of domain folders, mirroring the umbrella `WeRa Global/KnowledgeBase/` pattern.

## Quick reference
- Business: Inteligente
- Website: `www.inteligente.site`
- Legal entity: **Inteligente Razão — Unipessoal LDA** (Lisboa, Portugal) — verified (see `kb-governance/docs/legal/11-legal-structure.md`); VAT/NIF confirmed as **PT514477580**
- Product line: **Human Center** — human-facilitated consultancy services around AI adoption
  - Service — "Shrinking AI" (B2B, researched): human-facilitated AI-adoption sessions (free empathy call -> paid RCGFC session -> optional referral to Automation Center) for SMEs, independent professionals, and AI-frustrated consultants/freelancers in Western Europe and the Nordics
  - Service — "Expanding Human" (individuals and organizations, hypothesis-stage): explores where AI may support goals, problems, or ambitions; one founder-reported €50/60-minute paid observation, not a standard price or validated segment
- Product line: **Automation Center** (B2B, researched, standalone): build-and-implement automation service (n8n/Make/Zapier + LLM APIs) for back-office workflows, gated by a proprietary evidence-graded discovery-and-ROI methodology; broader target than Human Center's services (any professional-services firm/solo consultant); has its own documented, market-benchmark pricing
  - Product/use case — "Consultancy Automation": planned internal-first validation to automate Inteligente's own consultancy operations and measure efficiency/outcomes; workflow, baseline, and host not selected
  - Service — "Financial Automation": Automation Center's first named external service, specialising in workflow automation for the financial industry, including investment-fund-adjacent and financial-advisory clients
- Stage: internal Consultancy Automation validation must precede any external Financial Automation pilot. The partner-led pilot was formally initiated in Sept 2026 but is deferred, not cancelled, pending internal validation and passage of its existing safety, actionable-human-notification, privacy, data-flow, and authorization gates; no partner session or result is confirmed. The founder confirmed the authorized external-pilot database runs on Odoo Online. Its separate synthetic-only draft chatbot (bot 4) is archived/inactive after sensitive-input, advice, and guaranteed-ROI stop tests failed; do not use it live until the hard stops, data handling, and actionable human notification pass. The existing Human Center `/discovery-interview` route to Agent 5, with CRM Create/Get Lead tools available, is a separate unaudited route; reachability and side effects are pending review. Do not conflate it with the previously documented generic bot on Frank; the relationship between the site, Odoo Online database, and Frank remains unresolved. Region, provider/runtime, API-key mode, context, and retention remain unverified. The Odoo Online → Frank → SolarSeed sequence applies only to future external Financial Automation; no internal Consultancy Automation host is selected. Shrinking AI's paid-session price is documented at €50/60-min (from 2 real engagements, Sept 2026); Expanding Human has one separate paid observation, not a standard rate; no public proof assets are recorded; knowledgebase evidence includes desk research and founder-reported paid Human Center engagements (`../Resources/Documents/Research/`).

## Naming conventions
- Each Business-Model-Canvas / Lean-Canvas block is a top-level `kb-<domain>/` folder.
- Substantive documents live at `kb-<domain>/docs/<sub-area>/NN-title.md` and use `templates/KB-Domain-Document-Template-v1.md`.
- Thin domains with no dedicated document yet carry only a `kb-<domain>/README.md`.
- Claims must declare `evidence_status: verified|unverified|hypothesis` and cite a source (typically a file under `../Resources/Documents/Research/`).

## File index
| # | Domain | Canonical path | Scope |
|---|--------|----------------|----------------|
| 00 | Governance / glossary | `kb-governance/docs/standards/00-glossary.md` | All |
| 01 | Value proposition — company overview | `kb-value-proposition/docs/company/01-company-overview.md` | All |
| 02 | Value proposition — services | `kb-value-proposition/docs/products/02-services.md` | Human Center / Shrinking AI |
| 03 | Value proposition — Automation Center | `kb-value-proposition/docs/products/03-automation-center.md` | Automation Center (line-level) |
| 04 | Value proposition — Financial Automation | `kb-value-proposition/docs/products/04-financial-automation.md` | Automation Center / Financial Automation |
| 05 | Value proposition — Expanding Human | `kb-value-proposition/docs/products/05-expanding-human.md` | Human Center / Expanding Human (hypothesis) |
| 01 | Problem | `kb-problem/docs/market/01-problem.md` | Human Center / Shrinking AI |
| 02 | Solution | `kb-solution/docs/strategy/02-solution.md` | Human Center / Shrinking AI |
| 03 | Solution — Automation Center | `kb-solution/docs/strategy/03-automation-center-solution.md` | Automation Center (line-level) |
| 04 | Solution — Financial Automation | `kb-solution/docs/strategy/04-financial-automation-solution.md` | Automation Center / Financial Automation |
| 05 | Solution — Consultancy Automation methodology | `kb-solution/docs/strategy/05-consultancy-automation-methodology.md` | Automation Center / Consultancy Automation (hypothesis) |
| 03 | Customers | `kb-customers/docs/gtm/03-customer-segments.md` | Human Center / Shrinking AI |
| 04 | Customers — Automation Center | `kb-customers/docs/gtm/04-automation-center-segments.md` | Automation Center (line-level) |
| 05 | Customers — Financial Automation | `kb-customers/docs/gtm/05-financial-automation-segments.md` | Automation Center / Financial Automation |
| 06 | Customers — Expanding Human | `kb-customers/docs/gtm/06-expanding-human-segments.md` | Human Center / Expanding Human (hypothesis) |
| 04 | Key activities | `kb-key-activities/docs/execution/04-key-activities.md` | Human Center / Shrinking AI |
| 05 | Key activities — Automation Center | `kb-key-activities/docs/execution/05-automation-center-key-activities.md` | Automation Center |
| 05 | Key resources | `kb-key-resources/docs/architecture/05-key-resources.md` | Human Center / Shrinking AI |
| 06 | Key resources — Automation Center | `kb-key-resources/docs/architecture/06-automation-center-key-resources.md` | Automation Center |
| 06 | Key partners | `kb-key-partners/docs/partnerships/06-key-partners.md` | All |
| 07 | Revenue streams | `kb-revenue-streams/docs/model/07-revenue-streams.md` | All |
| 08 | Cost structure | `kb-cost-structure/docs/model/08-cost-structure.md` | Mainly Automation Center |
| 09 | Key metrics | `kb-metrics/docs/financial/09-key-metrics.md` | All |
| 10 | Unfair advantage | `kb-unfair-advantage/docs/strategy/10-unfair-advantage.md` | Human Center / Shrinking AI |
| 11 | Unfair advantage — Automation Center | `kb-unfair-advantage/docs/strategy/11-automation-center-unfair-advantage.md` | Automation Center |
| 11 | Channels | `kb-channels/docs/gtm/11-channels.md` | Human Center / Shrinking AI |
| 12 | Channels — Automation Center | `kb-channels/docs/gtm/12-automation-center-channels.md` | Automation Center |
| 11 | Legal structure | `kb-governance/docs/legal/11-legal-structure.md` | All |

Note: numbering is per-domain (matches the umbrella KB convention of grouping numbered docs by domain rather than one global sequence); a domain may carry multiple numbered documents when its content is product/service-specific.

## Domains
Each domain below spans one or more product lines/services; see the File index above for which document covers which scope.
- `kb-problem/` — the problem being solved (Human Center / Shrinking AI)
- `kb-solution/` — the solution approach (Human Center / Shrinking AI; Automation Center; Financial Automation)
- `kb-value-proposition/` — company overview and service packaging (all)
- `kb-customers/` — customer segments and go-to-market (Human Center / Shrinking AI; Automation Center; Financial Automation; Expanding Human)
- `kb-channels/` — distribution/acquisition channels (Human Center / Shrinking AI; Automation Center)
- `kb-key-activities/` — core delivery activities (Human Center / Shrinking AI; Automation Center)
- `kb-key-resources/` — tooling, infrastructure, expertise (Human Center / Shrinking AI; Automation Center)
- `kb-key-partners/` — partnership candidates (all)
- `kb-revenue-streams/` — pricing and revenue model (all)
- `kb-cost-structure/` — cost model (mainly Automation Center)
- `kb-metrics/` — key metrics (all)
- `kb-unfair-advantage/` — differentiation/moat (Human Center / Shrinking AI; Automation Center)
- `kb-governance/` — legal structure, glossary, standards (all)
