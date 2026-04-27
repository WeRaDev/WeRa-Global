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
- `kb-governance/formal-proofs/**/*.lean`

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
9. TRL6 formal proof contract gate
   - Every changed operational KB document must include a `formal_proof` block with `engine: ml-hilbert`, `trl_phase: TRL6`, `obligation_id`, `proof_artifact`, and `verification_status`.
   - Referenced proof artifact must be a repository-relative Lean file with no `sorry`.
   - Proof artifact must declare `proof_engine: ml-hilbert` and reference the same obligation ID.
10. Legacy numbered-doc freeze gate (Phase A)
   - Top-level numbered source docs under `KnowledgeBase/` are frozen to the approved allowlist.
   - New numbered docs at `KnowledgeBase/<NN>-*.md` must be migrated into canonical `KnowledgeBase/kb-*/docs/...` paths instead of being added at top level.
11. Canonical index/link cutover gate (Phase C)
   - `KnowledgeBase/README.md` File Index must reference existing canonical paths.
   - README numeric index rows must not reference top-level legacy numbered files.
   - Wiki seed indexes (`Home`, `Domain-Index`, `Governance-Index`) must resolve to existing canonical repository markdown targets.
12. Migration contract and drift gate (Phase D)
   - Canonicalized entries in `kb-governance/migration/kb-legacy-map-v1.yaml` must pass `kb_migrate_legacy_docs.py --mode verify` for both `move` and `mirror_stub` modes.
   - Periodic drift detection workflow must execute canonical/routing/proof/index/migration checks and emit a consolidated report.

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
- `.gitea/workflows/kb-formal-proof-trl6.yml`
- `.gitea/workflows/kb-drift-detection.yml`

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
