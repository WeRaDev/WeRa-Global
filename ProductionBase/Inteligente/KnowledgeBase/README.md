# Inteligente — Knowledgebase
Machine- and human-readable reference for the Inteligente consultancy, structured as a Business-Model-Canvas-shaped set of domain folders, mirroring the umbrella `WeRa Global/KnowledgeBase/` pattern.

## Quick reference
- Business: Inteligente
- Website: `www.inteligente.site`
- Legal entity: **Inteligente Razão — Unipessoal LDA** (Lisboa, Portugal) — verified (see `kb-governance/docs/legal/11-legal-structure.md`); VAT/NIF confirmed as **PT514477580**
- Product line: **Human Center** — human-facilitated consultancy services around AI adoption
  - Service — "Shrinking AI" (B2B, researched): human-facilitated AI-adoption sessions (free empathy call -> paid RCGFC session -> optional referral to Automation Center) for SMEs, independent professionals, and AI-frustrated consultants/freelancers in Western Europe and the Nordics
  - Service — "Empowering Human" (B2C, hypothesis-stage): discovery of the most suitable AI applications for business and personal use; folds in the earlier, unresearched "Career Development" concept
- Product line: **Automation Center** (B2B, researched, standalone): build-and-implement automation service (n8n/Make/Zapier + LLM APIs) for back-office workflows, gated by a proprietary evidence-graded discovery-and-ROI methodology; broader target than Human Center's services (any professional-services firm/solo consultant); has its own documented, market-benchmark pricing
  - Service — "Financial Automation": Automation Center's first named service, specialising in workflow automation for the financial industry, including investment-fund-adjacent and financial-advisory clients
- Stage: the partner-led Financial Automation Discovery Pilot was formally initiated in Sept 2026; the first session and results are not yet confirmed. Stage 1 is Odoo Online (cloud-hosted, not local-only), with the Financial partner acting as customer using authorized aggregated metrics from their own firm and the Operations partner validating the method. The existing live Odoo chatbot on Frank remains generic lead capture and is not this pilot. Verify Odoo’s scripted-chatbot/AI-agent handoff and data handling before enabling automatic escalation; until then, the founder triggers the analyst manually on minimized single-question/answer context. After pilot validation, stage 2 is a local Odoo/local-model MVP on Frank (TRL4); stage 3 is deployment of the first paying customer’s account/agent on the SolarSeed TRL5 host after readiness and isolation checks. Shrinking AI's paid-session price is documented at €50/60-min (from 2 real engagements, Sept 2026); Empowering Human has no research yet; no proof assets produced for any service; knowledgebase largely validated from desk research (`../Resources/Documents/Research/`), not yet from paying client engagements

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
| 05 | Value proposition — Empowering Human | `kb-value-proposition/docs/products/05-empowering-human.md` | Human Center / Empowering Human (hypothesis) |
| 01 | Problem | `kb-problem/docs/market/01-problem.md` | Human Center / Shrinking AI |
| 02 | Solution | `kb-solution/docs/strategy/02-solution.md` | Human Center / Shrinking AI |
| 03 | Solution — Automation Center | `kb-solution/docs/strategy/03-automation-center-solution.md` | Automation Center (line-level) |
| 04 | Solution — Financial Automation | `kb-solution/docs/strategy/04-financial-automation-solution.md` | Automation Center / Financial Automation |
| 03 | Customers | `kb-customers/docs/gtm/03-customer-segments.md` | Human Center / Shrinking AI |
| 04 | Customers — Automation Center | `kb-customers/docs/gtm/04-automation-center-segments.md` | Automation Center (line-level) |
| 05 | Customers — Financial Automation | `kb-customers/docs/gtm/05-financial-automation-segments.md` | Automation Center / Financial Automation |
| 06 | Customers — Empowering Human | `kb-customers/docs/gtm/06-empowering-human-segments.md` | Human Center / Empowering Human (hypothesis) |
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
- `kb-customers/` — customer segments and go-to-market (Human Center / Shrinking AI; Automation Center; Financial Automation; Empowering Human)
- `kb-channels/` — distribution/acquisition channels (Human Center / Shrinking AI; Automation Center)
- `kb-key-activities/` — core delivery activities (Human Center / Shrinking AI; Automation Center)
- `kb-key-resources/` — tooling, infrastructure, expertise (Human Center / Shrinking AI; Automation Center)
- `kb-key-partners/` — partnership candidates (all)
- `kb-revenue-streams/` — pricing and revenue model (all)
- `kb-cost-structure/` — cost model (mainly Automation Center)
- `kb-metrics/` — key metrics (all)
- `kb-unfair-advantage/` — differentiation/moat (Human Center / Shrinking AI; Automation Center)
- `kb-governance/` — legal structure, glossary, standards (all)
