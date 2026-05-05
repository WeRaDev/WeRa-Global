# WeRa Global — Project Knowledge Base

> **Version**: 2.6 — May 2026
> **Scope**: Complete machine-readable reference for the WeRa Global project
> **Sources**: Project transcripts, wera.global website, SolarSeed technical description, WeRa financials (4 CSVs), web research, academic literature, social media
> **Changelog v2.6**: Recorded repository-governance migration of `ProductionBase/Poly-Robot` from umbrella-native tracking to independent delegated repository registration under `ProductionBase/repos.yaml`, while preserving umbrella `KnowledgeBase/` canonical authority.

---

## Quick Reference

| Field | Value |
|---|---|
| **Company** | WeRa Global (brand); incubated by INTELIGENTE RAZÃO - UNIPESSOAL LDA |
| **Website** | [www.wera.global](https://www.wera.global) |
| **LinkedIn** | [WeRa Global](https://www.linkedin.com/company/wera-global) — 22 followers |
| **X / Twitter** | [@wera_global](https://x.com/wera_global) |
| **Tagline** | Solar Network State of Federated Clouds |
| **HQ** | Lisboa, Portugal |
| **Stage** | Pre-seed / Incubation (Q2 2026 registration target) |
| **Physical product** | SolarSeed — modular solar stations (12 kW–500 kW) |
| **Digital product** | WERA Cloud — privacy-first Nextcloud-based collaboration platform |
| **Platform / App** | FilantropiaSolar — smart energy management system (beta) |
| **Blockchain** | Polygon (ERC-compatible; Digital Depositary Receipts) |
| **Installation partner** | Iberia Renew Engineering ([renewiberia.com](https://renewiberia.com)) — signed |
| **Pilot customer** | Off-grid micro-farm, Torres Vedras, Portugal |
| **Current burn** | €2,000/month |
| **Funding ask** | Active track: object-level financing proposals (per-install cashflow packages). Model baseline: SAFE €660,136 + seed/equity stages (see `09`, `13`). |
| **Implied post-money** | ~€18.3M |
| **Cloud pricing** | Free / €1/user/month / €12/user/month (Royal) |
| **SolarSeed base CAPEX** | €5,001.26 (69% energy / 31% compute) |
| **SolarSeed avg CAPEX** | €22,979.69 (89% energy / 11% compute) |
| **Base monthly lease** | €70.00 (20-year term) |
| **Avg monthly lease** | €460.00 (25-year term) |
| **Y1 revenue target** | €170,954 (100 units, 8k cloud users) |
| **Y2 revenue target** | €6,475,142 (1,000 units, 376k cloud users) |

---

## Naming Conventions

| Term | Meaning | Status |
|---|---|---|
| **WeRa Global** | Brand / company name | Canonical |
| **SolarSeed** | Physical solar + storage + compute station | Canonical (replaces early "SolarSeat") |
| **WERA Cloud** | Digital cloud platform (Nextcloud-based) | Canonical (not "VERA Cloud") |
| **FilantropiaSolar** | Internal smart energy management platform (REEMS) | Working name / beta |
| **Solar Citizens** | End users / prosumers in the WeRa ecosystem | Canonical |
| **City of Light** | Gamified UX layer for SolarSeed infrastructure | Conceptual / roadmap |

---

## File Index

> Legacy top-level files are compatibility stubs. The canonical source-of-truth paths listed below are under `kb-*/docs/...`.

| # | File | Contents |
|---|---|---|
| 00 | `kb-governance/docs/standards/00-glossary.md` | Canonical naming, acronyms, entity definitions |
| 01 | `kb-value-proposition/docs/company/01-company-overview.md` | Brand, vision, mission, founding, incubation status |
| 02 | `kb-value-proposition/docs/products/02-products.md` | SolarSeed hardware, WERA Cloud, FilantropiaSolar, pricing |
| 03 | `kb-revenue-streams/docs/model/03-business-model.md` | Leasing mechanics, cloud revenue, cost structure, financial flywheel |
| 04 | `kb-key-resources/docs/architecture/04-system-architecture.md` | Federated infrastructure, virtual power plant, data pipeline |
| 05 | `kb-governance/docs/tokenomics/05-tokenomics-and-governance.md` | Three tokens (WeD/WeG/WeP), governance boards, Polygon/DDR |
| 06 | `kb-governance/docs/legal/06-legal-structure.md` | Three-entity architecture, cap table, IP, MiCA alignment |
| 07 | `kb-customers/docs/gtm/07-customers-and-gtm.md` | Customer segments, sales pipeline, ambassador programme |
| 08 | `kb-key-partners/docs/partnerships/08-partnerships.md` | Renew Iberia, Soula, Ubbu, WiFi Map, Mitsubishi, equipment |
| 09 | `kb-solution/docs/strategy/09-strategy-and-investment.md` | DePIN thesis, Triple Jump, funding ask, use of funds, revenue targets |
| 10 | `kb-problem/docs/market/10-market-context.md` | Portugal solar market, DePIN landscape, EU regulation, competitors |
| 11 | `kb-governance/docs/references/11-academic-references.md` | Scholarly sources on DePIN, tokenization, energy communities |
| 12 | `kb-governance/docs/open-questions/12-open-questions.md` | Compatibility mirror/index for unresolved items; canonical register at `kb-governance/docs/open-questions/12-open-questions.md` |
| 13 | `kb-metrics/docs/financial/13-financial-model.md` | Full P&L, OpEx/CapEx, unit economics, fundraising model, cash position |
| 14 | `kb-governance/docs/audit/14-kb-audit-v1.1.md` | Systematic audit of v1.1 against all 7 source documents |
| 15 | `kb-key-resources/docs/suppliers/15-sunified-quantum-resistance.md` | Sunified Group UNITY sensor, quantum resistance thesis, WeRa integration |
| 16 | `kb-key-activities/docs/platform/16-filantropiasolar-platform.md` | Platform architecture, map app, proposal calculator, ML pipeline |
| 17 | `kb-key-activities/docs/execution/17-execution-readiness-and-next-30-days.md` | Immediate sequencing, investor gate criteria, and operational risk controls |
| 18 | `kb-governance/docs/reviews/18-mempalace-critical-review-action-plan.md` | Critical review of memPalace spec, corrected decisions, and actionable KB-upgrade workstreams |
| 19 | `kb-governance/docs/architecture/19-domain-taxonomy-map-v1.md` | Verified current structure and defined canonical 12-domain BMC+Lean taxonomy |
| 20 | `kb-governance/docs/architecture/20-file-domain-ownership-map-v1.md` | Mapped existing KB files to primary/secondary domains and ownership model |
| 21 | `kb-governance/docs/standards/21-controlled-vocabulary-entity-standards-v1.md` | Canonical terminology, status enums, evidence labels, and provenance requirements |
| 22 | `kb-customers/docs/standards/22-anonymized-case-schema-lifecycle-v1.md` | Privacy boundary contract, anonymized case schema, and lifecycle transition rules |
| 24 | `kb-governance/docs/workflows/24-governance-workflows-v1.md` | Governance workflows for intake, evidence, privacy, cross-domain review, cadence, and PR readiness |
| 25 | `kb-governance/docs/architecture/25-cross-domain-integration-matrix-v1.md` | Cross-domain integration patterns, matrix, and pilot operational link path |
| 26 | `kb-governance/docs/validation/26-validation-protocol-v1.md` | Validation layers and checklists for cross-domain consistency and case-safety |
| 31 | `kb-governance/docs/status/31-kb-upgrade-status-next-steps-2026-04-15.md` | KB-upgrade completion-state status and post-upgrade handoff summary |
| 32 | `kb-governance/docs/status/32-kb-upgrade-completion-deferral-policy-2026-04-15.md` | Canonical completion decision, unresolved-question deferral policy, and TRL4-scoped MemPalace integration rule |
| 33 | `kb-governance/docs/status/33-kb-ai-native-bridge-v3.2-2026-04-24.md` | v3.2 bridge from AI-native research proposal to KPI-gated operational rollout policy |
| — | `WARP.md` | Dedicated KnowledgeBase operating rules, reflection outcomes, and mandatory PR checklist |
| — | `kb-governance/docs/open-questions/12-open-questions.md` | Canonical unresolved-question register for governance execution |
| — | `kb-governance/docs/events/2026-04-24-q31-emergency-closure-kickoff.md` | Emergency governance kickoff event for Q31 closure package |
| — | `tools/run_mempalace_longmemeval_docker.sh` | Docker-only LongMemEval dry-run runner for Q29 evidence collection |
| — | `tools/security_checks_onnx.sh` | ONNX version/pattern security checks for CVE risk controls |
| — | `templates/LOI-SolarSeed-Template.md` | Letter of Intent template for customer pre-assessment |
| — | `templates/KB-Domain-Document-Template-v1.md` | Reusable metadata-first template for new domain documents |
| — | `templates/KB-Governance-Event-Template-v1.md` | Reusable template for governance workflow event records |

---

## Data Sources

- **Primary**: 6 project transcripts (sales, marketing, business-model, system-description, strategy-overall, strategy-pdf), structure.md, Renew Iberia pitch deck, SolDevlist.csv
- **Technical**: Technical-Description.SolarSeed.BaseConfiguration.md v2.0, FilantropiaSolar-Technical-Description.md (platform architecture)
- **Financial**: OpEx-CapEx-Table-1.csv, P-L-Q-Table-1.csv, SolarSeed_avg-Table-1.csv, SolarSeed_base-Table-1.csv
- **Partner docs**: PROSUNIFIED-GROUP-TECH_OVERVIEW (Oct 2024), Sunified-Group-BV-CC-Forum-TECH-OVERVIEW (Jan 2025 Davos) — Commercial in Confidence
- **Website**: wera.global (home, /products, /about, /solarseed) — last fetched April 2026
- **Web research**: DePIN market reports, Portugal energy data, partner company profiles, EU regulatory frameworks, hardware vendor specs (AIKO, Huawei, GEEKOM, Voltronic)
- **Academic**: 40+ papers on DePIN, blockchain energy communities, tokenization governance, energy-aware edge computing (MDPI, IEEE, Frontiers, arXiv, Nature)
- **Social**: LinkedIn (WeRa Global, Iberia Renew Engineering), X (@wera_global)
