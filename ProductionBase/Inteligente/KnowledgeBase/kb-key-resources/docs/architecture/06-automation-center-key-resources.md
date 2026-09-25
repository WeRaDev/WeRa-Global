---
metadata:
  primary_domain: key-resources
  secondary_domains: [key-activities, cost-structure, solution]
  owner_role: Founder/Consultant
  temporal_scope: current
  evidence_status: verified
  last_reviewed_at: 2026-09-25
  next_review_due: 2026-12-25
  provenance:
    actor: agent-warp
    source: "Inteligente/Resources/Documents/Research/HumanCenter.Pricing.md; Inteligente/Resources/Documents/Research/Critical Review and Revised Chatbot ROI Interview Playbook.md; founder-approved Discovery Pilot decision; Odoo 19.0 AI and Live Chat documentation"
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
- **The discovery-and-ROI methodology itself** (role-routed interview design, evidence grading A-E, benefit classification, screening logic): the core proprietary asset, analogous in importance to Shrinking AI's RCGFC framework. Fully specified down to an implementation-ready level in `../../../../Resources/Documents/Research/Financial Automation/financial_advisory_automation_mvp.xlsx` (turn-by-turn chatbot script, logical data model, ROI formulas, controls/scorecard, and phased implementation plan).
- **Odoo as discovery platform and intended agent workspace.** The existing live Odoo chatbot at `www.inteligente.site` is hosted on Frank and implements only generic livechat/lead-routing/lead-creation behavior; verified inspection found none of the governed disclosure, consent, sensitive-data interrupt, role-routing, evidence-grading, or Stop/Measure/Prototype/Pilot logic. It is not the partner pilot. The Discovery Pilot is planned for Odoo Online, with an Odoo AI Agent using GPT-4o (founder-reported; confirm in the pilot database) and intended to analyze only a minimized question/answer after explicit escalation. Odoo 19 docs state that the AI Agent takes priority over a scripted chatbot when both are assigned to one channel, while the scripted chatbot stores free-input answers in transcripts. The docs do not specify the exact agent prompt payload, retention, or provider data handling. Verify these behaviors in the live database before automated handoff; use founder-triggered analysis if needed. Odoo's longer-term role as an agent workspace with bounded roles/permissions and client connections remains an intention, not a deployed capability.
- **Staged hosting: Odoo Online → Frank → SolarSeed.** The partner pilot runs on Odoo Online (Odoo-managed cloud, not local-only). After pilot validation, Frank (`wera-ss-pt-sn-1`, TRL4) is the intended local Odoo/live-chat host with a local AI model. The SolarSeed TRL5 machine (`wera-ss-pt-tv-1`) is intended for the first paying customer's dedicated account/agent after readiness and customer-isolation checks. Both machines are owned and in Portugal/EU; combined connectivity cost is €71.54/month (see `../../../kb-cost-structure/docs/model/08-cost-structure.md`). Frank's current workload report is not a substitute for a pre-deployment capacity and isolation check.
- **Workflow-automation stack (for the build-and-implement phase, distinct from the discovery-chatbot tool above)**: n8n/Make/Zapier for workflow orchestration, LLM APIs for drafting/classification/extraction, OCR/document-extraction tooling for invoice/receipt/document automation. Whether Odoo's own automation/workflow capabilities substitute for or complement this stack in client builds is not yet decided (see Open Actions).
- **Accounting/CRM/ERP integration capability**: connectors needed to deliver combined packages (e.g. accounting + email automation).
- **EU-hosted infrastructure / data residency** (firm requirement where applicable): required given the target audience includes Financial Automation clients with confidential financial/investor/deal information (see `../../../kb-value-proposition/docs/products/04-financial-automation.md`); consistent with `../../../../SOUL.md` and security expectations (human approval, audit logs, DPA, no client-data training on public models). Odoo Online is cloud-hosted and must not be represented as local-only; verify the selected database region and provider processing/retention terms before the partner pilot. The later Frank/local-model MVP and SolarSeed client deployment have separate capacity, residency, and isolation gates.
- **Knowledge asset**: the pricing-benchmark and discovery-methodology research library under `../../../../Resources/Documents/Research/`, including the MVP workbook above.
- **Founder/consultant delivery expertise**: process mapping, workflow design, and financial/compliance-aware discovery facilitation.

## Decisions / Rules
- The workflow-automation stack (n8n/Make/Zapier + LLM APIs) is a committed resource for Automation Center's client-facing builds, unlike its "candidate, not yet committed" status under Human Center's Shrinking AI.
- EU data residency, audit logging, and DPA infrastructure are mandatory (not optional) given Financial Automation's investment-fund-adjacent and financial-advisory sub-segments (see `../../../kb-customers/docs/gtm/05-financial-automation-segments.md`).
- **Limit the initial pilot to the partner-approved data scope.** The Odoo Online pilot may use only aggregated metrics from the Financial partner's own firm after written authorization and cloud/privacy review; exclude credentials, raw client records, and third-party confidential data. Keep the existing generic bot separate from the pilot. Do not enable automatic analyst handoff until the scripted-first sequence, exact context, transcript/log retention, and provider handling are tested; otherwise the founder manually invokes the analyst with minimized one-question/answer context.
- Preserve the three-stage deployment boundary: Odoo Online partner pilot; Frank TRL4 local MVP after pilot validation; SolarSeed TRL5 first-customer deployment after readiness and isolation checks.
- Only add new infrastructure (a third machine, a paid hosting tier, new tooling) when a specific, evidenced requirement appears — per the resource-acquisition principle in `../../../kb-cost-structure/docs/model/08-cost-structure.md`.

## Evidence
- `../../../../Resources/Documents/Research/HumanCenter.Pricing.md` — unverified (self-described AI-chat estimate; see `../../../kb-revenue-streams/docs/model/07-revenue-streams.md`), defines the workflow-automation stack and named agency comparables.
- `../../../../Resources/Documents/Research/Critical Review and Revised Chatbot ROI Interview Playbook.md` — verified, defines the evidence-grading and benefit-classification methodology as a resource in its own right.
- `../../../../Resources/Documents/Research/Financial Automation/financial_advisory_automation_mvp.xlsx` — verified, implementation-ready chatbot script, data model, ROI model, controls/scorecard, and phased build plan.
- `../../../../Resources/Documents/Research/inteligente.working.note..md` — verified as the founder's own working note; source of the agent-workspace/Odoo-as-delivery-platform concept and the deliverable-centered automation approach.
- **Live Odoo agent configuration inspection (Sept 2026)** — verified: the deployed system prompt at `www.inteligente.site` contains only generic livechat identity, response-style, and lead-creation instructions; no disclosure, consent, sensitive-data-interrupt, role-routing, evidence-grading, or stop-rule logic is present in the visible top-level prompt. This is the most reliable evidence in this document, since it is a direct inspection of the live system rather than a stated intent.
- **Founder-reported Frank/SolarSeed machine roles and cost (Sept 2026)** — verified: 2 dedicated servers, €71.54/month combined connectivity, Frank = platform host (no other current workload), SolarSeed machine = first-client-instance host.
- [Odoo 19 AI live chat](https://www.odoo.com/documentation/19.0/applications/productivity/ai/live-chat.html), [AI agents](https://www.odoo.com/documentation/19.0/applications/productivity/ai/agents.html), [AI API keys](https://www.odoo.com/documentation/19.0/applications/productivity/ai/apikeys.html), and [scripted chatbots](https://www.odoo.com/documentation/19.0/applications/websites/livechat/chatbots.html) — document native routing priority, agent configuration/provider options, and transcript capture; the live payload and retention behavior still require verification.

## Cross-Domain Links
- Related domains: `kb-key-activities`, `kb-cost-structure`, `kb-solution`, `kb-channels`, `kb-governance`, `kb-key-partners`
- Related documents: `../../../kb-key-activities/docs/execution/05-automation-center-key-activities.md`, `../../../kb-cost-structure/docs/model/08-cost-structure.md`, `../../../kb-solution/docs/strategy/03-automation-center-solution.md`, `../../../kb-channels/docs/gtm/12-automation-center-channels.md`, `../../../kb-key-partners/docs/partnerships/06-key-partners.md`

## Open Actions
- Complete written authorization and cloud/privacy review for the Financial partner's aggregate data before the first Odoo Online pilot session; record allowed fields and exclusions, owner: Founder/Consultant.
- Inspect every pilot-database channel rule, chatbot script, agent prompt/topic/tool, model selection, request context, transcript/log storage and retention, and provider/privacy term. Test scripted-first behavior; if automatic escalation cannot preserve the boundary, keep founder-triggered minimized Q/A analysis, owner: Founder/Consultant.
- Record the Discovery Pilot session date, actual outputs, Operations partner validation, corrections, and buying decision or qualified paid-pilot offer; none is confirmed yet, owner: Founder/Consultant.
- After pilot validation, confirm Frank's capacity, ingress, tenancy, access controls, backups, and isolation before deploying the local Odoo/local-model MVP, owner: Founder/Consultant.
- Before the first paid customer is deployed on SolarSeed TRL5, verify host readiness and customer-specific account/agent isolation, owner: Founder/Consultant.
- Decide whether Odoo's native automation/workflow tooling replaces or complements n8n/Make/Zapier for client-facing builds, owner: Founder/Consultant.
- Stand up and review the applicable DPA/sub-processor terms before processing prospect-identifying or client personal data (see `../../../kb-governance/docs/legal/11-legal-structure.md`), owner: Founder/Consultant.
