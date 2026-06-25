---
title: "WeRa — Legal Operating Description Draft"
date: "2026-04-23"
updated: "2026-04-24"
type: "legal-operating-description"
status: "pre-counsel-draft"
purpose: "Полное юридико-операционное описание текущей модели WeRa для подготовки counsel memos и последующих authority-specific regulator-facing summaries."
not_legal_advice: true
source_of_truth:
  - "Strategy/Business-Model/current-business-model.md"
  - "Strategy/Business-Model/starter-drr.md"
  - "Strategy/Business-Model/UTS.md"
  - "Strategy/Business-Model/claim-register.md"
  - "Strategy/Business-Model/executed-vs-designed.md"
  - "Strategy/Business-Model/capital-architecture.md"
  - "Strategy/Business-Model/open-gates.md"
  - "Strategy/Business-Model/torres-vedras-pilot-questionnaire.md"
  - "Strategy/Legal/regulatory-routing-and-power-tier-matrix.md"
---

## Consolidation provenance
- consolidation_actor: `WARP`
- consolidation_source: `/Users/mikhailananyin/Documents/WeRa Global/KB-latest-original/Strategy/Legal/legal-operating-description-draft.md`
- consolidation_date: `2026-06-22`
- consolidation_status: `canonicalized`


# WeRa — Legal Operating Description Draft

> This is a **pre-counsel working draft**, not a legal opinion and not a regulator submission.

> Regulatory routing update (`2026-04-24`): this draft must not be turned into one generic "regulator memo". Energy / UPAC questions, consumer-credit questions, CIC/securities questions, tax questions and telemetry/data questions have different counsel and authority routes.

Цель документа — описать WeRa так, чтобы юрист мог проверить:

- что именно является текущим operating object;
- какие роли сторон предполагаются;
- где selected baseline, а где альтернативы;
- где факты подтверждены, а где есть только founder-memory / hypothesis;
- какие вопросы нужно вынести в отдельные counsel memos.

Документ сознательно не пытается доказать, что модель уже юридически чистая. Его задача — подготовить точную и не расползающуюся юридическую гипотезу.

Read together first:

- `Strategy/Legal/regulatory-routing-and-power-tier-matrix.md`

## 1. One-Sentence Legal Hypothesis

`Selected baseline`:

> WeRa acts as a third-party solar service/operator layer around distributed self-consumption installations, with the customer remaining the final consumer in the relevant local self-consumption regime, the core solar asset preferably titled at customer or project-SPV level, and WeRa monetising through a fixed service fee for access, monitoring, coordination, billing and operational management, not through retail electricity resale or kWh-based supply.

Русская формула:

> WeRa выступает как third-party оператор / service-layer holder распределённых self-consumption солнечных установок. Клиент остаётся final consumer, основной solar asset в selected baseline предпочтительно находится на титуле клиента или project SPV, а выручка WeRa описывается как fixed service fee за доступ, мониторинг, координацию, биллинг и эксплуатационный контур, а не как продажа электроэнергии или `€/kWh` billing.

## 2. Document Discipline

В этом документе используются четыре статуса:

- `selected baseline` — текущая рабочая модель для юридической проверки.
- `live alternative` — вариант, который может оказаться лучше после counsel / tax / capital review, но сейчас не выбран.
- `open legal hypothesis` — вопрос, который нельзя подавать как решённый.
- `far path` — стратегически возможный, но не относящийся к текущему first operating object вариант.

Ключевое правило: **не смешивать operating object, legal wrapper, monetization add-ons, long-term moat and investor story**.

## 3. Current Operating Object

### 3.1 What WeRa is

WeRa на текущем этапе — это solar service/operator business around distributed self-consumption assets.

WeRa:

- sources and qualifies customer opportunities;
- coordinates site assessment and technical scoping;
- contracts with installer partners;
- structures customer-facing recurring payment logic;
- coordinates installation, commissioning, telemetry and ongoing operations;
- manages monitoring, support, billing and customer interface;
- may attach optional digital services later.

### 3.2 What WeRa is not in the selected baseline

WeRa is not currently described as:

- retail electricity supplier / commercializadora;
- installer of record;
- EPC contractor;
- generic cloud provider;
- distributed compute marketplace;
- GPU datacenter operator;
- token-governed investment network;
- fully formed collective investment / CIC structure;
- consumer-credit lender.

Some of these may become alternatives or later structures, but they must not define the first legal object.

## 4. Parties and Roles

### 4.1 Customer

`Selected baseline`:

The customer:

- remains the final consumer in the relevant self-consumption regime;
- controls or has lawful access to the consumption site / roof / property;
- receives a functioning self-consumption solar installation and service layer;
- pays a fixed recurring service fee or neutral monthly payment, depending on final contract drafting;
- does not buy electricity from WeRa on a `€/kWh` retail basis.

Open issues:

- whether the customer holds title to the solar equipment;
- whether a project SPV holds title;
- whether any end-of-term transfer / purchase option exists;
- whether the recurring payment could be characterised as consumer credit or disguised equipment finance.

### 4.2 WeRa

`Selected baseline`:

WeRa:

- acts as third-party operator / service-layer holder;
- does not automatically hold legal title to the solar asset;
- coordinates the commercial, operational and digital layer;
- bills the customer for the service wrapper;
- interfaces with installer partners;
- monitors the installation through edge telemetry;
- may arrange or contribute to financing, subject to legal qualification.

WeRa must not be described as `owner/operator` without qualification. `Owner`, `operator`, `lessor`, `service provider`, `manager` and `financier` are separate roles.

### 4.3 Installer Partner

The installer partner:

- performs technical site assessment;
- designs and installs the system;
- handles installer-side compliance and technical commissioning;
- may perform field maintenance;
- should remain distinct from WeRa unless counsel confirms otherwise.

Current evidence:

- Iberia Renew Engineering is signed as an installation partner.
- This proves delivery-side relationship, not yet repeatable channel volume.

### 4.4 Grid Supplier / Commercializer

`Selected baseline`:

The customer keeps the grid-supply relationship with the electricity supplier / commercializer.

Reason:

- this preserves the distinction between self-consumption service and retail electricity supply;
- it reduces risk that WeRa is recharacterised as an electricity supplier;
- it keeps customer / supplier / grid-operator rights and obligations clearer.

`New founder hypothesis, not baseline`:

Misha suggested that WeRa could potentially manage or even take over parts of the grid-supply relationship as a "hosting company" / energy-service proxy, buying residual electricity when the solar installation does not cover all needs.

Current status:

- `open legal hypothesis`;
- potentially valuable as customer simplification;
- not safe to include in selected baseline before counsel review;
- may trigger supply, agency, billing, consumer-protection or requalification issues.

### 4.5 Project SPV

`Live alternative / scaling option`:

A project SPV may hold title to one installation or a pool of installations, while WeRa manages the contract stack and operations.

Potential advantages:

- cleaner asset ring-fencing;
- clearer lender collateral;
- separation of operational company and asset pool;
- future bankability.

Open issues:

- who capitalises the SPV;
- whether customers contract with WeRa, SPV or both;
- tax and VAT treatment;
- default and de-installation rights;
- whether the structure increases or reduces consumer-credit exposure.

## 5. Asset and Title Logic

### 5.1 Selected baseline title posture

The selected posture is:

- client or project-SPV title preferred;
- WeRa as service/operator layer;
- WeRa-owned balance-sheet asset remains live alternative, not default baseline.

Status:

> `selected working baseline for testing`, not counsel-confirmed clean structure.

Rationale:

- keeps operator and owner roles separated;
- avoids assuming WeRa has immediate balance-sheet capacity for assets;
- may reduce legal and accounting complexity at first;
- preserves optionality for future SPV / portfolio financing.

Risk:

- customer-title may help energy-law separation but can increase consumer-credit / disguised-equipment-finance risk if WeRa funds or arranges the customer's equipment acquisition;
- project-SPV title may help asset pooling but can add securities, fund, tax, collateral or consumer-credit questions;
- WeRa-title may be cleaner for true lease in some situations but heavier for default, repossession, insurance and balance-sheet treatment.

### 5.2 Live alternatives

| Variant | Status | Why it matters | Counsel question |
|---|---|---|---|
| Client-owned asset + WeRa operator | `selected working baseline for testing` | may be clean for energy-law separation, but not necessarily for consumer-credit | Does the service fee avoid consumer-credit / supplier requalification if WeRa funds or arranges equipment economics? |
| Project-SPV-owned asset + WeRa operator | `live scaling alternative` | cleaner asset pooling and finance shell, but possible fund/securities/tax questions | What entity contracts with customer, installer, insurer and lender? |
| WeRa-owned asset + customer lease/service payment | `live but heavier alternative` | may be clearer for true lease / collateral | Does it create stronger consumer-credit, repossession and insurance risk? |
| WeRa-owned asset + external compute monetization in same object | `fragile / not baseline` | mixes solar and compute | Should be avoided unless separated. |

## 6. Product and Technical Layer

### 6.1 SolarSeed

SolarSeed is the physical solar product family:

- PV generation;
- inverter / control layer;
- battery or storage where applicable;
- installation and commissioning;
- edge telemetry device.

### 6.2 Edge / telemetry layer

The edge device is mandatory for baseline telemetry and local data capture.

Its legal role:

- accessory infrastructure to the solar service;
- not proof that WeRa is a cloud or compute business;
- not a standalone external compute marketplace in the selected baseline.

Open issue:

- current BOM still carries a legacy compute share; an edge-only BOM recut is required before investor or regulator materials reuse the current cost split.

## 7. Contract Package — Selected Baseline

The selected baseline likely requires a contract package containing at least:

1. Customer service agreement:
   - role of WeRa;
   - fixed service fee / monthly payment;
   - no `€/kWh` resale;
   - access and operating rights;
   - monitoring and data terms;
   - maintenance obligations;
   - default and termination.
2. Site / roof access consent:
   - installation permission;
   - access for maintenance;
   - de-installation rights;
   - property damage responsibilities.
3. Installer agreement:
   - technical scope;
   - compliance obligations;
   - warranties;
   - insurance;
   - handover / commissioning.
4. Asset title / ownership schedule:
   - equipment owner;
   - beneficial control;
   - rights at default;
   - end-of-term transfer / purchase option, if any.
5. Insurance and liability schedule:
   - fire;
   - roof damage;
   - third-party damage;
   - theft / vandalism;
   - force majeure;
   - storm / hail events.
6. Data and telemetry terms:
   - what is collected;
   - where it is stored;
   - who can access it;
   - customer dashboard rights;
   - use of data for savings calculation.

This package is not yet drafted and requires counsel validation.

## 8. Revenue and Billing Logic

### 8.1 Selected label

The selected baseline revenue label is:

> `fixed service fee`

Reason:

- separates WeRa from `€/kWh` electricity resale;
- avoids premature `lease fee` language unless true lease is selected;
- avoids `facility fee`, which may sound like financing / credit.

### 8.2 Pricing logic

The recurring payment may be commercially calculated using:

- cost of installation;
- installer cost;
- licensing / compliance / connection cost;
- maintenance and support cost;
- expected system lifetime;
- replacement assumptions;
- customer bill baseline;
- customer load and device inventory;
- desired discount level;
- target return over contract term.

However, counsel should confirm whether the contract may refer to these calculations without creating:

- disguised equipment finance;
- consumer-credit characterisation;
- kWh-linked energy resale;
- misleading savings guarantee.

## 9. The 20% Savings Claim

### 9.1 Current status

`20% savings guaranteed` is currently:

- externally visible in legacy / GTM materials;
- founder-supported as a pricing logic;
- not yet evidence-carried as canonical promise;
- not proven by Torres Vedras.

### 9.2 Founder logic

Misha's explanation:

- a 20% discount may be achievable over a long contract term of `240-360` months;
- founder target is to preserve more than `10%` annual yield across the full contract life;
- the model can tune discount by using 12 months of customer bills and device/load information;
- replacement component costs may decline over time;
- declining replacement component costs may create an amortisation buffer over the long contract period;
- additional services may increase average revenue while keeping the customer's total spend below or near their prior energy budget.

### 9.3 Legal-safe status

Until validated, this should be framed as:

> `conditional underwriting / calculator output`, not universal baseline promise.

Safe draft wording:

> WeRa may offer a customer-specific projected savings proposal where sufficient historical bill and load data are available. Any guaranteed discount should be limited to contractually defined conditions and should not be presented as a universal claim until validated by counsel and supported by segment-level calculations.

Possible discount-policy framing:

- discount tier should depend on available customer data;
- maximum discount tier should require at least 12 months of electricity bills and a device/load inventory;
- lower-information customers should receive either a lower discount tier, a non-guaranteed projection, or a proposal subject to later verification;
- the underwriting model should explicitly show CAPEX, installer/licensing costs, term length, replacement assumptions, expected yield and customer-bill baseline.

## 10. Add-On Monetization Layer

`Optional / monetization add-on`, not baseline:

- additional battery storage;
- energy-efficient appliances;
- security systems;
- smart-house components;
- gardening / landscaping;
- pool maintenance;
- partner services around property operation.

Commercial logic:

- if solar reduces the customer's energy burden, part of the savings wallet may be used for additional services;
- this may increase average customer value;
- partner services may strengthen the channel and ecosystem.

Legal caution:

- add-ons should not obscure the core service fee;
- partner services may create separate liability, warranty and consumer-protection obligations;
- bundled offers may require clear pre-contractual disclosure.

## 11. Electricity Supply and Self-Consumption

### 11.1 Selected baseline

The selected baseline assumes:

- customer remains final consumer;
- customer retains ordinary supply relationship;
- WeRa does not sell electricity to the customer;
- self-consumption remains the core energy logic.

### 11.2 Supply-management hypothesis

Misha's comment suggests a possible stronger customer convenience layer:

- WeRa could act as proxy / manager for the grid-supply relationship;
- WeRa could procure residual electricity when the installation does not cover all needs;
- customer could receive a simplified single service relationship.

Current status:

- `open legal hypothesis`;
- not selected baseline;
- not to be included in authority-facing summary until counsel-reviewed.

Questions for counsel:

- Can WeRa manage the supplier relationship as agent without becoming supplier?
- Can WeRa be the contract holder for residual electricity supply while the customer remains final consumer?
- Would this create electricity resale, aggregation, supply or consumer-protection obligations?
- What disclosures and authorisations would be required?

Official regulatory pointers to review with counsel:

- ERSE describes electricity supply contracts, supplier switching, pre-contractual information, additional services and consumer rights: https://www.erse.pt/en/energy-consumers/eletricity/contractingswitching-supplier/
- ERSE states that, for individual self-consumption using the public network, the network-use contract holder must be the self-consumer; collective self-consumption uses the collective managing entity logic: https://www.erse.pt/communication/highlights/erse-approves-general-conditions-of-the-contract-for-the-use-of-the-networks-for-self-consumption/
- DGEG describes UPAC / autoconsumo as regulated under Decree-Law 15/2022: https://www.dgeg.gov.pt/pt/areas-setoriais/energia/energia-eletrica/producao-de-energia-eletrica/producao-descentralizada-autoconsumo-e-upp-mp-mn/autoconsumo-e-cer/3-enquadramento-legal/

## 12. Regulatory Classification Risks

### 12.0 Routing by authority

`Regulator` is not one address.

| Route | Question family | Counsel memo |
|---|---|---|
| `DGEG` / `ERSE` after Portuguese energy counsel | UPAC, self-consumption, final consumer, supplier requalification, excess generation, network-use, installer/technical compliance | `miguel-track-b1-energy-contract-memo.md` |
| `Banco de Portugal` after consumer-finance counsel | consumer credit, credit intermediation, financed equipment, third-party financing, installer referral / point-of-sale finance | `miguel-track-b2-consumer-credit-memo.md` |
| `CMVM` after corporate/securities/tax counsel | PT CIC / OIC, STAK, customer participation, tokens, revenue rights, fund regulation | `miguel-track-b3-corporate-structure-memo.md` |
| tax authority after tax counsel | VAT, invoices, stamp duty, excedente, service fee and lease alternative | `miguel-track-b3-corporate-structure-memo.md` |
| privacy authority / CNPD if needed | telemetry, household energy data, consent, retention, controller / processor roles | B.1 data section + privacy counsel |

Do not send a blended external regulator package before counsel gives an authority-specific routing map.

### 12.1 Energy-law risk

Main risk:

- WeRa is recharacterised as electricity supplier or retail reseller.

Avoidance logic:

- no `€/kWh` billing to customer;
- customer remains final consumer;
- generation is for self-consumption;
- WeRa provides service/operator layer;
- excess generation is separately analysed;
- supply contract remains with customer unless counsel validates another arrangement.

### 12.2 Consumer-credit / intermediation risk

Main risk:

- recurring payment is characterised as financing of equipment to a consumer or microbusiness.

This risk is acute when:

- customer is an individual;
- the customer avoids upfront CAPEX;
- payment duration is long;
- asset transfer or buyout exists;
- default mechanics look like financed purchase.

Counsel must answer whether the selected model requires:

- consumer-credit licence;
- credit-intermediary registration;
- specific disclosures;
- APR / total cost disclosure;
- restrictions on marketing and guarantees.

### 12.3 Installer / technical compliance risk

WeRa should not be installer of record unless it has the required status. The installer partner should carry the installation-side compliance and warranties.

Open questions:

- thresholds for installer-side licensing and DGEG control by power / grid-status tier;
- who signs technical documentation;
- who is responsible for connection and commissioning;
- whether the system is off-grid, grid-tied or hybrid.

The oral `21-25 kW` threshold should not be used as an operational legal fact. Counsel must map isolated/off-grid, `>700 W`, `<=30 kW`, `>30 kW`, `>1 MW`, multi-module and collective cases separately.

### 12.4 Data / telemetry risk

Edge telemetry may collect:

- generation data;
- consumption data;
- battery status;
- device / usage patterns;
- potentially personal or household-behaviour data.

Counsel should verify:

- data controller / processor roles;
- consent requirements;
- data minimisation;
- retention;
- use of telemetry for savings calculations.

## 13. Torres Vedras Evidence Status

### 13.1 What Torres Vedras proves

Torres Vedras currently supports:

- existence of a real installed object;
- technical and operator familiarity;
- off-grid micro-farm / small-household equivalent context;
- founder-built deployment capability;
- founder-reported client-funded CapEX path;
- founder-reported verbal agreement;
- reported maintenance check after storms.

### 13.2 What Torres Vedras does not yet prove

Torres Vedras does not yet prove:

- repeatable commercial baseline;
- clean contract package;
- recurring-payment behaviour;
- measured bill-vs-bill savings;
- external-grade payment trail;
- title / ownership / de-installation rights;
- insurance and liability allocation;
- finance-ready portfolio evidence.

### 13.3 Missing evidence pack

Before using Torres Vedras externally as commercial proof, collect:

- signed written agreement or memorialisation;
- payment trail by component / installer / logistics;
- ownership / control / removal memo;
- telemetry export and proxy-savings sheet;
- maintenance ledger;
- site-verified as-built inventory;
- liability / insurance notes.

## 13A. Two Separate Counsel Tracks

This draft must be split into two legally separate tracks before being sent to Miguel or any other counsel.

Reason:

- Torres Vedras is an executed object with an incomplete commercial wrapper.
- The prospective selected baseline is a designed model for future repeatable contracts.
- If these two tracks are blended, counsel may answer a hybrid that is neither the actual pilot nor the intended baseline.

### 13A.1 Track A — Retrospective Torres Vedras Qualification

Purpose:

> Ask counsel to characterise the legal status of what already happened in Torres Vedras and to identify the minimum written carrier needed now.

Track A should answer:

- What is the legal character of the current Torres Vedras arrangement?
- Does the reported client-funded CapEX create ownership, reimbursement, loan, donation, informal service, lease, mandate or other legal reading?
- What risks are created by the current verbal / founder-memory state?
- What can be signed now as a truthful memorialisation without worsening the legal position?
- Who must sign: site owner, beneficiary, founder, future WeRa entity, or another party?
- What should be said about title, operational control, access, de-installation, maintenance, liability and future buy-back?

Track A should not answer:

- whether the future selected `service-fee + operator` baseline is viable;
- whether WeRa should use PT CIC / NL STAK;
- whether customer-shareholder conversion is possible.

### 13A.2 Track B — Prospective Baseline Design

Purpose:

> Ask counsel to design or validate the future repeatable `service-fee + operator first` contract package.

For counsel packaging, Track B is split into three specialist memos:

- `Track B.1` — Portuguese energy-law and contract package.
- `Track B.2` — consumer-credit / financial-intermediation classification.
- `Track B.3` — corporate / securities / tax structure.

Together, these should answer:

- Can the selected PT structure work with customer as final consumer, WeRa as third-party operator, fixed service fee and no disguised kWh resale?
- Which Portuguese contract type is safest: `prestação de serviços`, `locação`, `contrato misto/atípico`, or another form?
- Which asset-title posture is legally cleanest for first contracts: customer title, project SPV title or WeRa title?
- Does the recurring payment trigger consumer-credit or financial-intermediation rules?
- How should default, de-installation, end-of-term ownership, insurance and liability be written?
- Can WeRa manage the grid-supply relationship as an authorised service layer without becoming supplier?
- Which entity / SPV / fund / tax structure is proportionate for first contracts?
- What regulator-facing wording is safe after counsel review?

Track B should not assume:

- Torres Vedras already proves commercial repeatability;
- the `20%` discount is universally guaranteed;
- STAK/CIC/tokenised real-estate mechanisms are part of the first operating model.

### 13A.3 Working Rule for Counsel Package

When sending to counsel:

- Track A must carry evidence status labels (`FACT`, `MEMORY`, `ESTIMATE`, `UNKNOWN`).
- Track B must carry model status labels (`selected baseline`, `live alternative`, `open legal hypothesis`, `far path`).
- Counsel should be asked to answer the two tracks separately.
- Any response that blends the tracks should be treated as incomplete and clarified.

## 14. Corporate / Securities / Tax Architecture

### 14.1 Current selected position

No final corporate / securities structure is selected yet.

For current legal-operating analysis, the minimum necessary structure is:

- operating entity or pre-formation operating team;
- installer contracts;
- customer service agreements;
- possible project SPVs later;
- financing instruments for proof-stage CAPEX.

### 14.2 STAK -> PT CIC hypothesis

Misha's founder hypothesis:

- NL STAK could sit above PT CIC / collective investment company;
- this may simplify future tokenisation / depositary receipts / administrative fund logic;
- starting with PT company and later transferring shares to NL admin foundation may create additional bureaucracy.

Current status:

- `open corporate / securities / tax hypothesis`;
- not selected baseline;
- must not block first operating contract package;
- requires counsel beyond energy lawyer.

Questions:

- What exact Portuguese structure is meant by "CIC"?
- Is it legally available and proportionate for this stage?
- Can it hold or finance many small solar assets?
- Does it trigger fund regulation / collective investment restrictions?
- Can customers become economic participants without securities-law issues?
- Is NL STAK appropriate before first Portuguese operating validation?
- What is the concrete cost/time difference between `STAK-first -> PT vehicle` and `PT-first -> later transfer to NL foundation / STAK`?
- Would later ownership transfer to an NL foundation / STAK trigger additional Portuguese approvals, taxes, notary steps, bank/KYC steps or registry filings?

### 14.3 Customer -> shareholder conversion

Current status:

- `far path / separate counsel track`;
- not current operating model.

Reason:

- mixes customer contract, securities, tax and possibly consumer-finance logic;
- may change the entire regulatory profile of the company;
- should not be included in energy-law baseline.

## 15. Real-Estate Tokenization / Crisis Payment Hypothesis

Misha's comment:

- if a customer cannot pay, they could "digitise" real estate where the installation is located;
- WeRa could accept a tokenised share of the property as payment;
- WeRa may obtain priority buyout rights in liquidation / crisis.

Current classification:

> `far path / high-risk legal-financial hypothesis`.

Why not baseline:

- likely engages real-estate law;
- likely engages securities / tokenisation regulation;
- may be seen as secured lending, distressed acquisition, consumer-credit or unfair-practice risk;
- not supported by current pilot evidence;
- not needed to validate first solar service/operator model.

Counsel track required:

- corporate / securities;
- real estate;
- tax;
- consumer protection;
- insolvency / enforcement;
- tokenisation / digital assets.

This hypothesis should not appear in regulator-facing energy summary unless a lawyer explicitly asks for a full long-term structure map.

## 16. Portugal and Spain

### 16.1 Portugal

Portugal is the immediate operating reality:

- current pilot is in Torres Vedras;
- near-term relationships are in Portugal;
- UPAC / autoconsumo language is relevant.

Current status:

- PT service/operator wrapper = `open legal hypothesis`;
- desk research indicates conditional viability, not certainty;
- local counsel must validate exact contract package.

### 16.2 Spain

Spain appears structurally attractive for ESE-compatible self-consumption models.

Current status:

- `research-supported, not counsel-confirmed`;
- possible cleaner scale wrapper;
- not a replacement for PT validation if the first operating reality remains PT.

### 16.3 Cross-border vocabulary rule

Do not use `autoconsumidor` as pan-Iberian shorthand.

Use:

- PT: `UPAC / autoconsumidor`;
- ES: `self-consumption consumer / ESE-compatible structure`;
- bridge label: `final consumer`.

## 17. Authority-Specific Regulator-Facing Narrative Boundaries

Any authority-facing summary must name its authority route.

Energy / UPAC-facing summary may say, after counsel review:

- WeRa is exploring a solar self-consumption service/operator model;
- customer remains final consumer;
- WeRa does not intend to sell electricity on a retail `€/kWh` basis;
- installation is carried out by qualified installer partners;
- WeRa coordinates service, monitoring, maintenance and billing;
- exact asset title and contract package are under counsel review;
- WeRa seeks preliminary feedback on avoiding requalification into supply activity.

Consumer-finance-facing summary should instead focus on:

- whether the long-term recurring payment, title posture and CAPEX funding path create consumer-credit or credit-intermediation duties;
- whether installer-channel referrals or lender introductions create point-of-sale finance risk.

Corporate/securities-facing summary should instead focus on:

- whether PT `CIC` / OIC, NL STAK, project SPVs, customer participation, revenue rights or tokenised mechanisms are legally available and proportionate;
- whether any of those are first-stage requirements or later structures.

No authority-facing summary should say:

- WeRa is a hosting company that buys and resells residual electricity;
- WeRa guarantees universal 20% savings;
- WeRa already has a validated CIC/STAK/tokenisation structure;
- customers can pay with tokenised real estate;
- Torres Vedras proves the full commercial model.
- the selected client/project-SPV title structure is already clean;
- `21-25 kW` is a settled operational threshold.

## 18. Counsel Memos to Derive From This Draft

### 18.1 Energy / local regulatory counsel memo

Core questions:

- Is selected `service-fee + operator` wrapper viable in Portugal?
- Which Portuguese contract type is safest: `prestação de serviços`, `locação`, `contrato misto/atípico`, or another form?
- What exact customer contract package is required?
- Can WeRa avoid supplier classification?
- What happens with excess generation?
- What documents would regulator expect?
- Which regulator or authority should receive which question, if any?
- Which power / grid-status tier applies to the first customer subset?
- Can WeRa manage supplier relationship as agent or contract holder?
- Is the same contract stack materially cleaner in Spain, and should an ES colleague review it?

Draft memo:

- `Strategy/Legal/miguel-track-b1-energy-contract-memo.md`

### 18.2 Consumer-credit / financial intermediation memo

Core questions:

- Does long-term recurring payment equal consumer credit?
- Does zero/low upfront CAPEX change classification?
- Is WeRa arranging credit if it organises financing?
- Does customer-title or project-SPV-title make credit classification better or worse than WeRa-title?
- Do installer-channel referrals trigger credit-intermediation or point-of-sale finance issues?
- What disclosures / licences are required?
- Does true lease reduce or increase risk?
- If a pilot-style client-funded CapEX + future WeRa buy-back path is ever reused, does the buy-back step trigger consumer-credit / lease / securities qualification?

Draft memo:

- `Strategy/Legal/miguel-track-b2-consumer-credit-memo.md`

### 18.3 Corporate / securities / tax memo

Core questions:

- What is the minimum first legal structure?
- Is PT CIC real and proportionate?
- Is NL STAK -> PT CIC advisable at start?
- How should project SPVs be used?
- Can customers later participate economically without securities issues?
- What tax/VAT treatment applies to service fee, lease alternative, excess generation and digital add-ons?
- Which external authority, if any, should be approached on each corporate/fund/tax point?

Draft memo:

- `Strategy/Legal/miguel-track-b3-corporate-structure-memo.md`

### 18.4 Retrospective pilot qualification memo

Core question:

- What is the legal status of the executed Torres Vedras arrangement and what written carrier should be signed now?

Draft memo:

- `Strategy/Legal/miguel-track-a-torres-vedras-memo.md`

## 19. Immediate Gaps Before External Submission

Before sending anything to any authority-specific regulator route, obtain or prepare:

1. Counsel-reviewed role map.
2. Draft customer contract summary.
3. Draft billing logic.
4. Draft asset-title / ownership logic.
5. Draft default and de-installation logic.
6. Insurance / liability allocation.
7. Torres Vedras external-grade evidence pack.
8. Consumer-credit preliminary view.
9. Supply-management hypothesis answer.
10. Regulatory routing and power-tier matrix.

Before sending anything to investor, additionally prepare:

1. Base case without WiFi Map dependency.
2. Edge-only BOM recut.
3. Discount underwriting model for any `20%` claim.
4. Lean operating budget.
5. CAPEX funding path for first 10 installs.

## 20. Working Conclusion

The current legally safest description is:

> WeRa is a solar self-consumption service/operator company, not an electricity retailer, not an installer and not a compute business in its first operating object. The selected baseline is a fixed-service-fee wrapper around customer or project-SPV titled solar assets, delivered by installer partners and monitored through an edge telemetry layer. Several attractive founder hypotheses exist - supply-management proxy, stronger 20% discount policy, add-on services, STAK/CIC architecture and customer-investor mechanisms - but these are alternatives or later layers, not the current legal baseline.

The next step is not to finalise the legal structure, but to obtain counsel feedback on the selected baseline and the main requalification risks.

## 21. Read Together With

- `Strategy/Business-Model/current-business-model.md`
- `Strategy/Business-Model/UTS.md`
- `Strategy/Business-Model/starter-drr.md`
- `Strategy/Business-Model/claim-register.md`
- `Strategy/Business-Model/executed-vs-designed.md`
- `Strategy/Business-Model/capital-architecture.md`
- `Strategy/Business-Model/open-gates.md`
- `Strategy/Business-Model/torres-vedras-pilot-questionnaire.md`
- `Strategy/Legal/regulatory-routing-and-power-tier-matrix.md`

formal_proof:
  engine: ml-hilbert
  trl_phase: TRL6
  obligation_id: kb.governance.annex_source_sync_strategy_legal_legal_operating_description_draft
  proof_artifact: kb-governance/formal-proofs/governance-annex-source-sync-strategy-legal-legal-operating-description-draft.lean
  verification_status: verified
