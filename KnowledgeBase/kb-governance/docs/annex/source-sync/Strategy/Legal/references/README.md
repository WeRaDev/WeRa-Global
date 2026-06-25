# Legal References — внешние авторитетные источники

## Consolidation provenance
- consolidation_actor: `WARP`
- consolidation_source: `/Users/mikhailananyin/Documents/WeRa Global/KB-latest-original/Strategy/Legal/references/README.md`
- consolidation_date: `2026-06-22`
- consolidation_status: `canonicalized`


Папка для официальных/первичных документов, на которые опирается legal-работа WeRa. Это **референсы**, не наши драфты.

---

## ESMA-2013-600-guidelines-AIFMD-key-concepts.pdf

**Что это:** ESMA Final Report — *Guidelines on key concepts of the AIFMD* (ESMA/2013/600). Официальные критерии ЕС, по которым определяется, является ли структура «alternative investment fund» (AIF) / коллективным инвествехиклом.

**Откуда у нас:** прислан представителем **CMVM Inov** на звонке **22 мая 2026** как авторитетный референс в ответ на наш вопрос о практической границе «операционная компания vs коллективный инвествехикл». См. `Meetings/2026-05-22-cmvm-call.md`.

**Почему важно (load-bearing):** это тот самый тест, который применяет CMVM. Сущность является коллективным инвествехиклом только если присутствуют **все** признаки (Annex III, п. 12). Ключевые определения и тесты — **Annex III, пункты 12–22**:

- **general commercial or industrial purpose** — реальная коммерческая/промышленная деятельность (поставка нефинансовых услуг, производство). Если она есть — это **не** коллективный инвествехикл. Это главный щит WeRa: операционная компания и реально оперирующие SPV такую цель имеют.
- **pooled return** — доходность от пула активов, привлечённого от инвесторов.
- **day-to-day discretion or control** — отсутствие у акционеров как группы повседневного операционного контроля.
- **pre-existing group** — деньги основателей/семьи для собственного капитала вынесены из понятия «raising capital» (п. 15).
- п. 21: реальная **бизнес-стратегия** операционной компании ≠ «инвестиционная политика».

**Как использовать:** как формулировочный референс для регистрационных документов операционной компании (показать general commercial/industrial purpose) и как чек-лист перед любым шагом к investment vehicle / `customer → shareholder`. Подробный разбор итогов звонка — в `Meetings/2026-05-22-cmvm-call.md`; routing — в `../regulatory-routing-and-power-tier-matrix.md` §1B.

formal_proof:
  engine: ml-hilbert
  trl_phase: TRL6
  obligation_id: kb.governance.annex_source_sync_strategy_legal_references_readme
  proof_artifact: kb-governance/formal-proofs/governance-annex-source-sync-strategy-legal-references-readme.lean
  verification_status: verified
