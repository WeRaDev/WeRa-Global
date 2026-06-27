---
title: "WeRa Cloud — R&D Concept Note: Digital Risk-Hedge Track"
date: "2026-05-18"
type: "rnd-proposal"
status: "draft-for-cofounder-review"
addressee: "Михаил (CEO), Алексей (Co-founder), Таня (Co-founder)"
author: "Business Analyst, WeRa Global"
purpose: "Сформулировать R&D-программу цифрового продукта как независимый risk-hedge для Track B (service-fee + operator baseline)."
related_docs:
  - "Strategy/Business-Model/current-business-model.md"
  - "Strategy/Business-Model/open-gates.md"
  - "Strategy/Business-Model/claim-register.md"
  - "Strategy/Legal/regulatory-routing-and-power-tier-matrix.md"
  - "research/WeRa-Consultant-Frame.md"
  - "uploads/WeRa Cloud — Business-as-a-Software — Transcription & Deep Critical Analysis.md"
---

## Consolidation provenance
- consolidation_actor: `WARP`
- consolidation_source: `/Users/mikhailananyin/Documents/WeRa Global/KB-latest-original/Strategy/Digital-RnD/2026-05-18-concept-note-wera-cloud-rnd.md`
- consolidation_date: `2026-06-22`
- consolidation_status: `canonicalized`


# WeRa Cloud — R&D Concept Note: Digital Risk-Hedge Track

> **Адресат:** со-основатели WeRa Global — Михаил, Алексей, Таня.
> **Версия:** draft v0.1, 18 мая 2026.
> **Решение, которое запрашивается:** запуск 12-недельной R&D-программы по WeRa Cloud (BaaS-прототип) как **независимого hedge-трека** к Track B + параллельный desk-research по Tokenized Service-Financing.

---

## English Executive Summary

WeRa's current strategic frame — Track B `service-fee + operator` baseline around distributed self-consumption solar assets — carries seven load-bearing open gates (energy-law routing, power-tier matrix, consumer-credit qualification, corporate/securities structure, WiFi Map 66% Y2 dependency, Torres Vedras evidence boundary, default/insurance stack). Each gate must be resolved through counsel, regulators or physical pilots whose iteration cost is measured in months and €5k–€23k of CAPEX per data point. **The cost of being wrong on the solar track is high; the speed of validating it is low.**

This concept note proposes a **second, independent track**: a focused 12-week R&D programme that builds and field-tests a privacy-first AI knowledge-management cloud for SMEs (WeRa Cloud BaaS). The purpose is **not** to bolt a "digital upsell" onto the solar offer. The purpose is to **stand up a parallel commercial object whose €/iteration is two orders of magnitude lower than solar**, whose regulatory surface is confined to GDPR and the EU AI Act, and whose customer segment partially overlaps the Track B target SME without depending on it.

We propose to build the prototype on the existing Nextcloud + local-AI architecture WeRa is already familiar with, validate it against five paying pilot SMEs sourced **independently** of the solar pipeline, and treat the speaker's tokenized-service-financing idea as a **research-only workstream** — desk research, counsel scoping, legal-architecture mapping — with **zero customer-facing claims** until corporate/securities/PSD2/MiCA routing is closed.

The proposal asks the co-founders to approve four things: (1) a 12-week scope with three explicit Go/No-Go gates, (2) a sub-€8k cash budget plus founder time-share, (3) a clean organisational separation between the digital and solar tracks at the operational level, and (4) two new owners on the captable RACI: **Михаил** as product/IC owner, **Алексей** as data-protection and architecture owner. Track B remains the primary investor-facing narrative; the digital track is held as an internal optionality lever and a Y2-revenue diversifier away from the WiFi Map concentration risk.

If the prototype hits its three Go-gates — five paying pilots, ≥€50 ARPU/month, ≥40% week-4 active use — the digital track is promoted to a co-equal frame in the next investor update. If any gate fails, the track is paused with **<€8k sunk cost and a documented learning asset**, while Track B continues unaffected.

---

## 1. Контекст и постановка задачи

### 1.1. Почему вообще нужен digital R&D трек

Track B (`service-fee + operator` baseline) — наш **selected working baseline**, не доказанная чистая структура (см. `Strategy/Business-Model/current-business-model.md`, `Strategy/Business-Model/starter-drr.md`). Его валидация требует:

- завершения energy-law / UPAC routing у португальского energy counsel и потенциально DGEG/ERSE;
- закрытия consumer-credit qualification у finance counsel и потенциально Banco de Portugal;
- разделения corporate/securities/tax вопросов (CIC/STAK/customer-participation) у соответствующего counsel и потенциально CMVM;
- privacy/CNPD маршрута для телеметрии;
- power/grid-status matrix (устный порог `21-25 kW` пока не операциональный факт);
- evidence pack по Torres Vedras сверх founder-memory questionnaire;
- default/insurance/repossession stack.

Каждый из этих gates требует месяцев календарного времени, юридических часов и в случае физических пилотов — €5k–€23k CAPEX за единицу опыта. Параллельно у нас **Y2 revenue на 66% зависит от WiFi Map**, по которому нет договора (Consultant Frame, Assumption §2 и §5).

**Сухая формулировка:** мы выбрали трек, на котором цикл "гипотеза → проверка → знание" длинный, дорогой и зависит от внешних authority. У pre-seed команды с burn-rate €2k/мес и одним исполненным пилотом такая конфигурация — стратегически хрупкая.

### 1.2. Что предлагает приложенный документ

Транскрипт `WeRa Cloud — Business-as-a-Software` и сопровождающий критический анализ описывают **две различные продуктовые идеи**, неявно склеенные в один концепт:

- **Product 1 — WeRa Cloud (BaaS).** Privacy-first AI-облако для SME: Nextcloud + локальные модели + frontier API через прокси-слой, со структурированной knowledge base "бизнес как софт". Регуляторная поверхность: GDPR + EU AI Act. Time-to-market: 6–18 месяцев. Капитал: умеренный.

- **Product 2 — Tokenized Service-Financing.** SME отдают токенизированную долю в обмен на ваучеры, покрывающие их цифровые сервисы; WeRa выступает collective investment vehicle + payment-issuer + data-broker. Регуляторная поверхность: AIFMD/UCITS, PSD2, MiCA, GDPR, securities law, потенциально несколько юрисдикций. Time-to-market: 18–36+ месяцев. Капитал: высокий.

Критический анализ корректно фиксирует, что **смешивание этих двух продуктов в одной пресс-странице — операционная ошибка**. Со-основатели должны принять решение об их разделении.

### 1.3. Что предлагает этот документ

Сформулировать R&D-программу, в которой:

- **Product 1 (WeRa Cloud BaaS)** становится **независимым build-track-ом** — pure risk-hedge к Track B, со своей командной ролью, своим бюджетом, своими ICP-пилотами, не пересекающимися с solar pipeline;
- **Product 2 (Tokenized Service-Financing)** становится **research-only workstream** — desk research, counsel scoping, regulatory architecture mapping; **без customer-facing claims**, без обещаний инвесторам, без присутствия в pitch;
- Track B остаётся **primary investor-facing narrative** в соответствии с правилом Four Boxes (Consultant Frame). Digital track держится внутри — как optionality lever и Y2-revenue diversifier.

---

## 2. Цель и принципы R&D

### 2.1. Цель программы

> За 12 недель и менее чем €8k cash подтвердить или опровергнуть, что **privacy-first AI knowledge-management для португальских/иберийских SME — это коммерчески жизнеспособный самостоятельный продукт WeRa Global**, не зависящий от исхода Track B.

### 2.2. Принципы

1. **Independence.** Digital R&D не использует solar pipeline как warm channel. ICP-пилоты ищутся через индустриальные ассоциации, локальные business associations, MSP-партнёров, прямую outreach. Это намеренное ограничение: если мы успешно валидируем digital track через solar клиентов, мы не узнаем, работает ли он сам по себе.
2. **Cheap iterations.** Каждый прототип-цикл ≤ 2 недели и ≤ €500 marginal cost. Никакого Lean 4 / Coq / multi-agent orchestration в MVP — только rule-based валидация + LLM consistency check (см. §5).
3. **Evidence over ambition.** Любое утверждение для инвесторов или для самих со-основателей сопровождается claim status в стиле `Strategy/Business-Model/claim-register.md`: `working`, `tested`, `confirmed`. По умолчанию все тезисы — `working`.
4. **Regulatory hygiene.** GDPR DPIA, базовый DPA-шаблон и AI Act risk classification — **до** первого реального customer-onboarding, не после. Любая идея, требующая securities/PSD2/MiCA-licensing — в research-only track.
5. **Four Boxes discipline.** Внутреннее positioning может говорить о цифровой optionality. Investor-facing pitch обновляется только после прохождения Go-gate 3 (см. §9).
6. **No tokenization claims to customers.** До прохождения corporate/securities counsel — никаких упоминаний share-for-service voucher mechanism в product copy, sales scripts, marketing pages.

---

## 3. Объект R&D — два продукта, две дисциплины

### 3.1. Product 1: WeRa Cloud (BaaS) — Build Track

**Что это:** SaaS-облако для малого бизнеса, в котором клиент загружает документы и подключает свои digital channels (email, WhatsApp Business, Facebook Marketplace, локальные платформы), а система автоматически строит и поддерживает **структурированную knowledge base его бизнеса** ("персональная Wikipedia бизнеса"), которая, в свою очередь, питает:

- автоматизированные ответы клиентам;
- генерацию маркетинговых артефактов (посты, страницы, описания);
- внутреннюю поисковую систему "что мы знаем о X";
- задачник / лёгкий CRM на базе той же knowledge base.

**Архитектура (см. §5):** Nextcloud Hub (workspace, files, talk) + локальная LLM через Ollama/LocalAI (квантизация и feature extraction) + frontier-API (валидация, генерация финального текста) через свой proxy с zero-retention контрактом. Никакой формальной verification (Lean/Coq) в MVP — её обещание было самым шатким технически в исходном транскрипте.

**Кому продаётся (ICP, см. Приложение A):** португальский/испанский SME, 5–25 сотрудников, реальная экономика (агро, локальные услуги, ремесло, небольшие производства), уже платит за хотя бы один из: email-хостинг, веб-сайт, Facebook/Google Ads, CRM, рекламу на локальных marketplace. Не зависит от того, является ли он solar клиентом WeRa.

**Монетизация (для прототипа):** €49–€79/мес subscription + token-pass-through (markup 20–30% на frontier inference). Сознательный отказ от `1€ entry point` из транскрипта — на этой стадии unit economics такой цены не выдерживают, а freemium создаёт когорту без intent.

**Что мы НЕ делаем в R&D:** multi-agent dispute resolution; формальная verification бизнес-логики; токенизация долей; интеграция с energy-billing / utility-billing для "follow-the-money" data acquisition (это требует отдельного legal-pass и параллельных DPA с провайдерами).

### 3.2. Product 2: Tokenized Service-Financing — Research-Only Track

**Что это (как идея):** механизм, в котором SME продаёт минорную токенизированную долю collective investment vehicle, получает в обмен ваучеры, оплачивает ими свои digital services (email, internet, energy, ads), а WeRa получает (а) долевую позицию, (б) "follow-the-money" data access, (в) management fee.

**Что мы делаем в research-only track:**

- Desk research по compliant STO frameworks: ONINO (DE), SIX Digital Exchange (CH), Dusk Network — какие из них применимы к португальскому SME, при какой структуре;
- Mapping регуляторных режимов: AIFMD vs UCITS vs национальная PT classification; PSD2 для voucher issuance; MiCA для inference-tokens; securities law per jurisdiction;
- Scoping вопросов для corporate/securities counsel (это **не Miguel** — это отдельный counsel по corporate/securities/tax);
- Анализ existing GDPR DPIA precedent для email/billing data access под обоснование "follow-the-money".

**Что мы НЕ делаем в research-only track:**

- не строим прототип;
- не упоминаем механизм в customer-facing материалах;
- не обещаем инвесторам конкретный timeline;
- не привязываем unit-economics Product 1 к субсидии от Product 2.

**Deliverable research-only track-а к концу 12 недель:** один структурированный memo на 8–15 страниц в `Strategy/Digital-RnD/research/tokenization-routing-memo.md` с фиксацией: какие counsel-разговоры нужны, какая корпоративная структура минимально жизнеспособна, какой timeline и какие капитальные требования, какой первый "tokenization gate" — аналогично `Strategy/Business-Model/open-gates.md`.

---

## 4. Гипотезы и метрики валидации

### 4.1. Load-bearing hypotheses

| # | Гипотеза | Что считаем доказательством | Способ проверки |
|---|---|---|---|
| H1 | Иберийский SME (5–25 чел.) готов платить ≥€50/мес за privacy-first AI-облако, привязанное к его данным | 5 paying pilots × ≥€50 ARPU/мес за 12 недель | Прямые продажи через ассоциации/MSP/cold outreach |
| H2 | Структурированная knowledge base даёт измеримое сокращение времени поиска/ответа клиенту | ≥30% reduction в среднем time-to-customer-response у пилотов на неделе 8 vs baseline неделя 1 | Time-tracking instrument в самом продукте + customer interviews |
| H3 | Hybrid local+frontier архитектура держит unit economics при €50–€79 ARPU | Marginal cost per active user ≤ 35% от ARPU на конец недели 12 | Реальное измерение infrastructure + frontier API spend |
| H4 | Privacy-first позиционирование — significant purchase driver для PT/ES SME | ≥60% пилотов в exit interviews независимо называют privacy как top-3 reason | Структурированные exit interviews |
| H5 | Digital R&D track не каннибализирует solar pipeline и не размывает фокус Михаила | Track B milestones по `Partnership/Roadmap.md` не отстают; weekly check-in показывает <8h/week founder digital-load после недели 4 | Weekly RACI review (см. §7) |

### 4.2. Falsifiers (что считаем "stop signal")

- **Stop H1:** <3 paying pilots на неделе 8 при ≥40 outbound attempts → продукт не находит pull в выбранном ICP. Decision: либо смена ICP (extra cycle), либо пауза digital track-а.
- **Stop H3:** Marginal cost >50% ARPU на неделе 12 → unit economics не работают при текущей архитектуре. Decision: либо смена price point (≥€99 ARPU), либо смена inference-stack, либо пауза.
- **Stop H5:** Track B slippage > 2 недели по любому Priority-1 gate из `open-gates.md` в течение программы → возврат фокуса на solar, digital track замораживается до закрытия solar gates.

### 4.3. Leading indicators (наблюдаем еженедельно)

- # outbound contacts per week
- # discovery calls completed
- # active pilots
- 7d / 28d active use
- Время от sign-up до первого "ah-ha moment" (первая полезная структурированная knowledge artifact)
- Frontier API spend / active user / week

---

## 5. Архитектурные принципы прототипа

### 5.1. Stack (MVP)

| Слой | Компонент | Обоснование |
|---|---|---|
| **Hosting** | Self-hosted (Hetzner DE/FI) или OVH Iberia | EU data residency, известная инфраструктура, цена |
| **Workspace** | Nextcloud Hub 8+ (Files, Talk, Deck, Office) | Известный нам стек, open-source, EU-friendly, активно развивает AI features |
| **Local inference** | Ollama + Llama 3.1 8B / Mistral 7B (квантованные) | Дешёво, on-premise, достаточно для extraction/quantization, EU AI Act limited-risk |
| **Frontier inference (proxy)** | OpenAI / Anthropic / Mistral La Plateforme через свой gateway с zero-retention | Качество, валидация логики, генерация итоговых артефактов |
| **Knowledge base** | Nextcloud Collectives + custom Wiki schema + vector store (Qdrant) | Structured knowledge artifact = main value anchor (см. §5.2) |
| **Channel integrations (MVP scope)** | Email (IMAP), WhatsApp Business Cloud API, локальный CSV import | Не пытаемся в MVP интегрировать всё; берём 2-3 канала с очевидной ценностью |
| **Auth & access** | Nextcloud native + 2FA | Базовый уровень для пилота |
| **Monitoring** | Plausible / Matomo (privacy-friendly) + structured product telemetry | Чтобы измерять §4.3 leading indicators |

### 5.2. Knowledge base — главная ценностная точка

Критический анализ корректно отмечает: **durable margin живёт не в inference, а в knowledge base**. Inference будет дешеветь дальше, knowledge base — нет.

Поэтому MVP организован вокруг одного артефакта — структурированной "Wikipedia бизнеса" клиента, в которой:

- есть фиксированная **минимальная схема** ("Who we are", "What we sell", "Who buys", "How we deliver", "How we charge", "Open issues") — заполняется в первый день после onboarding;
- каждая запись имеет **источник** (документ, email, разговор) — версионируется;
- каждая запись имеет **claim status** аналогично `claim-register.md` (`working`/`tested`/`confirmed`);
- knowledge base — это **единственный источник правды** для всех AI-генераций (ответы клиентам, маркетинг, посты), и каждый сгенерированный артефакт **ссылается на конкретные knowledge entries**.

Это даёт нам два конкурентных преимущества против Notion AI, Microsoft Viva и generic ChatGPT wrappers: (1) explainability на уровне business reasoning, (2) собственно тот самый "intellectual pleasure of seeing the full picture", который упомянул спикер транскрипта.

### 5.3. Privacy & compliance baseline (с первого дня)

- **DPIA** заполняется ДО первого реального пилота, не после;
- **DPA-шаблон** между WeRa Cloud (controller или joint-controller, зависит от роли) и SME-пилотом — готов до первого контракта;
- **EU AI Act risk classification:** документация того, что мы — `limited risk` (не biometric, не employment, не credit, не critical infrastructure), с подтверждением counsel;
- **Frontier API:** только endpoints с zero-retention / EU residency или enterprise-агрегатор с подписанным DPA (например, через Mistral La Plateforme или Azure OpenAI EU);
- **Local model:** хранится on-premise, не отправляет данные третьим сторонам.

### 5.4. Что **не** строим в MVP

- formal Lean/Coq verification бизнес-логики (критический анализ был прав: переоценено);
- multi-agent orchestration с feedback loops и dispute resolution (post-PMF);
- payment-vouchers, token issuance, любая on-chain логика (Product 2 research-only);
- автоматическое подключение к утилитам и energy-billing (требует отдельных DPA с провайдерами, отдельный pass-through).

---

## 6. Этапы и сроки — 12 недель, 4 спринта × 3 недели

### Sprint 0 (неделя 0, до старта): pre-flight, ~5 дней

- Согласование данного концепта со-основателями (Go/No-Go #0).
- Регистрация placeholder-юрлица или подтверждение, что R&D ведётся как cost-center существующей юрструктуры (см. open question OQ-1, Приложение B).
- Подписание DPIA-шаблона, DPA-шаблона, AI Act limited-risk memo (Алексей + Михаил).
- Подъём окружения: Hetzner-сервер, Nextcloud Hub, Ollama, frontier API ключи.
- Перенос данного документа в `Strategy/Digital-RnD/` (выполнено).

### Sprint 1 (недели 1–3): "Skinny MVP + 3 discovery calls"

- Цель: работающий self-hosted Nextcloud + Ollama + frontier proxy + первая итерация knowledge base schema.
- Подготовка ICP-лонглиста (50+ SME через ассоциации, локальные business networks, Iberian SME accelerators — **без solar pipeline**).
- 10 outbound contacts → 3 discovery calls → 1 design partner candidate.
- Внутренний тест на синтетическом SME-кейсе (например, fake bakery в Lisbon — фейковые документы, email-ы, посты).
- **Go/No-Go #1 на конце Sprint 1:** есть рабочий prototype + есть 1 confirmed design partner. Если оба — продолжаем. Если только один — re-scope.

### Sprint 2 (недели 4–6): "First paying pilot + onboarding rails"

- Закрытие 1-го платящего пилота (€49–€79/мес).
- Построение onboarding flow: 1-day setup, 7-day "first knowledge base sketch", 14-day "first AI-generated artifact".
- Структурированные discovery calls по 5+ дополнительным leads.
- Начало research-only track-а по Product 2: первая итерация `tokenization-routing-memo.md` — список вопросов для corporate/securities counsel.
- Сбор leading indicators (см. §4.3).

### Sprint 3 (недели 7–9): "Scale-test to 3 pilots"

- 3 платящих пилота total, 5–7 active discovery calls.
- Первое измерение H2 (time-to-customer-response reduction): сравнение neделя 1 vs неделя 8 у 1-го пилота.
- Первое измерение H3 (unit economics): фактический marginal cost на 3-х пилотах.
- Closing iteration of `tokenization-routing-memo.md` (research-only track).
- **Go/No-Go #2 на конце Sprint 3:** ≥3 платящих пилота с ARPU ≥€50, продукт активно используется. Если нет — re-scope ICP или price point.

### Sprint 4 (недели 10–12): "5 pilots + decision pack"

- 5 платящих пилотов total.
- Финальное измерение всех 5 гипотез из §4.1.
- Exit interviews со всеми пилотами (H4 driver-analysis).
- Подготовка `decision-pack.md` для со-основателей: рекомендация GO / PAUSE / KILL + апдейт `Strategy/Business-Model/claim-register.md` по digital track.
- **Go/No-Go #3 на конце Sprint 4:** см. §9.

---

## 7. Бюджет и команда

### 7.1. Cash budget (12 недель)

| Статья | Оценка | Комментарий |
|---|---|---|
| Hetzner / OVH hosting (3 мес) | €180 | Один dedicated server + бэкап |
| Frontier API spend (3 мес, prototype + 5 pilots) | €1,200–€2,500 | Зависит от объёма; вшит soft cap €1.5k |
| Domain, email, SSL, monitoring | €120 | |
| Legal — DPIA review, DPA template, AI Act memo | €1,500–€2,500 | Privacy counsel; **отдельно от Miguel** (Miguel — energy/Track B) |
| Tokenization research-only track legal scoping | €1,000–€1,800 | Corporate/securities counsel discovery call + memo review |
| Marketing/outreach (ассоциации, листинги) | €300–€600 | Никаких paid ads на этой стадии |
| Дизайн / контент landing page | €400–€700 | Минимум — статичный landing на собственном поддомене |
| Buffer | €500 | |
| **Total cash** | **€5,200–€8,700** | **Hard cap: €8,000** |

### 7.2. Команда и RACI

| Роль | Owner | Время (часов/неделю) |
|---|---|---|
| Product / R&D lead (IC owner) | Михаил | 12–16 h |
| Architecture / DevOps / data-protection | Алексей | 8–12 h |
| Customer discovery / sales calls / interviews | Михаил | 4–6 h |
| Content / community / outreach | Таня | 4–6 h |
| Legal coordination (privacy + tokenization scoping) | Алексей | 2–3 h |
| Track B / solar (existing, не урезается) | Михаил + Алексей + Miguel | без изменений |

**RACI правило:** еженедельный 30-минутный sync (понедельник). Один shared dashboard. Если digital track начинает съедать более 16 h/неделю у Михаила, программа автоматически переходит в slow-mode, не пауза.

### 7.3. Что НЕ запрашивается

- Найм. До прохождения Go/No-Go #3 в команду никого не берём.
- Внешний фандрейзинг под digital track. Финансирование — из текущего runway.
- Перестановка equity / captable. Digital R&D — это R&D-cost внутри текущей структуры.

---

## 8. Риски и митигации

| # | Риск | Вероятность | Воздействие | Митигация |
|---|---|---|---|---|
| R1 | Founder bandwidth distraction → Track B milestones slip | Высокая | Высокое | Hard cap 16 h/week digital для Михаила; еженедельный sync; falsifier H5 в §4.2 |
| R2 | GDPR/AI Act compliance breach в pilot | Средняя | Очень высокое | DPIA + DPA до 1-го пилота; counsel review до signing |
| R3 | Inference cost surge (frontier API price changes, heavy users) | Средняя | Среднее | Soft cap €500/mes; alerting; quota per pilot |
| R4 | Customer acquisition не работает через предложенные каналы | Высокая | Высокое | Falsifier H1; готовый backup-канал (sectoral associations) к концу Sprint 1 |
| R5 | Nextcloud начинает строить аналогичный SME-layer сам | Низкая в 12 недель, высокая в 18+ мес | Среднее | Architecture-agnostic слой knowledge base; рассмотреть partner-track с Nextcloud GmbH к концу программы |
| R6 | Tokenization research-only track создаёт preempted regulatory liability (даже без customer-facing claims) | Низкая | Высокое | Никаких публикаций, никаких pre-marketing страниц; memo держится в `Strategy/Digital-RnD/research/` private; counsel review до любой внешней коммуникации |
| R7 | Конфликт с инвесторской narrative (Track B как primary) | Средняя | Среднее | Four Boxes discipline: digital track не входит в pitch до Go/No-Go #3 |
| R8 | Несбалансированный equity вклад / напряжение между со-основателями | Средняя | Высокое | RACI зафиксирован до старта; еженедельный check-in на conflict surface; результаты R&D документируются в общем репозитории |

---

## 9. Decision Gates / Go-No-Go

### Gate #0 — co-founder approval (сейчас, до Sprint 0)

**Решение:** одобряем ли мы концепт-программу в текущем виде, бюджет до €8k, формальное разделение от solar track-а.
**Выход:** signed-off версия этого документа в `Strategy/Digital-RnD/`, апдейт `Partnership/Roadmap.md`, апдейт `Strategy/Business-Model/open-gates.md` (P3 row "Separate digital/commercial object" переходит в active).

### Gate #1 — конец Sprint 1 (неделя 3)

**Критерии prosperity (минимум одного из двух — продолжаем; обоих — accelerate):**
- ✅ working prototype self-hosted Nextcloud + Ollama + frontier proxy на синтетическом кейсе;
- ✅ ≥1 confirmed design partner (готовность подписать pilot agreement).

**Stop condition:** оба отсутствуют → пауза, retro, либо kill.

### Gate #2 — конец Sprint 3 (неделя 9)

**Критерии prosperity:**
- ≥3 платящих пилота с ARPU ≥€50/мес;
- average 7d-active-use ≥30% по пилотам.

**Stop condition:** <3 пилота при ≥30 outreach attempts → re-scope ICP или price point; <30% active use → re-design onboarding flow.

### Gate #3 — конец Sprint 4 (неделя 12)

**Критерии для "GO — promote digital to co-equal frame":**
- ≥5 платящих пилотов с ARPU ≥€50/мес;
- ≥40% 28d active use;
- marginal cost ≤35% ARPU;
- ≥60% пилотов в exit interview называют privacy как top-3 reason;
- Track B milestones (`Partnership/Roadmap.md`) НЕ просели более чем на 2 недели.

**Критерии для "PAUSE — hold as optionality":**
- 2-4 платящих пилота; unit economics не подтверждены, но и не опровергнуты.

**Критерии для "KILL — close digital track":**
- <2 платящих пилота при выполненной outreach-квоте;
- марджинальные затраты >50% ARPU;
- Track B серьёзно просел из-за distraction.

**Deliverable Gate #3:** `2026-08-XX-digital-rnd-decision-pack.md` в `Strategy/Digital-RnD/` с рекомендацией и обновлением `claim-register.md`.

---

## 10. Связь с canonical docs и open gates

### 10.1. Какие canonical docs затрагиваются

| Doc | Изменение |
|---|---|
| `Strategy/Business-Model/open-gates.md` | Priority-3 row "Separate digital/commercial object for Nextcloud wedge" переходит в active; добавляется новый owner (Михаил + Алексей) и trigger (конец Sprint 4) |
| `Strategy/Business-Model/claim-register.md` | Добавляется набор `working` claims по digital track: H1–H5 из §4.1 |
| `Strategy/Business-Model/current-business-model.md` | НЕ меняется до Gate #3; digital track — optionality, не часть current model |
| `research/WeRa-Consultant-Frame.md` | Box 2 (Scale architecture) и Box 4 (Vision) **не** меняются; Four Boxes discipline сохраняется |
| `Partnership/Roadmap.md` | Добавляется параллельная R&D-полоса с 4-мя спринтами |
| `Strategy/Legal/regulatory-routing-and-power-tier-matrix.md` | Не меняется. Privacy counsel — отдельный maршрут, не пересекается с energy/credit/securities routes |

### 10.2. Что НЕ меняется

- Investor-facing pitch остаётся `Resilience-driven solar leasing business with sovereign cloud upside` до Gate #3;
- Track B priorities, Miguel agenda, Torres Vedras evidence pack, Iberia Renew Engineering relationship — без изменений;
- Equity / Captable / Partnership Terms — без изменений.

---

## Приложение A — Pilot Customer Profile (ICP)

| Атрибут | Значение |
|---|---|
| География | Portugal continental (Lisboa metro, Centro region); Spain если естественно (контакты Тани/Алексея) |
| Размер | 5–25 сотрудников |
| Отрасли | Локальные услуги (стоматология, ремонт, мастерские), агро/small farm operations, ремесло, малое производство, локальная розница, B2B-сервисы |
| Цифровая зрелость | Уже платит за минимум один из: email-хостинг, веб-сайт, social ads, локальные marketplace ads, CRM, accounting software |
| Месячный digital spend | €100–€800/мес total |
| Анти-критерии | Solar клиент WeRa (исключаем для чистоты эксперимента); компания >50 человек; tech-startups (не наш ICP); компании в регулируемых отраслях с heavy compliance (банки, healthcare) — пока |
| Channels поиска | Industry associations (CCP, IAPMEI partners, sectoral camaras), local business networks, MSP-партнёры, прямая outreach через LinkedIn |
| Discovery hook | "Мы помогаем малому бизнесу превратить весь его цифровой шум в одну живую базу знаний, которая работает на вас, а не на OpenAI" |

---

## Приложение B — Открытые вопросы и owners

| # | Вопрос | Owner | Когда нужно закрыть |
|---|---|---|---|
| OQ-1 | Юридический контейнер для digital R&D — отдельный SPV или cost-center внутри текущей структуры? | Алексей + corporate counsel | до Sprint 0 |
| OQ-2 | Privacy counsel — кого нанимаем для DPIA review и DPA template? | Алексей | до Sprint 1 |
| OQ-3 | Corporate/securities counsel для tokenization research-only — кто? | Михаил | до Sprint 2 |
| OQ-4 | Какие 2 partner-ассоциации мы можем активно использовать для outreach? | Таня + Михаил | Sprint 1, неделя 1 |
| OQ-5 | Edge-only BOM recut (existing open gate в `open-gates.md` P2) — нужно ли координировать с digital track для consistency или они независимы? | Алексей | Sprint 2 |
| OQ-6 | Backup-канал acquisition если associations не сработают | Михаил | Sprint 1, неделя 2 |
| OQ-7 | Какие компоненты Nextcloud Hub мы конфигурируем "из коробки" vs дорабатываем? | Алексей | Sprint 0 |
| OQ-8 | Brand: используем "WeRa Cloud" сразу или временный internal codename для R&D? | Михаил + Таня | до Sprint 1 |

---

## Приложение C — Глоссарий (синхрон с UTS.md)

- **Track B** — `service-fee + operator` baseline; см. `Strategy/Business-Model/current-business-model.md`.
- **BaaS (Business-as-a-Software)** — позиционирующая категория Product 1, отличная от SaaS: продукт становится операционным слоем бизнеса клиента, не просто инструментом.
- **Knowledge base / digital twin** — структурированный артефакт "Wikipedia бизнеса" клиента, главная ценностная точка Product 1.
- **Hybrid local+frontier inference** — архитектурный паттерн: локальная модель делает extraction/quantization приватных данных, frontier API делает finalization/validation.
- **Tokenized Service-Financing** — Product 2, research-only track; механизм share-for-vouchers; **не упоминается в customer-facing материалах** до прохождения corporate/securities counsel.
- **Go/No-Go gates** — формальные decision points (§9). Каждый gate — формальное решение со-основателей.
- **Claim status** — `working` (рабочая гипотеза), `tested` (проверено локально), `confirmed` (внешне валидировано). Аналогично `Strategy/Business-Model/claim-register.md`.

---

## Финальная просьба к со-основателям

Если данный концепт принимается, прошу:

1. **Михаил, Алексей, Таня** — sign-off на §9 Gate #0 в течение недели от даты документа.
2. **Алексей** — поднять список privacy counsel-кандидатов (OQ-2) и проверить OQ-1 с corporate counsel.
3. **Михаил** — закрыть OQ-3 и OQ-8.
4. **Таня** — закрыть OQ-4 (2 industry associations для outreach).
5. После sign-off обновить `Partnership/Roadmap.md` и `Strategy/Business-Model/open-gates.md` (см. §10.1).

Если есть несогласие с любым из §2 принципов (особенно с **independence** от solar pipeline и **research-only** статусом Product 2) — пожалуйста, поднимите это **до** Gate #0. Эти два принципа держат всю логику программы; их компромисс размывает risk-hedge эффект.

---

*Документ хранится в `Strategy/Digital-RnD/`. Обновления — через дополнительные dated документы (`YYYY-MM-DD-...md`), не через перезапись данного файла, чтобы сохранялась traceability решений.*

formal_proof:
  engine: ml-hilbert
  trl_phase: TRL6
  obligation_id: kb.governance.annex_source_sync_strategy_digital_rnd_2026_05_18_concept_note_wera_cloud_rnd
  proof_artifact: kb-governance/formal-proofs/governance-annex-source-sync-strategy-digital-rnd-2026-05-18-concept-note-wera-cloud-rnd.lean
  verification_status: verified
