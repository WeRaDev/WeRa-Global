---
metadata:
  primary_domain: cost-structure
  secondary_domains: [key-resources, revenue-streams]
  owner_role: Founder/Consultant
  temporal_scope: future
  evidence_status: hypothesis
  last_reviewed_at: 2026-09-18
  next_review_due: 2026-12-15
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
- In scope: cost categories for Automation Center's build-and-operate automation service, and a quantified, clearly-labeled **scenario** model for a hypothetical 4-person team (Consulting Officer, Operations Officer, Financial Officer, Fullstack Developer).
- Out of scope: Human Center's costs (founder time only, not a meaningful infrastructure cost center); any commitment that this team will actually be hired — no hires exist yet, this is a planning scenario.

## Current State
- Candidate cost categories (Automation Center): LLM/API usage, workflow-orchestration hosting (n8n/Make/Zapier), OCR/document-extraction tooling, EU-hosted storage and backups, founder/delivery time, tooling/subscriptions, marketing and the shared `www.inteligente.site` website.
- Economy-of-scale note (from pricing research on comparable vendors): shared authentication, hosting, AI API access, logging, and monitoring infrastructure reduces the marginal cost of delivering additional workflow types to the same client, which is why combined packages (e.g. accounting + email) are priced below the sum of their parts.

### Quantified scenario: 4-person Automation Center team (Portugal payroll)
**This is a hypothesis/scenario model, not a committed hiring plan or a measured actual cost — no one has been hired.** It exists to test whether a 4-person team (Consulting Officer, Operations Officer, Financial Officer, Fullstack Developer) is financially viable against Automation Center's current documented pricing, using Portugal employer-cost rules confirmed via independent research (Sept 2026):
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

**Verdict**: A 4-person, ~€150k-168k/year fully-loaded team is **not currently profitable or safely sustainable** at Automation Center's documented pricing and with a single-developer delivery capacity, given zero validated deal flow. The model implicitly assumes a sales/delivery velocity (2+ signed projects/month, sustained) with no supporting evidence. Recommendation: treat this 4-person structure as a **Phase 2 scale-up scenario**, gated on first proving out signed-client demand and delivery throughput with a much leaner structure (e.g. founder covering the Consulting Officer role plus the Fullstack Developer only), then adding Operations Officer once deal volume regularly exceeds ~3-4 signed engagements/month, and using a fractional bookkeeper/accountant instead of a full Financial Officer until revenue complexity justifies more.

## Decisions / Rules
- Do not finalize pricing tiers in `../../../kb-revenue-streams/docs/model/07-revenue-streams.md` until an actual, non-scenario cost model exists.
- Do not hire any of the 4 roles above until Automation Center has at least one signed, paying client (HC-011) and a track record of manual discovery interviews (HC-009); this scenario model must not be read as a hiring commitment.
- Re-run this scenario with real payroll quotes (e.g. from a Portuguese accountant or EOR) before treating any of the salary figures as more than a rough planning assumption.

## Evidence
- `../../../../Resources/Documents/Research/HumanCenter.Pricing.md` — unverified (self-described AI-chat estimate); notes the shared-infrastructure economy-of-scale effect for comparable vendors, used qualitatively only.
- **Portugal employer Social Security / TSU rate (23.75% employer, 11% employee, 14 monthly payments)** — verified via independent Sept 2026 web research, cross-confirmed across PwC Portugal's 2026 Tax Guide, teamed.global's Portugal employer cost breakdown, remotepass.com, and PayMetric Labs.
- **Portugal salary benchmarks (Fullstack Developer)** — verified as directionally consistent across multiple sources (national median ~€32k-€40k/yr for mid-level roles outside FAANG-tier employers); Consulting Officer, Operations Officer, and Financial Officer salary assumptions are **unverified** (no direct market benchmark found for these specific titles), flagged accordingly in the table above.

## Cross-Domain Links
- Related domains: `kb-key-resources`, `kb-revenue-streams`
- Related documents: `../../../kb-key-resources/docs/architecture/06-automation-center-key-resources.md`, `../../../kb-revenue-streams/docs/model/07-revenue-streams.md`

## Open Actions
- Build an actual, non-payroll, per-category cost model (LLM/API usage, hosting, OCR tooling, storage) with real vendor quotes rather than the current €1,200-1,800/month placeholder, owner: Founder/Consultant, due: see `../../../../tasks/backlog.md` HC-003.
- Get a real payroll/EOR quote from a Portuguese provider to replace the illustrative salary assumptions for Consulting Officer, Operations Officer, and Financial Officer before this scenario is used for any actual hiring decision, owner: Founder/Consultant.
- Do not act on the 4-person scenario until Automation Center has at least 1 signed client (HC-011) and evidence of sustained deal flow; re-run the breakeven math once that evidence exists, owner: Founder/Consultant.
