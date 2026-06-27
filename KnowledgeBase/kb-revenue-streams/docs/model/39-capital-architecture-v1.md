---
title: "WeRa — Capital Architecture"
date: "2026-04-22"
updated: "2026-04-24"
type: "working-capital-architecture"
status: "working-baseline"
purpose: "Собрать в одном месте CAPEX funding logic для current selected operating object."
---

## Consolidation provenance
- consolidation_actor: `WARP`
- consolidation_source: `/Users/mikhailananyin/Documents/WeRa Global/KB-latest-original/Strategy/Business-Model/capital-architecture.md`
- consolidation_date: `2026-06-22`
- consolidation_status: `canonicalized`


# WeRa — Capital Architecture

> Этот документ отвечает на вопрос: **кто и на каких основаниях финансирует CAPEX текущего solar object на каждой стадии, не пряча ownership и credit-risk решения за общими словами.**

## 1. Selected capital posture

Текущая selected capital posture выглядит так:

- canonical baseline **не предполагает**, что WeRa автоматически держит все solar assets на собственном балансе;
- client / project-SPV title is a **selected working posture for testing**, not a confirmed clean structure;
- proof stage опирается прежде всего на `bridge equity / convertible-like capital / object-level finance`;
- Torres Vedras содержит founder-reported working version отдельного bridge path: `client-funded CapEx` with possible future buy-back / monthly-cost conversion, но это не доказывает repeatable WeRa-funded recurring-service model;
- recurring revenue в baseline описывается как `fixed service fee`, а не как `€/kWh` billing;
- debt against portfolio — это не стартовая реальность, а scale-stage path;
- переход к heavier asset-on-WeRa model допустим только после того, как собраны legal, tax, default and recoverability answers.

Critical caution:

- if the customer holds title while WeRa funds or arranges the equipment economics, the structure may become more exposed to consumer-credit / disguised-equipment-finance analysis;
- if project SPVs hold assets, the structure may improve ring-fencing but add fund, securities, tax and collateral questions;
- therefore capital architecture must be read together with `Strategy/Legal/regulatory-routing-and-power-tier-matrix.md`, not as proof that the selected title posture is already clean.

## 2. Stage map

| Stage | Practical scale | Main capital sources | Expected asset-title posture | What is explicitly not assumed |
|---|---|---|---|---|
| `Proof stage` | `1-10` installs | founder capital, friends & family, bridge equity, convertible-like money, object-level finance | client or project `SPV` title is preferred in baseline | portfolio debt, securitization, institutional cost of capital |
| `Early growth` | `10-50` installs | vendor financing, crowdlending, working-capital / green-loan facilities, small family-office debt | mix of client-title and project-`SPV` structures | large receivables facility as if risk stack were already proven |
| `Portfolio stage` | `50-250+` installs | receivables-backed facilities, project `SPV` debt, warehouse-like lines | stronger use of project `SPV` and standardized contract pack | pretending debt is available without clean default and insurance package |
| `Institutional stage` | `250+` installs / pools | institutional debt, securitization-like structures, dedicated asset pools | portfolio entities with ring-fenced governance | using this stage as current fundraising shorthand |

## 3. Why day-1 debt is not the baseline assumption

Debt does not arrive just because the asset is physical. For WeRa, lenders will care about:

- exact contract nature of the recurring payment;
- who holds title to the equipment;
- what happens on default;
- whether repossession is real or mostly theoretical;
- who insures the asset and third-party liability;
- whether consumer-credit rules contaminate the structure;
- whether the selected title posture reduces or increases consumer-credit exposure compared with WeRa-title or SPV-title alternatives;
- whether there is executed data beyond a founder-built pilot.

Пока эти узлы не закрыты, honest capital story = `bridge capital first, structured debt later`.

## 4. What makes the model financeable

Чтобы модель вообще стала bankable, нужно не “больше цифр вообще”, а конкретно:

- Torres Vedras fact sheet as executed carrier;
- first repeatable contract package for selected service-fee baseline;
- explicit answer on consumer-credit qualification;
- default / cure / repossession logic that a lender can underwrite;
- insurance and liability allocation;
- edge-only BOM recut;
- base-case economics without WiFi Map dependency.

## 5. Current stage-by-stage reading

### 5.1 Proof stage

Best current reading:

- WeRa raises bridge capital to make first installs possible;
- where possible, object-level capital is attached to a specific deal;
- ownership is kept as light and structurally clean as possible;
- the goal of this stage is not leverage, but evidence.

Torres Vedras does not yet prove this capital posture as a repeatable financing pattern. Its founder-reported working version is closer to `client-funded CapEx + incomplete commercial wrapper + possible future buy-back`, which is useful directional evidence of possible customer economic participation but must be kept separate from the selected recurring-service baseline until a written carrier and payment trail are collected.

### 5.2 Early growth

Only after repeatable contracts appear does it make sense to pursue:

- vendor credit;
- crowdlending / green-loan lines;
- project `SPV` structures for small pools.

At this stage the capital question changes from “can we pay for the next unit?” to “can we recycle capital without breaking the wrapper?”

### 5.3 Portfolio stage

Portfolio debt becomes realistic only when WeRa can show:

- contract standardization;
- measurable payment behaviour;
- default and recovery assumptions;
- insurer-backed risk allocation;
- receivables quality.

## 6. What would justify switching to asset-on-WeRa ownership

The heavier `WeRa-owned asset on own balance sheet` path should be revisited only if one or more of the following becomes true:

- counsel confirms that true lease is cleaner than service wrapper for the chosen subset;
- tax/accounting treatment is materially better;
- lenders prefer WeRa title for collateral reasons;
- collection/default mechanics are strong enough to justify ownership risk.

Until then, `service-layer first` remains the cleaner working baseline.

## 7. Read together with

- `Strategy/Business-Model/current-business-model.md`
- `Strategy/Business-Model/starter-drr.md`
- `Strategy/Business-Model/open-gates.md`
- `Strategy/Business-Model/claim-register.md`
- `Strategy/Legal/regulatory-routing-and-power-tier-matrix.md`

formal_proof:
  engine: ml-hilbert
  trl_phase: TRL6
  obligation_id: kb.revenue_streams.model_39_capital_architecture_v1
  proof_artifact: kb-governance/formal-proofs/revenue-streams-model-39-capital-architecture-v1.lean
  verification_status: verified
