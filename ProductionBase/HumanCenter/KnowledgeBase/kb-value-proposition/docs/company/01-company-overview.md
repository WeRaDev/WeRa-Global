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
- Two distinct product lines exist and must be kept strictly separate in navigation, tone, and messaging (a named risk in the source research):
  1. **Product 1 — "Shrinking AI"** (B2B): a human-facilitated service that converts "AI frustration" into bounded, actionable workflows. This is the primary, actively-researched product; see `../products/02-services.md`.
  2. **Product 2 — "Career Development"** (B2C): a separate product line, not yet researched in this knowledgebase. Requires its own navigation/tone system, distinct from Product 1, per the site-architecture recommendation.
- Geography: Western Europe and the Nordics — targeting companies with budgets for AI and cultures of supporting employees with organisational tools.
- Ecosystem: developed under `ProductionBase/HumanCenter/` within the WeRa Global umbrella repository (`native` vcs_mode, `enforced` baseline_policy per `ProductionBase/repos.yaml`).

## Decisions / Rules
- Product 1 (Shrinking AI) and Product 2 (Career Development) must not share primary navigation, tone, or CTA framing on the website — mixing B2B and B2C register was flagged as a heuristic "consistency and standards" risk.
- Do not represent Human Center as a generic "AI-automation agency" (n8n/Make workflow builder) externally — that framing belongs to a separate, less-validated pricing-research thread (see `../../../kb-revenue-streams/docs/model/07-revenue-streams.md`), not to the validated Shrinking AI product concept.

## Evidence
- `../../../../Resources/Documents/Research/Human Center — Product 1  Shrinking AI  Desk Research, Heuristic Evaluation &amp; Competitive Analysis.md` — verified (states the entity name, product structure, and geography directly from project documentation relayed within the research brief).
- `../../../../Resources/Documents/Research/Shrinking AI (B2B Consultancy) — Desk Research, He.md` — verified, corroborating desk research for Product 1.

## Cross-Domain Links
- Related domains: `kb-governance`, `kb-solution`, `kb-problem`, `kb-customers`
- Related documents: `../products/02-services.md`, `../../../kb-governance/docs/legal/11-legal-structure.md`, `../../../kb-problem/docs/market/01-problem.md`

## Open Actions
- Research and document Product 2 ("Career Development") in this knowledgebase once material exists, owner: Founder/Consultant.
- Confirm the entity's official registry details (registration number, VAT) for compliance documentation, owner: Founder/Consultant, due: see `../../../../tasks/backlog.md` HC-004.
