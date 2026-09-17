---
metadata:
  primary_domain: solution
  secondary_domains: [problem, value-proposition, key-activities, unfair-advantage]
  owner_role: Founder/Consultant
  temporal_scope: current
  evidence_status: verified
  last_reviewed_at: 2026-09-17
  next_review_due: 2026-12-15
  provenance:
    actor: agent-warp
    source: "Inteligente/Resources/Documents/Research/Interview Playbook  Financial-Advisory Automation Discovery.md; Inteligente/Resources/Documents/Research/Chatbot-Led Automation Discovery  Critique and Revised Interview Playbook.md; Inteligente/Resources/Documents/Research/Critical Review and Revised Chatbot ROI Interview Playbook.md"
    confidence: high
    review_status: draft
---
# Automation Center Solution

## Purpose
Describe Automation Center's solution approach at product-line level: a build-and-operate automation service gated by a proprietary, evidence-graded discovery-and-ROI methodology.

## Scope
- In scope: the generic discovery/screening methodology and the automation-build delivery model, applicable line-wide.
- Out of scope: Human Center's Shrinking AI (`02-solution.md`) and Empowering Human; Financial Automation's finance-specific compliance extensions to this methodology, see `04-financial-automation-solution.md`.

## Current State

### Core differentiator: the discovery-and-ROI methodology
The methodology's design evolved across three research passes and is itself the product's moat (see `../../../kb-unfair-advantage/docs/strategy/11-automation-center-unfair-advantage.md`):

1. **Three knowledge-owner roles**, each asked only what they can reliably know: the adviser/owner (deliverable, customer outcome, fee model, demand, recent example), the operational colleague (active time, handoffs, rework, exceptions, volume), and the compliance/data owner (data location, permissions, retention, controls — a feasibility gate, not an ROI source). An optional finance-owner route is triggered only when a financial ROI figure will actually be presented.
2. **One recent concrete instance, not an average.** The interview reconstructs the most recent normal example of a recurring deliverable rather than asking abstract "how many hours does this usually take" questions, which are vulnerable to recall bias. Short recall periods and elicited-then-ranged numbers (never anchored with example ranges) improve reliability.
3. **Screening decision, not an investment-grade ROI promise.** The chatbot (or its human-run precursor) never outputs a single-point "guaranteed ROI." It classifies every benefit as one of: cash-releasing saving, cost avoidance, incremental contribution margin, released capacity (not counted as cash until an owner confirms conversion), or quality/risk benefit (monetized only with evidence). It calculates `Recurring unit x eligible volume x observed net improvement x adoption x value-capture rate - full cost`, and separates capacity from cash: `Released capacity = V x E x (Tb-Ta) x A`; `Financial benefit = Cs + Ca + Mi + Qv`; `ROI = (Financial benefit - full cost) / full cost x 100`.
4. **Evidence grading (A-E).** Every input is graded: A = system record/invoice/ledger, B = recent sample/timestamps/diary, C = reconciled two-respondent estimate, D = single unsupported recollection, E = automation-team/chatbot assumption (never presented as client evidence). Low-grade opportunities are redirected to a short **measurement sprint** (sample 5-10 normal cases, record active time/exceptions) rather than guessed.
5. **Four possible outcomes:** Stop (no material/permissible opportunity), Measure (insufficient baseline, run a measurement sprint), Prototype (value route exists, low-risk technical test justified), Pilot (baseline, controls, owner and success thresholds are ready).
6. **Safety and neutrality constraints** (mandatory if/when implemented as an actual chatbot): one question per turn, no leading or praising language, no silent gap-filling, explicit consent/disclosure before collection, sensitive-data detection and interruption, mandatory human escalation for legal/tax/investment-advice requests, credentials, suspected breaches, disputed consent, or binding-ROI-guarantee requests.

### Delivery: automation build
Once a Pilot is approved: process mapping and design, workflow automation via n8n/Make/Zapier, LLM API integration, OCR/document extraction where needed, integration with the client's accounting/CRM/ERP systems, security/testing/documentation/training, deployment, then matched pre/post pilot monitoring (eligible/excluded volume, active time, errors, overrides, adoption, actual expenditure/revenue consequence, full cost) before any renewal or expansion decision.

### Compliance for regulated clients
For financial-advisory or otherwise regulated clients, the compliance/data-owner route (present in the generic methodology above) becomes mandatory rather than optional. Financial Automation extends this route with finance-specific jurisdictional and sector-obligation detail, see `04-financial-automation-solution.md`.

## Decisions / Rules
- Never convert a respondent's estimate into a financial ROI figure without labeling its evidence grade.
- Never count released staff capacity as cash benefit unless a named owner confirms how and when it converts to a financial outcome.
- Route legal/tax/investment-advice requests, credential exposure, suspected breaches, and disputed consent to human escalation immediately; the automated/human-run interview does not resolve these itself.
- Regulated-client engagements (see Financial Automation) require the compliance/data-owner route to complete before any pilot is proposed.

## Evidence
- `../../../../Resources/Documents/Research/Interview Playbook  Financial-Advisory Automation Discovery.md` — verified, original three-role discovery design and ROI worksheet.
- `../../../../Resources/Documents/Research/Chatbot-Led Automation Discovery  Critique and Revised Interview Playbook.md` — verified, chatbot-safe conversational design, evidence model, escalation triggers.
- `../../../../Resources/Documents/Research/Critical Review and Revised Chatbot ROI Interview Playbook.md` — verified, screening-vs-investment separation, benefit classification, evidence grading, financial formulas.

## Cross-Domain Links
- Related domains: `kb-value-proposition`, `kb-key-activities`, `kb-unfair-advantage`, `kb-customers`
- Related documents: `../../../kb-value-proposition/docs/products/03-automation-center.md`, `../../../kb-key-activities/docs/execution/05-automation-center-key-activities.md`, `../../../kb-unfair-advantage/docs/strategy/11-automation-center-unfair-advantage.md`, `04-financial-automation-solution.md`

## Open Actions
- Run the discovery methodology manually (human-led) with the first few prospects before investing in chatbot automation, owner: Founder/Consultant.
- Build and test a real chatbot implementation once the manual version is validated, owner: Founder/Consultant.
- Define the client-authorized secure channel for redacted artifact collection (the interview design assumes one exists but does not create it), owner: Founder/Consultant.
