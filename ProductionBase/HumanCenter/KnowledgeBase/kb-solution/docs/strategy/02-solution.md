---
metadata:
  primary_domain: solution
  secondary_domains: [problem, value-proposition, key-activities]
  owner_role: Founder/Consultant
  temporal_scope: current
  evidence_status: unverified
  last_reviewed_at: 2026-09-15
  next_review_due: 2026-12-15
  provenance:
    actor: agent-warp
    source: HumanCenter/Resources/Documents/Research/
    confidence: medium
    review_status: draft
---

# Solution

## Purpose
Describe Human Center's solution approach to the problem in `../../../kb-problem/docs/market/01-problem.md`.

## Scope
- In scope: packaged, narrowly-scoped AI-driven automations for specific high-friction workflows.
- Out of scope: open-ended "AI transformation" consulting; automating tax-return filing or other high-risk unsupervised financial/legal decisions.

## Current State
- Delivery approach: packaged automations built with n8n/Make/Zapier-style workflow orchestration plus LLM APIs, targeting specific workflows (email triage/drafting/follow-up; document/receipt OCR + bookkeeping handoff) rather than broad "AI transformation."
- Discovery method: Design Thinking + Theory of Constraints framing is used to identify the client's actual bottleneck before proposing an automation.
- Delivery principles (from desk research on comparable vendors): EU-hosted infrastructure, GDPR compliance, no client data used to train public models, mandatory human approval for financially/legally consequential actions, audit logging.
- A first product idea ("Product 1: Shrinking AI") has an existing desk-research, heuristic-evaluation, and competitive-analysis pass; not yet finalized into a shipped offer.

## Decisions / Rules
- Every proposed automation must map to a validated bottleneck, not a generic AI pitch (see `../../../../SOUL.md`).
- Consequential actions (financial/legal) always require human approval in the workflow design.

## Evidence
- `../../../../Resources/Documents/Research/Shrinking AI (B2B Consultancy) — Desk Research, He.md` — unverified/hypothesis, desk research.
- `../../../../Resources/Documents/Research/Human Center — Product 1  Shrinking AI  Desk Research, Heuristic Evaluation &amp; Competitive Analysis.md` — unverified/hypothesis, desk research.
- `../../../../Resources/Documents/Research/Design Thinking and Theory of Constraints as Remedies for AI Input-Quality and Productivity Aggregation Problems.md` — unverified/hypothesis, desk research.
- `../../../../Resources/Documents/Research/HumanCenter.Pricing.md` — describes comparable vendors' delivery/security posture (EU hosting, human approval, DPA) — unverified, third-party desk research.

## Cross-Domain Links
- Related domains: `kb-problem`, `kb-value-proposition`, `kb-key-activities`
- Related documents: `../../../kb-problem/docs/market/01-problem.md`, `../../../kb-value-proposition/docs/products/02-services.md`, `../../../kb-key-activities/docs/execution/04-key-activities.md`

## Open Actions
- Run heuristic evaluation against the competitor tools already named in desk research, owner: Founder/Consultant, due: before first pilot.
- Finalize the v1 solution scope for the first pilot client, owner: Founder/Consultant, due: see `../../../../tasks/backlog.md` HC-003.
