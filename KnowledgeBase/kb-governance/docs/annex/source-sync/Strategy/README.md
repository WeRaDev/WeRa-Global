# Strategy Index

## Consolidation provenance
- consolidation_actor: `WARP`
- consolidation_source: `/Users/mikhailananyin/Documents/WeRa Global/KB-latest-original/Strategy/README.md`
- consolidation_date: `2026-06-22`
- consolidation_status: `canonicalized`


Updated: 2026-04-24

This folder stores **canonical strategic documents** for WeRa.

Rule of thumb:
- `research/` = dated research, desk work, stress-tests, hypothesis memos
- `Strategy/` = what WeRa currently treats as the best assembled internal frame
- `Legal/` = legal packaging, counsel questions, draft structures
- `Outputs/` = external-facing materials

## Structure

- `Business-Model/`
  - current canonical model
  - selected-set rationale (`starter-drr.md`)
  - term discipline (`UTS.md`)
  - claim register
  - executed-vs-designed separator
  - CAPEX and capital-architecture logic
  - open gates before legal/investor packaging
- `Legal/`
  - pre-counsel legal-operating descriptions
  - source drafts for counsel memos and authority-specific regulator-facing summaries
  - regulatory routing and power-tier matrix
- `Scenarios/`
  - alternative development paths and their triggers
- `Fundraising/`
  - investor-facing baseline cases, funding asks, instrument logic

## Start here

1. `Business-Model/current-business-model.md`
2. `Business-Model/starter-drr.md`
3. `Business-Model/UTS.md`
4. `Business-Model/claim-register.md`
5. `Business-Model/executed-vs-designed.md`
6. `Business-Model/capital-architecture.md`
7. `Business-Model/open-gates.md`
8. `Legal/regulatory-routing-and-power-tier-matrix.md`
9. `Legal/legal-operating-description-draft.md`

Only after that go back into `research/` for evidence, traces, and dated memo context.

## Regulatory Rule

Do not draft one generic "regulator" package from Strategy docs.

Route first:

- energy / UPAC / final-consumer questions -> Portuguese energy counsel, then possible `DGEG` / `ERSE`;
- consumer-credit / credit intermediation -> finance counsel, then possible `Banco de Portugal`;
- CIC / STAK / customer participation / fund or securities questions -> corporate/securities/tax counsel, then possible `CMVM` and tax authority;
- telemetry / household energy data -> privacy counsel, then possible `CNPD`.

The selected customer/project-SPV title posture is a working baseline for testing, not a confirmed clean structure. Torres Vedras is Track A / technical evidence and does not prove grid-connected UPAC / final-consumer Track B.

formal_proof:
  engine: ml-hilbert
  trl_phase: TRL6
  obligation_id: kb.governance.annex_source_sync_strategy_readme
  proof_artifact: kb-governance/formal-proofs/governance-annex-source-sync-strategy-readme.lean
  verification_status: verified
