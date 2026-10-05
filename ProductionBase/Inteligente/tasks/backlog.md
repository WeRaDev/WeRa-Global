# Inteligente backlog

## HC-001 Build the qualification gate and booking page
- Problem: No lead-qualification gate or booking page exists yet, so unqualified calls waste founder time (a named operational risk in research).
- Scope: Build a booking page following the boutique-agency benchmark pattern (single embedded scheduler, one CTA, 2-3 question qualification micro-form) per `KnowledgeBase/kb-channels/docs/gtm/11-channels.md`. Include explicit disqualification copy for wrong-fit visitors (see `KnowledgeBase/kb-unfair-advantage/docs/strategy/10-unfair-advantage.md`).
- Acceptance: booking page live at `www.inteligente.site`, qualification form in place, disqualification copy reviewed against the AI Jungle benchmark pattern.

## HC-002 Choose booking/scheduling stack (ADR)
- Problem: No hosting/scheduler stack decision has been recorded.
- Scope: Define minimal site scope (positioning, Shrinking AI services, free-call booking, contact) and choose hosting/scheduler stack; record the decision as an ADR.
- Acceptance: `docs/adr/000X-site-stack.md` exists and the site is reachable at `www.inteligente.site`.

## HC-003 Set and document Shrinking AI's paid-session price
- Problem: Shrinking AI's core paid-session price was undocumented anywhere in research. **Resolved (Sept 2026): €50/60-min, established from the first 2 real paid engagements** (self-published writer, self-employed tour guide) — see `KnowledgeBase/kb-revenue-streams/docs/model/07-revenue-streams.md`.
- Scope (remaining): treat €50/60-min as an introductory rate; test price elasticity once more sessions are booked before deciding whether to hold, raise, or tier the price.
- Acceptance: `kb-revenue-streams/docs/model/07-revenue-streams.md` updated with a documented session price and `evidence_status: verified` — **done for the initial price**; elasticity testing remains open.

## HC-004 Confirm commercial-registry number and formalize DPA
- Problem: The legal entity (Inteligente Razão — Unipessoal LDA) is confirmed. **VAT/NIF confirmed (Sept 2026): PT514477580.** The DPA template is not yet built (see `kb-governance/docs/legal/11-legal-structure.md`).
- Scope (remaining): finalize the sub-processor list (LLM API provider, n8n/Make/Zapier, EU hosting), adapt a GDPR Art. 28(3)-compliant DPA template to that list and to the confirmed VAT/entity details, and get it reviewed by counsel.
- Acceptance: `kb-governance/docs/legal/11-legal-structure.md` Open Actions item on VAT closed (**done**); DPA template exists (**open**).

## HC-005 Produce first proof assets
- Problem: No proof assets exist yet to support the "demonstrated not claimed" positioning (see `kb-unfair-advantage/docs/strategy/10-unfair-advantage.md` and `kb-metrics/docs/financial/09-key-metrics.md`). **Progress (Sept 2026): 2 of 10 sessions completed** (self-published writer, self-employed tour guide).
- Scope: Deliver 8+ more completed paid sessions, write up 3 client cases (pending consent from the 2 completed clients), and assemble a consent evidence pack authorizing their use.
- Acceptance: 3 case write-ups published (post-consent) and referenced from the site and `kb-metrics/`.

## HC-006 Build an on-site RCGFC preview
- Problem: The RCGFC framework (Role, Context, Goal, Format, Constraints) is Shrinking AI's core differentiator but is not yet demonstrated anywhere client-facing.
- Scope: Design a short, self-serve RCGFC preview/interactive element for the site so prospects can experience the framework before booking.
- Acceptance: RCGFC preview live on `www.inteligente.site`, linked from the booking page.

## HC-007 Keep Human Center and Automation Center services strictly separated
- Problem: Shrinking AI (Human Center diagnostic), Expanding Human (Human Center exploration; hypothesis-stage with one paid observation), and Automation Center/Financial Automation (build-and-implement) have distinct needs and could be confused if their positioning is blended.
- Scope: Keep product identities, primary navigation, tones, and CTAs distinct while allowing need-based referrals between Human Center and Automation Center in either direction.
- Acceptance: Site navigation and service guidance preserve distinct offers and document need-based routing without implying that referrals or interest signals are conversions.

## HC-008 Validate problem framing with real discovery calls
- Problem: Problem/solution framing in `KnowledgeBase/kb-problem/` and `kb-solution/` is currently validated only via desk research (industry stats, competitive analysis), not real client conversations.
- Scope: Run 3-5 discovery calls with the primary ICP segment (A4: AI-frustrated consultants/freelancers); capture findings as evidence in the KB.
- Acceptance: `kb-problem` and `kb-customers` documents cite findings from at least 3 real discovery calls alongside the existing desk research.

## HC-009 Run the deferred partner-led Financial Automation Discovery Pilot
- Problem: Automation Center's discovery-and-ROI methodology (`KnowledgeBase/kb-solution/docs/strategy/03-automation-center-solution.md`) is designed, but the partner pilot has not yet produced a confirmed session or result.
- **Status (29 Sept 2026): DEFERRED, not cancelled; BLOCKED.** No partner session or result is confirmed. Consultancy Automation internal validation (HC-021) must be completed first, and HC-016's existing safety/data-flow gates must pass before any external session. The founder confirmed the authorized external-pilot database runs on Odoo Online. Separate synthetic-only draft chatbot 4 is archived/inactive after sensitive-input, legal/tax/investment-advice, and guaranteed-ROI stop tests failed. Region/provider/runtime details remain unresolved. The pilot may use only authorized aggregated metrics from the Financial partner's own firm; no credentials, raw client records, or third-party confidential data. Use the workbook at `Resources/Documents/Research/Financial Automation/financial_advisory_automation_mvp.xlsx`.
- Scope: Only after HC-021 internal validation and HC-016's external safety/data-flow gates pass, run the partner-led deliverable-first pilot, retain evidence for authorization and data scope, validate interview questions and evidence-graded deterministic ROI/plan output with the Operations partner, and capture the Financial partner's buying decision or qualified paid-pilot offer. The founder reviews the draft plan/ROI before it is presented.
- Acceptance: A dated pilot record links to completed internal Consultancy Automation validation; contains authorization/data scope, passing isolated synthetic hard-stop and human-notification tests, verified data handling, validated interview/ROI workflow and corrections, founder-reviewed draft output, Operations partner validation, and the Financial partner's documented buying decision or qualified paid-pilot offer. Payment is tracked as a separate milestone.

## HC-016 Verify Odoo Online handoff, data flow, and safety gates for the partner pilot
- Problem: The 25 Sept synthetic test of pilot chatbot 4 failed the sensitive-input, legal/tax/investment-advice, and guaranteed-ROI stops. Its compliance/data-owner referral stopped intake but delivered no human notification or transfer. The draft is archived; Odoo 19 documentation also says an AI Agent assigned to a Live Chat channel rule takes priority over a scripted chatbot when both are assigned. Exact payload, provider processing, and retention remain unknown, and Odoo Online does not support custom modules.
- Scope: In an isolated, non-public test configuration with synthetic data, determine whether an authorized runtime can stop intake and further tools on sensitive/advice/ROI/consent/incident triggers, prevent downstream CRM/email/summary copies where controllable, make no substantive advice/ROI claim, and deliver a verified actionable human transfer/notification. Inspect pilot channel rules, scripts, Agent prompts/topics/tools, configured and actual model/provider, API-key mode (without viewing keys), region, context, transcript/log access and retention, and applicable privacy terms. Test ordinary scripted behavior and permitted escalation context. Do not test by creating production leads or sending real partner data.
- Acceptance: Document pass/fail/unverified evidence for each trigger, side effect, notification delivery, routing, model/provider, transmitted context, storage/access/retention, and privacy item. A terminal chat message or prompt instruction alone is not a pass. Keep the bot archived/out of live use if any safety or data boundary fails or cannot be verified; use a founder-triggered fallback only after its own data handling and human process are approved.

## HC-020 Audit existing `/discovery-interview` route and Agent 5 (Comet; audit only)
- Problem: The 25 Sept handoff records an always-enabled Human Center `/discovery-interview` rule assigned to Agent 5, with CRM Create/Get Lead tools available. Public reachability, actual tool/CRM side effects, safety behavior, human notification, and privacy are untested. This route is separate from archived pilot chatbot 4 and from the previously documented Frank generic bot; their hosting relationship is unresolved.
- Scope: Use `tasks/comet-audit-discovery-interview-agent5.md` for a read-only browser audit of the founder-confirmed Odoo Online target. Check logged-out reachability without sending production prompts; inspect route, Agent 5's prompts/topics/tools, CRM capability/effects, privacy settings, and available audit metadata. Test trigger and notification behavior only in an isolated non-production environment with synthetic data and no production tools. Do not change configuration, publish/disable routes, create/update leads, send email, or expose secrets/personal data.
- Acceptance: Report PASS/FAIL/UNVERIFIED/BLOCKED by audit area, distinguishing configuration from runtime evidence. Verify a real test notification delivery or mark human handoff unverified; merely ending the chat fails. No production side effects occur. If route safety, notification, or data handling fails or remains unverified, recommend no live use and escalate to the founder without changing the route.

## HC-010 Validate the pilot before operational-partner network distribution
- Problem: Sharing the chatbot with the Operations partner's network of small financial firms is intended only after the interview methodology is validated; the pilot has not yet produced results, and the Odoo Online AI handoff/data boundary remains gated on HC-016.
- Scope: After HC-021 internal validation and HC-009, review method validation, consent/authorization, sensitive-data interruption, evidence grading, founder review, and commercial outcome. Confirm pilot controls under HC-016 and resolve the separate existing-route audit under HC-020 before any network distribution. If native escalation remains unavailable, limit work to a founder-supervised workflow using the manual analyst fallback only after its data handling is approved; decide separately whether/when to offer public self-service.
- Acceptance: A documented go/no-go decision approves partner-network sharing only after interview/ROI validation, safety/data-flow tests, and the route audit, with permitted audience, data scope, human oversight, and unresolved limits recorded. Any broader self-service launch requires a separate decision.

## HC-015 Build and validate the Frank TRL4 local MVP
- Problem: Stage 2 is a local Odoo/local-model MVP on Frank after partner-pilot validation; the existing generic chatbot on Frank does not validate capacity, tenancy, or isolation for this service.
- Scope: After HC-009 pilot validation and HC-016's Odoo Online data-flow decision, verify Frank's capacity, ingress, database/instance tenancy, access controls, backups, rollback, and outbound model connections. Then deploy the local MVP with a local AI model and test it using synthetic or otherwise approved non-sensitive data.
- Acceptance: A pre-deployment review records the readiness/isolation checks; the MVP passes the agreed functional and safety checks, including human escalation and rollback, without exposing pilot or customer data; close the corresponding Open Action in `KnowledgeBase/kb-key-resources/docs/architecture/06-automation-center-key-resources.md`.

## HC-011 Validate Automation Center's benchmark pricing with a first signed client
- Problem: Automation Center's pricing (`KnowledgeBase/kb-revenue-streams/docs/model/07-revenue-streams.md`) is market-benchmark-derived, not yet tested against a real Inteligente client.
- Scope: Build a quantified cost model (`kb-cost-structure/`) and quote the documented benchmark pricing to the first real Automation Center prospect.
- Acceptance: `KnowledgeBase/kb-revenue-streams/docs/model/07-revenue-streams.md` updated with a signed-client price point and `evidence_status: verified` for Automation Center pricing.

## HC-012 Financial-advisory compliance review for Financial Automation
- Problem: Financial Automation's target audience includes financial-advisory and investment-fund-adjacent clients (`KnowledgeBase/kb-customers/docs/gtm/05-financial-automation-segments.md`), which may trigger sector-specific supervision/recordkeeping obligations not yet reviewed by counsel.
- Scope: Before onboarding any regulated-sector client, confirm the applicable regulatory perimeter and required controls with counsel or a qualified compliance reviewer, per the compliance/data-owner discovery route.
- Acceptance: `KnowledgeBase/kb-governance/docs/legal/11-legal-structure.md` Open Actions item on regulatory-perimeter confirmation closed for the first regulated-sector client.

## HC-013 Validate Expanding Human positioning and audience
- Problem: Expanding Human (Human Center's service for exploring where AI can support goals, problems, or ambitions) has one founder-reported €50/60-minute paid observation, but its audience, willingness to pay, and repeatable delivery method remain unvalidated (`KnowledgeBase/kb-value-proposition/docs/products/05-expanding-human.md`, `KnowledgeBase/kb-customers/docs/gtm/06-expanding-human-segments.md`).
- Scope: Use additional delivery observations, discovery interviews, and/or desk research to assess which individual or organizational audience has a recurring need; keep the observed transaction distinct from a standard price or general market validation.
- Acceptance: The two Expanding Human docs accurately separate founder-reported evidence from hypotheses, and any narrower audience, price, or delivery-method claim is supported by new cited evidence; do not promote the overall service to verified from the single paid case.

## HC-014 Clarify Automation Center vs. Financial Automation scope boundary
- Problem: Automation Center (the product line) and Financial Automation (its first named service) currently share the same generic discovery methodology and benchmark pricing; it is not yet decided whether Automation Center will host additional named services beyond Financial Automation, or whether Financial Automation should diverge with its own pricing/methodology over time.
- Scope: Decide whether to keep a single generic methodology/pricing model across all Automation Center services, or let Financial Automation (and any future named services) diverge; document the decision as an ADR.
- Acceptance: `docs/adr/000X-automation-center-service-scope.md` exists recording the decision; `KnowledgeBase/kb-value-proposition/docs/products/03-automation-center.md` and `04-financial-automation.md` updated to reflect it if needed.

## HC-017 Track real-resource-base and bidirectional referral decisions through to evidence
- Problem: The Sept 2026 correction round recorded the actual current resource base (1 paid employee, 2 unpaid partner relationships, and 2 servers; see `KnowledgeBase/kb-cost-structure/docs/model/08-cost-structure.md`) and established need-based referrals in both directions between Human Center and Automation Center. The routing is a strategy, not demonstrated conversion; two Human-to-Automation interest signals remain unqualified, and no reverse-direction conversion is reported.
- Scope: As Automation Center engages prospects, record whether (a) the resource base holds without unjustified acquisitions and (b) need-based referrals produce qualified opportunities, orders, deliveries, and outcomes in either direction. Keep stated interest, proposals, signed orders, collected revenue, and delivered Human Center services distinct.
- Acceptance: `kb-cost-structure/docs/model/08-cost-structure.md`, `kb-value-proposition/docs/company/01-company-overview.md`, and the relevant service/metrics docs are updated with actual evidence after meaningful opportunities, or explicitly retain the routing and resource assumptions as unvalidated when no outcome exists.

## HC-018 Deploy the first paying customer on SolarSeed TRL5
- Problem: Stage 3 is the first paying customer's dedicated account/agent on SolarSeed TRL5; the host's intended role does not itself establish readiness or customer-specific isolation.
- Scope: After the partner pilot is validated, HC-015's Frank local MVP is implemented and validated, and a paying customer is signed, verify SolarSeed host readiness, tenant/account separation, access controls, backups, rollback, and incident handling. Obtain written authorization and the required DPA before deploying the dedicated account/agent; keep authorization evidence in an approved secure location, not in the repository.
- Acceptance: The customer-specific account/agent is deployed only after a documented readiness/isolation review and confirmed authorization/DPA; access, backup, rollback, and incident controls are tested, and the corresponding Open Action in `KnowledgeBase/kb-key-resources/docs/architecture/06-automation-center-key-resources.md` is closed.

## HC-019 Resolve partner compensation and discovery-fee terms
- Problem: The current free-discovery decision conflicts with a proposed partner share of a one-time discovery fee, and the broader partner revenue-share proposal is not approved.
- Scope: Decide whether Automation Center discovery remains free or becomes fee-bearing; if partner compensation proceeds, document percentages, allocation, attribution, collected-revenue and direct-cost basis, maintenance-period duration/cap, and obtain required employer/conflict, tax, and legal review. Keep Shrinking AI's separate paid diagnostic decision distinct.
- Acceptance: A written decision resolves the free-versus-paid discovery conflict and approves or rejects the complete partner-compensation terms; `KnowledgeBase/kb-key-partners/docs/partnerships/06-key-partners.md`, `KnowledgeBase/kb-revenue-streams/docs/model/07-revenue-streams.md`, and any affected channel guidance agree. No fee or share is promised before approval.

## HC-021 Validate internal Consultancy Automation before external Financial Automation
- Problem: The external partner-led Financial Automation Discovery Pilot is deferred until Inteligente has validated Consultancy Automation on its own consultancy operations; no internal workflow, baseline, host, or outcome is yet defined.
- Scope: Select a bounded internal workflow; document its owner, data boundary, and any required authorization; define a comparable baseline and workflow-appropriate efficiency/outcome measures; decide whether an implementation or host is needed without assuming Frank, Odoo Online, or SolarSeed; run the internal validation and record results, limitations, and a go/no-go decision.
- Acceptance: A dated internal validation record documents the selected workflow, scope/data boundary, baseline, measures, system/hosting used (or why none was needed), pre/post results, limitations, and explicit validation decision. No external Financial Automation pilot begins until this record supports internal validation and HC-016's existing external safety/data-flow gates pass; the partner pilot remains deferred, not cancelled.
