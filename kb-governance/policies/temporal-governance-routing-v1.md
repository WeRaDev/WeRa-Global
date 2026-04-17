# Temporal Governance Routing Policy v1
version: 1.0
status: active-draft
owner: Three-entity governance council (WeRa Capital / WeRa STAK / WeRa Association)
applies_to: All split KB repositories

## Purpose
Define executable governance routing for KB changes by temporal curation intent, aligned to the approved three-entity model.

## Governance entities
- WeRa Capital: executive branch, curation of current processes.
- WeRa STAK: judicial branch, curation of past processes.
- WeRa Association: future branch, curation of future processes.

## Mandatory metadata contract
Every changed KB document must include:
- `temporal_scope`: `current | past | future | mixed`
- `primary_domain`
- `secondary_domains`
- `evidence_status`
- `provenance.actor`
- `provenance.source`
- `provenance.confidence`
- `provenance.review_status`

## Approval routing matrix
- `temporal_scope=current` => WeRa Capital approval required.
- `temporal_scope=past` => WeRa STAK approval required.
- `temporal_scope=future` => WeRa Association approval required.
- `temporal_scope=mixed` => approvals required from all impacted entities.

## Hard-gate change classes
The following always require three-entity approval regardless of temporal scope:
- Canonical naming and alias policy changes.
- Domain taxonomy changes.
- Cross-repository governance process changes.
- Privacy-boundary rule changes.

## Conflict adjudication protocol
If approvals conflict:
1. Open governance event in `kb-governance/events/`.
2. Record conflicting rationale with evidence labels.
3. Assign adjudication owner from WeRa STAK.
4. Publish binding decision and supersession reference.

## Operational integration
- Review routing is a merge gate requirement for protected `main` branches.
- CI policy checks enforce presence and validity of `temporal_scope`.
- Missing temporal metadata blocks merge.

## Rollout sequence
1. Apply this policy to `kb-governance` first.
2. Propagate to all domain repositories.
3. Validate with one mixed-scope pilot change before broad migration.
