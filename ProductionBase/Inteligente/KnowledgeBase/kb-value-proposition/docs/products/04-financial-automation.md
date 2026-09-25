---
metadata:
  primary_domain: value-proposition
  secondary_domains: [solution, revenue-streams, key-activities, governance]
  owner_role: Founder/Consultant
  temporal_scope: current
  evidence_status: verified
  last_reviewed_at: 2026-09-25
  next_review_due: 2026-12-25
  provenance:
    actor: agent-warp
    source: "Inteligente/Resources/Documents/Research/HumanCenter.Pricing.md; Inteligente/Resources/Documents/Research/Interview Playbook  Financial-Advisory Automation Discovery.md; Inteligente/Resources/Documents/Research/Chatbot-Led Automation Discovery  Critique and Revised Interview Playbook.md; Inteligente/Resources/Documents/Research/Critical Review and Revised Chatbot ROI Interview Playbook.md; founder-approved Discovery Pilot decision; Odoo 19.0 AI and Live Chat documentation"
    confidence: high
    review_status: draft
---
# Financial Automation

## Purpose
Define Financial Automation, Automation Center's first named service: workflow automation specialised for the financial industry.

## Scope
- In scope: the finance-specific application of Automation Center's build-and-implement automation service and discovery-and-ROI methodology, including compliance/regulatory considerations distinct to financial-advisory and investment-fund-adjacent clients.
- Out of scope: Automation Center's generic, line-level positioning and methodology (`03-automation-center.md`, `../../../kb-solution/docs/strategy/03-automation-center-solution.md`); Human Center's services (Shrinking AI, Empowering Human).

## Current State
Financial Automation applies Automation Center's general build-and-operate automation capability to clients in the financial industry, where confidential deal/investor information and sector-specific obligations raise the bar on security, compliance, and evidence handling. Two evidenced client profiles ground this service (see `../../../kb-customers/docs/gtm/05-financial-automation-segments.md`):

1. **Solo consultant/independent professional with confidential client data** — an independent consultant working with investment funds in Europe, needing email and accounting/bookkeeping automation with a human-approval, audit-logged, DPA-backed security posture because of confidential deal/investor information. The buyer is the solo consultant, not the fund itself — this must not be priced or positioned as a "PE AI solution."
2. **Small financial-advisory or professional-services firms with distinct roles** — firms large enough to have separate adviser/owner, operational colleague, and compliance/data-owner functions. These firms may fall under sector-specific supervision, communications, and recordkeeping obligations (e.g. FINRA-adjacent duties in relevant US-perimeter firms), which must be established per client rather than assumed.

**Delivery**: Financial Automation follows Automation Center's standard delivery flow (discovery and ROI screening, build, deployment, monitoring — see `03-automation-center.md`), with the compliance/data-owner discovery route mandatory for every engagement, establishing jurisdiction, permitted data, required approvals, and prohibited actions before any pilot proceeds (see `../../../kb-solution/docs/strategy/04-financial-automation-solution.md`).

**Partner-led Discovery Pilot (formally initiated Sept 2026):** the Financial partner acts as the customer, using only aggregated metrics from their own firm after written authorization and cloud/privacy review; the Operations partner validates the interview method and output. No first-session date or result is confirmed. The pilot is planned on Odoo Online and is cloud-hosted, not local-only. The existing live chatbot on Frank is generic lead capture and is separate from this pilot. Do not use credentials, raw client records, or third-party confidential data.

The intended Odoo AI Agent uses GPT-4o (founder-reported; verify in the pilot database) and should analyze a minimized question/answer only after explicit escalation. Odoo 19 docs state that assigning an AI Agent and scripted chatbot to the same channel prioritizes the agent; verify actual handoff, prompt context, transcript/log retention, and provider handling before automatic invocation. Use founder-triggered analyst prompts if the scripted-first boundary cannot be demonstrated. The draft automation plan and deterministic, evidence-graded ROI range/assumptions require founder review before being presented as a proposal.

After method validation, stage 2 is a local Odoo/local-model MVP on Frank (TRL4), subject to capacity and isolation checks. Stage 3 is the first paying customer's dedicated account and agent on SolarSeed TRL5 after readiness and customer-isolation checks. Pilot success requires a validated interview/ROI workflow plus a documented buying decision or qualified paid-pilot offer; payment is a separate milestone.

The Automation-Center-leads cross-sell direction remains in effect — a Financial Automation engagement, once signed, may be followed by attaching Human Center consultancy, not the reverse (see `03-automation-center.md`).

## Decisions / Rules
- Every Financial Automation engagement triggers the compliance/data-owner discovery route and heightened controls (human approval, audit logging, DPA, EU data residency) before any pilot proceeds.
- For the partner pilot, authorize only aggregated metrics from the Financial partner's own firm after privacy/cloud review; no credentials, raw client records, or third-party confidential data. Odoo Online must not be described as local-only.
- Do not enable automatic analyst handoff until the Odoo Online scripted-first flow, actual context sent, transcript/log retention, and provider handling pass live verification; otherwise the founder triggers minimized single-question/answer analysis.
- Pilot output is a draft automation plan and evidence-graded ROI range with assumptions, reviewed by the founder; it is not a guaranteed ROI or binding proposal.
- Do not position Financial Automation as a "private equity AI solution" merely because a client's own clients are investment funds; pricing and scope target the solo consultant/small firm buyer, not the fund itself.
- Existing sector obligations (e.g. supervision, communications and recordkeeping duties in relevant regulated firms) can remain applicable to AI-assisted activity; findings must be recorded as confirmed, unresolved, or requiring specialist review — never "compliant" merely because a respondent believes it is.

## Evidence
- `../../../../Resources/Documents/Research/HumanCenter.Pricing.md` — unverified (self-described AI-chat estimate); its persona and security-requirement framing are directionally useful but not independently confirmed with a real financial-industry prospect yet (see Open Actions and `../../../kb-revenue-streams/docs/model/07-revenue-streams.md` for the pricing corroboration note).
- `../../../../Resources/Documents/Research/Interview Playbook  Financial-Advisory Automation Discovery.md` — verified, defines the financial-advisory firm persona with distinct adviser/operations/compliance roles.
- `../../../../Resources/Documents/Research/Chatbot-Led Automation Discovery  Critique and Revised Interview Playbook.md` — verified, chatbot-safe redesign applicable to regulated-client discovery.
- `../../../../Resources/Documents/Research/Critical Review and Revised Chatbot ROI Interview Playbook.md` — verified, screening-vs-investment separation and evidence grading applied to regulated engagements.
- [Odoo 19 AI live chat](https://www.odoo.com/documentation/19.0/applications/productivity/ai/live-chat.html) — documents priority behavior when both an AI Agent and scripted chatbot are assigned to a channel.
- [Odoo 19 AI agents](https://www.odoo.com/documentation/19.0/applications/productivity/ai/agents.html) and [scripted chatbots](https://www.odoo.com/documentation/19.0/applications/websites/livechat/chatbots.html) — document agent topics/sources and storage of chatbot free-input answers; live context/retention still require verification.

## Cross-Domain Links
- Related domains: `kb-solution`, `kb-customers`, `kb-governance`, `kb-revenue-streams`
- Related documents: `03-automation-center.md`, `../../../kb-solution/docs/strategy/04-financial-automation-solution.md`, `../../../kb-customers/docs/gtm/05-financial-automation-segments.md`, `../../../kb-governance/docs/legal/11-legal-structure.md`

## Open Actions
- Run the first partner-led Discovery Pilot session; record the session date, authorization, allowed data scope, validator findings, reviewed output, and buying decision or qualified paid-pilot offer, owner: Founder/Consultant.
- Verify Odoo Online's scripted-first AI escalation and data-handling boundary; use founder-triggered analysis if automatic handoff cannot be demonstrated, owner: Founder/Consultant.
- Confirm which specific regulatory regimes apply per target jurisdiction (Western Europe and the Nordics primary), owner: Founder/Consultant.
- Validate the documented benchmark pricing against the first signed Financial Automation client, owner: Founder/Consultant.
- After pilot validation, verify Frank capacity/isolation for the local MVP and SolarSeed TRL5 readiness/isolation before any paying-customer deployment, owner: Founder/Consultant.
