# Human Center backlog

## HC-001 Validate problem framing with discovery calls
- Problem: Problem/solution framing in `KnowledgeBase/kb-problem/` and `kb-solution/` is derived from desk research only, not real client conversations.
- Scope: Run 3-5 discovery calls with the target segment (independent consultants / small professional-services firms); capture findings as evidence in the KB.
- Acceptance: `kb-problem` and `kb-customers` documents updated with `evidence_status: verified` findings from at least 3 calls.

## HC-002 Stand up www.inteligente.site
- Problem: No public-facing site exists yet for the consultancy.
- Scope: Define minimal site scope (positioning, services, contact) and choose hosting/stack; record the decision as an ADR.
- Acceptance: `docs/adr/000X-site-stack.md` exists and the site is reachable at `www.inteligente.site`.

## HC-003 Scope and price the first pilot package
- Problem: Pricing in `kb-revenue-streams/` is market-benchmark-derived, not Human-Center-specific.
- Scope: Build an actual cost model (`kb-cost-structure/`) and define a concrete first-pilot package and price.
- Acceptance: `kb-revenue-streams/docs/model/07-revenue-streams.md` updated with a Human-Center-specific offer and `evidence_status: verified` once a pilot is signed.

## HC-004 Confirm legal entity and compliance posture
- Problem: Legal-entity linkage is unverified (see `kb-governance/docs/legal/11-legal-structure.md`).
- Scope: Confirm the legal entity, data-processing posture (DPA template, EU hosting), and update `kb-governance/`.
- Acceptance: `kb-governance/docs/legal/11-legal-structure.md` has `evidence_status: verified`.
