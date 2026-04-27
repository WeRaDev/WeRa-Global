# 02 — Products

## Consolidation provenance
- consolidation_actor: `WARP`
- consolidation_source: `KnowledgeBase/02-Products.md`
- consolidation_date: `2026-04-27`
- consolidation_status: `canonicalized`


---

## 1. SolarSeed (Physical Product)

### Description
SolarSeed is an energy-first self-hosting infrastructure. Its primary function is **energy self-hosting** (local PV generation, storage, dispatch, and critical-load continuity). Its secondary function is **private server hosting** (data, collaboration, AI inference). Server hosting is a value multiplier, not the core product purpose.

Source: Technical-Description.SolarSeed.BaseConfiguration.md v2.0

### Value Proposition Hierarchy

1. **Primary: Energy self-hosting** — generate locally from PV, store and dispatch by criticality, maintain essential appliances during grid instability, reduce dependence on volatile tariffs
2. **Secondary: Private server hosting** — private data storage and collaboration, secure remote access, local AI inference and automation

### Product Architecture (Energy-First)

#### Layer E — Energy Hosting Core

| Sub-layer | Function |
|---|---|
| **E1 Generation** | PV field sized by customer demand and site irradiation |
| **E2 Conversion** | MPPT and inverter stages for efficient DC/AC management |
| **E3 Storage** | Battery bank sized by critical-load autonomy target |
| **E4 Distribution** | Protected AC/DC circuits with critical/deferrable load segregation |
| **E5 Telemetry** | Production, SOC, and load monitoring for policy control |

#### Layer D — Digital Hosting Add-On

Deployed only after E-layer stability:
- Private cloud / data workloads
- Observability and operations stack
- Local AI inference endpoint
- Edge automations linked to energy state

#### Control Principle: "Energy Budget Before Compute Budget"
- Critical appliances always have priority over non-critical digital jobs
- AI and heavy compute scheduled into high-PV windows
- Low-SOC triggers graceful service degradation, not hard failure

---

### Sizing Profiles

| Profile | PV Capacity | Daily Output | Use Case | Reference |
|---|---|---|---|---|
| **S-Profile** (Essential) | 0.6–1.0 kWp | ~2.3–3.8 kWh/day | Irrigation, lighting, minimal digital | ARS Sustineri [R2] |
| **M-Profile** (Base hybrid) | ~3.03 kWp | ~9–14 kWh/day | Critical appliances + private server + local AI | Components baseline [R1] |
| **L-Profile** (High-throughput) | 29.5 kWp | ~113 kWh/day (41,374 kWh/yr) | Large building, broad self-consumption, multi-service digital | São Martinho SmartDesign [R3] |

---

### Base Configuration BOM (M-Profile: €5,001.26)

Source: SolarSeed_base-Table-1.csv

#### Energy Subsystem (€3,450.53 — 69% of total)

| Component | QTY | Specs | Unit Price | Total | Depreciation Rate |
|---|---|---|---|---|---|
| YH SUNPRO SP505-132M10 panels | 6 | 505 W each → 3.03 kWp total | €135.00 | €810.00 | 2.5 yr |
| Voltronic Axpert MKS 3K-24 Plus | 1 | 3 kW pure sine wave, 24V, 60A MPPT, 93% peak efficiency | €640.30 | €640.30 | 1.2 yr |
| TAB Monoblock batteries | 2 | 12V 250Ah (C100) → ~6 kWh total | €349.00 | €698.00 | 1.2 yr |
| Misc (mounting, cabling) | 1 | Isolated solar kit | €192.23 | €192.23 | 2.5 yr |
| Installation | 2 | Labour units | €555.00 | €1,110.00 | — |

#### Compute Subsystem (€1,550.73 — 31% of total)

| Component | QTY | Specs | Unit Price | Total | Depreciation Rate |
|---|---|---|---|---|---|
| GEEKOM GT1 Mega Mini AI PC | 1 | Intel Core Ultra 9 185H, 16 cores/22 threads, 32GB DDR5, 2TB NVMe, Intel AI Boost NPU (8× efficiency), Wi-Fi 7, dual 2.5G LAN, 45W TDP | €899.00 | €899.00 | 0.6 yr |
| ZTE Router 5G MU5002 | 1 | 5G connectivity, 54W | €299.00 | €299.00 | 0.6 yr |
| Samsung 4TB External SSD | 1 | USB 3.2, 10W | €352.73 | €352.73 | 0.6 yr |

#### Base Operating Envelope

| Parameter | Value |
|---|---|
| Continuous compute/network load | ~264 W |
| Daily digital-load energy (24/7) | ~6.34 kWh/day |
| Battery-only digital runtime | ~18–23 hours (DoD policy dependent) |
| PV output range (3.03 kWp) | ~9.1–14.2 kWh/day (PSH/PR dependent) |
| Monthly lease price | €70.00 |
| Lease term | 240 months (20 years) |
| Monthly amortization cost | €51.62 |
| Unit ROI | 474% over lease lifetime |
| LTV per unit | €16,800 |

---

### Average Configuration BOM (€22,979.69)

Source: SolarSeed_avg-Table-1.csv

#### Energy Subsystem (€20,529.96 — 89%)

| Component | QTY | Specs | Unit Price | Total |
|---|---|---|---|---|
| AIKO-A-MAH60Db 500W Neostar panels | 16 | 500 W, n-type xBC, 22.56% efficiency, glass-glass, 25yr product warranty, 30yr 88% power warranty, 5400 Pa snow / 2400 Pa wind, 1954×1134×30mm, 27.2 kg | €146.24 | €2,339.84 |
| Huawei SUN2000-10K-LC0 hybrid inverter | 1 | 10 kW single-phase, 3 MPPT, 40–560V DC range, IP66, backup via SmartGuard, natural convection + smart air cooling, 15 kg | €1,896.00 | €1,896.00 |
| Huawei SmartGuard-63A-S0 | 1 | Whole-home backup, ≤20ms switchover, 63A max, IP55, EMMA energy assistant integrated, 10yr warranty | €983.38 | €983.38 |
| Huawei BCU Power Module LUNA2000 | 1 | Battery control unit for LUNA2000 system | €950.48 | €950.48 |
| Huawei LUNA2000 5kWh battery modules | 3 | 5 kWh LFP each → 15 kWh total, IP66, 2.5kW continuous / 3.5kW peak, 10yr warranty, modular to 30 kWh max | €2,760.96 | €8,282.88 |
| Sunfer 01V4-A coplanar mounting | 3 | Clip-bolt tile roof system | €228.00 | €684.00 |
| Huawei Smart Power Sensor DDSU666-H | 1 | Energy meter | €125.58 | €125.58 |
| AC/DC protection panel | 1 | Electrical protection | €625.40 | €625.40 |
| UPAC installation certificate | 1 | Regulatory certification | €550.00 | €550.00 |
| Production meter | 1 | Generation monitoring | €856.15 | €856.15 |
| Travel + fuel surcharge | 1 | Logistics | €40.25 | €40.25 |
| Fixing materials + sealants | 1 | Misc hardware | €186.00 | €186.00 |
| Cables (electrical + solar + ducts) | 1 | Wiring | €225.00 | €225.00 |
| Installation | 1 | Professional labour | €2,785.00 | €2,785.00 |

#### Compute Subsystem (€2,449.73 — 11%)

| Component | QTY | Specs | Unit Price | Total |
|---|---|---|---|---|
| GEEKOM GT1 Mega Mini AI PC | 2 | Same specs as base; 200W each | €899.00 | €1,798.00 |
| ZTE Router 5G MU5002 | 1 | 54W | €299.00 | €299.00 |
| Samsung 4TB External SSD | 1 | 10W | €352.73 | €352.73 |

#### Average Configuration Economics

| Parameter | Value |
|---|---|
| Total CAPEX | €22,979.69 |
| Monthly amortization | €198.02 |
| Monthly lease price | €460.00 |
| Lease term | 300 months (25 years) |
| Unit ROI | 96% (over amortization) / 435% (at €600 lease) |

---

### Optional Extension Packs

SolarSeed uses a **base + optional packs** model (automotive-style feature customization):

| Pack | Contents | Impact |
|---|---|---|
| **Extra Battery** | Additional battery modules | Longer backup, better peak-shaving |
| **Smart-House** | Smart relays, meters, room sensors, automation controller | Finer appliance control and demand scheduling |
| **Security** | CCTV, access control, alarm sensors, perimeter monitoring | Safety + surveillance continuity |
| **Household Appliances** | Pre-qualified bundles (fridge, HVAC, water heating, kitchen/laundry) | Broader electrification under SolarSeed governance |
| **Server & AI Performance** | Extra compute, storage, GPU/NPU acceleration | Heavier digital throughput within energy policies |
| **Smart Mobility / EV-Ready** | EV charger + charging policy tied to PV surplus/SOC | Transport electrification on same control plane |

All packs addable post-commissioning. Quoted with incremental CAPEX, energy demand/flexibility impact, and compatibility prerequisites.

---

### Appliance Classification and Energy-State Policy

| Class | Examples | Priority |
|---|---|---|
| **A (Critical)** | Water pumping, refrigeration, essential lighting, control gateways | Always preserved |
| **B (Important)** | Communications, office endpoints, routine automation | Reduced at low SOC |
| **C (Deferrable)** | Non-urgent compute, batch AI tasks, background sync | Suspended at low SOC |

**Energy-state policy:**
- **High PV / high SOC** → full service set including heavy AI/inference windows
- **Medium SOC** → keep A+B, throttle C
- **Low SOC** → preserve A, reduce B, suspend C until recovery

---

### Implementation Sequence

1. **Energy audit** — classify loads, define autonomy targets
2. **Sizing** — dimension PV, inverter, storage from real demand + irradiation
3. **Electrical deployment** — install protection, distribution, telemetry
4. **Energy commissioning** — validate generation, charging, critical-load continuity
5. **Digital onboarding** — deploy private services and local AI with energy-aware policies
6. **Optimization** — tune schedules, reserve thresholds, service priorities

### Acceptance Criteria
- Critical appliance uptime target met under defined outage scenarios
- SOC reserve policies enforced automatically
- Digital services available within declared energy envelopes
- Local AI operates without violating critical-load protection
- Unified observability shows energy + appliance + server state together

---

### Leasing Model
- Equipment is **leased**, not sold
- Monthly leasing rate set **minimum 20% below the customer's current electricity bill** (guaranteed; range 20–50% discount)
- **€1 symbolic first payment** (Tesla pre-order analogy)
- **20-year base lease / 25-year average lease**
- Customer receives energy production + cloud access + token rewards
- No energy community license required — self-hosting model under Portuguese law
- Energy license obtainable 12–18 months after company establishment for future energy sales

---

## 4. SolarSeed Marketplace (Proposal Calculator)

The FilantropiaSolar platform serves as the **SolarSeed proposal calculator and marketplace prototype** where customers explore and order tailored installations.

- Customer enters electricity bill data → receives personalized SolarSeed configuration
- Calculator auto-selects sizing profile (S/M/L) and extension packs based on demand
- Generates preliminary proposal with monthly lease price, savings estimate, and ROI
- Leads to Letter of Intent (LOI) → site assessment → formal proposal
- Full details in `16-FilantropiaSolar-Platform.md`

### Marketplace Services (Additional Offerings)

Beyond SolarSeed core, the marketplace includes partner services ordered through the proposal calculator:

| Service | Category | Status |
|---|---|---|
| Landscaping / gardening | Property management | Partner (gutmangardens) |
| Quinta management | Property management | Partner (gutmangardens) |
| Pool management | Property management | Partner (gutmangardens) |
| Irrigation systems | Agricultural | Partner (gutmangardens) |
| Energy-efficient appliances | Equipment lease | Roadmap |
| Gaming consoles / industrial equipment | Equipment lease | Roadmap |
| Water supply solutions | Utility | Roadmap |

Future vision: "We want to provide not only energy, but also water, everything necessary for hosting life" (strategy transcript).

---

## 5. Server-Focused SolarSeed (Secondary Business Model)

A secondary business model to be implemented after the base leasing model is established.

- **Product**: SolarCore installations focused purely on solar-powered server hosting in partnership with famrs/industrial sites
- **Form factor**: Industrial containers with compute infrastructure + solar infrastructure
- **Target**: Customers who want solar-powered cloud/AI compute on premisses in addition to energy provision
- **Part of**: WeRa Cloud business model
- **Status**: Conceptual — to be developed after base leasing model is validated
- **Origin**: Identified through ambassador candidate #3 (connections in Germany/Poland for industrial installations)

### Pre-Order
- Open for European market only
- Requires scan/copy of electricity bill (encrypted, securely stored)
- Positioned as emergency response to April 2025 Iberian blackout

---

## 2. WERA Cloud (Digital Product)

### Description
A comprehensive, secure, privacy-first alternative to proprietary cloud services (Google Workspace, Microsoft 365). Built on Nextcloud. Enables organizations to regain control over digital infrastructure.

Source: [wera.global/products](https://www.wera.global/products)

### Business Apps

| App | Function |
|---|---|
| Files | Store, share, access files from anywhere |
| Notes | Note-taking and idea organization |
| Music | Private music collection management |
| Calendar | Scheduling meetings and events |
| AI Assistant | Document Q&A, translation, writing assistance |
| Open Office | Real-time collaboration on docs, spreadsheets, presentations |
| Photos | Photo and video storage/sharing |
| Talk | P2P/group video/audio calls, screen sharing |
| Contacts | Contact and group management |
| Deck & Tasks | Project management with boards, tasks, deadlines |

### Pricing

| Plan | Label | Price | Storage | Rented Cost/User | Target |
|---|---|---|---|---|---|
| **Freemium** | Visitors | Free | 0.1 GB | -€0.0005 | Newcomers |
| **Premium** | Residents | €1/user/month (€12/yr) | 100 GB | €0.4655 | Small teams |
| **Sovereign** | Citizens | €12/user/month (€144/yr) | 1,000 GB | €4.6549 | Enterprises |

Revenue model: 80% Residents + 20% Citizens blended mix (from P&L model).

### Infrastructure Costs

| Server Type | Monthly Cost | Storage Quota | Cost/Quota |
|---|---|---|---|
| Backup (Hetzner) | €526.00 | 113,000 GB | €0.0047/GB |
| Local (SolarSeed) | €0.00 | 5,000 GB | €0.0000/GB |

### B2B2C Partner User Acquisition Model

Source: P-L-Q-Table-1.csv

| Partner | Total Users | Year 1 (0–2%) | Year 2 (2–4%) | Year 3 (4–6%) | Year 4 (6–8%) | Year 5 (8–10%) |
|---|---|---|---|---|---|---|
| WiFi Map | 180,000,000 | 0 | 360,000 | 7,200,000 | 10,800,000 | 14,400,000 |
| Ubbu | 300,000 | 6,000 | 12,000 | 18,000 | 24,000 | 30,000 |
| Soula | 100,000 | 2,000 | 4,000 | 6,000 | 8,000 | 10,000 |
| **Total** | **180,400,000** | **8,000** | **376,000** | **7,224,000** | **10,832,000** | **14,440,000** |

Cloud hosting CAC: €0.14/user. Total CAC budget: €283,250 (1,000 leads).

### Cloud Revenue Per Unit (Per SolarSeed)

| Metric | Value |
|---|---|
| Revenue per unit (Resident blend) | €2.53/month |
| LTV per cloud user | €404.77 |
| Cloud user lifespan | 120 months (10 years) |
| Own capacity per SolarSeed | 100 GB quotas |
| Gross margin (rented capacity) | 81.6% |
| Gross margin (own capacity) | Higher (zero hosting cost on SolarSeed) |

---

## 3. FilantropiaSolar (Smart Energy Platform)

### Description
Working name for the smart system to optimize energy usage, storage, and trading. Integrates with IoT and AI for efficiency improvements. Aligns with Iberia Renew Engineering's REEMS platform.

### Status
- **Stage**: Beta
- **Live features**: Solar calculator, interactive map (local testing environment)
- **In development**: CRM, energy prediction model, full energy management dashboard
- **Capitalized R&D value**: €180,000 per year (€360,000 over 2 years; in P&L as Capitalised R&D)

---

---

## Four Hubs (Marketing Layer)

1. **Energy Hub** — solar generation, storage, and smart grid management
2. **Coordination Hub** — files, sharing, chats, calls, calendar, project management (Nextcloud)
3. **Tokenization Hub** — peer-to-peer digital transactions for accounting, voting, ownership
4. **Intelligence Hub** — AI agent creation, automation, and management

---

## Product Flywheel

```
SolarSeed installed → Energy generated → Powers WERA Cloud node (COGS = €0)
    → Cloud services sold at 81.6–92% margin → Revenue shared with Solar Citizens
    → More SolarSeeds installed → Network grows
    → More data + compute → Better AI services → Higher cloud value
    → More partners embed WERA Cloud → More users → More revenue → Loop
```

## Source References

- **[R1]** `docs/reference/components.csv` — Base configuration BOM
- **[R2]** `docs/reference/ARS Sustineri.odt` — S-Profile origin model
- **[R3]** `docs/reference/São Martinho 9000-273 Funchal 4_Design One_20260309-192243.pdf` — L-Profile benchmark (29.5 kWp, Funchal, ~1,402.5 kWh/kWp/yr specific yield)
