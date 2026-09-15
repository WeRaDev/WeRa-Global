---
metadata:
  primary_domain: cost-structure
  secondary_domains: [key-resources, revenue-streams]
  owner_role: Founder/Consultant
  temporal_scope: future
  evidence_status: hypothesis
  last_reviewed_at: 2026-09-15
  next_review_due: 2026-12-15
  provenance:
    actor: agent-warp
    source: analysis
    confidence: low
    review_status: draft
---

# Cost Structure

## Purpose
Identify Human Center's cost categories, as input to pricing decisions.

## Scope
- In scope: cost categories expected to apply to a solo AI-automation consultancy.
- Out of scope: an actual quantified cost model (not yet built).

## Current State
- No quantified cost model exists yet.
- Candidate cost categories: LLM/API usage, workflow-orchestration hosting (n8n/Make/Zapier), EU-hosted storage and backups, founder time (primary cost as a solo consultancy), tooling/subscriptions, marketing and the `www.inteligente.site` website.
- Economy-of-scale note (from pricing research on comparable vendors): shared authentication, hosting, AI API access, logging, and monitoring infrastructure reduces the marginal cost of delivering additional workflow types to the same client, which is why combined packages (e.g. accounting + email) are priced below the sum of their parts.

## Decisions / Rules
- Do not finalize pricing tiers in `../../../kb-revenue-streams/docs/model/07-revenue-streams.md` until an actual cost model exists.

## Evidence
- `../../../../Resources/Documents/Research/HumanCenter.Pricing.md` — unverified, notes the shared-infrastructure economy-of-scale effect for comparable vendors.

## Cross-Domain Links
- Related domains: `kb-key-resources`, `kb-revenue-streams`
- Related documents: `../../../kb-key-resources/docs/architecture/05-key-resources.md`, `../../../kb-revenue-streams/docs/model/07-revenue-streams.md`

## Open Actions
- Build an actual, quantified cost model, owner: Founder/Consultant, due: see `../../../../tasks/backlog.md` HC-003.
