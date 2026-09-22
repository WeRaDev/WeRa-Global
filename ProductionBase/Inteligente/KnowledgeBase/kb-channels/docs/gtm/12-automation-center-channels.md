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
    source: "Inteligente/Resources/Documents/Research/Chatbot-Led Automation Discovery  Critique and Revised Interview Playbook.md; Inteligente/Resources/Documents/Research/Critical Review and Revised Chatbot ROI Interview Playbook.md"
    confidence: medium
    review_status: draft
---
# Automation Center Channels

## Purpose
Document Automation Center's acquisition/qualification channel mechanics.

## Scope
- In scope: the personal/professional-network acquisition channel and the founder-assisted discovery chatbot as a qualification mechanism.
- Out of scope: Human Center's Shrinking AI booking-page channel (`11-channels.md`); paid acquisition/media strategy; a future public/self-service chatbot deployment (not the current plan).

## Current State
**Decided (Sept 2026): acquisition channel and qualification tool are two separate things, and must be tracked separately.**

1. **Acquisition channel (top-of-funnel): the founder's personal/professional network.** Automation Center's first-cohort leads come from warm introductions via existing relationships, not from cold outbound, paid media, industry associations, or partner referrals. Named prospects already exist (mostly small financial-advisory/consultancy firms with employees, see `../../../kb-customers/docs/gtm/05-financial-automation-segments.md`). This is a real, evidenced channel for reachability, though not yet evidenced for conversion (no session has occurred yet).
2. **Qualification tool (once a conversation starts): a founder-assisted discovery chatbot**, not a public self-service tool. A pilot chatbot already exists, partially configured with role-routing/discovery questions, built on **Odoo** and targeted for deployment on the **TRL4 machine** (`wera-ss-pt-sn-1.tailfb390c.ts.net`, Portugal/EU) within days (see `../../../kb-key-resources/docs/architecture/06-automation-center-key-resources.md`). The founder runs or sits alongside the session with the warm-introduced prospect rather than sending a cold link — this reduces the safety/escalation risk of an unsupervised public chatbot while still testing the real tool end-to-end.

This resolves the previous open question (public/self-service vs. founder-assisted): **founder-assisted for the first cohort**; a public/self-service deployment is an explicit later-phase decision, not the current plan.

Secondary channel candidates (accounting-firm/bookkeeper referrals, industry associations, cold outbound, paid media — see `../../../kb-key-partners/docs/partnerships/06-key-partners.md`) are **not currently pursued**; they remain candidates for a later phase once the warm-network channel's conversion is evidenced.

## Decisions / Rules
- Do not launch a public-facing, unsupervised chatbot before the founder-assisted sessions have validated the discovery process with real prospects and the mandatory safety/escalation rules are implemented (consent disclosure, sensitive-data detection, human escalation triggers) — this applies even though the underlying tool (Odoo chatbot) already exists, since "built" is not the same as "validated."
- The chatbot must never be presented as providing a guaranteed ROI or binding commercial commitment; every session output is a screening decision, not a signed proposal.
- Treat the personal/professional network as the sole active acquisition channel until it is evidenced to convert (or fail to convert) with the named prospects; do not simultaneously stand up other channels before that evidence exists.
- Automation Center's channel and Human Center's Shrinking AI booking-page channel may share the same top-of-funnel website traffic in the longer term, but must diverge into distinct qualification flows once a visitor's product interest is identified — not yet relevant while the channel is founder-network-only.

## Evidence
- `../../../../Resources/Documents/Research/Chatbot-Led Automation Discovery  Critique and Revised Interview Playbook.md` — verified, evidences that conversational interview systems can elicit richer responses than web forms, with documented risks (over-probing, bias) that any future public channel must control for.
- `../../../../Resources/Documents/Research/Critical Review and Revised Chatbot ROI Interview Playbook.md` — verified, defines the screening-decision output shown to a prospect.
- `../../../../Resources/Documents/Research/financial_advisory_automation_mvp.xlsx` — verified, an implementation-ready MVP spec (chatbot question script, data model, ROI model, controls/scorecard, phased implementation plan) not previously cited in this KB; see `../../../kb-key-resources/docs/architecture/06-automation-center-key-resources.md` for how it maps to the Odoo/TRL4 build.
- **Founder-reported named prospect pipeline (Sept 2026)** — verified as a reachability fact; mostly small advisory/consultancy firms with employees.

## Cross-Domain Links
- Related domains: `kb-customers`, `kb-solution`, `kb-unfair-advantage`, `kb-key-partners`, `kb-key-resources`
- Related documents: `../../../kb-customers/docs/gtm/04-automation-center-segments.md`, `../../../kb-customers/docs/gtm/05-financial-automation-segments.md`, `../../../kb-solution/docs/strategy/03-automation-center-solution.md`, `../../../kb-unfair-advantage/docs/strategy/11-automation-center-unfair-advantage.md`, `../../../kb-key-resources/docs/architecture/06-automation-center-key-resources.md`

## Open Actions
- Deploy the Odoo chatbot on the TRL4 machine and run the first founder-assisted discovery sessions with named prospects (target: within days), owner: Founder/Consultant.
- Evidence whether the warm-network channel actually converts (named prospect → completed discovery session → screening decision) before investing in any secondary channel, owner: Founder/Consultant.
- Revisit public/self-service chatbot deployment only after the founder-assisted cohort validates the safety/escalation controls in practice, owner: Founder/Consultant.
