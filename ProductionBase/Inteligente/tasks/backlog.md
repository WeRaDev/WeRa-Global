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
- Problem: Shrinking AI (Human Center, B2B diagnostic), Empowering Human (Human Center, B2C, hypothesis-stage), and Automation Center/Financial Automation (B2B build-and-implement) risk brand collision if not deliberately separated.
- Scope: When building site navigation, tone, and CTAs, ensure the services never share a page, CTA, or messaging tone; document the separation decision as an ADR once Empowering Human work begins in earnest.
- Acceptance: Site navigation and any Empowering Human planning docs show clear separation from Shrinking AI and Automation Center/Financial Automation.

## HC-008 Validate problem framing with real discovery calls
- Problem: Problem/solution framing in `KnowledgeBase/kb-problem/` and `kb-solution/` is currently validated only via desk research (industry stats, competitive analysis), not real client conversations.
- Scope: Run 3-5 discovery calls with the primary ICP segment (A4: AI-frustrated consultants/freelancers); capture findings as evidence in the KB.
- Acceptance: `kb-problem` and `kb-customers` documents cite findings from at least 3 real discovery calls alongside the existing desk research.

## HC-009 Run the partner-led Financial Automation Discovery Pilot
- Problem: Automation Center's discovery-and-ROI methodology (`KnowledgeBase/kb-solution/docs/strategy/03-automation-center-solution.md`) is designed, but the partner pilot has not yet produced a confirmed session or result.
- **Status (Sept 2026): formally initiated, not yet run.** The Financial partner acts as the customer using authorized aggregated metrics from their own firm; the Operations partner validates the method. Stage 1 is planned on Odoo Online, not the existing generic lead-capture bot on Frank. No first-session date or result is confirmed. The pilot must not include credentials, raw client records, or third-party confidential data. Use the workbook at `Resources/Documents/Research/Financial Automation/financial_advisory_automation_mvp.xlsx`.
- Scope: Run the partner-led deliverable-first pilot, document authorization and data scope, validate interview questions and evidence-graded deterministic ROI/plan output with the Operations partner, and capture the Financial partner's buying decision or qualified paid-pilot offer. The founder reviews the draft plan/ROI before it is presented.
- Acceptance: A dated pilot record contains the authorized data scope, validated interview/ROI workflow and corrections, founder-reviewed draft output, Operations partner validation, and the Financial partner's documented buying decision or qualified paid-pilot offer. Payment is tracked as a separate milestone.

## HC-016 Verify Odoo Online AI-agent handoff and data flow for the partner pilot
- Problem: The existing live Odoo chatbot on Frank is generic lead capture. Odoo 19 documentation says an AI Agent assigned to a Live Chat channel rule takes priority over a scripted chatbot when both are assigned, so the intended scripted-interview-first, escalation-only analyst flow cannot be assumed. The docs do not specify this deployment's exact prompt payload or retention, and Odoo Online does not support custom modules.
- Scope: In the actual Odoo Online pilot database, inspect channel rules, chatbot script, AI Agent prompts/topics/tools, GPT-4o/provider and API-key mode, database region, transcript/log storage and retention, and applicable privacy terms. Test whether the script completes its ordinary questions without invoking the agent and whether an explicit escalation sends only the permitted minimized question/answer. Use the script/data model in `Resources/Documents/Research/Financial Automation/financial_advisory_automation_mvp.xlsx`.
- Acceptance: Record observed routing, model/provider, transmitted context, storage/access/retention, and privacy terms. Enable automatic handoff only if live tests demonstrate the scripted-first boundary and permitted context. If they do not, keep automatic invocation disabled and use a founder-triggered, minimized single-question/answer prompt for the partner pilot; record that as the accepted fallback.

## HC-010 Validate the pilot before operational-partner network distribution
- Problem: Sharing the chatbot with the Operations partner's network of small financial firms is intended only after the interview methodology is validated; the pilot has not yet produced results, and the Odoo Online AI handoff/data boundary remains gated on HC-016.
- Scope: After HC-009, review method validation, consent/authorization, sensitive-data interruption, evidence grading, founder review, and commercial outcome. Confirm the Odoo Online handoff is safe under HC-016. If native escalation remains unavailable, limit distribution to a founder-supervised workflow using the manual analyst fallback; decide separately whether/when to offer public self-service.
- Acceptance: A documented go/no-go decision approves partner-network sharing only after interview/ROI validation and safety/data-flow tests, with the permitted audience, data scope, human oversight, and unresolved limits recorded. Any broader self-service launch requires a separate decision.

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

## HC-013 Research and validate Empowering Human
- Problem: Empowering Human (Human Center's second service, discovery of suitable AI applications for business/personal use) currently has no dedicated research; its value proposition and segments are hypothesis-stage only (`KnowledgeBase/kb-value-proposition/docs/products/05-empowering-human.md`, `KnowledgeBase/kb-customers/docs/gtm/06-empowering-human-segments.md`).
- Scope: Commission desk research and/or discovery interviews to validate Empowering Human's target audience (B2B, B2C, or both), competitive landscape, and a candidate delivery methodology.
- Acceptance: `05-empowering-human.md` and `06-empowering-human-segments.md` updated to `evidence_status: verified` (or a more mature hypothesis) with cited sources.

## HC-014 Clarify Automation Center vs. Financial Automation scope boundary
- Problem: Automation Center (the product line) and Financial Automation (its first named service) currently share the same generic discovery methodology and benchmark pricing; it is not yet decided whether Automation Center will host additional named services beyond Financial Automation, or whether Financial Automation should diverge with its own pricing/methodology over time.
- Scope: Decide whether to keep a single generic methodology/pricing model across all Automation Center services, or let Financial Automation (and any future named services) diverge; document the decision as an ADR.
- Acceptance: `docs/adr/000X-automation-center-service-scope.md` exists recording the decision; `KnowledgeBase/kb-value-proposition/docs/products/03-automation-center.md` and `04-financial-automation.md` updated to reflect it if needed.

## HC-017 Track real-resource-base and cross-sell-direction decisions through to evidence
- Problem: The Sept 2026 correction round replaced several previously unvalidated framings with concrete decisions: (1) the actual current resource base is 1 paid employee (Consulting Officer) plus 2 unpaid partner relationships (Operations, Financial) and 2 servers (Frank + SolarSeed machine) — not the earlier illustrative 4-person team (see `KnowledgeBase/kb-cost-structure/docs/model/08-cost-structure.md`); (2) cross-sell direction is decided as Automation Center leads, with Human Center consultancy attached on top (see `KnowledgeBase/kb-value-proposition/docs/company/01-company-overview.md`, `docs/products/03-automation-center.md`). Neither decision has been tested against real client behavior yet.
- Scope: As Automation Center signs its first prospects, record whether (a) the resource base actually holds (no unplanned new hires/tools acquired outside the resource-acquisition principle) and (b) the Automation-Center-leads cross-sell pattern actually converts into attached Human Center engagements.
- Acceptance: `kb-cost-structure/docs/model/08-cost-structure.md` and `kb-value-proposition/docs/company/01-company-overview.md` updated with real conversion/resource evidence after the first signed Automation Center client, or `evidence_status` explicitly re-confirmed as still provisional if no signal yet exists.

## HC-018 Deploy the first paying customer on SolarSeed TRL5
- Problem: Stage 3 is the first paying customer's dedicated account/agent on SolarSeed TRL5; the host's intended role does not itself establish readiness or customer-specific isolation.
- Scope: After the partner pilot is validated, HC-015's Frank local MVP is implemented and validated, and a paying customer is signed, verify SolarSeed host readiness, tenant/account separation, access controls, backups, rollback, and incident handling. Obtain written authorization and the required DPA before deploying the dedicated account/agent; keep authorization evidence in an approved secure location, not in the repository.
- Acceptance: The customer-specific account/agent is deployed only after a documented readiness/isolation review and confirmed authorization/DPA; access, backup, rollback, and incident controls are tested, and the corresponding Open Action in `KnowledgeBase/kb-key-resources/docs/architecture/06-automation-center-key-resources.md` is closed.

## HC-019 Resolve partner compensation and discovery-fee terms
- Problem: The current free-discovery decision conflicts with a proposed partner share of a one-time discovery fee, and the broader partner revenue-share proposal is not approved.
- Scope: Decide whether Automation Center discovery remains free or becomes fee-bearing; if partner compensation proceeds, document percentages, allocation, attribution, collected-revenue and direct-cost basis, maintenance-period duration/cap, and obtain required employer/conflict, tax, and legal review. Keep Shrinking AI's separate paid diagnostic decision distinct.
- Acceptance: A written decision resolves the free-versus-paid discovery conflict and approves or rejects the complete partner-compensation terms; `KnowledgeBase/kb-key-partners/docs/partnerships/06-key-partners.md`, `KnowledgeBase/kb-revenue-streams/docs/model/07-revenue-streams.md`, and any affected channel guidance agree. No fee or share is promised before approval.
