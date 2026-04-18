# WeRa Global KB Upgrade Plan v3
document_id: WERA-KB-UPGRADE-V3
version: 3.1
status: APPROVED-DRAFT-REALIGNED
scope: Single-repository `KnowledgeBase/` architecture + wiki readiness + governance + quality gates
authoritative_owner: Three-entity governance council (Capital/STAK/Association)
## 1. Problem statement
WeRa requires an executable KB upgrade plan that preserves governance rigor and agent-readiness while restoring one canonical source of truth in the umbrella repository.
The canonical source of truth is:
- one repository (`WeRa-Global`),
- one canonical KB root (`KnowledgeBase/`),
- domain partitioning by folders (not by separate repositories),
- a Gitea wiki surface for human-readable navigation and governance-controlled manual operations.
## 2. Locked directives
1. Canonical KB source of truth is `KnowledgeBase/` in the umbrella repository.
2. Domain partitioning is implemented as folders inside `KnowledgeBase/` (not separate `kb-*` repositories).
3. Existing split `kb-*` repositories are frozen as migration staging/history and are not canonical authoring targets.
4. Canonical naming is enforced according to `KnowledgeBase/21-KB-Controlled-Vocabulary-and-Entity-Standards-v1.md`.
5. Temporal governance remains split across three entities:
   - WeRa Capital: executive branch, current-process curation
   - WeRa STAK: judicial branch, past-process curation
   - WeRa Association: future branch, future-process curation
6. Current development scope is structured markdown + metadata contract readiness for later agentic automation (`KB + mempalace + openfang`) in TRL4-TRL5 testing.
7. Weekly cadence remains the execution rhythm.
## 3. Canonical topology (single repository)
### 3.1 Canonical KB root
`KnowledgeBase/` remains the only canonical KB location.
### 3.2 Domain folder model inside `KnowledgeBase/`
1. `KnowledgeBase/kb-customers/`
2. `KnowledgeBase/kb-channels/`
3. `KnowledgeBase/kb-value-proposition/`
4. `KnowledgeBase/kb-solution/`
5. `KnowledgeBase/kb-revenue-streams/`
6. `KnowledgeBase/kb-key-resources/`
7. `KnowledgeBase/kb-key-activities/`
8. `KnowledgeBase/kb-key-partners/`
9. `KnowledgeBase/kb-cost-structure/`
10. `KnowledgeBase/kb-problem/`
11. `KnowledgeBase/kb-metrics/`
12. `KnowledgeBase/kb-unfair-advantage/`
13. `KnowledgeBase/kb-governance/`
### 3.3 Human-facing wiki layer
Gitea Wiki is the navigation and operational interaction surface for humans:
- knowledge navigation pages,
- governance process pages,
- operational runbooks and index pages.
Wiki pages do not replace canonical records; they index and reference canonical markdown in `KnowledgeBase/`.
## 4. Reusable artifact synthesis map
### 4.1 Direct adoption baseline
- `KnowledgeBase/18-KB-MemPalace-Critical-Review-and-Action-Plan.md`
- `KnowledgeBase/19-KB-Domain-Taxonomy-Map-v1.md`
- `KnowledgeBase/20-KB-File-to-Domain-Ownership-Map-v1.md`
- `KnowledgeBase/21-KB-Controlled-Vocabulary-and-Entity-Standards-v1.md`
- `KnowledgeBase/22-KB-Anonymized-Case-Schema-and-Lifecycle-v1.md`
- `KnowledgeBase/24-KB-Governance-Workflows-v1.md`
- `KnowledgeBase/25-KB-Cross-Domain-Integration-Matrix-v1.md`
- `KnowledgeBase/26-KB-Validation-Protocol-v1.md`
- `KnowledgeBase/templates/KB-Domain-Document-Template-v1.md`
- `KnowledgeBase/templates/KB-Governance-Event-Template-v1.md`
### 4.2 Adopt with adaptation
- `KnowledgeBase/23-KB-Domain-Template-Pack-v1.md` adapted to folderized single-repo layout.
- Pilot chain metadata blocks from:
  - `KnowledgeBase/03-Business-Model.md`
  - `KnowledgeBase/07-Customers-and-GTM.md`
  - `KnowledgeBase/08-Partnerships.md`
  - `KnowledgeBase/12-Open-Questions.md`
  normalized into one metadata contract for future automation.
### 4.3 Deferred (non-blocking for current scope)
- Benchmark/security lane artifacts:
  - `KnowledgeBase/27-...` through `KnowledgeBase/32-...`
  - `KnowledgeBase/tools/run_mempalace_longmemeval_docker.sh`
  - `KnowledgeBase/tools/security_checks_onnx.sh`
- Production agent runtime automation rollout (mempalace/openfang integration) remains deferred until TRL4-TRL5 validation phase.
## 5. Governance architecture: three entities
## 5.1 Governance requirements
- Traceable provenance for high-impact changes
- Evidence classification for decision-critical claims
- Temporal accountability across current/past/future process curation
- Cross-domain consistency and privacy-safe case handling
## 5.2 Branch responsibility model
- WeRa Capital (executive/current): active operating process curation and current-state decisions.
- WeRa STAK (judicial/past): historical records, audits, incident logs, superseded decisions, contradiction adjudication.
- WeRa Association (future): hypotheses, roadmap decisions, deferred tracks, future-state architecture.
## 5.3 Approval routing policy
- `temporal_scope=current` => WeRa Capital approval required.
- `temporal_scope=past` => WeRa STAK approval required.
- `temporal_scope=future` => WeRa Association approval required.
- `temporal_scope=mixed` => approval required from all impacted entities.
- Canonical naming or taxonomy rule changes => three-entity approval required.
## 6. Agent-facing surface (current plan scope)
`KnowledgeBase/` content must be structured for future automation, but remains human-governed markdown now.
Required metadata contract on operational records:
- `primary_domain`
- `secondary_domains`
- `temporal_scope`
- `evidence_status`
- `upstream dependencies`
- `downstream dependencies`
- `validation hooks`
- provenance block (`actor`, `source`, `confidence`, `review_status`)
Current scope outcome:
- machine-readable markdown ready for later `KB + mempalace + openfang` validation (TRL4-TRL5),
- without committing to production autonomous write actions in this phase.
## 7. Realigned implementation phases
## Phase 0: Realignment lock and branch policy
Objective:
- lock single-repo canonical architecture and freeze split repos as staging history.
Outputs:
- updated plan and ADR,
- branch-based delivery policy (`feat/kb-single-repo-wiki-realignment`).
## Phase 1: Folderized KB topology in `KnowledgeBase/`
Objective:
- scaffold and validate domain folder layout inside canonical KB root.
Outputs:
- domain folder structure present,
- ownership and metadata starter files.
## Phase 2: Consolidation from split staging into canonical KB
Objective:
- move/mirror migrated artifacts from split staging work into canonical `KnowledgeBase/` folders with provenance.
Outputs:
- split-to-canonical consolidation index,
- pilot chain and direct-adoption artifacts in canonical paths.
## Phase 3: Wiki information architecture
Objective:
- initialize Gitea wiki structure as human navigation and governance portal.
Outputs:
- wiki home and domain index pages,
- governance workflow index pages linked to canonical markdown.
## Phase 4: Human operations integration contract
Objective:
- define practical repo/wiki linkage patterns for manual and semi-automated operations.
Outputs:
- Nextcloud integration contract (projects/tasks/calendar/talk linkage model),
- permission and workflow boundaries for human operators.
## Phase 5: Agent-readiness contract (TRL4-TRL5 prep)
Objective:
- finalize metadata and interface readiness for future agentic testing.
Outputs:
- mempalace/openfang readiness checklist,
- MCP/skills interface contract against canonical markdown structure.
## Phase 6: Single-repo quality gates
Objective:
- enforce policy and metadata checks in one repository with path/domain targeting.
Outputs:
- merge-blocking checks for naming, metadata, provenance, evidence labels, and privacy boundaries.
## Phase 7: Pilot chain validation and governance review
Objective:
- validate customers -> partners -> revenue -> metrics -> open-questions chain in canonical KB paths.
Outputs:
- pilot chain consistency report,
- contradiction routing record with owner and due action.
## 8. Acceptance criteria
1. Canonical KB source of truth is `KnowledgeBase/` in the umbrella repository.
2. Domain segmentation is implemented as folders in `KnowledgeBase/`, not separate canonical repos.
3. Split `kb-*` repositories are explicitly marked as frozen staging/history.
4. Structured markdown metadata contract is present on required operational records.
5. Governance routing by temporal scope is active and auditable.
6. Wiki layer is initialized as human navigation surface linked to canonical markdown.
7. Agentic automation readiness for TRL4-TRL5 is documented without premature production autonomy.
## 9. Risks and mitigations
- Risk: confusion between canonical and staging sources.
  - Mitigation: explicit freeze policy and canonical path policy.
- Risk: migration drift while consolidating split artifacts.
  - Mitigation: provenance-preserving consolidation index and review checkpoints.
- Risk: governance ambiguity during transition.
  - Mitigation: mandatory temporal metadata and three-entity approval routing.
- Risk: over-scoping agent runtime before validation.
  - Mitigation: enforce readiness-only scope for current phase.
## 10. Operational ownership
- Governance policy authority: Capital/STAK/Association council.
- Operational curation authority: domain stewards under entity-specific approval policy.
- CI/CD enforcement authority: technical steward delegated by governance council.
## 11. Plan file targets
- Canonical plan: `kb-governance/instructions/WERA-KB-UPGRADE-V3.md`
- Decision record: `kb-governance/docs/adr/0001-kb-upgrade-v3-immediate-split.md`
- Sprint execution: `kb-governance/tasks/sprints/`
## 12. Verification baseline against attached complete document
Verification source:
- `/Users/mikhailananyin/Documents/WeRa materials/WeRa Global KB Upgrade — Complete Final Document.md` (`document_id: WERA-KB-COMPLETE-V1`)
### 12.1 Aligned directives retained in this roadmap
- Sovereign self-hosted architecture and governance-first execution posture are retained.
- 12-domain model plus governance meta-domain intent is retained, implemented inside canonical `KnowledgeBase/` folders.
- Structured metadata/provenance and temporal governance routing are retained as mandatory policy signals.
- Quality-gate enforcement and steward-governed review flow are retained as merge-control mechanisms.
### 12.2 Controlled deviations from attached document
- Canonical topology:
  - Attached document Section 2.4 prescribes 13 standalone repositories.
  - This roadmap enforces one canonical repository root (`KnowledgeBase/`) with folderized domains and treats split repositories as frozen staging/history.
- Cadence:
  - Attached document Section 10.1 defines a fixed 2-week sprint line.
  - This roadmap follows weekly sprint cadence under umbrella governance policy.
- Delivery scope sequencing:
  - Attached document includes full stack rollout tracks (Nextcloud/Odoo/Forkbomb/MemPalace runtime operations).
  - This roadmap sequences contracts/readiness first, with runtime autonomy and production integrations deferred to TRL4-TRL5 validation tracks.
- Branch strategy normalization:
  - Attached document references a literal `drafts/` branch strategy.
  - This roadmap applies governed PR-based branch workflows compatible with current repository policy and CI controls.
### 12.3 Phase verification status (as of sprint 2026-18)
- Completed:
  - Phase 0: realignment lock and branch policy.
  - Phase 1: folderized KB topology.
  - Phase 2: consolidation from split staging to canonical paths.
  - Phase 3: wiki information architecture initialization.
  - Phase 4: human operations integration contract.
  - Phase 5: agent-readiness contract baseline.
- Advanced/in progress:
  - Phase 6: quality-gate workflows/scripts are active and now include fixture-based reject/accept proof.
  - Phase 7: pilot-chain governance review is active with contradiction routing and runner-backed CI evidence trail.
### 12.4 Verification evidence trail
- `kb-governance/tasks/sprints/2026-16.md`
- `kb-governance/tasks/sprints/2026-17.md`
- `kb-governance/tasks/sprints/2026-18.md`
- `KnowledgeBase/kb-governance/docs/events/2026-04-17-realign-11-canonical-pilot-chain-review.md`
- `KnowledgeBase/kb-governance/docs/events/2026-04-18-follow-01-runner-ci-phase-advance-review.md`
