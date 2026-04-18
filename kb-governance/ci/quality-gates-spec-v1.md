# Split KB CI Quality Gates Specification v1
version: 1.0
status: ready
owner: technical steward
scope: SPLIT-10

## Purpose
Define merge-blocking CI checks for split KB repositories.

## Required checks
1. Metadata schema check
   - Required fields present (`primary_domain`, `temporal_scope`, `evidence_status`, provenance fields).
2. Canonical naming check
   - Enforce policy from `kb-governance/policies/canonical-naming-policy-v1.md`.
3. Evidence labeling check
   - High-impact claims must include one of `verified`, `unverified`, `hypothesis`.
4. Privacy boundary check
   - Block known PII patterns in case-content repositories.
5. Cross-domain dependency check
   - Require upstream/downstream dependency blocks in operational docs.
6. Temporal routing readiness check
   - `temporal_scope` present and valid enum value.

## Repository rollout order
1. `kb-governance`
2. `kb-customers`
3. `kb-key-partners`
4. `kb-revenue-streams`
5. `kb-metrics`
6. Remaining domain repositories

## Baseline workflow files
Each repository should include:
- `.gitea/workflows/kb-validate.yml`
- `.gitea/workflows/kb-governance-gate.yml`

## Failure policy
- Any required check failure blocks merge to `main`.
- Waivers require governance event reference and applicable temporal-entity approvals.

## Minimum success criteria
- Both workflow files present in target repository.
- At least one failing test case is proven to block merge.
- At least one passing test case is proven to allow merge.
