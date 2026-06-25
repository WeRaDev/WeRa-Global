# Torres Vedras Pilot — Technical Runtime Brief + Working Evidence Review

## Consolidation provenance
- consolidation_actor: `WARP`
- consolidation_source: `/Users/mikhailananyin/Documents/WeRa Global/KB-latest-original/Strategy/Business-Model/SolarSeed.pilot.tv.md`
- consolidation_date: `2026-06-22`
- consolidation_status: `canonicalized`


## 0) Review scope and method
- Scope reviewed: prior technical synthesis / pilot review against `torres-vedras-pilot-questionnaire.md`.
- Method markers (from questionnaire): `FACT`, `MEMORY`, `ESTIMATE`, `UNKNOWN`.
- Evidence policy used here: only statements traceable to currently available documents were treated as `FACT`.

## FPF status note
- This file is a **supporting technical/runtime brief**, not the canonical commercial fact sheet.
- The canonical pilot status is controlled by `torres-vedras-pilot-questionnaire.md`, `claim-register.md` and `executed-vs-designed.md`.
- Founder-update items below keep their original evidence status (`MEMORY`, `FACT/MEMORY`, `ESTIMATE`); they must not be upgraded to `FACT` until payment, contract, telemetry or signed carriers are attached.
- References to `ProductionBase/...` are legacy source paths from the prior technical review and are **not verified as live workspace paths** in the current package.
- This pilot must not be used as proof of the future grid-connected UPAC / final-consumer / fixed-service-fee baseline. Current records point to an off-grid / no-supplier-contract context, so the legal proof boundary is narrower.

## Review verdict
- **Accuracy:** medium-high for technical/runtime parts; medium for business/commercial statements.
- **Completeness:** partial.
  - Strongly covered: technical architecture baseline, TRL5 host runtime snapshot, some pilot context.
  - Weak or missing: legal counterparties, contract/payment trail, ownership mechanics, measured savings baseline, maintenance history, user perception.
- Practical conclusion: prior version is a good **technical brief**, but not yet a **reality-grade pilot fact sheet** under the questionnaire standard.

## Founder update (2026-04-23, to integrate into next full revision)
- `MEMORY` Pilot status confirmed as: **technical/executed proof, not full commercial proof**.
- `MEMORY` Initial monthly-rent intent existed, but founder-reported working version shifted to **client-funded CapEx**.
- `MEMORY` Conditional commercial path was stated: after WeRa funding, possible **buy-back** of equipment and re-sale to client on monthly cost.
- `FACT/MEMORY` Client has no energy-supplier contract; bill-vs-bill savings baseline is unavailable.
- `ESTIMATE` Savings proxy should be calculated as: average monthly generation × grid price vs component cost (source reference: `solar.seed.components.csv`, to be attached).
- `MEMORY` Maintenance: field maintenance happened in January after storms; digital maintenance is weekly.

## Torres Vedras working evidence snapshot v1 (2026-04-23)

- `MEMORY` Object status: **technical/executed proof, not full commercial proof**.
- `MEMORY` Commercial path in founder-reported working version: intent started as monthly rent; executed path shifted to client-funded CapEx with a stated conditional future buy-back and re-sale at monthly cost once WeRa Global is funded.
- `MEMORY` Agreement status: founder reports verbal agreement; written agreement can be signed at any moment, but is not yet executed in this package.
- `FACT/MEMORY` Savings baseline constraint: no supplier contract available, so bill-vs-bill method is not possible for this site.
- `FACT/MEMORY` Legal-baseline constraint: because no ordinary supplier-contract baseline is available, this site does not prove customer-as-final-consumer treatment inside a grid-connected UPAC structure.
- `ESTIMATE` Allowed proxy method: average monthly generation × grid price, then compare against component cost baseline from `Strategy/Business-Model/solar.seed.components.csv`.
- `MEMORY` Maintenance baseline: 30 January maintenance check after storms found the system operational with no fixes required; digital maintenance is reported as weekly.

### Missing carriers before external-grade claiming

- `OPEN` Executed written agreement artifact (or equivalent signed written memorialization).
- `OPEN` Payment trail by component / installer / logistics.
- `OPEN` Ownership/control/removal memo separating payer, title-holder, operator and de-installation rights.
- `OPEN` Telemetry export and explicit proxy-savings worksheet based on measured average monthly generation.
- `OPEN` Structured maintenance ledger with dated entries (starting with 30 January check).

## Accuracy corrections to prior version
1. `FACT` CAPEX `€5,001.26` is a **baseline BOM reference** (`components.csv` lineage), not yet proven as exact realized CAPEX of the Torres Vedras pilot.
2. `FACT` ARS Sustineri numbers (3–5 x 200W, 2.3–3.8 kWh/day usable) are an **origin model**, not proof of current as-installed field configuration.
3. `FACT` “1 live pilot in Torres Vedras” appears in WeRa-Global-KB summaries, but pilot commercial status (contract, recurring payments, legal wrapper) is not evidenced in reviewed files.
4. `FACT` runtime/service findings on `wera-ss-pt-tv-1` are **snapshot-specific** (dated in TRL5 reference), not longitudinal performance proof.

## 1) Questionnaire-aligned fact sheet (current known state)

### 1.1 Baseline identification
**Answer**
- `FACT` Internal object identity used in sources: Torres Vedras pilot / `wera-ss-pt-tv-1` field host context.
- `ESTIMATE` Most precise current label (based on evidence available): **founder-built live installation / customer installation with incomplete commercial wrapper**.
- `FACT` Potentially misleading label at this stage: “fully validated commercial pilot with proven repeatable economics.”

**Evidence carrier**
- `WeRa-Global-KB/01-Company-Overview.md`
- `WeRa-Global-KB/07-Customers-and-GTM.md`
- `ProductionBase/SolarSeed-v3/docs/reference/Technical Description.TRL5.md`

**Confidence**
- medium

### 1.2 Location and type
**Answer**
- `FACT` Location described as Torres Vedras, Portugal.
- `FACT` Type described as off-grid micro-farm / small household-equivalent private property.
- `UNKNOWN` Exact postal address and cadastral/legal site details were not found in reviewed files.
- `UNKNOWN` Definitive current electrical regime classification (strict off-grid vs hybrid fallback) was not explicitly evidenced beyond narrative wording.

**Evidence carrier**
- `WeRa-Global-KB/07-Customers-and-GTM.md`
- `WeRa-Global-KB/00-Glossary.md`

**Confidence**
- medium

### 1.3 Chronology
**Answer**
- `FACT` TRL5 technical snapshot date: 2026-04-07.
- `UNKNOWN` Idea start date, procurement date, installation date, go-live date, upgrade timeline (not found with evidence in reviewed corpus).

**Evidence carrier**
- `ProductionBase/SolarSeed-v3/docs/reference/Technical Description.TRL5.md`

**Confidence**
- high (for snapshot date), high (that broader chronology is currently unknown)

### 2) Parties and counterparty reality
**Answer**
- `UNKNOWN` Named beneficiary/user identity, legal decision-maker, payer identity for this specific site.
- `UNKNOWN` Relationship category (external client vs friend/family/affiliate vs founder-owned site) not explicitly documented in evidence scanned.
- `UNKNOWN` Formal legal counterparty for this specific pilot.

**Evidence carrier**
- No direct counterparty dossier found in reviewed files.

**Confidence**
- high

### 3) What is installed
**Answer**
- `FACT` Origin architecture references: ARS Sustineri off-grid stack (panels + MPPT + inverter + battery).
- `FACT` TRL5 host runtime evidence exists for compute/ops stack (Debian host, Nextcloud, Prometheus, Grafana, inverter-exporter, Tailscale ingress).
- `UNKNOWN` Exact as-installed energy hardware BOM at Torres Vedras site today (panel model/count, inverter model, battery model/capacity) with direct installation proof.
- `UNKNOWN` Full change log (added/replaced/failed components over time).

**Evidence carrier**
- `ProductionBase/SolarSeed-v3/docs/reference/ARS Sustineri.odt`
- `ProductionBase/SolarSeed-v3/docs/reference/Technical Description.SolarSeed.BaseConfiguration.md`
- `ProductionBase/SolarSeed-v3/docs/reference/Technical Description.TRL5.md`

**Confidence**
- medium

### 4) CAPEX and source of funds
**Answer**
- `FACT` Reference baseline CAPEX appears in product references (`€5,001.26` baseline BOM).
- `UNKNOWN` Actual paid CAPEX for Torres Vedras pilot.
- `UNKNOWN` Who paid each subsystem, logistics, and installation in factual breakdown.
- `UNKNOWN` Post-purchase ownership rights by component.

**Evidence carrier**
- `ProductionBase/SolarSeed-v3/docs/reference/Technical Description.SolarSeed.BaseConfiguration.md`
- `WeRa-Global-KB/02-Products.md`

**Confidence**
- medium (reference CAPEX), high (unknown actual payment trail)

### 5) Legal and contractual reality
**Answer**
- `UNKNOWN` Signed contract for this pilot (lease/service/loan/installation agreement).
- `UNKNOWN` Site-right basis and explicit dismantling rights.
- `UNKNOWN` Liability/insurance allocation for this specific installation.

**Evidence carrier**
- No pilot-specific legal artifact found in reviewed files.

**Confidence**
- high

### 6) Commercial reality (payments)
**Answer**
- `UNKNOWN` Upfront payment by pilot user (if any).
- `UNKNOWN` Recurring payment amount/frequency/history for this site.
- `FACT` Generic model claims exist in product docs (e.g., symbolic €1 and leasing logic), but these are **not** evidence of executed payment behavior for Torres Vedras.

**Evidence carrier**
- `WeRa-Global-KB/02-Products.md`
- `WeRa-Global-KB/07-Customers-and-GTM.md`

**Confidence**
- high

### 7) Technical data and telemetry
**Answer**
- `FACT` Live/runtime signals were documented in TRL5 snapshot:
  - Nextcloud status endpoint over tailnet,
  - Prometheus targets,
  - inverter-exporter metrics samples,
  - service and port observations.
- `UNKNOWN` Longitudinal dataset completeness (daily/monthly generation/consumption, full outage history, structured maintenance log).
- `UNKNOWN` Export package availability and retention window for all KPIs.

**Evidence carrier**
- `ProductionBase/SolarSeed-v3/docs/reference/Technical Description.TRL5.md`
- `WeRa-Global-KB/16-FilantropiaSolar-Platform.md`

**Confidence**
- high for snapshot facts; medium-low for longitudinal completeness

### 8) Savings and economics
**Answer**
- `UNKNOWN` Baseline pre-install bills for this specific site.
- `UNKNOWN` Measured post-install savings evidence (monthly/annual comparison) for this specific site.
- `FACT` “20% minimum savings” appears as product-level positioning in KB/strategy context, but pilot-specific measured savings evidence was not found in reviewed files.

**Evidence carrier**
- `WeRa-Global-KB/02-Products.md`
- `WeRa-Global-KB/07-Customers-and-GTM.md`
- `WeRa-Global-KB/14-KB-Audit-v1.1.md` (references of guarantee wording context)

**Confidence**
- high

### 9) Incidents, support, maintenance
**Answer**
- `FACT` Technical constraints observed in TRL5 snapshot (e.g., docker group access limitation for `wera-admin`, `/data` mount note, auth-gated service on `:3000`).
- `UNKNOWN` Historical incident ledger (downtime/failure history/weather incidents) with dates and resolutions.
- `UNKNOWN` Formal maintenance burden and who paid replacement events.

**Evidence carrier**
- `ProductionBase/SolarSeed-v3/docs/reference/Technical Description.TRL5.md`

**Confidence**
- medium

### 10) User/commercial meaning
**Answer**
- `UNKNOWN` User perception category (own system vs service vs temporary experiment) and referral willingness.
- `ESTIMATE` External-sale readiness of current evidence package is limited; commercial wrapper appears incomplete.

**Evidence carrier**
- No direct user interview or signed customer feedback artifact found.

**Confidence**
- low-medium

### 11) What Torres Vedras currently proves vs does not prove
**11.1 What it proves (`FACT`)**
- A field node exists with real runtime stack and remote operations path.
- Energy telemetry integration was implemented (inverter-exporter + Prometheus target).
- The project can connect ARS/SolarSeed architecture concepts to a deployed runtime host.

**11.2 What it does not prove yet (`FACT` / `UNKNOWN`)**
- Repeatable commercial baseline across customers.
- Contractually clean service-fee model for this site.
- Verified recurring payment behavior.
- Grid-connected UPAC / final-consumer wrapper for future contracts.
- Auditable measured savings with before/after bill-grade evidence.
- Finance-ready, diligence-grade portfolio trail for this pilot.

**11.3 Safe wording options**
- `internal truthful version`: “We have a real Torres Vedras pilot runtime with technical evidence, but commercial/legal/payment proof set is incomplete.”
- `investor-safe version`: “We have one live pilot deployment in Torres Vedras with telemetry and operations evidence; commercialization evidence is being formalized into an auditable fact sheet.”
- `regulator/counsel-safe version`: “Current records confirm technical deployment and operation signals; contractual/payment/ownership evidence requires consolidation before legal characterization.”

### 12) Artifact retrieval checklist (questionnaire format)
- фото объекта: **неизвестно**
- фото оборудования: **неизвестно**
- список компонентов: **есть** (reference-level, not yet fully site-verified)
- invoice / receipt / payment trail: **неизвестно**
- договор / переписка про условия: **неизвестно**
- телеметрия / screenshots: **можно достать** (runtime endpoints/monitoring evidence)
- bills / cost comparison: **неизвестно**
- maintenance notes: **скорее нет** (structured log not found)
- contact details involved persons: **неизвестно**
- site diagram / one-line diagram: **скорее нет** (not found in reviewed set)

### 13) Short summary (5–10 lines)
Torres Vedras appears to be a real pilot deployment with technical runtime evidence on `wera-ss-pt-tv-1` and documented telemetry integration.  
The previous synthesis was technically accurate in many points, but it overstated completeness for commercial/legal reality.  
Reference CAPEX and ARS model data exist, but they are not yet enough to claim audited realized pilot economics.  
No direct contract/payment/ownership dossier for the specific site was found in the reviewed materials.  
Measured savings baseline vs post-install evidence is currently missing from the assembled fact package.  
At this stage, safest classification is technical/operationally evidenced pilot with incomplete commercial wrapper.  
To make this externally diligence-ready, priority is to collect payment trail, legal agreement basis, named counterparties, and longitudinal performance/savings exports.

### 14) Read together with
- `torres-vedras-pilot-questionnaire.md`
- `WeRa-Global-KB/07-Customers-and-GTM.md`
- `WeRa-Global-KB/02-Products.md`
- `ProductionBase/SolarSeed-v3/docs/reference/Technical Description.TRL5.md`
- `ProductionBase/SolarSeed-v3/docs/reference/Technical Description.SolarSeed.BaseConfiguration.md`
- `ProductionBase/SolarSeed-v3/docs/reference/ARS Sustineri.odt`

---
## Appendix A — Technical synthesis (from prior version)
### SolarSeed Pilot Run — Torres Vedras (ARS Sustineri / TRL5)

## 1) Pilot identity and scope
- Target pilot: **SolarSeed field run in Torres Vedras, Portugal** (user request used spelling “Torres Vedres”; canonical spelling in source docs is **Torres Vedras**).
- Project lineage: **ARS Sustineri** (small off-grid farm autonomy model) -> evolved into **SolarSeed TRL5 field deployment**.
- TRL5 primary host: **`wera-ss-pt-tv-1`**  
  - Tailscale FQDN: `wera-ss-pt-tv-1.tailfb390c.ts.net`  
  - Tailscale IP: `100.82.252.18`
- TRL5 snapshot reference date in technical doc: **2026-04-07**.

## 2) Torres Vedras pilot context (business + site profile)
- Pilot customer/site is consistently described as:
  - **Off-grid micro-farm**
  - **Private property**
  - **Small household equivalent (~2 people)**
  - **Location: Torres Vedras, Portugal**
- Portfolio positioning in WeRa docs:
  - Current live customers: **1 pilot (Torres Vedras)**.
  - Pipeline references include additional proposals/estimated leads, but only one confirmed live pilot in this location.

## 3) ARS Sustineri baseline (origin model for the pilot)
### 3.1 Mission and use case
- ARS Sustineri defines a farm-focused sustainability plan where the off-grid solar system powers:
  - water pumping,
  - lighting,
  - small appliances,
  - with independence from conventional grid supply.

### 3.2 Solar resource and production assumptions (Torres Vedras)
- Average irradiance used: **4.5 kWh/m²/day** (Solar Global Atlas reference in document).
- Panel scenarios (200W modules):
  - **3 panels** -> 600W installed -> **2.7 kWh/day** estimated production
  - **4 panels** -> 800W installed -> **3.6 kWh/day**
  - **5 panels** -> 1000W installed -> **4.5 kWh/day**
- System losses considered: **15–20%**, resulting usable output range around:
  - **~2.3 to 3.8 kWh/day** (notably for upper scenario after losses).

### 3.3 Baseline system architecture in ARS
- Core components:
  - PV panels (3–5 x 200W),
  - MPPT converter,
  - inverter (DC -> AC),
  - battery bank,
  - charge controller + breakers.
- Battery sizing example in source:
  - 12V, 200Ah battery ~**2.4 kWh** storage;
  - storing ~4.5 kWh/day scenario requires **at least two** such batteries.

### 3.4 Physical implementation details in ARS
- Structure footprint: **3.10m x 3.20m** (~9.92 m² roof area).
- Typical panel size used for layout assumptions: ~**1.7m x 1m**.
- Roof capacity planning notes:
  - 3 panels fit comfortably;
  - 4 panels possible with tighter spacing.
- Orientation guidance:
  - tilt **30–35°**,
  - south-facing alignment (northern hemisphere assumption in doc).
- Additional practical notes:
  - roof strength and wind load checks,
  - waterproofing at mounts,
  - weatherproof cable conduits,
  - battery room ventilation and electrical protection.

### 3.5 Farm-system coupling
- Solar system is explicitly coupled to well-pump operation.
- Pump compatibility checks required against inverter voltage/power.
- If pump demand exceeds production, scaling path is documented:
  - add more panels and/or larger battery bank.

## 4) SolarSeed product mapping to ARS baseline
- SolarSeed technical baseline documents map ARS as reference **[R2]** and define ARS-derived **S-Profile**:
  - **0.6–1.0 kWp**
  - **~2.3–3.8 kWh/day usable output**
  - use case: irrigation pumping, basic lighting, minimal digital layer.
- SolarSeed control principle maintained:
  - **“Energy budget before compute budget.”**
- This confirms continuity from ARS farm autonomy intent into productized SolarSeed sizing logic.

## 5) TRL5 field machine (`wera-ss-pt-tv-1`) — observed runtime state
### 5.1 Compute and OS
- Hardware: **GEEKOM A6**.
- CPU: **AMD Ryzen 7 6800H** (16 logical CPUs / 8 cores SMT).
- RAM observed: ~**27 GiB** visible.
- OS: **Debian GNU/Linux 13.2 (trixie)**.
- Kernel: `6.12.57+deb13-amd64`.
- Uptime at capture: **54 days**.

### 5.2 Storage
- Disk: `nvme0n1` ~953.9G (KINGSTON OM8PGP41024N-A0).
- Root usage at snapshot: **134G used / 731G available (~16%)**.
- `/data` mount state in TRL5 snapshot: **not mounted** (flagged in doc for review).

### 5.3 Network and access
- LAN (`wlan0`): `192.168.1.132/24`.
- Tailscale (`tailscale0`): `100.82.252.18/32`.
- Tailnet: `tailfb390c.ts.net`.
- SSH service active on port 22.

### 5.4 Platform/runtime services
- Docker stack available:
  - Docker Engine `29.1.2`
  - Compose plugin `v5.0.0`
  - containerd `2.2.0`
- Tailscale version: `1.96.4`.
- Python version observed: `3.13.5`.

### 5.5 Observability and energy telemetry
- Running observability services:
  - `prometheus.service` (`2.53.3+ds1`)
  - `prometheus-node-exporter.service` (`1.9.0`)
  - `grafana-server.service` (`12.3.0`)
  - `inverter-exporter.service` (custom Python exporter, `:9105/metrics`)
- Prometheus jobs include:
  - `prometheus`, `node`, `nextcloud`, `inverter`
  - all reported **UP** at snapshot.

### 5.6 Nextcloud deployment evidence on TRL5 host
- Nextcloud appears active via AIO-style process signals.
- Status endpoint evidence:
  - `installed: true`
  - `maintenance: false`
  - `needsDbUpgrade: false`
  - version observed: **`32.0.2.2` (`versionstring 32.0.2`)**
- Tailnet ingress pattern:
  - `https://wera-ss-pt-tv-1.tailfb390c.ts.net` -> proxy to `http://127.0.0.1:11000`.

### 5.7 Port and endpoint checks (TRL5 snapshot)
- Listening ports observed include: `22, 80, 443, 3000, 8080, 8443, 9090, 9100, 9105, 9205, 3478, 20000`.
- Endpoint checks reported:
  - Prometheus ready: OK (`200`)
  - inverter metrics endpoint: returns metrics
  - `localhost:4200/api/health`: not listening
  - `localhost:8081/health`: not listening
  - `localhost:3000/api/healthz`: `401` (service reachable, auth required)
  - tailnet Nextcloud status URL: returns JSON status.

### 5.8 Live energy telemetry examples captured
- `inverter_battery_voltage_volts 24.55`
- `inverter_battery_capacity_percent 83`
- `inverter_pv_in_watts 0.0` (night snapshot context in doc)
- `inverter_ac_out_voltage_volts 229.0`

## 6) Cost baseline retained into TRL5 documentation
- Components baseline retained from SolarSeed references:
  - Energy subsystem: **€3,450.53** (~69%)
  - Compute subsystem: **€1,550.73** (~31%)
  - Total baseline CAPEX: **€5,001.26**
- TRL5 document notes baseline remains useful for planning, while live host hardware differs from earlier assumptions.

## 7) TRL delta summary (as documented)
### 7.1 TRL5 improvements over conceptual baseline
- Operational field node with sustained uptime.
- Mature observability stack with inverter telemetry integrated.
- Tailnet-only ingress for remote operations.
- Live Nextcloud instance with confirmed runtime version.

### 7.2 Differences vs prior TRL4 assumptions in docs
- Services expected in some TRL4 profiles (`:4200`, `:8081`) were not active in the specific TRL5 snapshot.
- Port `:9105` used by inverter exporter in TRL5 context (not Spirit API in this snapshot).

## 8) Constraints and risks explicitly noted in TRL5 doc
- SSH operator account `wera-admin` not in `docker` group (limits non-interactive container inventory).
- `/data` mount absent at capture (needs operational review).
- Auth-gated service on port `3000` detected but not fully identified in that inventory pass.
- Follow-up recommendation in source: perform privileged container inventory (`docker ps`, `docker inspect`, compose-level `ps`) and append container-level appendix.

## 9) Source corpus used for this synthesis
- `ProductionBase/SolarSeed-v3/docs/reference/Technical Description.TRL5.md`
- `ProductionBase/SolarSeed-v3/docs/reference/Technical Description.SolarSeed.BaseConfiguration.md`
- `ProductionBase/SolarSeed-v3/docs/reference/ARS Sustineri.odt` (extracted to text for analysis)
- `WeRa-Global-KB/00-Glossary.md`
- `WeRa-Global-KB/01-Company-Overview.md`
- `WeRa-Global-KB/02-Products.md`
- `WeRa-Global-KB/04-System-Architecture.md`
- `WeRa-Global-KB/07-Customers-and-GTM.md`
- `WeRa-Global-KB/16-FilantropiaSolar-Platform.md`
- `WeRa-Global-KB/README.md`

formal_proof:
  engine: ml-hilbert
  trl_phase: TRL6
  obligation_id: kb.customers.cases_46_torres_vedras_runtime_evidence_brief_v1
  proof_artifact: kb-governance/formal-proofs/customers-cases-46-torres-vedras-runtime-evidence-brief-v1.lean
  verification_status: verified
