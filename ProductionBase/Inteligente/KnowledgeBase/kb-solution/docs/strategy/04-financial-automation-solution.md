---
metadata:
  primary_domain: solution
  secondary_domains: [problem, value-proposition, key-activities, unfair-advantage, governance]
  owner_role: Founder/Consultant
  temporal_scope: current
  evidence_status: verified
  last_reviewed_at: 2026-09-29
  next_review_due: 2026-12-29
  provenance:
    actor: agent-warp
    source: "Inteligente/Resources/Documents/Research/Interview Playbook  Financial-Advisory Automation Discovery.md; Inteligente/Resources/Documents/Research/Chatbot-Led Automation Discovery  Critique and Revised Interview Playbook.md; Inteligente/Resources/Documents/Research/Critical Review and Revised Chatbot ROI Interview Playbook.md; founder-approved Discovery Pilot decision; founder-defined Consultancy Automation internal-first decision (2026-09-29); Odoo 19.0 AI and Live Chat documentation"
    confidence: medium
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

### Internal Consultancy Automation prerequisite
Before any external Financial Automation pilot, validate a bounded automation use case within Inteligente's own consultancy operations and measure its efficiency/outcomes. The workflow, baseline, measures, implementation, and host have not been selected. This is a planned internal validation step, not a claim that an automation has been built or that it will use Frank.

### Partner-led Discovery Pilot (formally initiated Sept 2026; deferred, not cancelled)
The external pilot has not been completed: no first-session date or result has been confirmed. It is deferred until Consultancy Automation is validated and the existing safety, actionable-human-notification, privacy, data-flow, and authorization gates pass. The **Financial partner acts as the customer**, using only aggregated metrics from their own firm after written authorization and cloud/privacy review. The **Operations partner validates** the interview method and output. The planned external stage 1 is Odoo Online, so data processing is cloud-hosted and is not local-only. Credentials, raw client records, and third-party confidential data are out of scope.

The intended AI analyst is an Odoo AI Agent using GPT-4o (reported current model; verify it in the pilot database). It should be called only after an explicit chatbot escalation and analyze one minimized question/answer at a time to suggest a clarifying follow-up. Odoo 19 documentation states that when both a chatbot and AI Agent are assigned to a Live Chat channel, the AI Agent workflow takes priority. The exact deferred-handoff capability, context payload, and transcript/provider retention are not established by the docs and must be verified in the live instance before automatic handoff; otherwise the founder manually triggers the analyst. The draft automation plan and evidence-graded ROI estimate/range are reviewed by the founder before being presented as a proposal.

After method validation, stage 2 is a local Odoo/local-model MVP on Frank (TRL4); stage 3 is the first paying customer's dedicated account and agent on SolarSeed TRL5, subject to capacity, readiness, and isolation checks. Pilot success is a validated interview/ROI workflow plus a documented buying decision or qualified paid-pilot offer. Payment is a separate milestone.

### Configuration and test gate (25 September 2026)
The founder confirmed that the authorized database runs on Odoo Online. The separate pilot chatbot 4 was configured for synthetic testing, then archived/inactivated after sensitive-input, legal/tax/investment-advice, and guaranteed-ROI stop tests failed by advancing to the next question. Its compliance/data-owner referral stopped intake but sent no human notification or transfer. No partner session or result is confirmed. The pilot remains blocked; it is not safe to infer a human handoff from a terminal message. A passing safety gate requires immediate intake/tool stop, no substantive advice or ROI promise, prevention of downstream CRM/email/summary copies where controllable, and an actionable human transfer or notification whose delivery is verified in an isolated test. See `../../../../tasks/Financial Automation Discovery Pilot  Configuration and Test Handoff.md`.

The same handoff records a separate existing Human Center `/discovery-interview` route assigned to Agent 5, with CRM Create/Get Lead tools available. The route's public reachability, runtime side effects, safety behavior, and human-notification path have not been tested; use the audit-only task at `../../../../tasks/comet-audit-discovery-interview-agent5.md`. The hosting confirmation does not establish database region, provider/runtime, API-key mode, request context, or retention.

## Decisions / Rules
- Every Financial Automation engagement must complete the compliance/data-owner discovery route before any pilot is proposed; this is a firm requirement, not case-by-case judgment.
- Do not begin any external Financial Automation pilot until Consultancy Automation has been validated and the existing safety, actionable-human-notification, privacy, data-flow, and authorization gates pass; the partner pilot remains deferred, not cancelled.
- The partner Discovery Pilot may use only authorized aggregated metrics from the Financial partner's own firm after cloud/privacy review; no credentials, raw client records, or third-party confidential data. Do not describe the Odoo Online phase as local-only.
- Do not enable automatic AI-agent handoff until the scripted-chatbot-first sequence, actual prompt context, transcript/log retention, and provider handling have been verified in the pilot database. Use founder-triggered, minimized single-question/answer analysis if these controls cannot be demonstrated.
- Findings from the compliance/data-owner route must be recorded as confirmed, unresolved, or requiring specialist review — never assumed compliant.
- Use need-based referrals between Human Center and Automation Center in either direction. Do not infer cross-line conversion from the routing strategy or the two unqualified Human-to-Automation interest signals.
- Route legal/tax/investment-advice requests, sensitive-input/credential exposure, suspected breaches, disputed consent, and guaranteed-ROI requests to an immediate hard stop and human escalation. Do not repeat or propagate trigger content to CRM leads, emails, or summaries where controllable; make no substantive advice/ROI claim. Verify an actual human transfer or delivered minimal notification—not just a conversation end. If the runtime cannot enforce and evidence this, no live session or public use is allowed.

## Evidence
- `../../../../Resources/Documents/Research/Interview Playbook  Financial-Advisory Automation Discovery.md` — verified, original three-role discovery design including the compliance/data-owner role.
- `../../../../Resources/Documents/Research/Chatbot-Led Automation Discovery  Critique and Revised Interview Playbook.md` — verified, chatbot-safe conversational design and escalation triggers applicable to regulated engagements.
- `../../../../Resources/Documents/Research/Critical Review and Revised Chatbot ROI Interview Playbook.md` — verified, evidence grading and compliance-recording discipline.
- **Founder-defined Consultancy Automation internal-first decision (2026-09-29)** — primary sequencing decision; internal workflow, host, baseline, and validation result are not yet established.
- [Odoo 19 AI live chat](https://www.odoo.com/documentation/19.0/applications/productivity/ai/live-chat.html) — documents AI-agent priority when both an agent and scripted chatbot are assigned to one channel.
- [Odoo 19 scripted chatbots](https://www.odoo.com/documentation/19.0/applications/websites/livechat/chatbots.html) — documents free-input capture and transcript storage.

## Cross-Domain Links
- Related domains: `kb-value-proposition`, `kb-customers`, `kb-governance`
- Related documents: `03-automation-center-solution.md`, `../../../kb-value-proposition/docs/products/04-financial-automation.md`, `../../../kb-customers/docs/gtm/05-financial-automation-segments.md`, `../../../kb-governance/docs/legal/11-legal-structure.md`

## Open Actions
- Define and validate the internal Consultancy Automation workflow, baseline, and efficiency/outcome measures before any external pilot; hosting remains undecided, owner: Founder/Consultant, see `../../../../tasks/backlog.md` HC-021.
- Confirm which specific regulatory regimes apply per target jurisdiction before the first Financial Automation pilot; per Sept 2026 decision, treat this generically (GDPR baseline) across Europe for now rather than researching country-specific advisory regulation upfront, owner: Founder/Consultant.
- Define the client-authorized secure channel for redacted artifact collection for regulated clients, owner: Founder/Consultant.
- Review evidence for the written authorization and cloud/privacy review that the founder reports complete before the first pilot session; record the authorized data fields and excluded data, owner: Founder/Consultant.
- Resolve the failed hard-stop tests, actionable human-notification behavior, and transcript/data-handling boundary in an isolated synthetic test before any partner session or automatic analysis; use founder-triggered analysis only after its data handling is approved, and keep the bot out of live use if the native flow cannot prove the boundary, owner: Founder/Consultant.
- Complete the separate audit of `/discovery-interview` and Agent 5 for reachability, CRM side effects, safety behavior, human notification, and privacy using `../../../../tasks/comet-audit-discovery-interview-agent5.md`; do not create production leads, owner: Founder/Consultant.
- After the pilot, validate the compliance/data-owner route with the named profile-2 prospects before proposing a client pilot (see `../../../kb-customers/docs/gtm/05-financial-automation-segments.md`), owner: Founder/Consultant.
