---
metadata:
  primary_domain: value-proposition
  secondary_domains: [governance]
  owner_role: Founder/Consultant
  temporal_scope: current
  evidence_status: verified
  last_reviewed_at: 2026-09-15
  next_review_due: 2026-12-15
  provenance:
    actor: agent-warp
    source: "HumanCenter/Resources/Documents/Research/Human Center — Product 1  Shrinking AI  Desk Research, Heuristic Evaluation &amp; Competitive Analysis.md"
    confidence: high
    review_status: draft
---

# Company Overview

## Purpose
Establish the canonical company identity for Human Center.

## Scope
- In scope: brand, legal entity, website, product-line structure, ecosystem relationship.
- Out of scope: compliance/DPA posture (see `../../../kb-governance/docs/legal/11-legal-structure.md`).

## Current State
- Name: Human Center — a consultancy project of **Inteligente Razão — Unipessoal LDA**.
- Website: `www.inteligente.site`.
- Three distinct product lines exist and must be kept strictly separate in navigation, tone, and messaging (a named risk in the source research):
  1. **Product 1 — "Shrinking AI"** (B2B): a human-facilitated diagnostic service that converts "AI frustration" into a bounded, AI-ready problem statement via a paid RCGFC session. See `../products/02-services.md`.
  2. **Product 2 — "Career Development"** (B2C): a separate product line, not yet researched in this knowledgebase. Requires its own navigation/tone system, distinct from Products 1 and 3, per the site-architecture recommendation.
  3. **Product 3 — "Automation Center"** (B2B): a build-and-implement automation service (n8n/Make/Zapier + LLM APIs) for back-office workflows, gated by a proprietary chatbot-led, evidence-graded discovery-and-ROI methodology. Distinct standalone go-to-market from Shrinking AI, not merely its implementation follow-on. See `../products/03-automation-center.md`.
- Geography: Western Europe and the Nordics — targeting companies with budgets for AI and cultures of supporting employees with organisational tools. Automation Center's addressable market is broader than Shrinking AI's: any professional-services firm or solo consultant needing back-office automation, including clients in investment-fund-adjacent, more heavily regulated contexts (see `../../../kb-customers/docs/gtm/04-automation-center-segments.md`).
- Ecosystem: developed under `ProductionBase/HumanCenter/` within the WeRa Global umbrella repository (`native` vcs_mode, `enforced` baseline_policy per `ProductionBase/repos.yaml`).

## Decisions / Rules
- Products 1, 2, and 3 must not share primary navigation, tone, or CTA framing on the website — mixing B2B/B2C register and mixing a diagnostic-only service with a build-and-implement service were both flagged as "consistency and standards" risks.
- Automation Center may be represented externally as an AI-automation agency (n8n/Make/Zapier workflow builder) with documented, market-benchmark-derived pricing — this is now Product 3's own validated positioning (see `../../../kb-revenue-streams/docs/model/07-revenue-streams.md`), not to be confused with Shrinking AI's facilitation-only positioning.

## Evidence
- `../../../../Resources/Documents/Research/Human Center — Product 1  Shrinking AI  Desk Research, Heuristic Evaluation &amp; Competitive Analysis.md` — verified (states the entity name, product structure, and geography directly from project documentation relayed within the research brief).
- `../../../../Resources/Documents/Research/Shrinking AI (B2B Consultancy) — Desk Research, He.md` — verified, corroborating desk research for Product 1.
- `../../../../Resources/Documents/Research/HumanCenter.Pricing.md` — verified as Product 3 (Automation Center)'s own market-benchmark pricing research; no longer treated as an ambiguous/unrelated thread now that Automation Center exists as a named product.
- `../../../../Resources/Documents/Research/Interview Playbook  Financial-Advisory Automation Discovery.md`, `../../../../Resources/Documents/Research/Chatbot-Led Automation Discovery  Critique and Revised Interview Playbook.md`, `../../../../Resources/Documents/Research/Critical Review and Revised Chatbot ROI Interview Playbook.md` — verified, define Product 3's discovery-and-ROI methodology.

## Cross-Domain Links
- Related domains: `kb-governance`, `kb-solution`, `kb-problem`, `kb-customers`
- Related documents: `../products/02-services.md`, `../products/03-automation-center.md`, `../../../kb-governance/docs/legal/11-legal-structure.md`, `../../../kb-problem/docs/market/01-problem.md`

## Open Actions
- Research and document Product 2 ("Career Development") in this knowledgebase once material exists, owner: Founder/Consultant.
- Confirm the entity's official registry details (registration number, VAT) for compliance documentation, owner: Founder/Consultant, due: see `../../../../tasks/backlog.md` HC-004.
- Decide whether Products 1 and 3 are cross-sold to the same prospect (e.g. Shrinking AI session surfacing an Automation Center opportunity) or kept fully independent in sales motion, owner: Founder/Consultant.
