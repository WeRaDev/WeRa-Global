# 18 — KB MemPalace Spec: Critical Review and Action Plan

---

## Purpose

This document reviews `KB-memPalace-upgrade.md` as a task specification, identifies critical issues (inconsistencies, unverifiable claims, and implementation risks), and converts it into an actionable, auditable KB upgrade path for WeRa Global.

---

## Critical Findings

### F1. Tooling contradiction: “all local” vs Notion
- The source spec states all data should be local/self-hosted, but lists Notion as a wiki layer option.
- Notion conflicts with sovereign self-hosting requirements.
- **Correction**: limit human-facing wiki layer to self-hosted options only: gitea and mempalace. Human-facing UI is developed separately on top of wiki

### F2. Naming inconsistency with canonical KB
- The source spec uses `Vera Cloud` and `Solar Seed`; canonical KB uses `WERA Cloud` and `SolarSeed`.
- **Correction**: correct canonical names to be: `WeRaCloud` for digital product line where `CityLight` (wera-global/SolarSeed-v3/src/commit/2f68bc548636aa46b0e032e4f618f7f60bae7c9e#solarseed-v3--city-of-light-trl4) is the base product; `WeRaSolar` for physical product line where `SolarSeed` is the base product; enforce canonical names everywhere to prevent taxonomy drift.

### F3. Leasing formula inconsistency (logical conflict)
- Source process defines:
  - `leasing_monthly = max(quoted_price / amortisation_months, bill * 0.80)`
  - and also validates `leasing_monthly ≤ bill * 0.80`.
- These two rules can conflict when amortized cost is above the threshold.
- **Correction**: separate qualification from pricing:
  - `required_leasing = quoted_price / amortisation_months + investment_cost_month * quoted_price / amortisation_months`, where investment_cost_month is calculated from 8% yearly dividends (Logic: we borrow money at 8% yearly to invest in equipment that we are leasing to our customers at 80% of their regular bill that should pay 8% investment cost and generate >0 profit).
  - Deal is qualified only if `required_leasing ≤ bill * 0.80`; otherwise route to exception workflow.

### F4. Unsupported “hard” benchmark claims
- The source file presents specific performance claims (e.g., LongMemEval and retrieval uplift) as established facts without in-repo evidence.
- **Correction**: research https://github.com/mempalace/mempalace to verify the claims.

### F5. Over-prescriptive implementation commands without environment proof
- Source includes CLI/API commands and MCP activation paths that are not validated against current WeRa environment.
- **Correction**: move command blocks into “candidate runbooks” status until tool availability and successful dry-runs are documented.

### F6. Governance write permissions too broad
- “Any agent can write events” creates integrity and provenance risks.
- **Correction**: require write-scoped permissions by wing and mandatory provenance metadata (`actor`, `source`, `timestamp`, `confidence`, `review_status`).

### F7. “Zero isolated rooms” as mandatory KPI is unrealistic at bootstrap
- Early-stage knowledge systems naturally contain isolated nodes during migration.
- **Correction**: use staged tunnel-density targets (baseline, week-1, quarter-1) instead of zero-at-start hard gate.

---

## Corrected Decision Set (Adopt / Reject / Defer)

### Adopt now
- BMC + Lean layered taxonomy (9 core + 3 overlay)
- Case-centric knowledge flow (customer case → channel → partner → offer → revenue → metrics)
- Privacy split (PII outside KB, anonymized case data in KB)
- Cross-reference/tunnel model as design principle (not strict auto-mandate in phase 1)

### Adopt with constraints
- MemPalace as candidate memory engine, subject to technical validation and operational fit
- AAAK-style compressed summaries, but only as a derived layer from verifiable source records

### Reject/replace in current form
- Notion option under “fully local” constraint
- Conflicting leasing equation logic
- Unverified benchmark claims presented as facts
- Broad write access for all agents

### Defer
- Full MCP automation stack until phase-1 structure and provenance model are stable
- Automated tunnel generation as default behavior before taxonomy quality is validated

---

## Actionable KB Upgrade Plan

### Workstream A — Canonical business taxonomy (BMC + Lean)
1. Define canonical directory/taxonomy map for 12 domains.
2. Map existing KB files to domain ownership.
3. Define controlled vocabulary for core entities (products, segments, channels, statuses).

Acceptance:
- Domain map approved.
- Every active KB file mapped to one primary domain owner.

### Workstream B — Case data model and privacy boundary
1. Define anonymized case schema (required fields only).
2. Define PII vault contract (what must never enter KB).
3. Define case lifecycle statuses and transition rules.

Acceptance:
- Schema validated with 2 sample cases.
- PII exclusion checks documented.

### Workstream C — Pricing and qualification integrity
1. Replace conflicting leasing formula with qualification-first rule.
2. Document exception handling when discount rule cannot be met.
3. Align with revenue and partner quote workflows.

Acceptance:
- Formula and decision tree are internally consistent.
- At least one worked example (qualified and unqualified) is documented.

### Workstream D — Evidence and claim governance
1. Introduce evidence labels for all non-trivial claims: `verified`, `unverified`, `hypothesis`.
2. Require citation and reproducibility notes for benchmark/tooling claims.
3. Add quarterly claim-audit task in governance cadence.

Acceptance:
- Existing high-impact claims in KB are labeled.
- No benchmark claim remains unlabeled.

### Workstream E — Agent permissions and provenance
1. Define per-wing write permissions.
2. Require immutable event provenance fields.
3. Add review workflow for AI-written entries.

Acceptance:
- Permission matrix published.
- Provenance fields enforced in templates.

### Workstream F — Implementation sequencing
1. Phase 1: structure + schema + governance.
2. Phase 2: migration of current content to new taxonomy.
3. Phase 3: optional mem-engine integration and MCP activation.

Acceptance:
- Each phase has completion checklist and rollback notes.

---

## Immediate KB Changes Required from This Review

1. Keep MemPalace initiative as **candidate architecture**, not established baseline.
2. Enforce canonical names: `WeRaCloud`:`CityLight` and `WeRaSolar`:`SolarSeed`.
3. Correct leasing logic as qualification rule, not contradictory formula.
4. Research to address questions for benchmark verification, tooling reality, and governance safety.

---

## Definition of Done for This Upgrade Program

- The KB contains a consistent 12-domain operating taxonomy.
- Customer-case data handling is privacy-safe and auditable.
- Core pricing logic is mathematically and operationally consistent.
- All strategic/technical claims have explicit evidence status.
- Agent write operations are permissioned and reviewable.
- The architecture is executable in WeRa’s actual environment, not only in abstract specification.
