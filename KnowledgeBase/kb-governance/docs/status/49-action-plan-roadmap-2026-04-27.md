---
title: "WeRa Global — Action Plan & пересобранная Roadmap"
date: "2026-04-28"
type: "action-plan"
status: "v1-pm-proposal"
horizon: "next 7 / 30 / 90 days; H6-12 как outline"
companion: "2026-04-27-project-review.md"
purpose: "Превратить диагностику project review в исполняемый план: re-prioritized open gates, RACI, дедлайны, decision triggers, замена для skeleton-Roadmap."
note: "Этот документ — proposal. Требует совместной проверки на командной сессии перед коммитом. Дедлайны указаны от 2026-04-28 (вторник) как baseline."
---

## Consolidation provenance
- consolidation_actor: `WARP`
- consolidation_source: `/Users/mikhailananyin/Documents/WeRa Global/KB-latest-original/Outputs/PM-Reviews/2026-04-27-action-plan-and-roadmap.md`
- consolidation_date: `2026-06-22`
- consolidation_status: `canonicalized`


# WeRa Global — Action Plan & пересобранная Roadmap

> Companion к `2026-04-27-project-review.md`. Проблематика и контекст — там; здесь — что делать, кто, к какой дате, и что является trigger переключения режима.

---

## 0. Принципы плана

1. **Sequence гейтов важнее агрегатной скорости.** Pilot evidence → counsel feedback → first commercial install → investor pipeline. Без gate N нельзя начинать gate N+1; параллельно идут только треки, которые не зависят друг от друга.
2. **Owners single-named.** Каждая задача имеет одного primary owner. «Все», «команда» — не owner.
3. **Дедлайны привязаны к датам, не к итерациям.** «На этой неделе» = до пятницы 2026-05-01, 17:00 Lisbon.
4. **Anti-list равноправен с приоритетами.** То, что мы НЕ делаем, защищает то, что делаем.
5. **Cadence — главный инструмент компенсации single-founder bottleneck.** Без weekly sync план не работает.

---

## 1. Cadence (фундамент, без которого остальное не держится)

| Ритм | Что | Owner | Дата старта |
|---|---|---|---|
| **Понедельник 10:00 LIS, 30 мин** | Weekly sync: статус 7 пунктов `Operations/_next.md`, разбор blockers, переназначение owners | Алексей | 2026-05-04 (первая) |
| **Среда async** | Mid-week status в Telegram-чате: каждый owner ставит ✅/🟡/🔴 по своим задачам | Все | 2026-04-29 (завтра) |
| **Пятница 16:00 LIS, 60 мин** | Weekly retrospective + апдейт `Operations/_next.md` на следующую неделю + апдейт `Log.md` | Алексей | 2026-05-01 (эта пятница) |
| **Раз в 2 недели, четверг** | Decision review: claim register, executed-vs-designed, open gates — что закрылось/изменилось | Алексей | 2026-05-07 |
| **Раз в месяц, конец месяца** | Roadmap re-sync с canon (см. §6) | Алексей | 2026-05-29 |

> Если не зафиксировать cadence сейчас, всё ниже превратится в «список идей PM, который мы прочитали».

---

## 2. RACI на 6 критических решений

R = Responsible (делает), A = Accountable (отвечает за результат), C = Consulted, I = Informed.

| Решение | R | A | C | I | Дедлайн решения |
|---|---|---|---|---|---|
| **Что делать с `20% savings guaranteed`** (limit / prove / remove) | Алексей | Михаил | Tanya | — | 2026-05-04 |
| **Какой Stage 1 instrument канонический** (CLA / SAFE / Equity bridge / иной) | Михаил | Михаил | Алексей, Mигель/finance counsel | Tanya | 2026-05-15 |
| **PT vs ES первая операционная юрисдикция** | Михаил | Михаил | Mигель + ES counsel | Алексей, Tanya | после Track B.1 ответа Мигеля (≤2026-06-15) |
| **Формат участия Алексея и Тани** (advisory / part-time / full-time, какие зоны) | Михаил | Михаил | Алексей, Таня | — | 2026-05-04 |
| **Регистрировать КИК Q2 vs ждать Track B.3 counsel** | Михаил | Михаил | corporate counsel (ещё не engaged) | Алексей, Tanya | после Track B.3 ответа (≤2026-07-15) |
| **Перенос или сохранение compute/Nextcloud Block 6 wedge в активной работе** | Алексей | Алексей | Mигель (energy implications), Михаил | Tanya | после первого commercial install (≤2026-08-31) |

> Принципиальное правило: А-роль в этой таблице за Мишей по 4 из 6 решений. Это ОК на текущей стадии, но требует чтобы C/I-стороны действительно получали материалы за 48 часов до дедлайна решения, иначе bottleneck повторится.

---

## 3. Next 7 days (2026-04-28 → 2026-05-04)

> Цель недели: **закрыть Torres Vedras evidence pack + дать решение по `20% claim` + назначить Sintra meeting + синхронизировать Roadmap с canon.**

| # | Задача | Owner | Deliverable | Deadline |
|---|---|---|---|---|
| 1 | Подписать written agreement / signed memorialization по Torres Vedras на основе `Outputs/Legal-Drafts/torres-vedras-short-memorialisation-draft-v1.md` | Михаил | Подписанный артефакт в `Outputs/Legal-Drafts/` + запись в Log.md | 2026-04-30 |
| 2 | Собрать payment trail: инвойсы / чеки / переводы по CAPEX TV; оформить ownership/control memo | Михаил | Payment trail PDF + ownership memo в `Outputs/Legal-Drafts/` | 2026-04-30 |
| 3 | Telemetry export + proxy-savings sheet (avg monthly generation × grid price vs `solar.seed.components.csv`) | Engineering team (Михаил координирует) | `.xlsx` + CSV в `Strategy/Business-Model/` | 2026-05-01 |
| 4 | Maintenance ledger: формализовать 30 января check + weekly digital maintenance в табличный формат | Engineering team (Михаил координирует) | `Strategy/Business-Model/torres-vedras-maintenance-ledger.md` | 2026-05-02 |
| 5 | Решение по `20% savings guaranteed`: limit / prove / remove. Если remove — обновить funnel/calculator/сайт. Если limit — переписать на conditional underwriting language из `legal-operating-description-draft.md` §9.3 | Алексей | Запись в `Log.md` + при необходимости commits в funnel | 2026-05-04 |
| 6 | Removed §15 (real-estate tokenization) из `legal-operating-description-draft.md`; перенести в отдельный sealed `Strategy/Legal/far-paths-tokenization-memo.md` | Алексей | Updated draft + new sealed file | 2026-04-30 |
| 7 | Назначить in-person meeting с installer из Синтры; подготовить Frame IV opening package (1 page: что предлагаем installer-у, что требуем взамен) | Михаил | Meeting calendar invite + 1-pager в `Outputs/Pitches/frame-iv-installer-opening.md` | 2026-05-02 |
| 8 | Пересинхронизировать `Partnership/Roadmap.md`: убрать «КИК Q2», заменить на legal-gate-driven последовательность (см. §6 этого файла) | Алексей | Updated `Partnership/Roadmap.md` + запись в Log.md | 2026-05-03 |
| 9 | Зафиксировать формат участия Алексея и Тани в `Partnership/Roles.md` (advisory / part-time / full-time, какие зоны owner) | Михаил | Updated Roles.md, signed by all three в Telegram | 2026-05-04 |
| 10 | Engagement statement с Мигелем: friend lawyer vs engaged counsel, scope, ожидаемый turnaround, retainer (если применимо) | Михаил | Email или короткий .md файл в `Operations/Legal/` | 2026-05-04 |

**Definition of done для недели:** все 10 задач закрыты или явно эскалированы как `blocked: <причина>` в weekly retrospective пятницы 2026-05-01. Если 7+ закрыто — неделя удачная.

---

## 4. Next 30 days (2026-04-28 → 2026-05-28)

> Цель месяца: **получить первый written counsel feedback + пересобрать base case без WiFi Map + закрыть второго клиента в proposal stage + получить engagement signal от Sintra installer.**

### 4.1 Legal track

| Задача | Owner | Deliverable | Deadline |
|---|---|---|---|
| Финальный package для Мигеля по Track A: Torres Vedras retrospective qualification + signed memorialization + ownership/control memo | Алексей | Email Мигелю с приложениями | 2026-05-08 |
| Параллельно отправить Track B.1 (energy/contract package) — он не зависит от Track A evidence | Алексей | Email Мигелю с приложениями | 2026-05-08 |
| Получить **письменный** ответ Мигеля по Track A | Михаил (follow-up) | Email response в `Operations/Legal/` | до 2026-05-22 |
| Получить **письменный** ответ Мигеля по Track B.1 | Михаил (follow-up) | Email response | до 2026-05-22 |
| Identify + warm intro к consumer-finance counsel (Track B.2) и corporate/securities/tax counsel (Track B.3) | Михаил | 2 имени + warm intros в `Operations/Legal/_index.md` | 2026-05-15 |
| Identify + warm intro к Spanish energy counsel для PT vs ES сравнения | Алексей | 1 имя + warm intro | 2026-05-22 |
| Insurance counsel preliminary call — primary risk allocation вопросы | Михаил | Call notes в `Operations/Legal/` | 2026-05-25 |

### 4.2 Capital / financial track

| Задача | Owner | Deliverable | Deadline |
|---|---|---|---|
| Edge-only BOM recut: чистая стоимость минимального monitoring/edge baseline без legacy compute stack | Алексей (engineering input) | Updated BOM в `Strategy/Business-Model/edge-only-bom.md` + numbers in `WeRa.Financials.xlsx` | 2026-05-15 |
| Base case без WiFi Map: пересобрать Y1-Y2 финмодель без 66% revenue dependency. Включить sensitivity ±20%, ±50% от target conversion в base subset | Михаил | Updated `WeRa.Financials.xlsx` + 1-pager в `Strategy/Fundraising/base-case-no-wifimap.md` | 2026-05-22 |
| Lean operating budget (12 мес, 3-4 человека): отдельно от scaled 16-person KB model | Алексей | `Strategy/Fundraising/lean-budget-12m.md` | 2026-05-22 |
| Stage 1 canonical instrument decision: CLA vs SAFE vs equity bridge. Включить ask size, valuation cap, conversion mechanics | Михаил | Decision memo в `Strategy/Fundraising/stage1-instrument.md` + Log.md entry | 2026-05-15 |
| 5-7 warm investor leads на watchlist с typed routing (angel / family office / strategic / seed fund) | Алексей | `Operations/Investors/_pipeline.md` updated | 2026-05-27 |

### 4.3 GTM / clients

| Задача | Owner | Deliverable | Deadline |
|---|---|---|---|
| In-person meeting с Sintra installer + signed informal partnership intent | Михаил | Meeting note в `Meetings/` + signal record в `Operations/Suppliers/` | 2026-05-15 |
| Закрыть второго клиента (Proposal Sent → Technical Assessment) | Михаил | Updated `Operations/Clients/_pipeline.md` + LOI или signed proposal | 2026-05-27 |
| Подготовить repeatable proposal template для selected first subset (small controllable site, simple decision chain) | Алексей | `Outputs/Templates/customer-proposal-template.md` | 2026-05-15 |
| First-subset GTM playbook: lead criteria, qualification questions, contract checklist, pricing logic (без `20%` claim до решения по нему) | Алексей | `Outputs/Templates/first-subset-gtm-playbook.md` | 2026-05-22 |
| Frame IV installer playbook: что installer-партнёр получает (lead-fee / rev-share / margin / discount), exclusivity, lead-routing | Михаил | `Outputs/Templates/installer-partnership-playbook.md` | 2026-05-25 |

### 4.4 Block 6 (compute wedge research, не product)

| Задача | Owner | Deliverable | Deadline |
|---|---|---|---|
| 5-7 интервью с NGO / cooperatives / small public-interest entities в PT/ES о local managed Nextcloud / data room | Алексей или Таня (если онбординг готов) | Notes consolidated в `research/2026-05-XX-block6-interviews.md` | 2026-05-27 |
| Block 6 продуктовый wedge: launch decision (go / hold / kill) **не принимается** в этом окне; интервью — только для информирования будущего решения | — | — | post-90-days |

### 4.5 Team / operations

| Задача | Owner | Deliverable | Deadline |
|---|---|---|---|
| Зафиксировать минимум 1 ownership transfer от Михаила к Алексею или Тане (один operational track owner switch) | Михаил | Updated Roles.md + Log.md entry | 2026-05-15 |
| Подготовить short investor-safe one-pager на базе `current-business-model.md` (без unverified claims, без real-estate tokenization, без NL STAK) | Алексей | `Outputs/Pitches/wera-one-pager-investor-safe.md` | 2026-05-25 |
| Закрыть нижний порог ликвидности в `Partnership/Terms.md` §5 (конкретная цифра) | Михаил | Updated Terms.md + signed amendment | 2026-05-15 |
| Уточнить перечень решений, требующих vето основателя, в `Partnership/Terms.md` §8 | Михаил | Updated Terms.md | 2026-05-15 |

---

## 5. Next 90 days (2026-04-28 → 2026-07-27)

> Цель квартала: **первый repeatable grid-connected commercial install + 5-7 quoted proposals в одном subset + Track A/B.1 закрыты + Stage 1 instrument готов к outreach + установлен второй counsel (B.2 или B.3) + начат formal investor outreach.**

### 5.1 Strategy & business-model

- **Phase 1 success metric** зафиксирован численно: «3 quoted proposals + 1 signed contract в первом subset с recurring payment trail at 30+ days» — это и есть transition trigger к рассмотрению Block 6 wedge launch.
- Updated `Strategy/Business-Model/current-business-model.md` после первых counsel ответов (только если требуется; иначе — оставить v1 24 апреля как-есть).
- `Strategy/Scenarios/` — собрать 3 working scenarios: (a) base case без WiFi Map, (b) base case + Frame IV traction, (c) downside (1 client only). Не больше трёх.

### 5.2 Legal

- Track B.2 (consumer credit) — counsel engaged, первый call проведён, written feedback получен.
- Track B.3 (corporate/securities/tax) — counsel engaged, первый call проведён.
- PT vs ES counsel comparison: одна страница в `Strategy/Legal/pt-vs-es-comparison.md` с counsel-confirmed точками сравнения.
- CMVM re-engagement decision: идём ли сами (Миша) или через counsel.
- Insurance / liability allocation: working draft в `Strategy/Legal/`.

### 5.3 Capital

- Stage 1 instrument finalized (CLA / SAFE / иной), term-sheet в `Outputs/Legal-Drafts/`.
- Investor pipeline: 10-15 named leads, typed по investor type, 3-5 в `First Call` или дальше.
- Если есть warm signal — открытый soft-close разговор с одним инвестором.

### 5.4 GTM

- 1-2 commercial recurring contracts signed (не Torres Vedras, не founder-built).
- 3-5 quoted proposals в selected first subset.
- Iberia Renew Engineering — Master Service Agreement или working framework, который определяет lead-routing / margin / responsibility split.
- Sintra installer — либо signed channel partnership, либо явно closed как dead lead.

### 5.5 Operations

- Команда: явный second owner на минимум одном operational track (legal pipeline / investor pipeline / GTM ops).
- `Outputs/` — каждая папка имеет минимум 1-2 готовых артефакта (pitch, proposal template, legal draft).
- Cadence: 12 weekly syncs прошли без срывов; `Operations/_next.md` обновляется еженедельно.

### 5.6 Block 6 wedge

- Интервью завершены, research-memo в `research/`.
- Решение go / hold / kill **в конце 90-дневного окна, не раньше.**

---

## 6. Roadmap-замена для `Partnership/Roadmap.md`

> Этот раздел — текст, который должен заменить `Партнёрство/Roadmap.md` (или быть туда скопирован, после согласования). Ключевая идея: **gate-driven, не calendar-driven.** Регистрация юрструктуры идёт **после** counsel feedback, не до.

### Горизонт 1 — следующие 30 дней (2026-04-28 → 2026-05-28)

| # | Задача | Owner | Trigger |
|---|---|---|---|
| 1 | Torres Vedras evidence pack closed (memorialization signed + payment trail + ownership memo + telemetry export + maintenance ledger) | Михаил | до отправки Мигелю |
| 2 | Counsel package для Мигеля по Track A + Track B.1 отправлен | Алексей | пока на руках evidence |
| 3 | Решение по `20% savings guaranteed` принято и отражено в funnel | Алексей | до next live proposal |
| 4 | Sintra installer in-person meeting проведена | Михаил | до Frame IV становится investor-facing claim |
| 5 | `Partnership/Roles.md` закрыт (формат участия Алексея/Тани зафиксирован) | Михаил | до investor outreach |
| 6 | Engagement statement с Мигелем зафиксирован | Михаил | до отправки тяжёлого counsel package |
| 7 | Real-estate tokenization §15 вынесена в sealed memo | Алексей | до отправки package |

### Горизонт 2 — следующие 90 дней (2026-05-28 → 2026-07-27)

| # | Задача | Owner | Trigger |
|---|---|---|---|
| 1 | Письменный ответ Мигеля по Track A и Track B.1 получен | Михаил | внутренний blocker для Track B.2/B.3 outreach |
| 2 | Edge-only BOM recut завершён | Алексей | до investor / regulator материалы |
| 3 | Base case без WiFi Map пересобран; lean budget зафиксирован | Михаил | до investor outreach |
| 4 | Stage 1 canonical instrument выбран (CLA / SAFE / иной); term-sheet draft в `Outputs/Legal-Drafts/` | Михаил | до first investor call |
| 5 | Track B.2 counsel engaged + первый written feedback | Михаил | до signing first household contract |
| 6 | Track B.3 counsel engaged + первый written feedback | Михаил | до фиксации первой формальной юрструктуры |
| 7 | First repeatable grid-connected commercial install (не TV, не founder-built, recurring payment) | Михаил | до апгрейда «у нас есть pilot» в «у нас есть commercial baseline» |
| 8 | 3-5 quoted proposals в selected first subset | Михаил | до Phase 1 success criteria |
| 9 | Investor watchlist: 10-15 named leads, typed routing | Алексей | до первого formal pitch |

### Горизонт 3 — 6-12 месяцев (2026-07-27 → 2027-04-28)

> Заполнять после того, как закроется хотя бы 5 пунктов H2.

Outline (не commitment):

- Stage 1 close (€500k or revised ask) — после canonical instrument + 2-3 commercial contracts + Track A&B.1 closed.
- Юрструктура зарегистрирована: PT или ES, по результату Track B.3 counsel и PT/ES comparison. **НЕ КИК автоматически** — это могло измениться по counsel feedback.
- Phase 1 → Block 6 wedge transition decision (go / hold / kill).
- Frame IV scaling: 3-5 installer-партнёров с repeatable origination.
- Y1 commercial target: **не €170,954/100 юнитов**, а consensus-target после base-case rebuild. Honest version, скорее всего: 5-10 contracts по avg config или 15-25 по base config, ARR €50-150k.
- Resilience-narrative окно: сильно использовать до Q2 2027, дальше narrative-foundation менять.

### Критерии успеха партнёрства (Y1) — обновлено

Старая формулировка (Lisbon meeting): *«К концу года: есть клиенты, есть базовый денежный поток, есть следующий шаг (инвестиции для роста). Если есть клиенты и деньги, но нет следующего шага — это можно считать проигрышем партнёрства.»*

Я бы добавил:
- **Минимум 5 commercial contracts** (не TV, не founder-built);
- **Stage 1 close или term-sheet** на руках;
- **Track A/B.1/B.2/B.3 counsel feedback в письменном виде**;
- **Working juridical structure registered** (на основе counsel feedback, не legacy КИК);
- **Минимум 2 operating-track owners в команде** (не Миша как single owner всех treков).

Если 4 из 5 закрыты — год успешный. Если 2-3 — открыто пересматривать партнёрство. Если 0-1 — закрытие по Terms §5/§6.

---

## 7. Decision triggers / no-go thresholds

| Trigger | Что меняется | Action |
|---|---|---|
| **Мигель не даёт письменный ответ к 2026-06-15 (45 дней с отправки)** | Track A/B.1 timeline удлиняется; Sintra и second client становятся рисковыми | Парallel engage второго PT energy counsel (`hot-swap` стратегия), не как замена, а как acceleration |
| **20% savings claim прошёл 2026-05-04 без решения** | Live external exposure без internal alignment | PM-эскалация в weekly sync; deadline переносится максимум на 1 неделю, потом по умолчанию `remove` |
| **Stage 1 instrument не выбран к 2026-05-15** | Investor outreach невозможно открыть | Engage finance/securities counsel по специально-узкому вопросу (1 hour call), не по Track B.2 broad memo |
| **Investor pipeline пуст к 2026-05-27** | Runway clock работает без conversion potential | Открыть angel/family-office channel через personal network; не ждать typed seed-fund outreach |
| **Sintra installer meeting не назначен к 2026-05-02** | Frame IV evidence остаётся `signal only` | Phase down Frame IV в narrative до получения evidence; перейти на direct GTM как primary |
| **Roles.md не закрыт к 2026-05-04** | Single-founder bottleneck продолжает блокировать делегирование | PM-эскалация: 1-час session между Михаилом, Алексеем и Таней с явным forced-decision frame |
| **Track A counsel ответ показывает unrecoverable issues с TV** | Pilot нельзя использовать как evidence ни в какой форме | Pivot на «у нас есть TV как technical demo, но first commercial — это next install»; usable, но investor narrative должен это явно сказать |
| **Y2 base case без WiFi Map даёт ARR < €100k** | Honest finmodel показывает, что Stage 1 €500k не закрывает runway до Y2 break-even | Re-design Stage 1 как €750k–€1M ask с longer runway, или re-design product mix (Average Config vs Base Config split) |

---

## 8. Anti-list (что НЕ делаем в 90 дней)

> Этот раздел — защитный.

1. **Не открываем formal investor outreach** до того, как (а) base case без WiFi Map пересобран и (б) Stage 1 instrument выбран и (в) Track A&B.1 counsel feedback на руках. Слишком ранний outreach = burned warm leads.
2. **Не регистрируем юрструктуру** до Track B.3 counsel feedback. Особенно — не «КИК Q2», как написано в legacy Roadmap.
3. **Не подписываем формальный контракт** с household или microbusiness customer до Track B.2 (consumer credit) feedback. Если рывок нужен срочно — только small SME с явно non-consumer profile.
4. **Не возвращаем GPU datacenter / Объект A** ни в внешние материалы, ни во внутренние стратегические дискуссии до того, как все 4 trigger conditions выполнены (anchor demand + power/site thesis + funding object + operating model).
5. **Не запускаем Block 6 как product**. Только interviews. Product launch — после Phase 1 success criteria.
6. **Не пишем новый «strategy doc»**, которого нет в canon (UTS / DRR / claim register / executed-vs-designed / capital architecture / open gates / regulatory routing / legal-operating-description). Канон полный. Если новый artifact нужен — он расширяет существующий, не создаёт parallel doc.
7. **Не возвращаем `customer → shareholder conversion` / NL STAK / real-estate tokenization / network state** в любые external или quasi-external материалы (включая investor decks, proposals, websites, calculator copy) до Track B.3 counsel feedback.
8. **Не торопим reset canon**. 22-24 апреля canon только зафиксирован. Любые re-canonical итерации — после 15 мая (≥3 weeks отстоя), кроме явных ошибок типа real-estate tokenization §15 (которая уже идёт в работу на этой неделе).

---

## 9. Verification checkpoints

> PM-функция должна проверять не «список выполнен», а «реальность совпадает с canon».

| Когда | Что проверяем | Owner проверки |
|---|---|---|
| Каждую пятницу | `Operations/_next.md` отражает реальные приоритеты следующей недели; нет `active` задач, висящих 2+ недели | Алексей |
| 2026-05-04 | Все 10 задач недели §3 либо closed, либо явно escalated | Алексей (PM-роль) |
| 2026-05-15 | Stage 1 instrument decision принят; Roles.md закрыт; Sintra meeting проведена | Алексей (PM-роль) |
| 2026-05-28 | 30-day milestones §4 закрыты на 70%+ | Алексей (PM-роль) |
| 2026-06-15 | Мигель ответил по Track A и B.1 в письменном виде. Если нет — trigger §7 | Михаил (lead) + Алексей (PM-функция) |
| 2026-07-27 | 90-day milestones §5 closed на 60%+; Roadmap H3 заполнен по правилу «после 5 пунктов H2 закрыто» | Все |

---

## 10. Финальный совет PM

Этот план — это **не апгрейд canon**, а **исполнительный экзоскелет вокруг существующего canon**. Если в команде возникает ощущение «надо переписать current-business-model снова» в ближайшие 14 дней, это сигнал, что план игнорируется. Канон зафиксирован 24 апреля. Сейчас задача — не уточнять его, а проверять его реальностью: counsel feedback, signed contracts, payment trails. Каждое такое внешнее evidence либо подтверждает canon, либо — и только в этом случае — даёт право его пересмотреть.

Главный риск ближайших 30 дней — **спутать совершенствование canon с execution**. Это два разных режима, и в текущем окне нужен второй.

---

*Companion: `2026-04-27-project-review.md` — диагностика и обоснование приоритетов. Этот файл — план без обоснований.*

formal_proof:
  engine: ml-hilbert
  trl_phase: TRL6
  obligation_id: kb.governance.status_49_action_plan_roadmap_2026_04_27
  proof_artifact: kb-governance/formal-proofs/governance-status-49-action-plan-roadmap-2026-04-27.lean
  verification_status: verified
