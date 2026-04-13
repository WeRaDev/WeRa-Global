# 17 — Execution Readiness and Next 30 Days

---

## Purpose

This document translates strategic-session findings into an execution-first operating layer for the KB. It defines what must happen first, what can run in parallel, and what must be true before re-entering intensive investor outreach.

---

## Current State Snapshot

- Strategic clarity improved, but execution readiness remains the bottleneck.
- Solar-first framing is accepted, but cloud/platform narrative creep remains a live risk.
- GTM channel readiness is asymmetric:
  - installer-backlog channel can run now
  - institutional/association channel requires legal trust signals
- Data quality issue is mostly traceability and proxy-data dependence, not total data absence.
- Delivery readiness is not yet proven for repeated multi-object execution.

---

## Priority Sequence (0–30 Days)

### Priority 1 (Immediate): Installer-Backlog Outreach

Objective: acquire qualified declined-clients pipeline fast.

Actions:
- Contact Portuguese installers directly
- Request clients who wanted installations but dropped due to upfront CAPEX
- Pre-qualify for lease viability and installation constraints

Expected output:
- first object list with status and estimated conversion likelihood

### Priority 2 (Parallel): Delivery-Path Validation

Objective: reduce execution risk before scaling claims.

Actions:
- Qualify at least one backup installer
- Validate one backup equipment path (lead times + procurement reliability)
- Document proposal and installation SLA assumptions

Expected output:
- minimum delivery-reliability baseline for 5–10 object scenario

### Priority 3 (After 1+2): Object-Level Investor Re-Engagement

Objective: move from abstract raise to asset-backed financing conversation.

Actions:
- Build object-level package (see section below)
- Re-engage investor leads with concrete object economics

Expected output:
- investor conversation based on measurable per-object cashflow, not only top-down model

---

## Minimum Object-Level Investor Package

- Qualified object list (customer/site, stage, expected timeline)
- CAPEX per object (equipment, installation, contingency)
- Lease terms per object (duration, monthly amount, customer savings)
- Expected cashflow per object (base and downside/default scenario)
- Delivery proof (installer + backup path available)

---

## Narrative Discipline Rule

- **Now:** lead with financing + leasing + concrete object economics
- **Later:** expand to cloud/platform sovereignty upside

Rule: long-horizon platform vision is strategic context, not the first conversion payload for current investor conversations.

---

## Operational Risk Controls

### R1. Single-Counterparty Dependency
- Risk: waiting on one installer or one investor creates repeated execution stalls
- Control: parallel outreach and parallel qualification as default operating mode

### R2. Runway Compression
- Risk: execution timeline mismatch with available founder runway
- Control: weekly contingency review and short-cycle pipeline checkpoints

### R3. Delivery-Readiness Gap
- Risk: sales/fundraising claims outpace real installation capacity
- Control: no scale claim without validated backup installer and procurement path

### R4. Proxy-Data Overconfidence
- Risk: assumptions treated as evidence
- Control: explicit label of proxy vs own operating data in each investor artifact

---

## Weekly Cadence

- Weekly execution review focused on:
  - pipeline movement by object stage
  - delivery readiness status
  - runway-sensitive decisions
  - narrative discipline adherence

This cadence exists to prevent strategic clarity from collapsing back into narrative overload or serial waiting patterns.

---

## Version-Control Integrity Rule (Gitea)

- Agent changes must follow **feature branch → pull request → merge**.
- Direct pushes to `main` are disallowed except explicit emergency maintenance.
- Every task delivery must be committed to the Gitea remote for auditability.
- PR description must summarize scope, risks, and validation commands used.
