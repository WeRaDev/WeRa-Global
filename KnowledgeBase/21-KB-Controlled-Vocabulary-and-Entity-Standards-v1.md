# 21 — KB Controlled Vocabulary and Entity Standards v1

---

## Purpose
Define canonical terminology and status enums for WeRa KB operations to prevent drift across documents, case workflows, and AI-agent outputs.

---

## Canonical Product Names

| Canonical | Alias (deprecated/variant) | Notes |
|---|---|---|
| `WeRaSolar` | Solar business line | Physical product line wrapper |
| `SolarSeed` | Solar Seed, SolarSeat | Base physical product under WeRaSolar |
| `WeRaCloud` | WERA Cloud, Vera Cloud | Digital product line wrapper |
| `CityLight` | City of Light | Base product concept under WeRaCloud line context |

Rule: deprecated aliases may appear only in historical notes with explicit “alias/deprecated” label.

---

## Customer Segments (v1)

| Code | Canonical Segment | Definition |
|---|---|---|
| `PRO` | Mindful Prosumers | Aware of energy risk; motivated but upfront-CAPEX constrained |
| `ENT` | Enterprise Sustainability Seekers | Organizations pursuing resilience, savings, and ESG alignment |

---

## Channel Codes (v1)

| Code | Channel |
|---|---|
| `LI` | LinkedIn |
| `EM` | Email |
| `WF` | Website form |
| `PR` | Partner referral |
| `LG` | Lead-generation bot |

---

## Case Lifecycle Status Enum (v1)

| Status | Meaning |
|---|---|
| `NEW` | Case created with minimum required anonymized fields |
| `QUALIFIED` | Segment and feasibility checks passed |
| `RFQ_SENT` | Terms of reference sent to partner(s) |
| `QUOTED` | Quote received and offer configured |
| `OFFER_SENT` | Customer-facing offer issued |
| `NEGOTIATION` | Terms under discussion |
| `DECLINED` | Case closed without deal |
| `SIGNED` | Commercial terms signed |
| `INSTALLED` | Installation completed |
| `OPERATIONAL` | Live operation with measured performance |

---

## Evidence Labels (v1)

| Label | Use |
|---|---|
| `verified` | Claim supported by traceable source and/or measured internal data |
| `unverified` | Claim present but not validated in WeRa context |
| `hypothesis` | Forward-looking assumption pending validation |

---

## Provenance Metadata (mandatory for AI-authored entries)

- `actor`
- `timestamp`
- `source`
- `confidence`
- `review_status`

Without these fields, entry is draft-only and cannot be treated as KB fact.
