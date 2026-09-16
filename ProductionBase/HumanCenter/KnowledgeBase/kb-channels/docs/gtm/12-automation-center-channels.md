---
metadata:
  primary_domain: channels
  secondary_domains: [customers, solution, unfair-advantage]
  owner_role: Founder/Consultant
  temporal_scope: current
  evidence_status: hypothesis
  last_reviewed_at: 2026-09-16
  next_review_due: 2026-12-15
  provenance:
    actor: agent-warp
    source: "HumanCenter/Resources/Documents/Research/Chatbot-Led Automation Discovery  Critique and Revised Interview Playbook.md; HumanCenter/Resources/Documents/Research/Critical Review and Revised Chatbot ROI Interview Playbook.md"
    confidence: medium
    review_status: draft
---
# Automation Center Channels

## Purpose
Document Product 3 ("Automation Center")'s acquisition/qualification channel mechanics.

## Scope
- In scope: the discovery chatbot as a self-service acquisition and qualification mechanism.
- Out of scope: Shrinking AI's booking-page channel (`11-channels.md`); paid acquisition/media strategy.

## Current State
Automation Center's channel design differs from Shrinking AI's in one important way: **the discovery-and-ROI interview is not just a sales-qualification tool, it can itself function as the acquisition channel.** A self-service or lightly-assisted discovery chatbot embedded on the site lets a prospect reconstruct their own automation opportunity, receive a graded screening decision (Stop/Measure/Prototype/Pilot), and self-select into a next step — a differentiated top-of-funnel experience versus a generic "book a call" CTA, and consistent with research showing conversational interview systems can elicit richer, more specific responses than static web forms.

This channel is **hypothesis-stage**: the underlying methodology is fully designed (see `../../../kb-solution/docs/strategy/03-automation-center-solution.md`) but no chatbot has been built or tested, and the manual (human-run) version of the interview should be validated first.

Secondary channel candidates (not yet tested): accounting-firm/bookkeeper referrals and the automation-tooling ecosystem (see `../../../kb-key-partners/docs/partnerships/06-key-partners.md`).

## Decisions / Rules
- Do not launch a public-facing chatbot before the manual discovery process has been validated with real prospects and the mandatory safety/escalation rules are implemented (consent disclosure, sensitive-data detection, human escalation triggers).
- The chatbot must never be presented as providing a guaranteed ROI or binding commercial commitment; every session output is a screening decision, not a signed proposal.
- Automation Center's channel and Shrinking AI's booking-page channel may share the same top-of-funnel website traffic, but must diverge into distinct qualification flows once a visitor's product interest is identified.

## Evidence
- `../../../../Resources/Documents/Research/Chatbot-Led Automation Discovery  Critique and Revised Interview Playbook.md` — verified, evidences that conversational interview systems can elicit richer responses than web forms, with documented risks (over-probing, bias) that a public channel must control for.
- `../../../../Resources/Documents/Research/Critical Review and Revised Chatbot ROI Interview Playbook.md` — verified, defines the screening-decision output that would be shown to a self-service prospect.

## Cross-Domain Links
- Related domains: `kb-customers`, `kb-solution`, `kb-unfair-advantage`, `kb-key-partners`
- Related documents: `../../../kb-customers/docs/gtm/04-automation-center-segments.md`, `../../../kb-solution/docs/strategy/03-automation-center-solution.md`, `../../../kb-unfair-advantage/docs/strategy/11-automation-center-unfair-advantage.md`

## Open Actions
- Validate the manual discovery process with real prospects before building any self-service chatbot channel, owner: Founder/Consultant.
- Decide whether the chatbot channel is public/self-service or founder-assisted for the first cohort of clients, owner: Founder/Consultant.
