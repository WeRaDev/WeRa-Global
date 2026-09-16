---
metadata:
  primary_domain: governance
  secondary_domains: [value-proposition]
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

# Legal Structure

## Purpose
Record Human Center's legal-entity and compliance posture.

## Scope
- In scope: legal-entity identification and baseline compliance posture (DPA, data residency).
- Out of scope: full legal/tax structuring advice.

## Current State
- **Legal entity confirmed**: Human Center (`www.inteligente.site`) is a consultancy project of **Inteligente Razão — Unipessoal LDA** (HQ Lisboa, Portugal), stated directly in the Product 1 "Shrinking AI" research document's project description.
- Baseline compliance posture (candidate, not yet formalized): EU-hosted data storage, signed DPA per client, no client data used to train public models, audit logging for consequential actions — consistent with `../../../../SOUL.md` and comparable-vendor practice noted in pricing research.
- **Heightened considerations for Product 3 ("Automation Center")**: Automation Center's target audience is broader than Shrinking AI's and explicitly includes financial-advisory firms and investment-fund-adjacent solo consultants (see `../../../kb-customers/docs/gtm/04-automation-center-segments.md`). Existing sector-specific obligations (e.g. supervision, communications and recordkeeping duties in relevant US-regulated firms) can remain applicable to AI-assisted activity and must be established per client and jurisdiction, never assumed. The compliance/data-owner discovery route (see `../../../kb-solution/docs/strategy/03-automation-center-solution.md`) is the mechanism for this and must complete before any pilot proceeds for a regulated or confidential-data client.

## Decisions / Rules
- The entity name may now be used in external-facing material as confirmed; the registry/VAT number is still unconfirmed (see Open Actions) and must not be stated until verified.
- Any client engagement handling confidential/financial data requires a signed DPA before work begins.
- Automation Center engagements with financial-advisory or otherwise regulated clients require jurisdiction and regulatory-perimeter confirmation via the compliance/data-owner discovery route; findings must be recorded as confirmed, unresolved, or requiring specialist review — never treated as "compliant" merely because a respondent believes it is.

## Evidence
- `../../../../Resources/Documents/Research/Human Center — Product 1  Shrinking AI  Desk Research, Heuristic Evaluation &amp; Competitive Analysis.md` — verified, states the entity name directly in the project description.
- `../../../../Resources/Documents/Research/HumanCenter.Pricing.md` — verified, describes the compliance posture comparable vendors advertise (EU servers, GDPR, DPA, no training on client data), now Automation Center's own reference.
- `../../../../Resources/Documents/Research/Interview Playbook  Financial-Advisory Automation Discovery.md` — verified, evidences that existing financial-services obligations (supervision, communications, recordkeeping) can remain applicable to AI-assisted activity.

## Cross-Domain Links
- Related domains: `kb-value-proposition`, `kb-customers`, `kb-solution`
- Related documents: `../../../kb-value-proposition/docs/company/01-company-overview.md`, `../../../kb-customers/docs/gtm/04-automation-center-segments.md`, `../../../kb-solution/docs/strategy/03-automation-center-solution.md`

## Open Actions
- Confirm the Portuguese commercial-registry number / VAT (NIF) for Inteligente Razão — Unipessoal LDA and formalize a DPA template, owner: Founder/Consultant, due: see `../../../../tasks/backlog.md` HC-004.
- Before onboarding any financial-advisory or otherwise regulated Automation Center client, confirm the applicable regulatory perimeter and required controls with counsel or a qualified compliance reviewer, owner: Founder/Consultant.
