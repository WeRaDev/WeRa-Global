---
metadata:
  primary_domain: value-proposition
  secondary_domains: [solution, revenue-streams, key-activities]
  owner_role: Founder/Consultant
  temporal_scope: current
  evidence_status: verified
  last_reviewed_at: 2026-09-17
  next_review_due: 2026-12-15
  provenance:
    actor: agent-warp
    source: "Inteligente/Resources/Documents/Research/HumanCenter.Pricing.md; Inteligente/Resources/Documents/Research/Interview Playbook  Financial-Advisory Automation Discovery.md; Inteligente/Resources/Documents/Research/Chatbot-Led Automation Discovery  Critique and Revised Interview Playbook.md; Inteligente/Resources/Documents/Research/Critical Review and Revised Chatbot ROI Interview Playbook.md"
    confidence: high
    review_status: draft
---
# Automation Center (Product Line)

## Purpose
Define Automation Center, Inteligente's second product line: a standalone build-and-implement automation service, distinct from the Human Center product line.

## Scope
- In scope: the automation-build service (n8n/Make/Zapier + LLM APIs) for back-office workflows, and its proprietary discovery-and-ROI methodology, at product-line level.
- Out of scope: Human Center's services, Shrinking AI (`02-services.md`) and Empowering Human (`05-empowering-human.md`); Financial Automation, Automation Center's own named service specialized for the financial industry, see `04-financial-automation.md`.

## Current State
Automation Center is a **build-and-operate automation agency service**. It targets a broad audience: any professional-services firm or solo consultant needing back-office automation (see `../../../kb-customers/docs/gtm/04-automation-center-segments.md`). Financial Automation is its first named service, specialising this general capability for the financial industry, including investment-fund-adjacent and other more heavily regulated contexts (see `04-financial-automation.md`).

**Cross-sell direction (decided, Sept 2026): Automation Center leads.** A prospect is signed for an Automation Center engagement first; Human Center consultancy (Shrinking AI) is then attached on top of that relationship, not the reverse. This corrects the earlier "sold and delivered independently of Human Center" framing and the open question below.

**Near-term focus (Sept 2026):** Automation Center is currently in the **discovery phase only** — founder-led manual discovery sessions with named prospects (see `../../../kb-solution/docs/strategy/03-automation-center-solution.md`), not yet full build-and-implement delivery. No Automation Center pilot has been signed as of this writing.

**Delivery flow:**
1. **Discovery and ROI screening** (currently founder-led manually, chatbot-assisted for lead capture only — see `../../../kb-solution/docs/strategy/03-automation-center-solution.md`) — a role-routed interview (adviser/owner, operational colleague, compliance/data owner, optional finance owner) reconstructs one recent concrete instance of a recurring deliverable, grades the evidence behind every claim (A-E), and classifies benefits as cash-releasing savings, cost avoidance, incremental margin, released capacity (not counted as cash until an owner confirms conversion), or quality/risk benefit.
2. **Screening decision** — the process outputs one of four recommendations: Stop, Measure (run a short measurement sprint), Prototype, or Pilot. It never outputs a single-point "guaranteed ROI" figure.
3. **Build** — workflow automation using n8n/Make/Zapier plus LLM APIs, OCR/document extraction where needed, and integration with the client's accounting/CRM/ERP systems.
4. **Security, testing, documentation and training** delivered before go-live.
5. **Deployment and pilot monitoring** — matched pre/post evidence: eligible/excluded volume, active time, errors, human overrides, adoption, and actual expenditure/revenue consequence.
6. **Ongoing monitoring/support retainer** as an optional recurring service.

**Example service scope** (from market-benchmark research, see `../../../kb-revenue-streams/docs/model/07-revenue-streams.md` for full pricing):
- Email triage, drafting, filing, follow-ups (basic to advanced "agent" tiers).
- Accounting/bookkeeping and document/receipt automation (OCR, expense classification, reconciliation, accountant handoff).
- Combined multi-workflow packages, which benefit from shared infrastructure economies of scale.
- Ongoing monitoring/support retainer.

## Decisions / Rules
- Do not promise ROI or implementation feasibility during the discovery interview itself; every ROI figure must show its evidence grade and be labeled screening vs. validated (post-pilot).
- Automation Center may quote using the documented market-benchmark pricing (see revenue-streams); Human Center's services must not (their pricing is undocumented, a separate gap).
- Regulated or financial-advisory clients trigger the compliance/data-owner discovery route and heightened controls (human approval, audit logging, DPA, EU data residency) before any pilot proceeds; this heightened posture is documented in full under Financial Automation, see `04-financial-automation.md`.
- Do not position Automation Center as a "private equity AI solution" merely because a client's own clients are investment funds; pricing and scope target the solo consultant/small firm buyer, not the fund itself.

## Evidence
- `../../../../Resources/Documents/Research/HumanCenter.Pricing.md` — the service-scope description is a reasonable synthesis of real agency offerings; the market-benchmark **pricing** is unverified (self-described AI-chat estimate), partially corroborated by independent Sept 2026 research (see `../../../kb-revenue-streams/docs/model/07-revenue-streams.md` for the full corroboration note) — treat as directionally plausible, not verified official pricing.
- `../../../../Resources/Documents/Research/Interview Playbook  Financial-Advisory Automation Discovery.md` — verified, original three-role discovery design.
- `../../../../Resources/Documents/Research/Chatbot-Led Automation Discovery  Critique and Revised Interview Playbook.md` — verified, chatbot-safe redesign (atomic questions, consent, bias controls, escalation).
- `../../../../Resources/Documents/Research/Critical Review and Revised Chatbot ROI Interview Playbook.md` — verified, screening-vs-investment separation, evidence grading, benefit classification.

## Cross-Domain Links
- Related domains: `kb-solution`, `kb-customers`, `kb-key-activities`, `kb-revenue-streams`, `kb-unfair-advantage`
- Related documents: `../../../kb-solution/docs/strategy/03-automation-center-solution.md`, `../../../kb-customers/docs/gtm/04-automation-center-segments.md`, `../../../kb-key-activities/docs/execution/05-automation-center-key-activities.md`, `../../../kb-revenue-streams/docs/model/07-revenue-streams.md`, `04-financial-automation.md`

## Open Actions
- Build a first working version of the discovery interview (even manually human-run, before chatbot automation), owner: Founder/Consultant.
- Validate the documented benchmark pricing against the first signed Automation Center client, owner: Founder/Consultant.
- Track conversion evidence for the Automation-Center-leads cross-sell direction (see Decisions/Rules) once the first Automation Center prospect is signed, owner: Founder/Consultant.
