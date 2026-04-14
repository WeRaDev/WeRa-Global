---
# KB-memPalace-upgrade.md
# PURPOSE: AI-agent implementation specification for the WeRa Global Knowledge Base upgrade.
# This file encodes all research, architectural decisions, intent, and directives
# needed for an AI agent to verify, validate, and implement the Mind Palace KB.
# Format: machine-readable YAML front matter + human-readable Markdown body + agent directives.
# Authored: 2026-04-14 | Version: 1.0.0 | Owner: WeRa Global / FilantropiaSolar
---

## AGENT DIRECTIVE HEADER

```yaml
agent_directive:
  document_type: KB_IMPLEMENTATION_SPEC
  version: "1.0.0"
  date: "2026-04-14"
  organisation: "WeRa Global / FilantropiaSolar"
  location: "Lisbon, Portugal"
  primary_goal: >
    Restructure the WeRa Global knowledge base into a MemPalace-based
    mind palace that is equally navigable by human operators and AI agents.
    The KB is the Single Source of Truth (SSOT) for the entire organisation.
  implementation_steps:
    - VERIFY: Read and parse this entire file before acting
    - VALIDATE: Cross-check against existing KB structure if available
    - SCAFFOLD: Create directory and file skeleton per wing_config
    - POPULATE: Mine existing documents and conversations into palace rooms
    - LINK: Establish tunnel cross-references between wings
    - ACTIVATE: Deploy specialist agents and MCP server
    - GOVERN: Apply lifecycle policies and steward assignments
  constraints:
    - All data stored locally (sovereign self-hosting, no cloud)
    - Private customer data stored in encrypted vault OUTSIDE palace
    - Anonymised data ONLY enters palace drawers
    - KB language: English (primary), Portuguese (secondary for local operations)
  toolchain:
    memory_system: MemPalace (https://github.com/mempalace/mempalace)
    vector_db: ChromaDB (local)
    graph_db: SQLite (local, RDF-style triples)
    wiki_surface: Notion or MediaWiki (human-facing layer)
    ai_agents: MCP-compatible (Claude, local LLMs)
    benchmark: LongMemEval R@5 = 96.6% raw, 100% with reranking
```

---

## SECTION 1 — CONTEXT AND INTENT

### 1.1 Organisation Profile

WeRa Global operates the FilantropiaSolar project in Portugal, offering:

- **Solar Seed**: base solar + edge server station for energy sovereignty (non-habitable land, enterprises, households)
- **Vera Cloud**: sovereign digital self-hosting services
- **Marketplace layer**: third-party services (gardening, pool, security, irrigation) added to core offers
- **Core value proposition**: "Sustainable sovereign self-hosting at a cheaper price" — minimum 20% discount on average monthly electricity bill

Target customers (two initial segments):

1. **Mindful Prosumers**: aware of energy crisis, funding-constrained, not ready for full CapEx investment → reachable via LinkedIn, Instagram, Facebook, installer networks
2. **Enterprise Sustainability Seekers**: organisations seeking energy independence and ESG compliance

Crisis trigger documented: 2025 Portugal storms left 150,000+ households/organisations without electricity overnight → emergency market event that must be captured as a founding entry in `wing_problems`.

### 1.2 The KB Upgrade Intent

The existing KB is unstructured and does not serve as an operational intelligence system. The upgrade intent is:

> "Reorganise our knowledge base, specifically targeting business model. Our knowledge base is a source of truth used for entire organisation, operations, and coordination. The knowledge base should be constructed as some sort of business Wikipedia with cross-references across all documents."
>
> "In the future [the KB should be] one unified Wikipedia of WeRa Global business organisation, including business, finance, public relations."

**Implementation principle**: The KB is not a filing system. It is the organisation's second brain — a temporal, cross-referenced, AI-queryable mind palace that preserves every decision, case, discovery, and event with zero context loss.

### 1.3 Why MemPalace

MemPalace is the chosen implementation engine because:

- **Highest-scoring open-source AI memory system**: 96.6% R@5 on LongMemEval with zero API calls; 100% with reranking
- **Palace structure alone produces +34% retrieval improvement** over flat vector search (60.9% → 94.8%)
- **Fully local**: ChromaDB + SQLite, no cloud dependency — consistent with WeRa's sovereign self-hosting philosophy
- **MIT licensed**: free to deploy, modify, extend
- **Dual-readable**: human-navigable wiki surface + machine-traversable MCP tools (19 tools)
- **Temporal KG**: RDF-style triples with validity windows capture business relationship evolution over time

---

## SECTION 2 — ARCHITECTURAL SPECIFICATION

### 2.1 The Six Spatial Layers

```
PALACE (WeRa Global)
├── WING        → BMC/Lean domain (12 wings, see Section 3)
│   ├── ROOM    → Specific topic within domain
│   │   ├── HALL        → Memory type corridor (5 halls, same in every wing)
│   │   │   ├── CLOSET  → Summary pointer to source content
│   │   │   └── DRAWER  → Verbatim original content (never summarised away)
│   └── TUNNEL  → Bidirectional link to same room concept in another wing
```

**HALLS (universal, present in every wing):**

| Hall | Purpose | WeRa Examples |
|---|---|---|
| `hall_facts` | Locked decisions, established truths | Product specs, pricing logic, policy decisions |
| `hall_events` | Sessions, milestones, executed actions | Customer installs, outreach campaigns, partner meetings |
| `hall_discoveries` | Insights, breakthroughs, market learnings | Storm crisis → new customer segment found |
| `hall_preferences` | Customer/partner/operator preferences | Installer turnaround expectations, payment terms |
| `hall_advice` | Recommendations, solutions, quotes | Partner RFQ responses, installer recommendations |

**TUNNELS**: Auto-connecting the same concept across wings. A tunnel is created whenever the same named entity (case ID, product name, event) appears in two or more wings. This replaces manual cross-referencing.

### 2.2 The 4-Layer Memory Stack

```
L0  IDENTITY     (~50 tokens)   → Always loaded. WeRa mission, products, team.
L1  CRITICAL FACTS (~120 tokens) → AAAK-compressed. Active segments, offers, partners, KPIs.
L2  ROOM RECALL   (on demand)   → Active case context, current campaign, open negotiation.
L3  DEEP SEARCH   (on demand)   → Semantic query across all closets and drawers.
```

**L0 template for WeRa** (populate during `mempalace init`):

```
WeRa Global | Solar + Digital Sovereignty | Lisbon, Portugal
Products: Solar Seed (energy self-hosting), Vera Cloud (digital self-hosting)
Customers: Prosumers (funding-constrained), Enterprises (ESG)
Partners: Solar installers PT network | Lead-gen platforms | Marketplace vendors
KB: ~/.mempalace/palace | SSOT: This palace | Private data: encrypted vault (separate)
Value prop: Sovereign self-hosting ≥20% cheaper than grid bill
```

**L1 AAAK entity registry** (populate during `mempalace init`):

```yaml
aaak_entities:
  # Customer segments
  PRO: prosumer
  ENT: enterprise
  # Products
  SS: solar-seed
  VC: vera-cloud
  # Channels
  LI: linkedin
  EM: email
  WF: website-form
  PR: partner-referral
  LG: lead-gen-bot
  # Revenue model
  LSE: leasing
  # Status codes
  QUL: qualified
  QTD: quoted
  INS: installed
  OPR: operational
  # Rating
  "★": low-outcome
  "★★": medium-outcome
  "★★★": good-outcome
  "★★★★": excellent-outcome
```

### 2.3 Tunnel Architecture

Tunnels are the cross-referencing backbone. Every shared named entity automatically creates a tunnel:

**Mandatory tunnel patterns for WeRa:**

```
# Per-case tunnels (one tunnel set per customer case)
wing_customers  / hall_events    / case-{id}  ↔  wing_partners / hall_events / case-{id}
wing_customers  / hall_events    / case-{id}  ↔  wing_revenue  / hall_events / case-{id}
wing_customers  / hall_events    / case-{id}  ↔  wing_metrics  / hall_events / case-{id}
wing_channels   / hall_events    / case-{id}  ↔  wing_customers / hall_events / case-{id}

# Per-product tunnels
wing_value-prop / hall_facts     / {product}  ↔  wing_solutions / hall_facts  / {product}
wing_value-prop / hall_facts     / {product}  ↔  wing_costs     / hall_facts  / {product}
wing_value-prop / hall_facts     / {product}  ↔  wing_resources / hall_facts  / {product}
wing_value-prop / hall_facts     / {product}  ↔  wing_revenue   / hall_facts  / {product}

# Per-event tunnels (crisis, campaigns, milestones)
wing_problems   / hall_events    / {event}    ↔  wing_solutions  / hall_discoveries / {event}
wing_problems   / hall_events    / {event}    ↔  wing_channels   / hall_events      / {event}
wing_problems   / hall_events    / {event}    ↔  wing_customers  / hall_discoveries / {event}

# Per-partner tunnels
wing_partners   / hall_facts     / {partner}  ↔  wing_channels   / hall_facts / {partner}
wing_partners   / hall_advice    / {partner}  ↔  wing_costs      / hall_facts / {partner}
```

---

## SECTION 3 — WING CONFIGURATION (12 WINGS)

### 3.1 Wing Registry

```json
{
  "palace": "wera-global",
  "created": "2026-04-14",
  "wings": {
    "wing_customers": {
      "bmc_element": "Customer Segments",
      "canvas_type": "both",
      "keywords": ["customer", "prosumer", "enterprise", "case", "install", "profile", "segment"],
      "steward": "customer-success-role",
      "review_cadence": "quarterly",
      "rooms": [
        "prosumer-profile",
        "enterprise-profile",
        "installation-cases",
        "case-builder-output",
        "crm-anonymised-data"
      ],
      "private_data_note": "Raw customer PII stored in encrypted vault only. Palace contains anonymised entries."
    },
    "wing_channels": {
      "bmc_element": "Channels",
      "canvas_type": "both",
      "keywords": ["linkedin", "email", "website", "form", "outreach", "campaign", "partner-referral", "lead-gen"],
      "steward": "growth-operations-role",
      "review_cadence": "after-each-campaign",
      "rooms": [
        "linkedin-skill",
        "email-skill",
        "website-forms-skill",
        "partner-referral-skill",
        "lead-gen-bot-skill",
        "channel-metrics"
      ],
      "skill_note": "Each room contains an executable skill file for AI agents or human operators."
    },
    "wing_value-prop": {
      "bmc_element": "Value Propositions",
      "canvas_type": "both",
      "keywords": ["solar-seed", "vera-cloud", "offer", "product", "proposition", "sovereignty", "self-hosting"],
      "steward": "product-role",
      "review_cadence": "on-product-change",
      "rooms": [
        "general-value-concept",
        "solar-seed-product-line",
        "vera-cloud-product-line",
        "offer-layer-3-configurator",
        "marketplace-extensions"
      ],
      "three_layer_note": "Layer 1=general concept, Layer 2=product line, Layer 3=configured offer (output of case-builder script)"
    },
    "wing_revenue": {
      "bmc_element": "Revenue Streams",
      "canvas_type": "traditional",
      "keywords": ["leasing", "invoice", "pricing", "bill", "discount", "taxation", "payment", "monthly"],
      "steward": "finance-role",
      "review_cadence": "on-pricing-change",
      "rooms": [
        "leasing-model",
        "invoice-templates",
        "taxation-PT",
        "bill-discount-logic",
        "payment-conditions"
      ],
      "pricing_rule": "Base leasing amount must produce minimum 20% discount vs customer average monthly bill."
    },
    "wing_partners": {
      "bmc_element": "Key Partners",
      "canvas_type": "traditional",
      "keywords": ["installer", "partner", "rfq", "quote", "lead-gen", "marketplace", "third-party"],
      "steward": "partnerships-role",
      "review_cadence": "monthly",
      "rooms": [
        "solar-installers-PT",
        "lead-gen-platforms",
        "marketplace-vendors",
        "third-party-services"
      ]
    },
    "wing_resources": {
      "bmc_element": "Key Resources",
      "canvas_type": "traditional",
      "keywords": ["equipment", "panel", "inverter", "battery", "edge-server", "software", "spec"],
      "steward": "technical-role",
      "review_cadence": "on-product-change",
      "rooms": [
        "solar-panel-specs",
        "inverter-specs",
        "battery-specs",
        "edge-server-docs",
        "software-stack"
      ]
    },
    "wing_activities": {
      "bmc_element": "Key Activities",
      "canvas_type": "traditional",
      "keywords": ["workflow", "process", "sop", "installation", "outreach", "case-builder", "partner-coordination"],
      "steward": "operations-role",
      "review_cadence": "after-each-install-cycle",
      "rooms": [
        "installation-workflow",
        "case-builder-process",
        "partner-coordination-sop",
        "outreach-cycle-sop",
        "after-action-review-template"
      ]
    },
    "wing_costs": {
      "bmc_element": "Cost Structure",
      "canvas_type": "traditional",
      "keywords": ["capex", "opex", "cost", "margin", "equipment-cost", "leasing-calc"],
      "steward": "finance-role",
      "review_cadence": "quarterly",
      "rooms": [
        "capex-models",
        "opex-breakdown",
        "leasing-cost-calc",
        "margin-targets",
        "cost-per-install"
      ]
    },
    "wing_problems": {
      "bmc_element": "Problems (Lean Canvas)",
      "canvas_type": "lean",
      "keywords": ["crisis", "storm", "outage", "problem", "pain", "constraint", "funding"],
      "steward": "strategy-role",
      "review_cadence": "on-market-event",
      "rooms": [
        "grid-dependency-crisis",
        "funding-constraint-prosumers",
        "storm-events-PT",
        "emerging-crises"
      ],
      "founding_entry": "2025 Portugal storms: 150,000+ households/orgs lost electricity overnight. Filed in room: storm-events-PT, hall: hall_events."
    },
    "wing_solutions": {
      "bmc_element": "Solutions (Lean Canvas)",
      "canvas_type": "lean",
      "keywords": ["pilot", "mvp", "prototype", "solution", "iteration", "test"],
      "steward": "product-role",
      "review_cadence": "per-sprint",
      "rooms": [
        "solar-seed-mvp",
        "vera-cloud-mvp",
        "pilot-outcomes",
        "product-iterations",
        "emergency-response-protocols"
      ]
    },
    "wing_metrics": {
      "bmc_element": "Key Metrics (Lean Canvas)",
      "canvas_type": "lean",
      "keywords": ["kpi", "metric", "savings", "performance", "conversion", "retention", "nps"],
      "steward": "analytics-role",
      "review_cadence": "monthly",
      "rooms": [
        "kpi-definitions",
        "channel-performance-metrics",
        "installation-outcome-metrics",
        "customer-savings-tracking",
        "partner-performance-metrics"
      ]
    },
    "wing_governance": {
      "bmc_element": "Governance (Meta-layer)",
      "canvas_type": "meta",
      "keywords": ["policy", "steward", "governance", "access", "aaak-registry", "taxonomy", "lifecycle"],
      "steward": "kb-steward-role",
      "review_cadence": "quarterly",
      "rooms": [
        "aaak-entity-registry",
        "kb-policies",
        "steward-assignments",
        "update-cadences",
        "access-controls",
        "taxonomy-controlled-vocabulary"
      ]
    }
  }
}
```

---

## SECTION 4 — KNOWLEDGE GRAPH SCHEMA

### 4.1 Triple Patterns

All business relationships are encoded as temporal RDF-style triples:
`subject → predicate → object` with `valid_from` and optional `valid_until`.

**Customer case lifecycle triples:**

```python
# Registration
kg.add_triple("case-{id}", "segment",          "{PRO|ENT}",       valid_from="{date}")
kg.add_triple("case-{id}", "location_postcode", "{postcode}",      valid_from="{date}")
kg.add_triple("case-{id}", "buildable_area_sqm", "{value}",        valid_from="{date}")
kg.add_triple("case-{id}", "avg_monthly_bill_eur", "{value}",      valid_from="{date}")
kg.add_triple("case-{id}", "avg_daily_consumption_kwh", "{value}", valid_from="{date}")
kg.add_triple("case-{id}", "avg_night_consumption_kwh", "{value}", valid_from="{date}")

# Qualification
kg.add_triple("case-{id}", "channel_acquired", "{channel}",        valid_from="{date}")
kg.add_triple("case-{id}", "status",           "qualified",        valid_from="{date}")

# Quoting
kg.add_triple("case-{id}", "partner_assigned",  "{partner-id}",   valid_from="{date}")
kg.add_triple("case-{id}", "product_assigned",  "{product-id}",   valid_from="{date}")
kg.add_triple("case-{id}", "quoted_capex_eur",  "{value}",        valid_from="{date}")
kg.add_triple("case-{id}", "leasing_monthly_eur", "{value}",      valid_from="{date}")
kg.add_triple("case-{id}", "status",            "quoted",         valid_from="{date}")

# Installation
kg.add_triple("case-{id}", "install_date",      "{date}",         valid_from="{date}")
kg.add_triple("case-{id}", "status",            "installed",      valid_from="{date}")

# Operational
kg.add_triple("case-{id}", "savings_vs_baseline_pct", "{value}",  valid_from="{date}")
kg.add_triple("case-{id}", "status",            "operational",    valid_from="{date}")
```

**Product evolution triples:**

```python
kg.add_triple("{product-id}", "status",          "launched",      valid_from="{date}")
kg.add_triple("{product-id}", "avg_install_cost_eur", "{value}",  valid_from="{date}")
kg.add_triple("{product-id}", "avg_leasing_eur", "{value}",       valid_from="{date}")
kg.add_triple("{product-id}", "avg_savings_pct", "{value}",       valid_from="{date}")
# When value changes, invalidate old triple and add new:
kg.invalidate("{product-id}", "{predicate}", "{old_value}",       ended="{date}")
kg.add_triple("{product-id}", "{predicate}",  "{new_value}",      valid_from="{date}")
```

**Partner performance triples:**

```python
kg.add_triple("{partner-id}", "type",                "installer",  valid_from="{date}")
kg.add_triple("{partner-id}", "region_PT",           "{region}",   valid_from="{date}")
kg.add_triple("{partner-id}", "avg_turnaround_days", "{value}",    valid_from="{date}")
kg.add_triple("{partner-id}", "cases_completed",     "{count}",    valid_from="{date}")
kg.add_triple("{partner-id}", "avg_quote_eur",       "{value}",    valid_from="{date}")
```

**Event triples (crises, campaigns, milestones):**

```python
kg.add_triple("{event-id}", "type",            "{crisis|campaign|milestone}", valid_from="{date}")
kg.add_triple("{event-id}", "affected_region", "{region}",                    valid_from="{date}")
kg.add_triple("{event-id}", "triggered_wing",  "{wing-name}",                 valid_from="{date}")
kg.add_triple("{event-id}", "outcome",         "{description}",               valid_from="{date}")
```

---

## SECTION 5 — SPECIALIST AGENT DEFINITIONS

### 5.1 Agent Registry

Six specialist agents serve the WeRa palace. Each has its own diary and expertise domain.

```json
{
  "agents": {
    "case-builder-agent": {
      "primary_wing": "wing_customers",
      "secondary_wings": ["wing_partners", "wing_value-prop", "wing_revenue"],
      "responsibilities": [
        "Process raw customer data input",
        "Route PII to encrypted vault (outside palace)",
        "File anonymised profile to wing_customers / hall_events / case-{id}",
        "Add KG triples for new case",
        "Generate partner RFQ using wing_partners data",
        "Generate offer layer-3 using wing_value-prop pricing logic",
        "Calculate leasing amount ensuring ≥20% bill discount"
      ],
      "diary_format": "AAAK",
      "diary_example": "240414|case-001|PRO|SS|INS-N|bill=€185|lse=€143|svgs=23pct|★★★★"
    },
    "channel-agent": {
      "primary_wing": "wing_channels",
      "secondary_wings": ["wing_customers", "wing_metrics"],
      "responsibilities": [
        "Execute channel skill files (LinkedIn, email, website-forms, partner-referral)",
        "Log outreach outcomes to hall_events per channel room",
        "Update hall_discoveries when new channel performance insights emerge",
        "Feed results to wing_metrics for KPI tracking",
        "Flag channel skills for update when performance drops below threshold"
      ],
      "diary_format": "AAAK",
      "diary_example": "240414|LI|PRO|SS|sent=47;open=31;reply=12|★★★"
    },
    "product-agent": {
      "primary_wing": "wing_value-prop",
      "secondary_wings": ["wing_solutions", "wing_costs", "wing_resources"],
      "responsibilities": [
        "Maintain three-layer offer architecture documents",
        "Calculate offer layer-3 configurations on demand",
        "Sync product spec changes to wing_resources",
        "Log product iterations to wing_solutions / hall_events",
        "Invalidate and update KG triples when product specs change"
      ],
      "diary_format": "AAAK"
    },
    "partner-agent": {
      "primary_wing": "wing_partners",
      "secondary_wings": ["wing_channels", "wing_costs"],
      "responsibilities": [
        "Maintain partner profiles with performance history",
        "Match partners to customer cases based on region and product type",
        "Update partner performance KG triples after each case",
        "Flag underperforming partners for review"
      ],
      "diary_format": "AAAK",
      "diary_example": "240414|INS-N|case-001|turnaround=12d|quote=€7800|★★★★"
    },
    "metrics-agent": {
      "primary_wing": "wing_metrics",
      "secondary_wings": ["all"],
      "responsibilities": [
        "Read all wings to generate KPI summaries",
        "Produce monthly performance digest",
        "Identify hall imbalances (events without discoveries = learning debt)",
        "Alert on cases where savings < 20% threshold",
        "Generate AAAK-compressed L1 critical facts for wake-up command"
      ],
      "diary_format": "structured-json"
    },
    "governance-agent": {
      "primary_wing": "wing_governance",
      "secondary_wings": ["all"],
      "responsibilities": [
        "Monitor KB freshness per lifecycle policy",
        "Flag stale rooms (no updates > cadence threshold)",
        "Alert stewards to pending review obligations",
        "Enforce AAAK entity registry consistency across all wings",
        "Run quarterly knowledge graph audit (mempalace_kg_stats)",
        "Detect rooms with no tunnel connections (isolated knowledge)"
      ],
      "diary_format": "structured-json"
    }
  }
}
```

---

## SECTION 6 — CHANNEL SKILL FILE TEMPLATE

Each room in `wing_channels` is an executable skill file. Agent directive: implement each skill as a self-contained file in this format.

```markdown
# Skill: [channel-name]
## Wing: wing_channels | Room: [room-name] | Hall: hall_facts

## Purpose
[One-sentence description of what this skill does]

## Input (from wing_customers)
- Customer segment: {PRO|ENT}
- Case ID: {case-id}
- Target: {individual|list|partner}
- Product context: {SS|VC}

## Process
1. [Step 1: data retrieval from palace]
2. [Step 2: message construction using value prop from wing_value-prop]
3. [Step 3: execution action]
4. [Step 4: log outcome to hall_events]
5. [Step 5: update KG triple]

## Output
- Action taken: {sent|submitted|contacted}
- Log entry format: {AAAK diary entry}
- KG update: kg.add_triple("case-{id}", "channel_attempt", "{channel}", valid_from="{date}")

## Performance thresholds
- Minimum reply rate: {X%} (flag for review if below)
- Review trigger: {condition}

## Last validated: {date} | Steward: {role}
```

**LinkedIn Skill (populated example):**

```markdown
# Skill: linkedin-outreach
## Wing: wing_channels | Room: linkedin-skill | Hall: hall_facts

## Purpose
Find solar installer profiles and prosumer contacts on LinkedIn; send connection
requests and value proposition messages tailored to PRO segment.

## Input
- Customer segment: PRO (mindful prosumers)
- Product context: SS (Solar Seed)
- Target list: installer profiles + lead-gen aggregated lists

## Process
1. Query wing_customers / prosumer-profile for current segment definition
2. Query wing_value-prop / general-value-concept for message framing
3. Search LinkedIn for solar installer profiles in PT region
4. Extract company profiles + contact submission forms
5. Send personalised outreach using Wing VP Layer 1 narrative
6. Log to hall_events: "240414|LI|PRO|SS|sent=X;conn=Y;reply=Z"
7. Update KG: kg.add_triple("case-{id}", "channel_attempt", "linkedin", valid_from=date)

## Performance thresholds
- Minimum connection rate: 15%
- Minimum reply rate: 10%
- Review trigger: two consecutive campaigns below threshold

## Last validated: 2026-04-14 | Steward: growth-operations-role
```

---

## SECTION 7 — BUSINESS WIKIPEDIA PAGE TEMPLATE

Each room in any wing renders as a human-readable wiki page in this format. Agent directive: generate this template for every room during scaffold phase.

```markdown
---
room: [room-name]
wing: [wing-name]
hall: [primary hall]
steward: [role]
last_updated: [date]
review_due: [date per cadence]
tunnels: [list of linked rooms in other wings]
---

# [Room Name]
> **Wing**: [Wing Name] | **Hall**: [hall_type] | **Steward**: [role]
> **Tunnels**: [↔ wing/room links]

## What this is
[2–3 sentence plain-language definition. No jargon. Readable by new team member day 1.]

## Current state (hall_facts)
- [Locked decision 1]
- [Locked decision 2]
- [Locked decision N]

## Recent activity (hall_events)
| Date | Event | Outcome |
|---|---|---|
| [date] | [event description] | [outcome] |

## What we've learned (hall_discoveries)
- [Discovery 1 — source: case-{id} or event-{id}]
- [Discovery 2]

## Preferences and patterns (hall_preferences)
- [Preference/pattern observed]

## Recommendations (hall_advice)
- [Actionable recommendation with source]

## Linked resources (drawers)
- [Document 1 — verbatim source]
- [Document 2]

## Machine query
\`\`\`
mempalace search "[key terms]" --wing [wing] --hall [hall]
mempalace_kg_query entity="[entity-id]"
\`\`\`
```

---

## SECTION 8 — CASE BUILDER PROCESS SPECIFICATION

Agent directive: implement this process as an automated pipeline triggered by new customer data input.

```
INPUT (from operator or lead-gen bot):
  - avg_daily_consumption_kwh: float
  - avg_night_consumption_kwh: float
  - location_postcode: string       ← PII boundary: postcode only
  - buildable_area_sqm: float
  - avg_monthly_bill_eur: float
  - customer_segment: PRO | ENT
  - channel_source: LI | EM | WF | PR | LG

PROCESS:
  Step 1: VALIDATE input completeness
  Step 2: ENCRYPT PII → vault (NOT in palace)
           PII fields: name, address, contact details, exact location
           Vault key: case-{uuid} (same as palace case ID)
  Step 3: CREATE anonymised palace entry
           Destination: wing_customers / hall_events / case-{uuid}
           Content: all fields except PII fields
  Step 4: ADD KG triples (see Section 4.1 customer lifecycle)
  Step 5: SCORE against customer segment profiles
           Query: wing_customers / {segment}-profile
           Output: segment match confidence %
  Step 6: MATCH partner
           Query: wing_partners where region matches postcode AND product=SS
           Select: partner with highest ★ rating and lowest turnaround
  Step 7: GENERATE Terms of Reference for partner
           Template: wing_activities / partner-coordination-sop
           Populate: consumption data + buildable area + segment type
  Step 8: CALCULATE offer layer-3
           Base: partner quote (from Step 6 partner history)
           Rule: leasing_monthly = max(quoted_price / amortisation_months, bill * 0.80)
           Validation: leasing_monthly ≤ avg_monthly_bill * 0.80 (≥20% discount)
  Step 9: FILE offer to wing_value-prop / offer-layer-3-configurator / case-{uuid}
  Step 10: ADD KG triple: kg.add_triple("case-{uuid}", "status", "quoted", valid_from=today)
  Step 11: LOG to case-builder-agent diary

OUTPUT:
  - Palace entry: wing_customers / hall_events / case-{uuid}
  - KG triples: full lifecycle start set
  - Partner RFQ: terms of reference document
  - Customer offer: configured layer-3 product with leasing amount
  - Agent diary entry: AAAK format
```

---

## SECTION 9 — AFTER ACTION REVIEW (AAR) PROTOCOL

Agent directive: trigger AAR process at each of these stage gates. File output to relevant wing.

```
STAGE GATE 1: Lead Qualified
  → Update: wing_channels / hall_events / {channel} (log conversion)
  → Update: wing_customers / hall_events / case-{id} (status: qualified)
  → Question: "What did we do that made this lead qualify?"
  → File discovery: wing_channels / hall_discoveries / {channel} if new insight

STAGE GATE 2: Partner Quote Received
  → Update: wing_partners / hall_advice / {partner-id} (quote, turnaround)
  → Update: wing_partners / hall_events / case-{id} (quote details)
  → KG: add_triple partner performance data
  → Question: "Was this quote within expected range? Why or why not?"

STAGE GATE 3: Deal Closed / Declined
  If CLOSED:
    → Update: wing_revenue / hall_events / case-{id} (leasing terms finalised)
    → KG: status = installed
  If DECLINED:
    → Update: wing_problems / hall_events / decline-{date} (root cause)
    → Question: "Which stage did we lose them? What would change the outcome?"

STAGE GATE 4: Installation Completed
  → Update: wing_activities / hall_events / install-{date} (workflow performance)
  → Update: wing_metrics / hall_events / case-{id} (install duration, issues)
  → Update: wing_partners / hall_facts / {partner-id} (update performance KG triples)

STAGE GATE 5: Month 1 Operational Review
  → Update: wing_metrics / hall_events / case-{id} (actual vs projected savings)
  → If savings < 20%: flag to wing_problems + wing_solutions
  → If savings > 25%: file to wing_metrics / hall_discoveries (outperformance case)
  → KG: add_triple("case-{id}", "savings_vs_baseline_pct", actual_value)
```

---

## SECTION 10 — IMPLEMENTATION PHASES

### Phase 1 — Palace Initialisation (Weeks 1–2)

```bash
pip install mempalace

# Initialise palace
mempalace init ~/wera-palace

# During guided init, provide:
# - Identity (L0): paste content from Section 2.2 L0 template
# - AAAK registry: paste entity list from Section 2.2 L1 template
# - Wing config: use JSON from Section 3.1

# Verify installation
mempalace status
mempalace list-wings
```

Deliverables:
- [ ] 12 wings created
- [ ] L0 identity loaded
- [ ] AAAK entity registry filed to wing_governance / aaak-entity-registry
- [ ] 6 specialist agent JSON configs created
- [ ] Governance policies filed to wing_governance

### Phase 2 — Content Mining (Weeks 3–6)

```bash
# Mine existing documents
mempalace mine ~/existing-kb/ --wing value-prop
mempalace mine ~/product-docs/ --wing value-prop
mempalace mine ~/partner-emails/ --wing partners
mempalace mine ~/customer-communications/ --mode convos --wing customers

# Split large chat exports before mining
mempalace split ~/ai-sessions/ --min-sessions 2
mempalace mine ~/ai-sessions/ --mode convos --extract general
```

Priority population order (outside-in, customer-facing first):
1. wing_customers — segment profiles (PRO and ENT)
2. wing_value-prop — three-layer offer architecture
3. wing_channels — skill files (LinkedIn, email, website-forms, partner-referral)
4. wing_problems — storm event 2025 as founding entry
5. wing_partners — existing installer network profiles
6. wing_revenue — leasing model and pricing logic
7. wing_resources — equipment specs
8. wing_activities — installation workflow SOPs
9. wing_costs — CapEx/OpEx models
10. wing_solutions — Solar Seed MVP outcomes
11. wing_metrics — KPI definitions
12. wing_governance — policies, steward assignments

### Phase 3 — Tunnel Creation (Week 5–6, parallel with Phase 2)

For each tunnel pattern in Section 2.3, verify bidirectional connection after each wing is populated. Run:

```bash
mempalace find-tunnels --wing wing_customers
mempalace find-tunnels --wing wing_channels
# Repeat for all 12 wings
mempalace graph-stats  # identify isolated nodes (rooms with 0 tunnels)
```

### Phase 4 — MCP Activation (Weeks 7–10)

```bash
# Connect to Claude (primary AI agent interface)
claude mcp add mempalace -- python -m mempalace.mcp_server

# Activate auto-save hooks
cp hooks/mempal_save_hook.sh ~/.config/claude/hooks/
cp hooks/mempal_precompact_hook.sh ~/.config/claude/hooks/

# Test palace query
mempalace wake-up --wing wera-global
mempalace search "prosumer solar seed portugal" --wing customers
```

### Phase 5 — Governance and Iteration (Month 3+)

- Run `mempalace kg-stats` quarterly → identify sparse wings and isolated rooms
- Governance agent monitors freshness against cadences defined in wing_config
- Rotating steward assignments per sprint cycle
- Annual full knowledge graph audit: `mempalace graph-stats --deep`

---

## SECTION 11 — KNOWLEDGE GOVERNANCE POLICIES

```yaml
governance_policies:
  
  content_lifecycle:
    hall_facts:
      review_trigger: "on-decision-change"
      max_age_without_review: "indefinite (facts are locked until explicitly changed)"
    hall_events:
      review_trigger: "automatic (event-driven, no manual review needed)"
      retention: "permanent (verbatim drawer), summarised closet after 90 days"
    hall_discoveries:
      review_trigger: "quarterly"
      action_if_stale: "validate or demote to hall_facts"
    hall_preferences:
      review_trigger: "after 3 new contradicting data points"
    hall_advice:
      review_trigger: "after each use in production"

  taxonomy_governance:
    controlled_vocabulary: "wing_governance / taxonomy-controlled-vocabulary"
    add_new_term_process: "governance-agent approval + wing steward consent"
    aaak_entity_add: "governance-agent → update entity registry → notify all agents"

  access_control:
    palace_read: "all team members, all AI agents"
    palace_write: "steward of respective wing, or any agent for event logging"
    vault_read: "case-builder-agent only (PII access restricted)"
    vault_write: "case-builder-agent only"
    governance_wing_write: "kb-steward-role only"

  quality_standards:
    minimum_tunnel_density: "every room must link to ≥1 room in another wing"
    maximum_stale_rooms_pct: "10% (governance agent flags if exceeded)"
    aar_completion_rate: "100% of stage gates must produce palace entries"
    kg_triple_coverage: "every active case must have full lifecycle triples"

  stewardship_rotation:
    cycle: "sprint (2 weeks)"
    handoff: "steward files hall_events entry summarising wing state"
    escalation: "unresolved wing issues → governance-agent → kb-steward-role"
```

---

## SECTION 12 — FOUNDING ENTRIES (SEED DATA)

Agent directive: create these specific entries as the first palace population actions.

```
ENTRY 1: The WeRa Mission (L0 Identity)
  Wing: N/A (system identity)
  Content: L0 template from Section 2.2
  Action: mempalace set-identity

ENTRY 2: Portugal Storm Crisis 2025 (founding problem statement)
  Wing: wing_problems
  Room: storm-events-PT
  Hall: hall_events
  Content: "2025 Portugal storms left 150,000+ households and organisations
            without electricity overnight. Event triggered urgent demand for
            energy sovereignty solutions. Solar Seed positioned as emergency
            energy resilience product. Three new customer cases opened within
            72 hours of event."
  KG: kg.add_triple("storm-2025-PT", "type", "grid-crisis", valid_from="2025")
      kg.add_triple("storm-2025-PT", "affected_count", "150000+", valid_from="2025")
      kg.add_triple("storm-2025-PT", "triggered_product", "solar-seed", valid_from="2025")
  Tunnels: → wing_solutions / emergency-response-protocols
           → wing_channels / hall_discoveries / crisis-outreach
           → wing_customers / hall_discoveries / crisis-segment

ENTRY 3: Mindful Prosumer Segment Definition
  Wing: wing_customers
  Room: prosumer-profile
  Hall: hall_facts
  Content: "Mindful prosumers (PRO): individuals aware of energy crisis and
            actively seeking solutions. Primary constraint: not ready for full
            CapEx investment. Reachable via digital channels (LinkedIn, Instagram,
            Facebook), installer networks, and lead-gen aggregators.
            Data points needed: avg daily consumption, avg night consumption,
            location postcode, buildable area sqm, avg monthly bill EUR."

ENTRY 4: Solar Seed Product Definition (Layer 1+2)
  Wing: wing_value-prop
  Room: solar-seed-product-line
  Hall: hall_facts
  Content: "Solar Seed: base station for energy sovereignty. Non-habitable land
            + habitable premises. Components: solar panels + inverter + battery +
            edge server. Connectivity: serves as station for automatic irrigation
            and security. Layer 1 value: Sustainable sovereign self-hosting.
            Layer 2: Solar Seed product line. Layer 3: configured via case-builder
            script (consumption data + quote + extras + leasing calc).
            Pricing rule: leasing ≤ 80% of avg monthly bill."

ENTRY 5: Leasing Model Core Rule
  Wing: wing_revenue
  Room: bill-discount-logic
  Hall: hall_facts
  Content: "Base leasing rule: monthly leasing amount must be at minimum 20%
            below the customer's average monthly electricity bill.
            Formula: leasing_monthly ≤ avg_monthly_bill * 0.80
            This is a non-negotiable commercial constraint.
            Rationale: value proposition is sustainability at cheaper price."
  KG: kg.add_triple("leasing-model", "discount_minimum_pct", "20", valid_from="2026-04-14")
```

---

## SECTION 13 — VALIDATION CHECKLIST FOR IMPLEMENTING AGENT

Agent directive: run this checklist after completing each implementation phase.
File results to wing_governance / hall_events / implementation-audit.

```
PHASE 1 VALIDATION:
  [ ] mempalace status returns OK
  [ ] mempalace list-wings returns 12 wings
  [ ] mempalace wake-up returns WeRa identity + ≥5 critical facts
  [ ] AAAK entity registry accessible at wing_governance / aaak-entity-registry
  [ ] 6 agent JSON configs present in ~/.mempalace/agents/

PHASE 2 VALIDATION:
  [ ] wing_customers contains ≥2 segment rooms (prosumer-profile, enterprise-profile)
  [ ] wing_value-prop contains ≥3 rooms (general-concept, solar-seed, vera-cloud)
  [ ] wing_channels contains ≥4 skill files (linkedin, email, website-forms, partner-ref)
  [ ] wing_problems contains storm-events-PT founding entry
  [ ] wing_governance contains kb-policies and aaak-entity-registry

PHASE 3 VALIDATION:
  [ ] mempalace graph-stats shows 0 isolated rooms (0 tunnel connections)
  [ ] Case tunnel pattern verified: wing_customers ↔ wing_partners ↔ wing_revenue
  [ ] Product tunnel verified: wing_value-prop ↔ wing_costs ↔ wing_resources
  [ ] Storm event tunnel verified: wing_problems ↔ wing_solutions ↔ wing_channels

PHASE 4 VALIDATION:
  [ ] MCP server running: mempalace mcp-status
  [ ] Claude can query palace: test "what is the leasing model rule?"
  [ ] Auto-save hooks active: verify after next AI session
  [ ] Case builder end-to-end test: create test case, verify vault separation

ONGOING GOVERNANCE VALIDATION (quarterly):
  [ ] mempalace kg-stats: all active cases have full lifecycle triples
  [ ] Stale rooms < 10% threshold
  [ ] AAR completion rate 100% of stage gates
  [ ] Governance agent diary shows no unresolved flags
```

---

## APPENDIX A — THEORETICAL FOUNDATIONS (FOR AGENT CONTEXT)

This KB architecture is grounded in validated knowledge management frameworks:

**Nonaka-Takeuchi SECI Model**: The hall structure (facts/events/discoveries) maps to the SECI spiral — events=Socialisation, discoveries=Externalisation, facts=Combination, agent skills=Internalisation.

**PARA Method (Tiago Forte)**: Active cases = Projects; BMC wings = Areas; skill files = Resources; completed cases = Archives.

**US Army CALL Doctrine**: AAR protocol (Section 9) mirrors CALL's 5-element system: Collection (AAR triggers) → Repository (palace) → Transfer (tunnels) → Implementation (agent skills) → Analysis (metrics wing).

**NATO KMP Principle**: Every wing has a steward (knowledge officer). Senior leadership must actively contribute. KM is everyone's responsibility.

**Single Source of Truth (SSOT)**: Palace is the SSOT. CRM is downstream consumer of anonymised customer data. No duplicate authoritative records.

**MemPalace Benchmarks**: 96.6% R@5 LongMemEval (raw), 100% (reranked). Palace structure alone +34% vs flat vector search. Fully local, MIT licensed, zero cloud.

---

## APPENDIX B — EXPANSION ROADMAP

After core BMC/Lean 12-wing palace is operational:

```
NEXT EXPANSION WINGS:
  wing_finance      → P&L, budgets, investor relations, funding rounds
  wing_legal        → Contracts, IP, regulatory compliance (PT energy law)
  wing_hr           → Team, roles, onboarding, steward rotation log
  wing_pr           → Press, social media, public narrative, brand voice
  wing_innovation   → R&D pipeline, new product ideation, market research

VERA CLOUD WING EXPANSION:
  wing_vera-cloud   → Digital self-hosting product line (separate wing from solar)
  wing_marketplace  → Third-party service partners (gardening, pool, security)

GEOGRAPHIC EXPANSION:
  wing_markets-ES   → Spain market entry
  wing_markets-FR   → France market entry
  (one wing per country, each with own tunnel set back to core wings)
```

---
*END OF SPECIFICATION*
*File: KB-memPalace-upgrade.md*
*Version: 1.0.0 | Date: 2026-04-14 | Organisation: WeRa Global*
*AI agent: read, verify, validate, implement in order — Sections 1→2→3→4→5→6→7→8→9→10→11→12→13*
---
