# Pilot Chain Metadata Normalization Checklist v1
version: 1.0
status: ready
owner: domain stewards
scope: SPLIT-09

## Purpose
Standardize metadata and dependency blocks on first operational migration chain:
- customers
- partners
- revenue
- metrics
- open questions

## Target destination files
- `kb-customers/docs/gtm/07-customers-and-gtm.md`
- `kb-key-partners/docs/partnerships/08-partnerships.md`
- `kb-revenue-streams/docs/model/03-business-model.md`
- `kb-metrics/docs/financial/13-financial-model.md`
- `kb-governance/docs/open-questions/12-open-questions.md`

## Required normalization fields
Each file must include:
- `primary_domain`
- `secondary_domains`
- `temporal_scope`
- `evidence_status` baseline
- `upstream dependencies`
- `downstream dependencies`
- `validation hooks`
- provenance block (`actor`, `source`, `confidence`, `review_status`)

## Chain integrity checks
1. `customers -> partners` reference exists and is current.
2. `partners -> revenue` reference exists and pricing dependency is explicit.
3. `revenue -> metrics` reference exists and formula source is explicit.
4. `metrics -> open-questions` exception routing is explicit.
5. No contradictory qualification rule remains.

## Completion criteria
- All five target files contain the required fields.
- All five chain integrity checks pass.
- Any unresolved contradiction is logged in open questions with owner and due action.
