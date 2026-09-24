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

## HC-009 Run the Automation Center discovery methodology with first prospects (founder-led manual sessions)
- Problem: Automation Center's discovery-and-ROI methodology (`KnowledgeBase/kb-solution/docs/strategy/03-automation-center-solution.md`) is fully designed but has never been run with a real prospect.
- **Status (Sept 2026, corrected): a live Odoo chatbot exists on the Frank machine, but verified inspection shows it implements only generic livechat and lead-routing/lead-creation — none of the governed-interview safety/routing logic.** This corrects the earlier claim that it was "partially configured with role-routing questions" and "targeted for deployment within days"; no such near-term timeline is committed. Named prospects already exist, mostly small financial-advisory/consultancy firms with employees, sourced from the founder's two active partner relationships (see `KnowledgeBase/kb-customers/docs/gtm/05-financial-automation-segments.md`, `KnowledgeBase/kb-channels/docs/gtm/12-automation-center-channels.md`, `KnowledgeBase/kb-key-partners/docs/partnerships/06-key-partners.md`). Real sessions must be run **manually by the founder** in the meantime, using the MVP script (`Resources/Documents/Research/financial_advisory_automation_mvp.xlsx`); see HC-016 for the chatbot build task.
- Scope: Run founder-led manual discovery sessions (adviser/operations/compliance routes) with named prospects; log which questions/probes worked and produce at least one screening decision (Stop/Measure/Prototype/Pilot).
- Acceptance: At least one completed, evidence-graded screening decision record exists for a real, named prospect, produced via a founder-led manual session.

## HC-016 Build the governed-interview safety/routing logic into the Odoo chatbot
- Problem: The live Odoo chatbot on the Frank machine currently implements only generic livechat and lead-routing; it lacks all six governed-interview elements required before it can safely run a real discovery session: opening disclosure, explicit consent request, sensitive-data detection/interrupt, role-based (adviser/operations/compliance/finance) routing, evidence grading (A-E), and Stop/Measure/Prototype/Pilot completion logic (see `KnowledgeBase/kb-key-resources/docs/architecture/06-automation-center-key-resources.md`).
- Scope: Design and implement the missing logic in Odoo (or a connected automation layer), using the implementation-ready script/data model in `Resources/Documents/Research/financial_advisory_automation_mvp.xlsx` as the spec; this is real, unscheduled engineering work, not a near-complete configuration step.
- Acceptance: The chatbot passes a pre-release adversarial test set (vague answers, sensitive-data attempts, escalation triggers) covering all six governed-interview elements before it is used for any real, unsupervised prospect session.

## HC-010 Validate the chatbot once governed logic exists, then evaluate a public/self-service deployment
- Problem: A public/self-service deployment is an explicit later-phase decision, not the current plan (see `KnowledgeBase/kb-channels/docs/gtm/12-automation-center-channels.md`); it is now also gated on HC-016 (the chatbot does not yet have governed-interview logic to validate).
- Scope: Once HC-016 delivers the governed-interview logic and founder-supervised sessions validate the conversational state machine, consent/disclosure, evidence model, adaptive probing limits, and human-escalation triggers in practice, decide whether and when to open the chatbot to self-service prospects.
- Acceptance: Chatbot passes a pre-release adversarial test set (vague answers, sensitive-data attempts, escalation triggers) before any public/self-service launch is considered.

## HC-015 Confirm the Frank/SolarSeed machine split keeps client data isolated
- Problem: **Corrected (Sept 2026): the discovery chatbot is hosted on Frank, which currently has zero other active workload** (no contention or cross-project data-mixing risk today); the SolarSeed machine is separately earmarked for the first signed client's automation instance, kept apart from the platform layer by design. This replaces the earlier framing that assumed shared-tenancy risk with other WeRa Global projects on a single "TRL4" machine.
- Scope: Before the first real discovery session or client engagement touches any prospect-identifying information, confirm the Frank/SolarSeed separation remains intact (verify no shared database/instance) and document access controls for each machine's Odoo/automation deployment.
- Acceptance: `KnowledgeBase/kb-key-resources/docs/architecture/06-automation-center-key-resources.md` Open Actions item on Frank/SolarSeed data isolation closed.

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
