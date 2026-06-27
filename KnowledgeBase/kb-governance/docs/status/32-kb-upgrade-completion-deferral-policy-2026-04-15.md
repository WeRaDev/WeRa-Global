# 32 — KB Upgrade Completion and Deferral Policy (2026-04-15)

## Consolidation provenance
- consolidation_actor: `WARP`
- consolidation_source: `KnowledgeBase/32-KB-Upgrade-Completion-and-Deferral-Policy-2026-04-15.md`
- consolidation_date: `2026-04-27`
- consolidation_status: `canonicalized`


---

## Decision Statement

The current KB-upgrade cycle is declared **complete** for governance, structure, and benchmark-method assurance scope.
Unresolved analytical and extended validation items are intentionally moved to a post-upgrade execution lane.

This decision is based on completion of:
- governance and workflow hardening (`24`, `27`, `28`)
- benchmark-method verification evidence at sampled and expanded scope (`29`, `30`)
- cross-repo TRL4 planning alignment in `ProductionBase/SolarSeed-v3/WARP.md`

---

## Scope Boundary for This Completion

Included in completion scope:
- KB governance workflow enforcement and security controls
- reproducible containerized benchmark method validation
- documentation/index alignment for upgrade status and policy

Excluded from completion scope (deferred):
- full-scope benchmark reproducibility as a mandatory closure gate
- local CLI/MCP compatibility validation when local path is not baseline-required
- unresolved business/operational questions that are non-blocking for KB-upgrade closure

---

## Amendment (2026-04-24): v3.2 Bridge Policy

1. `WeRa Global AI-Native KB  Complete Agent-Focused Setup & Configuration Instructions.md` is classified as a research-proposal input and not as direct rollout plan.
2. Implementation transition is constrained by `33-KB-AI-Native-Bridge-v3.2-2026-04-24.md`.
3. DAO/SBT execution scope is deferred until KPI stabilization is achieved.
4. KPI stabilization gates for autonomy expansion:
   - customer pipeline >= `10`,
   - CapEx funding secured >= `€500000`,
   - stable monthly income flow >= `€500`.
5. Before KPI stabilization, AI actions are limited to low-risk tasks only (lead generation and customer outreach).
6. Controlled hybrid services are allowed where ROI is clear, but each approval must include:
   - quantified ROI hypothesis and validation horizon,
   - sovereignty impact assessment,
   - rollback plan and owner.

---

## Unresolved Questions Handling Policy

1. `12-Open-Questions.md` remains the authoritative unresolved-question registry.
2. Unresolved items are classified as:
   - immediate blocker (must be handled in current delivery scope), or
   - deferred post-upgrade (owned and scheduled, but non-blocking for KB-upgrade closure).
3. Deferred items must include owner and next action with evidence-label discipline (`verified`, `unverified`, `hypothesis`).
4. Deferred status does not reduce verification standards when item execution occurs.

### Registry canonicalization amendment

- Canonical unresolved-question registry path is now:
  - `KnowledgeBase/kb-governance/docs/open-questions/12-open-questions.md`
- `KnowledgeBase/12-Open-Questions.md` remains as a compatibility mirror/index entry and must reference the canonical path.

---

## MemPalace Policy for This Cycle

1. MemPalace integration remains in **TRL4 testing scope** for this cycle.
2. Hardened benchmark and security controls in `27` remain mandatory whenever benchmark validation is performed.
3. Q29/Q32 may be advanced via post-upgrade TRL4 test runs, but their outstanding evidence work does not reopen KB-upgrade completion status.
4. Production-wide dependency elevation requires explicit future governance decision and evidence package.

---

## Governance and Traceability Requirements

- `README`, `31`, and `12` must remain consistent with this decision.
- `24` governance workflow must enforce explicit deferred-vs-blocking classification.
- Any future status change to this policy requires governance PR review and documented rationale.

---

## Immediate Operating Instructions

1. Treat this document as canonical completion decision for the current KB-upgrade thread.
2. Execute deferred items through normal sprint/governance cadence.
3. When deferred items are resolved, update `12` and publish a governance event if scope or policy shifts.

formal_proof:
  engine: ml-hilbert
  trl_phase: TRL6
  obligation_id: kb.governance.status_32_kb_upgrade_completion_deferral_policy_2026_04_15
  proof_artifact: kb-governance/formal-proofs/governance-status-32-kb-upgrade-completion-deferral-policy-2026-04-15.lean
  verification_status: verified
