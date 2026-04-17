# Nextcloud Human Operations Integration Contract v1
version: 1.0
status: active-draft
owner: operations steward
scope: REALIGN-08

## Purpose
Define governed integration touchpoints between canonical KB markdown and Nextcloud apps used by human operators (`Projects`, `Tasks`, `Calendar`, `Talk`).

## Canonical boundaries
1. Canonical source records remain in `KnowledgeBase/`.
2. Nextcloud stores operational coordination context, not canonical source-of-truth records.
3. Any decision-critical content must be written back to canonical KB markdown through governed repository workflow.

## Supported touchpoints

### Projects
- Project records may reference canonical KB artifacts using repository paths.
- Required reference fields:
  - `kb_primary_ref` (single canonical path),
  - `kb_secondary_refs` (optional list),
  - `temporal_scope`.

### Tasks
- Task entries must reference either:
  - canonical KB document path, or
  - governance event path.
- Task closure requires:
  - evidence status assignment (`verified`, `unverified`, `hypothesis`),
  - trace to canonical update PR/commit when content changed.

### Calendar
- Governance cadence events (weekly/monthly/quarterly) are mirrored from workflow policy.
- Calendar events include:
  - review scope,
  - owner role,
  - canonical reference set.

### Talk
- Talk channels support discussion and coordination.
- Binding decisions from Talk must be captured in canonical markdown event records.

## Permissions and approval boundaries
1. WeRa Capital governs `temporal_scope=current`.
2. WeRa STAK governs `temporal_scope=past`.
3. WeRa Association governs `temporal_scope=future`.
4. Mixed-scope or taxonomy changes require multi-entity approval.
5. Nextcloud users may coordinate work items, but canonical KB changes still require repository governance flow.

## Minimal metadata exchange contract
For every synchronized operational item:
- `kb_ref_path`
- `primary_domain`
- `temporal_scope`
- `evidence_status`
- `owner_role`
- `review_due_date`
- `governance_event_ref` (if applicable)

## Out of scope for this sprint
- Automated bidirectional sync implementation.
- Autonomous write-backs from apps to canonical KB.
- Production-grade webhook orchestration.

## Validation checklist
1. Sample project/task/calendar/talk workflows reference canonical paths.
2. Approval routing is traceable by temporal scope.
3. Decision-critical outcomes are persisted in canonical KB markdown.
