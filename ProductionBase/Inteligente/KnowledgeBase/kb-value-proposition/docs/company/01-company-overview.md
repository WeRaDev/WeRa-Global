---
metadata:
  primary_domain: value-proposition
  secondary_domains: [governance]
  owner_role: Founder/Consultant
  temporal_scope: current
  evidence_status: verified
  last_reviewed_at: 2026-09-17
  next_review_due: 2026-12-15
  provenance:
    actor: agent-warp
    source: "Inteligente/Resources/Documents/Research/Human Center — Product 1  Shrinking AI  Desk Research, Heuristic Evaluation &amp; Competitive Analysis.md"
    confidence: high
    review_status: draft
---

# Company Overview

## Purpose
Establish the canonical company identity for Inteligente and its product-line/service structure.

## Scope
- In scope: brand, legal entity, website, business/product-line/service structure, ecosystem relationship.
- Out of scope: compliance/DPA posture (see `../../../kb-governance/docs/legal/11-legal-structure.md`).

## Current State
- Name: **Inteligente** — the consultancy business operated by **Inteligente Razão — Unipessoal LDA**.
- Website: `www.inteligente.site`.
- Inteligente operates two product lines, each hosting one or more named services. Product lines and their services must be kept strictly separate in navigation, tone, and messaging (a named risk in the source research):
  1. **Human Center** — a consultancy product line offering human-facilitated services around AI adoption:
     - **Shrinking AI** (B2B): a human-facilitated diagnostic service that converts "AI frustration" into a bounded, AI-ready problem statement via a paid RCGFC session. See `../products/02-services.md`.
     - **Empowering Human** (B2C, hypothesis-stage): a discovery service to identify the most suitable AI applications for business and personal use. See `../products/05-empowering-human.md`.
  2. **Automation Center** — a build-and-implement automation product line (n8n/Make/Zapier + LLM APIs) for back-office workflows, gated by a proprietary chatbot-led, evidence-graded discovery-and-ROI methodology, addressable to any professional-services firm or solo consultant. See `../products/03-automation-center.md`.
     - **Financial Automation**: Automation Center's first named service, specialising in workflow automation for the financial industry, including investment-fund-adjacent and other more heavily regulated contexts. See `../products/04-financial-automation.md`.
- Geography: Western Europe and the Nordics — targeting companies with budgets for AI and cultures of supporting employees with organisational tools. Automation Center's addressable market is broader than Human Center's Shrinking AI service (see `../../../kb-customers/docs/gtm/04-automation-center-segments.md` and `../../../kb-customers/docs/gtm/05-financial-automation-segments.md`).
- Ecosystem: developed under `ProductionBase/Inteligente/` within the WeRa Global umbrella repository (`native` vcs_mode, `enforced` baseline_policy per `ProductionBase/repos.yaml`).

## Decisions / Rules
- Human Center and Automation Center, and the services within each, must not share primary navigation, tone, or CTA framing on the website — mixing B2B/B2C register and mixing a diagnostic-only service with a build-and-implement service were both flagged as "consistency and standards" risks.
- Automation Center may be represented externally as an AI-automation agency (n8n/Make/Zapier workflow builder) with documented, market-benchmark-derived pricing — this is its own validated positioning (see `../../../kb-revenue-streams/docs/model/07-revenue-streams.md`), not to be confused with Human Center's facilitation-only positioning.
- Empowering Human is hypothesis-stage: it folds in the earlier, unresearched "Career Development" B2C concept and must be labeled `evidence_status: hypothesis` until validated.

## Evidence
- `../../../../Resources/Documents/Research/Human Center — Product 1  Shrinking AI  Desk Research, Heuristic Evaluation &amp; Competitive Analysis.md` — verified (states the entity name, product structure, and geography directly from project documentation relayed within the research brief).
- `../../../../Resources/Documents/Research/Shrinking AI (B2B Consultancy) — Desk Research, He.md` — verified, corroborating desk research for Shrinking AI.
- `../../../../Resources/Documents/Research/HumanCenter.Pricing.md` — verified as Automation Center's own market-benchmark pricing research.
- `../../../../Resources/Documents/Research/Interview Playbook  Financial-Advisory Automation Discovery.md`, `../../../../Resources/Documents/Research/Chatbot-Led Automation Discovery  Critique and Revised Interview Playbook.md`, `../../../../Resources/Documents/Research/Critical Review and Revised Chatbot ROI Interview Playbook.md` — verified, define Automation Center's discovery-and-ROI methodology and Financial Automation's regulated-industry framing.

## Cross-Domain Links
- Related domains: `kb-governance`, `kb-solution`, `kb-problem`, `kb-customers`
- Related documents: `../products/02-services.md`, `../products/03-automation-center.md`, `../products/04-financial-automation.md`, `../products/05-empowering-human.md`, `../../../kb-governance/docs/legal/11-legal-structure.md`, `../../../kb-problem/docs/market/01-problem.md`

## Open Actions
- Research and validate Empowering Human's target segments and pricing once material exists, owner: Founder/Consultant.
- Confirm the entity's official registry details (registration number, VAT) for compliance documentation, owner: Founder/Consultant, due: see `../../../../tasks/backlog.md` HC-004.
- Decide whether Human Center services and Automation Center/Financial Automation are cross-sold to the same prospect (e.g. Shrinking AI session surfacing an Automation Center opportunity) or kept fully independent in sales motion, owner: Founder/Consultant.
