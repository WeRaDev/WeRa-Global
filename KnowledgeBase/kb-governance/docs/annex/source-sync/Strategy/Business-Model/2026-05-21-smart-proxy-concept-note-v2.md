---
title: "WeRa — Smart Proxy Concept Note v2.1 (CIC + CELL Architecture, Complementary to Working Note v2)"
date: "2026-05-21"
type: "concept-note"
status: "selected-vehicle-pending-counsel-confirmation"
purpose: "Описать Smart Proxy как операционный носитель каждой CELL-SPV под WeRa CIC (Collective Investment Company) — selected legal architecture per Miguel guidance. Этот документ — complementary к Working Note v2 (2026-05-21-working-note-v2-anti-crisis-strategy.md), где центральная стратегия — digital transformation consultancy as anti-crisis core, а Smart Proxy = operational vehicle, в который consulting funnel конвертирует customer relationship на длинном горизонте."
authors:
  - "Михаил (CEO, тезисы)"
  - "AI-сессия (синтез, fact-check, CIC+CELL architecture integration)"
reviewers:
  - "Алексей"
  - "Таня"
version_history:
  - "v1 (2026-05-19): первоначальная Smart Proxy concept от Perplexity AI на базе voice working note. SPV-per-client architecture."
  - "v2.0 (2026-05-21): synthesis с Working Note v1 fact-check. Track B.3-gated replacement candidate. Phase 1 / Phase 2 gating discipline."
  - "v2.1 (2026-05-21): CIC + CELL architecture от Miguel принята как selected legal scaffolding. ECSP €5M crowdfunding rail intgrated. Three-pillar umbrella reference добавлен. Smart Proxy переqualified из replacement-candidate в operational vehicle per cell."
reality_discipline: "designed reality vs executed reality preserved"
not_legal_advice: true
parent_document: "Strategy/Business-Model/2026-05-21-working-note-v2-anti-crisis-strategy.md"
based_on:
  - "uploads/WeRa Global — Working Note Fact-Check, Validation & Critical Analysis.md"
  - "uploads/WeRa_Smart_Proxy_Concept_Note_v1.md"
  - "Strategy/Business-Model/2026-05-21-working-note-v2-anti-crisis-strategy.md"
  - "Strategy/Business-Model/current-business-model.md"
  - "Strategy/Business-Model/open-gates.md"
  - "Strategy/Business-Model/claim-register.md"
  - "Strategy/Legal/regulatory-routing-and-power-tier-matrix.md"
  - "Strategy/Legal/miguel-track-b3-corporate-structure-memo.md"
  - "Strategy/Legal/miguel-track-b2-consumer-credit-memo.md"
  - "research/WeRa-Consultant-Frame.md"
external_foundations:
  - "Protopia Garden, AI-Native NGO Concept v2 (April 2026)"
  - "AI-Native Playbook (Gerstep, 2026): The Compounding Firm, Software Factories, Build Knowledge Not Systems"
  - "Bergolla, Seif, Eken — Kleros (Stanford / Ohio State JDR, 2022)"
  - "Schöning & Kruse — Compliance of AI Systems (arxiv 2503.05571, 2025) — Article 10 II AI Act для edge devices"
  - "EU Regulation 2020/1503 — European Crowdfunding Service Providers (ECSP), €5M threshold"
  - "Lei 16/2015 + DL 27/2023 — Regime Geral dos Organismos de Investimento Colectivo (RGOIC), PT compartment structure"
---

## Consolidation provenance
- consolidation_actor: `WARP`
- consolidation_source: `/Users/mikhailananyin/Documents/WeRa Global/KB-latest-original/Strategy/Business-Model/2026-05-21-smart-proxy-concept-note-v2.md`
- consolidation_date: `2026-06-22`
- consolidation_status: `canonicalized`


# Smart Proxy Concept Note v2.1 — CIC + CELL Architecture, Complementary to Working Note v2

> **TL;DR (v2.1).** Smart Proxy — это **операционный носитель каждой CELL-SPV в составе WeRa Collective Investment Company (CIC)**, как предложил Miguel. CELL = segregated compartment под единым CMVM-authorized CIC wrapper. Один CIC + N CELLs ≠ N independent SPVs: дramatically снижает административные, аудиторские и юридические расходы. Каждый CELL обслуживает customer cluster через DT-consultancy-driven onboarding → Nextcloud / WERA Cloud subscription → opportunistic solar + edge deployment, и может привлечь до **€5M через ECSP-licensed crowdfunding platform** (EU Regulation 2020/1503). Это закрывает customer-as-shareholder gate из v1 как executable mechanism per cell, не abstract far-path.
>
> **Где этот документ находится в архитектуре.** Working Note v2 — стратегическое целое (anti-crisis solution + DT consultancy as core + three-pillar umbrella). Этот концепт-нота — operational vehicle layer одного из трёх pillars (Pillar B — for-profit CIC). См. Working Note v2 §4.2 для overall framing.
>
> **Решения, которые нужны от сооснователей** — переработаны в Working Note v2 §9 (Decisions 1-6). Этот документ выполняет Decision 3 (ECSP rail) operationally.

---

## 1. Чем эта нота не является

Чтобы убрать риск смешения слоёв в самом начале:

- это **не** замена `Strategy/Business-Model/current-business-model.md`;
- это **не** утверждённая стратегия — это `concept note` для co-founder review;
- это **не** investor-facing документ; формулировки здесь internal-only до решения сооснователей;
- это **не** legal opinion; все юридические формулировки сохраняют `open hypothesis` статус из существующего канона.

---

## 2. Что обнажает Working Note (критический разбор и дополнение)

Working Note содержит две части: стенограмма + fact-check 11 тезисов. Fact-check полезен, но **неполон в одном измерении**: он валидирует тезисы по отдельности, но не оценивает их **совместимость с уже выбранным WeRa baseline**. Ниже завершение review с учётом существующего канона и находок Smart Proxy v1.

### 2.1 Подтверждаемые и сильные тезисы Working Note

| Тезис | Статус fact-check | Reading через канон WeRa |
|---|---|---|
| 95% AI-пилотов в enterprise не дают P&L impact (MIT NANDA, PwC 56% «nothing») | `strongly validated` | Прямая market evidence для consulting + digital transformation funnel. Совместимо с §11.1 current-business-model (managed local workspace demand for NGO/SME). |
| PT solar market растёт (1.77 GW в 2024, target 20.8 GW к 2030, modules USD 0.10-0.12/W) | `strongly validated` | Совместимо с §3.1 baseline. Подтверждает timing, но **не закрывает grid/licensing bottleneck** (substation upgrade lag до 18 мес). |
| Family offices сдвигаются к direct PE / impact / long-duration assets (Deloitte 2025) | `accurate` | Совместимо с investor-narrative, но family offices требуют 2-5 лет operating history — у нас этого нет. |
| Edge AI / local inference растёт (30%+ новых AI-серверов 2025 в edge, Jetson Orin Nano за $249 тянет 7-13B) | `validated` | Совместимо с обязательным edge layer (§4.3 canon). Не делает compute marketplace. |
| Tokenisation RWA — emerging, $14B+ on-chain к концу 2024 | `validated but high-complexity` | Совместимо с far-path. **Не** даёт права использовать токенизацию как near-term revenue engine. |
| Design Thinking + psychotherapy hybrid — конструктивная синтеза | `conceptually grounded` | Margin €100/час реалистичен, но требует Ordem dos Psicólogos compliance check. |

### 2.2 Тезисы Working Note, требующие коррекции перед любым внешним использованием

| Тезис в записи | Корректный fact | Действие |
|---|---|---|
| «JP Morgan Jr. создал trust organization» | J.P. Morgan **Sr.** (1837-1913), Panic of 1907, U.S. Steel 1901 | Заменить во всех будущих материалах. JP Morgan Jr. (Jack Morgan, 1867-1943) известен прежде всего как сын — не основатель trust-эпохи. |
| «BlackRock — three vehicle closed loop ownership» | Inaccurate. BLK — публичная компания на NYSE. Vanguard 6.9%, KIA 5.1%, BlackRock Advisors LLC 5.1%. Self-referential petlja minor. Closed-loop архитектура характерна для **Exor, Berkshire Hathaway, family holdings** — не BlackRock. | Закрытый shareholder loop остаётся валидной **design goal** для нашей структуры, но атрибуция «как у BlackRock» неверна. Если структура нужна — её надо проектировать самостоятельно через Track B.3, не через копирование. |
| «BlackRock scales inference across businesses» (Fink на WEF 2026) | Partially accurate. Fink на WEF 2026 говорил про **AI-driven wealth inequality**. BlackRock реально **скупает инфраструктуру, на которой работает inference**: GIP $12.5B, HPS $12B, Preqin $3.2B, Aligned Data Centers ~$40B (Oct 2025), потенциально AES $38B. | Переформулировать: «BlackRock накапливает energy + compute infrastructure layer». Это **ближе к нашей логике**, чем оригинальная формулировка про inference-в-портфельных-компаниях. |
| Network state как near-term legal form | По Balaji Srinivasan-у концепция корректна, но **ни одно network state до сих пор не получило diplomatic recognition**. | Держать network state как aspirational identity (Box 4 по Consultant Frame), не как Box 1 / Box 2. Это **уже зафиксированное правило** Four Boxes — Working Note это правило нарушает. |
| «Минимум 20% дешевле» как customer-facing claim | Уже флагнут в `current-business-model.md §1.3` и в `open-gates.md` как live external claim outrunning evidence. Smart Proxy v1 это правило **повторяет**: €80 → €62/мес = 22% savings — то же необоснованное обещание, переписанное на новый wrapper. | Не использовать в Smart Proxy materials до segment-level verification. |

### 2.3 Дополнения к fact-check, которые Working Note пропустил

Working Note fact-check не проверил два load-bearing claim, которые критически важны для Smart Proxy:

**(a) «Company registered at client's premises» (Smart Proxy v1 §1)** — Working Note это не обсуждает, но это центральная архитектурная гипотеза Smart Proxy. Открытые вопросы:

- registered office at private residential address в PT — допустимо (с согласия собственника / арендатора), но создаёт **substance-over-form risk** при N SPV per N клиентов;
- audit / accounting / contabilista-cost для каждой SPV ≈ €1.5-3k/год минимум — это **сжирает margin €12-14/мес** уже на масштабе ~20+ клиентов;
- **beneficial ownership transparency** (PT registo central): N SPV = N filings;
- риск что налоговая classifies SPV-cluster как `single economic activity through artificial fragmentation`.

**(b) «Customers buy 1 share/month → become minority shareholders» (Smart Proxy v1 §Revenue Streams)** — Working Note валидирует RWA tokenisation в общем, но не проверяет **PT-specific securities trigger**:

- продажа shares неограниченному кругу клиентов = **public offering trigger** под CMVM rules, кроме case с private-placement exemption (<150 non-qualified investors, no advertising);
- даже €1/мес × 1000 клиентов = клас­сический **collective investment characteristic** под `Lei 16/2015` и `RJOIC`;
- это **точно тот вопрос**, который вынесен в `miguel-track-b3-corporate-structure-memo.md` §4.5 (questions 22-25) и помечен как `far path / separate counsel track`.

### 2.4 Что Working Note подсветил особенно сильно (priority repetitions)

Из Part III WN, multi-repeat themes (≥3 повторений) — в порядке стратегического веса для синтеза:

1. **«Survive the crisis» (5+)** + **«Anti-crisis pill» (6+)** → это primary mission frame, должен жить в Box 1 + Box 4 по Four Boxes, не подменять Box 1 одной только Vision.
2. **«Scale inference» (4+)** → mechanism, не product. В нашем контексте = on-premise edge stack + curated AI agent layer + data-room. Smart Proxy v1 даёт этому конкретное место (§Cost Model + §Equipment Flow).
3. **«AI native organization» (4)** → operating design principle. Не блокируется ни одним из counsel tracks. Может быть запущено сейчас без legal gating.
4. **«Social capital» (3)** → differentiator vs BlackRock-extraction model. Совместимо с Fink-овской критикой неравенства от WEF 2026 (его собственная risk-frame).
5. **«Tokenization mechanism» (3)** → most legally complex; остаётся в far-path.
6. **«Confidence» (3)** → execution posture; полезно, но signals credibility gap, если повторяется чаще, чем подтверждается evidence.

---

## 3. Что добавляет Smart Proxy Concept Note v1 (находки и оценка)

Smart Proxy v1 — это **первая попытка дать operational vehicle тезисам Working Note**. Что он реально решает и что — нет.

### 3.1 Сильные стороны Smart Proxy v1

| Элемент | Почему важен |
|---|---|
| **Fixed subscription, не €/kWh** | Совместимо с canonical `fixed service fee` label из `current-business-model.md §10.5`. Уходит от disguised retail electricity sale. |
| **On-premise / edge data processing** | Совместимо с §4.3 (edge device = baseline) и снимает GDPR-Article 25 / EU Cloud Act-side claim cleanly. |
| **Унифицирует energy + data + services под одним wrapper** | Решает проблему «3 разных бизнеса» Working Note (solar ops / consulting / digital transformation): один SPV держит все три revenue streams. |
| **Smart Proxy framing = реализация `hosting frame` гипотезы** | Это **самое важное открытие синтеза**: Smart Proxy = операционная инстанциация уже пре-флагнутой в `regulatory-routing-and-power-tier-matrix.md §1A` `hosting characterisation`. Если PT counsel подтвердит hosting characterisation, Smart Proxy получает legal scaffolding. Если опровергнет — Smart Proxy в текущем виде падает. |
| **Customer satisfaction token + share subscription как loyalty/governance gradient** | Конкретизирует абстрактный customer-as-shareholder из Working Note. |

### 3.2 Слабые места Smart Proxy v1 (то, что он пропускает или решает плохо)

| Проблема | Канонический комментарий |
|---|---|
| **Umbrella owns equipment → intra-group lease to SPV** | Это **возврат equipment ownership на WeRa-side** через косвенный путь — variant #2 из `current-business-model.md §10.2` (project SPV owns asset). Workable scaling variant, но **не** selected baseline. Триггерит fund/securities/tax/collateral вопросы + усиливает consumer-credit risk (Track B.2). |
| **«€1/month share subscription»** | Public offering trigger под CMVM — см. §2.3(b). До Track B.3 counsel feedback это **не** должно выходить за пределы internal notes. |
| **«22% savings»** | Повторяет уже-флагнутый `20% savings guaranteed` claim. См. `claim-register.md` и `open-gates.md` Priority 1 row. |
| **Google Workspace proxy / cloning** | Прямой риск нарушения Google ToS. Open-source substitute (Nextcloud, Mailcow, OnlyOffice, Collabora) — уже в canon (`current-business-model.md §11.1`). Google-proxy идею **снять** из Smart Proxy v2. |
| **Не закрывает Torres Vedras evidence boundary** | Smart Proxy v1 ссылается на Torres Vedras pilot, но Torres Vedras `does not prove` grid-connected UPAC / final-consumer / fixed-service-fee Track B. См. `current-business-model.md §7.1`. Smart Proxy v2 не имеет права наследовать «proof» от Torres Vedras. |
| **Не учитывает SPV-per-client cost stack** | Audit / contabilista / banking / KYC per SPV ≈ €1.5-3k/год. На margin €12-14/мес/клиент SPV окупается только после ~10-15 клиентов **per SPV**. Это противоречит идее «one SPV per client cluster». Нужна явная политика кластеризации. |
| **Не учитывает default / repossession / insurance** | Уже Priority 1 gate в `open-gates.md`. Smart Proxy v1 этот узел не упоминает. |
| **Shelly meters в собственности SPV → CNPD route** | Smart Proxy v1 говорит «GDPR compliant», но не указывает controller/processor роль, retention, consent mechanism. См. `regulatory-routing-and-power-tier-matrix.md §1` — privacy/CNPD route. |
| **`Hosting frame` characterisation остаётся open hypothesis** | Smart Proxy v1 строит весь legal scaffold на допущении, что hosting framing «работает». В каноне это `open characterisation hypothesis`, не подтверждённый legal fact. |

---

## 4. Reconciled object — что именно мы рассматриваем (v2.1)

Smart Proxy в v2.1 описывается так:

> **Каждый CELL — это segregated compartment в WeRa CIC (PT Collective Investment Company под `RGOIC`, Lei 16/2015 + DL 27/2023). CELL обслуживает customer cluster (3-20 клиентов) как digital-transformation hosting company on-premises: предоставляет Nextcloud / WERA Cloud private workspace, AI-instruction orchestration, energy + data monitoring через edge stack, opportunistic solar deployment через installer partner channel. Customer = final consumer of energy and data; CELL = service provider; CIC = collective investment vehicle holding equipment and asset titles; Foundation = governance overlay (см. Working Note v2 Pillar C). Capital rail per CELL — ECSP-platform crowdfunding до €5M / 12 months (EU Regulation 2020/1503). Customer-as-shareholder реализуется через periodic equity tranches, не continuous €1/мес subscription.**

### 4.1 Phase separation discipline (v2.1 update)

Phase 1 / Phase 2 / Phase 3 gating сохраняется, но содержание уточнено:

| Phase | Что включает | Gating conditions |
|---|---|---|
| **Phase 0 — Pre-CELL (current quarter)** | DT consultancy L1-L3 (см. Working Note v2 §3.3) запускается через co-founders. Zero CAPEX, zero CIC, zero CELL. Cash engine + customer development. | Not blocked by anything except corporate office setup |
| **Phase 1 — First CELL stand-up** | One CELL registered under CIC compartment. 3-10 customers from consulting funnel converted to DT software subscription (L4). On-premise edge stack at first 1-3 customer sites. Service-fee wrapper, no `€/kWh`. ECSP licensed platform onboarded but **not yet first round**. | Requires: B.1 + B.3 + tax + privacy counsel feedback closure. Foundation legal form decision can be deferred to Phase 2. |
| **Phase 2 — First crowdfunding round + Smart Proxy deployment** | First ECSP-platform round for CELL-01 (target €100-500k as sub-scale validation of channel). First solar + edge deployment under selected baseline (`service fee + operator-light`, equipment title held by CELL as project-SPV equivalent). Customer-shareholder onboarding. | Requires: B.2 consumer-credit closure; ECSP platform legal agreement signed; Phase 1 operating evidence pack assembled. |
| **Phase 3 — Multi-cell anchor node** | 5-10 active CELLs under CIC. Cross-cell knowledge reuse (shared skill library, instruction templates, hook chains). Cumulative customer-shareholder base >100. Foundation legal form registered. | Requires: Phase 2 operating evidence; second CELL crowdfunding closure; PT/ES jurisdiction choice if expanding. |

**Working rule:** Phase 0 не требует ничего сверх обычной business setup. Phase 1 — структура без crowdfunding. Phase 2 — первый crowdfunding round. Phase 3 — scale validation.

---

## 4A. CIC + CELL + ECSP Architecture (selected legal scaffolding per Miguel)

Этот раздел — **новое содержание v2.1**, заменяющее spekulative "umbrella → SPV intra-group lease" формулировку из v1.

### 4A.1 Legal anchor

**WeRa Global CIC** = Portuguese Collective Investment Company под `Regime Geral dos Organismos de Investimento Colectivo` (`RGOIC`, Lei 16/2015 + Decreto-Lei 27/2023). CIC может быть структурирована как **collective investment vehicle with compartments** (`fundo / sociedade de investimento por compartimentos`), где каждый compartment — segregated sub-fund.

**Применимая legal form (open hypothesis pending Track B.3 counsel):** `Sociedade de Investimento Colectivo de Capital Variável` (SICAV-style) или `Sociedade de Investimento Imobiliário` (SII), в зависимости от того, какой класс assets (operating service + edge hardware + solar) Miguel предложит как primary characterisation. Counsel-confirmable point.

**CELL** = compartment / sub-portfolio внутри CIC, не отдельная юр. форма. У каждой CELL:

- segregated assets и liabilities (one CELL's bankruptcy не затрагивает другие CELLs);
- собственный investor base;
- собственная operating activity (DT-services + solar + edge deployment per cluster);
- общий management company (CIC level), depositary, auditor, governance documents.

### 4A.2 Why this is dramatically cheaper than SPV-per-client (v1 critique resolved)

В v1 / v2.0 Smart Proxy я флагал N independent SPV cost stack: ~€1.5-3k/year contabilista per SPV, banking/KYC per SPV, audit per SPV. На margin €12-14/mo/customer это съедало unit economics уже на 10-15 customers per SPV.

CIC + CELL архитектура решает это:

| Cost item | N independent SPVs (v1 model) | CIC + N CELLs (v2.1 model) |
|---|---|---|
| Regulatory authorization | per-SPV если applicable (≈€10-20k initial each) | one CMVM authorization for CIC |
| Depositary | per-SPV если applicable | one depositary serving all CELLs |
| Auditor | per-SPV (~€3-5k/yr each) | one auditor at CIC level (split allocation to CELLs proportional to AUM) |
| Contabilista / accounting | per-SPV (~€1.5-3k/yr each) | one accounting team at CIC, per-CELL sub-ledgers |
| Banking | per-SPV banking relationship (~€500-1k/yr each) | one CIC master account + per-CELL sub-accounts |
| Governance documents | per-SPV articles + bylaws | one set at CIC level, per-CELL terms attached |
| KYC for investors | per-SPV (overhead each time) | one KYC framework, per-CELL investor allocation |

**Order-of-magnitude estimate:** при 10 cells CIC + CELL architecture стоит ~€30-50k/yr admin total (rough estimate, не counsel-confirmed); 10 independent SPVs стоят ~€50-100k+/yr. Разница увеличивается с scale. **Counsel-confirmable точные цифры — task в §9.**

### 4A.3 ECSP €5M per-CELL crowdfunding rail

**Legal anchor:** EU Regulation 2020/1503 — `European Crowdfunding Service Providers for Business`. Harmonized across EU as of November 2021. Key parameters:

- **Per-offer ceiling:** €5,000,000 over 12-month rolling period.
- Below ceiling: **lighter KIIS** (Key Investment Information Sheet) disclosure regime — significantly cheaper than full prospectus.
- Above ceiling: full prospectus under Regulation 2017/1129 required.
- ECSP-licensed platforms (PT-licensed or EU-passport) handle KYC, AML, investor categorization (sophisticated vs non-sophisticated), and crowdfunding mechanics.
- Non-sophisticated investor protections: knowledge entry test, simulation tools, 4-day reflection period, individual investment limit thresholds.

**Application к WeRa:**

- Каждая CELL может attract до €5M от retail + qualified investors через licensed ECSP platform.
- Это закрывает "customer-as-shareholder" mechanism: customer **проходит KYC на ECSP platform**, инвестирует periodic equity tranche (например, €100-500-1000 per round), и получает **legitimate shareholder rights в этой CELL** (voting, info access, dividends per CIC governance docs).
- Cumulative across CELLs: 10 CELLs × €5M = €50M theoretical capacity (subject to actual demand + per-customer caps + Phase gating).

**Working rule:** ECSP route доступен только после CIC registration + Track B.3 counsel sign-off on (a) CIC-as-issuer fitness, (b) per-CELL share class structure, (c) ECSP platform vendor selection. Не используется в Phase 1.

### 4A.4 Selected ECSP platform candidates (для desk-check, не selection)

Counsel needs to confirm, но из публично доступной информации PT-licensed ECSP platforms на 2026 включают:

- **PPL (Portugal)** — местная платформа с PT licensing.
- **GoParity (Portugal)** — фокус на impact / sustainability projects.
- **Seedrs / Crowdcube** — UK origin с EU passport (post-Brexit status varies — check).
- **Republic Europe** — EU-licensed.
- **Companisto / WiSEED** — DE/FR-based with EU passport.

**Selection criteria:** PT-licensed для primary fitness, EU-passport-capable для cross-border investor base, demonstrated track record in impact / sustainability sector (matches WeRa Foundation narrative), fee structure ≤ 5-7% of raise. Final selection — Phase 1 task.

### 4A.5 Customer-as-shareholder mechanism — fixed v1 design flaw

**v1 Smart Proxy:** "Share subscription — Customers buy 1 share/month → become minority shareholders — €1/month"

**Problem identified в v2.0 §2.3(b):** continuous €1/мес micro-equity не фитит ECSP regulation (rounds-based, not continuous), и может triggered public offering rules без proper structure.

**v2.1 fix:**

- ECSP-platform rounds happen **periodically per CELL** (например, semi-annual: rounds in March + September, or quarterly).
- Per round, individual customer-investor может вложить tranche-based (например, €100, €500, €1000, €5000 — соответствует ECSP investor categorization thresholds).
- Между rounds — customer accumulates **satisfaction tokens** (см. v1 §Revenue Streams), которые в next round могут быть applied как priority right на subscription (но не как direct equity — это требует separate counsel review).
- Customer voting rights + governance access — per CELL governance docs, не CIC level.

Это **executable structure**, не abstract subscription mechanism.

---

## 5. Regulatory routing (применение CLAUDE.md rule к Smart Proxy v2.1)

Не существует одного адресата «regulator». Smart Proxy v2.1 задаёт вопросы сразу к **шести** counsel-routes (добавлен ECSP path). Каждый route — отдельная задача, отдельный counsel, отдельный возможный authority touchpoint.

| Question family | Smart Proxy v2.1 element | First counsel route | Possible authority | Owner | Status |
|---|---|---|---|---|---|
| Energy / UPAC / hosting characterisation | «Smart Proxy» framing as `hosting of customer's electrical equipment` | Portuguese energy counsel (Miguel B.1) | `DGEG` / `ERSE` | Алексей + Михаил | В очереди (B.1 memo). v2.1: CELL = operator entity, customer = final consumer; clarify how CIC-owned equipment affects this. |
| Consumer credit / point-of-sale finance | CIC финансирует CAPEX → CELL operates → recurring service payment from customer | consumer-finance counsel (Miguel B.2) | `Banco de Portugal` | Алексей | В очереди (B.2 memo). v2.1: CIC/CELL может изменить consumer-credit qualification (collective investment ≠ direct finance). |
| Securities / collective investment / CIC + ECSP | CIC compartment structure; per-CELL ECSP rounds; customer-investor onboarding via licensed platform | corporate-securities-tax counsel (Miguel B.3 + specialist) | `CMVM` | Михаил | **v2.1 highest priority.** Phase 2 заблокирован до B.3 confirmation. ECSP platform selection — separate task. |
| **ECSP platform selection + onboarding** (new in v2.1) | Selection из PPL / GoParity / Seedrs / Republic Europe / Companisto; review platform Terms; legal agreement | securities counsel + ECSP platform legal team | n/a (platform regulated by `CMVM` if PT-based or EU passport authority) | Михаил | New task. Desk-check feasibility before signing platform agreement. |
| Tax / VAT / intra-CIC transfer | CIC management fees; per-CELL VAT; ECSP equity treatment; satisfaction token tax | tax counsel | `Autoridade Tributária` if counsel advises | Алексей | New task. CIC + ECSP combination изменяет VAT structure relative to v2.0 design. |
| Privacy / telemetry / household data + AI Act compliance | Shelly meters + on-premise edge processing + AI inference at edge (Article 10 II AI Act compliance) | privacy counsel + AI-compliance counsel | `CNPD` if counsel advises | Таня | v2.1 expands scope to AI Act (см. Schöning & Kruse 2025 paper). Edge devices require Ex-Ante dataset audit + Ex-Nunc behavior monitoring + Ex-Post tracing. |
| Foundation legal form | PT Associação vs Fundação vs NL alternative для governance overlay (Pillar A) | corporate counsel + non-profit specialist | — | Михаил | New task. Foundation legal form not blocking Phase 1 but needed before Phase 3. |

**Working rule:** ни один Smart Proxy документ не уходит к external party (counsel, authority, investor, installer, customer), пока не помечен **по какому конкретному route он составлен**. Generic «memo to the regulator» запрещён каноном.

---

## 6. New risks created by the synthesis (риски, которых нет в исходниках по отдельности)

Эти риски возникают только при совмещении нарратива Working Note с операционным vehicle Smart Proxy:

1. **Narrative-operational mismatch.** Working Note описывает WeRa как «alternative BlackRock с социальным капиталом». Smart Proxy operationally — это **N небольших SPV на премайсах клиентов**. Эти два уровня **не совместимы без явного umbrella + sub-SPV ladder**, который сам по себе является CMVM-trigger. Если умолчать про этот ladder в investor materials — это misrepresentation.
2. **Premature institutional pitch.** Family offices (Working Note primary audience) требуют operating track record. У WeRa: 1 pilot (Torres Vedras, без external-grade evidence pack), 1 proposal-stage client, signed installer partner. Smart Proxy v1 говорит «pilot is in Torres Vedras». Это значит, что **первый внешний investor-touch по Smart Proxy наследует Torres Vedras evidence gap** — пока pack не собран (Priority 1 gate), все pitches преждевременны.
3. **Compound regulatory load.** Каждый из пяти routes (energy, consumer credit, securities, tax, privacy) сам по себе — окно 4-12 недель counsel-time. Если их запускать sequentially, до Phase 2 readiness — 6-9 месяцев. Параллельный запуск требует ~€20-40k counsel budget — это новая capital request, которой нет в текущей финмодели.
4. **Confidence-vs-evidence asymmetry.** Working Note повторяет «confidence» 3+ раз как execution posture. Smart Proxy добавляет №-крупных claim (€12/мес, 22% savings, €60/мес pro, dividend-as-discount). На текущей evidence-base это создаёт **investor narrative debt** — каждый необоснованный claim становится узлом, который нужно либо закрыть, либо ограничить, либо снять.
5. **Scope-creep recurrence.** Working Note сам себя останавливает на трёх бизнесах (solar / consulting / DT). Smart Proxy v1 расширяет scope обратно до 6 revenue streams (base sub, satisfaction token, pro sub, cloud agent, marketplace curation, share subscription). Это противоречит §5.3 Smart Proxy v1's собственному self-correction. **MVP scope must be explicitly bounded** до Phase 1.

---

## 7. Investor narrative (Four Boxes, post-synthesis)

Из `research/WeRa-Consultant-Frame.md`: Box 1 обязателен; Box 2 — только как multiplier; Box 3 — только по запросу; Box 4 — не открывает разговор. Применяем к синтезу:

- **Box 1 (Operating business).** *«WeRa строит resilience-driven solar service business в Iberia. Selected working baseline — third-party operator с fixed service fee. Один pilot в Torres Vedras (technical evidence package в сборке), один client в proposal stage, signed installer partner Iberia Renew Engineering. Phase 1 Smart Proxy = unified service wrapper для energy + on-premise data + UX optimization, продаваемый через installer-network channel.»*
- **Box 2 (Scale architecture).** *«Multiplier — installer-network channel (Frame IV) + edge data-services attach. На горизонте Phase 2 — project-SPV pool под umbrella, что позволяет capital recycling через portfolio debt, gated by counsel.»*
- **Box 3 (Governance/legal).** Только по запросу: routing matrix, hosting characterisation, Track B memos.
- **Box 4 (Vision).** Anti-crisis solution + social capital retention + sovereign cloud + customer participation. **Не** открывает разговор; **не** держит JP Morgan Jr / BlackRock 3-loop / generic network-state shorthand.

---

## 8. Решения, которые нужны от сооснователей (v2.1 — defer к Working Note v2)

**Decisions перенесены в Working Note v2** (`2026-05-21-working-note-v2-anti-crisis-strategy.md` §9), потому что они структурно зависят от стратегического выбора DT-consultancy-as-core, а не только от operational Smart Proxy vehicle. v2.1 этой ноты выполняет **Decision 3 operationally** (CIC + CELL + ECSP architecture as selected scaffolding) — остальные decisions остаются в Working Note v2.

Краткое mapping decisions:

| Working Note v2 Decision | Что это значит для Smart Proxy v2.1 |
|---|---|
| **Decision 1** (DT consultancy as primary cash engine) | Если (A): Smart Proxy CELL deployment следует за consulting funnel, не предшествует. Phase 0 = consulting, Phase 1 = first CELL stand-up. |
| **Decision 2** (Three-pillar umbrella as working architecture) | Если (A): CELL = Pillar B operational layer; Foundation governance overlay (Pillar A) и Compliance layer (Pillar C) ставят architectural constraints на CELL design (см. §4A.1, §4A.5, §5). |
| **Decision 3** (CIC + CELL + ECSP €5M rail) | Если (A): этот документ v2.1 = operationalisation. §4A полностью реализует. |
| **Decision 4** (Counsel parallel routes) | Confirmed (А) parallel. §5 table расширена до 6 routes. |
| **Decision 5** (AI-native frameworks в investor materials) | Если (A): Smart Proxy v2.1 cite-ит Schöning & Kruse 2025 (AI Act compliance), Protopia (Pillar A reference), AI-Native Playbook (Pillar B reference), Kleros (Pillar C reference) в Appendix. |
| **Decision 6** (Document ownership) | Алексей — owner обоих документов (v2 working note + v2.1 concept note). |

---

## 9. Next-step package (gates → owners → triggers)

Только items, которые двигают синтез вперёд. Не дублирует существующий `open-gates.md`.

| # | Действие | Owner | Срок | Зависит от |
|---|---|---|---|---|
| 1 | Co-founder review этой ноты, решения 1-5 в §8 | Михаил, Алексей, Таня | до конца недели | — |
| 2 | Добавить hosting-characterisation question в `miguel-track-b1-energy-contract-memo.md` §6.1 как **Smart Proxy use-case** (не как абстрактный вопрос) | Алексей | следующий drop Miguel-у | Решение 2 |
| 3 | Добавить «registered office at private address» quick-check в `miguel-track-b3-corporate-structure-memo.md` | Михаил | следующий drop Miguel-у | Решение 2 |
| 4 | Открыть **privacy/CNPD task** в Operations/Legal index — explicit Shelly + telemetry + controller/processor scope | Таня | две недели | Решение 2 |
| 5 | Открыть **tax route task** — VAT для intra-group lease + service fee + share subscription | Алексей | две недели | Решение 2 |
| 6 | Recut Phase 1 unit economics с учётом SPV cluster overhead (€1.5-3k/год contabilista per SPV) | Михаил | две недели | Решение 1 |
| 7 | Снять `22% savings` claim из Smart Proxy materials до segment-verification | Алексей | сразу | Решение 4 |
| 8 | Подготовить consulting-funnel launch checklist (если решение 3 = A): pricing, intake form, recording protocol, instruction-template) | Михаил | две недели | Решение 3 |
| 9 | Обновить `claim-register.md`: добавить «hosting characterisation», «SPV cluster economics», «€1/мес share subscription» с явными `status` маркерами | Алексей | одна неделя | Решение 1 |
| 10 | Закрыть Google-Workspace-proxy идею официально, выбрать Nextcloud/Mailcow substitute для Phase 1 messaging | Алексей | одна неделя | — |

---

## 10. Что эта нота **не** делает

Чтобы не было ложных ожиданий:

- не утверждает, что Smart Proxy = «правильный» путь — это `replacement candidate`, gated;
- не закрывает ни один из counsel-routes;
- не заменяет существующие memo (B.1, B.2, B.3, regulatory routing matrix);
- не даёт investor-pitch language — даёт only internal frame;
- не оценивает финансовую модель Phase 1 / Phase 2 в цифрах — это отдельный task (#6 в §9);
- не решает, что делать с Torres Vedras evidence boundary — это уже Priority 1 gate в `open-gates.md` и движется отдельно.

---

## Приложение A — Mapping cross-document (для трассировки)

| Working Note claim | Smart Proxy v1 element | Canon reference | Status в v2.0 |
|---|---|---|---|
| «Third party operator who doesn't own equipment» | Umbrella owns equipment + leases to SPV | `current-business-model.md §10.2 #1 vs #2` | **Contradiction** — синтез выбирает Phase 1 = WN-aligned; Phase 2 = SP-v1-aligned, gated. |
| «Scaling inference across organizations» | On-premise edge stack + data services subscription | `current-business-model.md §11.1-11.2` | Совместимо как accessory layer; не как primary investor narrative. |
| «Social capital / customer-as-shareholder» | €1/мес share subscription | `miguel-track-b3 §4.5 questions 22-25` | Phase 2, CMVM-gated. |
| «AI native organization» | Cloud agent / marketplace curation | `WeRa-Consultant-Frame` (Operating Object) | Operating design principle, not gated. |
| «Survive the crisis» (mission frame) | — (отсутствует в SP v1) | Box 4 / `WeRa-Consultant-Frame` | Investor narrative anchor, не Box 1. |
| «John / Sun Viva partnership» (Working Note) | — (отсутствует в SP v1) | `current-business-model.md §9.2-9.3` | Дополняет Frame IV channel — независимая работа. |
| «20% savings» / «22% savings» | Smart Proxy §Cost Model | `claim-register.md`, `open-gates.md` Priority 1 | **Снять** до evidence. |
| «Consulting + Design Thinking + psychologist» (WN) | — (отсутствует в SP v1) | Новый элемент; Решение 3 в §8. | Track independent, zero CAPEX, не блокирован. |
| «Network state» (WN) | — (отсутствует в SP v1) | Box 4 only | Aspirational identity. |
| «JP Morgan Jr» | — | Fact-check correction § 2.2 | JP Morgan **Sr.**, заменить. |
| «BlackRock 3-vehicle loop» | — | Fact-check correction §2.2 | Inaccurate — design own structure. |

---

## Приложение B — Что мы хотели бы изменить в Working Note v1 fact-check (если делать v2)

Working Note fact-check полезен, но узок. Если делать v2 fact-check, AI-сессия рекомендует добавить:

1. Fact-check на **timing claims** (Portugal solar growth до 2030 — какие assumptions, какой risk-window до 2027 vs 2029).
2. Fact-check на **PT specific consumer-credit threshold** (Lei do Consumidor + Decreto-Lei 133/2009 transposing Consumer Credit Directive — что именно triggered и какие exemptions).
3. Fact-check на **SPV-cluster economics** в PT (real contabilista / ROC / auditor costs at scale; transfer-pricing rules для intra-group lease).
4. Fact-check на **Ordem dos Psicólogos Portugueses** rules для psychologist-as-consultant model.
5. Fact-check на **Nextcloud + GDPR** PT-specific precedents (DPA opinions, sector guidance).

Эти проверки не блокируют co-founder review, но укрепят финальные investor materials.

---

*Конец Smart Proxy Concept Note v2.0. Эта нота — артефакт для co-founder review, не утверждённая стратегия. После решений в §8 — либо merge в `current-business-model.md` (если Phase 1 принят), либо архив в `research/`.*

---

## Addendum v2.2 (2026-05-22) — CIC Re-Positioning + STAK NL Capital Rail + CMVM AIFMD Discipline

> **Этот addendum модифицирует §4 (Reconciled object) и §5 (Regulatory routing). Body документа остаётся как detailed source, но canonical operational vehicle identity — addendum, не §4.**

### B1. Why the addendum

(a) `OLD.WeRa.White.v.0.9.pdf` (uploaded 2026-05-22) восстановил legacy three-entity scaffolding — Foundation CH + Capital PT + STAK NL — superior к invented Smart Proxy v1 ("Umbrella owns equipment + leases to SPV").
(b) CMVM call 2026-05-22 (`Meetings/2026-05-22-cmvm-call.md`) показал: pursuing CIC под RGOIC ради admin convenience сам по себе — AIFMD trigger. Clean Phase 0/1 path = ordinary operating company + truly operational SPVs.

### B2. Smart Proxy CELL — corrected operational frame

| Element | v2.1 (superseded) | v2.2 (current canonical) |
|---|---|---|
| **Legal vehicle Phase 0/1** | PT `OIC` под RGOIC с compartment / CELL structure (Miguel-confirmed scaffolding) | **Ordinary PT `Sociedade` (Capital PT) + per-installation operating SPVs** (each SPV must have real operational function: solar service operation, monitoring, edge data processing). **CIC под RGOIC explicitly NOT Phase 0/1 vehicle.** |
| **CIC под RGOIC** | Phase 0/1 default scaffolding | **Phase 2+ destination ONLY** when conscious collective-investment step taken WITH CMVM authorization (1–2 mo process, 3 mo lead time) |
| **Equipment ownership** | Umbrella / CIC owns equipment, intra-group leases to CELL SPV | **Capital PT (or each operational SPV) owns equipment** — direct operational holding, not intra-group lease. Preserves AIFMD criterion 1 (commercial/industrial purpose). |
| **Customer-as-shareholder mechanism** | €1/mo continuous share subscription (Phase 2 gated) | **STAK NL Y-share depositary receipts** (voting / ownership, Type A) and **X-share depositary receipts** (profit, Type B). Phase 1 = founders only. Phase 2+ external offering ONLY after CMVM authorization-department clearance. |
| **ECSP €5M rail per CELL** | Phase 3 capital scale mechanism | **Preserved as Phase 2+** but each ECSP round separately AIFMD-tested; STAK X-share placement = anchor-LP rail; ECSP retail/qualified = follow-on. **First ECSP round NOT before CMVM authorization-department engagement (3 mo lead time).** |
| **"22% savings" customer claim** | Listed в §3.2 weaknesses | **Removed** entirely per `claim-register.md` Priority 1 gate. |
| **Google Workspace proxy / cloning** | Listed в §3.2 weaknesses | **Removed** — substitute = Nextcloud + Mailcow + OnlyOffice / Collabora. |
| **Hosting characterisation** | Open characterisation hypothesis | **Confirmed orally by CMVM** that operating company с явной commercial/industrial purpose = outside fund regulation perimeter; hosting characterisation остаётся Miguel B.1 sub-task для energy law (DGEG/ERSE), но не CMVM. |

### B3. AIFMD design discipline (extends §5 regulatory routing)

Каждое design decision Smart Proxy CELL должно проходить ESMA/2013/600 AIFMD 4-criteria test:

1. **General commercial / industrial purpose** — каждая операционная SPV должна иметь и **документировать** real operational function (solar service operation, monitoring, edge data processing, customer relationship). Не passive asset holder. **Registration documents Capital PT** explicitly включают this language per ESMA para 21.
2. **No pooled return** — Phase 0/1 cash flow = service revenue, founder/F&F (excluded per para 15), direct convertible. **No external customer-investor pool** до CMVM authorization step.
3. **Day-to-day control retained by executive** — operational governance Capital PT в executive board hands; Y-share voting (когда выпускается) на strategic decisions only, not day-to-day.
4. **Pre-existing group** — founders + Foundation CH + Capital PT form pre-existing operational team, не investor pool.

**SPV cohort qualification = open action item.** CMVM представитель просит detailed SPV functional description для authorization-department review. Готовится перед any Phase 2 customer-as-shareholder attempt.

### B4. Pointer

Canonical reading этого обновления — `Strategy/Business-Model/2026-05-21-project-note-v1-anti-crisis-decision-pack.md v1.1` (§2 + §3a + §6 + Appendix D). Smart Proxy v2.1 body остаётся как detailed operational source; addendum B1–B4 — current canonical version operational identity.

*Конец Smart Proxy Addendum v2.2.*

formal_proof:
  engine: ml-hilbert
  trl_phase: TRL6
  obligation_id: kb.governance.annex_source_sync_strategy_business_model_2026_05_21_smart_proxy_concept_note_v2
  proof_artifact: kb-governance/formal-proofs/governance-annex-source-sync-strategy-business-model-2026-05-21-smart-proxy-concept-note-v2.lean
  verification_status: verified
