---
title: "WeRa — Regulatory Routing and Power-Tier Matrix"
date: "2026-04-29"
type: "legal-routing-addendum"
status: "working-baseline"
purpose: "Зафиксировать, что regulator is not one address, selected title baseline is not yet proven clean, and power / grid-status tiers must be routed separately before counsel or authority use."
not_legal_advice: true
related:
  - "Strategy/Business-Model/current-business-model.md"
  - "Strategy/Legal/legal-operating-description-draft.md"
  - "Strategy/Legal/miguel-track-b1-energy-contract-memo.md"
  - "Strategy/Legal/miguel-track-b2-consumer-credit-memo.md"
  - "Strategy/Legal/miguel-track-b3-corporate-structure-memo.md"
---

## Consolidation provenance
- consolidation_actor: `WARP`
- consolidation_source: `/Users/mikhailananyin/Documents/WeRa Global/KB-latest-original/Strategy/Legal/regulatory-routing-and-power-tier-matrix.md`
- consolidation_date: `2026-06-22`
- consolidation_status: `canonicalized`


# WeRa — Regulatory Routing and Power-Tier Matrix

> This is a **pre-counsel routing addendum**, not legal advice and not a regulator submission.

## 1. Core rule

`Regulator` is not one address.

Before any external regulatory contact, the question must be routed by subject matter:

| Question family | First route | Possible authority after counsel | What belongs here | What does not belong here |
|---|---|---|---|---|
| PT energy / self-consumption / UPAC / supplier requalification | Portuguese energy counsel | `DGEG` / `ERSE` | final consumer status, UPAC registration, self-consumption, excess generation, grid/supply role, installer/technical compliance | consumer-credit licensing, CIC/STAK, securities, fund structure |
| Consumer credit / credit intermediation / financed equipment risk | consumer-finance counsel | `Banco de Portugal` | long-tenor recurring payments, zero/low upfront structures, third-party financing, installer referral / point-of-sale finance, required disclosures | UPAC technical registration, energy supplier classification, CIC/STAK design |
| Corporate / securities / fund / CIC / customer participation | corporate, securities and tax counsel | `CMVM` and tax authority if counsel advises — CMVM contacts: Luís Leal de Faria `luislealdefaria@cmvm.pt`, João Vieira dos Santos `joaovieirasantos@cmvm.pt` | PT `CIC` / OIC hypothesis, NL STAK, project SPVs, customer-to-shareholder path, tokenised or revenue-right structures | UPAC contract package, energy supply, installer thresholds |
| Tax / VAT / invoicing | tax counsel | `Autoridade Tributaria` if counsel advises | VAT treatment of service fee, lease alternative, excedente, add-ons, buy-back, SPV flows | energy-law viability as such |
| Telemetry / energy data / household data | privacy counsel | `CNPD` if counsel advises | data controller / processor role, consent, retention, energy-use data, telemetry for savings calculations | energy title, consumer credit, fund regulation |
| ES comparison path | Spanish energy / corporate counsel | competent ES energy / consumer / securities authorities if counsel advises | ESE-compatible self-consumption, Spanish entity wrapper, PT vs ES comparison on the same contract stack | using Spanish doctrine to bypass Portuguese validation for Portuguese sites |

Working rule:

- do not send one blended memo to "the regulator";
- derive an authority-specific summary only after counsel has cleaned the relevant question family;
- every authority-facing draft must state which facts are executed and which elements remain designed model.

## 1A. Characterisation gate (`hosting frame` alternative)

The routing in §1 assumes the operating object is characterised as `third-party solar operator / service-layer holder around UPAC self-consumption installation`.

A complementary characterisation has been raised internally and must be put to PT counsel before the routing in §1 is treated as final:

> the operating object could be described as `hosting of the customer's electrical equipment` (`hosting electroустановки клиента`), by analogy to infrastructure / colocation hosting in the IT sector — customer remains owner and final consumer of the equipment, WeRa provides a hosting-level service and operational continuity wrapper.

If that characterisation is legally real in Portugal, the routing in §1 may shift partially:

- the contract type could move from energy-services / `locação` toward general commercial-services / hosting / outsourcing law;
- consumer-protection and tax routes remain in place;
- the energy / UPAC route may become narrower (technical / safety only, not the contract-defining frame);
- anti-circumvention rules in PT energy law may push back.

Counsel-facing question (substantive answer requested in `miguel-track-b1-energy-contract-memo.md` §6.1, not here):

- is the hosting characterisation jurisdictionally real for our object;
- if yes, does it move us into a cleaner contractual frame, or does it create new consumer-services / outsourcing duties that are heavier than the UPAC route;
- if no, why exactly — anti-circumvention, mandatory classification, consumer-credit spillover, or other.

Until counsel answers, this remains an `open characterisation hypothesis`. The selected baseline in §2 stays as `service-fee + operator`; hosting frame is parallel arbitrage check, not a replacement.

## 1B. CMVM verbal guidance (2026-05-22)

On 2026-05-22 WeRa (Михаил + Алексей) held an introductory online call with **CMVM Inov**. This was a filter meeting, not a binding ruling, and no WeRa-specific written opinion was issued. Working takeaways for routing:

- At first stage, an **ordinary operating company** with a *general commercial or industrial purpose* (fixed service fee, no securities issuance, no collective-investment offering) is **outside CMVM's authorization perimeter**. CMVM authorises only regulated activity (investment vehicles, investment firms, IPO prospectuses), and only on the applicant's request — authorisation must be obtained **before** commencing the regulated activity.
- **Trigger into CMVM perimeter:** moving to a pooled-capital-for-pooled-return structure with passive participants (`customer → shareholder`, investment vehicle). Process: engage the **authorization department ~3 months before** intended launch; authorisation itself takes **1–2 months**.
- **Project-SPV cohort:** *not automatically* a fund — "it depends; many SPVs have another function." CMVM offered to check qualification with the authorization department **if WeRa sends a detailed description of what the SPVs actually do**. Caution: reaching for a CIC/collective-investment wrapper purely for administrative convenience is what pulls a structure *into* fund regulation.
- **Authoritative criteria** for the operating-company vs collective-investment-vehicle line: the ESMA AIFMD key-concepts guidelines (provided by CMVM) — see §5 anchor and `references/ESMA-2013-600-guidelines-AIFMD-key-concepts.pdf` (Annex III §12–22): *general commercial or industrial purpose*, *pooled return*, *day-to-day discretion or control*, *pre-existing group*. WeRa's main shield is the general commercial/industrial purpose limb.

Full debrief and transcript: `Meetings/2026-05-22-cmvm-call.md`.

## 2. Selected title baseline is not yet clean

Current selected baseline:

> customer or project-SPV title + WeRa as operator / service-layer holder + fixed service fee.

This is a **risk-balanced working selection**, not a legally confirmed clean structure.

Why it is selected for now:

- separates `owner` and `operator`;
- reduces automatic WeRa balance-sheet asset assumptions;
- helps avoid presenting WeRa as retail electricity seller;
- keeps project-SPV / portfolio-finance optionality open.

Why it remains risky:

- if the customer holds title and WeRa funds or arranges funding for the equipment, the recurring payment may look like financed equipment acquisition;
- if a project SPV holds title, the structure may raise fund, securities, tax, collateral or consumer-credit questions;
- if WeRa holds title, energy-law treatment may be clearer in some jurisdictions, but default, repossession, insurance, accounting and consumer-protection risks may become heavier.

Counsel must compare title variants side by side. The selected baseline should not be described as `clean`; it should be described as `selected for testing`.

## 3. Power / grid-status matrix

This matrix is a routing tool. It does not replace counsel.

| Tier / structure | Current working reading | Why it matters | Required questions before use |
|---|---|---|---|
| Isolated / off-grid installation | not the same legal object as grid-connected UPAC baseline | Torres Vedras appears closest to this bucket; it can evidence technical operation but not ordinary grid-supply / final-consumer wrapper | What electrical safety, insurance, property-access and contractual duties apply? Can it be used only as technical evidence? |
| `<=700 W` no-injection micro setup | public-source marker for lighter control in PT; likely irrelevant to SolarSeed commercial baseline | useful only to avoid false analogies | Is this outside the actual product range? Do not use it to infer anything about `12-500 kW` SolarSeed. |
| `>700 W` and `<=30 kW` UPAC | likely practical small-site grid-connected tier for early installs, but counsel must confirm exact procedure | may map to first small farms / households / SMEs | Who is autoconsumidor? Who submits / signs technical documentation? Can title be customer / SPV / WeRa? What contract label is safe? |
| `>30 kW` and `<=1 MW` UPAC | heavier prior-control / certification path; relevant to larger SolarSeed configs | important because SolarSeed range goes up to `500 kW` | Does the service-fee wrapper remain viable? What extra DGEG / installer / insurance / grid steps are triggered? |
| `>1 MW` | outside current SolarSeed commercial baseline, but relevant to far-path infra | should not contaminate first operating model | Treat as separate funding and permitting object. |
| Multiple modules at same site | not a safe harbor by itself | `5 x 20 kW` should not be treated as automatically different from one larger project | Are modules technically and administratively independent? Is aggregation relevant for control thresholds? |
| Collective / multi-IU / community self-consumption | separate governance and EGAC-like logic; not first subset | can be future lane, but not first clean customer subset | Who manages participants, coefficients, network-use contracts, excedente and governance? |

## 4. Torres Vedras evidence boundary

Torres Vedras should be described as:

> real technical / operating evidence for an off-grid or isolated customer-side installation with incomplete commercial wrapper.

It does not yet prove:

- grid-connected UPAC / self-consumption compliance;
- customer-as-final-consumer treatment in an ordinary grid-supply relationship;
- fixed service fee enforceability;
- consumer-credit clean recurring-payment structure;
- repeatable contract package for `12-500 kW` installations;
- `DGEG` / `ERSE`-facing authority acceptance.

Therefore, Torres Vedras can support Track A and technical investor narrative, but it should not be used as proof of Track B viability.

## 5. Official-source anchors to review with counsel

- DGEG describes UPAC / autoconsumo as regulated under `Decreto-Lei n.º 15/2022`: https://www.dgeg.gov.pt/pt/areas-setoriais/energia/energia-eletrica/producao-de-energia-eletrica/producao-descentralizada-autoconsumo-e-upp-mp-mn/autoconsumo-e-cer/3-enquadramento-legal/
- ERSE states that for individual self-consumption using the public network, the network-use contract holder must be the self-consumer; collective self-consumption uses the managing-entity route: https://www.erse.pt/comunicacao/destaques/erse-aprova-condicoes-gerais-do-contrato-de-uso-das-redes-para-o-autoconsumo/
- Banco de Portugal describes registration, information and conduct duties for credit intermediaries: https://clientebancario.bportugal.pt/pt-pt/exercicio-da-atividade-de-intermediario-de-credito
- IDAE FAQ supports the Spanish ESE-compatible distinction between consumer, owner, producer and service billing: https://www.idae.es/sites/default/files/documentos/idae/tecnologias/energias_renovables/OFICINA-de-AUTOCONSUMO/2023-03-31-99_preguntas_FAQ_v2.pdf
- ESMA Guidelines on key concepts of the AIFMD (ESMA/2013/600) — the criteria CMVM uses to classify a collective investment undertaking / AIF (operating-company vs fund line); provided by CMVM on 2026-05-22. Archived: `references/ESMA-2013-600-guidelines-AIFMD-key-concepts.pdf` (Annex III §12–22). Source: https://www.esma.europa.eu/sites/default/files/library/2015/11/2013-600_final_report_on_guidelines_on_key_concepts_of_the_aifmd.pdf

## 6. Working use

Use this file before:

- sending anything to Miguel or another counsel;
- drafting an authority-facing summary;
- interpreting installer-side threshold claims;
- using Torres Vedras as evidence in investor or legal materials;
- comparing PT and ES routes.

formal_proof:
  engine: ml-hilbert
  trl_phase: TRL6
  obligation_id: kb.governance.legal_40_regulatory_routing_power_tier_matrix_v1
  proof_artifact: kb-governance/formal-proofs/governance-legal-40-regulatory-routing-power-tier-matrix-v1.lean
  verification_status: verified
