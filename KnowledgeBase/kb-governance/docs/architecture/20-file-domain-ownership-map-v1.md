# 20 — KB File-to-Domain Ownership Map v1
## Consolidation provenance
- consolidation_actor: `WARP`
- consolidation_source: `origin/feat/kb-mempalace-critical-upgrade:KnowledgeBase/20-KB-File-to-Domain-Ownership-Map-v1.md@eba9cbde025e90b389042ae6f2d840763f894e27`
- consolidation_date: `2026-04-17`
- consolidation_status: `canonicalized`


---

## Purpose
This file maps existing KB documents to primary and secondary domains from `19-KB-Domain-Taxonomy-Map-v1.md` and establishes ownership expectations for future updates.

---

## Mapping

| File | Primary Domain | Secondary Domains | Owner Role (TBD by leadership) |
|---|---|---|---|
| `00-Glossary.md` | `domain_governance` | all | KB steward |
| `01-Company-Overview.md` | `domain_value_prop` | `domain_relationships` | Strategy/Product |
| `02-Products.md` | `domain_value_prop` | `domain_resources`, `domain_solutions` | Product |
| `03-Business-Model.md` | `domain_revenue` | `domain_value_prop`, `domain_costs` | Finance/Product |
| `04-System-Architecture.md` | `domain_resources` | `domain_activities`, `domain_solutions` | Technical |
| `05-Tokenomics-and-Governance.md` | `domain_governance` | `domain_revenue`, `domain_relationships` | Governance/Finance |
| `06-Legal-Structure.md` | `domain_governance` | `domain_relationships` | Legal/Governance |
| `07-Customers-and-GTM.md` | `domain_customers` | `domain_channels`, `domain_relationships` | Growth/Customer |
| `08-Partnerships.md` | `domain_partners` | `domain_channels`, `domain_activities` | Partnerships |
| `09-Strategy-and-Investment.md` | `domain_solutions` | `domain_revenue`, `domain_problems` | Strategy/Finance |
| `10-Market-Context.md` | `domain_problems` | `domain_solutions`, `domain_metrics` | Strategy/Research |
| `11-Academic-References.md` | `domain_governance` | `domain_solutions` | Research/KB steward |
| `12-Open-Questions.md` | `domain_governance` | all | KB steward |
| `13-Financial-Model.md` | `domain_costs` | `domain_revenue`, `domain_metrics` | Finance |
| `14-KB-Audit-v1.1.md` | `domain_governance` | all | KB steward |
| `15-Sunified-Quantum-Resistance.md` | `domain_resources` | `domain_solutions` | Technical/Strategy |
| `16-FilantropiaSolar-Platform.md` | `domain_activities` | `domain_resources`, `domain_metrics` | Product/Technical |
| `17-Execution-Readiness-and-Next-30-Days.md` | `domain_activities` | `domain_metrics`, `domain_problems` | Operations |
| `18-KB-MemPalace-Critical-Review-and-Action-Plan.md` | `domain_governance` | all | KB steward |
| `KB-memPalace-upgrade.md` | `domain_governance` | all | KB steward |
| `19-KB-Domain-Taxonomy-Map-v1.md` | `domain_governance` | all | KB steward |
| `templates/LOI-SolarSeed-Template.md` | `domain_relationships` | `domain_customers`, `domain_revenue` | Customer/Legal |

---

## Operational Rules
- A file update should be approved by the primary domain owner.
- Cross-domain changes require acknowledgment from affected secondary domain owners.
- If ownership is unassigned, default approver is KB steward.

---

## Gap Notes
- `domain_relationships` requires fuller dedicated documentation (beyond LOI and fragments in GTM docs).
- `domain_metrics` currently distributed across files; a dedicated domain summary file should be created in next phase.

formal_proof:
  engine: ml-hilbert
  trl_phase: TRL6
  obligation_id: kb.governance.architecture_20_file_domain_ownership_map_v1
  proof_artifact: kb-governance/formal-proofs/governance-architecture-20-file-domain-ownership-map-v1.lean
  verification_status: verified
