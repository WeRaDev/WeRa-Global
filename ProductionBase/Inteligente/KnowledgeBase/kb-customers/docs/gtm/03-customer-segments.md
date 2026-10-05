---
metadata:
  primary_domain: customers
  secondary_domains: [problem, value-proposition]
  owner_role: Founder/Consultant
  temporal_scope: current
  evidence_status: verified
  last_reviewed_at: 2026-09-29
  next_review_due: 2026-12-29
  provenance:
    actor: agent-warp
    source: "Inteligente/Resources/Documents/Research/Human Center — Product 1  Shrinking AI  Desk Research, Heuristic Evaluation &amp; Competitive Analysis.md; founder-reported anonymized case summaries and outcome follow-up (business-analysis session, 2026-09-29)"
    confidence: medium
    review_status: draft
---

# Customer Segments

## Purpose
Define Shrinking AI's validated target customer segments and go-to-market approach.

## Scope
- In scope: the four scored B2B segments validated for Shrinking AI.
- Out of scope: Expanding Human segments (hypothesis-stage, see `06-expanding-human-segments.md`); Automation Center segments, which are broader and not yet scored — see `04-automation-center-segments.md`; enterprise/PE-fund direct clients (see Decisions / Rules).

## Current State
Four B2B segments were scored across six weighted criteria (pain intensity 25%, readiness to act 20%, willingness to pay 20%, channel efficiency 15%, upgrade potential 10%, case-study quality 10%):

| Segment | Score | Role |
|---|---|---|
| A4 — AI-frustrated consultant/freelancer | **91/100** | **Primary ICP** |
| A1 — Micro-SME owner | 86/100 | Secondary |
| A2 — Ops lead, small org | 84/100 | Tertiary |
| A3 — Independent professional | 79/100 | Tertiary |

Because the primary ICP (A4) is itself a consultant/freelancer segment, copy, proof, and CTA framing should be built primarily around a **peer-to-peer professional register** (consultant speaking to consultant), not a generic SME sales register. This also creates a distribution opportunity: A4 clients are well-positioned to refer their own clients, supporting a light partner/referral mechanic (see `../../../kb-key-partners/docs/partnerships/06-key-partners.md`).

**Methodology caveat**: the six criteria and their weights (25/20/20/15/10/10%) are explicitly documented in the source research, but the per-segment, per-criterion scores that produce the 91/86/84/79 totals are not accompanied by a visible scoring rubric or raw data (e.g. survey responses, interview counts) — they read as qualitative judgment calls made during desk research, not measurements against real prospects. Treat the ranking (A4 > A1 > A2 > A3) as a reasonable prioritization hypothesis, not a validated fact, until confirmed by real discovery calls (see Open Actions, HC-008).

**Founder-reported real-world evidence (2 initial Shrinking AI client accounts; follow-up update 2026-09-29)**: Client A, a self-publishing writer, had spent about a month trying to use AI for book editing/formatting and print/e-book preparation without a satisfactory result; the consultant elicited requirements, configured AI, and sent pre-publication materials. The client later confirmed using those materials to print and publish the book; causal contribution and business impact remain unknown. Client A then paid €50 for a separate 60-minute Expanding Human consultancy on using AI in the business beyond editing and formatting, receiving a business model canvas and a "marketing scope of AI application." The client is considering unspecified Automation Center services. Client B, a self-employed tour guide, had tried AI-generated YouTube content without the expected engagement; the consultant redirected the proposed priority toward a booking website and delivered a business-model canvas and business plan for website construction. The client has started building the site and expressed interest in ordering website-administration automation. No Automation Center order or delivery was reported. See `../../../kb-value-proposition/docs/products/02-services.md` for the fuller anonymized chronology. Both initial clients are solo creative/service professionals, closest to A3 ("Independent professional") but not a clean match. Their shared pattern—unsatisfactory self-directed AI use followed by a goal-focused consultation—is worth testing, but the needs and deliverables differed. The separate Expanding Human follow-up and two Automation Center interest signals are useful observations, not enough to validate A3, A4, a new segment, cross-sell conversion, or a generalized market need; keep the A4 ranking as a desk-research prioritization hypothesis until discovery calls validate it. Website completion, leads/bookings, and attributable impact remain unknown.

## Decisions / Rules
- Do not position or price Shrinking AI as a PE-fund-facing AI vendor; if an A4 client's own clients happen to be investment funds, the buyer is still the solo consultant, not the fund.
- Any client whose data includes confidential deal/investor information requires the stricter security posture (human approval, audit logs, DPA, EU data residency) per `../../../../SOUL.md`.
- Build the website's primary CTA and copy around the A4 (consultant/freelancer) register first; treat A1/A2/A3 as secondary framing variants, not the default.

## Evidence
- `../../../../Resources/Documents/Research/Human Center — Product 1  Shrinking AI  Desk Research, Heuristic Evaluation &amp; Competitive Analysis.md` — verified, full scoring table and rationale.
- `../../../../Resources/Documents/Research/HumanCenter.Pricing.md` — unverified, third-party desk research; originally used to describe a solo-consultant/investment-fund-adjacent segment, now understood as a narrower, separate pricing-benchmark thread rather than the validated ICP definition (see `../../../kb-revenue-streams/docs/model/07-revenue-streams.md`).
- **Founder-reported anonymized case summaries and outcome follow-up (business-analysis session, 2026-09-29)** — primary, retrospective evidence for two client accounts, one separate paid Expanding Human consultancy, reported use of materials for publication, website-build progress, and Automation Center interest; no independent client artifacts or downstream business-impact metrics were reviewed.

## Cross-Domain Links
- Related domains: `kb-problem`, `kb-value-proposition`, `kb-channels`, `kb-key-partners`
- Related documents: `../../../kb-problem/docs/market/01-problem.md`, `../../../kb-value-proposition/docs/products/02-services.md`, `../../../kb-key-partners/docs/partnerships/06-key-partners.md`

## Open Actions
- Run discovery calls to validate segment fit and rank order, owner: Founder/Consultant, due: see `../../../../tasks/backlog.md` HC-008.
- Assess, once more real clients are booked, whether a fifth segment (solo creative/service professional using AI for a production task, distinct from A3) should be added and scored, owner: Founder/Consultant.
