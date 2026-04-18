# Canonical KB CI Quality Gates Specification v2
version: 2.0
status: ready
owner: technical steward
scope: REALIGN-10
supersedes: `kb-governance/ci/quality-gates-spec-v1.md`

## Purpose
Define merge-blocking quality gates for one canonical repository model with domain folders under `KnowledgeBase/`.

## Trigger scope
Run gates when a change touches any of:
- `KnowledgeBase/**/*.md`
- `KnowledgeBase/templates/**/*.md`
- `kb-governance/**/*.md`

## Required checks
1. Metadata schema check
   - Required metadata/provenance contract fields are present on operational records.
2. Canonical naming check
   - Enforce canonical naming policy and alias labeling rules.
3. Evidence labeling check
   - High-impact claims must include `verified`, `unverified`, or `hypothesis`.
4. Privacy boundary check
   - Block known PII patterns in case-content paths.
5. Cross-domain dependency check
   - Require upstream/downstream dependency references for cross-domain operational docs.
6. Temporal routing readiness check
   - `temporal_scope` exists and uses valid enum values.
7. Provenance continuity check
   - Consolidated and newly created governed docs include provenance block or equivalent metadata.
8. Canonical path policy check
   - Reject source-of-truth additions outside canonical `KnowledgeBase/` tree for KB content.

## Path-scoped ownership signals
- `KnowledgeBase/kb-customers/**` -> customer domain steward.
- `KnowledgeBase/kb-key-partners/**` -> partnership domain steward.
- `KnowledgeBase/kb-revenue-streams/**` -> revenue domain steward.
- `KnowledgeBase/kb-metrics/**` -> metrics domain steward.
- `KnowledgeBase/kb-governance/**` and `kb-governance/**` -> governance/technical steward.

## Baseline workflow specifications
Single repository should include:
- `.gitea/workflows/kb-canonical-validate.yml`
- `.gitea/workflows/kb-governance-routing.yml`

## Failure policy
- Any required check failure blocks merge to `main`.
- Waivers require:
  - governance event reference,
  - temporal-scope-appropriate approvals.

## Minimum success criteria
1. Workflow specs are present and executable in Gitea CI.
2. One negative fixture proves merge blocking on metadata/policy violation.
3. One positive fixture proves merge acceptance for compliant change.
4. Pilot-chain file updates pass all gates in dry-run.
