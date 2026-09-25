---
metadata:
  primary_domain: solution
  secondary_domains: [problem, value-proposition, key-activities, unfair-advantage]
  owner_role: Founder/Consultant
  temporal_scope: current
  evidence_status: verified
  last_reviewed_at: 2026-09-25
  next_review_due: 2026-12-25
  provenance:
    actor: agent-warp
    source: "Inteligente/Resources/Documents/Research/Interview Playbook  Financial-Advisory Automation Discovery.md; Inteligente/Resources/Documents/Research/Chatbot-Led Automation Discovery  Critique and Revised Interview Playbook.md; Inteligente/Resources/Documents/Research/Critical Review and Revised Chatbot ROI Interview Playbook.md; founder-approved Discovery Pilot decision; Odoo 19.0 AI and Live Chat documentation"
    confidence: high
    review_status: draft
---
# Automation Center Solution

## Purpose
Describe Automation Center's solution approach at product-line level: a build-and-operate automation service gated by a proprietary, evidence-graded discovery-and-ROI methodology.

## Scope
- In scope: the generic discovery/screening methodology and the automation-build delivery model, applicable line-wide.
- Out of scope: Human Center's Shrinking AI (`02-solution.md`) and Empowering Human; Financial Automation's finance-specific compliance extensions to this methodology, see `04-financial-automation-solution.md`.

## Current State

### Core differentiator: the discovery-and-ROI methodology
The methodology's design evolved across three research passes and is itself the product's moat (see `../../../kb-unfair-advantage/docs/strategy/11-automation-center-unfair-advantage.md`):

1. **Three knowledge-owner roles**, each asked only what they can reliably know: the adviser/owner (deliverable, customer outcome, fee model, demand, recent example), the operational colleague (active time, handoffs, rework, exceptions, volume), and the compliance/data owner (data location, permissions, retention, controls — a feasibility gate, not an ROI source). An optional finance-owner route is triggered only when a financial ROI figure will actually be presented.
2. **One recent concrete instance, not an average.** The interview reconstructs the most recent normal example of a recurring deliverable rather than asking abstract "how many hours does this usually take" questions, which are vulnerable to recall bias. Short recall periods and elicited-then-ranged numbers (never anchored with example ranges) improve reliability.
3. **Screening decision, not an investment-grade ROI promise.** The chatbot (or its human-run precursor) never outputs a single-point "guaranteed ROI." It classifies every benefit as one of: cash-releasing saving, cost avoidance, incremental contribution margin, released capacity (not counted as cash until an owner confirms conversion), or quality/risk benefit (monetized only with evidence). It calculates `Recurring unit x eligible volume x observed net improvement x adoption x value-capture rate - full cost`, and separates capacity from cash: `Released capacity = V x E x (Tb-Ta) x A`; `Financial benefit = Cs + Ca + Mi + Qv`; `ROI = (Financial benefit - full cost) / full cost x 100`.
4. **Evidence grading (A-E).** Every input is graded: A = system record/invoice/ledger, B = recent sample/timestamps/diary, C = reconciled two-respondent estimate, D = single unsupported recollection, E = automation-team/chatbot assumption (never presented as client evidence). Low-grade opportunities are redirected to a short **measurement sprint** (sample 5-10 normal cases, record active time/exceptions) rather than guessed.
5. **Four possible outcomes:** Stop (no material/permissible opportunity), Measure (insufficient baseline, run a measurement sprint), Prototype (value route exists, low-risk technical test justified), Pilot (baseline, controls, owner and success thresholds are ready).
6. **Safety and neutrality constraints** (mandatory if/when implemented as an actual chatbot): one question per turn, no leading or praising language, no silent gap-filling, explicit consent/disclosure before collection, sensitive-data detection and interruption, mandatory human escalation for legal/tax/investment-advice requests, credentials, suspected breaches, disputed consent, or binding-ROI-guarantee requests.

### Delivery: automation build
Once a Pilot is approved: process mapping and design, workflow automation via n8n/Make/Zapier, LLM API integration, OCR/document extraction where needed, integration with the client's accounting/CRM/ERP systems, security/testing/documentation/training, deployment, then matched pre/post pilot monitoring (eligible/excluded volume, active time, errors, overrides, adoption, actual expenditure/revenue consequence, full cost) before any renewal or expansion decision.

### Compliance for regulated clients
For financial-advisory or otherwise regulated clients, the compliance/data-owner route (present in the generic methodology above) becomes mandatory rather than optional. Financial Automation extends this route with finance-specific jurisdictional and sector-obligation detail, see `04-financial-automation-solution.md`.

## Decisions / Rules
- Never convert a respondent's estimate into a financial ROI figure without labeling its evidence grade.
- Never count released staff capacity as cash benefit unless a named owner confirms how and when it converts to a financial outcome.
- Route legal/tax/investment-advice requests, credential exposure, suspected breaches, and disputed consent to human escalation immediately; the automated/human-run interview does not resolve these itself.
- Regulated-client engagements (see Financial Automation) require the compliance/data-owner route to complete before any pilot is proposed.
- During the partner pilot, use only authorized aggregated metrics from the Financial partner's own firm; exclude credentials, raw client records, and third-party confidential data. Odoo Online is cloud-hosted, not local-only.
- Do not enable automatic AI-agent handoff until a live-instance test verifies the scripted-chatbot-first sequence, actual prompt context, transcript/log retention, and provider handling. If these boundaries cannot be demonstrated, the founder manually triggers the analyst with minimized single-question/answer context.

### Staged delivery decision (Sept 2026)
The partner-led Financial Automation Discovery Pilot was **formally initiated**, but no first-session date or result has been confirmed. This is a commercial pilot as well as a method test. It proceeds through three gates:

1. **Discovery Pilot — Odoo Online.** The Financial partner acts as the customer; the Operations partner validates the method. A structured, scripted interview collects answers and numeric values one at a time, focusing on deliverables and using only aggregated metrics from the Financial partner's own firm after written authorization and cloud/privacy review. Do not collect credentials, raw client records, or third-party confidential data. Odoo Online is cloud-hosted, so this stage is not local-only.
2. **Local MVP — Frank (`wera-ss-pt-sn-1`, TRL4).** After pilot validation, host Odoo and live chat on Frank and use a local AI model, subject to capacity, ingress, tenancy, access-control, backup, and isolation checks.
3. **First paying customer — SolarSeed TRL5 (`wera-ss-pt-tv-1`).** After a paid customer is signed, deploy that customer's account and agent on the intended TRL5 host after confirming readiness and customer isolation. The future direction is a dedicated machine per customer, either within Inteligente's framework/network or on the customer's premises.

The existing live Odoo chatbot on Frank remains a separate, generic lead-capture deployment; inspected configuration did not show the governed interview logic. For the pilot, the intended analyst is an Odoo AI Agent using GPT-4o (founder-reported; confirm the model in the pilot database). It should be invoked only on explicit escalation and receive minimized, schema-allowed context for one specific question and answer, so it can suggest a targeted follow-up. However, Odoo 19 documentation says an AI Agent assigned to a Live Chat channel rule takes priority over the scripted chatbot if both are assigned. The documentation does not establish that the agent can be deferred until a particular scripted step, nor does it specify the exact context sent to the model or transcript/provider retention. Standard chatbot free-text answers are stored in chat transcripts. Verify the live configuration, prompt payload, provider processing, storage, access, and retention before enabling automatic handoff. If Odoo Online cannot demonstrate the required scripted-first boundary, the founder triggers the analyst manually on a minimized single-question/answer; do not claim that prompts alone prevent access to the full transcript or guarantee non-reconstructability.

The interview is deliverable-first: identify the output, owner, recipient, frequency, quality criteria, effort, exceptions, review, and delivery, then design a better way to produce the outcome rather than copy the current workflow. Use deterministic calculations to produce a draft automation plan, evidence-graded ROI range, sensitivity, and assumptions. The founder reviews the draft before presenting it as a proposal. Pilot success requires a validated interview/ROI workflow plus a documented buying decision or qualified paid-pilot offer; actual payment is a separate milestone.

## Evidence
- `../../../../Resources/Documents/Research/Interview Playbook  Financial-Advisory Automation Discovery.md` — verified, original three-role discovery design and ROI worksheet.
- `../../../../Resources/Documents/Research/Chatbot-Led Automation Discovery  Critique and Revised Interview Playbook.md` — verified, chatbot-safe conversational design, evidence model, escalation triggers.
- `../../../../Resources/Documents/Research/Critical Review and Revised Chatbot ROI Interview Playbook.md` — verified, screening-vs-investment separation, benefit classification, evidence grading, financial formulas.
- `../../../../Resources/Documents/Research/Financial Automation/financial_advisory_automation_mvp.xlsx` — verified, implementation-ready chatbot script (turn-by-turn questions, probe triggers, escalation conditions), logical data model, dynamic ROI model, controls/scorecard, and phased build/QA/pilot plan.
- [Odoo 19 AI live chat](https://www.odoo.com/documentation/19.0/applications/productivity/ai/live-chat.html) — documents channel-rule assignment, agent priority over a scripted chatbot when both are assigned, and explicit escalation/topic behavior.
- [Odoo 19 AI agents](https://www.odoo.com/documentation/19.0/applications/productivity/ai/agents.html), [AI API keys](https://www.odoo.com/documentation/19.0/applications/productivity/ai/apikeys.html), and [scripted chatbots](https://www.odoo.com/documentation/19.0/applications/websites/livechat/chatbots.html) — describe agent prompts/topics/sources, provider configuration, and transcript persistence for free-input answers; they do not specify this deployment's exact context payload or retention settings.

## Cross-Domain Links
- Related domains: `kb-value-proposition`, `kb-key-activities`, `kb-unfair-advantage`, `kb-customers`, `kb-key-resources`, `kb-channels`
- Related documents: `../../../kb-value-proposition/docs/products/03-automation-center.md`, `../../../kb-key-activities/docs/execution/05-automation-center-key-activities.md`, `../../../kb-unfair-advantage/docs/strategy/11-automation-center-unfair-advantage.md`, `04-financial-automation-solution.md`, `../../../kb-key-resources/docs/architecture/06-automation-center-key-resources.md`, `../../../kb-channels/docs/gtm/12-automation-center-channels.md`

## Open Actions
- Schedule and run the first Odoo Online partner-pilot session; record the session date, partner authorization, data scope, validation findings, output review, and commercial buying decision. The pilot is initiated but no session/result is recorded, owner: Founder/Consultant.
- Test in the actual Odoo Online database whether a scripted questionnaire can invoke the AI Agent only after explicit escalation. Inspect assigned channel rules, all prompts/topics/tools, model selection, actual request context, transcript/log storage and retention, and provider/privacy terms. Keep agent assignment disabled if it overrides the script or exposes more context than approved; use founder-triggered, minimized Q/A analysis for the pilot until verified, owner: Founder/Consultant.
- Test the interview against the required disclosure/authorization, sensitive-data interrupt, deliverable-first probes, evidence grading, Stop/Measure/Prototype/Pilot logic, deterministic ROI range, and founder-review gates before broadening beyond the partner pilot, owner: Founder/Consultant.
- After successful pilot validation, verify Frank's capacity, ingress, tenancy, access controls, backup, and isolation; then build the local Odoo/local-model MVP, owner: Founder/Consultant.
- Before onboarding the first paying customer on SolarSeed TRL5, confirm host readiness, customer-specific account/agent separation, access controls, and rollback/incident handling, owner: Founder/Consultant.
- Define a client-authorized secure channel for any later redacted artifact collection, owner: Founder/Consultant.
