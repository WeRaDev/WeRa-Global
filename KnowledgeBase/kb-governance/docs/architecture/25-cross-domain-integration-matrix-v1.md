# 25 — KB Cross-Domain Integration Matrix v1
## Consolidation provenance
- consolidation_actor: `WARP`
- consolidation_source: `origin/feat/kb-mempalace-critical-upgrade:KnowledgeBase/25-KB-Cross-Domain-Integration-Matrix-v1.md@eba9cbde025e90b389042ae6f2d840763f894e27`
- consolidation_date: `2026-04-17`
- consolidation_status: `canonicalized`


---

## Purpose
Define operational cross-domain integration patterns for case-centric execution and ensure consistent linking across core KB domains.

---

## Integration Principles
- Each operational flow must connect at least: `customers`, `channels`, `partners`, `revenue`, `metrics`.
- Primary-domain documents must reference downstream and upstream dependencies.
- Cross-domain links are directional for workflow execution but treated as bidirectional for knowledge retrieval.

---

## Core Integration Matrix

| From Domain | To Domain | Integration Object | Required Link Artifact |
|---|---|---|---|
| `domain_customers` | `domain_channels` | case intake source and outreach path | case source + channel code |
| `domain_channels` | `domain_partners` | partner-mediated acquisition and RFQ routing | partner routing rule |
| `domain_partners` | `domain_revenue` | quote and financing feasibility inputs | quote + pricing dependency |
| `domain_revenue` | `domain_metrics` | expected vs actual economic performance | metric definitions and thresholds |
| `domain_metrics` | `domain_problems` | underperformance/risk escalation | exception trigger record |
| `domain_problems` | `domain_solutions` | mitigation and redesign actions | solution action link |
| `domain_solutions` | `domain_activities` | SOP updates and rollout actions | workflow update record |
| `domain_activities` | `domain_customers` | lifecycle status transitions and outcomes | case status update |

---

## Required Cross-Domain Blocks in Operational Docs

Each operational file in `customers`, `channels`, `partners`, `revenue`, `metrics` must include:
1. `Primary domain`
2. `Secondary domains`
3. `Upstream dependencies`
4. `Downstream dependencies`
5. `Validation hooks` (what to check before status/progression updates)

---

## Priority Pilot Links (Phase 3)

Pilot file set:
- `07-Customers-and-GTM.md`
- `08-Partnerships.md`
- `03-Business-Model.md`

Required link path:
`07 -> 08 -> 03 -> 13 -> 12`

Interpretation:
- GTM generates cases/channels
- Partnerships supply quote/delivery capacity
- Business model defines pricing/qualification logic
- Financial model defines measurable performance outcomes
- Open questions capture unresolved risk and validation backlog
