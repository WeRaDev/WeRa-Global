---
metadata:
  primary_domain: governance
  secondary_domains: []
  owner_role: Founder/Consultant
  temporal_scope: current
  evidence_status: verified
  last_reviewed_at: 2026-09-15
  next_review_due: 2026-12-15
  provenance:
    actor: agent-warp
    source: umbrella BOOTSTRAP.md / KnowledgeBase conventions
    confidence: high
    review_status: draft
---

# Glossary

## Purpose
Define terms used across the Inteligente knowledgebase and project scaffold.

## Scope
- In scope: terms specific to how this repository is organized and governed.
- Out of scope: general AI/automation industry terminology.

## Current State
- **BMC domain (`kb-*`)**: a top-level folder representing one Business-Model-Canvas / Lean-Canvas block (e.g. `kb-problem`, `kb-revenue-streams`).
- **ADR**: Architecture (or business) Decision Record, stored under `docs/adr/`.
- **DoR / DoD**: Definition of Ready / Definition of Done, as defined in `../../../../CONTRIBUTING.md`.
- **`native` vcs_mode**: the project's code/docs are versioned directly inside the `WeRa-Global` umbrella repository, rather than as a separate Gitea repo/submodule (see `ProductionBase/repos.yaml`).
- **`evidence_status`**: a required KB-document metadata field (`verified|unverified|hypothesis`) declaring how well-supported a claim is.
- **Human-in-the-loop / human approval**: a mandatory design constraint (per `../../../../SOUL.md`) requiring explicit human confirmation before any financially or legally consequential automated action executes.

## Decisions / Rules
- New domain-specific terms should be added here rather than redefined ad hoc in individual documents.

## Evidence
- `../../../../../BOOTSTRAP.md` (umbrella `ProductionBase/BOOTSTRAP.md`) — verified, defines the baseline/ADR/DoR/DoD conventions this project follows.

## Cross-Domain Links
- Related domains: all
- Related documents: `../../../../README.md`, `../../../../CONTRIBUTING.md`

## Open Actions
- None currently.
