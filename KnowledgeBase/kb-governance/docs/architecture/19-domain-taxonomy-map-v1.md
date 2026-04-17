# 19 — KB Domain Taxonomy Map v1 (BMC + Lean + Governance)
## Consolidation provenance
- consolidation_actor: `WARP`
- consolidation_source: `origin/feat/kb-mempalace-critical-upgrade:KnowledgeBase/19-KB-Domain-Taxonomy-Map-v1.md@eba9cbde025e90b389042ae6f2d840763f894e27`
- consolidation_date: `2026-04-17`
- consolidation_status: `canonicalized`


---

## Purpose
This document verifies current KB structure and defines the canonical 12-domain taxonomy required by the corrected update plan in `18-KB-MemPalace-Critical-Review-and-Action-Plan.md`.

---

## Verification Summary (Current State)
- Current KB is organized as a numbered monograph set (`00` to `26`) plus templates.
- Coverage exists for most BMC/Lean topics, but not as explicit domain-governed modules.
- Cross-domain ownership and controlled vocabulary were not formally codified.

Conclusion: current structure is content-rich but governance-light for a case-operational model.

---

## Canonical 12-Domain Taxonomy

### Core (Business Model Canvas — 9)
1. Customer Segments (`domain_customers`)
2. Value Propositions (`domain_value_prop`)
3. Channels (`domain_channels`)
4. Customer Relationships (`domain_relationships`)
5. Revenue Streams (`domain_revenue`)
6. Key Resources (`domain_resources`)
7. Key Activities (`domain_activities`)
8. Key Partners (`domain_partners`)
9. Cost Structure (`domain_costs`)

### Overlay (Lean Canvas — 3)
10. Problems (`domain_problems`)
11. Solutions (`domain_solutions`)
12. Key Metrics (`domain_metrics`)

### Meta-governance (cross-cutting control layer)
- Governance (`domain_governance`) is mandatory as operational control, but not counted in 9+3.

---

## Domain Rules
- Every KB file must have one **primary domain owner** and optional secondary domain links.
- Primary ownership controls updates, approvals, and evidence quality.
- Cross-domain links are required for case-operational files (customers/channels/partners/revenue/metrics).
- Claims must carry evidence status labels (`verified`, `unverified`, `hypothesis`) where applicable.

---

## Phase 1 Completion Check (Workstream A)
- [x] Canonical domain map defined
- [x] Domain naming standardized
- [x] Governance layer explicit
- [ ] Domain stewards assigned by role/person
- [ ] Migration of all documents to domain-front-matter complete
