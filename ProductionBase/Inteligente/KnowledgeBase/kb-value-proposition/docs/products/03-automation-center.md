---
metadata:
  primary_domain: value-proposition
  secondary_domains: [solution, revenue-streams, key-activities]
  owner_role: Founder/Consultant
  temporal_scope: current
  evidence_status: verified
  last_reviewed_at: 2026-09-29
  next_review_due: 2026-12-29
  provenance:
    actor: agent-warp
    source: "Inteligente/Resources/Documents/Research/HumanCenter.Pricing.md; Inteligente/Resources/Documents/Research/Interview Playbook  Financial-Advisory Automation Discovery.md; Inteligente/Resources/Documents/Research/Chatbot-Led Automation Discovery  Critique and Revised Interview Playbook.md; Inteligente/Resources/Documents/Research/Critical Review and Revised Chatbot ROI Interview Playbook.md; founder-approved Discovery Pilot decision; Odoo 19.0 AI and Live Chat documentation; founder-reported anonymized cross-sell outcome follow-up (2026-09-29)"
    confidence: medium
    review_status: draft
---
# Automation Center (Product Line)

## Purpose
Define Automation Center, Inteligente's second product line: a standalone build-and-implement automation service, distinct from the Human Center product line.

## Scope
- In scope: the automation-build service (n8n/Make/Zapier + LLM APIs) for back-office workflows, and its proprietary discovery-and-ROI methodology, at product-line level.
- Out of scope: Human Center's services, Shrinking AI (`02-services.md`) and Expanding Human (`05-expanding-human.md`); Financial Automation, Automation Center's named external service specialized for the financial industry, see `04-financial-automation.md`.

## Current State
Automation Center is a **build-and-operate automation agency service**. It targets a broad audience: any professional-services firm or solo consultant needing back-office automation (see `../../../kb-customers/docs/gtm/04-automation-center-segments.md`). Financial Automation is its first named service, specialising this general capability for the financial industry, including investment-fund-adjacent and other more heavily regulated contexts (see `04-financial-automation.md`).

**Need-based referral strategy (decided Sept 2026): bidirectional, not lead-first.** Refer Human Center clients to Automation Center when they have a defined organizational process-automation need; refer Automation Center clients to Shrinking AI when they need help improving existing AI use, or to Expanding Human when they are exploring where AI could support their goals. The two reported Human-Center-originating Automation Center interest signals remain unqualified: Client A is considering unspecified services after a separate paid Expanding Human consultancy; Client B has started building a booking website and expressed interest in website-administration automation. No Automation Center order or delivery, or Automation-Center-to-Human conversion, has been reported. The routing strategy is not a sales result.

**Near-term focus (Sept 2026): internal-first Consultancy Automation.** This planned internal product/use case will automate Inteligente's own consultancy operations and measure efficiency/outcomes before wider external rollout. Its workflows, baseline, implementation, and hosting are not yet defined or validated. The external partner-led Financial Automation Discovery Pilot was formally initiated but is **deferred, not cancelled**, until internal validation is complete and all existing safety, actionable-human-notification, privacy, and data-flow gates pass. It has no first-session date or result; the planned external pilot remains Odoo Online. The existing live chatbot on Frank remains generic lead capture and is not this pilot. See `../../../kb-solution/docs/strategy/03-automation-center-solution.md` for the sequence and gates.

**Internal Consultancy Automation (planned; not an external offer):** identify an appropriate workflow within Inteligente's own consultancy operations, establish a baseline and outcome measures, then validate the effect of a bounded automation before any wider external Financial Automation pilot. Do not claim that an internal workflow, system, host, or efficiency gain has already been selected or implemented.

**Delivery flow:**
1. **Deferred partner-led Financial Automation Discovery Pilot and ROI screening (Odoo Online)** — only after Consultancy Automation has been internally validated and the existing safety/data-flow gates pass, the Financial partner acts as customer and the Operations partner validates the method. A structured, deliverable-first interview identifies the output, owner, recipient, frequency, quality criteria, effort, exceptions, review, and delivery. It may collect only aggregated metrics from the Financial partner's own firm after written authorization and cloud/privacy review; no credentials, raw client records, or third-party confidential data.
2. **Escalation-gated analyst and screening output** — the intended Odoo AI Agent (GPT-4o is founder-reported; verify in the pilot database) analyzes one minimized question/answer only after explicit escalation and suggests a clarifying follow-up. Odoo 19 documentation says an AI Agent assigned to a Live Chat channel rule takes priority over a scripted chatbot when both are assigned; test actual handoff, prompt context, transcript/log retention, and provider handling before automatic invocation. If that boundary cannot be demonstrated, the founder triggers the analyst manually. The process produces a draft automation plan plus deterministic, evidence-graded ROI range and assumptions for founder review—not a guaranteed or investment-grade ROI promise.
3. **Pilot decision** — classify the opportunity as Stop, Measure (run a short measurement sprint), Prototype, or Pilot. Pilot success requires a validated interview/ROI workflow plus a documented buying decision or qualified paid-pilot offer; payment is a separate milestone.
4. **Build** — after a signed engagement, workflow automation using n8n/Make/Zapier plus LLM APIs, OCR/document extraction where needed, and integration with the client's accounting/CRM/ERP systems.
5. **Security, testing, documentation and training** delivered before go-live.
6. **Deployment and pilot monitoring** — matched pre/post evidence: eligible/excluded volume, active time, errors, human overrides, adoption, and actual expenditure/revenue consequence.
7. **Ongoing monitoring/support retainer** as an optional recurring service.

**Later stages:** after successful method validation, host Odoo and a local AI model on Frank (TRL4) for the local MVP, subject to capacity and isolation checks. Deploy the first paying customer's dedicated account/agent on SolarSeed TRL5 only after readiness and customer-isolation checks. Odoo Online is cloud-hosted and is not local-only.

**Example service scope** (from market-benchmark research, see `../../../kb-revenue-streams/docs/model/07-revenue-streams.md` for full pricing):
- Email triage, drafting, filing, follow-ups (basic to advanced "agent" tiers).
- Accounting/bookkeeping and document/receipt automation (OCR, expense classification, reconciliation, accountant handoff).
- Combined multi-workflow packages, which benefit from shared infrastructure economies of scale.
- Ongoing monitoring/support retainer.

## Decisions / Rules
- Do not promise ROI or implementation feasibility during the discovery interview itself; every ROI figure must show its evidence grade and be labeled screening vs. validated (post-pilot).
- Keep the Odoo Online partner pilot restricted to authorized aggregated metrics from the Financial partner's own firm; do not treat it as local-only or as permission to use third-party data.
- Do not enable automatic AI-agent handoff until the scripted-first flow, actual model context, transcript/log retention, and provider handling are verified in the pilot database. The founder-triggered analyst is the fallback.
- The founder reviews the draft automation plan and evidence-graded ROI range/assumptions before presenting them as a proposal.
- Automation Center may quote using the documented market-benchmark pricing (see revenue-streams); Human Center's services must not (their pricing is undocumented, a separate gap).
- Consultancy Automation is an internal-first validation use case; its workflows, baseline, and hosting remain open until explicitly defined. Do not use external-client data or claim a result before an appropriately authorized internal test.
- Do not begin any external Financial Automation pilot until Consultancy Automation is validated and the already-defined safety, human-notification, privacy, data-flow, and authorization gates pass. The partner pilot is deferred, not cancelled.
- Route between Human Center and Automation Center by client need in either direction; treat the two Human-to-Automation interest reports as unqualified and do not claim reverse-direction conversion.
- Regulated or financial-advisory clients trigger the compliance/data-owner discovery route and heightened controls (human approval, audit logging, DPA, EU data residency) before any pilot proceeds; this heightened posture is documented in full under Financial Automation, see `04-financial-automation.md`.
- Do not position Automation Center as a "private equity AI solution" merely because a client's own clients are investment funds; pricing and scope target the solo consultant/small firm buyer, not the fund itself.

## Evidence
- `../../../../Resources/Documents/Research/HumanCenter.Pricing.md` — the service-scope description is a reasonable synthesis of real agency offerings; the market-benchmark **pricing** is unverified (self-described AI-chat estimate), partially corroborated by independent Sept 2026 research (see `../../../kb-revenue-streams/docs/model/07-revenue-streams.md` for the full corroboration note) — treat as directionally plausible, not verified official pricing.
- `../../../../Resources/Documents/Research/Interview Playbook  Financial-Advisory Automation Discovery.md` — verified, original three-role discovery design.
- `../../../../Resources/Documents/Research/Chatbot-Led Automation Discovery  Critique and Revised Interview Playbook.md` — verified, chatbot-safe redesign (atomic questions, consent, bias controls, escalation).
- `../../../../Resources/Documents/Research/Critical Review and Revised Chatbot ROI Interview Playbook.md` — verified, screening-vs-investment separation, evidence grading, benefit classification.
- [Odoo 19 AI live chat](https://www.odoo.com/documentation/19.0/applications/productivity/ai/live-chat.html) — documents AI-agent priority when both an agent and a scripted chatbot are assigned to a channel.
- [Odoo 19 scripted chatbots](https://www.odoo.com/documentation/19.0/applications/websites/livechat/chatbots.html) — documents structured scripts and storage of free-input answers in chat transcripts.
- **Founder-reported anonymized cross-sell outcome follow-up (2026-09-29)** — primary, retrospective report that two Human Center client accounts expressed Automation Center interest; requirements, orders, delivery, and payment have not been confirmed.
- **Founder-defined Consultancy Automation internal-first and bidirectional-routing decisions (2026-09-29)** — primary business-model decisions only; internal validation and cross-line conversion have not been demonstrated.

## Cross-Domain Links
- Related domains: `kb-solution`, `kb-customers`, `kb-key-activities`, `kb-revenue-streams`, `kb-unfair-advantage`
- Related documents: `../../../kb-solution/docs/strategy/03-automation-center-solution.md`, `../../../kb-customers/docs/gtm/04-automation-center-segments.md`, `../../../kb-key-activities/docs/execution/05-automation-center-key-activities.md`, `../../../kb-revenue-streams/docs/model/07-revenue-streams.md`, `04-financial-automation.md`

## Open Actions
- Define, baseline, run, and evaluate the internal Consultancy Automation use case before any external Financial Automation pilot; workflow and host remain undecided, owner: Founder/Consultant, see `../../../../tasks/backlog.md` HC-021.
- Resume the deferred Odoo Online partner-pilot preparation only after Consultancy Automation is validated and the existing safety/data-flow gates pass; no session date or result is confirmed yet, owner: Founder/Consultant, see `../../../../tasks/backlog.md` HC-009 and HC-016.
- Verify the Odoo Online scripted-chatbot-first/AI-agent escalation and data-handling boundary; use founder-triggered minimized Q/A analysis if automatic handoff cannot be demonstrated, owner: Founder/Consultant.
- Validate the documented benchmark pricing against the first signed Automation Center client, owner: Founder/Consultant.
- After successful pilot validation, scope the local Odoo/local-model MVP on Frank and verify capacity, ingress, tenancy, and isolation before deployment, owner: Founder/Consultant.
- Qualify and track the two Human-Center-originating Automation Center interest signals through scope, proposal, order, delivery, and outcome; keep them separate from contracted sales, owner: Founder/Consultant.
- Track need-based referral and conversion evidence in both directions between Human Center and Automation Center; do not infer conversion from the routing strategy, owner: Founder/Consultant, see `../../../kb-metrics/docs/financial/09-key-metrics.md`.
