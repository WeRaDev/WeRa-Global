---
metadata:
  primary_domain: key-resources
  secondary_domains: [key-activities, cost-structure, solution]
  owner_role: Founder/Consultant
  temporal_scope: current
  evidence_status: verified
  last_reviewed_at: 2026-09-16
  next_review_due: 2026-12-15
  provenance:
    actor: agent-warp
    source: "HumanCenter/Resources/Documents/Research/HumanCenter.Pricing.md; HumanCenter/Resources/Documents/Research/Critical Review and Revised Chatbot ROI Interview Playbook.md"
    confidence: high
    review_status: draft
---
# Automation Center Key Resources

## Purpose
List the resources Product 3 ("Automation Center") depends on to deliver its build-and-operate automation service.

## Scope
- In scope: the discovery/ROI methodology asset, workflow-automation stack, and infrastructure Automation Center depends on.
- Out of scope: Shrinking AI's RCGFC/facilitation resources (`05-key-resources.md`).

## Current State
- **The discovery-and-ROI methodology itself** (role-routed interview design, evidence grading A-E, benefit classification, screening logic): the core proprietary asset, analogous in importance to Shrinking AI's RCGFC framework. Currently exists only as a designed methodology (this knowledgebase); not yet implemented as a working chatbot or tested with real prospects.
- **Workflow-automation stack**: n8n/Make/Zapier for workflow orchestration, LLM APIs for drafting/classification/extraction, OCR/document-extraction tooling for invoice/receipt/document automation.
- **Accounting/CRM/ERP integration capability**: connectors needed to deliver combined packages (e.g. accounting + email automation).
- **EU-hosted infrastructure / data residency** (firm requirement, not a candidate): required given the target audience includes clients with confidential financial/investor/deal information; consistent with `../../../../SOUL.md` and fund-oriented security-standard expectations (human approval, audit logs, DPA, no training on client data).
- **Knowledge asset**: the pricing-benchmark and discovery-methodology research library under `../../../../Resources/Documents/Research/`.
- **Founder/consultant delivery expertise**: process mapping, workflow design, and financial/compliance-aware discovery facilitation.

## Decisions / Rules
- The workflow-automation stack (n8n/Make/Zapier + LLM APIs) is a committed resource for Automation Center, unlike its "candidate, not yet committed" status under Shrinking AI.
- EU data residency, audit logging, and DPA infrastructure are mandatory (not optional) given the investment-fund-adjacent and financial-advisory sub-segments.
- The discovery methodology must be validated manually with real prospects before investing engineering effort in chatbot automation.

## Evidence
- `../../../../Resources/Documents/Research/HumanCenter.Pricing.md` — verified, defines the workflow-automation stack and named agency comparables.
- `../../../../Resources/Documents/Research/Critical Review and Revised Chatbot ROI Interview Playbook.md` — verified, defines the evidence-grading and benefit-classification methodology as a resource in its own right.

## Cross-Domain Links
- Related domains: `kb-key-activities`, `kb-cost-structure`, `kb-solution`
- Related documents: `../../../kb-key-activities/docs/execution/05-automation-center-key-activities.md`, `../../../kb-cost-structure/docs/model/08-cost-structure.md`, `../../../kb-solution/docs/strategy/03-automation-center-solution.md`

## Open Actions
- Select and commit to a specific n8n/Make/Zapier + LLM API + OCR toolchain, owner: Founder/Consultant.
- Stand up EU-hosted infrastructure and a DPA template before onboarding the first client, owner: Founder/Consultant.
- Build and test the discovery chatbot once the manual methodology is validated, owner: Founder/Consultant.
