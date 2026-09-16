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
    source: "HumanCenter/Resources/Documents/Research/Human Center — Product 1  Shrinking AI  Desk Research, Heuristic Evaluation &amp; Competitive Analysis.md; HumanCenter/Resources/Documents/Research/HumanCenter.Pricing.md"
    confidence: high
    review_status: draft
---
# Revenue Streams

## Purpose
Define Human Center's revenue model across its two priced product lines (Shrinking AI, Automation Center), keeping their pricing threads clearly separate.

## Scope
- In scope: Shrinking AI's (Product 1) still-undocumented session pricing, and Automation Center's (Product 3) documented market-benchmark pricing.
- Out of scope: final, client-contracted pricing for either product (none exists yet — no client contracts signed); Product 2 pricing (unresearched).

## Current State

### Product 1 — Shrinking AI: pricing gap
**Shrinking AI's core paid-session price remains undocumented anywhere in current research.** The session flow (see `../../../kb-key-activities/docs/execution/04-key-activities.md`) is: (1) free 15-minute empathy call, (2) a paid, structured RCGFC session producing an AI-ready problem statement and instruction set, (3) an optional retainer/implementation-support follow-on (which may be referred to Automation Center). Steps 1 and 2 are validated as the core product; no source document states what the paid session in step 2 actually costs. This remains the highest-priority pricing gap for Product 1.

### Product 3 — Automation Center: validated benchmark pricing
Automation Center now has its own documented, market-benchmark-derived pricing (sourced from named European/US agency comparables: ABC OPTIM, FETCHER Solutions, NeuraWeb, Flow Architects, Bitech Prime, Go Rogue Ops, Connex Digital). This is real market pricing, not yet tested against a signed Human Center client, but it is Automation Center's own official pricing reference (not an ambiguous background thread).

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

**Investment-fund-adjacent pricing caveat:** do not price Automation Center like a PE-fund AI consultancy (which can run $12,500 for a readiness sprint alone, or $35,000 readiness + $75,000-$150,000 for a production build) merely because a client's own clients are investment funds. That pricing tier is for funds deploying software across deal teams and portfolio companies — not for a solo consultant or small firm automating its own back office. The heightened *security* standard from that world (human approval, audit logs, DPA, EU data residency, no training on public models) is relevant; the heightened *price* is not.

## Decisions / Rules
- Automation Center may quote using the documented benchmark pricing above; Shrinking AI must not (its pricing remains undocumented — a separate, unresolved gap).
- Do not quote Automation Center pricing without a cost-model check (`../../../kb-cost-structure/docs/model/08-cost-structure.md`).
- Do not price or position Automation Center like a PE-fund-facing AI vendor; the buyer remains a solo consultant/small firm even when their own clients are funds (see `../../../kb-customers/docs/gtm/04-automation-center-segments.md`).
- Re-benchmark Automation Center's pricing periodically as the automation-agency market shifts; treat the figures above as current as of this research pass, not permanently fixed.

## Evidence
- `../../../../Resources/Documents/Research/Human Center — Product 1  Shrinking AI  Desk Research, Heuristic Evaluation &amp; Competitive Analysis.md` — verified for the Shrinking AI session-flow structure; confirms no session price is documented.
- `../../../../Resources/Documents/Research/HumanCenter.Pricing.md` — verified as Automation Center's own official market-benchmark pricing research.

## Cross-Domain Links
- Related domains: `kb-value-proposition`, `kb-cost-structure`, `kb-customers`, `kb-key-activities`
- Related documents: `../../../kb-value-proposition/docs/products/02-services.md`, `../../../kb-value-proposition/docs/products/03-automation-center.md`, `../../../kb-cost-structure/docs/model/08-cost-structure.md`, `../../../kb-key-activities/docs/execution/04-key-activities.md`, `../../../kb-key-activities/docs/execution/05-automation-center-key-activities.md`

## Open Actions
- Set and document Shrinking AI's actual paid-session price (currently undocumented anywhere) — highest-priority pricing gap for Product 1, owner: Founder/Consultant, due: see `../../../../tasks/backlog.md` HC-003.
- Validate Automation Center's benchmark pricing against the first signed client engagement, owner: Founder/Consultant.
- Build a real cost model for Automation Center before finalizing a standard quote (see `../../../kb-cost-structure/docs/model/08-cost-structure.md`), owner: Founder/Consultant.
