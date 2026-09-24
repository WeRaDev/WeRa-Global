---
metadata:
  primary_domain: revenue-streams
  secondary_domains: [value-proposition, cost-structure]
  owner_role: Founder/Consultant
  temporal_scope: current
  evidence_status: verified
  last_reviewed_at: 2026-09-16
  next_review_due: 2026-12-15
  provenance:
    actor: agent-warp
    source: "Inteligente/Resources/Documents/Research/Human Center — Product 1  Shrinking AI  Desk Research, Heuristic Evaluation &amp; Competitive Analysis.md; Inteligente/Resources/Documents/Research/HumanCenter.Pricing.md"
    confidence: high
    review_status: draft
---
# Revenue Streams

## Purpose
Define Inteligente's revenue model across its two priced services (Shrinking AI, Automation Center/Financial Automation), keeping their pricing threads clearly separate.

## Scope
- In scope: Shrinking AI's now-established introductory session price, and Automation Center's documented, partially-corroborated market-benchmark pricing (which also covers Financial Automation, since it has no distinct pricing tier yet).
- Out of scope: final, client-contracted pricing for Automation Center (none exists yet — no client contracts signed); Empowering Human pricing (unresearched, hypothesis-stage).

## Current State

### Human Center / Shrinking AI: real pricing established
**Shrinking AI's paid-session price is now documented from real transactions: €50 for a 60-minute session.** This was set from the first 2 completed, paid engagements (Sept 2026): a self-published writer (AI for e-book formatting) and a self-employed tour guide (AI for content creation). The session flow (see `../../../kb-key-activities/docs/execution/04-key-activities.md`) is: (1) free 15-minute empathy call, (2) the €50/60-min paid, structured RCGFC session producing an AI-ready problem statement and instruction set, (3) an optional retainer/implementation-support follow-on (which may be referred to Automation Center). This is the first primary (client-transaction) evidence in the entire KB, replacing what was previously an undocumented pricing gap. It should still be treated as an **introductory** price, not a final one — see Decisions/Rules and Open Actions on price-elasticity testing.

### Automation Center (including Financial Automation): benchmark pricing, partially corroborated
Automation Center's pricing is sourced from named European/US agency comparables (ABC OPTIM, FETCHER Solutions, NeuraWeb, Flow Architects, Bitech Prime, Go Rogue Ops, Connex Digital) as compiled by `HumanCenter.Pricing.md` — itself a first-person, self-described AI-chat pricing estimate, not primary or client-sourced data. An independent web-research pass (Sept 2026) partially corroborates it:
- **FETCHER Solutions**: its current live pricing page matches the cited figures exactly (€600/workflow, €2,800 document/OCR agent) — strong corroboration for this specific comparable.
- **Broader 2026 market range**: other agencies (BOVO Digital, Polish agencies such as Wiszniewsky and biznesailab.pl, French-market surveys) show comparable overall ranges (roughly €600-€12,000+ for typical projects, up to €20,000-€44,000+ for complex/enterprise builds), so the general envelope in the table below is directionally plausible.
- **NeuraWeb's own current pricing has drifted** from the tiers originally cited (€999+€29/mo, €2,999+€79/mo, €5,999+€149/mo) to different figures on its own current blog (e.g. simple workflows now quoted at €800-1,500, multi-agent solutions at €5,000-12,000) — the underlying comparable has changed since the original research, so that specific tier breakdown should be treated as stale.
- One source (NeuraWeb's own market commentary) reports category-wide price declines of 60-75% over the prior 18 months, i.e. this market moves fast and a point-in-time benchmark ages quickly.

**Net assessment**: treat Automation Center's benchmark pricing as directionally plausible and partially corroborated by live agency pricing pages, but not verified/official pricing, and due for periodic re-benchmarking (already a Decision/Rule below). Financial Automation, as Automation Center's first named service, uses this same benchmark pricing until service-specific pricing is validated.

### Discovery/ROI-screening is free (Sept 2026 decision)
Unlike Shrinking AI's paid €50/60-min diagnostic, Automation Center's discovery-and-ROI-screening chatbot session is **free** — a qualification and lead-generation step, not a monetized product. Revenue only begins once a screening decision reaches Prototype or Pilot and the client signs an implementation engagement, using the benchmark pricing above. This is a deliberate difference from Shrinking AI: the discovery conversation itself does not need to independently prove willingness-to-pay, because the founder is running it with a named, warm-introduced prospect rather than a cold/anonymous visitor.

### Commercial-model structure (from the MVP research)
The previously un-cited `financial_advisory_automation_mvp.xlsx` sketches a 4-part commercial model, reconciled here with the free-discovery decision above:
- **Discovery/measurement**: the xlsx proposes a "fixed fee for assessment, evidence plan and baseline sprint" — **not adopted for now**; discovery stays free per the decision above. Revisit if the free-discovery motion proves too resource-intensive relative to conversion.
- **Implementation**: milestone fee by deliverable family and bounded scope, consistent with the existing per-project pricing table above.
- **Recurring service**: platform/hosting/monitoring/support/maintenance/review/governance, consistent with the existing retainer pricing above.
- **Outcome-linked option**: only with an attributable baseline, a named finance owner, and contractual measurement — never priced from ambiguous "time saved." Not yet used; a future option once a pilot has produced matched pre/post evidence.

**Service-line pricing (Europe / US):**

| Scope | European agency quote | US agency quote |
|---|---:|---:|
| Accounting/bookkeeping workflow automation | €2,500-€6,000 setup | $4,000-$8,000 |
| More sophisticated tax + accounting automation | €5,000-€12,000+ | $8,000-$20,000+ |
| Email triage, drafting, filing, follow-ups | €1,500-€4,000 setup | $4,000-$10,000 |
| Advanced email "agent" (attachments/context/integrations) | €3,000-€7,000 | $5,000-$12,000 |
| Combined accounting + email | roughly €5,000-€9,000 | roughly $8,000-$15,000 |
| Ongoing support/monitoring | €100-€500/mo normal; €500-€1,000/mo high-touch | $300-$800/mo |

**Recommended first-engagement budget (~€6,000 total, European solo-consultant buyer):**

| Component | Target |
|---|---:|
| Process mapping / design | €500-€1,000 |
| Accounting + document automation | €2,500-€3,500 |
| Email AI workflows | €1,500-€2,500 |
| Security, testing, documentation, training | €500-€1,000 |
| Expected combined quote | €5,000-€8,000 |
| Ongoing monitoring/support | €150-€400/month |

**Confidence bands:** €4,000-€5,000 is a good low quote; €6,000-€8,000 is very normal; €10,000-€12,000 is defensible only with significant custom integration/security/tax complexity; €20,000+ needs strong justification for two workflows on a single-consultant client; €500-€1,000 total implies a fragile setup with limited testing/documentation/exception handling.

**Named European benchmarks:** ABC OPTIM (France, €3,000 accounting-automation case study, €8,000 tax-analysis system); FETCHER Solutions (Poland, €600/workflow, €2,800 document/OCR agent, €7,000+ advanced system, €160-€350/mo maintenance); NeuraWeb (France, €999+€29/mo, €2,999+€79/mo, €5,999+€149/mo tiers); Flow Architects (Poland, from €1,900 lead-management+email); Bitech Prime (Germany, ~€3,700 setup + €695/mo "Email Autopilot," EU servers/GDPR/no-training-on-client-data). US benchmark: Go Rogue Ops ($4k-$8k accounting, $4k-$10k email, $300-$800/mo maintenance); Connex Digital ($200-$300/hr, $1,000 minimum).

**Investment-fund-adjacent pricing caveat:** do not price Financial Automation like a PE-fund AI consultancy (which can run $12,500 for a readiness sprint alone, or $35,000 readiness + $75,000-$150,000 for a production build) merely because a client's own clients are investment funds. That pricing tier is for funds deploying software across deal teams and portfolio companies — not for a solo consultant or small firm automating its own back office. The heightened *security* standard from that world (human approval, audit logs, DPA, EU data residency, no training on public models) is relevant; the heightened *price* is not.

## Decisions / Rules
- Automation Center (including Financial Automation) may quote using the documented, partially-corroborated benchmark pricing above; Shrinking AI must use its own real €50/60-min price, not the Automation Center benchmark.
- Automation Center's discovery/ROI-screening chatbot session is free; do not charge for it or imply a screening decision is a paid deliverable.
- Do not quote Automation Center pricing without a cost-model check (`../../../kb-cost-structure/docs/model/08-cost-structure.md`).
- Do not price or position Financial Automation like a PE-fund-facing AI vendor; the buyer remains a solo consultant/small firm even when their own clients are funds (see `../../../kb-customers/docs/gtm/05-financial-automation-segments.md`).
- Re-benchmark Automation Center's pricing periodically as the automation-agency market shifts — the Sept 2026 corroboration pass already found one comparable (NeuraWeb) to have drifted; treat the figures above as current as of this research pass, not permanently fixed.
- Do not raise or lower Shrinking AI's €50/60-min price without at least a handful more sessions at the current price to gauge demand first (see Open Actions).

## Evidence
- `../../../../Resources/Documents/Research/Human Center — Product 1  Shrinking AI  Desk Research, Heuristic Evaluation &amp; Competitive Analysis.md` — verified for the Shrinking AI session-flow structure.
- **First 2 real paid Shrinking AI engagements (Sept 2026)** — verified, primary evidence establishing the €50/60-min price (self-published writer; self-employed tour guide).
- `../../../../Resources/Documents/Research/HumanCenter.Pricing.md` — unverified (self-described AI-chat estimate), partially corroborated by independent Sept 2026 web research (FETCHER Solutions exact match; broader market range consistent; NeuraWeb tiers stale) — see Current State above for the full corroboration note.
- `../../../../Resources/Documents/Research/financial_advisory_automation_mvp.xlsx` — verified, source of the 4-part commercial-model structure (discovery, implementation, recurring, outcome-linked).
- **Founder decision: free discovery (Sept 2026)** — verified as a decision, not yet evidenced against a real conversion outcome.

## Cross-Domain Links
- Related domains: `kb-value-proposition`, `kb-cost-structure`, `kb-customers`, `kb-key-activities`
- Related documents: `../../../kb-value-proposition/docs/products/02-services.md`, `../../../kb-value-proposition/docs/products/03-automation-center.md`, `../../../kb-value-proposition/docs/products/04-financial-automation.md`, `../../../kb-cost-structure/docs/model/08-cost-structure.md`, `../../../kb-key-activities/docs/execution/04-key-activities.md`, `../../../kb-key-activities/docs/execution/05-automation-center-key-activities.md`

## Open Actions
- Set and document Shrinking AI's actual paid-session price (currently undocumented anywhere) — Human Center's highest-priority pricing gap, owner: Founder/Consultant, due: see `../../../../tasks/backlog.md` HC-003.
- Validate Automation Center's benchmark pricing against the first signed client engagement, owner: Founder/Consultant.
- Build a real cost model for Automation Center before finalizing a standard quote (see `../../../kb-cost-structure/docs/model/08-cost-structure.md`), owner: Founder/Consultant.
