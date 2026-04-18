# Split-Staging to Canonical KnowledgeBase Consolidation Index v1
version: 1.0
status: active
owner: migration steward
scope: REALIGN-03

## Purpose
Define authoritative mapping from prior split-staging artifacts and legacy flat `KnowledgeBase/` files into canonical folderized destinations under `KnowledgeBase/`.

## Canonical policy
- Canonical source of truth is `KnowledgeBase/` in umbrella repository.
- Split `kb-*` repositories are frozen staging/history and are not canonical authoring targets.
- Every migrated file must carry provenance metadata.

## Consolidation mapping
| Source type | Source path | Canonical destination path | Domain | Status |
|---|---|---|---|---|
| split-staging | `_kb-split-migration/kb-customers/docs/gtm/07-customers-and-gtm.md` | `KnowledgeBase/kb-customers/docs/gtm/07-customers-and-gtm.md` | current | planned |
| split-staging | `_kb-split-migration/kb-key-partners/docs/partnerships/08-partnerships.md` | `KnowledgeBase/kb-key-partners/docs/partnerships/08-partnerships.md` | current | planned |
| split-staging | `_kb-split-migration/kb-revenue-streams/docs/model/03-business-model.md` | `KnowledgeBase/kb-revenue-streams/docs/model/03-business-model.md` | current | planned |
| split-staging | `_kb-split-migration/kb-metrics/docs/financial/13-financial-model.md` | `KnowledgeBase/kb-metrics/docs/financial/13-financial-model.md` | current | planned |
| split-staging | `_kb-split-migration/kb-governance/docs/open-questions/12-open-questions.md` | `KnowledgeBase/kb-governance/docs/open-questions/12-open-questions.md` | mixed | planned |
| legacy/reusable | `KnowledgeBase/18-KB-MemPalace-Critical-Review-and-Action-Plan.md` | `KnowledgeBase/kb-governance/docs/reviews/18-mempalace-critical-review-action-plan.md` | past | planned |
| reusable branch | `origin/feat/kb-mempalace-critical-upgrade:KnowledgeBase/19-KB-Domain-Taxonomy-Map-v1.md` | `KnowledgeBase/kb-governance/docs/architecture/19-domain-taxonomy-map-v1.md` | mixed | planned |
| reusable branch | `origin/feat/kb-mempalace-critical-upgrade:KnowledgeBase/20-KB-File-to-Domain-Ownership-Map-v1.md` | `KnowledgeBase/kb-governance/docs/architecture/20-file-domain-ownership-map-v1.md` | mixed | planned |
| reusable branch | `origin/feat/kb-mempalace-critical-upgrade:KnowledgeBase/21-KB-Controlled-Vocabulary-and-Entity-Standards-v1.md` | `KnowledgeBase/kb-governance/docs/standards/21-controlled-vocabulary-entity-standards-v1.md` | mixed | planned |
| reusable branch | `origin/feat/kb-mempalace-critical-upgrade:KnowledgeBase/22-KB-Anonymized-Case-Schema-and-Lifecycle-v1.md` | `KnowledgeBase/kb-customers/docs/standards/22-anonymized-case-schema-lifecycle-v1.md` | current | planned |
| reusable branch | `origin/feat/kb-mempalace-critical-upgrade:KnowledgeBase/24-KB-Governance-Workflows-v1.md` | `KnowledgeBase/kb-governance/docs/workflows/24-governance-workflows-v1.md` | mixed | planned |
| reusable branch | `origin/feat/kb-mempalace-critical-upgrade:KnowledgeBase/25-KB-Cross-Domain-Integration-Matrix-v1.md` | `KnowledgeBase/kb-governance/docs/architecture/25-cross-domain-integration-matrix-v1.md` | mixed | planned |
| reusable branch | `origin/feat/kb-mempalace-critical-upgrade:KnowledgeBase/26-KB-Validation-Protocol-v1.md` | `KnowledgeBase/kb-governance/docs/validation/26-validation-protocol-v1.md` | mixed | planned |
| governance templates | `kb-governance/templates/KB-Domain-Document-Template-v1.md` | `KnowledgeBase/templates/KB-Domain-Document-Template-v1.md` | mixed | planned |
| governance templates | `kb-governance/templates/KB-Governance-Event-Template-v1.md` | `KnowledgeBase/templates/KB-Governance-Event-Template-v1.md` | mixed | planned |

## Execution notes
- Preserve split-staging metadata blocks when source already includes canonical contract fields.
- Add consolidation provenance block to each destination file:
  - `consolidation_actor`
  - `consolidation_source`
  - `consolidation_date`
  - `consolidation_status`
- Validate pilot chain link integrity after transfer.
