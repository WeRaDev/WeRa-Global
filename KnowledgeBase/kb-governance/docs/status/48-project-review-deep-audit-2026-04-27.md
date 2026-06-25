---
title: "WeRa Global — PM-ревью проекта"
date: "2026-04-28"
type: "pm-review"
status: "deep-audit-v1"
author: "PM-сессия"
scope: "Strategy & business-model, Legal & regulatory, Operations & roadmap"
based_on:
  - "CLAUDE.md (2026-04-24)"
  - "Strategy/Business-Model/* (canon, 2026-04-22..24)"
  - "Strategy/Legal/* (Track A + B.1/B.2/B.3, 2026-04-23..24)"
  - "research/WeRa-Consultant-Frame.md (2026-04-09)"
  - "research/2026-04-22-strategic-synthesis-memo.md"
  - "Operations/Clients/_pipeline.md, Operations/Investors/_pipeline.md"
  - "Operations/_next.md (2026-04-24)"
  - "Partnership/Terms.md, Partnership/Roadmap.md, Partnership/Roles.md, Partnership/Captable.md"
  - "Log.md (по 2026-04-24 включительно)"
  - "Meetings/2026-04-22-solar-leasing-model.md и более ранние"
purpose: "Дать стороннюю PM-оценку текущего состояния проекта, отделить solid от fragile, перечислить top issues и подготовить почву под Action Plan."
companion: "2026-04-27-action-plan-and-roadmap.md"
---

## Consolidation provenance
- consolidation_actor: `WARP`
- consolidation_source: `/Users/mikhailananyin/Documents/WeRa Global/KB-latest-original/Outputs/PM-Reviews/2026-04-27-project-review.md`
- consolidation_date: `2026-06-22`
- consolidation_status: `canonicalized`


# WeRa Global — PM-ревью проекта (deep audit v1)

> Это диагностический документ. Он не пересобирает стратегию, а оценивает то, что собрано командой к 24 апреля 2026. План действий — в companion-файле `2026-04-27-action-plan-and-roadmap.md`.

---

## 1. Executive verdict

WeRa за последние 10 дней совершила редкий для pre-seed манёвр: команда сама обнаружила, что в одном проекте параллельно жили **три разных бизнеса** (GPU datacenter, solar leasing, installer-network finance) и провела честную операцию object-discrimination. Текущий канон (`Strategy/Business-Model/*` + `Strategy/Legal/*`, 2026-04-22..24) — это уже не «pre-seed месиво», а внутренне непротиворечивая, дисциплинированная сборка под ясный operating object: `solar third-party operator + fixed service fee + edge baseline + installer-channel delivery`.

Сильная сторона проекта сейчас — не пилот и не финмодель, а **качество мышления о собственной бизнес-модели**. UTS, claim-register, executed-vs-designed, regulatory routing matrix, Track A / B.1-B.3 split — это инструменты, которые большинство pre-seed команд не имеют и в seed-стадии.

Слабая сторона — **исполнительный отрыв от этой ясности**:

- единственный executed carrier (Torres Vedras) пока несёт `customer installation with incomplete commercial wrapper`, не grid-connected UPAC-baseline;
- legal-package под Мигеля собран, но не отправлен;
- инвесторский pipeline пустой;
- roadmap в `Partnership/Roadmap.md` — `skeleton` с пустыми датами, при этом он по-прежнему ставит регистрацию КИК на Q2 2026, хотя сама КИК в каноне теперь — `open Track B.3 hypothesis`;
- роли Алексея/Тани формально не зафиксированы;
- `20% savings guaranteed` остаётся externally visible на сайте/в funnel, при том что внутри claim уже понижен до `externally visible but unverified`.

**Главный риск ближайших 4-6 недель** — не стратегический, а операционный: накопленная стратегическая ясность не превращается в исполнение, и качество канона деградирует под давлением fundraising-нетерпения.

**Оценка project health:** 🟡 `yellow-leaning-green`. Зелёная — стратегия, легальная дисциплина, понимание реальности. Жёлтая — исполнение, runway, evidence package, GTM-машина. Красных зон **нет**, но три жёлтых трека (Torres Vedras evidence, counsel turnaround, investor outreach) могут стать красными за 4-8 недель, если не двинуться.

---

## 2. State of project at a glance

| Срез | Где сейчас | Что должно стать к концу 90 дней | Светофор |
|---|---|---|---|
| **Operating object** | Selected baseline зафиксирован: `service-fee + operator first` | Counsel-confirmed contract package + 1 первый repeatable grid-connected install | 🟢 |
| **Executed reality** | 1 technical pilot (Torres Vedras, off-grid, no supplier contract) + 1 client at proposal stage + 1 signed installer | Pilot fact-sheet external-grade + 1-2 commercial contracts с recurring payment | 🟡 |
| **Legal package** | 4 specialist memos + routing matrix + memorialisation draft v1 — не отправлены | Письменные ответы Мигеля по Track A и B.1; declared route на B.2 и B.3 | 🟡 |
| **Capital architecture** | Honest staging: bridge first, debt later. Stage 1 €500k CLA + Stage 2 €2.2M equity — `legacy draft`, не canonical | Canonical инструмент + Stage 1 ask + 5-7 warm investor leads | 🟡 |
| **Financial model** | Y2 на 66% зависит от WiFi Map; €2k/мес vs €263k/кв scaled OpEx — gap | Base case без WiFi Map + lean operating budget на первые 12 мес | 🔴* |
| **GTM** | 2 client рассказа (TV + второй), 1 installer signed, 1 Sintra signal | 3-5 quoted proposals в выбранном subset + 1 разговор с Sintra installer проведён | 🟡 |
| **Team / capacity** | 1 full-time (Миша); Алексей+Таня — формат не зафиксирован | Зафиксированный формат участия; первый делегированный owner на legal/research | 🟡 |
| **Narrative discipline** | Four Boxes введены, UTS работает, но `20% savings guaranteed` всё ещё на внешнем funnel | Внешние материалы прошли UTS-чек; claim либо подтверждён по сегментам, либо ограничен, либо снят | 🟡 |
| **Roadmap** | `skeleton` без дат; КИК на Q2 при том что КИК — Track B.3 hypothesis | Roadmap синхронизирован с canon; legal-gates перед registration-gate | 🔴* |

*🔴 = «не критично-красный, но требует немедленной коррекции, потому что либо вводит в заблуждение наружу, либо нарушает внутреннюю последовательность».

---

## 3. Что у проекта solid (на чём можно опираться)

### 3.1 Object-discrimination как core competency
В период 21–24 апреля команда явно разделила:
- **Объект A** — старый GPU datacenter (Capital Pitch v0.9, €2.175M/юнит, 20× H100);
- **Объект B** — текущий SolarSeed solar leasing (€5–23k/юнит);
- **Объект C** — finance-layer поверх installer network (Frame IV).

Это сделано не общими словами, а через целенаправленный research-такт (Блоки 5A/5B/6/7/8A) и зафиксировано в `2026-04-22-strategic-synthesis-memo.md`. Большинство проектов на этой стадии не доходят до object-discrimination и продолжают пытаться продавать всё сразу. У WeRa теперь есть baseline, явно отделённый от far path.

### 3.2 Term discipline (UTS) и claim register
`Strategy/Business-Model/UTS.md` и `claim-register.md` — это рабочие инструменты, не декорация. Они уже сейчас ловят конкретные ошибки: `owner/operator` bundle, `autoconsumidor` как pan-Iberian термин, `21-25 kW` как operational fact, `regulator` как один адресат. Каждый load-bearing claim имеет статус, носителя evidence, next test и owner. Это редкий уровень собственной дисциплины для pre-seed.

### 3.3 Legal routing matrix
`Strategy/Legal/regulatory-routing-and-power-tier-matrix.md` — это, на мой взгляд, лучший документ в каноне. Он закрыл четыре системных ошибки одновременно: один generic "regulator", смешение PT/ES self-consumption терминов, oral 21-25 kW, и upgrade Torres Vedras в proof of Track B. Он же даёт routing на 4 разных counsel/authority families — это уровень pre-seed legal hygiene, который инвесторы обычно увидят в Series A проектах с in-house counsel.

### 3.4 Executed-vs-designed как защита от self-deception
Жёсткое разделение `executed carrier` vs `designed reality` (`Strategy/Business-Model/executed-vs-designed.md`) уже сейчас не даёт команде выдавать Torres Vedras за commercial proof. Это уберегает от наиболее частой pre-seed ошибки — investor narrative, который рассыпается на due diligence.

### 3.5 Реальные точки опоры
Не все activos одинаково сильны, но **они есть**:
- 1 настоящая физическая установка с TRL5 runtime evidence (telemetry, Nextcloud, инвертор-экспортёр работают);
- 1 подписанный installer partner (Iberia Renew Engineering);
- 1 живой installer-сигнал из Синтры, который воспроизвёл «concierge без leasing» — органическая market validation Frame IV;
- machine-readable knowledge base, KB v1.0 + research dossier 16+ файлов, что ускоряет любую DD-итерацию;
- timing: blackout 28 April 2025 в Иберии создал реальное окно чувствительности к resilience-narrative (хотя shelf-life ограничен);
- partnership terms согласованы (10 пунктов, Lisbon meeting 2026-04-17), доли ясны (Миша 34%, Алексей+Таня 22%, остальное — пулы).

### 3.6 Capital architecture honesty
`Strategy/Business-Model/capital-architecture.md` явно говорит: «debt does not arrive just because the asset is physical», явно разводит `proof stage` / `early growth` / `portfolio stage` / `institutional stage` и отказывается прятать ownership и credit-risk решения за общими словами. Это снижает риск investor-pitch, который на DD ломается.

---

## 4. Что у проекта fragile (load-bearing риски)

### 4.1 Torres Vedras всё ещё ≠ commercial pilot
Это **самый load-bearing узел** проекта. Когда WeRa говорит «у нас есть пилот», слушатель достраивает `running, customer pays, savings measured, contract signed`. Реальность: `customer installation with incomplete commercial wrapper`. Founder-reported verbal agreement, written agreement не подписан, нет supplier-contract baseline (значит bill-vs-bill savings не доказуемы), нет payment trail, нет maintenance ledger как структурированного артефакта.

Команда это понимает (claim register, executed-vs-designed, `Operations/_next.md`), но **execution gap**: задачи 1-4 на этой неделе были `active` со 24 апреля, и я не вижу подтверждения, что они закрылись за прошедшие 3 дня. Если evidence pack не собран до встречи с Мигелем, Track A пойдёт в counsel с тем же founder-memory, что и до canonical reset.

### 4.2 «20% savings guaranteed» — externally visible vs internally suspended
В `WeRa-Global-KB/07-Customers-and-GTM.md` шаг 4 funnel: customer-facing claim. В claim register: `externally visible but still unverified`. В legal-operating-description-draft §9: `not legal-safe as canonical promise`. **Это live exposure**: gap между сайтом/калькулятором и внутренним статусом claim. Любой потенциальный investor / counsel / regulator, который увидит обе версии, прочтёт это как negligence или как marketing-first culture. Дата создания canonical canon — 22 апреля. Прошло 5 дней. Решение должно быть принято либо «убрать с сайта», либо «ограничить условиями», либо «перевести в conditional underwriting calculator output».

### 4.3 Roadmap inconsistency: КИК на Q2 vs КИК как Track B.3 hypothesis
`Partnership/Roadmap.md` (Горизонт 2 — 90 дней): «Зарегистрировать КИК (Португалия или Испания)» к Q2 2026. Это написано 17 апреля, до canonical reset 22-24 апреля. После reset:
- `current-business-model.md` §12: «PT CIC architecture» — `not baseline / open hypothesis`;
- `regulatory-routing-and-power-tier-matrix.md`: CIC/CMVM-вопросы маршрутизируются через corporate/securities/tax counsel, **не Мигеля**, и до этого counsel-feedback CIC нельзя считать selected;
- `miguel-track-b3-corporate-structure-memo.md`: «is PT CIC real and proportionate?» — open question;
- meeting note 2026-04-22: «документы встречи Миши с CVM утеряны».

**Если roadmap не пересинхронизирован, команда движется по дате, которая опирается на гипотезу, признанную внутри проекта непроверенной.** Инвестор, который сравнит Roadmap.md и canon, увидит inconsistency.

### 4.4 WiFi Map dependency 66% Y2 — внутри понижен, в финмодели не пересобран
`current-business-model.md` §8.7 явно: «не должна использоваться как baseline proof of business viability». Но `WeRa-Global-KB/13-Financial-Model.md` всё ещё содержит цифры, опирающиеся на WiFi Map. Open gate `Base case без WiFi Map` — Priority 2, owner Миша, trigger «before investor-facing finance pack». Это значит: сейчас инвестор-материалы делать **нельзя**, но pipeline инвесторов уже задан как H2-задача. Последовательность нарушена: outreach без rebuilt base case = или slide deck с устаревшими цифрами, или slide deck с честным отказом от WiFi Map, но без новых цифр. Оба варианта плохие.

### 4.5 Single-founder bottleneck
`research/WeRa-Consultant-Frame.md` Assumption §5 уже говорил это 9 апреля. С тех пор:
- партнёрские terms согласованы (Алексей+Таня единым субъектом, 22%, 1 год коммитмента);
- Roles.md остаётся `draft, требует уточнения`, формат участия Алексея/Тани прямо помечен как «уточнить»;
- TaskList распределение в `Operations/_next.md`: 5 из 7 задач имеют Михаила в owners; на двух — Engineering team (без имён);
- canonical документы (current-business-model, claim register, executed-vs-designed) указывают `Алексей + Михаил` как co-owners по большинству claims, но executed выгрузка идёт через Мишу.

Это создаёт два параллельных риска: (а) Миша не вытянет одновременно legal-package, pilot evidence, Sintra meeting, financial rebuild и investor outreach; (б) для seed-инвесторов отсутствие зафиксированного key-operator structure снижает investability.

### 4.6 Empty investor pipeline + Stage 1/Stage 2 как `legacy draft`
`Operations/Investors/_pipeline.md` — пустая таблица. Контекстная вставка: «Stage 1: €500k convertible, 8% годовых; Stage 2: €2.2M equity, 12% голосующих; post-money ~€18.3M». Помечено: «Canonical fundraising terms пока не зафиксированы единым документом». Это означает: cap table уже распределяет 22% «Инвесторам» (Captable.md), но кто эти инвесторы, какой инструмент, и какой ask — внутри не выбрано. До того как ask/инструмент определены, любой outreach деградирует в «расскажи мне про свой проект» без conversion.

### 4.7 Frame IV как «scaling path» не имеет evidence beyond conversation
`current-business-model.md` §9.2 описывает Frame IV (installer-network) как «один из самых чистых путей роста current model». Evidence: 1 signed installer (Iberia Renew, no repeatable volume yet) + 1 conversation with Sintra installer (no signed channel). В claim register оба помечены как `partially carried` и `signal only`. Если Frame IV становится investor-facing scaling story, это `selected internally, not yet evidenced`. Sintra meeting in-person ещё не назначена.

### 4.8 BOM / edge-only baseline не пересчитан
`Strategy/Business-Model/current-business-model.md` §4.3: текущий compute share `€1,550.73 / 31%` base config — `legacy figure`, нужен recut. Это load-bearing, потому что: (а) если investor увидит 31% compute в hardware, attached к solar-leasing бизнесу, он спросит «вы — energy company или compute company?», и canonical narrative разваливается; (б) capital-architecture стадии опираются на честный CAPEX per unit. До recut любой quote — это либо завышенная цена для клиента, либо урезание маржи (если clean edge стоит сильно меньше).

### 4.9 «Real-estate tokenization / crisis payment» как далёкая, но не отгороженная гипотеза
`legal-operating-description-draft.md` §15 описывает идею «если customer не может платить, digitise real estate, WeRa получает priority buyout». Помечена как `far path / high-risk legal-financial hypothesis`. Хорошо, что не в baseline. Но она в legal-operating draft — то есть в документе, который пойдёт к Мигелю как контекст. Если Мигель прочтёт §15, реакция counsel может уйти в side-track «эти ребята хотят строить tokenised real-estate engine», и Track A/B turnaround замедлится. Должна быть либо вынесена в отдельный far-path memo, либо зафиксирован явный counsel instruction «do not address §15 in current package».

### 4.10 Resilience narrative shelf-life
Сегодня **28 апреля 2026, ровно один год** с blackout 28 April 2025 в Иберии. Окно «свежей чувствительности» рынка PT/ES — год прошёл, ещё ~12 мес максимум, дальше narrative становится фоновым. Это не fragile в смысле ошибки, это **скоропортящийся актив**. У проекта реалистичное окно использовать resilience как top-of-funnel ~до Q2 2027.

---

## 5. Strategy & business-model — диагностика

### 5.1 Что хорошо
- Canonical operating object описан без двусмысленности: third-party operator + fixed service fee + edge baseline + installer delivery.
- `Selected baseline` явно отделён от `live alternative`, `open legal hypothesis`, `far path`. Это redirects спорные founder-hypotheses (supply-management, tokenised real estate, customer-shareholder conversion, STAK→CIC) в правильное место без подавления.
- Five-layer model (`operating object / legal wrapper / monetization add-ons / long-term moat / investor story`) — реальный инструмент против narrative overload.
- Customer subset выбран по operational признакам, не по типу юрлица: «small controllable sites with simple decision chain» — это правильная разметка для первой 1-10 установок.

### 5.2 Что требует немедленной правки
- **`20% savings guaranteed` claim** — самая срочная strategy-задача (см. §4.2). Решение должно быть принято не позднее этой недели и отражено в funnel/calculator.
- **Edge-only BOM recut** — без него любая investor/counsel/regulator-package реиспользует legacy 31% compute share и подрывает `service-fee + operator first` narrative. Owner: Алексей. Trigger: `before investor/regulator материалы`.
- **Base case без WiFi Map** — owner: Миша. Этот recalc блокирует начало investor-outreach. Без него pipeline невозможно открыть.
- **Customer-as-shareholder mechanism** — в `current-business-model.md` §12 помечен как `not baseline`, но в Block 0 / synthesis memo / меморандумах Миши встречается как elements of investor story. Должно быть либо вынесено в Phase-2 memo (separate corporate counsel track), либо прямо удалено из near-term материалов.

### 5.3 Что недо-выстроено стратегически
- **Phase 1 success criteria** — нет численного определения, что «Phase 1 завершена и можно переходить к compute wedge». Метрика «3-5 repeatable installs in same subset with measured contract performance» (executed-vs-designed §2) задана, но без таргета по дате, conversion, contract value, default rate.
- **Sequence: Phase 1 → Block 6 wedge** — Block 6 (Nextcloud для NGO/cooperatives) описан как `optional secondary wedge`, но триггер запуска не зафиксирован. Когда переходить? После 5 contracts? После signed counsel feedback? После €X выручки?
- **Frame IV как channel** — нет canonical playbook, чем installer-партнёр получает по сделке (lead-fee? rev-share? margin? equipment discount?). До этого playbook любая Sintra-meeting расходится в общие разговоры.

### 5.4 Что хорошо отгорожено, но требует периодического пересмотра
- GPU datacenter thesis (Объект A) — `far path`, поддержано Блоком 8A. Хорошо отгорожено. Триггер revisit: anchor demand + power/site thesis + funding object + operating model — все четыре одновременно. Это правильный фильтр.
- Mini-PC marketplace (`~€1000 → €100-200/мес`) — закрыто Блоком 5A, в `current-business-model.md` явно `rejected`. Хорошо.
- Token / governance layer — Box 3, не открывает разговор. Хорошо.

---

## 6. Legal & regulatory — диагностика

### 6.1 Что хорошо
- Multi-track architecture (A + B.1/B.2/B.3) — это правильная декомпозиция. Counsel получает фокусированные вопросы, не blended memo.
- Power/grid-status matrix введена и явно дисквалифицирует oral `21-25 kW` как operational fact.
- Selected title posture явно описана как `selected working baseline for testing`, не `clean baseline`.
- Pre-counsel signed memorialisation draft v1 для Torres Vedras уже собран — это снимает риск, что counsel получит «у нас в пилоте всё устно».

### 6.2 Что требует немедленной правки
- **Counsel package не отправлен.** Все 4 specialist memos + matrix + memorialisation draft существуют. Гипотеза, что они отправляются «после Torres Vedras evidence pack», правильная для Track A, но Track B.1/B.2/B.3 могут идти параллельно — они касаются prospective baseline, не пилота. Sequence можно ускорить.
- **Real-estate tokenization §15 в legal-operating-description-draft.md** — должно быть либо вынесено в отдельный sealed far-path memo, либо помечено явным counsel instruction «не отвечать в этом раунде» (см. §4.9).
- **Customer→shareholder conversion** — Track B.3 §14.3 helpfully разводит это как `far path`, но в reality часть founder-narrative до сих пор тащит механизм в near-term конверсии. Нужен внутренний явный freeze на эту тему до B.3 counsel ответа.

### 6.3 Что недо-выстроено
- **Конкретная identity Мигеля** — в Operations/Legal/_index стоит как `Михаил + Miguel + Алексей`, но самого договора с Мигелем (engagement letter, scope, retainer, conflict-of-interest declaration) в каноне не видно. Если Мигель — `friend lawyer`, это ускоряет первый ответ, но удлиняет formal opinion turnaround. Если он — `engaged counsel`, должен быть retainer и сроки. Это load-bearing для timeline.
- **CMVM contact reset** — meeting note 2026-04-22: «контакты в CVM сохранились, документы утеряны». Нужно отдельно решить, идём ли к CMVM повторно после B.3 counsel ответа, и если да — кем (Миша → CMVM напрямую vs counsel → CMVM via formal route).
- **Insurance / liability stack** — `current-business-model.md` §6.8: open gating issue. До первого реального grid-connected install это не критично, но без insurance counsel turn первая sales conversation с risk-aware fermer будет ломаться.
- **Spain track parallelism** — `2026-04-20-spain-legal-structure-wera.md` есть, в claim register помечено `research-supported, not counsel-confirmed`. Без хотя бы одного звонка с Spanish energy counsel сравнение PT vs ES остаётся desk-thesis, и Roadmap «КИК Португалия или Испания» — гадание.

### 6.4 Самая большая legal-задача месяца
Получить **письменный** (не устный) Мигеля feedback по двум вещам одновременно:
1. **Track A:** что мы можем подписать сейчас по Torres Vedras, не ухудшив правовой позиции. Цель — превратить founder-memory в written carrier.
2. **Track B.1:** какой именно contract type в PT (`prestação de serviços` vs `locação` vs `contrato misto/atípico`) безопасен для selected baseline.

Без этих двух ответов B.2 (consumer credit) и B.3 (corporate/securities/tax) идут вторым эшелоном.

---

## 7. Operations & roadmap — диагностика

### 7.1 Что хорошо
- `Operations/_next.md` — реальный недельный приоритетный список из 7 пунктов. Это правильная гигиена.
- `Operations/Legal/_index.md` ведёт активные/подписанные документы.
- `Log.md` дисциплинирован: одна запись = одно решение, не редактируется. Это даёт чистый аудит-trail.
- Meeting hygiene: YAML frontmatter, резюме, задачи, транскрипт. Index meetings table компактен.
- Эскалация документов: `research/` (dated) → `Strategy/` (canonical) разделение работает.

### 7.2 Что fragile в operations
- **Pipeline клиентов**: 1 pilot + 1 «(второй клиент)» с пустыми полями. Owner — Михаил, дедлайнов нет. Это не pipeline, это log of two.
- **Pipeline инвесторов**: пустая таблица. Watchlist пустой. Это значит outbound investor activity = 0, при том что Stage 1 €500k convertible обозначен как инструмент.
- **Suppliers / Iberia Renew Engineering**: подписан, но я не вижу repeatable origination workflow или Master Service Agreement, который определял бы margin split, lead-routing, exclusivity.
- **Roles.md**: формат участия Алексея/Тани — `уточнить формат`. На дату 27 апреля прошло 10 дней с Lisbon meeting, и это не закрыто.
- **`Outputs/Pitches/`, `Outputs/Proposals/`, `Outputs/Templates/`** — все три имеют только `_index.md`. Нет ни одного готового pitch deck или proposal template. Это значит: даже если завтра появится investor lead или client lead, response-time будет 5-7 дней на создание материалов.

### 7.3 Roadmap-проблема
`Partnership/Roadmap.md` помечен как `Скелет. Требует выгрузки из головы Миши и отдельной сессии по приоритетам.` Это честно, но операционно — это значит:
- ни один из 5 пунктов H1 (30 дней) не имеет дедлайна;
- 4 из 5 пунктов H2 (90 дней) без дедлайна;
- H3 (6-12 мес) — пустой;
- success criteria определены неформально и не измеримо.

И **противоречие с canon** (см. §4.3): КИК на Q2 vs КИК как Track B.3 open hypothesis. Это main reason Roadmap нужно перезалить — это сделано в companion-файле `2026-04-27-action-plan-and-roadmap.md`.

### 7.4 Cadence
Не вижу зафиксированного weekly cadence (например, «вт 10:00 — командный звонок», «пт — обновление _next.md»). Учитывая, что из трёх participants полноценно full-time только один, cadence — главный инструмент компенсации single-founder bottleneck.

---

## 8. Cross-cutting themes

### 8.1 Narrative discipline
Four Boxes (`Operating business / Scale architecture / Governance & legal / Vision`) приняты, есть в Consultant Frame и подтверждены в meetings. Hand check: проверил 3 документа на violation:
- `current-business-model.md` — Box 1 ясно отделён, Box 2 (compute wedge) явно `optional`, Box 3 (CIC/STAK) явно `open hypothesis`, Box 4 (network state) отсутствует. ✅
- `legal-operating-description-draft.md` — Box 1 + Box 3 через Track B.3, Box 4 (real-estate tokenization §15) присутствует как `far path`, но физически в том же файле, что и Box 1 — это нарушение фактической изоляции, даже если логически она продекларирована (см. §4.9, 6.2). ⚠️
- `2026-04-22-strategic-synthesis-memo.md` — все четыре Boxes присутствуют, но явно maркированы. ✅

Совет: применять Four Boxes не только к narrative, но и к **физической компоновке файлов**. Box 4 не должен жить в том же `.md`, что и Box 1, даже если внутри стоит метка `far path`.

### 8.2 Evidence hygiene
`MEMORY` / `FACT` / `ESTIMATE` / `UNKNOWN` маркировка — отличная практика, видна в `SolarSeed.pilot.tv.md` и `torres-vedras-pilot-questionnaire.md`. Я бы расширил эту дисциплину на:
- `Operations/Clients/_pipeline.md` — статусы клиентов;
- `Operations/Investors/_pipeline.md` — статусы инвесторов;
- любые цифры, которые цитируются наружу (CAPEX per unit, LTV, monthly payment, Y1 target).

### 8.3 Founder dependency vs delegation
Дедлайны пролетели. Список «Roles.md → требует уточнения» от 17 апреля. Без явного scope для Алексея и Тани вся выгрузка research-продуктов, claim-register maintenance, legal-package preparation сидит на одном Алексее. Это работало до 24 апреля (массив документов вышел отличный), но не масштабируется на ближайшие 90 дней, когда нужны параллельно: pilot evidence, counsel turnaround, financial rebuild, investor pipeline, Sintra meeting, second client close, Block 6 interviews.

### 8.4 Speed vs depth tradeoff
Проект последние 10 дней работал в режиме `depth-first` (canonical reset, four-track legal split, claim register). Это правильно. Но команда сейчас рискует продолжить depth-first до бесконечности, потому что каждая итерация открывает новые open gates. Открытых gates сейчас **15** (Priority 1 = 7, Priority 2 = 5, Priority 3 = 3). Без явного gate-prioritization и параллельного включения execution команда легко потратит ещё 3-4 недели на canon без single new external evidence.

---

## 9. Top-10 issues, ranked

| # | Issue | Domain | Impact если не закрыть в 30 дней | Effort | Owner | Trigger |
|---|---|---|---|---|---|---|
| 1 | Torres Vedras external-grade evidence pack не собран | Strategy + Legal | Track A counsel goes in с founder-memory; investor narrative остаётся «1 pilot, no proof» | M | Михаил + Алексей | до Miguel A-meeting |
| 2 | `20% savings guaranteed` остаётся externally visible while internally `unverified` | Strategy + Legal | Регулятор/counsel/investor видит inconsistency; consumer-credit risk в B.2 ухудшается | S | Алексей | до next live proposal |
| 3 | Roadmap inconsistency (КИК на Q2 vs Track B.3 hypothesis) | Operations | Внешние читатели Roadmap.md видят inconsistency; команда движется по нерабочей дате | S | Алексей | now |
| 4 | Counsel package не отправлен, Мигель engagement не формализован | Legal | Каждая неделя задержки = неделя без legal-baseline; Sintra meeting и second client close становятся рисковыми без legal-cover | M | Михаил + Алексей | this week |
| 5 | Empty investor pipeline + canonical instrument не выбран | Operations + Capital | Любой outreach деградирует; runway clock работает | M | Михаил | в 30 дней |
| 6 | Base case без WiFi Map не пересобран | Capital | Investor materials делать нельзя; H2-задача «pipeline инвесторов» заблокирована | M | Михаил | до investor-pack |
| 7 | Single-founder bottleneck + Roles.md не закрыт | Team | Любая параллельная задача отстаёт; investability снижена | S | Михаил + Алексей + Таня | в 14 дней |
| 8 | Edge-only BOM recut не сделан | Strategy | Investor / regulator / counsel читают legacy 31% compute share | M | Алексей | до investor/regulator pack |
| 9 | Frame IV evidence beyond conversation | Strategy + GTM | Sintra meeting не назначена; installer-network claim в narrative выше evidence | S | Михаил | в 14 дней |
| 10 | Real-estate tokenization §15 в legal-operating-description | Legal | Counsel reaction может уйти в side-track; turnaround замедлится | S | Алексей | до отправки package Мигелю |

> Effort: S = ≤1 day focused work, M = 2-5 days, L = >1 week.

> Action plan по каждому пункту — в companion-файле `2026-04-27-action-plan-and-roadmap.md`.

---

## 10. Что я бы НЕ делал в ближайшие 30 дней

Анти-список не менее важен, чем приоритеты. Эти вещи кажутся важными, но в текущей раскладке — distraction:

- **Не открывать investor outreach** до того, как (а) base case без WiFi Map пересобран и (б) Stage 1 instrument canonically выбран. Иначе деградирует voice.
- **Не пытаться закрыть второго клиента в крупной конфигурации** (Average Config, €22k+ CAPEX) до counsel B.1 ответа. Risk: первый репитабельный контракт окажется не в clean tier.
- **Не возвращать compute/Nextcloud Block 6 wedge в активную работу** до того, как Phase 1 выдал хотя бы 1-2 commercial install. Block 6 интервью (5-7 NGO/coop) — да, можно начать; полноценный Block 6 product launch — нет.
- **Не тратить время на NL STAK / customer-shareholder conversion / real-estate tokenization** в любых внешних материалах до Track B.3 counsel ответа.
- **Не регистрировать КИК / SL / любую фунд-структуру** до Track B.3 ответа. Это противоречит текущему roadmap, но соответствует canon.
- **Не тратить недели на canonical fundraising scenarios doc** до того, как Stage 1 instrument выбран. Сценариев у проекта уже хватает; нужен один canonical инструмент.
- **Не апгрейдить current-business-model.md** в ближайшие 14 дней. Канон только-только зафиксирован 24 апреля, ему нужно 10-14 дней «отстоя» при работе. Иначе команда утонет в re-canonical итерациях.

---

## 11. Финальный взгляд PM

Проект не находится в кризисе. Проект находится в **окне самой высокой leverage за всё своё существование**: стратегическая ясность есть, легальная дисциплина есть, реальные точки опоры есть, timing работает. Если в ближайшие 30 дней закрыть Torres Vedras evidence + Track A&B.1 counsel ответ + base case rebuild + roles delegation, то к концу 90 дней WeRa может прийти к 3-5 quoted proposals в одном subset, 1-2 commercial recurring contracts, рабочему Stage 1 instrument и небольшому, но реальному investor warm-list.

Если же команда продолжит совершенствовать canon без параллельного включения execution, в Q3 2026 проект придёт в то же место, где находится сейчас, только с уставшей командой и износившимся resilience-narrative.

Главная задача PM-функции на этой стадии — **охранять баланс между depth и speed**. Canon работает только тогда, когда наружу выходят evidence-grade артефакты. Сейчас баланс смещён в depth. План действий в companion-файле направлен на короткую коррекцию.

---

*Companion: `2026-04-27-action-plan-and-roadmap.md` — приоритеты на 7/30/90 дней, RACI, decision triggers, обновлённая roadmap-замена для `Partnership/Roadmap.md`.*

formal_proof:
  engine: ml-hilbert
  trl_phase: TRL6
  obligation_id: kb.governance.status_48_project_review_deep_audit_2026_04_27
  proof_artifact: kb-governance/formal-proofs/governance-status-48-project-review-deep-audit-2026-04-27.lean
  verification_status: verified
