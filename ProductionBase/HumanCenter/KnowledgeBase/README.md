# Human Center — Knowledgebase
Machine- and human-readable reference for the Human Center consultancy, structured as a Business-Model-Canvas-shaped set of domain folders, mirroring the umbrella `WeRa Global/KnowledgeBase/` pattern.

## Quick reference
- Name: Human Center
- Website: `www.inteligente.site`
- Legal entity: **Inteligente Razão — Unipessoal LDA** (Lisboa, Portugal) — verified (see `kb-governance/docs/legal/11-legal-structure.md`); commercial-registry/VAT number still unconfirmed
- Product 1 — "Shrinking AI" (B2B, researched): human-facilitated AI-adoption sessions (free empathy call -> paid RCGFC session -> optional referral to Automation Center) for SMEs, independent professionals, and AI-frustrated consultants/freelancers in Western Europe and the Nordics
- Product 2 — "Career Development" (B2C, not yet researched): kept strictly separate from Products 1 and 3 in nav/tone/CTAs
- Product 3 — "Automation Center" (B2B, researched, standalone): build-and-implement automation service (n8n/Make/Zapier + LLM APIs) for back-office workflows, gated by a proprietary evidence-graded discovery-and-ROI methodology; broader target than Shrinking AI (any professional-services firm/solo consultant, including investment-fund-adjacent and financial-advisory clients); has its own documented, market-benchmark pricing
- Stage: pre-pilot for all products; Shrinking AI's paid-session price is undocumented anywhere (highest-priority gap for Product 1); Automation Center's discovery chatbot is designed but not yet built/tested; no proof assets produced yet; knowledgebase largely validated from desk research (`../Resources/Documents/Research/`), not yet from real client engagements

## Naming conventions
- Each Business-Model-Canvas / Lean-Canvas block is a top-level `kb-<domain>/` folder.
- Substantive documents live at `kb-<domain>/docs/<sub-area>/NN-title.md` and use `templates/KB-Domain-Document-Template-v1.md`.
- Thin domains with no dedicated document yet carry only a `kb-<domain>/README.md`.
- Claims must declare `evidence_status: verified|unverified|hypothesis` and cite a source (typically a file under `../Resources/Documents/Research/`).

## File index
| # | Domain | Canonical path | Product scope |
|---|--------|----------------|----------------|
| 00 | Governance / glossary | `kb-governance/docs/standards/00-glossary.md` | All |
| 01 | Value proposition — company overview | `kb-value-proposition/docs/company/01-company-overview.md` | All |
| 02 | Value proposition — services | `kb-value-proposition/docs/products/02-services.md` | Product 1 |
| 03 | Value proposition — Automation Center | `kb-value-proposition/docs/products/03-automation-center.md` | Product 3 |
| 01 | Problem | `kb-problem/docs/market/01-problem.md` | Product 1 |
| 02 | Solution | `kb-solution/docs/strategy/02-solution.md` | Product 1 |
| 03 | Solution — Automation Center | `kb-solution/docs/strategy/03-automation-center-solution.md` | Product 3 |
| 03 | Customers | `kb-customers/docs/gtm/03-customer-segments.md` | Product 1 |
| 04 | Customers — Automation Center | `kb-customers/docs/gtm/04-automation-center-segments.md` | Product 3 |
| 04 | Key activities | `kb-key-activities/docs/execution/04-key-activities.md` | Product 1 |
| 05 | Key activities — Automation Center | `kb-key-activities/docs/execution/05-automation-center-key-activities.md` | Product 3 |
| 05 | Key resources | `kb-key-resources/docs/architecture/05-key-resources.md` | Product 1 |
| 06 | Key resources — Automation Center | `kb-key-resources/docs/architecture/06-automation-center-key-resources.md` | Product 3 |
| 06 | Key partners | `kb-key-partners/docs/partnerships/06-key-partners.md` | All |
| 07 | Revenue streams | `kb-revenue-streams/docs/model/07-revenue-streams.md` | All |
| 08 | Cost structure | `kb-cost-structure/docs/model/08-cost-structure.md` | Mainly Product 3 |
| 09 | Key metrics | `kb-metrics/docs/financial/09-key-metrics.md` | All |
| 10 | Unfair advantage | `kb-unfair-advantage/docs/strategy/10-unfair-advantage.md` | Product 1 |
| 11 | Unfair advantage — Automation Center | `kb-unfair-advantage/docs/strategy/11-automation-center-unfair-advantage.md` | Product 3 |
| 11 | Channels | `kb-channels/docs/gtm/11-channels.md` | Product 1 |
| 12 | Channels — Automation Center | `kb-channels/docs/gtm/12-automation-center-channels.md` | Product 3 |
| 11 | Legal structure | `kb-governance/docs/legal/11-legal-structure.md` | All |

Note: numbering is per-domain (matches the umbrella KB convention of grouping numbered docs by domain rather than one global sequence); a domain may carry multiple numbered documents when its content is product-specific.

## Domains
Each domain below spans one or more products; see the File index above for which document covers which product.
- `kb-problem/` — the problem being solved (Product 1)
- `kb-solution/` — the solution approach (Products 1 and 3)
- `kb-value-proposition/` — company overview and service packaging (all products)
- `kb-customers/` — customer segments and go-to-market (Products 1 and 3)
- `kb-channels/` — distribution/acquisition channels (Products 1 and 3)
- `kb-key-activities/` — core delivery activities (Products 1 and 3)
- `kb-key-resources/` — tooling, infrastructure, expertise (Products 1 and 3)
- `kb-key-partners/` — partnership candidates (all products)
- `kb-revenue-streams/` — pricing and revenue model (all products)
- `kb-cost-structure/` — cost model (mainly Product 3)
- `kb-metrics/` — key metrics (all products)
- `kb-unfair-advantage/` — differentiation/moat (Products 1 and 3)
- `kb-governance/` — legal structure, glossary, standards (all products)
