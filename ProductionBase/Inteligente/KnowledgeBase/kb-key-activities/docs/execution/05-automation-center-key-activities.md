---
metadata:
  primary_domain: key-activities
  secondary_domains: [solution, key-resources, metrics]
  owner_role: Founder/Consultant
  temporal_scope: current
  evidence_status: verified
  last_reviewed_at: 2026-09-25
  next_review_due: 2026-12-25
  provenance:
    actor: agent-warp
    source: "Inteligente/Resources/Documents/Research/Interview Playbook  Financial-Advisory Automation Discovery.md; Inteligente/Resources/Documents/Research/Chatbot-Led Automation Discovery  Critique and Revised Interview Playbook.md; Inteligente/Resources/Documents/Research/Critical Review and Revised Chatbot ROI Interview Playbook.md; founder-approved Discovery Pilot decision"
    confidence: high
    review_status: draft
---
# Automation Center Key Activities

## Purpose
List Automation Center's core delivery activities.

## Scope
- In scope: activities from discovery interview through build, deployment, and support retainer.
- Out of scope: Human Center's session-flow activities, Shrinking AI (`04-key-activities.md`) and Empowering Human; Financial Automation's compliance-specific activity extensions (see `../../../kb-value-proposition/docs/products/04-financial-automation.md`).

## Current State
- **Status (Sept 2026): partner-led Discovery Pilot formally initiated; not yet run.** No first-session date or results are confirmed. The Financial partner acts as customer and the Operations partner validates the method. The intended stage-1 tool is an Odoo Online scripted interview with escalation-gated AI analysis; use a founder-triggered analyst step until automatic handoff and data boundaries are verified (HC-016).
- **Role-routed, deliverable-first discovery interview**: adviser/owner route (8-12 min), operational-colleague route (10-15 min), compliance/data-owner route (6-10 min, a feasibility gate), optional finance-owner route (only if a financial ROI will be presented). Start from the output to deliver, its owner/recipient, frequency, quality criteria, effort, exceptions, review, and delivery; design a better delivery method rather than copying the existing workflow.
- **Evidence grading and benefit classification**: every claimed number is graded A-E and every benefit classified (cash-releasing saving, cost avoidance, incremental margin, released capacity, quality/risk benefit) before any value calculation is presented.
- **Screening decision**: producing one of Stop / Measure / Prototype / Pilot as a one-page decision record (opportunity statement, baseline, value route, feasibility, uncertainty, recommendation) — never a single-point guaranteed ROI.
- **Measurement sprint** (when evidence grade is too low): sampling 5-10 normal cases and recording active time, exceptions, and rework close to real performance, before re-attempting the estimate.
- **Workflow build and integration**: configuring n8n/Make/Zapier workflows, LLM API integration, OCR/document extraction, and accounting/CRM/ERP integration as scoped.
- **Security, testing, documentation, and training** delivered before go-live, including data-processing boundaries agreed in the compliance route.
- **Pilot monitoring**: matched pre/post evidence covering eligible/excluded volume, successful completion and fallback, active human time, review/correction time, errors and severity, human overrides, adoption/abandonment, cycle time, actual expenditure/revenue consequence, and full implementation/operating cost.
- **Ongoing monitoring/support retainer**: post-deployment maintenance and monitoring as an optional recurring service.
- **Human escalation handling**: routing legal/tax/investment-advice requests, credential exposure, suspected breaches, disputed consent, and binding-ROI-guarantee requests to human review rather than resolving them within the interview or automation flow.

## Decisions / Rules
- Do not propose a build or quote a price before the discovery interview reaches a Prototype or Pilot recommendation.
- Do not skip the compliance/data-owner route for any client whose data may be regulated or confidential; this route is mandatory for Financial Automation clients (financial-advisory, investment-fund-adjacent), see `../../../kb-solution/docs/strategy/04-financial-automation-solution.md`.
- Every pilot must define its eligible unit, baseline, and success/guardrail/stop criteria before deployment, per the discovery methodology.
- For the Odoo Online partner pilot, use only authorized aggregated metrics from the Financial partner's own firm after cloud/privacy review; do not collect credentials, raw client records, or third-party confidential data. Odoo Online is cloud-hosted, not local-only.
- The AI analyst should receive a minimized question/answer only after explicit escalation. Odoo 19 documents that an assigned AI Agent takes priority over a scripted chatbot on the same channel; verify actual handoff, context payload, transcript/log retention, and provider handling before enabling automatic invocation. The founder triggers the analyst manually if the boundary cannot be demonstrated.
- Present the draft automation plan and evidence-graded ROI range/assumptions only after founder review; pilot success requires a validated interview/ROI workflow and a documented buying decision or qualified paid-pilot offer. Payment is a separate milestone.

## Evidence
- `../../../../Resources/Documents/Research/Interview Playbook  Financial-Advisory Automation Discovery.md` — verified, defines the interview structure and roles.
- `../../../../Resources/Documents/Research/Chatbot-Led Automation Discovery  Critique and Revised Interview Playbook.md` — verified, defines the conversational state machine and escalation triggers.
- `../../../../Resources/Documents/Research/Critical Review and Revised Chatbot ROI Interview Playbook.md` — verified, defines evidence grading, measurement sprints, and pilot monitoring requirements.
- [Odoo 19 AI live chat](https://www.odoo.com/documentation/19.0/applications/productivity/ai/live-chat.html) — documents agent-priority behavior when a Live Chat channel has both a scripted chatbot and an AI Agent.
- [Odoo 19 scripted chatbots](https://www.odoo.com/documentation/19.0/applications/websites/livechat/chatbots.html) — documents structured scripts, free-input capture, and transcript persistence.

## Cross-Domain Links
- Related domains: `kb-solution`, `kb-key-resources`, `kb-metrics`
- Related documents: `../../../kb-solution/docs/strategy/03-automation-center-solution.md`, `../../../kb-key-resources/docs/architecture/06-automation-center-key-resources.md`, `../../../kb-metrics/docs/financial/09-key-metrics.md`

## Open Actions
- Run the first Odoo Online partner-pilot session and record its date, authorized data scope, interview findings, validator feedback, reviewed output, and buying decision or qualified paid-pilot offer; no session/result is confirmed yet, owner: Founder/Consultant, tracked as HC-009.
- Define the standard operating procedure for a measurement sprint (tooling, template, duration), owner: Founder/Consultant.
- Verify the Odoo Online scripted-first/AI-agent handoff and data boundary; use founder-triggered, minimized single-answer analysis if automatic escalation fails the test, owner: Founder/Consultant, tracked as HC-016.
- After pilot validation, build the local Odoo/local-model MVP on Frank and verify capacity, ingress, access control, and isolation before deployment, owner: Founder/Consultant.
