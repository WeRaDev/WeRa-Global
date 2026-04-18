# ADR 0001: KB Upgrade v3 Single-Repository KnowledgeBase + Wiki
Date: 2026-04-17
Status: Accepted (amended in place)
Decision owners: WeRa Capital, WeRa STAK, WeRa Association
## Context
Earlier execution moved to immediate split repositories (`kb-*`). Latest scope clarification requires one canonical repository architecture:
- canonical source of truth in umbrella `KnowledgeBase/`,
- domain partitioning by folders inside `KnowledgeBase/`,
- Gitea wiki as human-facing navigation/operations layer,
- split repositories retained only as temporary migration staging/history.
The upgraded model must:
- preserve canonical naming from vocabulary standards in `21`,
- keep evidence/provenance discipline,
- enforce privacy-safe case handling,
- route decisions by temporal curation authority,
- keep markdown structure and metadata contract ready for later TRL4-TRL5 automation validation (`KB + mempalace + openfang`).
## Decision
1. Canonical KB remains in `KnowledgeBase/` in the umbrella repository.
2. Domain segmentation is implemented as folders under `KnowledgeBase/`:
   - `kb-customers`, `kb-channels`, `kb-value-proposition`, `kb-solution`,
   - `kb-revenue-streams`, `kb-key-resources`, `kb-key-activities`, `kb-key-partners`,
   - `kb-cost-structure`, `kb-problem`, `kb-metrics`, `kb-unfair-advantage`, `kb-governance`.
3. Existing split `kb-*` repositories are frozen as migration staging/history and are not canonical authoring targets.
4. Gitea wiki is enabled as human-facing navigation and operational index layer; canonical records stay in repository markdown.
5. Governance remains composed of three temporal branches:
   - WeRa Capital (executive/current)
   - WeRa STAK (judicial/past)
   - WeRa Association (legislative/future)
6. Approval routing policy remains:
   - `temporal_scope=current` => Capital board approval.
   - `temporal_scope=past` => STAK board approval.
   - `temporal_scope=future` => Association board approval.
   - `temporal_scope=mixed` => multi-entity approval, for example
    - Canonical naming/taxonomy changes => three-entity approval required.
7. Current scope is readiness for later automation testing, not production autonomous operation:
   - structured markdown + metadata contract now,
   - mempalace/openfang operational automation deferred to TRL4-TRL5 validation.
## Consequences
Positive:
- Restores single canonical source of truth for project knowledge.
- Aligns human workflows (manual read/write with governance permissions) with one repository and one wiki surface.
- Preserves current split work as reusable migration history rather than discarding it.
- Keeps agent-readiness progression explicit and testable.
Trade-offs:
- Requires consolidation work from split staging paths back into canonical `KnowledgeBase/`.
- Requires careful transition labeling to avoid dual-source confusion.
- Delays production-grade agentic automation until validation gates pass.
Required controls:
- Canonical path policy (`KnowledgeBase/` only).
- Split-staging freeze policy.
- Provenance-preserving consolidation index.
- Merge-blocking checks for naming, metadata, provenance, evidence status, and privacy boundaries.
## Implementation notes
- Execution order is defined in `kb-governance/instructions/WERA-KB-UPGRADE-V3.md`.
- Current sprint realignment sequence is defined in `kb-governance/tasks/sprints/2026-16.md`.
- Realignment work is executed on review branch `feat/kb-single-repo-wiki-realignment` before merge to `main`.
