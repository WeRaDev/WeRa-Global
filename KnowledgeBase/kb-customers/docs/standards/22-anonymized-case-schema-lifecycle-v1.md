# 22 — KB Anonymized Case Schema and Lifecycle v1
## Consolidation provenance
- consolidation_actor: `WARP`
- consolidation_source: `origin/feat/kb-mempalace-critical-upgrade:KnowledgeBase/22-KB-Anonymized-Case-Schema-and-Lifecycle-v1.md@eba9cbde025e90b389042ae6f2d840763f894e27`
- consolidation_date: `2026-04-17`
- consolidation_status: `canonicalized`


---

## Purpose
Implement Workstream B from `18-KB-MemPalace-Critical-Review-and-Action-Plan.md` by defining:
- the anonymized case schema for KB storage,
- the PII exclusion/vault boundary,
- canonical lifecycle transitions for case operations.

---

## Privacy Boundary Contract

### Must never enter KB (vault only)
- full name
- exact address
- phone number
- personal email
- government identifiers
- precise geolocation coordinates if personally identifying

### Allowed in KB (anonymized operational layer)
- `case_id` (non-semantic UUID/reference)
- segment code (`PRO`, `ENT`)
- channel source code (`LI`, `EM`, `WF`, `PR`, `LG`)
- postcode (regional granularity only)
- consumption and billing metrics
- technical feasibility indicators
- status and timeline events

---

## Required Case Schema (v1)

```json path=null start=null
{
  "case_id": "case-uuid",
  "segment_code": "PRO|ENT",
  "channel_source": "LI|EM|WF|PR|LG",
  "location_postcode": "string",
  "avg_daily_consumption_kwh": 0.0,
  "avg_night_consumption_kwh": 0.0,
  "avg_monthly_bill_eur": 0.0,
  "buildable_area_sqm": 0.0,
  "status": "NEW|QUALIFIED|RFQ_SENT|QUOTED|OFFER_SENT|NEGOTIATION|DECLINED|SIGNED|INSTALLED|OPERATIONAL",
  "created_at": "ISO-8601 timestamp",
  "updated_at": "ISO-8601 timestamp",
  "evidence_status": "verified|unverified|hypothesis",
  "provenance": {
    "actor": "string",
    "source": "string",
    "confidence": "low|medium|high",
    "review_status": "draft|reviewed|approved"
  }
}
```

---

## Lifecycle Transition Rules

- `NEW -> QUALIFIED` only if required fields are complete and feasible
- `QUALIFIED -> RFQ_SENT` after ToR dispatch to partner(s)
- `RFQ_SENT -> QUOTED` after at least one valid quote received
- `QUOTED -> OFFER_SENT` after configured offer generation
- `OFFER_SENT -> NEGOTIATION | DECLINED | SIGNED`
- `SIGNED -> INSTALLED`
- `INSTALLED -> OPERATIONAL`
- Any state may append a risk flag entry; terminal close path is `DECLINED`

Invalid transitions should be logged as review events and blocked in automated flows.

---

## Pricing Qualification Rule (Corrected)

For each quote:
- `required_leasing = amortized_install_component + financing_component`
- qualification requires: `required_leasing ≤ avg_monthly_bill_eur * 0.80`

If qualification fails:
- mark as `NEGOTIATION` or `DECLINED` based on outcome,
- record reason code (`pricing_gap`, `technical_gap`, `partner_gap`, etc.),
- do not force contradictory pricing into the KB model.

---

## Sample Cases (Schema Validation)

### Sample A (qualifies)

```json path=null start=null
{
  "case_id": "case-001",
  "segment_code": "PRO",
  "channel_source": "PR",
  "location_postcode": "2560-000",
  "avg_daily_consumption_kwh": 18.2,
  "avg_night_consumption_kwh": 6.4,
  "avg_monthly_bill_eur": 210.0,
  "buildable_area_sqm": 62.0,
  "status": "QUALIFIED",
  "evidence_status": "verified",
  "provenance": {
    "actor": "case-builder-agent",
    "source": "installer-referral-intake",
    "confidence": "high",
    "review_status": "approved"
  }
}
```

### Sample B (does not qualify at quote stage)

```json path=null start=null
{
  "case_id": "case-002",
  "segment_code": "ENT",
  "channel_source": "EM",
  "location_postcode": "8600-000",
  "avg_daily_consumption_kwh": 95.0,
  "avg_night_consumption_kwh": 41.0,
  "avg_monthly_bill_eur": 980.0,
  "buildable_area_sqm": 110.0,
  "status": "NEGOTIATION",
  "evidence_status": "verified",
  "provenance": {
    "actor": "case-builder-agent",
    "source": "email-intake-batch",
    "confidence": "medium",
    "review_status": "reviewed"
  }
}
```

---

## Workstream B Acceptance Check
- [x] Anonymized schema defined
- [x] PII exclusion contract defined
- [x] Lifecycle transition rules defined
- [x] Two sample cases provided

formal_proof:
  engine: ml-hilbert
  trl_phase: TRL6
  obligation_id: kb.customers.standards_22_anonymized_case_schema_lifecycle_v1
  proof_artifact: kb-governance/formal-proofs/customers-standards-22-anonymized-case-schema-lifecycle-v1.lean
  verification_status: verified
