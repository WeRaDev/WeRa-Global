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
- **Discovery chatbot platform and intended agent workspace: Odoo.** A live Odoo chatbot exists at `www.inteligente.site`, but **corrected assessment (Sept 2026, verified by inspecting the live agent configuration)**: it currently implements only generic livechat behavior and lead-routing/lead-creation logic (polite/concise responses, avoids fabrication, creates a lead when confidence is low or human follow-up is needed). It does **not** yet implement any of the governed-interview methodology from `../../../kb-solution/docs/strategy/03-automation-center-solution.md`: no opening disclosure of purpose/transcript use, no explicit consent request, no sensitive-data warning or interrupt/redaction behavior, no role-based (adviser/operations/compliance/finance) routing, no evidence grading, and no Stop/Measure/Prototype/Pilot completion logic. This corrects an earlier, overly optimistic entry in this document that described the bot as "partially configured with the role-routing/discovery questions" — that was not verified against the actual deployed configuration at the time. Per the founder's working note behind this build, Odoo's intended long-term role is broader than the chatbot alone: it is meant to become the **agent workspace** where automation agents hold user identities and bounded roles/permissions analogous to human Odoo users, and where clients connect through Odoo once they move from discovery to an active engagement — that long-term intent is unchanged, but the current build only covers generic lead capture, not the governed interview.
- **Hosting: two dedicated, already-owned servers — Frank and the SolarSeed machine** (both in Portugal/EU; combined connectivity cost €71.54/month, see `../../../kb-cost-structure/docs/model/08-cost-structure.md`). These two machines are designed to host business automation and can be deployed on-premises or in "farms" if a client wants a social/environmental-responsibility hosting option. Role split: **Frank** hosts Inteligente's own dedicated automation framework/platform (including the Odoo discovery chatbot above); the **SolarSeed machine** is earmarked to host the **first signed client's** automation instance, kept physically separate from the platform layer. As of Sept 2026, Frank has **no other active workload**, so there is currently no resource-contention risk from sharing it with other WeRa Global projects — but the Frank/SolarSeed split already gives good platform-vs-client-workload isolation by design for when that changes.
- **Workflow-automation stack (for the build-and-implement phase, distinct from the discovery-chatbot tool above)**: n8n/Make/Zapier for workflow orchestration, LLM APIs for drafting/classification/extraction, OCR/document-extraction tooling for invoice/receipt/document automation. Whether Odoo's own automation/workflow capabilities substitute for or complement this stack in client builds is not yet decided (see Open Actions).
- **Accounting/CRM/ERP integration capability**: connectors needed to deliver combined packages (e.g. accounting + email automation).
- **EU-hosted infrastructure / data residency** (firm requirement, not a candidate): required given the target audience includes Financial Automation clients with confidential financial/investor/deal information (see `../../../kb-value-proposition/docs/products/04-financial-automation.md`); consistent with `../../../../SOUL.md` and fund-oriented security-standard expectations (human approval, audit logs, DPA, no training on client data). The Frank/Odoo deployment is intended to satisfy this for the discovery-chatbot tool specifically; the SolarSeed machine is intended to satisfy it for the first client's automation instance.
- **Knowledge asset**: the pricing-benchmark and discovery-methodology research library under `../../../../Resources/Documents/Research/`, including the MVP workbook above.
- **Founder/consultant delivery expertise**: process mapping, workflow design, and financial/compliance-aware discovery facilitation.

## Decisions / Rules
- The workflow-automation stack (n8n/Make/Zapier + LLM APIs) is a committed resource for Automation Center's client-facing builds, unlike its "candidate, not yet committed" status under Human Center's Shrinking AI.
- EU data residency, audit logging, and DPA infrastructure are mandatory (not optional) given Financial Automation's investment-fund-adjacent and financial-advisory sub-segments (see `../../../kb-customers/docs/gtm/05-financial-automation-segments.md`).
- **Do not run a real, named-prospect discovery session through the Odoo chatbot until the governed-interview logic (disclosure, consent, sensitive-data interrupt, role routing, evidence grading, stop rules) is actually built and tested in it.** Until then, real sessions must be conducted manually by a human (see `../../../kb-solution/docs/strategy/03-automation-center-solution.md`), using the Odoo chatbot only for its current, verified capability: generic lead capture.
- Frank and the SolarSeed machine's role split (platform vs. first-client-instance) should be preserved going forward even as Frank's workload grows, to keep the isolation property intentional rather than incidental.
- Only add new infrastructure (a third machine, a paid hosting tier, new tooling) when a specific, evidenced requirement appears — per the resource-acquisition principle in `../../../kb-cost-structure/docs/model/08-cost-structure.md`.

## Evidence
- `../../../../Resources/Documents/Research/HumanCenter.Pricing.md` — unverified (self-described AI-chat estimate; see `../../../kb-revenue-streams/docs/model/07-revenue-streams.md`), defines the workflow-automation stack and named agency comparables.
- `../../../../Resources/Documents/Research/Critical Review and Revised Chatbot ROI Interview Playbook.md` — verified, defines the evidence-grading and benefit-classification methodology as a resource in its own right.
- `../../../../Resources/Documents/Research/financial_advisory_automation_mvp.xlsx` — verified, implementation-ready chatbot script, data model, ROI model, controls/scorecard, and phased build plan.
- `../../../../Resources/Documents/Research/inteligente.working.note..md` — verified as the founder's own working note; source of the agent-workspace/Odoo-as-delivery-platform concept and the deliverable-centered automation approach.
- **Live Odoo agent configuration inspection (Sept 2026)** — verified: the deployed system prompt at `www.inteligente.site` contains only generic livechat identity, response-style, and lead-creation instructions; no disclosure, consent, sensitive-data-interrupt, role-routing, evidence-grading, or stop-rule logic is present in the visible top-level prompt. This is the most reliable evidence in this document, since it is a direct inspection of the live system rather than a stated intent.
- **Founder-reported Frank/SolarSeed machine roles and cost (Sept 2026)** — verified: 2 dedicated servers, €71.54/month combined connectivity, Frank = platform host (no other current workload), SolarSeed machine = first-client-instance host.

## Cross-Domain Links
- Related domains: `kb-key-activities`, `kb-cost-structure`, `kb-solution`, `kb-channels`, `kb-governance`, `kb-key-partners`
- Related documents: `../../../kb-key-activities/docs/execution/05-automation-center-key-activities.md`, `../../../kb-cost-structure/docs/model/08-cost-structure.md`, `../../../kb-solution/docs/strategy/03-automation-center-solution.md`, `../../../kb-channels/docs/gtm/12-automation-center-channels.md`, `../../../kb-key-partners/docs/partnerships/06-key-partners.md`

## Open Actions
- Build the governed-interview logic (disclosure, consent, sensitive-data warning/interrupt, role-based routing for adviser/operations/compliance/optional-finance, evidence grading, Stop/Measure/Prototype/Pilot completion) into the Odoo agent, using the MVP workbook's script as the source — this is a real, non-trivial build task, not a configuration finishing touch, owner: Founder/Consultant.
- Until the above is built and tested, run real discovery sessions manually (human-led, per the MVP script) rather than through the chatbot; use the chatbot only for its current, verified lead-capture capability, owner: Founder/Consultant.
- Also inspect Odoo's Topics/Sources or any other injected prompt layer for logic not visible in the top-level agent prompt, to confirm the gap is real and not just hidden elsewhere, owner: Founder/Consultant.
- Confirm the intended Frank/SolarSeed data-isolation design (separate database/instance, access controls) is actually configured before the SolarSeed machine hosts its first real client instance, owner: Founder/Consultant.
- Decide whether Odoo's native automation/workflow tooling replaces or complements n8n/Make/Zapier for client-facing builds, owner: Founder/Consultant.
- Stand up a DPA template before the first real discovery session touches any prospect-identifying information (see `../../../kb-governance/docs/legal/11-legal-structure.md`), owner: Founder/Consultant.
