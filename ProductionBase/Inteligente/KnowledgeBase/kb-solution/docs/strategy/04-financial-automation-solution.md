---
metadata:
  primary_domain: solution
  secondary_domains: [problem, value-proposition, key-activities, unfair-advantage, governance]
  owner_role: Founder/Consultant
  temporal_scope: current
  evidence_status: verified
  last_reviewed_at: 2026-09-17
  next_review_due: 2026-12-15
  provenance:
    actor: agent-warp
    source: "Inteligente/Resources/Documents/Research/Interview Playbook  Financial-Advisory Automation Discovery.md; Inteligente/Resources/Documents/Research/Chatbot-Led Automation Discovery  Critique and Revised Interview Playbook.md; Inteligente/Resources/Documents/Research/Critical Review and Revised Chatbot ROI Interview Playbook.md"
    confidence: high
    review_status: draft
---
# Financial Automation Solution

## Purpose
Extend Automation Center's generic discovery-and-ROI methodology (`03-automation-center-solution.md`) with the compliance and regulatory handling specific to Financial Automation.

## Scope
- In scope: the mandatory compliance/data-owner discovery route, jurisdictional handling, and sector-obligation recording specific to financial-advisory and investment-fund-adjacent clients.
- Out of scope: the generic discovery methodology, evidence grading, and build delivery model, which apply line-wide and are documented in `03-automation-center-solution.md`; Human Center's services.

## Current State

### Compliance-aware by design
For Financial Automation clients, the compliance/data-owner route (one of Automation Center's three knowledge-owner roles, see `03-automation-center-solution.md`) is mandatory rather than optional. It establishes jurisdiction, permitted data, required approvals, and prohibited actions before any pilot proceeds. Existing sector obligations (e.g. supervision, communications and recordkeeping duties in relevant US-regulated firms) can remain applicable to AI-assisted activity; the chatbot/interviewer must record findings as confirmed, unresolved, or requiring specialist review — never "compliant" merely because a respondent believes it is.

### Applies to both evidenced client profiles
- The solo consultant/independent professional profile (confidential deal/investor information) requires human-approval, audit-logged, DPA-backed handling of any automation touching that data.
- The small financial-advisory/professional-services firm profile (with distinct adviser/owner, operational colleague, and compliance/data-owner functions) requires the compliance/data-owner role to be filled by an actual named person at the client, not inferred.

See `../../../kb-customers/docs/gtm/05-financial-automation-segments.md` for the full profile definitions.

## Decisions / Rules
- Every Financial Automation engagement must complete the compliance/data-owner discovery route before any pilot is proposed; this is a firm requirement, not case-by-case judgment.
- Findings from the compliance/data-owner route must be recorded as confirmed, unresolved, or requiring specialist review — never assumed compliant.
- Route legal/tax/investment-advice requests, credential exposure, suspected breaches, and disputed consent to human escalation immediately, per Automation Center's general escalation rule.

## Evidence
- `../../../../Resources/Documents/Research/Interview Playbook  Financial-Advisory Automation Discovery.md` — verified, original three-role discovery design including the compliance/data-owner role.
- `../../../../Resources/Documents/Research/Chatbot-Led Automation Discovery  Critique and Revised Interview Playbook.md` — verified, chatbot-safe conversational design and escalation triggers applicable to regulated engagements.
- `../../../../Resources/Documents/Research/Critical Review and Revised Chatbot ROI Interview Playbook.md` — verified, evidence grading and compliance-recording discipline.

## Cross-Domain Links
- Related domains: `kb-value-proposition`, `kb-customers`, `kb-governance`
- Related documents: `03-automation-center-solution.md`, `../../../kb-value-proposition/docs/products/04-financial-automation.md`, `../../../kb-customers/docs/gtm/05-financial-automation-segments.md`, `../../../kb-governance/docs/legal/11-legal-structure.md`

## Open Actions
- Confirm which specific regulatory regimes apply per target jurisdiction before the first Financial Automation pilot; per Sept 2026 decision, treat this generically (GDPR baseline) across Europe for now rather than researching country-specific advisory regulation upfront, owner: Founder/Consultant.
- Define the client-authorized secure channel for redacted artifact collection for regulated clients, owner: Founder/Consultant.
- Run the compliance/data-owner route in the founder-assisted Odoo/TRL4 discovery sessions with the named profile-2 prospects (see `../../../kb-customers/docs/gtm/05-financial-automation-segments.md`), owner: Founder/Consultant.
