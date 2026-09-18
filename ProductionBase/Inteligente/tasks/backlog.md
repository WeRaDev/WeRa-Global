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

## HC-009 Run the Automation Center discovery methodology manually with first prospects
- Problem: Automation Center's discovery-and-ROI methodology (`KnowledgeBase/kb-solution/docs/strategy/03-automation-center-solution.md`) is fully designed but has never been run with a real prospect, manually or via chatbot.
- **Status (Sept 2026): ongoing** — actively being worked, not just an open backlog item (see `KnowledgeBase/kb-key-activities/docs/execution/05-automation-center-key-activities.md`).
- Scope: Conduct the role-routed discovery interview (adviser/operations/compliance) manually with 2-3 real prospects; log which questions/probes worked and produce at least one screening decision (Stop/Measure/Prototype/Pilot).
- Acceptance: At least one completed, evidence-graded screening decision record exists for a real prospect.

## HC-010 Build and test the Automation Center discovery chatbot
- Problem: No chatbot implementation of the discovery methodology exists yet; it must not be built before the manual process is validated (see HC-009).
- Scope: Implement the conversational state machine, consent/disclosure, evidence model, adaptive probing limits, and human-escalation triggers defined in `KnowledgeBase/kb-solution/docs/strategy/03-automation-center-solution.md`.
- Acceptance: Chatbot passes the pre-release adversarial test set (vague answers, sensitive-data attempts, escalation triggers) before any public launch.

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
