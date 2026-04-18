# 13 — Financial Model
## Consolidation provenance
- consolidation_actor: `WARP`
- consolidation_source: `_kb-split-migration/kb-metrics/docs/financial/13-financial-model.md`
- consolidation_date: `2026-04-17`
- consolidation_status: `canonicalized`

## SPLIT-09 Metadata Contract
- primary_domain: `metrics`
- secondary_domains: `revenue-streams`, `cost-structure`, `governance`
- temporal_scope: `current`
- evidence_status: `quantified-model-v1.1`
- upstream dependencies: `kb-revenue-streams/docs/model/03-business-model.md`
- downstream dependencies: `kb-governance/docs/open-questions/12-open-questions.md`
- validation hooks: `chain.metrics_to_open_questions.exception_routing_explicit`, `formula.sources.cited`, `evidence.labels.non_empty`
- exception_routing: Any unresolved model contradiction, qualification conflict, or assumption gap must be logged and tracked in `kb-governance/docs/open-questions/12-open-questions.md` with owner and due action.
- provenance:
  - actor: `WARP`
  - source: `KnowledgeBase/13-Financial-Model.md@4c119831435ea9e39242278f2f639ccbcac5282f`
  - confidence: `direct-transfer-with-normalization`
  - review_status: `pending-entity-review`
- chain_link: `metrics -> open-questions` (exception lane)

> Extracted from WeRa.Financials: OpEx-CapEx-Table-1.csv, P-L-Q-Table-1.csv, SolarSeed_base-Table-1.csv, SolarSeed_avg-Table-1.csv

---

## Unit Economics

### SolarSeed Base Configuration (M-Profile)

| Metric | Value |
|---|---|
| **CAPEX per unit** | €5,001.26 |
| Energy subsystem | €3,450.53 (69%) |
| Compute subsystem | €1,550.73 (31%) |
| **Monthly lease revenue** | €70.00 |
| **Monthly amortization** | €51.62 |
| **Monthly profit per unit** | €9.13 (at 13.05% margin initially, stabilizing at 26.26%) |
| **Lease term** | 240 months (20 years) |
| **LTV per unit** | €16,800 |
| **LTV profit per unit** | €11,798.74 |
| **Unit ROI** | 235.92% (over 474% with associated cloud revenue) |
| Energy production | 300 quotas/month (2,424 Wh per quota) |
| Energy storage capacity | 6,000 Wh |

### SolarSeed Average Configuration

| Metric | Value |
|---|---|
| **CAPEX per unit** | €22,979.69 |
| Energy subsystem | €20,529.96 (89%) |
| Compute subsystem | €2,449.73 (11%) |
| **Monthly lease revenue** | €460.00 |
| **Monthly amortization** | €198.02 |
| **Lease term** | 300 months (25 years) |
| **Total depreciation book** | €26,899 |
| **Total lease revenue** | €138,000 (at €460/mo) or €144,000 (at €600/mo) |
| **Unit ROI** | 96% (at €460/mo) / 435% (at €600/mo) |

### Cloud User Economics

| Metric | Value |
|---|---|
| **Revenue per cloud user** | €2.53/month (80% Resident + 20% Royal blend) |
| **LTV per cloud user** | €404.77 |
| **Cloud user lifespan** | 120 months (10 years) |
| **Own capacity per SolarSeed** | 100 GB quotas |
| **Rented capacity cost (Hetzner)** | €0.0047/GB quota |
| **Own capacity cost (SolarSeed)** | €0.00/GB quota |
| **CAC per user** | €0.14 (B2B2C via partners) |
| **CAC per lead (direct)** | €283.25 total (lead gen 36% + sales team 54% + direct marketing 5%) |

---

## P&L Summary (2-Year Model)

Source: P-L-Q-Table-1.csv

### Unit Deployment Schedule

| Quarter | Q1Y1 | Q2Y1 | Q3Y1 | Q4Y1 | Q1Y2 | Q2Y2 | Q3Y2 | Q4Y2 |
|---|---|---|---|---|---|---|---|---|
| **SolarSeed units** | 3 | 10 | 50 | 100 | 250 | 500 | 750 | 1,000 |
| **Cloud users (combined)** | 15 | 2,000 | 8,000 | 8,000 | 16,000 | 16,000 | 376,000 | 376,000 |

Note: Massive user jump in Q3Y2 (16k → 376k) reflects WiFi Map integration going live with 360,000 converted users.

### Revenue Streams by Quarter

| Quarter | Node Revenue | Cloud Revenue (Own) | Cloud Revenue (Rented) | Total Revenue |
|---|---|---|---|---|
| Q1Y1 | €630 | €114 | €0 | €744 |
| Q2Y1 | €2,100 | €7,589 | €7,589 | €17,279 |
| Q3Y1 | €10,500 | €37,947 | €22,768 | €71,216 |
| Q4Y1 | €21,000 | €60,716 | €0 | €81,716 |
| Q1Y2 | €52,500 | €121,431 | €0 | €173,931 |
| Q2Y2 | €105,000 | €121,431 | €0 | €226,431 |
| Q3Y2 | €157,500 | €569,210 | €2,284,429 | €3,011,139 |
| Q4Y2 | €210,000 | €758,947 | €2,094,693 | €3,063,639 |

### Annual Totals

| Metric | Year 1 | Year 2 | Y1+Y2 Total |
|---|---|---|---|
| **Node revenue** | €34,230 | €525,000 | €559,230 |
| **Cloud revenue** | €136,724 | €5,950,142 | €6,086,866 |
| **Total revenue** | €170,954 | €6,475,142 | €6,646,096 |
| **Total COGS** | €1,104,807 | €5,315,198 | €6,420,005 |
| **Gross profit** | -€933,853 | €1,159,944 | €226,091 |
| **Gross margin** | -546.26% | 17.91% | 3.40% |
| **EBITDA** | -€1,985,872 | €107,924 | -€1,877,948 |
| **Net profit** | -€2,011,112 | -€440,617 | — |

### Key Inflection Points
- **EBITDA-positive**: Q3 Year 2 (EBITDA = €1,077,485)
- **Gross-profit positive**: Q3 Year 2 (profit = €1,340,490)
- **Revenue exceeds costs**: Q3 Year 2 (when WiFi Map users activate)
- **Net profit positive**: Q4 Year 2 (€1,009,336)

---

## OpEx Structure (Annual)

Source: OpEx-CapEx-Table-1.csv

| Category | Lead Entity | Cost/Unit | Units | Year 1 | Year 1+2 |
|---|---|---|---|---|---|
| **Solar Team** (Engineer, DevOps) | WeRa Capital PT | €60,000 | 2 | €120,000 | €180,000 |
| **Cloud Team** (Architect, FullStack, Frontend, UX/UI, web3) | WeRa Capital PT | €60,000 | 5 | €300,000 | €450,000 |
| **AI Team** (Scientist, FullStack, Engineer) | Inteligente Razão | €60,000 | 3 | €180,000 | €270,000 |
| **Sales & Partnerships** (BusDev, 2 Sales) | WeRa Foundation | €30,000 | 3 | €90,000 | €135,000 |
| **Officers** (CEO, CSO, CTO) | WeRa STAK NL | €60,000 | 3 | €180,000 | €270,000 |
| **Gateway servers & agents** | Inteligente Razão | €240/unit | 100 | €30,400 | €33,600 |
| **Workspace package** | WeRa Capital PT | €1,000/unit | 12 | €14,400 | €21,600 |
| **Reserve (15%)** | WeRa Capital PT | — | — | €137,220 | €204,030 |

**OpEx subtotals:**
| Category | 1st Q | Year 1 | Year 1+2 |
|---|---|---|---|
| Team costs | €217,500 | €870,000 | €1,305,000 |
| Admin costs | €37,905 | €151,620 | €243,030 |
| Server costs | €7,600 | €30,400 | €33,600 |
| **OpEx total** | **€263,005** | **€1,052,020** | **€1,581,629** |

### IP Investment
- €180,000 (IP transfer from Inteligente Razão to WeRa Global)

### 1-Month Setup Cost
- €110,013

### Year 1 Runway (OpEx only)
- €2,149,322 (includes setup)

---

## CapEx Structure

Source: OpEx-CapEx-Table-1.csv

| Category | Lead Entity | Cost | Units | Total |
|---|---|---|---|---|
| **Legal entities STAK NL + Association CH** | WeRa STAK NL | €3,000 | 2 | €9,600 |
| **Legal entities PT Capital** | WeRa STAK NL | — | — | €3,600 |
| **T&C, AML/KYC, PP and CP** | WeRa STAK NL | — | — | €4,200 |
| **SolarSeed hardware** (100 units) | WeRa Capital PT | €5,001.26 | 100 | €500,126 |
| **Lead generator** | WeRa Foundation CH | €100 | 1,000 | €100,000 |
| **Partnership integration** (Soula, Ubbu, WiFi Map) | Inteligente Razão | €10,000 | 3 | €42,600 |
| **Tests & internal education** | WeRa Foundation CH | — | — | €10,800 |
| **CAC (Customer Acquisition Cost)** | WeRa Foundation CH | €283.25 | 1,000 | €283,250 |
| **Reserve capital (15%)** | WeRa Capital PT | — | — | €143,126 |

**CapEx subtotals:**
| Category | Total |
|---|---|
| Assets acquisition | €643,252 |
| Customer acquisition | €436,650 |
| Legal & QA | €17,400 |
| **CapEx total** | **€1,097,302** |
| Infrastructure investment | €500,126 |

### CAC Breakdown

| Channel | % of Total CAC | Cost per Lead |
|---|---|---|
| Direct marketing | 5% | -€283.25 base |
| Lead generation | 36% | -€2,039.40 |
| Sales team | 54% | -€3,059.10 |
| **Total CAC per customer** | **100%** | **€283.25** |

Historical reference: Nepal FY2023 CAC = €5,665 (WeRa targets 20× lower).

---

## Total Investment Required

| Component | Amount |
|---|---|
| **OpEx Year 1+2** | €1,581,629 |
| **CapEx** | €1,097,302 |
| **IP Investment** | €180,000 |
| **Total** | ~€2,858,931 |

Split across funding stages:
- **1st equity round (Q1 — 3 months)**: €263,005 OpEx
- **Seed round**: €2.2M for remaining 15-month runway

---

## Fundraising and Valuation Model

Source: P-L-Q-Table-1.csv (rows 56–58)

| Stage | Quarter | Valuation | Equity Sold | Amount Raised | Instrument |
|---|---|---|---|---|---|
| **SAFE** | Q1Y1 | €600,000 | SAFE | €120,000 | Convertible |
| **SAFE** | Q2Y1 | €4,167,717 | SAFE | €540,136 | Convertible |
| **Seed** | Q3Y1 | €4,167,717 | 12% | — | Equity |
| **Seed (additional)** | Q4Y1 | — | 4% | €166,709 | Equity |
| **Series A** | Q2Y2 | €200,000,000 | 10% | €20,000,000 | Equity |
| **Series B** | Q4Y2 | €1,250,000,000 | 8% | €100,000,000 | Equity |

Total convertible loan: €660,136 (Q1+Q2 SAFE combined; differs from earlier €500k figure — the model shows €120k + €540k structure).

---

## Cash Position Trajectory

| Quarter | Runway | Cash Position | Net Cash |
|---|---|---|---|
| Q1Y1 | €500,126 | €2,861 | -€487,265 |
| Q2Y1 | €2,181,667 | €1,502,359 | -€669,308 |
| Q3Y1 | €1,502,359 | €1,106,330 | -€396,029 |
| Q4Y1 | €1,106,330 | €673,059 | -€433,271 |
| Q1Y2 | €673,059 | €1,330,022 | -€843,416 |
| Q2Y2 | €1,330,022 | €38,980 | -€1,291,042 |
| Q3Y2 | €38,980 | €1,116,465 | €1,076,815 |
| Q4Y2 | €1,116,465 | €2,281,362 | €1,164,182 |

**Critical runway points:**
- Near-zero cash at Q2Y2 (€38,980) — requires Series A close before this point
- Positive net cash achieved Q3Y2 (€1,076,815)
- Operating cash-burn: ~€263k–267k/quarter (Y1), escalating to ~€648k–683k/quarter (Y2)

---

## Asset Balance Sheet

| Quarter | Gross Assets | Net Assets | Total Fixed Assets | Gross Book Value |
|---|---|---|---|---|
| Q1Y1 | €15,004 | €14,539 | €194,539 | €195,283 |
| Q4Y1 | €500,126 | €484,641 | €1,204,641 | €1,286,357 |
| Q4Y2 | €5,001,260 | €4,846,413 | €6,286,413 | €9,350,052 |

Gross assets at scale: €5,001,260 (1,000 units × €5,001.26) — this represents the base configuration cost; actual deployment may use average configuration at higher CAPEX.

---

## Revenue Composition Analysis

| Revenue Source | Year 1 | Year 2 | % of Y1+2 Total |
|---|---|---|---|
| Node leasing | €34,230 | €525,000 | 8.4% |
| Cloud (own capacity) | €106,366 | €1,571,020 | 25.2% |
| Cloud (rented capacity) | €30,358 | €4,379,122 | 66.3% |
| **Total** | **€170,954** | **€6,475,142** | **100%** |

Cloud revenue dominates at 91.6% of total — the business is fundamentally a cloud platform monetized through physical solar infrastructure.

### LTV Analysis

| Revenue Stream | LTV | Lifespan |
|---|---|---|
| SolarSeed node | €16,800 per unit | 240 months |
| Cloud user (own) | €40,477.15 per unit | — |
| Cloud (rented) | €404.31 per user | — |
| **Total cloud LTV** | **€152,194,099** (full network) | 120 months |

---

## Model Assumptions and Risks

### Key Assumptions
1. WiFi Map activates 360,000 users in Year 2 (drives 66% of total revenue)
2. 1,000 SolarSeed units deployed by Q4Y2
3. Rented capacity cost stays at €0.0047/GB (Hetzner pricing)
4. 80/20 Resident/Royal cloud user mix
5. No churn modeled explicitly
6. Series A at €200M valuation closes before Q2Y2 cash exhaustion

### Key Risks
- **WiFi Map dependency**: 66% of Y2 revenue depends on a single partner activation with no signed MoU
- **Cash cliff at Q2Y2**: €38,980 remaining — Series A timing is critical
- **Rented capacity scaling**: Rented cloud costs scale linearly; need SolarSeed deployment to keep pace
- **Valuation jumps**: €4.2M → €200M → €1.25B in 2 years — aggressive; requires exceptional traction proof
