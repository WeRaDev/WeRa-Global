---
metadata:
  primary_domain: key-activities
  secondary_domains: [solution, key-resources, metrics]
  owner_role: Founder/Consultant
  temporal_scope: current
  evidence_status: verified
  last_reviewed_at: 2026-09-16
  next_review_due: 2026-12-15
  provenance:
    actor: agent-warp
    source: "Inteligente/Resources/Documents/Research/Interview Playbook  Financial-Advisory Automation Discovery.md; Inteligente/Resources/Documents/Research/Chatbot-Led Automation Discovery  Critique and Revised Interview Playbook.md; Inteligente/Resources/Documents/Research/Critical Review and Revised Chatbot ROI Interview Playbook.md"
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
- **Role-routed discovery interview**: adviser/owner route (8-12 min), operational-colleague route (10-15 min), compliance/data-owner route (6-10 min, a feasibility gate), optional finance-owner route (only if a financial ROI will be presented). Conducted manually until a chatbot implementation is built and tested.
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

## Evidence
- `../../../../Resources/Documents/Research/Interview Playbook  Financial-Advisory Automation Discovery.md` — verified, defines the interview structure and roles.
- `../../../../Resources/Documents/Research/Chatbot-Led Automation Discovery  Critique and Revised Interview Playbook.md` — verified, defines the conversational state machine and escalation triggers.
- `../../../../Resources/Documents/Research/Critical Review and Revised Chatbot ROI Interview Playbook.md` — verified, defines evidence grading, measurement sprints, and pilot monitoring requirements.

## Cross-Domain Links
- Related domains: `kb-solution`, `kb-key-resources`, `kb-metrics`
- Related documents: `../../../kb-solution/docs/strategy/03-automation-center-solution.md`, `../../../kb-key-resources/docs/architecture/06-automation-center-key-resources.md`, `../../../kb-metrics/docs/financial/09-key-metrics.md`

## Open Actions
- Run the discovery interview manually with the first few prospects and log which questions/probes work in practice, owner: Founder/Consultant.
- Define the standard operating procedure for a measurement sprint (tooling, template, duration), owner: Founder/Consultant.
- Build and test a chatbot implementation once the manual process is validated, owner: Founder/Consultant.
