# TRL4-TRL5 Agent Readiness Contract (KB + mempalace + openfang) v1
version: 1.0
status: active-draft
owner: technical steward
scope: REALIGN-09

## Purpose
Define readiness conditions for validating agentic operations against canonical KB markdown during TRL4-TRL5 without enabling premature production autonomy.

## Scope boundary
- In scope:
  - structured markdown contract validation,
  - read and retrieval behavior checks,
  - governed proposal workflow for potential write actions.
- Out of scope:
  - unrestricted autonomous write operations to canonical KB,
  - production-scale runtime orchestration.

## Canonical interface contract
Operational KB records used by agents must provide:
- `primary_domain`
- `secondary_domains`
- `temporal_scope`
- `evidence_status`
- `upstream dependencies`
- `downstream dependencies`
- `validation hooks`
- provenance fields (`actor`, `source`, `confidence`, `review_status`)

## Runtime role contract

### KB layer
- Acts as canonical source for retrieval and policy-aware reasoning.
- Accepts updates only through governed repository workflow.

### mempalace layer
- Performs retrieval, memory stitching, and context ranking from canonical markdown.
- Must preserve canonical references in generated outputs.

### openfang layer
- Orchestrates agent tasks and tool execution.
- At TRL4, write actions remain proposal-only unless explicitly approved by governance route.

## TRL4 readiness gates
1. Agent can resolve canonical path references for pilot-chain documents.
2. Retrieval outputs preserve provenance and evidence labels.
3. Any proposed update includes temporal scope and approval route.
4. Privacy-safe case handling constraints from `22` are enforced in prompts/tools.

## TRL5 readiness gates
1. Controlled write pilot executes with explicit approval checkpoints.
2. CI quality gates block metadata/provenance violations before merge.
3. Governance event log captures contradictions, decisions, and follow-up actions.
4. Rollback path exists for any automated write pipeline.

## Deferred runtime gates
- Full autonomous write mode stays deferred until:
  - TRL4 and TRL5 readiness gates pass,
  - governance council approves production autonomy policy,
  - audit evidence confirms privacy and naming compliance.

## Validation references
- `KnowledgeBase/kb-governance/docs/validation/26-validation-protocol-v1.md`
- `KnowledgeBase/kb-governance/docs/workflows/24-governance-workflows-v1.md`
- `kb-governance/ci/quality-gates-spec-v2.md`
