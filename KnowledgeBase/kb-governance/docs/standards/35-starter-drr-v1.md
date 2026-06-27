---
title: "WeRa — Starter DRR"
date: "2026-04-22"
updated: "2026-06-16"
type: "decision-rationale-register"
status: "working-baseline"
purpose: "Зафиксировать selected set текущей модели, критерии выбора и условия пересмотра."
---

## Consolidation provenance
- consolidation_actor: `WARP`
- consolidation_source: `/Users/mikhailananyin/Documents/WeRa Global/KB-latest-original/Strategy/Business-Model/starter-drr.md`
- consolidation_date: `2026-06-22`
- consolidation_status: `canonicalized`


# WeRa — Starter DRR

> `DRR` здесь читается как `Decision / Rationale / Revisit Register`. Его задача — не дать варианту незаметно стать “уже выбранной истиной” без причины и критерия.

## 1. Selection criteria

Все ключевые выборы ниже оцениваются по одним и тем же критериям:

1. legal defensibility inside self-consumption logic;
2. consumer-credit and disguised-financing exposure;
3. contractual and accounting clarity;
4. operational simplicity for first installs;
5. capital-path clarity and later bankability;
6. separability from optional compute and digital add-ons.

## 2. Selected set

| Decision area | Selected now | Why selected now | Live alternatives | Revisit trigger |
|---|---|---|---|---|
| Solar-side ownership mode | `Client or project SPV title + WeRa as operator/service-layer holder` | selected working baseline for testing; avoids hidden `owner/operator` bundle and may help energy-law separation | WeRa-balance-sheet ownership; hybrid sale-leaseback; project SPV with stronger finance role | if consumer-credit, tax, lender or counsel logic shows this title posture is not actually cleaner |
| Primary recurring revenue label | `fixed service fee` | clearest separation from `€/kWh` sale and from credit/facility vocabulary | `lease fee` for true-lease path; generic `monthly payment` as interim GTM language | if exact contract package is confirmed as true lease and tax/accounting treatment is cleaner that way |
| PT vs ES legal track | `PT as immediate operating reality; ES as stronger doctrinal reference and possible cleaner scale wrapper` | revenue reality and pilot are in PT, but ES currently reads stronger for selected object | PT-only doctrine; ES-first relocation of the whole baseline | after written counsel comparison on the same contract stack |
| Compute ownership | `client-owned edge baseline; WeRa as manager/operator` | strongest separability from solar wrapper and lowest legal contamination | separate compute SPV; hybrid rev-share; WeRa-owned external compute | if digital revenue starts to matter economically or external compute becomes a real product |
| First customer subset | `small controllable sites with simple decision chain and clear self-consumption contour` | reduces legal, operational and collection complexity in first contracts | broad residential mass market; complex communities; public-interest procurement-heavy objects | after 3-5 repeatable installs with measured contract performance |
| CAPEX path by stage | `proof-stage bridge equity / convertible-like funding + object-level finance first` | matches current maturity and avoids pretending portfolio debt already exists | vendor financing as primary; portfolio facility from day 1; full project SPV debt from first installs | once there is clean contract data, default logic and a small pool of receivables |
| Executed proof standard | `Torres Vedras is technical/executed carrier with founder-reported client-funded CapEx path, not yet full commercial proof` | keeps designed reality and executed reality separate; avoids treating founder-reported client-funded/incomplete-wrapper pilot as proof of selected recurring-service baseline | treating the pilot as already proving repeatable financed model; using client-funded CapEx + buy-back path as a separate transitional model | after external-grade evidence pack and first truly commercial recurring-payment install |
| Regulatory routing | `multi-authority routing, not one regulator` | energy, consumer-credit, securities/fund, tax and telemetry questions belong to different authorities and counsel tracks | one blended regulator memo; direct authority request before counsel | if counsel gives a different authority map or authority-specific submission path |
| Power / grid-status reading | `use power-tier matrix before legal/authority use` | oral `21-25 kW` threshold is not stable enough as an operating fact | treating one installer-side threshold as the whole legal answer | after Miguel confirms exact PT thresholds and installer / DGEG procedure by tier |
| DT consultancy operating-proof standard | `launch channel executed; business-line proof requires conversion + paid outcomes` | separates “post launched” from “repeatable paid service line” and protects planning discipline | treating bookings or engagement as proof of business viability | after 10+ completed sessions, paid conversion baseline, and 3 bounded case write-ups |
| AI-platform narrative language | `fact vs hypothesis split from evidence brief is mandatory` | prevents overclaiming intent/causality and protects investor/regulator credibility | strong rhetorical framing that outruns source quality | if new high-quality causal/intent evidence materially changes claim status |

## 3. What is intentionally not selected

- `WeRa owns and operates everything` as automatic baseline
- `lease / service / facility fee` as interchangeable wording
- `autoconsumidor` as single PT/ES concept
- one generic `regulator` address for all questions
- `21-25 kW` threshold as operational legal fact before counsel confirmation
- Torres Vedras as proof of grid-connected UPAC / final-consumer recurring-service baseline
- broad “households + farms + SMEs + associations” as first market definition
- `WeRa-owned compute monetized externally` as part of current object
- any customer-contract structure that requires consumer-credit licensing or equivalent regulator-facing finance licence as first baseline
- `platforms intentionally maximize token/time spend` as factual statement without high-quality intent evidence
- `engagement design causes enterprise KPI failure` as factual statement without causal-grade evidence

## 4. Working rule

Если появляется новый вариант:

1. добавить его в эту таблицу;
2. назвать критерий, по которому он лучше;
3. указать, что именно должен показать reality, чтобы выбранный baseline был пересмотрен.

## 5. Read together with

- `Strategy/Business-Model/current-business-model.md`
- `Strategy/Business-Model/UTS.md`
- `Strategy/Business-Model/executed-vs-designed.md`
- `Strategy/Legal/regulatory-routing-and-power-tier-matrix.md`

formal_proof:
  engine: ml-hilbert
  trl_phase: TRL6
  obligation_id: kb.governance.standards_35_starter_drr_v1
  proof_artifact: kb-governance/formal-proofs/governance-standards-35-starter-drr-v1.lean
  verification_status: verified
