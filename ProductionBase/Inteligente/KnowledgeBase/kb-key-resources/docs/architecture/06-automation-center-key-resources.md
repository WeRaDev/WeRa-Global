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
    source: "Inteligente/Resources/Documents/Research/HumanCenter.Pricing.md; Inteligente/Resources/Documents/Research/Critical Review and Revised Chatbot ROI Interview Playbook.md"
    confidence: high
    review_status: draft
---
# Automation Center Key Resources

## Purpose
List the resources Automation Center depends on to deliver its build-and-operate automation service.

## Scope
- In scope: the discovery/ROI methodology asset, workflow-automation stack, and infrastructure Automation Center depends on.
- Out of scope: Human Center's RCGFC/facilitation resources for Shrinking AI (`05-key-resources.md`).

## Current State
- **The discovery-and-ROI methodology itself** (role-routed interview design, evidence grading A-E, benefit classification, screening logic): the core proprietary asset, analogous in importance to Shrinking AI's RCGFC framework. Fully specified down to an implementation-ready level in `../../../../Resources/Documents/Research/financial_advisory_automation_mvp.xlsx` (turn-by-turn chatbot script, logical data model, ROI formulas, controls/scorecard, and a phased implementation plan) — this workbook was not previously cited anywhere in the KB.
- **Discovery chatbot platform and intended agent workspace (Sept 2026, concrete, no longer hypothetical): Odoo.** A pilot chatbot project already exists, partially configured with the role-routing/discovery questions from the methodology above. Per the founder's working note behind this build, Odoo's intended role is broader than the discovery chatbot alone: it is meant to become the **agent workspace** where automation agents hold user identities and bounded roles/permissions analogous to human Odoo users, and where clients connect through Odoo (or a comparable business workspace) once they move from discovery to an active engagement. This makes the discovery-chatbot deployment a first step toward the delivery platform, not a standalone tool to be discarded after qualification.
- **Hosting: the TRL4 machine** (`wera-ss-pt-sn-1.tailfb390c.ts.net`), an existing, already-owned WeRa Global machine physically located in Portugal/EU. Deploying Odoo here satisfies the EU-hosted infrastructure requirement below at near-zero incremental infrastructure cost, since the hardware is already owned and used by other WeRa Global projects (SolarSeed). Target deployment: within days of Sept 2026.
- **Workflow-automation stack (for the build-and-implement phase, distinct from the discovery-chatbot tool above)**: n8n/Make/Zapier for workflow orchestration, LLM APIs for drafting/classification/extraction, OCR/document-extraction tooling for invoice/receipt/document automation. Whether Odoo's own automation/workflow capabilities substitute for or complement this stack in client builds is not yet decided (see Open Actions).
- **Accounting/CRM/ERP integration capability**: connectors needed to deliver combined packages (e.g. accounting + email automation).
- **EU-hosted infrastructure / data residency** (firm requirement, not a candidate): required given the target audience includes Financial Automation clients with confidential financial/investor/deal information (see `../../../kb-value-proposition/docs/products/04-financial-automation.md`); consistent with `../../../../SOUL.md` and fund-oriented security-standard expectations (human approval, audit logs, DPA, no training on client data). The TRL4/Odoo deployment is intended to satisfy this for the discovery-chatbot tool specifically.
- **Knowledge asset**: the pricing-benchmark and discovery-methodology research library under `../../../../Resources/Documents/Research/`, including the MVP workbook above.
- **Founder/consultant delivery expertise**: process mapping, workflow design, and financial/compliance-aware discovery facilitation.

## Decisions / Rules
- The workflow-automation stack (n8n/Make/Zapier + LLM APIs) is a committed resource for Automation Center's client-facing builds, unlike its "candidate, not yet committed" status under Human Center's Shrinking AI.
- EU data residency, audit logging, and DPA infrastructure are mandatory (not optional) given Financial Automation's investment-fund-adjacent and financial-advisory sub-segments (see `../../../kb-customers/docs/gtm/05-financial-automation-segments.md`).
- The discovery chatbot (Odoo/TRL4) must run founder-assisted, not public/unsupervised, for the first cohort — see `../../../kb-channels/docs/gtm/12-automation-center-channels.md`. "Already built" does not waive the safety/escalation validation requirement from the discovery methodology.
- Because the TRL4 machine is shared with other WeRa Global projects (notably SolarSeed), any client-identifying or sensitive data processed by the discovery chatbot must be isolated from other workloads on that machine (separate database/instance, access controls) — do not assume shared-tenancy is automatically safe merely because the machine is EU-located.

## Evidence
- `../../../../Resources/Documents/Research/HumanCenter.Pricing.md` — unverified (self-described AI-chat estimate; see `../../../kb-revenue-streams/docs/model/07-revenue-streams.md`), defines the workflow-automation stack and named agency comparables.
- `../../../../Resources/Documents/Research/Critical Review and Revised Chatbot ROI Interview Playbook.md` — verified, defines the evidence-grading and benefit-classification methodology as a resource in its own right.
- `../../../../Resources/Documents/Research/financial_advisory_automation_mvp.xlsx` — verified, implementation-ready chatbot script, data model, ROI model, controls/scorecard, and phased build plan.
- `../../../../Resources/Documents/Research/inteligente.working.note..md` — verified as the founder's own working note; source of the agent-workspace/Odoo-as-delivery-platform concept and the deliverable-centered automation approach.
- **Founder-reported Odoo pilot + TRL4 hosting decision (Sept 2026)** — verified as a stated intent and partial build; not yet verified as a working, deployed, or tested system.

## Cross-Domain Links
- Related domains: `kb-key-activities`, `kb-cost-structure`, `kb-solution`, `kb-channels`, `kb-governance`
- Related documents: `../../../kb-key-activities/docs/execution/05-automation-center-key-activities.md`, `../../../kb-cost-structure/docs/model/08-cost-structure.md`, `../../../kb-solution/docs/strategy/03-automation-center-solution.md`, `../../../kb-channels/docs/gtm/12-automation-center-channels.md`

## Open Actions
- Finish configuring the Odoo chatbot with the remaining discovery questions/routes (adviser, operations, compliance, optional finance) from the MVP workbook, and deploy it on the TRL4 machine, owner: Founder/Consultant, target: within days.
- Verify the TRL4/Odoo deployment isolates client data from other WeRa Global workloads on that machine before the first real session, owner: Founder/Consultant.
- Decide whether Odoo's native automation/workflow tooling replaces or complements n8n/Make/Zapier for client-facing builds, owner: Founder/Consultant.
- Stand up a DPA template before the first real discovery session touches any prospect-identifying information (see `../../../kb-governance/docs/legal/11-legal-structure.md`), owner: Founder/Consultant.
