# Legacy KB to Split Repository Migration Index v1
version: 1.0
status: active
owner: migration steward

## Purpose
Define authoritative source-to-destination mapping from legacy `KnowledgeBase/` files to split repositories.

## Mapping rules
1. Every legacy file has one primary destination repository.
2. Secondary dependencies are documented for cross-domain review routing.
3. Each migration row carries `temporal_scope` to enforce entity approvals.

## Migration index
| Legacy file | Destination repository | Destination path (proposed) | Temporal scope | Secondary review dependencies |
|---|---|---|---|---|
| `KnowledgeBase/00-Glossary.md` | `kb-governance` | `docs/standards/00-glossary.md` | mixed | all domains |
| `KnowledgeBase/01-Company-Overview.md` | `kb-value-proposition` | `docs/company/01-company-overview.md` | current | `kb-solution` |
| `KnowledgeBase/02-Products.md` | `kb-value-proposition` | `docs/products/02-products.md` | current | `kb-key-resources`, `kb-solution` |
| `KnowledgeBase/03-Business-Model.md` | `kb-revenue-streams` | `docs/model/03-business-model.md` | current | `kb-key-partners`, `kb-metrics` |
| `KnowledgeBase/04-System-Architecture.md` | `kb-key-resources` | `docs/architecture/04-system-architecture.md` | current | `kb-key-activities`, `kb-solution` |
| `KnowledgeBase/05-Tokenomics-and-Governance.md` | `kb-governance` | `docs/tokenomics/05-tokenomics-and-governance.md` | mixed | `kb-revenue-streams` |
| `KnowledgeBase/06-Legal-Structure.md` | `kb-governance` | `docs/legal/06-legal-structure.md` | past | `kb-revenue-streams` |
| `KnowledgeBase/07-Customers-and-GTM.md` | `kb-customers` | `docs/gtm/07-customers-and-gtm.md` | current | `kb-channels`, `kb-key-partners` |
| `KnowledgeBase/08-Partnerships.md` | `kb-key-partners` | `docs/partnerships/08-partnerships.md` | current | `kb-revenue-streams`, `kb-key-activities` |
| `KnowledgeBase/09-Strategy-and-Investment.md` | `kb-solution` | `docs/strategy/09-strategy-and-investment.md` | future | `kb-revenue-streams`, `kb-problem` |
| `KnowledgeBase/10-Market-Context.md` | `kb-problem` | `docs/market/10-market-context.md` | future | `kb-solution`, `kb-metrics` |
| `KnowledgeBase/11-Academic-References.md` | `kb-governance` | `references/11-academic-references.md` | past | `kb-solution` |
| `KnowledgeBase/12-Open-Questions.md` | `kb-governance` | `docs/open-questions/12-open-questions.md` | mixed | all domains |
| `KnowledgeBase/13-Financial-Model.md` | `kb-metrics` | `docs/financial/13-financial-model.md` | current | `kb-revenue-streams`, `kb-cost-structure` |
| `KnowledgeBase/14-KB-Audit-v1.1.md` | `kb-governance` | `docs/audit/14-kb-audit-v1.1.md` | past | all domains |
| `KnowledgeBase/15-Sunified-Quantum-Resistance.md` | `kb-key-resources` | `docs/suppliers/15-sunified-quantum-resistance.md` | future | `kb-solution` |
| `KnowledgeBase/16-FilantropiaSolar-Platform.md` | `kb-key-activities` | `docs/platform/16-filantropiasolar-platform.md` | current | `kb-key-resources`, `kb-metrics` |
| `KnowledgeBase/17-Execution-Readiness-and-Next-30-Days.md` | `kb-key-activities` | `docs/execution/17-execution-readiness-next-30-days.md` | current | `kb-governance`, `kb-metrics` |
| `KnowledgeBase/18-KB-MemPalace-Critical-Review-and-Action-Plan.md` | `kb-governance` | `docs/reviews/18-mempalace-critical-review-action-plan.md` | past | all domains |
| `KnowledgeBase/19-KB-Domain-Taxonomy-Map-v1.md` | `kb-governance` | `docs/architecture/19-domain-taxonomy-map-v1.md` | mixed | all domains |
| `KnowledgeBase/20-KB-File-to-Domain-Ownership-Map-v1.md` | `kb-governance` | `docs/architecture/20-file-domain-ownership-map-v1.md` | mixed | all domains |
| `KnowledgeBase/21-KB-Controlled-Vocabulary-and-Entity-Standards-v1.md` | `kb-governance` | `docs/standards/21-controlled-vocabulary-entity-standards-v1.md` | mixed | all domains |
| `KnowledgeBase/22-KB-Anonymized-Case-Schema-and-Lifecycle-v1.md` | `kb-customers` | `docs/standards/22-anonymized-case-schema-lifecycle-v1.md` | current | `kb-revenue-streams`, `kb-governance` |
| `KnowledgeBase/23-KB-Domain-Template-Pack-v1.md` | `kb-governance` | `templates/23-domain-template-pack-v1.md` | mixed | all domains |
| `KnowledgeBase/24-KB-Governance-Workflows-v1.md` | `kb-governance` | `docs/workflows/24-governance-workflows-v1.md` | mixed | all domains |
| `KnowledgeBase/25-KB-Cross-Domain-Integration-Matrix-v1.md` | `kb-governance` | `docs/architecture/25-cross-domain-integration-matrix-v1.md` | mixed | all domains |
| `KnowledgeBase/26-KB-Validation-Protocol-v1.md` | `kb-governance` | `docs/validation/26-validation-protocol-v1.md` | mixed | all domains |
| `KnowledgeBase/templates/LOI-SolarSeed-Template.md` | `kb-channels` | `templates/LOI-SolarSeed-Template.md` | current | `kb-customers`, `kb-governance` |

## Migration execution notes
- Preserve source commit hash and migration actor in file provenance.
- Preserve legacy path reference in migrated file header until phase-2 stabilization closes.
- Route review by `temporal_scope` before accepting destination merge.
