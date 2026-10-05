---
metadata:
  primary_domain: value-proposition
  secondary_domains: [governance]
  owner_role: Founder/Consultant
  temporal_scope: current
  evidence_status: verified
  last_reviewed_at: 2026-09-29
  next_review_due: 2026-12-29
  provenance:
    actor: agent-warp
    source: "Inteligente/Resources/Documents/Research/Human Center — Product 1  Shrinking AI  Desk Research, Heuristic Evaluation &amp; Competitive Analysis.md; founder-defined Human Center routing and Consultancy Automation internal-first decision (2026-09-29)"
    confidence: medium
    review_status: draft
---

# Company Overview

## Purpose
Establish the canonical company identity for Inteligente and its product-line/service structure.

## Scope
- In scope: brand, legal entity, website, business/product-line/service structure, ecosystem relationship.
- Out of scope: compliance/DPA posture (see `../../../kb-governance/docs/legal/11-legal-structure.md`).

## Current State
- Name: **Inteligente** — the consultancy business operated by **Inteligente Razão — Unipessoal LDA**.
- Website: `www.inteligente.site`.
- Inteligente operates two product lines, each hosting one or more named services. Keep their product identities and primary navigation, tone, and messaging distinct; refer clients across lines when their needs warrant it:
  1. **Human Center** — a consultancy product line offering human-facilitated services around AI adoption:
     - **Shrinking AI** (B2B): a human-facilitated diagnostic service that converts "AI frustration" into a bounded, AI-ready problem statement via a paid RCGFC session. See `../products/02-services.md`.
     - **Expanding Human** (individuals and organizations, hypothesis-stage): explores where AI may support a person's or organization's goals, problems, or ambitions. One founder-reported paid session (€50/60 minutes) is recorded, not a validated price or repeatable method. See `../products/05-expanding-human.md`.
  2. **Automation Center** — a build-and-implement automation product line (n8n/Make/Zapier + LLM APIs) for back-office workflows, gated by a proprietary, deliverable-first and evidence-graded discovery-and-ROI methodology, addressable to any professional-services firm or solo consultant. See `../products/03-automation-center.md`.
     - **Consultancy Automation**: a planned internal Automation Center product/use case to automate Inteligente's own consultancy operations and measure efficiency and outcomes before wider external rollout. Its workflows, baseline, and hosting are not yet defined or validated.
     - **Financial Automation**: Automation Center's first named external service, specialising in workflow automation for the financial industry, including investment-fund-adjacent and other more heavily regulated contexts. See `../products/04-financial-automation.md`.
- **Need-based routing across product lines**: unclear AI opportunities go to Expanding Human; unsatisfactory results from AI already in use go to Shrinking AI; a defined organizational process-automation need goes to Automation Center. This routing is a strategy, not evidence of cross-line conversion.
- Geography: Western Europe and the Nordics — targeting companies with budgets for AI and cultures of supporting employees with organisational tools. Automation Center's addressable market is broader than Human Center's Shrinking AI service (see `../../../kb-customers/docs/gtm/04-automation-center-segments.md` and `../../../kb-customers/docs/gtm/05-financial-automation-segments.md`).
- Ecosystem: developed under `ProductionBase/Inteligente/` within the WeRa Global umbrella repository (`native` vcs_mode, `enforced` baseline_policy per `ProductionBase/repos.yaml`).

## Decisions / Rules
- Keep Human Center and Automation Center's product identities and primary navigation, tone, and CTA framing distinct; need-based referrals between them are appropriate and do not imply that their services or delivery methods are interchangeable.
- Automation Center may be represented externally as an AI-automation agency (n8n/Make/Zapier workflow builder) with documented, market-benchmark-derived pricing — this positioning is directionally corroborated by independent research but not yet validated against a signed client (see `../../../kb-revenue-streams/docs/model/07-revenue-streams.md`), not to be confused with Human Center's facilitation-only positioning.
- Expanding Human remains hypothesis-stage despite one reported paid session; its audience, pricing, and repeatable delivery method are not validated.
- **Cross-line referral strategy (decided, Sept 2026): need-based and bidirectional.** Human Center clients may be referred to Automation Center for a defined organizational automation need; Automation Center clients may be referred to Shrinking AI or Expanding Human when the need is human facilitation or exploration of AI opportunities. The two reported Human-to-Automation expressions of interest are unqualified; no cross-line order, delivery, or reverse-direction conversion is established.
- **Near-term focus (Sept 2026): internal-first Consultancy Automation.** This planned internal use case will automate Inteligente's own consultancy operations and measure efficiency/outcomes; the specific workflows, baseline, and hosting are open. The external partner-led Financial Automation Discovery Pilot was formally initiated but is **deferred, not cancelled**, until internal validation is complete and all existing safety, actionable-human-notification, privacy, and data-flow gates pass. It has no first-session date or result. Odoo Online remains the planned external-pilot platform; any later Frank MVP or SolarSeed first-customer deployment retains its separate readiness and isolation gates (see `../../../kb-solution/docs/strategy/03-automation-center-solution.md`). Do not represent either internal or external Automation Center validation as complete or claim paid external delivery.

## Evidence
- `../../../../Resources/Documents/Research/Human Center — Product 1  Shrinking AI  Desk Research, Heuristic Evaluation &amp; Competitive Analysis.md` — verified (states the entity name, product structure, and geography directly from project documentation relayed within the research brief).
- `../../../../Resources/Documents/Research/Shrinking AI (B2B Consultancy) — Desk Research, He.md` — verified, corroborating desk research for Shrinking AI.
- `../../../../Resources/Documents/Research/HumanCenter.Pricing.md` — **unverified**. This is a first-person, self-described AI-chat pricing estimate ("I found... my estimate..."), not measured or client-sourced data. An independent web-research pass (Sept 2026) found partial corroboration: FETCHER Solutions' live pricing page matches the cited €600/workflow and €2,800 document/OCR-agent figures exactly, and the broader European/US no-code-automation market (BOVO Digital, Polish agencies, French-market surveys) sits in a comparable €600-€12,000+ range. However, NeuraWeb's own current pricing has drifted materially from the tiers cited in the source document, and one source reports category-wide price declines of 60-75% over 18 months — so treat the benchmark as directionally plausible but stale and due for periodic re-verification (see `../../../kb-revenue-streams/docs/model/07-revenue-streams.md` for the full corroboration note), not as "verified official pricing."
- `../../../../Resources/Documents/Research/Interview Playbook  Financial-Advisory Automation Discovery.md`, `../../../../Resources/Documents/Research/Chatbot-Led Automation Discovery  Critique and Revised Interview Playbook.md`, `../../../../Resources/Documents/Research/Critical Review and Revised Chatbot ROI Interview Playbook.md` — verified, define Automation Center's discovery-and-ROI methodology and Financial Automation's regulated-industry framing (these are methodology/process documents, not pricing sources).
- **Founder-defined Human Center routing and Consultancy Automation internal-first decision (2026-09-29)** — primary business-model decisions; routing has no demonstrated cross-line conversion, and Consultancy Automation has not yet been built or validated.

## Cross-Domain Links
- Related domains: `kb-governance`, `kb-solution`, `kb-problem`, `kb-customers`
- Related documents: `../products/02-services.md`, `../products/03-automation-center.md`, `../products/04-financial-automation.md`, `../products/05-expanding-human.md`, `../../../kb-governance/docs/legal/11-legal-structure.md`, `../../../kb-problem/docs/market/01-problem.md`

## Open Actions
- Validate Expanding Human's target segments, willingness to pay, and repeatable delivery without generalizing from the single paid observation, owner: Founder/Consultant, see `../../../../tasks/backlog.md` HC-013.
- Track need-based referrals, qualified opportunities, orders, and outcomes in both directions between Human Center and Automation Center; keep the two existing interest signals separate from conversion, owner: Founder/Consultant, see `../../../../tasks/backlog.md` HC-017.
- Define and validate the internal Consultancy Automation workflow and baseline before resuming any external Financial Automation pilot, owner: Founder/Consultant, see `../../../../tasks/backlog.md` HC-021.
