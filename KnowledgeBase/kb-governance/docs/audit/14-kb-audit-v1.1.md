# 14 — Knowledge Base Audit v1.1

## Consolidation provenance
- consolidation_actor: `WARP`
- consolidation_source: `KnowledgeBase/14-KB-Audit-v1.1.md`
- consolidation_date: `2026-04-27`
- consolidation_status: `canonicalized`


> Systematic review of KB v1.1 (15 files, 2,111 lines) against all 7 primary sources:
> `structure.md`, `Business-model.txt`, `sales.txt`, `Marketing.txt`, `System-description.txt`, `strategy.overal.txt`, `WeRa.strategy.pdf`

---

## Audit Summary

| Category | Count |
|---|---|
| **Correctly captured** | 47 items |
| **Missing from KB (data exists in sources)** | 18 items |
| **Contradictions / discrepancies** | 9 items |
| **Enrichment opportunities (implicit in sources)** | 6 items |
| **Deprecated / superseded items** | 3 items |

---

## A. Missing From KB — Data Present in Sources but Not in KB

### A1. Mutual Leasing — Real Estate Tokenization Default Mechanism (HIGH)

**Source**: Business-model.txt (lines 273–289)

The transcript describes a specific crisis-protection mechanism in detail that the KB only summarizes superficially:

> "If our customer cannot pay... instead of shutting down the equipment and taking costs... we just continue powering the client and our own equipment, and receive €200 worth of tokenized shares of his real estate, of a household or enterprise."

The KB (`05-Tokenomics-and-Governance.md`, line 96–101) mentions "mutual leasing protection" but omits:
- The explicit flow: customer defaults → WeRa continues powering → accepts tokenized real estate fraction as payment at the monthly lease value
- The balance sheet benefit: tokenized real estate goes on balance sheet, showing positive profitability even during defaults
- The acquisition upside: during crisis liquidation, WeRa can acquire real estate at lowest market prices
- The stated social mission: "protecting our customers and the real estate from acquisition by giants like BlackRock" (strategy.overal.txt, line 171)

**Action**: Expand `05-Tokenomics-and-Governance.md` mutual leasing section with full mechanism.

---

### A2. Bond Revenue Stream — Detailed (HIGH)

**Source**: Business-model.txt (lines 357–362), System-description.txt (lines 111–125)

The transcripts describe a bond product with much more specificity than the KB captures:
- "Convertible loan agreement where we borrow money for solar installations with long-term conditions like a bond"
- "We offer stable return of 8% per year... and even more like risk-adjusted returns based on specific vertical products"
- System-description.txt: "We sell bonds to the investors, offering stable returns around 8 or 10% per year, collateralized by the leasing agreements"
- The bond is explicitly described as the **second product** / **second revenue stream**, not just a funding mechanism

**KB gap**: `03-Business-Model.md` only has "Stream 3: Tokenization Services" as a vague line. The bond as a distinct product / revenue stream is not properly documented.

**Action**: Add bond product details to `02-Products.md` and `03-Business-Model.md`.

---

### A3. Equipment Marketplace — Future Product Line (MEDIUM)

**Source**: strategy.overal.txt (lines 209–231)

The transcript describes a future product extension not in the KB:
- "We can offer extra equipment to lease. For example, new machines, fridges, stoves, new equipment, energy efficient, and also other equipment... gaming consoles, industrial equipment"
- "We provide our customers with a marketplace where they can get more electrical appliances from us in leasing terms"
- "We want to be able to provide not only energy, but also water, everything necessary for hosting life"

**KB gap**: `02-Products.md` documents extension packs (Smart-House, Security, etc.) from the technical doc, but not the broader marketplace vision for leasing any appliance.

**Action**: Add "Equipment Marketplace" as a roadmap product in `02-Products.md`.

---

### A4. Landscape / Quinta Management Partner Services (MEDIUM)

**Source**: Marketing.txt (lines 75–83)

The transcript mentions a partner type not documented in `08-Partnerships.md`:
- "Partner in landscaping, gardening, quinta management... pool management, irrigation systems, providing a full all-in-one solution"

This is described as an existing or planned partner relationship, not just an aspiration.

**KB gap**: Not mentioned in any KB file. `08-Partnerships.md` covers only Iberia Renew, Soula, Ubbu, WiFi Map, Sunified, Mitsubishi.

**Action**: Add landscaping/quinta management partner to `08-Partnerships.md` (status: described in transcript, no company name given).

---

### A5. Three-Pillar Strategy from Transcript (MEDIUM)

**Source**: strategy.overal.txt (lines 57–89)

The transcript defines three strategic pillars that differ slightly from the KB's version:
1. **Ownership over real-world assets** (not "Energy Sovereignty")
2. **Liquidity** — financial resources for system stability, focusing on institutional investors (not "Digital Sovereignty")
3. **Public** — future public is humans + algorithmic citizens/robots/agents (not "Financial Sovereignty")

The KB (`09-Strategy-and-Investment.md`, lines 17–21) lists:
1. Energy Sovereignty
2. Digital Sovereignty
3. Financial Sovereignty

These are from the website, not the transcript. Both are valid framings, but the transcript version is more foundational and the KB should preserve both.

**Action**: Add transcript's three-pillar framing alongside the website version in `09-Strategy-and-Investment.md`.

---

### A6. Quantum-Resistant Security Details (MEDIUM)

**Source**: Business-model.txt (lines 334–339)

The transcript provides specific technical detail about quantum security:
- "Every panel [has a] little trust execution environment that can encrypt all the data"
- "Virtual digital energy station composed of thousands of installations, each one composed of twenty panels, will give us very strong encryption"
- "While other systems will fall in 2028, our system will be resistant"
- This is tied to the Sunified partnership specifically

**KB gap**: `08-Partnerships.md` mentions Sunified as "Quantum-secure PV hardware supplier" and "aspirational target", but doesn't capture the per-panel TEE (Trusted Execution Environment) detail or the 2028 quantum resistance claim.

**Action**: Expand Sunified entry in `08-Partnerships.md` with TEE detail and 2028 timeline.

---

### A7. Lead Generator Economics (MEDIUM)

**Source**: Business-model.txt (lines 125–131), Marketing.txt (lines 178–193)

The transcript provides specific lead acquisition economics not fully captured:
- Secondary market leads: "€100–200" per lead (people who contacted solar companies, got a proposal, and decided it was too expensive)
- These are cheaper because they're "on a secondary market" — already aggregated and already paid for
- Contrast with the €283.25 CAC in the financial model (which is the total blended CAC including sales team time)
- Also building "own lead generation robot" (AI-based)

**KB gap**: `07-Customers-and-GTM.md` doesn't document the secondary lead market or the €100–200 lead cost distinction from the €283.25 blended CAC.

**Action**: Add secondary lead market details to `07-Customers-and-GTM.md`.

---

### A8. Batch Customer Acquisition via Associations (MEDIUM)

**Source**: Marketing.txt (lines 153–163), sales.txt (lines 11–13)

The transcript describes a specific batch acquisition strategy:
- Work with farmer associations and landlord associations (membership-based organizations)
- Arrange batch presentations: "working with several customers at the same time"
- "If we have association that has 20 local members... we can arrange a batch"
- This ties to municipality connections and grant/subsidy access
- Sales pipeline includes "several municipalities and associations and regeneration villages like eco-villages"

**KB gap**: `07-Customers-and-GTM.md` mentions "ambassador referrals" and "B2B direct sales" but doesn't describe the batch-through-associations model specifically.

**Action**: Add batch acquisition via associations to `07-Customers-and-GTM.md`.

---

### A9. Three Ambassador Profiles (LOW — privacy-sensitive)

**Source**: sales.txt (lines 115–133)

The transcripts describe three specific ambassador candidates:
1. Young woman — communication skills, family connections in Sintra municipality and associations, currently without a job
2. Ex-cloud architect — Portuguese, taking sales course, career change from tech to sales, very communicative
3. Polish guy — connections in Germany and Poland, focused on server-only SolarSeed installations (industrial containers)

**KB note**: Currently says "3 profiled (details in private documents)". The third candidate reveals an additional product variant — **server-only SolarSeed in industrial containers** for customers who don't want solar energy for their own use but just want a solar-powered server.

**Action**: Keep profiles private but add the server-only industrial container product variant to `02-Products.md`.

---

### A10. Map Station Types (LOW)

**Source**: sales.txt (lines 39–62)

The map shows three distinct station types:
1. **Operational** — live, generating, with real savings data
2. **In construction** — being built
3. **Planning** — customer confirmed interest, station added to map

The first stations include both the real pilot AND several "not real proposal" stations used to train the energy prediction model. The map shows aggregated, anonymized locations per freguesia (parish).

**KB gap**: `07-Customers-and-GTM.md` mentions the map but doesn't document the three station types or the training-data stations.

**Action**: Add station type taxonomy to `07-Customers-and-GTM.md`.

---

### A11. Letter of Intent Step (LOW)

**Source**: sales.txt (lines 83–86)

The sales process includes a specific legal step not in the KB:
- After the calculator, before the engineering proposal, the customer signs a **Letter of Intent by email**
- "This is the data that I'm providing, and this is my intent to get these conditions that your calculator gave me"

**KB gap**: The 10-step sales journey in `07-Customers-and-GTM.md` jumps from "Creates account" to "Sales team follow-up" without the LOI step.

**Action**: Insert LOI step into the sales journey.

---

### A12. Strategy PDF — "Technofeudal Trap" Framing (MEDIUM)

**Source**: WeRa.strategy.pdf (page 1)

The strategy PDF introduces specific investor-grade language not in the KB:
- **"The Technofeudal Trap"** — users locked into centralized ecosystems not because products are superior but because switching friction is high
- **"No middle class of cloud hosting"** — only massive incumbents (high privacy risk) and complex self-hosting (high technical barrier)
- **"Embedded Sovereign Cloud"** — the formal name for the B2B2C strategy
- **"deGigafactory"** — the term for the 1M-node expansion goal

**KB gap**: These framings and terms are not in the KB. They are important for investor communication.

**Action**: Add these terms to `00-Glossary.md` and reference them in `09-Strategy-and-Investment.md`.

---

### A13. Strategy PDF — Conversion Rate Detail (MEDIUM)

**Source**: WeRa.strategy.pdf (page 2)

The PDF specifies: "Conservative 2-4% conversion rate on partner user bases during the test period and catering for 20% conversion"

The KB financial model uses 0-2% (Y1), 2-4% (Y2), 4-6% (Y3) etc., which aligns. But the 20% long-term target is not in the KB.

**Action**: Add 20% long-term conversion target to `13-Financial-Model.md`.

---

### A14. Host Benefit — "20% Reduction Guaranteed" (MEDIUM)

**Source**: WeRa.strategy.pdf (page 1)

The PDF states: "Host Benefit: 20% reduction in monthly energy bills (guaranteed)"

The KB says "below the customer's current electricity bill" and the business model transcript says "50 to 20 percent" discount. The 20% figure from the strategy PDF is the specific minimum guarantee.

**KB gap**: The specific 20% guaranteed reduction is not stated in the KB.

**Action**: Add the 20% minimum guarantee to `02-Products.md` and `03-Business-Model.md`.

---

### A15. "CELL" Companies Concept (LOW)

**Source**: structure.md (line 13)

The structure document defines WeRa Capital as "dedicated to operating cohorts of co-owned RWA - 'CELL' companies" that hold shares of all RWA within the conglomerate across Europe.

**KB gap**: The "CELL" concept (each SolarSeed installation as a cell of a larger organism) is not documented anywhere.

**Action**: Add to `00-Glossary.md` and `06-Legal-Structure.md`.

---

### A16. Energy License Timeline (MEDIUM)

**Source**: strategy.overal.txt (lines 143–145), Business-model.txt (line 103)

Two sources provide the energy license timeline:
- Strategy: "12 to 18 months from the date of company establishment"
- Business model: "eventually in one year after we will receive a license for energy sales in terms of energy communities"

**KB gap**: `12-Open-Questions.md` (Q18) says "deliberate delay" and "will obtain when excess energy available" but doesn't include the 12–18 month timeline.

**Action**: Add 12–18 month timeline to Q18.

---

### A17. Prediction Markets and Dispute Resolution (LOW)

**Source**: Business-model.txt (lines 393–403)

The transcript describes two distinct governance feedback loops:
1. **WeD (loyalty) + WeG (voting) → Prediction markets** — quadratic voting for profit reinvestment decisions
2. **WeP (economic) → Dispute resolution system** — tokenized shares enable dispute resolution

**KB gap**: `05-Tokenomics-and-Governance.md` mentions quadratic voting and dispute resolution but doesn't map them to the specific token combinations.

**Action**: Add prediction market and dispute resolution token mapping to `05-Tokenomics-and-Governance.md`.

---

### A18. Y-Loyalty Impact NFTs (LOW)

**Source**: structure.md (line 7)

The structure document mentions: "Y-Loyalty Impact NFTs" — the combination of WeG bonding + WeD utility creates a "subscription-based stream of donation-loyalty points" used for "discounts and recognition."

**KB gap**: NFTs are not mentioned anywhere in the KB.

**Action**: Add Y-Loyalty Impact NFTs to `00-Glossary.md` and `05-Tokenomics-and-Governance.md`.

---

## B. Contradictions and Discrepancies

### B1. Discount Range — "50 to 20 percent" vs "20% guaranteed" (MEDIUM)

| Source | Claim |
|---|---|
| Business-model.txt (line 257) | "discount around 50 to 20 percent" |
| WeRa.strategy.pdf (page 1) | "20% reduction in monthly energy bills (guaranteed)" |
| KB (multiple) | "below the customer's current electricity bill" |

**Analysis**: The range is 20–50% cheaper than current bill, with 20% as the minimum guarantee. The strategy PDF firms up the guarantee at 20%. The KB should state both the range and the minimum.

---

### B2. Expansion Roadmap — Eastern Countries (LOW)

| Source | Claim |
|---|---|
| KB (`01-Company-Overview.md`) | Phase 1: Portugal → Phase 2: Spain → Phase 3: France, Italy → Phase 4: Eastern Europe |
| sales.txt (lines 141–145) | "Spain, France, Italy, Slovenia, Slovakia, Croatia, Ukraine" |
| strategy.overal.txt (line 265) | "Starting from Portugal and slowly moving towards Ukraine, connecting European South by one big solar pass" |

**Analysis**: The KB's "Eastern Europe" is too vague. The transcripts name specific countries and frame the expansion as a "Golden Pass" connecting the European South. Also, "towards Belarus, towards the east" appears in sales.txt but this likely means "towards the east" generally, not Belarus specifically (since Belarus is not in the EU solar belt).

---

### B3. Segment 1 Age Range Inconsistency (LOW)

| Source | Age Range |
|---|---|
| Business-model.txt (line 77) | "35–55 years old" |
| Marketing.txt (line 93) | "30–45 years old" |
| KB (`07-Customers-and-GTM.md`) | "30–50 age range" |

**Analysis**: The KB chose a merged range (30–50) which is reasonable. Should note this is a synthesis of two different transcript claims.

---

### B4. Average Station Size (LOW)

| Source | Claim |
|---|---|
| Business-model.txt (line 349) | "average station for the household is gonna be like twenty to thirty kilowatt power" |
| KB (`02-Products.md`) | Base: 3.03 kWp, Average: 8 kWp (16 panels × 500W), L-Profile: 29.5 kWp |

**Analysis**: The transcript's "20–30 kW" claim predates the technical document which defines three specific profiles. The base (3 kWp) and average (8 kWp) BOMs are well below 20–30 kW. However, the L-Profile (29.5 kWp) aligns with the transcript's "average household." This suggests the founder envisions larger deployments than the base BOM — the "average" will grow as deployment scales.

---

### B5. Pipeline Detail — "100+ beta sites (3 rural municipalities, 7 eco-villages)" (MEDIUM)

| Source | Claim |
|---|---|
| WeRa.strategy.pdf (page 2) | "100+ beta sites (3 rural municipalities, 7 eco-villages)" |
| sales.txt (lines 9–13) | "100 new customers, including several municipalities and associations and regeneration villages like eco-villages" |
| KB (`07-Customers-and-GTM.md`) | "~100 estimated" + "⚠️ Unvalidated" |

**Analysis**: The PDF adds granularity (3 municipalities + 7 eco-villages). The KB correctly flags this as unvalidated but should include the composition detail.

---

### B6. Triple Jump Phase 2 Timeline (LOW)

| Source | Claim |
|---|---|
| WeRa.strategy.pdf (page 2) | Phase 2: "Months 7–18" |
| KB (`09-Strategy-and-Investment.md`) | Phase 2: "Months 7–12" |
| KB (`00-Glossary.md`) | Phase 2: "Months 7–12" |

**Analysis**: The PDF says Phase 2 is Months 7–18, but the KB says 7–12. Similarly, the PDF says Phase 3 is Months 18–24, while the KB says 13–24. The PDF is the investor-facing document and should take precedence.

---

### B7. Bling Energy — "1,000+ solar subscriptions" vs "3,000 users" (LOW)

| Source | Claim |
|---|---|
| WeRa.strategy.pdf (page 2) | "Bling Energy... secured 1,000+ solar subscriptions in <2 years" |
| KB (`09-Strategy-and-Investment.md`) | "3,000 new residential users; 20 MW capacity" |

**Analysis**: Both are correct but represent different points in time. The PDF references Bling's earlier milestone (1,000+), while the KB references the post-€15M expansion target (3,000). Both should be preserved.

---

### B8. "Starbucks Model" Missing from Analogy (LOW)

| Source | Claim |
|---|---|
| Business-model.txt (lines 206–211) | "EDP + Airbnb + cooperative on steroids" **and also** "ADP with Airbnb run by a Starbucks model" |
| KB (`01-Company-Overview.md`) | "EDP + Airbnb + cooperative on steroids" only |

**Analysis**: The transcript uses both "ADP" (likely means EDP) and includes a "Starbucks model" reference that the KB doesn't capture. The Starbucks model implies franchise-like scalability with consistent branding. Minor but adds nuance.

---

### B9. SAFE Amount Discrepancy (HIGH — flagged in Q21 but now traceable)

| Source | Claim |
|---|---|
| Business-model.txt (line 360) | "stable return of 8% per year" on bonds |
| strategy.overal.txt (line 179) | "investors can receive up to 8%" from leasing terms |
| Financial model (P-L-Q) | SAFE #1: €120k, SAFE #2: €540k = €660k total, no interest modeled |
| KB `09-Strategy` previously | "€500k convertible loan at 8%" |

**Analysis**: The €500k / 8% figure comes from oral transcripts (general discussion). The financial model operationalizes it as two SAFEs totaling €660k without explicit interest. These are different instruments — a convertible loan has interest; a SAFE doesn't (it has a valuation cap instead). The 8% is associated with the **bond product** for institutional investors, not the SAFE for early investors. The KB should clarify this distinction.

---

## C. Correctly Captured (Validation)

The following critical elements are accurately represented in the KB:

| Topic | KB File | Assessment |
|---|---|---|
| Three-entity legal structure | `06-Legal-Structure.md` | ✅ Accurate and detailed |
| Three-token model | `05-Tokenomics-and-Governance.md` | ✅ Correct mapping |
| BFT governance cascade | `05-Tokenomics-and-Governance.md` | ✅ Matches structure.md |
| Golden Share mechanism | `06-Legal-Structure.md` | ✅ 12% Foundation veto |
| Cap table (44/22/12/22) | `06-Legal-Structure.md` | ✅ From structure.md |
| SolarSeed base BOM | `02-Products.md` | ✅ Matches SolarSeed_base CSV |
| SolarSeed avg BOM | `02-Products.md` | ✅ Matches SolarSeed_avg CSV |
| Energy-first principle | `04-System-Architecture.md` | ✅ From technical doc |
| Three sizing profiles | `02-Products.md` | ✅ S/M/L from technical doc |
| Dual-proposal close | `03-Business-Model.md` | ✅ Matches sales.txt |
| €1 symbolic payment | `02-Products.md` | ✅ Matches sales.txt |
| Ambassador commission | `07-Customers-and-GTM.md` | ✅ €500 / 5% × €10k |
| Torres Vedras pilot | `07-Customers-and-GTM.md` | ✅ First customer confirmed |
| Fear-based messaging | `07-Customers-and-GTM.md` | ✅ Matches Marketing.txt |
| Calculator → CRM flow | `07-Customers-and-GTM.md` | ✅ Matches sales.txt |
| Kubernetes-like clustering | `04-System-Architecture.md` | ✅ From System-description.txt |
| Virtual power plant concept | `04-System-Architecture.md` | ✅ From System-description.txt |
| DePIN thesis | `09-Strategy-and-Investment.md` | ✅ From strategy PDF |
| Negative-COGS definition | `03-Business-Model.md` | ✅ From strategy PDF |
| B2B2C Trojan Horse strategy | `09-Strategy-and-Investment.md` | ✅ From strategy PDF |
| Soula Phase 1 / Ubbu Phase 2 / WiFi Map Phase 3 | `08-Partnerships.md` | ✅ From strategy PDF |
| €2.50 Cappuccino Price Point | `03-Business-Model.md` | ✅ Reconciled as blended rate |
| CIC tax advantage (dividends only) | `06-Legal-Structure.md` | ✅ From System-description.txt |
| P&L unit economics | `13-Financial-Model.md` | ✅ From CSV files |
| Partner user conversion ramp | `13-Financial-Model.md` | ✅ From P-L-Q CSV |

---

## D. Enrichment Opportunities

### D1. "Hosting Life" Vision Statement

**Source**: strategy.overal.txt (lines 233–245)

> "We imagine our planet as a big spaceship, with a big garden where different forms of life are supporting each other to survive in space."

This is the most philosophical expression of WeRa's long-term vision and should be captured in `01-Company-Overview.md`.

### D2. Data Monetization as Strategic Layer

**Source**: System-description.txt (lines 130–135)

The system description explicitly names data monetization as a third layer beyond energy and cloud: "We gather validated information from the business if they're using our solar servers... we monetize the data, providing more services, internally, creating ecosystem."

This is not well-captured as a distinct revenue/strategy layer.

### D3. Digital Separation of Power Principle

**Source**: structure.md (line 4)

The legal structure explicitly copies "high-level state government processes" using a "digital separation of power principle in arbitrage of sectoral balances." This political theory framing (public/private/foreign network model) is richer than what's in the KB.

### D4. Equipment Supply Chain Risk Mitigation

**Source**: Business-model.txt (lines 330–339)

"Securing stock of equipment in warehouses across Europe, we will be independent from geopolitical crisis... We need to be also a distributor of equipment for our own partners."

This supply chain strategy is not documented in the KB.

### D5. Mitsubishi Loan-Based Equipment

**Source**: Business-model.txt (lines 376–381)

"Japanese companies can provide equipment on a loan-based condition... leasing conditions. That is working perfectly with our business model where from the leasing of our customers, we will pay the leasing to our suppliers."

This supplier-leasing model (cascading leases) is a significant business model detail not in the KB.

### D6. AI-Based Lead Generation

**Source**: Business-model.txt (line 131), OpEx-CapEx CSV (row 30)

The transcript mentions "building our own lead generation robot" and the CapEx table includes an "AI-based SMM and Sales engine" line. This is a planned internal tool not documented in the KB.

---

## E. Deprecated Items

### E1. "SolarSeat" → "SolarSeed"

Marketing.txt still uses "SolarSeat" throughout. The KB correctly flags this as the old name. No action needed — already documented in Glossary.

### E2. Earlier €500k Single Convertible Loan

The financial model supersedes the oral €500k figure with a two-tranche SAFE structure (€120k + €540k = €660k). Already flagged in Q21 of `12-Open-Questions.md`.

### E3. "Up to 1 MW" Station Size

Business-model.txt (line 348) says "not expecting to build stations more than one megawatt power." The technical doc constrains to S/M/L profiles (max 29.5 kWp benchmark). The 1 MW ceiling is a licensing boundary, not a product target.

---

## F. Recommended Actions (Priority Order)

| # | Action | Priority | Affected Files |
|---|---|---|---|
| 1 | Expand mutual leasing default mechanism with full flow | HIGH | `05-Tokenomics-and-Governance.md` |
| 2 | Document bond product as distinct revenue stream | HIGH | `02-Products.md`, `03-Business-Model.md` |
| 3 | Clarify 8% return context (bond, not SAFE) | HIGH | `09-Strategy-and-Investment.md`, Q21 |
| 4 | Add "20% guaranteed minimum" discount | MEDIUM | `02-Products.md`, `03-Business-Model.md` |
| 5 | Add strategy PDF terminology (Technofeudal Trap, Embedded Sovereign Cloud, deGigafactory) | MEDIUM | `00-Glossary.md`, `09-Strategy-and-Investment.md` |
| 6 | Fix Triple Jump Phase 2 timeline (7–18 per PDF, not 7–12) | MEDIUM | `09-Strategy-and-Investment.md`, `00-Glossary.md` |
| 7 | Add pipeline composition (3 municipalities, 7 eco-villages) | MEDIUM | `07-Customers-and-GTM.md` |
| 8 | Add equipment marketplace roadmap | MEDIUM | `02-Products.md` |
| 9 | Add batch acquisition via associations | MEDIUM | `07-Customers-and-GTM.md` |
| 10 | Add secondary lead market (€100–200) | MEDIUM | `07-Customers-and-GTM.md` |
| 11 | Add landscape/quinta management partner | MEDIUM | `08-Partnerships.md` |
| 12 | Add energy license 12–18 month timeline | MEDIUM | `12-Open-Questions.md` |
| 13 | Add server-only industrial container variant | LOW | `02-Products.md` |
| 14 | Add Y-Loyalty Impact NFTs | LOW | `00-Glossary.md`, `05-Tokenomics-and-Governance.md` |
| 15 | Add CELL company concept | LOW | `00-Glossary.md`, `06-Legal-Structure.md` |
| 16 | Add "Hosting Life" vision | LOW | `01-Company-Overview.md` |
| 17 | Add prediction market / dispute resolution token mapping | LOW | `05-Tokenomics-and-Governance.md` |
| 18 | Add 20% long-term conversion target | LOW | `13-Financial-Model.md` |
