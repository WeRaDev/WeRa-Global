---
metadata:
  primary_domain: channels
  secondary_domains: [customers, solution, unfair-advantage]
  owner_role: Founder/Consultant
  temporal_scope: current
  evidence_status: hypothesis
  last_reviewed_at: 2026-09-29
  next_review_due: 2026-12-29
  provenance:
    actor: agent-warp
    source: "Inteligente/Resources/Documents/Research/Chatbot-Led Automation Discovery  Critique and Revised Interview Playbook.md; Inteligente/Resources/Documents/Research/Critical Review and Revised Chatbot ROI Interview Playbook.md; founder-approved Discovery Pilot decision; founder-defined Consultancy Automation internal-first decision (2026-09-29); Odoo 19.0 AI and Live Chat documentation"
    confidence: medium
    review_status: draft
---
# Automation Center Channels

## Purpose
Document Automation Center's acquisition/qualification channel mechanics.

## Scope
- In scope: the partner-network channel, the partner-led Odoo Online Discovery Pilot, and the gated transition from the existing generic lead-capture chatbot to the governed interview.
- Out of scope: Human Center's Shrinking AI booking-page channel (`11-channels.md`); paid acquisition/media strategy; a future public/self-service chatbot deployment (not the current plan).

## Current State
**Decided (Sept 2026): acquisition channel and qualification tool are separate and must be tracked separately. The external Financial Automation Discovery Pilot was formally initiated but is deferred, not cancelled, until internal Consultancy Automation is validated and its existing safety/data-flow gates pass; no first session or result is confirmed.**

1. **Pilot partners and network channel.** The Financial partner, at a small financial-advisory firm, acts as the pilot customer using only aggregated metrics from their own firm after written authorization and cloud/privacy review. The Operations partner, who works within a network of financial companies, validates the interview method. After pilot validation, the Operations partner is expected to share the chatbot with its network of small financial firms; this is a planned distribution step, not yet evidence of conversion or customer adoption.
2. **Qualification tool.** Stage 1 is planned on Odoo Online with a structured, deliverable-first scripted interview and an Odoo AI Agent (GPT-4o is founder-reported and must be verified in the pilot database). The AI analyst should run only after explicit escalation, analyzing one minimized question/answer to suggest a clarifying follow-up. Odoo's documentation says an AI Agent assigned to a Live Chat channel rule takes priority over a scripted chatbot when both are assigned; it does not establish that a script can defer agent invocation until a chosen step or specify the exact prompt payload and retention. Test the live behavior before automatic handoff; otherwise the founder triggers the analyst manually. Do not collect credentials, raw client records, or third-party confidential data. Odoo Online is cloud-hosted, not local-only.

The existing Odoo chatbot at `www.inteligente.site` was previously documented as hosted on Frank and performing generic livechat/lead routing; the relationship between that deployment, the public site, and the founder-confirmed Odoo Online database remains unresolved. Do not assume they are the same deployment.

The 25 September handoff separately records an always-enabled Human Center `/discovery-interview` rule assigned to Agent 5, with CRM Create/Get Lead tools available. Its public reachability and actual CRM side effects were not tested. It is separate from archived pilot chatbot 4 and is pending a read-only/synthetic-only Comet audit at `../../../../tasks/comet-audit-discovery-interview-agent5.md`. The archived draft's synthetic safety tests failed, and its compliance/data-owner referral sent no human notification or transfer, so no partner session or public sharing is cleared. See `../../../kb-key-resources/docs/architecture/06-automation-center-key-resources.md` for the staged hosting and data-flow gates.

**Need-based cross-line referrals (decided, Sept 2026): bidirectional.** Refer Human Center clients to Automation Center when a defined organizational process needs automation; refer Automation Center clients to Shrinking AI for ineffective existing AI use or to Expanding Human when the AI opportunity itself is unclear. This is a routing strategy, not a conversion result. The two reported Human-to-Automation interest signals are unqualified; no Automation-Center-to-Human conversion is recorded (see `../../../kb-value-proposition/docs/products/03-automation-center.md`).

The first cohort is partner-led and non-public. The Operations partner may share the chatbot with its network only after the methodology is validated; that planned share is not permission to expose other firms' data or proof that a public/self-service model is ready.

Secondary channel candidates (accounting-firm/bookkeeper referrals, industry associations, cold outbound, paid media — see `../../../kb-key-partners/docs/partnerships/06-key-partners.md`) are **not currently pursued**; they remain candidates for a later phase once the warm-network channel's conversion is evidenced.

## Decisions / Rules
- Restrict the initial Odoo Online pilot to the Financial partner's own aggregated metrics after written authorization and cloud/privacy review; exclude credentials, raw client records, and third-party confidential data.
- Do not begin any external pilot until Consultancy Automation is internally validated and the existing safety, actionable-human-notification, privacy, data-flow, and authorization gates pass; the partner pilot remains deferred, not cancelled.
- Do not enable automatic AI-agent invocation until a live test confirms the scripted-chatbot-first sequence, actual context sent, transcript/log retention, and provider handling. Use founder-triggered, minimized Q/A analysis if the native handoff cannot demonstrate the boundary.
- Keep archived pilot chatbot 4, the existing `/discovery-interview` route/Agent 5, and the previously documented Frank generic bot distinct. The site/database/Frank topology is unresolved; the route audit and pilot safety gates are both pending. The Operations partner's network distribution is gated on validation and does not imply completed validation or public launch.
- The chatbot must never be presented as providing a guaranteed ROI or binding commercial commitment; every session output is a screening decision, not a signed proposal.
- Treat the personal/professional network (the two partner relationships) as the sole active acquisition channel until it is evidenced to convert (or fail to convert) with the named prospects; do not simultaneously stand up other channels before that evidence exists.
- Automation Center's channel and Human Center's Shrinking AI booking-page channel may share the same top-of-funnel website traffic in the longer term, but must diverge into distinct qualification flows once a visitor's product interest is identified — not yet relevant while the channel is founder-network-only.
- Route across Human Center and Automation Center according to need in either direction; do not infer an order or conversion from a referral strategy or stated interest.

## Evidence
- `../../../../Resources/Documents/Research/Chatbot-Led Automation Discovery  Critique and Revised Interview Playbook.md` — verified, evidences that conversational interview systems can elicit richer responses than web forms, with documented risks (over-probing, bias) that any future public channel must control for.
- `../../../../Resources/Documents/Research/Critical Review and Revised Chatbot ROI Interview Playbook.md` — verified, defines the screening-decision output shown to a prospect.
- `../../../../Resources/Documents/Research/Financial Automation/financial_advisory_automation_mvp.xlsx` — verified, an implementation-ready MVP spec (chatbot question script, data model, ROI model, controls/scorecard, phased implementation plan); see `../../../kb-key-resources/docs/architecture/06-automation-center-key-resources.md` for the staged Odoo deployment.
- **Founder-reported named prospect pipeline (Sept 2026)** — founder self-report, treated as reachability evidence only (not independently verified); mostly small advisory/consultancy firms with employees, most likely sourced from the two partner relationships (see `../../../kb-key-partners/docs/partnerships/06-key-partners.md`). Conversion remains completely unevidenced.
- [Odoo 19 AI live chat](https://www.odoo.com/documentation/19.0/applications/productivity/ai/live-chat.html) — documents channel-rule assignment and AI-agent priority over a scripted chatbot when both are assigned.

## Cross-Domain Links
- Related domains: `kb-customers`, `kb-solution`, `kb-unfair-advantage`, `kb-key-partners`, `kb-key-resources`
- Related documents: `../../../kb-customers/docs/gtm/04-automation-center-segments.md`, `../../../kb-customers/docs/gtm/05-financial-automation-segments.md`, `../../../kb-solution/docs/strategy/03-automation-center-solution.md`, `../../../kb-unfair-advantage/docs/strategy/11-automation-center-unfair-advantage.md`, `../../../kb-key-resources/docs/architecture/06-automation-center-key-resources.md`

## Open Actions
- Keep the Odoo Online partner-pilot session deferred until Consultancy Automation is validated and the failed safety gates, actionable human notification, data handling, and required approval evidence are resolved; no first session/result is confirmed yet, owner: Founder/Consultant, see `../../../../tasks/backlog.md` HC-009, HC-016, and HC-021.
- Verify scripted-first AI escalation and data handling in the pilot database; if it cannot be demonstrated, use founder-triggered analyst questions, owner: Founder/Consultant.
- Complete the separate `/discovery-interview`/Agent 5 audit of logged-out reachability, CRM effects, safety behavior, human notification, and privacy. Do not create a production lead or send production test prompts; owner: Founder/Consultant.
- After internal Consultancy Automation validation and then external interview/ROI workflow validation, coordinate the Operations partner's planned sharing with its network of small financial firms; track reach separately from completed interviews and conversion, owner: Founder/Consultant.
- Finalize partner compensation only after written agreement, direct-cost basis, allocation, percentage, cap/duration, conflict, tax, and legal review; reconcile the free-discovery decision first (see `../../../kb-key-partners/docs/partnerships/06-key-partners.md` and `../../../kb-revenue-streams/docs/model/07-revenue-streams.md`), owner: Founder/Consultant.
