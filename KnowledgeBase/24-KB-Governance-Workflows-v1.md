# 24 — KB Governance Workflows v1

---

## Purpose
Define Phase 2 governance workflows that operationalize ownership, quality, and consistency controls for the domain-structured KB.

---

## Workflow 1: Domain Document Intake

1. Submitter chooses primary domain from `19`.
2. Apply metadata block from `23`.
3. Validate terminology against `21`.
4. If case-related, validate schema/privacy against `22`.
5. Route for primary owner review.

Exit criteria:
- Domain assignment confirmed.
- Evidence labels applied.
- Required metadata complete.

---

## Workflow 2: Evidence and Claim Control

1. Identify non-trivial claims in edited document.
2. Assign evidence label (`verified`, `unverified`, `hypothesis`).
3. Attach source references and reproducibility notes where applicable.
4. If label is `unverified` or `hypothesis`, add explicit validation task to `12`.

Exit criteria:
- No unlabeled high-impact claim remains.

---

## Workflow 3: Case-Safety and Privacy Compliance

1. Run field-level check against PII exclusion list (`22`).
2. Confirm only anonymized operational fields are in KB.
3. Check lifecycle status transition validity.
4. Record provenance metadata for AI-authored updates.

Exit criteria:
- No PII in KB records.
- Invalid status transitions blocked or flagged.

---

## Workflow 4: Cross-Domain Change Review

Trigger: document update affects secondary domains.

1. Primary owner marks impacted secondary domains using `20`.
2. Secondary owners review only impacted sections.
3. Resolve conflicts through governance owner arbitration.
4. Record decision in governance log entry.

Exit criteria:
- Primary and impacted secondary owners acknowledged change.

---

## Workflow 5: Scheduled Governance Cadence

### Weekly
- stale-delta check on recently edited docs
- open-question sync (new risks/assumptions to `12`)

### Monthly
- evidence label drift review
- metrics and relationship domain consistency check

### Quarterly
- full taxonomy/ownership audit against `19` and `20`
- controlled vocabulary audit against `21`
- privacy and lifecycle compliance audit against `22`

Exit criteria:
- audit summary published as governance event entry.

---

## Workflow 6: PR Readiness Gate for KB Changes

Before merge:
1. Domain assignment present.
2. Evidence labels and provenance present.
3. Cross-domain impacts acknowledged.
4. Privacy/lifecycle checks passed for case-content.
5. README index updated when new KB files are introduced.

Exit criteria:
- PR approved for merge by governance policy.

---

## Governance Event Log Template

```yaml path=null start=null
governance_event:
  date: YYYY-MM-DD
  workflow: intake|evidence|privacy|cross-domain|cadence|pr-gate
  documents: []
  decisions: []
  open_actions: []
  owner: role
  status: open|closed
```
