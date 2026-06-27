---
title: "WeRa — UTS (Unified Term Sheet)"
date: "2026-04-22"
updated: "2026-06-16"
type: "uts"
status: "working-baseline"
purpose: "Стабилизировать рисковые термины вокруг текущей бизнес-модели и не давать текстам снова смешивать operating object, legal wrapper и investor story."
---

## Consolidation provenance
- consolidation_actor: `WARP`
- consolidation_source: `/Users/mikhailananyin/Documents/WeRa Global/KB-latest-original/Strategy/Business-Model/UTS.md`
- consolidation_date: `2026-06-22`
- consolidation_status: `canonicalized`


# WeRa — UTS (Unified Term Sheet)

> Это словарь для текущего канонического пакета. Если термин здесь помечен как `risky alias`, его нельзя использовать в legal, regulator-facing или investor-facing материалах как будто он нейтрален.

## 1. Object and reality terms

| Term | Selected meaning | Where to use | Risk / avoid |
|---|---|---|---|
| `operating object` | Первый продаваемый объект: solar self-consumption installation + operator/service wrapper + recurring payment | `current-business-model.md`, legal prep, GTM baseline | Не подменять `vision`, `cloud upside` или `governance` |
| `designed reality` | То, что собрано как модель, но ещё не подтверждено executed carrier | Strategy docs, DRR, claim register | Не описывать как уже доказанный market fact |
| `executed carrier` | Конкретный факт, объект или договор, который уже произошёл и несёт реальность модели; может быть carrier отдельного элемента модели или carrier всего operating object | `executed-vs-designed.md`, claim register | Не путать с hypothesis, live conversation или website copy |
| `SolarSeed` | Energy-first physical product family; solar asset с обязательным edge baseline | Product and strategy docs | Не использовать как shorthand для cloud business |
| `solar asset / installation` | Физическая солнечная установка на объекте клиента | Cross-functional prose | Не смешивать автоматически с `UPAC` без локального контекста |
| `UPAC` | PT-specific legal/technical category self-consumption installation | PT legal discussions | Не использовать как pan-Iberian term |
| `edge baseline` | Минимальный локальный telemetry/data layer на установке | Product, BOM, legal boundary docs | Не описывать как external compute business |

## 2. Party and role terms

| Term | Selected meaning | Where to use | Risk / avoid |
|---|---|---|---|
| `final consumer` | Cross-border bridge label: клиент остаётся потребляющей стороной в self-consumption structure | Canonical prose across PT/ES | Не выдавать за точный локальный правовой термин |
| `autoconsumidor` | PT-local legal term for self-consumption participant | PT-specific legal text only | Не переносить автоматически на ES |
| `ES self-consumption consumer` | Bridge label for Spanish side under RD 244/2019 / ESE-compatible reading | ES-specific legal text | Не заменять PT-термином `autoconsumidor` |
| `operator` | WeRa организует, мониторит, биллит и координирует эксплуатационный контур; `service-layer holder` в текущем пакете используется как допустимый синоним этого же baseline-role | Canonical baseline | Не подменять словом `owner` |
| `owner` | Лицо, на котором находится legal title to the asset | Capital architecture, counsel memo, tax/accounting docs | Не писать `owner/operator` как будто это одно и то же |
| `lessor` | Сторона true-lease конструкции, если такая модель отдельно выбрана | Only if true-lease path selected | Не использовать в selected baseline по инерции |
| `project SPV` | Отдельная проектная сущность для владения активом и/или финансирования портфеля | Capital architecture, scaling docs | Не описывать как обязательную стартовую форму |
| `installer partner` | Лицензированный монтажный / technical delivery partner | Operating docs, GTM, legal pack | Не подменять WeRa installation role |

## 3. Contract and revenue terms

| Term | Selected meaning | Where to use | Risk / avoid |
|---|---|---|---|
| `fixed service fee` | Канонический baseline label для recurring revenue WeRa | Current baseline, counsel questions, regulator summary | Не смешивать с `lease fee` и `facility fee` |
| `lease fee` | Альтернативный label только для отдельно выбранной true-lease структуры | Alternative structure docs | Не использовать как baseline synonym |
| `facility fee` | Рисковый label, близкий к financing / credit framing | Only if finance counsel explicitly requires it | По умолчанию избегать |
| `monthly payment` | Нейтральный operational label до выбора точной contract form | GTM and proposal scaffolding | Не заменяет точный legal label |
| `self-consumption` | Клиент потребляет onsite generation внутри локального regulatory frame | Cross-functional prose | Не подменять `retail energy sale` |
| `excedente` | Избыток generation beyond onsite consumption | Legal/tax discussions | Не делать частью baseline revenue promise |

## 4. Capital and evidence terms

| Term | Selected meaning | Where to use | Risk / avoid |
|---|---|---|---|
| `proof-stage capital` | Founder capital, bridge equity, convertible-like instruments, object-level finance for first installs | Capital architecture | Не описывать как portfolio debt |
| `object-level finance` | Финансирование под конкретную установку или небольшой набор установок | Proof-stage and early growth docs | Не путать с platform-level equity |
| `portfolio financing` | Debt/facility against a portfolio of receivables/assets | Scale-stage docs | Не переносить в day-1 narrative |
| `technical pilot` | Installed object that proves technical/operator capability | `executed-vs-designed.md`, pilot fact sheet | Не выдавать автоматически за commercial pilot |
| `commercial pilot` | Installed object with signed commercial terms, recurring payment and measured economics | Claims, investor and legal validation | Не использовать для Torres Vedras, пока не собран pilot pack |

## 4A. Regulatory routing terms

| Term | Selected meaning | Where to use | Risk / avoid |
|---|---|---|---|
| `relevant regulatory authority` | Конкретный адресат по типу вопроса: `DGEG` / `ERSE`, `Banco de Portugal`, `CMVM`, tax authority, privacy authority | Legal and regulator-facing prep | Не писать generic `the regulator` без routing |
| `power / grid-status tier` | Classification by isolated/off-grid, grid-connected, `>700 W`, `<=30 kW`, `>30 kW`, multi-module, collective | Legal prep, installer questions, proposals | Не использовать oral `21-25 kW` как operational legal fact |
| `selected working baseline for testing` | Выбранная текущая структура, которую нужно проверить у counsel | DRR, legal memos | Не называть `clean baseline` до counsel confirmation |
| `grid-connected baseline proof` | Evidence that the model works as UPAC / final-consumer / fixed-fee in ordinary supplier-contract context | Claims and investor/legal proof | Не использовать Torres Vedras как такой proof без нового carrier |

## 4B. Evidence-language terms (external narrative discipline)

| Term | Selected meaning | Where to use | Risk / avoid |
|---|---|---|---|
| `factual statement` | Утверждение, поддержанное достаточным carrier-уровнем evidence | Investor/public/legal-facing texts | Не подменять гипотезой без маркировки |
| `working hypothesis` | Логичное, но не полностью подтверждённое утверждение | Internal strategy, research requests, caveated external text | Не подавать как установленный факт |
| `intent claim` | Утверждение о намерении платформ/актора (design intent) | Только с явной пометкой hypothesis, если carrier слабый | Не использовать как factual statement без сильных независимых доказательств |
| `domain-scoped support` | Подтверждение действует в конкретных контекстах (например, advisory/social-judgment), а не универсально | Evidence briefs, GTM copy notes | Не обобщать на все use-cases |
| `enterprise-causality claim` | Утверждение о причинной связи между interaction pattern и KPI бизнеса | Только при высоком качестве причинных данных | Не использовать как факт при смешанной/слабой доказательной базе |

## 5. Working rule

Если в каком-то документе снова появляются конструкции типа:

- `owner/operator`
- `lease / service / facility fee`
- `autoconsumidor` как pan-Iberian term
- `regulator` as one address
- `21-25 kW` as a legal safe threshold
- `clean baseline` for the selected title posture
- `platforms are intentionally designed to maximize token/time spend` как установленный факт
- `engagement design causes enterprise KPI failure` как установленный факт
- domain-scoped evidence как universal proof

нужно сначала вернуться к этому файлу, а не продолжать писать “по памяти”.

## 6. Read together with

- `Strategy/Business-Model/current-business-model.md`
- `Strategy/Business-Model/starter-drr.md`
- `Strategy/Business-Model/claim-register.md`
- `Strategy/Legal/regulatory-routing-and-power-tier-matrix.md`

formal_proof:
  engine: ml-hilbert
  trl_phase: TRL6
  obligation_id: kb.governance.standards_34_unified_term_sheet_uts_v1
  proof_artifact: kb-governance/formal-proofs/governance-standards-34-unified-term-sheet-uts-v1.lean
  verification_status: verified
