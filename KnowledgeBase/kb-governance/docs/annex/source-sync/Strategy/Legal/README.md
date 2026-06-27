# Legal Strategy Index

## Consolidation provenance
- consolidation_actor: `WARP`
- consolidation_source: `/Users/mikhailananyin/Documents/WeRa Global/KB-latest-original/Strategy/Legal/README.md`
- consolidation_date: `2026-06-22`
- consolidation_status: `canonicalized`


This folder stores **pre-counsel legal packaging** derived from the canonical business-model package.

## Read order

1. `regulatory-routing-and-power-tier-matrix.md`
   - canonical pre-counsel routing addendum
   - fixes that `regulator` is not one address, power/grid-status tiers must be separated, selected title baseline is not yet clean, and Torres Vedras is not proof of Track B
2. `legal-operating-description-draft.md`
   - full pre-counsel legal-operating description of the current selected model
   - source for later counsel memos and authority-specific regulator-facing summaries
3. `miguel-track-a-torres-vedras-memo.md`
   - retrospective qualification of the executed Torres Vedras arrangement
   - asks what written carrier / ownership-control memo should be signed now
4. `miguel-track-b1-energy-contract-memo.md`
   - prospective Portuguese energy-law and contract-package validation
   - asks about UPAC/self-consumption, final consumer status, contract type, no `€/kWh` resale, power/grid-status tiers, default, de-installation and insurance
5. `miguel-track-b2-consumer-credit-memo.md`
   - consumer-credit / financial-intermediation classification
   - asks about long-term recurring payments, title variants, credit-arrangement risk, installer/finance referrals and pilot-style buy-back reuse
6. `miguel-track-b3-corporate-structure-memo.md`
   - corporate / securities / tax structure
   - asks about minimum first entity, project SPVs, PT CIC/OIC, NL STAK, customer participation, tax and far-path tokenisation

Supporting index:

- `miguel-track-b-baseline-memo.md`
  - superseded consolidated Track B index; do not send as operative counsel questionnaire

External references:

- `references/` — official/primary source documents the legal work relies on (see `references/README.md`)
  - `references/ESMA-2013-600-guidelines-AIFMD-key-concepts.pdf` — ESMA AIFMD key-concepts guidelines; the criteria CMVM uses for the operating-company vs collective-investment-vehicle line (provided by CMVM on 2026-05-22). Read with `../../Meetings/2026-05-22-cmvm-call.md` and `regulatory-routing-and-power-tier-matrix.md` §1B.

## Working rule

Documents here are not legal opinions.

They should:

- preserve the selected `service-fee + operator first` baseline;
- describe customer/project-SPV title as `selected working baseline for testing`, not as a confirmed clean baseline;
- mark founder hypotheses as alternatives or far paths;
- avoid upgrading `MEMORY` or `ESTIMATE` into `FACT`;
- avoid treating Torres Vedras as proof of grid-connected UPAC / final-consumer / fixed-service-fee Track B;
- avoid using oral `21-25 kW` thresholds as operational legal fact;
- carry open gates into counsel questions instead of hiding them.

Before external use, send only the relevant specialist memo, route the question family through `regulatory-routing-and-power-tier-matrix.md`, and get legal review.

## Track Discipline

- Track A = what already happened in Torres Vedras.
- Track B.1 = future repeatable energy / contract package; possible authority route after counsel: `DGEG` / `ERSE`.
- Track B.2 = consumer-credit and financial-intermediation gate; possible authority route after counsel: `Banco de Portugal`.
- Track B.3 = corporate / securities / tax gate; possible authority route after counsel: `CMVM` and tax authority.
- Do not send them as one blended question. If counsel answers a hybrid, ask for clarification.

formal_proof:
  engine: ml-hilbert
  trl_phase: TRL6
  obligation_id: kb.governance.annex_source_sync_strategy_legal_readme
  proof_artifact: kb-governance/formal-proofs/governance-annex-source-sync-strategy-legal-readme.lean
  verification_status: verified
