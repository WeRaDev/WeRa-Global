# 00 — Glossary and Canonical Naming

## Consolidation provenance
- consolidation_actor: `WARP`
- consolidation_source: `KnowledgeBase/00-Glossary.md`
- consolidation_date: `2026-04-27`
- consolidation_status: `canonicalized`


> Machine-readable reference for all project-specific terms, acronyms, and entities.

---

## Core Entities

| Term | Definition |
|---|---|
| **WeRa Global** | Brand and operating name of the solar network state project. Not yet formally registered; target Q2 2026. |
| **INTELIGENTE RAZÃO - UNIPESSOAL LDA** | Portuguese unipersonal limited company; incubator and current IP holder. Holds 44% founding equity. |
| **WeRa Foundation** | Planned Swiss entity (NPCSA — Non-Profit Civil Society Association). Issues WeD utility tokens. Governs via Impact Board. |
| **WeRa STAK** | Planned Dutch entity (Stichting Administratiekantoor). Issues WeP staking tokens. Managed by Legal Board. Registered at Dutch Chamber of Commerce. |
| **WeRa Capital** | Planned Portuguese entity (Collective Investment Company / CIC). Issues WeG bonding tokens (non-transferable). Regulated by Banco de Portugal + CMVM. Managed by Executive Board. |

## Products

| Term | Definition |
|---|---|
| **SolarSeed** | Physical product: energy-first self-hosting infrastructure. Primary: energy self-hosting (PV + storage + dispatch). Secondary: private server hosting (cloud + AI). Three sizing profiles: S-Profile (0.6–1.0 kWp), M-Profile (3.03 kWp, base config), L-Profile (29.5 kWp). Replaces early working name "SolarSeat". |
| **S-Profile** | Essential autonomy SolarSeed: 0.6–1.0 kWp, ~2.3–3.8 kWh/day. Farm irrigation, lighting, minimal digital. Reference: ARS Sustineri [R2]. |
| **M-Profile** | Base hybrid autonomy SolarSeed: 3.03 kWp, ~9–14 kWh/day. Critical appliances + server + AI. CAPEX: €5,001.26. Reference: components baseline [R1]. |
| **L-Profile** | High-throughput SolarSeed: 29.5 kWp, ~113 kWh/day. Large building, commercial. Reference: São Martinho SmartDesign [R3]. |
| **Base Configuration** | M-Profile BOM at €5,001.26 (69% energy / 31% compute). 6× YH SUNPRO 505W panels, Voltronic inverter, TAB batteries, 1× GEEKOM GT1 Mega. |
| **Average Configuration** | Enhanced BOM at €22,979.69 (89% energy / 11% compute). 16× AIKO Neostar 500W panels, Huawei SUN2000-10K-LC0 inverter, 15 kWh LUNA2000 battery, SmartGuard, 2× GEEKOM GT1 Mega. |
| **WERA Cloud** | Digital product: privacy-first, Nextcloud-based collaboration platform with file storage, calendar, chat, video, AI assistant, and real-time dashboards. |
| **FilantropiaSolar** | Working name for the smart energy management system (REEMS). Optimizes energy usage, storage, and trading. IoT + AI integration. Beta status: calculator + map features live locally. |
| **City of Light** | Gamified UX layer envisioning SolarSeed infrastructure as a living city with Digital Land (cloud) and Real Land (solar hardware). Conceptual / roadmap stage. |

## Tokens

| Token | Full Name | Type | Platform | Transferable | Issuing Entity |
|---|---|---|---|---|---|
| **WeD** | WeDo token | Utility / Loyalty | WeDo | Yes | WeRa Foundation |
| **WeP** | WeProfit token | Staking / Dividend | WeProfit | Yes | WeRa STAK |
| **WeG** | WeGovern token | Bonding / Governance | WeGovern | No | WeRa Capital |

## Blockchain & Legal

| Term | Definition |
|---|---|
| **DDR** | Digital Depositary Receipt — tokenized share representation on Polygon blockchain. |
| **Polygon** | EVM-compatible blockchain selected for WeRa's web3 infrastructure. Supports RWA tokenization with institutional adoption (>$800M tokenized assets). |
| **MiCA** | EU Markets in Crypto-Assets Regulation (2023/1114). Full enforcement mid-2026. Governs token issuance, CASPs, AML. |
| **STAK** | Stichting Administratiekantoor — Dutch foundation structure that separates voting rights from economic interest. Common in crypto governance. |
| **BFT** | Byzantine Fault Tolerance — governance cascade model used across the three WeRa entities. |
| **Golden Share** | 12% non-transferable governance instrument reserved for WeRa Foundation; veto power over STAK decisions. |
| **YX Digital Impact Bonds** | Bond instrument planned for WeRa's acceleration phase. |

## Customer / Market Terms

| Term | Definition |
|---|---|
| **Solar Citizens** | End users / prosumers in the WeRa ecosystem. Receive Impact, Ownership, and Profit rights. |
| **Segment 1** | Ideological prosumers (eco-conscious, values-driven, 30–50 age range). |
| **Segment 2** | Cost-driven local businesses / SMEs. |
| **Segment 3** | General public (future tier, strategy pending). |
| **DePIN** | Decentralized Physical Infrastructure Network — blockchain-incentivized physical infrastructure. |
| **Negative-COGS** | WeRa's model where the cost of goods is offset by energy production; own-capacity cloud hosting at €0.00/GB vs. €0.0047/GB rented. Hardware pays for itself over the 20–25 year lease. |
| **Energy-First** | SolarSeed design principle: "energy budget before compute budget". Layer E (energy) must be stable before Layer D (digital) is deployed. |
| **Class A/B/C** | Appliance priority classes: A = Critical (always on), B = Important (reduced at low SOC), C = Deferrable (suspended at low SOC). |
| **Triple Jump** | Three-phase growth strategy: Phase 1 (Months 1–6), Phase 2 (Months 7–18), Phase 3 (Months 18–24). Per Strategy PDF. |
| **CELL** | Administration unit / sub-fund within WeRa Capital (CIC). Each CELL holds a cohort of co-owned RWAs with legally segregated assets. Acts as a daughter-company. |
| **Technofeudal Trap** | Users locked into centralized ecosystems because switching friction is high, not because products are superior. WeRa's problem framing for investors. |
| **Embedded Sovereign Cloud** | Formal name for the B2B2C strategy where WERA Cloud is embedded inside partner platforms (Soula, Ubbu, WiFi Map). |
| **deGigafactory** | The 1-million-node long-term expansion goal; distributed manufacturing of infrastructure vs centralized mega-factories. |
| **Y-Loyalty Impact NFTs** | NFTs created by combining WeG (bonding) + WeD (utility) tokens. Subscription-based donation-loyalty points for discounts and recognition. |
| **UNITY** | Sunified Group's deep tech micro-sensor manufactured into solar panels. Creates immutable layer-0 energy data. Enables quantum-resistant encryption, tokenization, carbon credits. |
| **Mutual Leasing** | Default protection mechanism: when customer can't pay, WeRa leases a portion of their real estate (telecom tower model), paying via tokens that auto-consume as lease payment. |
| **Futarchy** | Governance mechanism using prediction markets: "vote on values, bet on beliefs." Used for WeD + WeG decisions in WeRa's governance. |
| **Proposal Calculator** | FilantropiaSolar's solar calculator feature used as the SolarSeed marketplace prototype for customer acquisition. |
| **LOI** | Letter of Intent signed by customer via email after calculator proposal, before site assessment. Non-binding. |
| **SIC** | Sociedade de Investimento Coletivo — Portuguese Collective Investment Company. The corporate form for WeRa Capital. |

## Partners

| Term | Definition |
|---|---|
| **Iberia Renew Engineering** | Signed installation partner. Based in Funchal, Portugal. Founded May 2025. Operates across Baltic and Iberian regions. Parent: RENEW ENGINEERING LLC (Lithuania, renewlt.com). |
| **Soula** | Mental health AI app for women. Co-founded by Natallia Miranchuk and Andrei Kulik. Personal relationship established; MoU pending. |
| **Ubbu** | EdTech platform teaching coding to children 6–12. 350,000+ students in 1,500+ schools across 20+ countries. Personal relationship established; MoU pending. |
| **WiFi Map** | DePIN connectivity app with 170M+ users (external verification; WeRa documents cite 180M). Personal relationship established; MoU pending. |
| **Sunified** | Sunified Group BV (Netherlands). Deep tech energy data company. UNITY micro-sensor supplier partner target. Creates quantum-resistant, blockchain-connected smart panels. Full profile in `15-Sunified-Quantum-Resistance.md`. |
| **Mitsubishi Group** | Personal connection with Director of International Relations & Partnerships. No formal engagement yet. |

## Phases

| Phase | Description | Timeline |
|---|---|---|
| **Incubation** | Current phase. Pre-registration, prototype, first customer. | Now → Q2 2026 |
| **Acceleration** | Post-registration. Formalize legal structure, partner agreements, scale platform. | Q2–Q3 2026 (3 months) |
| **Scaling** | Post-seed. Deploy first 100 SolarSeed units, hire team of 16, expand customer base. | Q3 2026 → Q4 2027 (15 months) |

## Geography

| Location | Relevance |
|---|---|
| **Torres Vedras, Portugal** | Pilot customer: off-grid micro-farm, ~2-person household scale. |
| **Lisboa, Portugal** | Company HQ. |
| **Sintra, Portugal** | Founder location. |
| **Funchal, Portugal** | Iberia Renew Engineering HQ. |

formal_proof:
  engine: ml-hilbert
  trl_phase: TRL6
  obligation_id: kb.governance.standards_00_glossary
  proof_artifact: kb-governance/formal-proofs/governance-standards-00-glossary.lean
  verification_status: verified
