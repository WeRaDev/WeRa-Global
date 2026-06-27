# 05 — Tokenomics and Governance

## Consolidation provenance
- consolidation_actor: `WARP`
- consolidation_source: `KnowledgeBase/05-Tokenomics-and-Governance.md`
- consolidation_date: `2026-04-27`
- consolidation_status: `canonicalized`


---

## Token Overview

WeRa uses a three-token model mapping to three entities and three governance boards:

| Token | Name | Type | Platform | Transferable | Issuing Entity | Board |
|---|---|---|---|---|---|---|
| **WeD** | WeDo | Utility / Loyalty | WeDo | Yes | WeRa Foundation (Swiss) | Impact Board |
| **WeP** | WeProfit | Staking / Dividend | WeProfit | Yes | WeRa STAK (Dutch) | Legal Board |
| **WeG** | WeGovern | Bonding / Governance | WeGovern | **No** | WeRa Capital (Portuguese) | Executive Board |

### Mapping from Transcript Labels

| Transcript Label | Formal Token | Function |
|---|---|---|
| Loyalty Token | WeD | B2C cash-back compensation for energy contributions |
| Voting Token | WeG | Bonding; quadratic voting on governance decisions |
| Dividend/Economic Token | WeP | Staking for profit-sharing from network operations |

---

## Token Mechanics

### WeD (Utility / Loyalty)
- Earned by Solar Citizens through energy production, donating, volunteering
- Represents **Impact Rights**: tokenized B2C Loyalty power equivalent to citizen's contribution to sustaining life
- "Cash-back" compensation of regular energy costs
- Transferable; can be used within the ecosystem

### WeP (Staking / Dividend)
- Represents **Profit Rights**: tokenized B2G-compliant depositary receipts
- Equivalent to investment strategies value of liquidity provision for market making and bonding activities
- Staking mechanism for profit-sharing from Network State projects
- Transferable

### WeG (Bonding / Governance)
- Represents **Ownership Rights**: tokenized B2B Real-World-Assets Securities
- Equivalent to value of assets employed in Real Impact Bond
- Collective agreement between businesses, society, and investors to maintain State infrastructure
- **Non-transferable** — governance-only token
- Quadratic voting: prevents plutocratic control

Source: [wera.global/about](https://www.wera.global/about)

---

## Blockchain Infrastructure

| Parameter | Value |
|---|---|
| **Chain** | Polygon (PoS, EVM-compatible) |
| **Token standard** | ERC-compatible (specific standards TBC) |
| **Tokenization model** | Digital Depositary Receipts (DDRs) |
| **Goal** | Tokenize shares in form of DDRs, tailored to WeRa's legal setup |
| **MiCA compliance** | Required by mid-2026 for EU operations |

### Polygon Ecosystem Context
- Polygon powers >$800M in tokenized assets ([polygon.technology/tokenization](https://polygon.technology/tokenization))
- Used by institutional players: JPMorgan tokenized cash deposits on Polygon ([Blockworks](https://blockworks.co/news/jpmorgan-trade-on-public-blockchain-monumental-step-for-defi))
- Fasanara launched tokenized money market fund on Polygon using ERC-3643 ([Tokeny](https://tokeny.com/fasanara-launches-tokenized-money-market-fund-on-polygon/))
- Full EVM-compatibility; supports permissioned RWA deployments with allowlists and role-based controls

---

## Governance Structure

### Three Boards

| Board | Entity | Jurisdiction | Primary Role |
|---|---|---|---|
| **Impact Board** | WeRa Foundation | Switzerland | Social impact oversight, utility token governance |
| **Legal Board** | WeRa STAK | Netherlands | Share administration, voting/economic rights separation |
| **Executive Board** | WeRa Capital | Portugal | Operational management, regulated financial instruments |

### BFT Governance Cascade
- Decisions cascade through the three boards using Byzantine Fault Tolerance principles
- Ensures no single entity can unilaterally control the network
- Golden Share (12%) held by Foundation provides veto over STAK decisions

### Quadratic Voting
- Used for WeG governance decisions
- Prevents concentration of voting power: cost of votes increases quadratically
- 1 vote = 1 token, 2 votes = 4 tokens, 3 votes = 9 tokens, etc.
- Implemented on-chain via Polygon smart contracts
- Academic basis: Glen Weyl & Eric Posner's "Radical Markets" (2018); practical implementations include Gitcoin Grants (quadratic funding) and Democracy Earth
- Reference implementation: [Avalanche Builder Hub — Quadratic Voting](https://build.avax.network/academy/l1-native-tokenomics/08-governance/04-quadratic-voting)

### Prediction Markets (Futarchy)
- **Token combination**: WeD (loyalty) + WeG (voting) feed into prediction markets
- Based on Robin Hanson's futarchy concept: "vote on values, bet on beliefs"
- For each governance proposal, two conditional markets are created: one for "pass" and one for "fail"
- Participants trade on expected outcomes; the market with higher confidence determines the decision
- Used for: profit reinvestment decisions, infrastructure expansion priorities, partner selection
- Reference: [MetaDAO](https://solanacompass.com/learn/Solfate/exploring-futarchy-governance-by-markets-with-metadaos-proph3t) — first futarchic DAO, operational on Solana

### Dispute Resolution
- **Token combination**: WeP (economic) tokens enable tokenized dispute resolution
- On-chain arbitration model using hybrid approach (on-chain + off-chain components)
- Options under consideration:
  - **Kleros-style crowdsourced arbitration**: anonymous jurors deposit tokens to be selected, review evidence, make decisions ([Kleros](https://kleros.io))
  - **Juris Protocol model**: staged process (self-mediation → poll judgement → binding panel)
  - **Cross-board arbitration**: disputes escalate through Impact Board → Legal Board → Executive Board
- Smart contract pauses performance during dispute, resumes upon resolution
- Reference: [Maastricht University — Dispute Resolution for Smart Contracts](https://cris.maastrichtuniversity.nl/ws/files/152295161/18580-Article_Text-51891-1-10-20220930.pdf)

### Y-Loyalty Impact NFTs
- **Token combination**: WeG (bonding) + WeD (utility) creates Y-Loyalty Impact NFTs
- Subscription-based stream of donation-loyalty points
- Used for: discounts on WERA Cloud services and recognition within the community
- NFTs represent cumulative impact contributions (energy produced, community participation)
- Source: structure.md

---

## Mutual Leasing Protection Mechanism

### Overview
When a customer cannot pay the monthly SolarSeed lease, WeRa offers a mutual leasing arrangement modelled on the telecom tower land-lease model (where operators lease a portion of land to install GSM towers).

### Default Flow

```
Customer misses lease payment
  → WeRa offers mutual leasing option (not equipment shutdown)
  → Customer signs additional leasing agreement
  → WeRa leases an adequate portion of customer's real estate
     (the land where SolarSeed equipment is installed)
  → Payment to RE owner is made via tokens (WeP)
  → Tokens are automatically consumed as the current lease payment
  → Next month: process can repeat if needed
  → Customer is transformed into shareholder via WeRa Capital
```

### Contract Terms
- **Additional leasing agreement** signed by customer, stating payment method from WeRa to the RE owner via tokens
- Tokens issued by WeRa Capital and automatically offset against monthly lease obligation
- **Liquidation protection clause**: in case of RE liquidation, WeRa reserves the right to acquire the property at the lowest market price as co-owners
- Social mission: "protecting customers and real estate from acquisition by giants like BlackRock" (strategy transcript)

### Balance Sheet Effect
- Tokenized RE fraction goes onto WeRa's balance sheet as an asset
- Shows positive profitability even during customer defaults
- During crisis/liquidation: WeRa can acquire RE at distressed prices, building asset portfolio

### Tokenization Entity
- Mutual leasing tokenization performed by **WeRa Capital** (Portuguese CIC)
- Customer is transformed into a shareholder in the CELL company holding the RWA

### Legal Framework (Portugal + EU)
- **Portuguese land lease model**: well-established under Decree-Law 294/2009 and Civil Code (Articles 1022–1063 on lease contracts). Telecom operators routinely lease rooftop/land portions under similar structures ([Analysys Mason report on EU tower land access](https://www.analysysmason.com/))
- **Real estate tokenization in Portugal**: governed by CMVM under MiCA (Law No. 69/2025, effective December 2025). First tokenized project: Sankofa Melides Resort (€4.3M, July 2025). BLOCKCHAIN.PT programme backs 26 RE tokenization products ([Tokenizer.Estate](https://tokenizer.estate/portugal))
- **Token classification**: RE tokens representing fractional SPV interests are classified as securities under MiFID II / Portuguese Securities Code (CMVM case-by-case assessment since 2018). Not covered by MiCA directly but must comply with Prospectus Regulation for public offerings >~€1M ([SQMU analysis](https://sqmu.net/real-estate-tokenisation-in-the-eu/))
- **Tax treatment**: Individuals holding tokens 365+ days: 0% capital gains (Portuguese crypto tax exemption). Short-term: 28%. Corporate: 21% headline rate ([Global Legal Insights — Portugal](https://www.globallegalinsights.com/practice-areas/blockchain-cryptocurrency-laws-and-regulations/portugal/))
- **Legal opinion**: obtained confirming mutual leasing + RE tokenization compliant under Portuguese and EU law

---

## Bond Mechanism (Funding, Not Product)

The bond is a **funding mechanism** designed for institutional investors, not a separate product.

### Structure
- **Instrument**: Convertible loan agreement structured like a bond
- **Target**: Institutional investors ("old money" seeking safety)
- **Return**: 8% stable yearly return, paid in **WeP tokens**
- **Collateral**: Backed by SolarSeed leasing agreements (recurring monthly lease payments)
- **Liquidity matching**: Bond liquidity is matched with projects for financing SolarSeed CapEx pipeline
- **Return source**: Generated by customer leasing payments flowing through dedicated smart contracts
- **Distribution**: Liquidity and return distribution via dedicated smart contracts on Polygon

### Risk-Return Profile
- Base offering: 8% stable annual return (bond-like)
- **Risk-sharing feature** (post-launch development): tool to increase returns by sharing risks with WeRa Global associated with additional products and services
- Risk-return profile is a feature to be developed after bond launch

### Relationship to YX Digital Impact Bonds
- YX Digital Impact Bonds are the formal instrument name for the acceleration phase
- Currently in concept stage — no bond prospectus or CMVM filing started
- To be structured under WeRa Capital (Portuguese CIC)

### Clarification: 8% Return Context
- The 8% return belongs to the **bond mechanism** for institutional investors
- The SAFEs for early-stage investors (€120k + €540k) have **no interest rate** — they have valuation caps
- These are different instruments and should not be conflated

---

## EU Regulatory Context

### MiCA (Markets in Crypto-Assets Regulation)
- Full enforcement: mid-2026
- Requires CASP licensing for token trading platforms
- Whitepaper requirements for token issuance
- AML/Travel Rule compliance for transfers >€1,000
- Passporting: single license covers all 27 EU countries
- WeRa Capital (CIC) will be registered under Banco de Portugal + CMVM

### Dutch STAK Framework
- Netherlands AFM opened CASP license portal April 2024 (among first EU states)
- STAK structure separates voting rights from economic interest — standard in crypto governance
- DNB (Dutch central bank) oversees AML/CTF compliance
- No prohibition on crypto use/trading in Netherlands
- Source: [Legal 500 — Netherlands Blockchain](https://www.legal500.com/guides/chapter/the-netherlands-blockchain-crypto-assets/)

### Real Estate Tokenization (EU)
- MiCA + MiFID II govern tokenized securities
- Projected €500B in tokenized real estate by 2027 (ECB estimates)
- Global tokenized RWAs reached ~$33B in 2025 (excluding stablecoins)
- Source: [CryptoverseLawyers MiCA 2026](https://www.cryptoverselawyers.io/mica-rwa-tokenization-eu-2026/)

formal_proof:
  engine: ml-hilbert
  trl_phase: TRL6
  obligation_id: kb.governance.tokenomics_05_tokenomics_and_governance
  proof_artifact: kb-governance/formal-proofs/governance-tokenomics-05-tokenomics-and-governance.lean
  verification_status: verified
