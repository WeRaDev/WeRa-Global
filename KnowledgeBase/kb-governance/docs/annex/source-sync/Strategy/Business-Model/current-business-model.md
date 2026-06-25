---
title: "WeRa — Полное системное описание текущей бизнес-модели"
date: "2026-04-22"
updated: "2026-04-24"
type: "business-model-description"
status: "working-draft-for-legal-structuring"
author: "Алексей + AI-сессия"
purpose: "Канонический документ для следующего шага: сборки юридической конструкции, разговора с юристом и предварительной верификации с relevant regulatory authorities, not one generic regulator."
layering_framework: "operating object / legal wrapper / monetization add-ons / long-term moat / investor story"
reality_discipline: "designed reality separated from executed reality"
based_on:
  - "2026-04-22-business-model-index.md"
  - "2026-04-22-strategic-synthesis-memo.md"
  - "2026-04-21-block0-object-discrimination-memo.md"
  - "2026-04-21-result-block6-specific-profile-demand.md"
  - "2026-04-21-result-block7-legal-hosting-wrapper-stress-test.md"
  - "2026-04-20-spain-legal-structure-wera.md"
  - "WeRa-Global-KB/02-Products.md"
  - "WeRa-Global-KB/03-Business-Model.md"
  - "WeRa-Global-KB/07-Customers-and-GTM.md"
  - "WeRa-Global-KB/13-Financial-Model.md"
  - "Meetings/2026-04-21-solar-hosting-model.md"
  - "Meetings/2026-04-22-solar-leasing-model.md"
  - "Strategy/Legal/regulatory-routing-and-power-tier-matrix.md"
---

## Consolidation provenance
- consolidation_actor: `WARP`
- consolidation_source: `/Users/mikhailananyin/Documents/WeRa Global/KB-latest-original/Strategy/Business-Model/current-business-model.md`
- consolidation_date: `2026-06-22`
- consolidation_status: `canonicalized`


# WeRa — Полное системное описание текущей бизнес-модели

> Этот документ описывает **не всю историческую и vision-архитектуру WeRa**, а **текущий рабочий operating business**, который можно:
> 1. положить на стол юристу;
> 2. проверить через relevant regulatory authorities после counsel-routing, а не через один общий запрос "регулятору";
> 3. использовать как каноническое описание того, что именно компания делает на первом шаге.

> Принцип документа: здесь явно разведены:
> - `baseline` — то, что входит в текущую рабочую модель;
> - `optional` — то, что можно добавлять поверх;
> - `far path` — то, что не должно подменять собой текущий объект;
> - `open legal hypothesis` — то, что требует отдельной верификации.

> Внутри документа каждая секция помечена по основному слою: `operating object`, `legal wrapper`, `monetization add-ons`, `long-term moat`, `investor story`. Если секция держит несколько слоёв сразу, это отмечено явно.

> Regulatory discipline update (`2026-04-24`): `regulator` is not one address. Energy/self-consumption questions route toward Portuguese energy counsel and then `DGEG` / `ERSE`; consumer-credit and intermediation questions route toward finance counsel and potentially `Banco de Portugal`; CIC/STAK/customer-participation questions route toward corporate/securities/tax counsel and potentially `CMVM`; telemetry/data questions may need privacy review. See `Strategy/Legal/regulatory-routing-and-power-tier-matrix.md`.

## 1. Каноническая формулировка объекта

> Слой: `operating object`

### 1.1 Что WeRa строит сейчас

WeRa на текущем этапе — это **third-party solar operator / service layer** поверх distributed solar self-consumption infrastructure.

Компания:
- не является установщиком;
- не является классическим retail-продавцом электроэнергии;
- не запускает сейчас самостоятельный GPU-hosting business;
- не строит сейчас compute marketplace.

`Selected baseline operating object`:

> **WeRa организует и управляет солнечной self-consumption installation как third-party operator. Клиент остаётся final consumer в соответствующем self-consumption режиме, основной solar asset в baseline-пути предпочтительно находится на титуле клиента или project SPV, а выручка WeRa описывается как fixed service fee за доступ, мониторинг, координацию и эксплуатационный контур, а не как retail sale of electricity или `€/kWh` billing.**

Это и есть базовая формула, вокруг которой дальше должна собираться юридическая конструкция.

Что важно:

- скрытая связка `владеет и/или управляет` больше не считается канонической формулой;
- `balance-sheet ownership` солнечного актива со стороны WeRa остаётся **живой альтернативой**, но не selected baseline;
                    - investor-facing shorthand может по-прежнему звучать как `solar leasing / service business`, но legal-baseline внутри документа теперь читается как **service-operator model first**;
- `client or project-SPV title + WeRa operator` — это **selected working baseline for testing**, а не доказанно "чистая" юридическая конструкция. Она может быть сильнее для energy-law separation, но при WeRa-funded или WeRa-arranged CAPEX может усилить consumer-credit / disguised-equipment-finance risk.

### 1.2 Что является первым sellable object

Первый коммерческий объект уже существует **в пилотной форме сейчас**. Горизонт `12-18` месяцев относится не к появлению объекта как такового, а к его **повторяемой, юридически чистой и внешне финансируемой версии**.

Этот объект:

- солнечная установка на объекте клиента;
- recurring service payment вместо upfront CAPEX в selected baseline;
- минимальный цифровой слой мониторинга и локального сбора данных;
- управление активом и клиентским контуром со стороны WeRa;
- монтаж и подключение через installer partner network.

Иначе говоря, first offer — это **solar leasing / energy-service business**, а не “облако для всех”, не “токенизированная экосистема” и не “дата-центр на солнце”.

### 1.3 Что бизнес обещает клиенту

На текущем этапе promise формулируется так:

- убрать или резко снизить upfront барьер на вход в solar;
- дать клиенту работающую установку с понятным monthly payment;
- дать клиенту локальную устойчивость и прозрачность по генерации/потреблению;
- не заставлять клиента менять свой обычный grid-supply relationship;
- при необходимости позже добавить поверх этого controlled digital services layer.

Важно: формула “минимум на `20%` дешевле текущего счета” встречается не только в legacy-материалах, но и в **живом GTM-описании** (`WeRa-Global-KB/07-Customers-and-GTM.md`, шаг `4` online funnel).

Статус этого тезиса:

- это **внешне выставленный claim**, а не внутренний артефакт истории;
- по состоянию на `2026-04-22` он **не считается подтверждённой частью канонического baseline promise**;
- до сегментной проверки и contract-level расчётов его нужно считать либо `suspended`, либо жёстко ограниченным до конкретных конфигураций.

Следовательно, claim нужно:

- либо отдельно подтвердить по сегментам и конфигурациям;
- либо ограничить до конкретных типов объектов;
- либо снять из customer-facing funnel.

## 2. Проблема, которую решает модель

> Слой: `operating object`

### 2.1 Проблема клиента

Для residential и small-business клиента проблема выглядит так:

- есть спрос на solar installation;
- есть желание снизить bills и повысить resilience;
- но нет готовности или возможности платить полный CAPEX upfront;
- дополнительно есть friction по выбору поставщика, оценке оборудования, установке и последующему управлению.

### 2.2 Проблема installer-side

Установщики умеют:
- монтировать;
- подключать;
- сертифицировать;
- закрывать техническую часть.

Но они не всегда закрывают:
- финансирование;
- recurring contract design;
- asset ownership layer;
- масштабируемую финансовую надстройку для клиентов, которым нужен лизинг.

### 2.3 Зачем нужен WeRa-layer

WeRa вставляется между installer и customer как слой, который:

- структурирует сделку;
- финансирует или организует финансирование актива;
- в selected baseline управляет активом и договорным контуром, а не автоматически держит asset title на собственном балансе;
- биллит клиента;
- ведёт цифровой мониторинг и client interface;
- в будущем может attach-ить дополнительный digital / cloud layer.

В этом смысле WeRa ближе к **asset-backed service/leasing operator**, чем к EPC-подрядчику или энергосбыту.

## 3. Границы модели

> Слой: `operating object`

### 3.1 Что входит в current baseline

`Baseline`

- solar installation as service-backed self-consumption asset;
- client as final consumer inside relevant self-consumption regime;
- WeRa as third-party operator / service-layer holder;
- primary revenue label = `fixed service fee`;
- installer network as delivery layer;
- solar asset title preferably at client or project `SPV` level in selected baseline;
- fixed recurring payment;
- edge device / Mini PC как обязательный элемент телеметрии и локального data layer;
- optional, но не обязательный digital monitoring interface для клиента.

### 3.2 Что optional, но допустимо как следующий слой

`Optional`

- дополнительные packs: storage, smart-house, security, appliances, EV-ready;
- managed local workspace / Nextcloud-like service для узких customer profiles;
- installer-network scaling path (`Frame IV`);
- отдельные `SPV` или ring-fenced structures для специальных активов или будущих портфелей;
- WeRa balance-sheet ownership of solar asset, если это позже подтвердится как лучший legal + capital path.

### 3.3 Что не должно входить в baseline-описание

`Not baseline`

- GPU datacenter thesis (`20 x H100`, `€2M+` CAPEX per unit);
- mini-PC marketplace revenue `€100-200/мес`;
- WeRa as electricity retailer / commercializadora;
- WeRa as installer of record;
- токеномика как operating revenue engine;
- старая three-entity structure как обязательная стартовая форма;
- WiFi Map как гарантированная revenue base Year 2;
- customer-to-shareholder conversion как уже собранная рабочая схема.

## 4. Продукт и актив

> Слой: `operating object`

### 4.1 Базовый физический актив: SolarSeed

В текущем корпусе SolarSeed описан как energy-first продукт с цифровым add-on слоем.

Ключевой смысл SolarSeed:
- локальная генерация;
- storage and dispatch;
- continuity of critical loads;
- наблюдаемость;
- возможность later attach digital services.

Это важно, потому что compute здесь **не должен определять legal nature** базового актива.

### 4.2 Две рабочие конфигурации

| Параметр | Base Config | Average Config |
|---|---:|---:|
| CAPEX | `€5,001.26` | `€22,979.69` |
| Energy subsystem | `€3,450.53` (`69%`) | `€20,529.96` (`89%`) |
| Compute / edge subsystem | `€1,550.73` (`31%`) | `€2,449.73` (`11%`) |
| Monthly payment (legacy lease-model figure) | `€70` | `€460` |
| Model duration (legacy lease-model figure) | `240` мес. (`20` лет) | `300` мес. (`25` лет) |
| Unit LTV | `€16,800` | `€138k-144k` |
| First payment | `€1` символический | `€1` символический |

Эти цифры остаются полезными как working economics current object.

### 4.3 Mini PC / edge device — обязательная часть baseline

На каждой установке должен быть локальный edge device / Mini PC.

Его функции:
- локальный сбор данных с инвертора;
- локальное хранение данных о генерации и потреблении;
- снижение зависимости от китайских vendor-clouds инверторов;
- предоставление клиенту базового digital interface;
- создание минимальной собственной цифровой основы актива.

Критически важно:

- этот элемент **входит в CAPEX baseline**;
- но его наличие **не превращает WeRa автоматически в compute marketplace business**;
- юридически и стратегически это инфраструктурный компонент, а не доказательство внешней compute-монетизации.

При этом текущая цифра `€1,550.73` (`31%` base-config CAPEX) для `compute / edge subsystem` выглядит завышенной, если читать её как цену “просто мониторингового Mini PC”.

Рабочее объяснение:

- это наследие старой BOM, где digital subsystem включал не только monitoring edge, но и более широкий compute/storage stack;
- внутри этой цифры смешаны Mini PC, router, external storage и более широкая логика цифрового слоя;
- для текущего baseline нужен **отдельный recut BOM**, который ответит на вопрос: сколько реально стоит минимальный обязательный edge-only слой для telemetry and local data.

До такого recut эту цифру лучше читать как **унаследованную модельную сборку**, а не как уже очищенную стоимость чистого monitoring baseline.

### 4.4 Что может стать поздним upsell

После стабилизации базового solar object возможны:

- extra battery;
- smart-house and relay packs;
- security systems;
- additional appliances under the same leasing logic;
- managed local workspace / data room;
- отдельные сервисы property/estate support через партнёров.

Но это нужно считать **расширением operating perimeter**, а не определением first business object.

## 5. Клиенты

> Слой: `operating object`

### 5.1 Основной клиент текущей модели

Primary solar customer на первом шаге задаётся **не типом юрлица как таковым, а набором характеристик объекта и сделки**.

`Selected first subset`:

- controllable roof/site with clear installation access;
- простая цепочка принятия решения;
- один понятный bill-payer и один понятный self-consumption contour;
- нет public procurement;
- нет сложной community governance;
- installer-side можно закрыть без захода в scarce large-project segment;
- размер установки и контур сделки остаются в зоне low-to-medium operational complexity.

Практические примеры такого subset:

- owner-managed household;
- small farm с одним decision-maker;
- local SME, где собственник и операционный контур совпадают.

Что не входит в first subset:

- сложные community / eco-village arrangements с множеством decision-makers;
- объекты с неоднозначным roof/title regime;
- случаи, где сразу включается тяжёлая public-interest procurement logic.

Устное уточнение от `2026-04-22`: разговор про пороги `~21-25 кВт` относится прежде всего к типу лицензии installer-side, а не к магическому освобождению самой модели WeRa от юридического анализа.

### 5.2 Вторичный клиент следующего слоя

Если digital/cloud layer запускается как отдельный узкий продукт, strongest fit сейчас обнаружен у:

- NGO;
- local associations;
- small public-interest entities;
- некоторых small teams, которым нужен local private workspace / archive / data room.

То есть у WeRa может появиться **второй тип клиента**, но:

- он не обязан совпадать с solar customer;
- его наличие не нужно для того, чтобы current baseline business был осмысленным;
- его юридический режим, скорее всего, должен быть либо accessory, либо отдельно структурирован.

### 5.3 Что не надо обещать рынку сейчас

Сейчас нельзя канонически описывать WeRa как:

- generic sovereign cloud provider;
- distributed compute marketplace;
- инфраструктуру для массовой монетизации mini-PC;
- enterprise GPU-hosting player.

Это создаёт ненужную путаницу между current product и vision layer.

## 6. Роли сторон и договорная логика

> Слой: `operating object` + `legal wrapper`

### 6.1 Клиент

Клиент:

- остаётся final consumer в соответствующем self-consumption режиме;
- остаётся holder of the consumption side;
- в cross-border prose ниже не нужно читать `autoconsumidor` как одинаковый PT/ES-термин;
- в PT-контексте нужно говорить языком `UPAC / autoconsumidor`;
- в ES-контексте нужно говорить языком `self-consumption under RD 244/2019 / ESE-compatible structure`;
- сохраняет свой supply relationship с commercializer/comercializadora;
- в selected baseline подписывает с WeRa service agreement;
- получает право на self-consumption от установки;
- платит recurring fixed service fee.

### 6.2 WeRa

WeRa:

- находит клиента;
- организует site assessment;
- заключает договор с клиентом;
- в selected baseline выступает как third-party operator / service-layer holder, а не как автоматически предполагаемый balance-sheet owner of the solar asset;
- финансирует или организует финансирование CAPEX;
- оплачивает монтаж и подключение installer partner;
- управляет billing, telemetry, customer interface и asset operations;
- позже может attach-ить optional digital services.

Важно:

- если в структуре появляется project `SPV`, WeRa может управлять операционным контуром, не держа сам solar asset на своём балансе;
- если solar asset title остаётся у клиента или project `SPV`, точная форма финансового вклада WeRa должна квалифицироваться отдельно: для physical person это близко к consumer-credit gate (см. `10.8`), для `SPV` требует явного описания инструмента в `capital-architecture.md`;
- WeRa-owned asset model остаётся допустимой альтернативой, но не считается выбранным baseline до отдельного legal + capital confirmation.

### 6.3 Installer / installation partner

Installer partner:

- делает обследование объекта;
- подбирает техническое решение;
- монтирует;
- подключает к сети;
- закрывает сертификацию и installer-side compliance;
- при необходимости выполняет maintenance field work.

Критическая граница:

- WeRa не должна описываться как entity, которая сама выполняет installation works и заменяет собой лицензированного подрядчика.

### 6.4 Grid supplier / commercializer

Обычный энергосбытовой контур клиента не исчезает.

Это важно и юридически, и для narrative:

- WeRa не заменяет supply contract с grid supplier;
- WeRa не становится классическим retail electricity seller только от того, что организует или контролирует onsite generation asset;
- customer relationship with grid остаётся частью модели.

### 6.5 Excess / excedente

**Статус:** `open legal hypothesis`

Продажа избытка может быть допустимой частью legal shell, но:

- сейчас это не должно быть центральным revenue promise;
- нужно отдельно определить, кто является продавцом избытка;
- нужен ясный ответ по договору с `CUR` / aggregator, налоговой и invoice-role.

До этой ясности excedente лучше считать **возможностью внутри конструкции, но не базовым описанием бизнеса**.

### 6.6 End-of-term ownership

**Статус:** `open legal hypothesis`

На текущем массиве материалов не зафиксирован канонически финальный режим конца договора:

- автоматический transfer;
- residual purchase option;
- продление service period;
- иной вариант.

Это нужно явно решить в legal/financial package, потому что это влияет на:

- consumer narrative;
- asset accounting;
- repossession/default logic;
- tax treatment.

### 6.7 Mid-term default

**Статус:** `open legal hypothesis`

Отдельный load-bearing вопрос модели — не только конец договора, но и **дефолт в середине срока**.

Если клиент перестаёт платить, возникают сразу четыре практических узла:

- имеет ли WeRa право и реальную возможность демонтировать актив с чужой крыши;
- насколько это операционно и экономически оправдано;
- как это влияет на pricing credit risk;
- как это воспринимается consumer law и потенциальными финансирующими сторонами.

Этот вопрос нельзя считать второстепенным. Для capital-intensive recurring-payment model он влияет и на legal design, и на economics, и на bankability.

### 6.8 Insurance, liability, and asset risk

**Статус:** `open legal hypothesis`

Так как solar equipment остаётся на чужом объекте `20-25` лет и WeRa может нести ownership risk, control risk или оба сразу, в модели обязательно должны быть отдельно собраны:

- страхование самого актива;
- ответственность за пожар, повреждение кровли, ущерб третьим лицам;
- распределение рисков между клиентом, WeRa, installer partner и insurer;
- treatment of force majeure, storm, hail, fire, theft and vandalism;
- обязанности по maintenance, inspection and incident reporting.

На текущем массиве документов этот блок пока не собран как contract package и должен считаться open gating issue.

## 7. Операционный цикл сделки

> Слой: `operating object`

Ниже canonical operating flow для текущей модели.

1. Lead generation:
   - direct website / calculator / map;
   - referrals;
   - installer/association channels.
2. Предварительная квалификация клиента:
   - bill data;
   - site basics;
   - customer intent.
3. Предварительное предложение:
   - ориентировочная конфигурация;
   - recurring payment;
   - предварительная оценка выгоды и применимости.
4. Site assessment:
   - выполняется installer-side partner.
5. Техническое и финансовое финальное предложение.
6. Подписание договора(ов):
   - service agreement с клиентом в selected baseline;
   - installation / service contract с партнёром;
   - при необходимости вспомогательные акты и consents.
7. Installation and grid connection.
8. Commissioning:
   - ввод в эксплуатацию;
   - telemetry;
   - customer monitoring setup.
9. Ongoing operations:
   - monthly billing;
   - support;
   - asset oversight;
   - optional digital layer.

На текущем GTM-уровне известный pipeline выглядит так:

- `1` живой пилот в Torres Vedras;
- `1` клиент в стадии предложения;
- signed installer partner `Iberia Renew Engineering`;
- дополнительный живой след по installer from Sintra, который уже воспроизвёл “concierge without leasing”.

### 7.1 Torres Vedras — главный текущий validation point

На сегодня Torres Vedras — это самый конкретный факт всей модели.

Более жёсткая формулировка:

- это **единственный executed carrier operating object**;
- всё остальное в документе нужно читать как `designed reality`, если для него не указан отдельный executed carrier.

Что подтверждено:

- это реальный installed pilot;
- тип объекта: off-grid micro-farm / private property;
- масштаб: small household equivalent (`~2` people);
- пилот был собран основателем руками, что подтверждает operator-level familiarity with the full cycle.

После заполнения Torres Vedras questionnaire (`2026-04-23`) появилась working-version фактология, но большая часть пока имеет статус `MEMORY`, а не `FACT`:

- пилот корректнее классифицировать как `customer installation with incomplete commercial wrapper`;
- по founder-reported working version, path сместился от изначального monthly-rent intent к `client-funded CapEx`;
- по founder-reported working version, после funding WeRa Global обсуждался возможный buy-back оборудования и повторная продажа клиенту по monthly cost;
- Миша сообщает, что verbal agreement существует, но written agreement / signed memorialization пока не исполнен в evidence package;
- подтверждённого recurring-payment trail по объекту нет;
- по текущей working version, у клиента нет supplier contract, поэтому bill-vs-bill savings baseline отсутствует;
- Миша сообщает о maintenance marker: check после штормов `30 января`, без выявленных проблем; structured maintenance ledger ещё не собран.

Жёсткая граница evidence:

- Torres Vedras **не доказывает** grid-connected `UPAC` / ordinary self-consumption compliance;
- не доказывает customer-as-final-consumer treatment inside a normal grid-supply relationship;
- не доказывает enforceability of fixed service fee for repeatable contracts;
- не доказывает consumer-credit clean recurring-payment structure.

Поэтому Torres Vedras полезен как Track A / technical-operating carrier, но не как proof of Track B prospective legal baseline.

Что всё ещё **не зафиксировано auditably**:

- payment trail по компонентам, монтажу и логистике;
- written agreement / memorialization с named legal counterparty;
- ownership/control/removal memo: `who paid / who owns / who controls / who can de-install`;
- telemetry export + proxy-savings sheet на основе measured monthly generation;
- site-verified as-built inventory с фото/серийниками;
- liability / insurance allocation for this specific installation.

Именно поэтому Torres Vedras одновременно является:

- strongest current validation point;
- и самым важным incomplete evidence block в каноническом описании.

Пока этот пакет не собран, Torres Vedras доказывает прежде всего:

- technical/operator familiarity with deployment cycle;
- способность собрать working installation;
- founder-reported evidence того, что один клиент был готов участвовать экономически через upfront CapEx path;
- наличие реального объекта.

Но он **ещё не доказывает** повторяемый, externally financeable и contract-clean commercial baseline.

## 8. Финансирование CAPEX и экономика модели

> Слой: `operating object` + `investor story`

### 8.1 Почему CAPEX financing — центральный слой модели

Это капиталоёмкий бизнес.

На каждой сделке должен быть закрыт `€5k-23k`+ upfront CAPEX на юнит до того, как начнут поступать долгие recurring payments. WeRa может финансировать этот CAPEX, организовывать object-level finance или работать через client/project-`SPV` funded path, но источник денег на актив всё равно является **центральной частью operating model**.

Без explicit funding path solar-leasing story остаётся неполной.

### 8.2 Текущие working hypotheses по CAPEX funding

На текущем массиве материалов видно не одну, а несколько гипотез финансирования. Они не сведены в один canonical path, но достаточно ясно читаются как staged architecture:

`Proof stage / первые установки`

- founder capital / friends & family / bridge equity;
- SAFE / convertible-like early funding;
- object-level financing под конкретные установки;
- в отдельных формулировках — supplier-side loan/leasing conditions на оборудование.

`Early growth / десятки установок`

- vendor financing;
- crowdlending / crowdfunding;
- working-capital and green-loan facilities;
- family-office / liquidity-provider relationships.

`Portfolio stage / сотни установок`

- portfolio debt facility под service/lease receivables, depending on the counsel-confirmed contract package;
- отдельные `SPV`;
- later securitization / institutional debt.

Рабочий вывод по состоянию на сейчас:

- **equity / bridge capital** нужно для proof stage;
- **capital recycling through debt** — это логика scale phase, а не day-1 reality;
- но точный canonical route пока не выбран и должен быть отдельно собран.

Полезный опорный research для этого: `research/2026-04-13-block3-financing-models-solar-leasing-scale.md`.

### 8.3 Что является load-bearing economics

Для текущего operating object load-bearing numbers — это прежде всего unit economics solar asset:

- CAPEX per unit;
- monthly recurring payment / service fee;
- срок договора;
- структура затрат между energy subsystem и edge subsystem;
- стоимость привлечения и servicing клиента;
- burn и runway до первых повторяемых контрактов;
- стоимость капитала и режим финансирования CAPEX;
- default behaviour and recoverability of assets.

### 8.4 Текущие рабочие цифры

Подтверждённые или используемые в current working model:

- current burn: `€2,000/мес` (`pre-registration`);
- post-registration OpEx first quarter: около `€263k`;
- Year 1 target из текущей финмодели: `100` юнитов и `€170,954` выручки;
- базовый two-year model требует около `€2.86M`, но её investor/story layer содержит спорные допущения.

При этом важно:

- `€263k/квартал` — это **scaled operating model from KB**, основанный на плановой команде `16` человек;
- это не надо читать как first-mover / day-1 budget;
- для раннего пакета решений нужна отдельная lean operating budget версия.

### 8.5 Как правильно читать существующую финмодель

Существующая financial model полезна, но её нужно читать с жёстким разделением:

`Reliable enough for current baseline`

- solar unit economics;
- CAPEX/OpEx contours;
- burn and setup logic;
- rough deployment logic.

`Not safe as baseline without scenario adjustment`

- cloud dominance as main source of Year 2 value;
- WiFi Map as critical conversion engine;
- large jump from `16k` to `376k` users in `Q3 Y2`;
- fundraising timing and valuation ladder as already-clean canonical path.

### 8.6 Gap между unit economics и corporate burn

Для базовой конфигурации `KB/13` даёт ориентир порядка `€9.13` monthly profit per unit на старте.

Это означает:

- даже `100` base-config юнитов дают только около `€913/мес` asset-level profit;
- это не покрывает даже текущий incubation burn `€2,000/мес`;
- и тем более не покрывает scaled OpEx из `16`-person model.

Это не делает модель автоматически плохой, но задаёт правильную логику чтения:

- **solar leasing unit economics** на раннем этапе доказывают прежде всего, что asset может быть положительным и financeable;
- они **не доказывают**, что corporate P&L становится самоподдерживающимся в `Y1-Y2`;
- gap закрывается либо за счёт fundraising, либо за счёт later attach-revenues, либо за счёт более дешёвого capital stack and leaner operating model.

Это ещё одна причина, почему формулу `minimum 20% savings guaranteed` нельзя держать как безусловный baseline promise без сегментной верификации.

Следовательно, baseline proof of business здесь — это **unit economics + contract quality + capital path**, а не мгновенная корпоративная прибыльность.

### 8.7 WiFi Map dependency

В текущей двухлетней модели:

- `66%` Year 2 revenue зависит от WiFi Map;
- подписанного коммерческого документа на сегодня нет;
- поэтому эта часть модели не должна использоваться как baseline proof of business viability.

Правильный статус:

- это не “ложь” и не обязательно “ошибка”;
- это **scenario**, а не canonical base case.

## 9. Go-to-market и масштабирование

> Слой: `operating object` + `investor story`

### 9.1 Direct path

Direct GTM path:

- map / calculator;
- inbound lead;
- proposal;
- site assessment;
- contract close;
- installation;
- onboarding.

Важно, что текущий digital funnel уже содержит customer-facing обещание `minimum 20% savings guaranteed`. Это значит, что GTM, finance model и legal positioning здесь должны быть выровнены: сайт не должен обещать то, чего базовая модель не умеет защищать по сегментам и по contract logic.

До закрытия claim-status правильное internal reading такое:

- это не часть canonical baseline promise;
- это externally visible claim, который должен либо получить evidence package, либо быть ограничен, либо быть снят.

### 9.2 Installer-network path (`Frame IV`)

Наиболее интересный scaling path сейчас — не отдельный новый бизнес, а **channel expansion** того же Phase 1 object через installer network.

Логика:

- installer уже находит и квалифицирует клиента;
- у части клиентов нет или недостаточно upfront CAPEX;
- WeRa добавляет поверх этого financing / leasing layer;
- installer получает больше закрытых сделок;
- WeRa получает distribution without becoming installer.

Это один из самых чистых путей роста current model.

### 9.3 Что подтверждает этот путь

Подтверждающие сигналы:

- подписанный партнёр `Iberia Renew Engineering`;
- живая линия через installer из Sintra;
- устное подтверждение, что leasing demand существует и в installer-side conversations;
- рыночная логика: small installers многочисленнее, ближе к residential/SME-сегменту и менее перегреты, чем large licensed players.

## 10. Юридическая обёртка current model

> Слой: `legal wrapper`

### 10.1 Базовая юридическая логика и критерии выбора

Юридическая опора current model строится не на грубом тезисе:

- “мы вообще не в энергии, мы просто хостим устройства”

а на более узкой и более правдоподобной формуле:

- клиент остаётся final consumer в локальном self-consumption режиме;
- onsite generation относится к его self-consumption;
- WeRa действует как third-party operator / service-layer holder;
- primary revenue label в baseline = `fixed service fee`;
- grid supply relationship остаётся у клиента;
- схема не превращается по существу в disguised retail electricity sale.

Критерии, по которым ниже ранжируются варианты:

1. legal defensibility inside self-consumption logic;
2. consumer-credit / disguised-financing exposure;
3. contractual and accounting clarity;
4. operational simplicity for first installs;
5. capital-path clarity and later bankability;
6. separability from optional compute and digital add-ons.

### 10.1A Regulatory routing rule

Не существует одного адресата `the regulator`.

Для текущего пакета вопросы должны маршрутизироваться отдельно:

- `DGEG` / `ERSE` path — PT energy, UPAC, self-consumption, supplier-requalification, excess generation, network-use and technical/installer questions;
- `Banco de Portugal` path — consumer-credit, credit intermediation, financed equipment, third-party finance and point-of-sale financing risk;
- `CMVM` path — PT `CIC`, collective investment, securities, customer participation, tokens or revenue rights;
- tax authority / tax counsel path — VAT, invoices, stamp duty and tax treatment;
- privacy / CNPD path if needed — telemetry, household energy data and customer consent.

Regulator-facing summaries must be derived **after counsel** and must not blend these question families.

### 10.2 Solar-side варианты по юридической и операционной прочности

По тем же критериям solar-side варианты сейчас читаются так:

1. `Client-owned solar asset; WeRa as operator/service-layer holder; fixed service fee` — **selected baseline for testing / potentially clean for energy-law separation, not yet proven clean for consumer-credit**.
2. `Project SPV owns the asset; WeRa manages contract stack and operations; separate finance shell` — workable scaling variant, but it may add fund, securities, tax, collateral or consumer-credit questions.
3. `WeRa-owned solar asset on own balance sheet; client pays lease/service` — live but heavier alternative, not selected baseline.
4. `WeRa-owned solar asset + externally monetized compute inside the same undivided object` — fragile.

Практический вывод:

- hidden bundle `владеет и/или управляет` больше не используется как канонический shorthand;
- baseline сейчас строится вокруг `operator/service-layer model first`;
- selected title posture не нужно называть "clean" до B.1/B.2/B.3 feedback; корректный label = `selected working baseline for testing`;
- asset-on-WeRa balance-sheet остаётся живой опцией только при отдельном подтверждении legal cleanliness, capital path and default mechanics.

### 10.3 Португалия

**Статус:** `open legal hypothesis`

По состоянию на `2026-04-21` desk research даёт по Португалии вердикт:

- `conditional`, но не `not-viable`.

Сильная сторона PT-case:

- third-party operation/management of `UPAC` выглядит допустимой;
- customer can remain final consumer;
- self-consumption service model не запрещён автоматически.

Слабая сторона PT-case:

- конструкция держится только пока сделка по существу остаётся self-consumption + service;
- любая попытка сделать из неё фактическую kWh-sale scheme ослабляет правовую позицию;
- compute inside the same undivided legal object быстро ухудшает защитимость модели.

Критически важно:

- в PT-контексте термин `autoconsumidor` нужно использовать как локальный правовой термин;
- его нельзя автоматически переносить как pan-Iberian shorthand без local-counsel bridge.

### 10.4 Испания

**Статус:** `open legal hypothesis`

Испания по состоянию на `2026-04-21` выглядит юридически сильнее для operating object.

Из текущего research следует:

- `consumer` и `owner of generation asset` могут быть разными лицами;
- `ESE`-логика признана официально;
- private agreement similar to service / lease выглядит институционально понятным;
- Spain-case выглядит `conditional-to-solid`, если не смешивать туда лишний external compute business.

Практический вывод:

- если выбирать, где модель читается естественнее как operating object, Испания сейчас выглядит сильнее;
- если revenue near-term всё равно в Португалии, это не отменяет необходимости португальской legal validation и локального footprint;
- терминологически ES-case нельзя описывать просто повторением PT-термина `autoconsumidor`, как будто это одно и то же понятие.

### 10.5 Что ломает юридическую обёртку

Current wrapper ослабевает или ломается, если:

- цена фактически привязана к `€/kWh`;
- WeRa начинает выглядеть как supplier, а не service operator;
- customer contract и factual consumption logic расходятся;
- `lease`, `service fee` и `facility fee` используются как будто это взаимозаменяемые ярлыки;
- WeRa-owned compute продаётся наружу как отдельный рыночный объект внутри того же legal shell;
- один и тот же объект одновременно описывается как self-consumption structure и как third-party compute seller;
- модульное дробление мощности используется как чистый threshold-arbitrage without real independence.

Отдельное правило vocabulary:

- `fixed service fee` — current canonical label;
- `lease fee` — допустимый альтернативный label только для отдельно выбранной true-lease структуры;
- `facility fee` — risky alias, который не должен использоваться в canonical baseline до отдельного ответа finance/counsel.

### 10.6 Compute-варианты по юридической прочности

Текущий rank-order по тем же критериям из `10.1`:

1. `Client-owned server, WeRa as manager/operator` — strongest.
2. `Separate compute SPV with separated contract stack` — workable.
3. `Hybrid rev-share` — conditional and document-heavy.
4. `WeRa-owned compute sold externally from the same undivided legal object` — fragile.

Отсюда следует важный управленческий вывод:

- legal shell current solar business не должен зависеть от того, что WeRa немедленно монетизирует compute как внешний рынок;
- edge-only baseline должен оставаться accessory layer, а не justification for external compute business.

### 10.7 Лицензии

Текущее разведение лицензий:

`Installer-side license`

- относится к монтажу и подключению;
- устно обсуждавшиеся пороги `~21-25 кВт` **не должны использоваться как operational legal fact**;
- для PT routing публичные source markers нужно проверять через power-tier matrix: `<=700 W`, `>700 W` to `<=30 kW`, `>30 kW` to `<=1 MW`, `>1 MW`, plus whether installation is isolated/off-grid, grid-connected, collective or multi-module;
- влияет на тип installer partner и доступность подрядчиков;
- не заменяет собой анализ статуса WeRa.

`Energy sale license`

- WeRa не нужна на текущем baseline, пока компания не продаёт энергию на внешний рынок как supplier;
- может понадобиться только в другой модели, где экспорт и продажа энергии становятся отдельным revenue line.

Это место нужно закрыть письменно у counsel через `Strategy/Legal/regulatory-routing-and-power-tier-matrix.md`, потому что устное уточнение от Миши снимает часть путаницы, но не заменяет formal legal opinion.

### 10.8 Consumer credit / credit intermediation gate

**Статус:** `open legal hypothesis`

Отдельный регуляторный узел модели — не energy law, а риск того, что recurring-payment structure будет прочитана как потребительское кредитование или кредитное посредничество.

Это особенно важно там, где:

- клиент — физлицо;
- или microbusiness;
- и economic substance сделки выглядит как financing of equipment over time.

На практике это может оказаться **gate не после energy-law, а параллельно с ним**, потому что:

- одна и та же модель может быть допустима как self-consumption service shell;
- но при этом требовать отдельной квалификации по consumer-finance rules.

Следовательно, current model нужно проверять одновременно в двух плоскостях:

- energy/regulatory qualification;
- consumer credit / financial intermediation qualification.

## 11. Digital / compute слой

> Слой: `monetization add-ons`

### 11.1 Что подтверждено

Подтверждено следующее:

- edge device на установке нужен;
- generic mini-PC marketplace economics как near-term revenue engine не подтверждены;
- узкий спрос на managed local private workspace / data room в PT/ES есть;
- strongest fit — NGO / local association / small public-interest entity;
- рабочий ценовой proxy по substitute market — примерно `€29-169/мес` для small-team scenarios.

Источник ценового proxy: `research/2026-04-21-result-block6-specific-profile-demand.md`, на базе substitute pricing `ProfesionalHosting` и `Librebit`.

### 11.2 Как правильно типизировать этот слой

Near-term compute/digital layer надо описывать не как:

- “ядро бизнеса”;
- “доказательство, что мы на самом деле hosting company”;
- “основной revenue engine current model”.

А как:

- optional add-on;
- secondary wedge;
- later monetization layer on top of physical installed base;
- possibly separate legal/commercial object if it begins to matter economically.

### 11.3 Что закрыто как текущая гипотеза

Закрытые тезисы:

- `~€1000 mini-PC -> €100-200/мес` как надёжный baseline;
- solar + GPU как трансформирующий moat для обычного H100 hosting;
- enterprise GPU hosting как продолжение current pre-seed object без отдельного funding path.

### 11.4 Что остаётся живым, но только как far path

**Статус:** `far path`

Живым остаётся только дальний тезис:

- отдельный energy-first AI / compute infrastructure object может когда-нибудь быть построен;
- но это уже другой инвестор, другой CapEx, другой sales motion, другой legal and operational perimeter.

Он не должен быть частью базового one-pager current business.

## 12. Что именно НЕ является текущей моделью

> Слой: `boundary discipline across operating object / monetization add-ons / long-term moat / investor story`

Чтобы убрать повторяющееся смешение слоёв, зафиксируем прямо.

WeRa current model — это **не**:

- solar installer business;
- electricity retail supplier;
- generic cloud platform for mass market;
- decentralized compute marketplace;
- H100 datacenter thesis;
- token-governed network state story;
- гарантированная WiFi Map monetization machine;
- готовая customer-shareholder conversion structure;
- already-finalized Portuguese `CIC` architecture.

Все эти элементы относятся либо к `legacy`, либо к `optional`, либо к `phase 2+`, либо к `open legal/corporate hypothesis`.

## 13. Открытые вопросы для юридической “отвёртки”

> Слой: `legal wrapper`

Ниже список вопросов, без которых legal packaging останется расплывчатой.

### 13.1 Вопросы к energy lawyer / local counsel

1. Как должен выглядеть exact contract package в Португалии:
   - customer = final consumer;
   - WeRa = third-party operator / service-layer holder around `UPAC`;
   - solar asset title at client or project `SPV` level in selected baseline;
   - fixed service fee;
   - no disguised kWh sale.
2. Нужно ли в базовом договоре избегать любых pricing formulas, похожих на `€/kWh`?
3. Как правильно оформить:
   - roof/site access;
   - title to equipment;
   - maintenance obligations;
   - insurance;
   - default and repossession mechanics.
4. Кто и как legally handles excedentes?
5. Не попадает ли текущая recurring model под consumer credit / financing intermediation, особенно для individuals and microbusinesses, и если да — что это меняет в license and disclosure package?
6. Кто несёт liability за fire / roof damage / third-party damage / force majeure, и как это должно быть распределено в contract + insurance stack?
7. Как должен выглядеть lawful default workflow:
   - notice periods;
   - cure periods;
   - suspension rights;
   - repossession / de-installation;
   - limits from consumer protection law?
8. Какие документы и сведения нужны для возможного `DGEG` / `ERSE` route, чтобы не было requalification into supply activity?

### 13.2 Вопросы к corporate / securities / tax lawyer

1. Жива ли вообще португальская `CIC / Sociedade de Investimento Coletivo` гипотеза как будущая оболочка, или это legacy-memory, утратившая актуальность?
2. Если нужна modular / cell-like structure, что practical first step:
   - opco;
   - holdco;
   - project `SPV`;
   - later investment wrapper?
3. Можно ли и как безопасно строить `customer -> shareholder` conversion через payment history внутри selected baseline?
4. Какой налоговый режим у:
   - fixed service fee;
   - alternative lease-fee structure, если later selected;
   - potential excedente flows;
   - separate digital revenue layer;
   - future investor participation in asset pools?

### 13.3 Вопросы к relevant regulatory authorities

Перед внешним запросом нужно определить адресата. Ниже не один список для "регулятора", а routing map.

`DGEG / ERSE path`:

1. Видит ли energy/self-consumption authority принципиальное препятствие в модели, где:
   - клиент остаётся final consumer;
   - WeRa действует как third-party operator;
   - основной solar asset находится у клиента или project `SPV`;
   - клиент платит fixed service fee;
   - supply contract с grid supplier остаётся у клиента?
2. Какие документы energy authority хотел бы видеть для preliminary assessment:
   - single-line diagram;
   - contract summary;
   - billing logic;
   - role map of parties;
   - treatment of excedentes?
3. Как power / grid-status tier влияет на answer:
   - isolated/off-grid;
   - `>700 W` to `<=30 kW`;
   - `>30 kW` to `<=1 MW`;
   - multi-module same-site structure?

`Banco de Portugal path`:

4. В каких вариантах recurring payment / CAPEX financing / installer referral может стать consumer credit или credit intermediation?

`CMVM path`:

5. Является ли PT `CIC / Sociedade de Investimento Coletivo` применимой и пропорциональной будущей structure, или это legacy/far-path hypothesis?

`Privacy path`:

6. Если telemetry/energy-use data используется для savings calculation, какие consent, controller/processor and retention rules нужны?

Digital add-on question:

7. Если поверх later attach-ится server/workspace layer, в какой момент это перестаёт быть accessory и требует отдельного структурирования?

## 14. Рабочий вывод

> Слой: `operating object` + `legal wrapper` + `investor story`

На дату `2026-04-22` каноническое описание бизнеса должно звучать так:

> **WeRa строит resilience-driven solar service / leasing business для small controllable sites, действуя как third-party operator of distributed self-consumption assets, не являясь установщиком и не являясь retail electricity seller. В selected baseline основной solar asset не обязан сидеть на балансе WeRa; компания монетизируется через recurring fixed service fee, использует installer partner network для delivery и включает обязательный edge monitoring layer. Optional digital/cloud services возможны только как вторичный слой поверх физической и юридически чистой solar-базы.**

Из этого следуют три практических правила:

1. Для юриста и relevant regulatory authority в центр разговора нужно ставить **solar asset + service-operator wrapper**, а не hosting mythology.
2. Для инвестора и команды baseline нужно считать **без WiFi Map как гарантированного revenue keystone**.
3. Для внутренней стратегии cloud / compute нужно держать как **upside and optionality**, но не как то, что определяет legal identity first business object.
4. Для внешней legal/regulatory работы нужно использовать **routing by authority**, а не один общий запрос к "регулятору".

## 15. Следующий пакет действий

> Слой: `operating object` + `legal wrapper`

На базе этого документа следующий рабочий шаг должен быть таким:

1. Дособрать external-grade evidence pack по Torres Vedras:
   - подписанный written agreement или signed memorialization;
   - payment trail по CAPEX;
   - ownership/control/removal memo;
   - telemetry export + proxy-savings sheet;
   - structured maintenance ledger.
2. Вынести на counsel exact answer по three load-bearing узлам:
   - selected service-fee wrapper;
   - consumer-credit gate;
   - default / insurance / repossession package.
3. Прогнать selected baseline через `regulatory-routing-and-power-tier-matrix.md`:
   - authority routing;
   - power / grid-status tier;
   - Torres Vedras evidence boundary.
4. Пересобрать финансовую модель в base case без WiFi Map dependency.
5. Сделать recut BOM для edge-only baseline.
6. Либо подтвердить, либо ограничить, либо снять customer-facing promise про `20% savings`.
7. Только после этого проверять, нужен ли переход от selected operator model к balance-sheet ownership model for scale.

Только после этого текущую модель можно считать достаточно собранной для полноценного внешнего подтверждения.

formal_proof:
  engine: ml-hilbert
  trl_phase: TRL6
  obligation_id: kb.governance.annex_source_sync_strategy_business_model_current_business_model
  proof_artifact: kb-governance/formal-proofs/governance-annex-source-sync-strategy-business-model-current-business-model.lean
  verification_status: verified
