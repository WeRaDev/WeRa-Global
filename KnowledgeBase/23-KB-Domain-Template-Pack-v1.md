# 23 — KB Domain Template Pack v1

---

## Purpose
Provide Phase 2 domain-specific templates for the canonical domains defined in `19-KB-Domain-Taxonomy-Map-v1.md`.

---

## Template Usage Rules
- Use one primary domain template per new document.
- Include optional cross-domain blocks when a document affects multiple domains.
- Apply evidence labels (`verified`, `unverified`, `hypothesis`) to non-trivial claims.
- Include provenance block for AI-authored updates.

---

## Domain Templates

### `domain_customers` Template
- Segment definition
- Case-intake criteria
- Anonymized data fields (reference `22`)
- Lifecycle status responsibilities
- Known objections and conversion blockers

### `domain_value_prop` Template
- Problem statement addressed
- Layered offer structure (general line, product line, configured offer)
- Qualification constraints
- Value proof requirements (measured, not assumed)

### `domain_channels` Template
- Channel description and target segment fit
- Execution workflow (human/agent steps)
- KPI thresholds and review triggers
- Failure modes and fallback channel

### `domain_relationships` Template
- Relationship stage definitions
- Contract/LOI dependencies
- Communication cadence and ownership
- Escalation and retention actions

### `domain_revenue` Template
- Pricing rule set
- Qualification logic and exception path
- Invoicing and payment conditions
- Tax/legal dependency notes

### `domain_resources` Template
- Resource scope (hardware/software/data/tooling)
- Version and compatibility constraints
- Supply/availability risk notes
- Validation checklist

### `domain_activities` Template
- SOP objective
- Step-by-step workflow
- Inputs/outputs and handoff conditions
- Stage-gate evidence requirements

### `domain_partners` Template
- Partner profile and scope
- Performance metrics and SLA targets
- Region/product fit
- Risk flags and replacement strategy

### `domain_costs` Template
- Cost model boundaries (CAPEX/OPEX)
- Assumptions and sensitivity factors
- Unit economics linkage
- Monitoring cadence and variance thresholds

### `domain_problems` Template
- Problem/event definition
- Trigger conditions and impact scope
- Root-cause hypotheses
- Linked mitigation initiatives

### `domain_solutions` Template
- Proposed solution and scope
- Validation method and success criteria
- Dependency list and execution order
- Adoption/rollback conditions

### `domain_metrics` Template
- Metric definition and formula
- Data source and owner
- Target band and alert threshold
- Interpretation notes and known caveats

---

## Required Metadata Block (for all domain docs)

```yaml path=null start=null
metadata:
  primary_domain: domain_name
  secondary_domains: []
  owner_role: TBD
  evidence_status: verified|unverified|hypothesis
  last_reviewed_at: YYYY-MM-DD
  next_review_due: YYYY-MM-DD
  provenance:
    actor: human|agent-name
    source: source-id
    confidence: low|medium|high
    review_status: draft|reviewed|approved
```
