---
metadata:
  primary_domain: key-resources
  secondary_domains: [key-activities, cost-structure]
  owner_role: Founder/Consultant
  temporal_scope: current
  evidence_status: unverified
  last_reviewed_at: 2026-09-15
  next_review_due: 2026-12-15
  provenance:
    actor: agent-warp
    source: HumanCenter/Resources/Documents/Research/
    confidence: low
    review_status: draft
---

# Key Resources

## Purpose
List the resources Human Center depends on to deliver its service.

## Scope
- In scope: tooling, infrastructure, and expertise currently identified as needed.
- Out of scope: resource decisions not yet made (tracked as Open Actions).

## Current State
- Automation stack (candidate): n8n/Make/Zapier-style workflow orchestration, LLM APIs, OCR/document-extraction tooling.
- Data infrastructure (candidate): EU-hosted infrastructure / Nextcloud-style data residency, following the pattern already used elsewhere in the WeRa Global ecosystem (e.g. `ProductionBase/FilantropiaSolar`'s Nextcloud integration).
- Expertise: founder/consultant expertise in AI automation and process design.
- Knowledge asset: the existing desk-research and pricing-benchmark library under `../../../../Resources/Documents/Research/`.

## Decisions / Rules
- No specific vendor/stack has been contractually committed to yet; treat the "candidate" items above as provisional until an ADR is recorded.

## Evidence
- `../../../../Resources/Documents/Research/HumanCenter.Pricing.md` — unverified, describes typical stacks used by comparable agencies (n8n/Make/Zapier + LLM APIs).

## Cross-Domain Links
- Related domains: `kb-key-activities`, `kb-cost-structure`
- Related documents: `../../../kb-key-activities/docs/execution/04-key-activities.md`, `../../../kb-cost-structure/docs/model/08-cost-structure.md`

## Open Actions
- Record a stack-selection ADR once the first pilot's technical requirements are known, owner: Founder/Consultant.
