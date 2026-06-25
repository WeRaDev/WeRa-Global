---
title: "WeRa — Open Gates"
date: "2026-04-22"
updated: "2026-06-16"
type: "open-gates"
status: "working-baseline"
purpose: "Список нерешённых, но load-bearing вопросов текущей бизнес-модели."
---

## Consolidation provenance
- consolidation_actor: `WARP`
- consolidation_source: `/Users/mikhailananyin/Documents/WeRa Global/KB-latest-original/Strategy/Business-Model/open-gates.md`
- consolidation_date: `2026-06-22`
- consolidation_status: `canonicalized`


# WeRa — Open Gates

> Это список не “всех вопросов”, а только тех узлов, которые реально держат legal, financial и strategic coherence модели.

## Priority 1 — cannot be deferred

| Gate | Why load-bearing | Owner | Trigger |
|---|---|---|---|
| Torres Vedras external-grade evidence pack | questionnaire now gives a founder-memory working version, but the only executed operating object still lacks written agreement, payment trail, ownership/control memo, telemetry proxy-savings sheet and maintenance ledger | Алексей + Михаил | before external legal/regulator/investor use of the pilot |
| Exact service-fee contract package | selected baseline is only a reading until counsel confirms the package | Miguel / local counsel | before first repeatable contract |
| Consumer-credit / intermediation qualification | may block household and microbusiness model in parallel with energy-law | Miguel + finance/corporate counsel | before signing first household / microbusiness deal |
| Regulatory routing map | `regulator` is not one address; energy, credit, securities/fund, tax and telemetry questions must go to different counsel / authority paths | Алексей | before any external authority-specific summary |
| Power / grid-status matrix | oral `21-25 kW` threshold cannot be treated as operational fact; off-grid, grid-connected, `>700 W`, `<=30 kW`, `>30 kW`, multi-module and collective cases route differently | Miguel + Алексей | before any proposal or regulator question depends on a threshold |
| Default / insurance / repossession stack | changes pricing, lender appetite and legal enforceability | Miguel + insurer / legal support | before scaling beyond pilot logic |
| Fate of `20% savings guaranteed` | live external claim currently outruns evidence | Алексей | before next public GTM iteration |
| DT session consent/privacy package | recording/transcription practice requires explicit consent and storage-access policy to stay compliant and defensible | Михаил + Алексей | before scaling DT sessions with recording/transcription |
| AI-platform claim wording discipline | external wording must preserve fact vs hypothesis split from evidence brief | Алексей | before investor/public materials use AI-behavior narrative as hard fact |
| **Luiz Fernandes 4% equity stake — status** | MoU-based 4% granted in 2024; Luiz withdrew Sep 2024; no formal release confirmed in available records; if unresolved, residual claim may attach to the new PT entity | Miguel / PT corporate counsel | **before entity registration** |
| **2024 angel investors (CLA/SAFE) — continuity** | ~7 CLAs/SAFEs signed in 2024 F&F round under the old investment-fund model; these investors have financial claims; their instruments must be either honoured by the new entity or formally novated / released | Miguel | **before entity registration** |
| **2024 DAO on-chain records — disclosure** | DAO at 0xcae36a534cca5d5d95fa988f1a76966543e1bc26 on Polygon contains signed MoUs, governance proposals, investor onboarding records — all publicly visible; if new entity is successor to WeRa Capital / Inteligente Razão, regulators or investors may discover these records | Miguel | before regulator-facing filings reference prior entity history |

## Priority 2 — required for clean scale path

| Gate | Why load-bearing | Owner | Trigger |
|---|---|---|---|
| Edge-only BOM recut | needed to clean the compute boundary and cost stack | Алексей | before investor/regulator materials reuse current BOM |
| Base case without WiFi Map | needed for honest fundraising and planning | Михаил | before investor-facing finance pack |
| PT vs ES comparison on same contract stack | otherwise jurisdiction choice stays rhetorical | Miguel / local counsel | before structural jurisdiction decision |
| First-subset contract repeatability | needed to prove the chosen customer subset is real, not just elegant on paper | Алексей + sales/installer side | after next 3-5 proposals/contracts |
| First grid-connected UPAC / final-consumer evidence | Torres Vedras does not prove the ordinary grid-connected baseline because current package has no supplier-contract / bill-vs-bill baseline | Алексей + Михаил | before claiming Track B is executed in reality |
| DT conversion chain baseline (`impressions -> clicks -> bookings -> completed -> paid -> upgrade`) | launch channel exists, but operating conversion economics are not yet stabilized | Михаил | before claiming repeatable paid DT demand |
| First 3 bounded DT case write-ups | needed to move from narrative to proof without overclaiming causality | Алексей | before broad GTM scaling or investor reuse |

## Priority 3 — optionality and expansion gates

| Gate | Why load-bearing later | Owner | Trigger |
|---|---|---|---|
| Installer-network evidence beyond one signed partner | needed before treating Frame IV as scale engine | Алексей + Михаил | before channel-expansion narrative becomes baseline |
| Separate digital/commercial object for Nextcloud wedge | needed if digital revenue starts to matter materially | Алексей | before digital attach moves from optional to meaningful revenue line |
| Customer -> shareholder path | corporate/securities/tax heavy, not part of current object | separate corporate/securities counsel | only if this mechanism returns to active strategy; **CMVM (2026-05-22): this is the trigger into CMVM perimeter — engage authorization department ~3 months before launch (authorisation takes 1–2 months)** |
| Project-SPV cohort fund-classification | a cohort of per-installation SPVs is **not automatically** a fund, but a passive pool raising external capital for a pooled return can be classified as an AIF | corporate/securities counsel + CMVM authorization dept | before opening SPVs to external participants; CMVM offered to check qualification if we send a **detailed description of what the SPVs actually do** |

> **CMVM verbal guidance (2026-05-22, ознакомительная встреча):** at first stage an ordinary operating company with a *general commercial or industrial purpose* (fixed service fee, no securities, no collective-investment offering) is **outside CMVM's authorization perimeter**. The operating-company vs collective-investment-vehicle line is governed by the ESMA AIFMD key-concepts criteria — general commercial/industrial purpose, pooled return, day-to-day control, pre-existing group (`Strategy/Legal/references/ESMA-2013-600-guidelines-AIFMD-key-concepts.pdf`, Annex III §12–22). No WeRa-specific written ruling obtained yet. Details: `Meetings/2026-05-22-cmvm-call.md`.

## How to use

Before any serious conversation with:

- counsel
- relevant regulatory authority
- investor
- installer partner

convert the relevant row into a meeting-specific question list and carry its `trigger`, not just the headline.

For regulator-facing work, first read `Strategy/Legal/regulatory-routing-and-power-tier-matrix.md` and route the question family before drafting.

formal_proof:
  engine: ml-hilbert
  trl_phase: TRL6
  obligation_id: kb.governance.open_questions_38_open_gates_v1
  proof_artifact: kb-governance/formal-proofs/governance-open-questions-38-open-gates-v1.lean
  verification_status: verified
