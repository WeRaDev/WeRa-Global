# Direct-Adoption Artifact Transfer Manifest v1
version: 1.0
status: execution-ready
owner: KB steward

## Purpose
Define first-pass transfer set for SPLIT-08 using reusable artifacts marked for direct adoption.

## Transfer set
| Source artifact | Destination repository | Destination path |
|---|---|---|
| `KnowledgeBase/18-KB-MemPalace-Critical-Review-and-Action-Plan.md` | `kb-governance` | `docs/reviews/18-mempalace-critical-review-action-plan.md` |
| `KnowledgeBase/19-KB-Domain-Taxonomy-Map-v1.md` | `kb-governance` | `docs/architecture/19-domain-taxonomy-map-v1.md` |
| `KnowledgeBase/20-KB-File-to-Domain-Ownership-Map-v1.md` | `kb-governance` | `docs/architecture/20-file-domain-ownership-map-v1.md` |
| `KnowledgeBase/21-KB-Controlled-Vocabulary-and-Entity-Standards-v1.md` | `kb-governance` | `docs/standards/21-controlled-vocabulary-entity-standards-v1.md` |
| `KnowledgeBase/22-KB-Anonymized-Case-Schema-and-Lifecycle-v1.md` | `kb-customers` | `docs/standards/22-anonymized-case-schema-lifecycle-v1.md` |
| `KnowledgeBase/24-KB-Governance-Workflows-v1.md` | `kb-governance` | `docs/workflows/24-governance-workflows-v1.md` |
| `KnowledgeBase/25-KB-Cross-Domain-Integration-Matrix-v1.md` | `kb-governance` | `docs/architecture/25-cross-domain-integration-matrix-v1.md` |
| `KnowledgeBase/26-KB-Validation-Protocol-v1.md` | `kb-governance` | `docs/validation/26-validation-protocol-v1.md` |
| `KnowledgeBase/templates/KB-Domain-Document-Template-v1.md` | `kb-governance` | `templates/KB-Domain-Document-Template-v1.md` |
| `KnowledgeBase/templates/KB-Governance-Event-Template-v1.md` | `kb-governance` | `templates/KB-Governance-Event-Template-v1.md` |

## Transfer constraints
- Preserve original content first, then apply destination normalization in a follow-up commit.
- Add provenance header to each migrated file:
  - source path
  - source commit
  - migration actor
  - migration date
- Route review by `temporal_scope` from migration index before merge.

## Validation
- Every transferred file exists at destination path.
- Legacy-to-new index entry exists for every transferred artifact.
- Naming policy check passes on active (non-source-capture) sections.
