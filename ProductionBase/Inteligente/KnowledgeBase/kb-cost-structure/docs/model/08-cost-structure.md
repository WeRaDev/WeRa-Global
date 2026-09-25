---
metadata:
  primary_domain: cost-structure
  secondary_domains: [key-resources, revenue-streams]
  owner_role: Founder/Consultant
  temporal_scope: future
  evidence_status: hypothesis
  last_reviewed_at: 2026-09-25
  next_review_due: 2026-12-25
  provenance:
    actor: agent-warp
    source: analysis; Portugal payroll-cost web research (PwC Portugal 2026 Tax Guide, teamed.global, remotepass.com, PayMetric Labs) and Portugal salary-benchmark web research (Sept 2026)
    confidence: medium
    review_status: draft
---

# Cost Structure

## Purpose
Identify Inteligente's cost categories, as input to pricing decisions. These categories apply primarily to Automation Center (including Financial Automation); Human Center's Shrinking AI has near-zero marginal delivery cost since it is mostly founder time, not infrastructure.

## Scope
- In scope: cost categories for Automation Center's build-and-operate automation service; the actual current resource base (1 employee, 2 servers, 2 unpaid partner relationships); and a quantified, clearly-labeled **illustrative-only scenario** for a hypothetical full 4-person team (Consulting Officer, Operations Officer, Financial Officer, Fullstack Developer), kept purely as a future-scale reference point.
- Out of scope: Human Center's costs (founder time only, not a meaningful infrastructure cost center); any commitment that additional hires will happen — the resource-acquisition principle (below) requires an evidenced need before any new resource is acquired.

## Current State
- Candidate cost categories (Automation Center): LLM/API usage, workflow-orchestration hosting (n8n/Make/Zapier), OCR/document-extraction tooling, EU-hosted storage and backups, founder/delivery time, tooling/subscriptions, marketing and the shared `www.inteligente.site` website.
- Economy-of-scale note (from pricing research on comparable vendors): shared authentication, hosting, AI API access, logging, and monitoring infrastructure reduces the marginal cost of delivering additional workflow types to the same client, which is why combined packages (e.g. accounting + email) are priced below the sum of their parts.

### Actual current resource base (Sept 2026) — the real starting point
This supersedes the earlier "Phase 0" framing with confirmed, real figures rather than a directional description:
- **1 employee**: a **Consulting Officer**, paid **€604.05 net/month**. Gross salary and full employer-loaded cost (TSU, subsidies) are not yet documented here — see Open Actions.
- **2 dedicated servers with AI tooling**, already owned/operating, costing **€71.54/month combined** for internet connectivity. These are the **Frank** and **SolarSeed** machines (see `../../../kb-key-resources/docs/architecture/06-automation-center-key-resources.md`). The current generic Odoo chatbot is on Frank; stage 1 of the Discovery Pilot is Odoo Online, stage 2 is a local Odoo/local-model MVP on Frank after pilot validation, and the SolarSeed TRL5 machine is intended for the first paying customer's dedicated account/agent after readiness and isolation checks. The two servers are existing infrastructure, not new spend.
- **"Operations Officer" and "Financial Officer" are not employees and carry no payroll cost.** They are external **partner relationships**: the Operations partner works within a network of financial companies; the Financial partner works at a small financial-advisory firm. Both are candidate sources of Financial Automation deal flow (see `../../../kb-key-partners/docs/partnerships/06-key-partners.md`), not headcount to be hired. Their compensation model (referral fee, revenue share, in-kind, or none yet) is undefined — see Open Actions.
- **Total known fixed monthly cost: ≈ €675.59/month** (€604.05 net salary + €71.54 hosting), before employer social-security add-ons on the salary and before any partner compensation. This excludes any Odoo Online subscription and GPT-4o/provider usage for the pilot; confirm actual quotes and usage before rollout.
- **Resource-acquisition principle (explicit business rule, Sept 2026)**: only acquire an additional resource — headcount, server, tool, or subscription — when a specific, evidenced business requirement justifies it. Do not pre-provision for hypothetical scale. This governs every Decision/Rule and Open Action below.
- Once at least one Prototype/Pilot engagement is signed (HC-011), the next real cost question is the **marginal cost of delivering that one engagement** (any contractor time, LLM/API usage, client-specific tooling) — not yet modeled here because no engagement has been signed.

### Illustrative-only scenario: a hypothetical 4-person Automation Center team (Portugal payroll)
**This is not the current state, not a near-term plan, and not a hiring commitment — it exists solely as a later-stage "what would full scale cost" reference check, kept for comparison against the real resource base above.** Two of its four roles (Operations Officer, Financial Officer) are, in reality, already informally covered by the unpaid partner relationships above, not vacant positions; this scenario treats them as if they were full-time hires purely to stress-test a worst-case/full-scale cost ceiling, not because that is the plan.
- **Employer Social Security (TSU): 23.75% of gross salary**, uncapped, paid by the employer on top of gross (employee separately pays 11%); confirmed by PwC Portugal's 2026 Tax Guide and cross-checked against 3 independent sources.
- **14 payments/year**: 12 regular months plus a mandatory holiday subsidy and a mandatory Christmas subsidy, each equal to one month's base salary; TSU applies to all 14 payments.
- **Working assumption**: fully-loaded annual employer cost = (monthly gross x 14) x ~1.26, where 1.26 approximates TSU (23.75%) plus mandatory labour-accident insurance (~1.75%, required from day one) plus a small administrative buffer. This is a simplified planning multiplier, not a precise payroll calculation.
- **Illustrative monthly gross salaries** (Portugal, non-enterprise/small-consultancy market rates, not Google/Farfetch-tier; sourced from Sept 2026 salary-benchmark research — treat as planning assumptions, not offers):

| Role | Monthly gross | Annual gross (x14) | Fully-loaded annual cost (x~1.26) | Basis |
|---|---:|---:|---:|---|
| Fullstack Developer (mid-level, full-time) | €2,800 | €39,200 | ~€49,400 | Portugal national mid-level full-stack/software-engineer benchmarks cluster at €30k-€40k/yr base outside FAANG-tier employers; €2,800/mo (~€33.6k/yr base) sits in that band. |
| Consulting Officer (client-facing discovery/sales, full-time) | €2,200 | €30,800 | ~€38,800 | No direct market benchmark for this exact title; assumed comparable to a mid-level business-development/analyst role in Portugal's professional-services market — **unverified assumption**. |
| Operations Officer (delivery coordination/admin, full-time) | €1,700 | €23,800 | ~€30,000 | Assumed comparable to a general operations/admin support role in Portugal — **unverified assumption**, roughly in line with Portugal's lower-band professional salaries. |
| Financial Officer (bookkeeping/financial oversight, **0.5 FTE / fractional**) | €1,800 FTE-equivalent | €12,600 (at 0.5 FTE) | ~€15,900 | At this team size a full-time Financial Officer is likely oversized; a fractional/part-time arrangement (common for Portuguese micro-businesses) is the more realistic near-term option — **unverified assumption**. Full-time equivalent shown for comparison: ~€31,800/yr fully loaded. |

- **Total fully-loaded payroll (fractional Financial Officer): ~€134,100/year (~€11,175/month).**
- **Total fully-loaded payroll (full-time Financial Officer instead): ~€150,000/year (~€12,500/month).**
- **Non-payroll operating overhead (rough placeholder, not yet a real line-item build)**: LLM/API usage, n8n/Make/Zapier hosting, OCR tooling, EU storage, accounting/admin services, insurance, minor marketing — estimated **€1,200-1,800/month (~€14,400-21,600/year)**, midpoint ~€1,500/month. This is a placeholder pending an actual per-category build-out (see Open Actions).
- **Total fully-loaded monthly burn: ~€12,700/month (fractional Financial Officer) to ~€14,000/month (full-time Financial Officer)**, i.e. roughly **€152,000-€168,000/year**.

### Profitability check against Automation Center's documented pricing
Using Automation Center's benchmark pricing (see `../../../kb-revenue-streams/docs/model/07-revenue-streams.md`: typical signed-engagement quote €5,000-8,000, midpoint ~€6,500; retainer €150-400/month, midpoint ~€275/month):
- **Breakeven on new projects alone**: ~€13,000/month burn ÷ ~€6,500/project = **~2 newly signed Automation Center projects every single month, indefinitely**, just to cover cost — with zero margin left over for founder return, taxes, buffer, or reinvestment.
- **Breakeven on retainers alone**: ~€13,000/month ÷ ~€275/retainer client = **~47 concurrent retainer clients** — not realistic in year one.
- **Delivery-capacity check**: a single Fullstack Developer is the only build resource in this scenario. Independent 2026 market research on comparable automation-agency builds shows typical delivery timelines of roughly 1-3+ weeks per project (scoping, build, testing, documentation, training). Sustaining 2 completed projects/month indefinitely, while also handling support-retainer work, bug fixes, and onboarding for new clients, would run this single developer at or above full capacity with no slack — before accounting for illness, vacation, ramp-up time on unfamiliar client systems, or the Financial Automation service's extra compliance/security work.
- **Deal-flow reality check**: as of Sept 2026, Automation Center has **zero signed clients** (HC-011 is still open) and its discovery methodology is only now being tested manually with real prospects for the first time (HC-009, just marked ongoing). There is no evidence yet that 2 signed projects/month is an achievable, let alone sustainable, sales velocity.

**Verdict**: A 4-person, ~€150k-168k/year fully-loaded team is **not currently profitable or safely sustainable** at Automation Center's documented pricing and with a single-developer delivery capacity, given zero validated deal flow. The model implicitly assumes a sales/delivery velocity (2+ signed projects/month, sustained) with no supporting evidence. **This concern is significantly less pressing than it sounds once compared against the actual current resource base above**: the real fixed cost today is roughly €676/month plus undefined partner compensation, not €12,700-14,000/month — there is no burn from 3 of the 4 modeled roles because they either don't exist as payroll (Operations/Financial Officer) or already exist as a single, already-affordable hire (Consulting Officer). Recommendation: do not use this illustrative scenario to justify hiring; instead, add any new paid resource only when a specific, evidenced requirement appears (per the resource-acquisition principle above) — e.g. a Fullstack Developer only once signed deal volume exceeds what the Consulting Officer and partners can deliver personally.

## Decisions / Rules
- Use cost data as a delivery-viability guardrail and to understand direct delivery costs; do not set customer revenue by cost-plus. Market-average competitor benchmarks with a modest case-by-case undercut remain the pricing direction (see `../../../kb-revenue-streams/docs/model/07-revenue-streams.md`).
- Do not hire any additional employee, and do not formalize Operations/Financial Officer as paid roles, until a specific, evidenced business requirement justifies it (resource-acquisition principle above) — the illustrative 4-person scenario must not be read as a hiring plan.
- Partner compensation remains an unapproved proposal, not a current cost or payroll item. If agreed, calculate shares from collected customer revenue after explicitly agreed direct delivery costs; percentages, allocation, duration/cap, and approvals remain open.
- Re-run the illustrative scenario with real payroll quotes (e.g. from a Portuguese accountant or EOR) before treating any of its salary figures as more than a rough planning assumption.
- Track the Consulting Officer's actual gross salary and fully-loaded employer cost (TSU, subsidies) as the one real, current payroll data point — do not substitute the illustrative Consulting Officer figure (€2,200/mo gross assumption) for the real €604.05 net figure in any actual accounting.

## Evidence
- `../../../../Resources/Documents/Research/HumanCenter.Pricing.md` — unverified (self-described AI-chat estimate); notes the shared-infrastructure economy-of-scale effect for comparable vendors, used qualitatively only.
- **Portugal employer Social Security / TSU rate (23.75% employer, 11% employee, 14 monthly payments)** — verified via independent Sept 2026 web research, cross-confirmed across PwC Portugal's 2026 Tax Guide, teamed.global's Portugal employer cost breakdown, remotepass.com, and PayMetric Labs.
- **Portugal salary benchmarks (Fullstack Developer)** — verified as directionally consistent across multiple sources (national median ~€32k-€40k/yr for mid-level roles outside FAANG-tier employers); the illustrative Consulting Officer, Operations Officer, and Financial Officer salary assumptions in that scenario are **unverified** (no direct market benchmark found for these specific titles) and, for Operations/Financial Officer specifically, **not applicable to the real business**, which uses unpaid partner relationships instead.
- **Founder-reported actual resource base (Sept 2026)** — verified: 1 employee (Consulting Officer, €604.05 net/month), 2 dedicated servers (Frank, SolarSeed machine) at €71.54/month combined connectivity, and 2 unpaid partner relationships (Operations, Financial).

## Cross-Domain Links
- Related domains: `kb-key-resources`, `kb-revenue-streams`, `kb-key-partners`
- Related documents: `../../../kb-key-resources/docs/architecture/06-automation-center-key-resources.md`, `../../../kb-revenue-streams/docs/model/07-revenue-streams.md`, `../../../kb-key-partners/docs/partnerships/06-key-partners.md`

## Open Actions
- Get the Consulting Officer's actual gross salary and fully-loaded employer cost (TSU, holiday/Christmas subsidies) from payroll records, to replace the €604.05 net-only figure with a real fully-loaded cost, owner: Founder/Consultant.
- Agree and document partner-share percentages, allocations, attribution, direct-cost basis, duration/cap, and required employer/conflict, tax, and legal approvals before treating any share as a cost or payment obligation, owner: Founder/Consultant.
- Build an actual, non-payroll, per-category cost model (Odoo Online and GPT-4o pilot usage, hosting, workflow/OCR tooling, storage) from real vendor quotes to test delivery viability and direct-cost attribution; do not use it as a cost-plus pricing formula, owner: Founder/Consultant.
- Get a real payroll/EOR quote from a Portuguese provider before ever treating the illustrative scenario's salary figures as more than a rough planning assumption, owner: Founder/Consultant.
- Do not act on the illustrative 4-person scenario until Automation Center has at least 1 signed client (HC-011) and evidence of sustained deal flow; re-run the breakeven math using real figures once that evidence exists, owner: Founder/Consultant.
