---
metadata:
  primary_domain: key-resources
  secondary_domains: [key-activities, cost-structure]
  owner_role: Founder/Consultant
  temporal_scope: current
  evidence_status: verified
  last_reviewed_at: 2026-09-15
  next_review_due: 2026-12-15
  provenance:
    actor: agent-warp
    source: "Inteligente/Resources/Documents/Research/Human Center — Product 1  Shrinking AI  Desk Research, Heuristic Evaluation &amp; Competitive Analysis.md"
    confidence: high
    review_status: draft
---

# Key Resources

## Purpose
List the resources Shrinking AI depends on for delivery.

## Scope
- In scope: the facilitation framework, expertise, and infrastructure the session flow depends on.
- Out of scope: a built-automation tech stack (not the core product; see `../../../kb-solution/docs/strategy/02-solution.md`) — that stack is the Automation Center product line's own resource set, see `06-automation-center-key-resources.md`.

## Current State
- **The RCGFC framework** (Role, Context, Goal, Format, Constraints): the core proprietary-in-use facilitation method for the paid structured session. This is the single most important resource — it is the product's methodology, not just a tool.
- **Founder/consultant facilitation expertise**: applying Design Thinking (empathize/define) and Theory-of-Constraints-informed discovery to identify a client's actual bottleneck.
- **Booking/scheduling infrastructure**: a lightweight scheduler (Calendly-style embed) plus a qualification micro-form, following the boutique-agency benchmark pattern (see `../../../kb-channels/docs/gtm/11-channels.md`).
- **Knowledge asset**: the existing desk-research library under `../../../../Resources/Documents/Research/` (problem validation, competitive analysis, pricing benchmarks).
- **Data infrastructure (candidate, not yet committed)**: EU-hosted infrastructure / Nextcloud-style data residency, following the pattern already used elsewhere in the WeRa Global ecosystem (e.g. `ProductionBase/FilantropiaSolar`'s Nextcloud integration) — relevant primarily if/when optional implementation support is delivered.

## Decisions / Rules
- No workflow-automation vendor/stack (n8n/Make/Zapier) is required for Shrinking AI itself; that stack belongs to the Automation Center product line, not Shrinking AI's core session product.

## Evidence
- `../../../../Resources/Documents/Research/Human Center — Product 1  Shrinking AI  Desk Research, Heuristic Evaluation &amp; Competitive Analysis.md` — verified, defines the RCGFC framework as the core deliverable/methodology.
- `../../../../Resources/Documents/Research/HumanCenter.Pricing.md` — verified as the Automation Center product line's own resource evidence (n8n/Make/Zapier + LLM APIs); not part of Shrinking AI's resource set.

## Cross-Domain Links
- Related domains: `kb-key-activities`, `kb-cost-structure`, `kb-channels`
- Related documents: `../../../kb-key-activities/docs/execution/04-key-activities.md`, `../../../kb-cost-structure/docs/model/08-cost-structure.md`, `../../../kb-channels/docs/gtm/11-channels.md`

## Open Actions
- Record a stack-selection ADR for booking/scheduling infrastructure, owner: Founder/Consultant, due: see `../../../../tasks/backlog.md` HC-002.
