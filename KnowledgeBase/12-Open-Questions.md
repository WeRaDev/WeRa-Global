# 12 — Open Questions and Due-Diligence Gaps

> Items that remain unresolved or require additional documentation for full knowledge base integrity.

---

## Critical — Blocks Timeline Calculations

| # | Question | Status | Notes |
|---|---|---|---|
| Q1 | WeRa Global formal registration date | 🟡 Partially resolved | Target: Q2 2026. Exact filing date TBD. Unlocks all timeline anchors. |
| Q2 | Exact legal entity names and registration numbers | 🟡 Partially resolved | Three entities planned (Foundation, STAK, Capital). None yet registered. |

---

## High Value — Investment Due Diligence

| # | Question | Status | Notes |
|---|---|---|---|
| Q3 | Financial model details | ✅ Resolved v1.1 | Extracted into `13-Financial-Model.md` from 4 CSV files: OpEx/CapEx, P&L, base BOM, avg BOM. |
| Q4 | Team composition and bios | ⚪ Private | Described in private documents. Not included in KB per instruction. |
| Q5 | Team vesting schedule | ⚪ Undefined | 22% team pool allocated; Chief Officers 3% each; remaining 10% pool. Vesting terms TBC. |
| Q6 | Formal MoU/LOI timeline for Soula, Ubbu, WiFi Map | 🟡 Pending | Personal relationships confirmed; interest expressed. No MoUs signed. Timeline for formalization unclear. |
| Q7 | Mitsubishi next steps | 🟡 Vague | Personal connection with Director of Intl Relations. No meeting or formal engagement planned. |
| Q8 | Financial model — unit economics verification | ✅ Resolved v1.1 | Base: €70/unit/month × 100 units = €7k MRR at Q4Y1. Avg: €460/unit/month. Both validated from spreadsheet. |
| Q9 | Post-seed burn rate validation | ✅ Resolved v1.1 | Quarterly burn: €263k–267k (Y1), €648k–683k (Y2). Cash cliff at Q2Y2 (€38,980). Details in `13-Financial-Model.md`. |

---

## Medium — Operational Clarity

| # | Question | Status | Notes |
|---|---|---|---|
| Q10 | SolarSeed exact hardware specifications | ✅ Resolved v1.1 | Full BOM for both base (€5,001.26) and avg (€22,979.69) configs documented in `02-Products.md`. Hardware verified against manufacturer specs (AIKO, Huawei, GEEKOM). |
| Q11 | FilantropiaSolar tech stack details | 🟡 Partial | Python backend confirmed. Database, frontend, hosting details not disclosed. |
| Q12 | WERA Cloud pricing reconciliation | ✅ Resolved v1.1 | Financial model confirms: Resident = €1/user/month, Royal = €12/user/month. Blended revenue = €2.53/user/month (80/20 mix). The €2.50 from strategy docs was the blended rate, not a separate tier. Website €288/cloud/month = Royal (€12 × 24 users per cloud). |
| Q13 | Ambassador formalization criteria | ⚪ Undefined | Still informal. No written commission agreement. Criteria for formalization not established. |
| Q14 | Renew Iberia proposal turnaround improvement | 🟡 Operational | Flagged as ~1 week turnaround. No resolution documented. |
| Q15 | Segment 3 (general public) go-to-market strategy | ⚪ Pending | Explicitly noted as "strategy pending" in transcripts. |

---

## Low — Enrichment

| # | Question | Status | Notes |
|---|---|---|---|
| Q16 | Signed legal opinion document | 🟡 Claimed | Legal opinion on mutual leasing + tokenization compliance "obtained" but not included in KB. |
| Q17 | Bond prospectus timeline | ⚪ Concept only | YX Digital Impact Bonds in concept stage. No prospectus or CMVM filing. Planned for acceleration phase. |
| Q18 | Energy community license timeline | 🟡 Partially resolved | Not filing now — leasing model avoids license requirement. Transcript references 12–18 months from company establishment for energy-sales licensing path when excess energy sale becomes relevant. |
| Q19 | WiFi Map user count reconciliation | ℹ️ Noted | External: 170M+; WeRa docs: 180M. Both preserved with context. Likely reflects different reporting dates. |
| Q20 | City of Light / gamification development timeline | ⚪ Conceptual | Gamified UX layer described in detail but no development timeline or resource allocation. |

---

## Files Not Yet Integrated

| File | Description | Priority |
|---|---|---|
| ~~WeRa.Financials.xlsx~~ | ~~Financial model with P&L projections~~ | ✅ Integrated v1.1 (4 CSVs → `13-Financial-Model.md`) |
| ~~Technical-Description.SolarSeed.BaseConfiguration.md~~ | ~~SolarSeed technical architecture~~ | ✅ Integrated v1.1 → `02-Products.md` + `04-System-Architecture.md` |
| **Private team document** | Team composition and bios | Excluded per instruction |
| **Signed legal opinion** | Compliance confirmation | Medium — would strengthen investment readiness |
| **Renew Iberia pitch deck (full)** | Partner detailed capabilities | Already partially integrated |
| **SolDevlist.csv** | Alternative solar development partners ranked list | Already referenced |

---

## New Questions Added (v1.1)

| # | Question | Status | Notes |
|---|---|---|---|
| Q21 | SAFE structure discrepancy | 🟡 Needs clarification | Transcripts reference €500k convertible loan at 8%. Financial model shows two SAFEs: €120k + €540k = €660k, no interest rate modeled. Which is canonical? |
| Q22 | Valuation justification | 🟡 Aggressive | Model projects €600k → €4.2M → €200M → €1.25B over 8 quarters. What external benchmarks or milestones justify each jump? |
| Q23 | WiFi Map revenue concentration risk | 🟡 Critical | 66% of Y2 revenue depends on WiFi Map activating 360k users. No MoU signed. If delayed or reduced, Q3Y2 cash-flow breakeven fails. |
| Q24 | Base vs average config deployment mix | 🟡 Unclear | P&L uses €5,001.26/unit (base config) for 100-unit CapEx (€500,126). But avg config is €22,979.69. Which will actually be deployed? Mix ratio? |
| Q25 | Team salary structure | 🟡 Needs detail | Model shows €60k/yr for technical and officer roles, €30k/yr for sales. Are these gross or net? Include social charges? Country of employment? |
| Q26 | Cloud rented capacity scaling | 🟡 Cost risk | At 376k users, rented capacity costs €814k (Y2). If SolarSeed deployment lags, rented costs consume margin. |
| Q27 | Runway operating reality vs model timeline | 🔴 Critical | Strategic session states founder runway is effectively exhausted (\"already finished, stretched to next month\"). Need contingency path if object-level financing is delayed 30+ days. |
| Q28 | Execution anti-pattern: single-counterparty dependency | 🟡 Pattern risk | Repeated waiting on one actor (installer or investor) instead of parallel channel execution. Must be tracked as an operating risk, not only a founder coaching note. |

## Recommendations for Next KB Update

1. ~~Extract WeRa.Financials.xlsx~~ ✅ Done
2. **Formalize partner MoUs** and update `08-Partnerships.md` with signed documents
3. ~~Obtain SolarSeed hardware BOM~~ ✅ Done
4. **Define team vesting schedule** for `06-Legal-Structure.md`
5. **Develop Segment 3 strategy** for `07-Customers-and-GTM.md`
6. **Create pitch deck KB file** summarizing investor-facing materials
7. **Clarify SAFE vs convertible loan** structure (Q21)
8. **Add sensitivity analysis** — model P&L with 50% and 75% of projected WiFi Map users
9. **Validate base vs avg deployment mix** and recalculate CapEx accordingly
10. **Define contingency plan under short runway** if object pipeline does not convert in current cycle
11. **Track and mitigate serial dependency risk** in GTM and fundraising execution
