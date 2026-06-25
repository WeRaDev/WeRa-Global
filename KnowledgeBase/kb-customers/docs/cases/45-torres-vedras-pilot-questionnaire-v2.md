---
title: "Torres Vedras — Pilot Questionnaire"
date: "2026-04-23"
type: "pilot-questionnaire"
status: "completed-v2-with-gaps"
purpose: "Полный опросник для Миши по пилоту Torres Vedras, чтобы собрать reality-grade fact sheet и отделить подтверждённые факты от устной реконструкции."
owner: "Миша"
related:
  - "Strategy/Business-Model/current-business-model.md"
  - "Strategy/Business-Model/executed-vs-designed.md"
  - "Strategy/Business-Model/claim-register.md"
---

## Consolidation provenance
- consolidation_actor: `WARP`
- consolidation_source: `/Users/mikhailananyin/Documents/WeRa Global/KB-latest-original/Strategy/Business-Model/torres-vedras-pilot-questionnaire.md`
- consolidation_date: `2026-06-22`
- consolidation_status: `canonicalized`


# Torres Vedras — Pilot Questionnaire

> Цель этой заметки: собрать **канонический факт-пакет** по Torres Vedras так, чтобы мы перестали ссылаться на пилот как на “что-то, что у нас в целом есть”, и могли точно сказать, что он **реально доказывает**, а что пока **не доказывает**.

> Пожалуйста, заполняй **не как эссе**, а как рабочий факт-лист. Если чего-то не знаешь или не можешь подтвердить, пиши прямо: `UNKNOWN`, `не помню`, `надо поднять документ`, `это была устная договорённость`, `это моя оценка`, `это не подтверждено`.

> Update `2026-04-24`: этот questionnaire не должен использоваться как proof будущей grid-connected `UPAC` / final-consumer / fixed-service-fee конструкции. Текущий пакет указывает на off-grid / no supplier-contract context, поэтому Torres Vedras несёт прежде всего Track A / technical-operating evidence.

## 0A. Filled snapshot v1 (from Misha, 2026-04-23)

> Ниже — первый заполненный проход по критическим пунктам (коммерческая форма пилота, CAPEX, платежи, maintenance, savings logic). Это **partial fill**, не финальный fact sheet.

### Q1. Статус пилота
- `MEMORY` На сегодня: **technical/executed proof, not full commercial proof**.
- `MEMORY` Более точный label: `customer installation with incomplete commercial wrapper`.

### Q2. Коммерческая схема по факту
- `MEMORY` Изначально клиент согласился на monthly rents.
- `MEMORY` Финально клиент согласился инвестировать CapEx с условием: после финансирования WeRa Global возможен buy-back оборудования и повторная продажа клиенту по monthly cost.
- `MEMORY` Между сторонами есть verbal agreement; written agreement может быть подписан в любой момент.

### Q3. CAPEX и ownership (текущая рабочая версия)
- `MEMORY` Для пилота фактически использован клиентский CapEx.
- `UNKNOWN` Полный подтверждённый payment trail по компонентам (инвойсы/чеки/выписки) ещё не приложен в пакет.

### Q4. Savings baseline
- `FACT/MEMORY` У клиента нет контракта с энергопоставщиком, поэтому bill-vs-bill baseline отсутствует.
- `FACT/MEMORY` Из-за отсутствия обычного supplier-contract baseline пилот не доказывает grid-connected `UPAC` / final-consumer wrapper.
- `ESTIMATE` Допустимый proxy-подход: средняя генерация в месяц × grid price, затем сравнение с equipment cost из `Strategy/Business-Model/solar.seed.components.csv`.
- `UNKNOWN` Формализованный monthly/annual proxy-расчёт в виде отдельного артефакта пока не приложен.

### Q5. Maintenance
- `MEMORY` `30 января` был maintenance check после штормов; всё работало корректно, проблем для исправления не выявлено.
- `MEMORY` Digital maintenance проводится еженедельно.
- `UNKNOWN` Единый maintenance log с датами/работами/стоимостью пока не собран.

### Q6. Gates linked to this snapshot
- `OPEN` Поднять и приложить payment trail и любые письменные договорённости/переписку по pilot deal.
- `OPEN` Приложить `Strategy/Business-Model/solar.seed.components.csv` как explicit evidence carrier.
- `OPEN` Engineering team: измерить average monthly generation и собрать telemetry-based proxy-savings sheet.
- `OPEN` Сформировать short maintenance ledger (минимум: дата, событие, действие, кто делал).

## 0. Правила заполнения

Перед ответами используй такие метки:

- `FACT` — подтверждено документом, платежом, фото, скрином, телеметрией, перепиской или иным носителем.
- `MEMORY` — это твоя память, но документ/носитель сейчас не приложен.
- `ESTIMATE` — это приблизительная оценка.
- `UNKNOWN` — данных сейчас нет.

Для каждого важного ответа желательно указывать:

- `Evidence carrier:` где это лежит сейчас или где это можно достать.
- `Confidence:` high / medium / low.

Если есть файл, скрин, договор, инвойс, фото, переписка, таблица, выписка, экспорт из инвертора или просто фото экрана — лучше указать это прямо, даже если файл ещё не переложен в проектную папку.

---

## 1. Базовая идентификация пилота

### 1.1 Как правильно называть этот объект

- Внутреннее имя объекта:
- Это `technical pilot`, `commercial pilot`, `founder-built demo`, `live customer installation` или что-то ещё?
- Какая формулировка наиболее точна на сегодня?
- Какая формулировка была бы **неточной или вводящей в заблуждение**?

Ответ:
- `FACT` Рабочее внутреннее имя: **technical pilot: SolarSeed.TRL5: ARS Sustineri**.
- `FACT` Для технического runtime-контекста также используется идентификатор `wera-ss-pt-tv-1` (через сводный pilot review).
- `FACT/MEMORY` Наиболее точная формулировка сейчас: `customer installation with incomplete commercial wrapper`.
- `FACT` Формулировка `full commercial baseline proven` на текущем evidence-пакете является завышением.

Evidence carrier:
- `Strategy/Business-Model/executed-vs-designed.md`
- `Strategy/Business-Model/claim-register.md`
- `Strategy/Business-Model/SolarSeed.pilot.tv.md`

Confidence:
- high

### 1.2 Локация и тип объекта

- Точный адрес или хотя бы максимально точное описание места:
- Тип объекта: дом / ферма / quinta / хозяйство / другое:
- Это off-grid, grid-tied или hybrid?
- Это основное место проживания, вторичный объект, хозяйственный объект или смешанный случай?

Ответ:
- `FACT` Локация: Torres Vedras, Portugal.
- `FACT` Тип: off-grid micro-farm / private property.
- `FACT/MEMORY` Масштаб: small household equivalent (`~2` people).
- `UNKNOWN` Точный адрес и кадастрово-юридическая идентификация site не зафиксированы в текущем пакете.
- `ESTIMATE` По режиму: off-grid reading является базовым, но formal technical/legal classification в отдельном carrier не приложена.

Evidence carrier:
- `WeRa-Global-KB/07-Customers-and-GTM.md`
- `WeRa-Global-KB/00-Glossary.md`
- `Strategy/Business-Model/current-business-model.md`

Confidence:
- medium

### 1.3 Временная хронология

Укажи, если возможно, с датами:

- когда возникла идея этого пилота;
- когда начался подбор оборудования;
- когда была закупка;
- когда был монтаж;
- когда объект начал реально работать;
- были ли потом апгрейды / замены / доработки.

Ответ:
- `MEMORY` Известный operational marker: `30 января` был maintenance check после штормов, система работала корректно.
- `FACT/MEMORY` Указание на технический snapshot вокруг `2026-04-07` присутствует в pilot review.
- `MEMORY` Дата возникновения идеи - Август 2024, дата закупки - Август 2025, дата монтажа и первого запуска - 21 декабря 2025.
- `UNKNOWN` Формальный журнал апгрейдов/замен по датам не собран.

Evidence carrier:
- `Strategy/Business-Model/torres-vedras-pilot-questionnaire.md` (section `0A`)
- `Strategy/Business-Model/SolarSeed.pilot.tv.md`
- `Strategy/Business-Model/executed-vs-designed.md`

Confidence:
- medium

---

## 2. Кто является стороной пилота

### 2.1 Кто пользователь / бенефициар объекта

- Кто фактически пользуется установкой?
- Это один человек, семья, хозяйство, юридическое лицо, несколько пользователей?
- Кто принимает решения по объекту?
- Кто оплачивает связанные расходы, если они есть?

Ответ:
- `MEMORY` Пользователь/бенефициар - молодая пара, посещающая этот объект несколько раз в месяц в качестве загородного дома для отдыха.
- `FACT/MEMORY` По профилю объекта: small household equivalent (`~2` people), off-grid micro-farm context.
- `MEMORY` По текущему описанию, клиент участвовал экономически через CapEx.
- `UNKNOWN` Формально подтверждённый payer-by-line (кто оплачивал какие работы/компоненты) не приложен.

Evidence carrier:
- `WeRa-Global-KB/07-Customers-and-GTM.md`
- `Strategy/Business-Model/executed-vs-designed.md`
- `Strategy/Business-Model/torres-vedras-pilot-questionnaire.md` (section `0A`)

Confidence:
- medium

### 2.2 Отношение этого пользователя к тебе и к WeRa

- Это сторонний клиент?
- Это знакомый / друг / родственник / аффилированный человек?
- Это объект Миши?
- Это объект, где ты сам контролируешь и site, и оборудование?
- Есть ли здесь конфликт между “пилот для проверки” и “реальный клиентский объект”?

Ответ:
- `FACT/MEMORY` В каноническом reading объект трактуется как клиентская установка, собранная основателем.
- `MEMORY` Бенефициар установки — очень близкий друг фаундера, заинтересованный в успехе проекта; по working version он делегировал фаундеру operational management/control, но это не подтверждает legal title, beneficial ownership или de-installation rights.
- `FACT` Конфликт интерпретации есть: объект одновременно real installation и неполный commercial wrapper.
- `FACT` Поэтому он учитывается как `technical/executed carrier`, но не как полный commercial proof.

Evidence carrier:
- `Strategy/Business-Model/executed-vs-designed.md`
- `Strategy/Business-Model/starter-drr.md`
- `Strategy/Business-Model/current-business-model.md`

Confidence:
- medium

### 2.3 Юридическая сторона

- Кто является собственником site / roof / property?
- Есть ли отдельный legal counterparty?
- Есть ли физлицо или юрлицо, с которым можно было бы подписывать договор по этому объекту?

Ответ:
- `MEMORY` Официальный собственник site/roof - Diogo Nascimento.
- `UNKNOWN` Именованный legal counterparty в текущих канонических docs не указан.
- `MEMORY` Зафиксировано, что письменное соглашение может быть подписано в любой момент.
- `OPEN` До закрытия факта необходимо привязать counterparty identity + письменный договор/мемо.

Evidence carrier:
- `Strategy/Business-Model/torres-vedras-pilot-questionnaire.md` (section `0A`)
- `Strategy/Business-Model/claim-register.md`
- `Strategy/Business-Model/open-gates.md`

Confidence:
- medium

---

## 3. Что именно установлено

### 3.1 Состав системы

Перечисли всё, что реально установлено:

- солнечные панели: количество, модель, мощность;
- инвертор(ы): модель, мощность;
- батарея / storage: модель, ёмкость;
- контроллеры / BMS / автоматика;
- mini PC / edge device;
- роутер / модем / connectivity;
- крепёж / конструкции;
- счётчики / датчики / телеметрия;
- прочее критичное оборудование.

Ответ:
- `FACT` Reference BOM (как baseline, не как полностью site-verified as-built): 6x panels 505W, Voltronic 3kW inverter, 2x TAB 12V 250Ah batteries, misc kit, installation, GEEKOM mini PC, 5G router, external SSD.
- `FACT/MEMORY` Для пилота зафиксирован telemetry/runtime контур (через сводный technical review).
- `UNKNOWN` As-built инвентаризация с серийниками, датами установки и фотофиксацией по компонентам не собрана как единый carrier.

Evidence carrier:
- `Strategy/Business-Model/solar.seed.components.csv`
- `Technical Description.SolarSeed.BaseConfiguration.md`
- `Strategy/Business-Model/SolarSeed.pilot.tv.md`

Confidence:
- medium

### 3.2 Текущая конфигурация vs исходная конфигурация

- Что из перечисленного было в исходной сборке?
- Что было добавлено позже?
- Что менялось, ломалось, снималось, заменялось?

Ответ:
- `UNKNOWN` В текущем пакете нет validated change-log по железу/конфигурации.
- `FACT` Есть только baseline reference конфигурация и отдельные runtime-наблюдения из technical review.
- `OPEN` Нужен краткий as-built vs baseline diff (что реально стоит сейчас, что было заменено/добавлено).

Evidence carrier:
- `Strategy/Business-Model/SolarSeed.pilot.tv.md`
- `Strategy/Business-Model/solar.seed.components.csv`

Confidence:
- high

### 3.3 Технический статус сейчас

- Объект сейчас работает?
- Если да, в каком режиме?
- Если нет, почему?
- Какие части системы реально активны, а какие формально стоят, но не используются?

Ответ:
- `MEMORY` По состоянию на maintenance check `30 января` система работала корректно, проблем для исправления не выявлено.
- `MEMORY` Digital maintenance выполняется еженедельно.
- `FACT/MEMORY` Есть признаки live runtime/telemetry слоя из собранного pilot review.
- `UNKNOWN` Актуальный на сегодня online/offline статус всех сервисов и контуров без свежего telemetry export не подтверждён.

Evidence carrier:
- `Strategy/Business-Model/torres-vedras-pilot-questionnaire.md` (section `0A`)
- `Strategy/Business-Model/executed-vs-designed.md`
- `Strategy/Business-Model/SolarSeed.pilot.tv.md`

Confidence:
- medium

---

## 4. CAPEX и источник денег

### 4.1 Кто реально оплатил объект

Это один из главных блоков. Нужен не общий рассказ, а разбор по факту.

По возможности распиши:

- кто оплатил панели;
- кто оплатил батарею;
- кто оплатил инвертор;
- кто оплатил mini PC / edge;
- кто оплатил монтаж;
- кто оплатил доставку / логистику / дополнительные работы;
- были ли donated / discounted / second-hand компоненты;
- были ли неформальные взаимозачёты.

Ответ:
- `MEMORY` По рабочей версии пилот был профинансирован клиентским CapEx.
- `UNKNOWN` Разбивка по линиям оплаты (панели/инвертор/батареи/edge/монтаж/логистика) пока не собрана.
- `UNKNOWN` Наличие скидок, донатов, second-hand или взаимозачётов документально не подтверждено.

Evidence carrier:
- `Strategy/Business-Model/torres-vedras-pilot-questionnaire.md` (section `0A`)
- `Strategy/Business-Model/executed-vs-designed.md`
- `Strategy/Business-Model/claim-register.md`

Confidence:
- medium

### 4.2 Общая оценка CAPEX

- Какой был total CAPEX?
- Это точная сумма, приблизительная или реконструкция по памяти?
- Есть ли инвойсы / чеки / выписки / Excel / фото счетов?

Ответ:
- `FACT` Есть reference baseline CAPEX по BOM: `€5,001.26`.
- `UNKNOWN` Фактический total CAPEX конкретно по Torres Vedras не подтверждён платежными носителями.
- `UNKNOWN` Инвойсы/чеки/выписки в канонический пакет пока не приложены.

Evidence carrier:
- `Strategy/Business-Model/solar.seed.components.csv`
- `Technical Description.SolarSeed.BaseConfiguration.md`
- `Strategy/Business-Model/SolarSeed.pilot.tv.md`

Confidence:
- high

### 4.3 Как это финансировалось по сути

- Это были твои личные деньги?
- Деньги пользователя?
- Деньги WeRa / пред-WeRa структуры?
- Заём?
- Партнёрская поставка?
- Грант / subsidy / special price?
- Это был тестовый объект, где часть стоимости вообще не считалась?

Ответ:
- `MEMORY` Изначальный intent был monthly rent, но фактическая развилка в пилоте: клиентское CapEx финансирование.
- `MEMORY` Зафиксирован условный будущий path: после funding WeRa Global возможен buy-back и переход к monthly cost logic.
- `UNKNOWN` Отдельные внешние источники финансирования (loan/subsidy/vendor credit) для данного объекта не подтверждены документами.

Evidence carrier:
- `Strategy/Business-Model/torres-vedras-pilot-questionnaire.md` (section `0A`)
- `Strategy/Business-Model/executed-vs-designed.md`
- `Strategy/Business-Model/claim-register.md`

Confidence:
- medium

### 4.4 Ownership after purchase

После покупки:

- кто стал собственником оборудования по факту;
- кто считал себя собственником;
- кто мог распоряжаться оборудованием;
- кто мог его снять / продать / перевезти;
- есть ли расхождение между “кто заплатил” и “кто владел”.

Ответ:
- `MEMORY/ESTIMATE` Если клиент финансировал CapEx, текущая working version указывает на founder-side operational control/management, но не на подтверждённый legal title.
- `MEMORY` Условие buy-back указывает, что ownership/title path нужно отдельно завалидировать, а не выводить из устной договорённости.
- `UNKNOWN` Юридически оформленное распределение title/control/removal rights в письменном виде отсутствует.
- `OPEN` Нужен explicit ownership memo: who paid / who owns / who controls / who can de-install.

Evidence carrier:
- `Strategy/Business-Model/torres-vedras-pilot-questionnaire.md` (section `0A`)
- `Strategy/Business-Model/current-business-model.md`
- `Strategy/Business-Model/open-gates.md`

Confidence:
- medium

---

## 5. Договорная и юридическая реальность

### 5.1 Был ли договор

- Был ли письменный договор вообще?
- Если да, между кем и кем?
- Как он назывался по смыслу: lease, service, loan, installation agreement, informal permission, nothing written?
- Сохранился ли файл / скан / переписка?

Ответ:
- `MEMORY` На сегодня есть verbal agreement; письменный договор ещё не исполнен, но может быть подписан в любой момент.
- `FACT` В claim layer зафиксировано: written agreement not yet executed.
- `UNKNOWN` Название и точный юридический тип текущей договорённости (lease/service/loan/other) в оформленном документе отсутствуют.

Evidence carrier:
- `Strategy/Business-Model/torres-vedras-pilot-questionnaire.md` (section `0A`)
- `Strategy/Business-Model/claim-register.md`
- `Strategy/Business-Model/executed-vs-designed.md`

Confidence:
- high

### 5.2 Если договора не было

Если письменного договора не было, опиши честно:

- какая была реальная устная договорённость;
- что каждая сторона считала происходящим;
- было ли это “поставили для теста”;
- было ли это “ставим как клиентскую систему”;
- был ли разговор про платежи, ownership, срок, обслуживание.

Ответ:
- `MEMORY` Реальная устная конструкция: изначально monthly rents как intent, затем клиентский CapEx с условным будущим buy-back path при funding WeRa.
- `MEMORY` По факту это ближе к `customer installation with incomplete commercial wrapper`, а не к fully structured lease case.
- `MEMORY` Разговоры про ownership/payment были, но письменная фиксация не приложена.
- `UNKNOWN` Детальные terms (срок, default, penalties, liability) в документе не подтверждены.

Evidence carrier:
- `Strategy/Business-Model/torres-vedras-pilot-questionnaire.md` (section `0A`)
- `Strategy/Business-Model/executed-vs-designed.md`
- `Strategy/Business-Model/current-business-model.md`

Confidence:
- medium

### 5.3 Право доступа к site

- На каком основании оборудование стоит на этом объекте?
- Есть ли permission на roof/site?
- Есть ли право демонтировать оборудование?
- Кто решает, можно ли что-то менять?

Ответ:
- `FACT/MEMORY` Де-факто доступ и размещение были предоставлены (иначе объект не был бы установлен).
- `UNKNOWN` Формальный документ о site/roof permission в текущем пакете отсутствует.
- `UNKNOWN` Письменные de-installation/change rights не зафиксированы.

Evidence carrier:
- `Strategy/Business-Model/executed-vs-designed.md`
- `Strategy/Business-Model/current-business-model.md` (open legal nodes)
- `Strategy/Business-Model/open-gates.md`

Confidence:
- low-medium

### 5.4 Обслуживание и ответственность

- Кто отвечает за maintenance?
- Кто чинит при поломке?
- Кто оплачивает replacement parts?
- Был ли разговор о liability за пожар / roof damage / property damage?
- Есть ли страховка хоть в каком-то виде?

Ответ:
- `MEMORY` Field maintenance: check после штормов (`30 января`), без выявленных неисправностей.
- `MEMORY` Digital maintenance: еженедельно.
- `UNKNOWN` Формальное распределение maintenance ownership/expenses в договоре пока не закреплено.
- `UNKNOWN` Liability/insurance stack по объекту в package не подтверждён.

Evidence carrier:
- `Strategy/Business-Model/torres-vedras-pilot-questionnaire.md` (section `0A`)
- `Strategy/Business-Model/executed-vs-designed.md`
- `Strategy/Business-Model/current-business-model.md` (sections on insurance/liability as open gate)

Confidence:
- medium

---

## 6. Коммерческая реальность: были ли деньги и платежи

### 6.1 Был ли это платящий объект

- Платил ли пользователь что-то upfront?
- Платит ли он что-то recurring?
- Была ли символическая оплата (`€1` или иная)?
- Были ли cash payments, перевод, invoice, просто обещание?

Ответ:
- `MEMORY` Клиент профинансировал CapEx.
- `UNKNOWN` Подтверждённый payment trail в пакете ещё не приложен.
- `FACT` Повторяющийся recurring-payment кейс по объекту документально не зафиксирован.
- `FACT` Символический `€1` встречается как продуктовая/маркетинговая рамка, но не как подтверждённый pilot-specific payment carrier.

Evidence carrier:
- `Strategy/Business-Model/torres-vedras-pilot-questionnaire.md` (section `0A`)
- `Strategy/Business-Model/claim-register.md`
- `WeRa-Global-KB/02-Products.md`

Confidence:
- high

### 6.2 Если recurring payment был

Нужно указать:

- размер платежа;
- периодичность;
- дата первого платежа;
- сколько платежей было реально сделано;
- есть ли просрочки / пропуски / остановка;
- есть ли invoice trail.

Ответ:
- `UNKNOWN` Размер recurring payment.
- `UNKNOWN` Периодичность.
- `UNKNOWN` Дата первого recurring платежа.
- `UNKNOWN` Количество выполненных recurring платежей.
- `UNKNOWN` Просрочки/пропуски.
- `UNKNOWN` Invoice trail.

Evidence carrier:
- `Strategy/Business-Model/executed-vs-designed.md`
- `Strategy/Business-Model/claim-register.md`

Confidence:
- high

### 6.3 Если recurring payment НЕ было

Нужно понять, почему:

- потому что это чисто технический пилот;
- потому что клиент знакомый;
- потому что договор ещё не оформлен;
- потому что объект не был задуман как коммерческий;
- потому что экономика ещё не была посчитана;
- другая причина.

Ответ:
- `MEMORY` Пилот развился в клиентский CapEx path, а не в чистый recurring lease path.
- `MEMORY` Договорная упаковка остаётся неполной (verbal agreement + writable, but not executed in pack).
- `FACT` По каноническому reading объект сейчас не является full commercial baseline.

Evidence carrier:
- `Strategy/Business-Model/torres-vedras-pilot-questionnaire.md` (section `0A`)
- `Strategy/Business-Model/executed-vs-designed.md`
- `Strategy/Business-Model/starter-drr.md`

Confidence:
- high

### 6.4 Что клиенту обещалось

- Что именно ты обещал пользователю этого объекта?
- Savings?
- Resilience?
- Independence?
- Просто работающую систему?
- Был ли разговор про `20% savings`, zero upfront, leasing, ownership transfer?

Ответ:
- `MEMORY` По факту обсуждались monthly-rent logic (на раннем этапе) и затем CapEx + условный buy-back path.
- `FACT/MEMORY` Для этого объекта bill-vs-bill baseline отсутствует, поэтому точные savings promises не подтверждены data-carrier.
- `FACT` External claim про `20% savings guaranteed` в целом по модели отмечен как unverified и требующий отдельной валидации.
- `UNKNOWN` Точный customer-facing wording, произнесённый в коммуникации с этим клиентом, документально не приложен.

Evidence carrier:
- `Strategy/Business-Model/torres-vedras-pilot-questionnaire.md` (section `0A`)
- `Strategy/Business-Model/claim-register.md`
- `Strategy/Business-Model/open-gates.md`

Confidence:
- medium

---

## 7. Технические данные и телеметрия

### 7.1 Какие данные реально есть

Отметь, что существует:

- generation by day / month;
- consumption by day / month;
- battery charge / discharge;
- outages;
- uptime;
- maintenance log;
- alarms / failures;
- before vs after energy cost;
- фото / видео / screenshots dashboards.

Ответ:
- `FACT/MEMORY` Telemetry/runtime integration по объекту описана в сводном pilot review.
- `MEMORY` Digital maintenance weekly.
- `FACT` Есть явный engineering task на измерение средней месячной генерации и сбор proxy-savings sheet.
- `UNKNOWN` В канонической папке пока нет приложенного monthly/annual telemetry export.
- `UNKNOWN` Structured maintenance log и complete outage history пока не собраны.

Evidence carrier:
- `Strategy/Business-Model/SolarSeed.pilot.tv.md`
- `Operations/_next.md` (task #7)
- `Strategy/Business-Model/torres-vedras-pilot-questionnaire.md` (section `0A`)

Confidence:
- medium

### 7.2 Где хранятся эти данные

- в приложении инвертора;
- локально на mini PC;
- в spreadsheet;
- в памяти;
- в переписке;
- у инженера / установщика;
- нигде не собраны.

Ответ:
- `ESTIMATE` Часть данных вероятно находится в inverter/app и в локальном edge-monitoring контуре.
- `FACT` В документальном пакете данные не консолидированы в единый выгруженный артефакт.
- `UNKNOWN` Точное место хранения raw исторических рядов и retention period.

Evidence carrier:
- `Strategy/Business-Model/SolarSeed.pilot.tv.md`
- `Operations/_next.md`

Confidence:
- low-medium

### 7.3 Что из этого можно реально выгрузить

- какие данные можно получить уже сейчас;
- в каком формате;
- за какой период;
- кто имеет к ним доступ;
- что для этого нужно сделать.

Ответ:
- `FACT` Можно (и нужно) выгрузить среднюю месячную генерацию для proxy-savings расчёта.
- `ESTIMATE` Формат выгрузки: CSV/XLSX/скриншоты dashboard (зависит от источника telemetry).
- `MEMORY/ESTIMATE` Доступ, вероятно, у engineering/founder-side operators.
- `FACT` Для выполнения требуется отдельная инженерная задача (уже поставлена).

Evidence carrier:
- `Operations/_next.md` (task #7)
- `Strategy/Business-Model/torres-vedras-pilot-questionnaire.md` (section `0A`)

Confidence:
- medium

### 7.4 Реальные технические результаты

Если можешь, напиши факты, а не впечатления:

- сколько система генерирует;
- были ли отключения;
- были ли поломки;
- как ведёт себя батарея;
- как работает edge device;
- есть ли реальные показатели reliability.

Ответ:
- `MEMORY` После штормов (`30 января`) проверка показала рабочее состояние без необходимости ремонта.
- `MEMORY` Digital maintenance выполняется еженедельно.
- `FACT/MEMORY` Объект подтверждается как live technical installation.
- `UNKNOWN` Надёжность в числах (uptime %, MTBF, monthly generation profile, outage count) пока не выгружена в canonical packet.

Evidence carrier:
- `Strategy/Business-Model/torres-vedras-pilot-questionnaire.md` (section `0A`)
- `Strategy/Business-Model/executed-vs-designed.md`
- `Operations/_next.md`

Confidence:
- medium

---

## 8. Savings, bills, economics

### 8.1 Есть ли baseline “до установки”

- Есть ли данные по счетам / расходу энергии до установки?
- Есть ли baseline, с которым можно сравнивать?
- Если объект off-grid, тогда какой baseline вообще имеет смысл?

Ответ:
- `FACT/MEMORY` У клиента нет контракта с энергопоставщиком, поэтому bill-vs-bill baseline отсутствует.
- `ESTIMATE` Практичный baseline для этого кейса: generation-based proxy (monthly generation × grid price).
- `FACT` Для сравнения CAPEX следует использовать компонентный baseline из `solar.seed.components.csv`.

Evidence carrier:
- `Strategy/Business-Model/torres-vedras-pilot-questionnaire.md` (section `0A`)
- `Strategy/Business-Model/solar.seed.components.csv`
- `Operations/_next.md`

Confidence:
- high

### 8.2 Есть ли measurable savings

- Есть ли хоть какое-то подтверждение экономии?
- Это measured, estimated или просто предполагаемое?
- Есть ли monthly / annual comparison?

Ответ:
- `FACT` На сегодня нет приложенного measurable monthly/annual savings artifact.
- `ESTIMATE` Возможен proxy-savings расчёт после telemetry measurement.
- `UNKNOWN` Пока нет законченного comparison sheet, пригодного для внешнего использования.

Evidence carrier:
- `Strategy/Business-Model/torres-vedras-pilot-questionnaire.md` (section `0A`)
- `Operations/_next.md` (task #7)
- `Strategy/Business-Model/claim-register.md`

Confidence:
- high

### 8.3 Какие числа можно безопасно публично произносить

- Какие технические цифры можно использовать во внешних разговорах?
- Какие финансовые цифры можно использовать?
- Какие числа звучали раньше, но сейчас не имеют достаточного основания?

Ответ:
- `SAFE FACT` Можно публично: есть один live pilot в Torres Vedras; это technical/executed proof, но не полный commercial proof.
- `SAFE FACT` Можно публично: bill-vs-bill baseline отсутствует; proxy метод находится в работе.
- `SAFE WITH CAVEAT` `€5,001.26` — только reference BOM baseline, не подтверждённый realized CAPEX именно этого пилота.
- `UNSAFE/UNVERIFIED` Нельзя подавать как доказанное: repeatable recurring-payment economics, measured savings guarantee по пилоту, `full commercial baseline proven`, grid-connected UPAC / final-consumer baseline.

Evidence carrier:
- `Strategy/Business-Model/claim-register.md`
- `Strategy/Business-Model/executed-vs-designed.md`
- `Strategy/Business-Model/SolarSeed.pilot.tv.md`
- `Strategy/Business-Model/solar.seed.components.csv`

Confidence:
- high

---

## 9. Обслуживание, сбои, доработки

### 9.1 Были ли инциденты

- поломки;
- downtime;
- battery issues;
- inverter issues;
- проблемы с mini PC / connectivity;
- ошибки установки;
- weather-related incidents.

Ответ:
- `MEMORY` Был weather-related trigger (штормы), после чего `30 января` выполнен maintenance check.
- `MEMORY` По результату check: всё работало корректно, проблем для устранения не было.
- `UNKNOWN` Полный incident ledger (downtime/failure log с датами) в пакете отсутствует.

Evidence carrier:
- `Strategy/Business-Model/torres-vedras-pilot-questionnaire.md` (section `0A`)
- `Strategy/Business-Model/executed-vs-designed.md`

Confidence:
- medium

### 9.2 Кто реально решал проблемы

- ты сам;
- установщик;
- пользователь;
- производитель / support;
- никто.

Ответ:
- `MEMORY/ESTIMATE` Field check и регулярный digital maintenance выполняются founder/engineering side.
- `UNKNOWN` Формально назначенный maintainer по договору и подтверждённые SLA-роли не зафиксированы.

Evidence carrier:
- `Strategy/Business-Model/torres-vedras-pilot-questionnaire.md` (section `0A`)
- `Strategy/Business-Model/current-business-model.md` (maintenance/liability как open package)

Confidence:
- low-medium

### 9.3 Есть ли maintenance burden

- сколько реально требует внимания объект;
- нужно ли ездить на место;
- как часто;
- есть ли recurring field-work.

Ответ:
- `MEMORY` Есть еженедельный digital maintenance burden.
- `MEMORY` Field-work выполняется по событию (пример: check после штормов).
- `UNKNOWN` Нормированный учёт трудозатрат/стоимости обслуживания по объекту не собран.

Evidence carrier:
- `Strategy/Business-Model/torres-vedras-pilot-questionnaire.md` (section `0A`)
- `Strategy/Business-Model/SolarSeed.pilot.tv.md`

Confidence:
- medium

---

## 10. Пользовательский и коммерческий смысл

### 10.1 Как пользователь воспринимает объект

- Считает ли он это своей системой?
- Считает ли он это сервисом?
- Считает ли он это временным экспериментом?
- Готов ли он был бы рекомендовать это другим?

Ответ:
- `UNKNOWN` В пакете нет user interview/feedback artifact с прямой формулировкой восприятия.
- `ESTIMATE` С учётом клиентского CapEx это может восприниматься как “своя система с сервисным/операторским сопровождением”.
- `UNKNOWN` Готовность рекомендовать другим не подтверждена.

Evidence carrier:
- `Strategy/Business-Model/SolarSeed.pilot.tv.md`
- `Strategy/Business-Model/torres-vedras-pilot-questionnaire.md` (section `0A`)

Confidence:
- low-medium

### 10.2 Был бы ли этот объект продан внешнему клиенту в таком виде

- Если бы это был не знакомый/свой объект, можно ли было бы продать ровно такую конфигурацию?
- Что пришлось бы изменить?
- Что в объекте выглядит pilot-only?

Ответ:
- `FACT/ESTIMATE` Технически объект/конфигурация продаваемы, но коммерчески текущий пакет недостаточно clean для repeatable external sales proof.
- `FACT` Для внешней готовности нужно закрыть: письменный договор, payment trail, telemetry-based savings sheet, maintenance ledger, liability/insurance clarity.
- `FACT` Pilot-only часть сейчас: reliance на verbal arrangement и неполный evidence package.

Evidence carrier:
- `Strategy/Business-Model/executed-vs-designed.md`
- `Strategy/Business-Model/open-gates.md`
- `Strategy/Business-Model/claim-register.md`

Confidence:
- high

### 10.3 Это технический пилот или уже коммерческий кейс

Выбери одну главную формулировку и объясни почему:

- `technical pilot`
- `commercial pilot`
- `founder-built live installation`
- `customer installation with incomplete commercial wrapper`
- другое

Ответ:
- `SELECTED` `customer installation with incomplete commercial wrapper`.
- `RATIONALE` Есть реальный installed объект и operator-level execution, но отсутствует закрытый commercial/legal/payment evidence set.

Evidence carrier:
- `Strategy/Business-Model/executed-vs-designed.md`
- `Strategy/Business-Model/starter-drr.md`
- `Strategy/Business-Model/claim-register.md`

Confidence:
- high

---

## 11. Что Torres Vedras реально доказывает

Пожалуйста, ответь очень дисциплинированно.

### 11.1 Что этот объект точно доказывает

Например:

- умеем собрать working installation;
- понимаем hardware stack;
- умеем работать с off-grid micro-farm context;
- умеем поставить edge baseline;
- и т.д.

Ответ:
- `FACT` Команда умеет собрать и запустить working installation в реальном объекте.
- `FACT` Есть выполненный carrier по технической/операционной стороне (installation reality + maintenance process presence).
- `FACT/MEMORY` Клиент принял реальное экономическое участие через CapEx path.
- `FACT` Пилот пригоден как executed carrier для технической осуществимости и operator familiarity.

### 11.2 Что этот объект НЕ доказывает

Например:

- repeatable commercial baseline;
- clean service-fee contract;
- consumer-credit-clean structure;
- externally financeable portfolio logic;
- real measured customer savings;
- и т.д.

Ответ:
- `FACT` Не доказывает repeatable commercial baseline.
- `FACT` Не доказывает clean contract package по этому объекту.
- `FACT` Не доказывает recurring-payment behavior.
- `FACT` Не доказывает measured bill-vs-bill savings (baseline отсутствует).
- `FACT` Не доказывает finance-ready diligence pack без доп. артефактов.

### 11.3 Какую формулировку можно использовать наружу

Напиши 3 версии:

- `internal truthful version`
- `investor-safe version`
- `regulator/counsel-safe version`

Ответ:
- `internal truthful version`: “У нас есть реальный пилот в Torres Vedras с подтверждённой технической/операционной реализацией, но коммерческий и юридический proof-pack ещё неполный.”
- `investor-safe version`: “WeRa has one live pilot deployment in Torres Vedras; technical operation is evidenced, while contract/payment/savings evidence is being consolidated into an auditable fact sheet.”
- `regulator/counsel-safe version`: “Current records support technical deployment and operation; contractual ownership/payment allocation still requires formal written carriers before legal characterization.”

---

## 12. Какие артефакты нужно поднять после заполнения

Поставь статус рядом с каждым пунктом: `есть / можно достать / скорее нет / неизвестно`.

- фото объекта;
- фото оборудования;
- список компонентов;
- invoice / receipt / payment trail;
- договор / переписка про условия;
- телеметрия / screenshots;
- bills / cost comparison;
- maintenance notes;
- contact details involved persons;
- site diagram / one-line diagram;
- anything else.

Ответ:
- фото объекта — `неизвестно`
- фото оборудования — `неизвестно`
- список компонентов — `есть` (reference-level: `solar.seed.components.csv`, требуется site-verification)
- invoice / receipt / payment trail — `неизвестно`
- договор / переписка про условия — `можно достать` (переписку поднять, письменное соглашение оформить/приложить)
- телеметрия / screenshots — `можно достать`
- bills / cost comparison — `скорее нет` (bill baseline отсутствует; нужен proxy метод)
- maintenance notes — `скорее нет` (structured ledger не собран)
- contact details involved persons — `можно достать`
- site diagram / one-line diagram — `неизвестно`
- anything else:
  - executed written agreement artifact — `можно достать`
  - proxy-savings worksheet (monthly generation × grid price) — `можно достать`
  - ownership memo (who paid/who owns/who controls) — `можно достать`

---

## 13. Итоговая короткая сводка от Миши

После заполнения всех секций напиши коротко, в 5–10 строк:

1. что это за объект по-честному;
2. кто за него платил;
3. был ли договор;
4. был ли recurring payment;
5. какие реальные данные по работе объекта уже есть;
6. можно ли считать его commercial pilot;
7. что нужно срочно достать из документов или памяти, чтобы fact sheet стал внешне пригодным.

Ответ:
- Torres Vedras — это реальная клиентская установка с технически исполненным контуром, но с неполной коммерческой упаковкой.
- По текущей рабочей версии объект был профинансирован клиентским CapEx, при этом платежные носители пока не приложены.
- Письменный договор в каноническом пакете пока не исполнен; есть verbal agreement и готовность подписать written agreement.
- Подтверждённого recurring-payment trail по объекту сейчас нет.
- По технике известны live-installation и maintenance markers (в т.ч. проверка 30 января после штормов без выявленных проблем), но нет оформленного telemetry export для savings.
- Корректная текущая классификация: `customer installation with incomplete commercial wrapper`, а не fully commercial pilot.
- Для внешней пригодности срочно нужны: подписанный письменный carrier, payment trail, proxy-savings sheet на measured generation, структурированный maintenance ledger и ownership/control memo.

---

## 14. Read together with

- `Strategy/Business-Model/current-business-model.md`
- `Strategy/Business-Model/executed-vs-designed.md`
- `Strategy/Business-Model/claim-register.md`
- `Strategy/Business-Model/open-gates.md`

formal_proof:
  engine: ml-hilbert
  trl_phase: TRL6
  obligation_id: kb.customers.cases_45_torres_vedras_pilot_questionnaire_v2
  proof_artifact: kb-governance/formal-proofs/customers-cases-45-torres-vedras-pilot-questionnaire-v2.lean
  verification_status: verified
