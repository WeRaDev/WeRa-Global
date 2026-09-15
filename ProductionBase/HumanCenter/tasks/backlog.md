# Human Center backlog

## HC-001 Build the qualification gate and booking page
- Problem: No lead-qualification gate or booking page exists yet, so unqualified calls waste founder time (a named operational risk in research).
- Scope: Build a booking page following the boutique-agency benchmark pattern (single embedded scheduler, one CTA, 2-3 question qualification micro-form) per `KnowledgeBase/kb-channels/docs/gtm/11-channels.md`. Include explicit disqualification copy for wrong-fit visitors (see `KnowledgeBase/kb-unfair-advantage/docs/strategy/10-unfair-advantage.md`).
- Acceptance: booking page live at `www.inteligente.site`, qualification form in place, disqualification copy reviewed against the AI Jungle benchmark pattern.

## HC-002 Choose booking/scheduling stack (ADR)
- Problem: No hosting/scheduler stack decision has been recorded.
- Scope: Define minimal site scope (positioning, Product 1 services, free-call booking, contact) and choose hosting/scheduler stack; record the decision as an ADR.
- Acceptance: `docs/adr/000X-site-stack.md` exists and the site is reachable at `www.inteligente.site`.

## HC-003 Set and document Shrinking AI's paid-session price
- Problem: Shrinking AI's core paid-session price is undocumented anywhere in research (see `KnowledgeBase/kb-revenue-streams/docs/model/07-revenue-streams.md`) — this is the highest-priority pricing gap. The `HumanCenter.Pricing.md` benchmarks describe a different, unrelated automation-agency offer and must not be used as a substitute.
- Scope: Build an actual cost model (`kb-cost-structure/`) and set a concrete price for the paid RCGFC session.
- Acceptance: `kb-revenue-streams/docs/model/07-revenue-streams.md` updated with a documented session price and `evidence_status: verified`.

## HC-004 Confirm commercial-registry number and formalize DPA
- Problem: The legal entity (Inteligente Razão — Unipessoal LDA) is confirmed, but the Portuguese commercial-registry/VAT (NIF) number is not yet confirmed (see `kb-governance/docs/legal/11-legal-structure.md`).
- Scope: Confirm the registry number and formalize a DPA template for client engagements handling confidential/financial data.
- Acceptance: `kb-governance/docs/legal/11-legal-structure.md` Open Actions item closed; DPA template exists.

## HC-005 Produce first proof assets
- Problem: No proof assets exist yet to support the "demonstrated not claimed" positioning (see `kb-unfair-advantage/docs/strategy/10-unfair-advantage.md` and `kb-metrics/docs/financial/09-key-metrics.md`).
- Scope: Deliver 10+ completed paid sessions, write up 3 client cases, and assemble a consent evidence pack authorizing their use.
- Acceptance: 3 case write-ups published (post-consent) and referenced from the site and `kb-metrics/`.

## HC-006 Build an on-site RCGFC preview
- Problem: The RCGFC framework (Role, Context, Goal, Format, Constraints) is Shrinking AI's core differentiator but is not yet demonstrated anywhere client-facing.
- Scope: Design a short, self-serve RCGFC preview/interactive element for the site so prospects can experience the framework before booking.
- Acceptance: RCGFC preview live on `www.inteligente.site`, linked from the booking page.

## HC-007 Keep Product 1/Product 2 strictly separated
- Problem: Product 1 ("Shrinking AI", B2B) and Product 2 ("Career Development", B2C) risk brand collision if not deliberately separated.
- Scope: When building site navigation, tone, and CTAs, ensure Product 1 and Product 2 never share a page, CTA, or messaging tone; document the separation decision as an ADR once Product 2 work begins.
- Acceptance: Site navigation and any Product 2 planning docs show clear separation from Product 1.

## HC-008 Validate problem framing with real discovery calls
- Problem: Problem/solution framing in `KnowledgeBase/kb-problem/` and `kb-solution/` is currently validated only via desk research (industry stats, competitive analysis), not real client conversations.
- Scope: Run 3-5 discovery calls with the primary ICP segment (A4: AI-frustrated consultants/freelancers); capture findings as evidence in the KB.
- Acceptance: `kb-problem` and `kb-customers` documents cite findings from at least 3 real discovery calls alongside the existing desk research.
