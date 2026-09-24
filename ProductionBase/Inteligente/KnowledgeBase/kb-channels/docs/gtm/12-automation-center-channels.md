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
- In scope: the personal/professional-network acquisition channel and the current founder-led manual discovery process as the qualification mechanism, with the Odoo chatbot used only for lead capture.
- Out of scope: Human Center's Shrinking AI booking-page channel (`11-channels.md`); paid acquisition/media strategy; a future public/self-service chatbot deployment (not the current plan).

## Current State
**Decided (Sept 2026): acquisition channel and qualification tool are two separate things, and must be tracked separately.**

1. **Acquisition channel (top-of-funnel): the founder's personal/professional network**, concretely the founder's two active partner relationships — a partner working in a network of financial companies (Operations), and a partner at a small financial advisory firm (Financial) (see `../../../kb-key-partners/docs/partnerships/06-key-partners.md`). Automation Center's first-cohort leads come from warm introductions via these relationships, not from cold outbound, paid media, or industry associations. Named prospects already exist (mostly small financial-advisory/consultancy firms with employees, see `../../../kb-customers/docs/gtm/05-financial-automation-segments.md`) and most likely originate from these two partner networks specifically. This is a real, evidenced channel for reachability, though not yet evidenced for conversion (no session has occurred yet).
2. **Qualification tool (once a conversation starts): currently a founder-led manual discovery session, not the chatbot.** A live Odoo chatbot exists at `www.inteligente.site`, hosted on the **Frank machine** (Portugal/EU), but **corrected assessment (Sept 2026, verified against live configuration)**: it implements only generic livechat and lead-routing/lead-creation, none of the governed-interview safety/routing logic (disclosure, consent, sensitive-data interrupt, role routing, evidence grading, stop rules — see `../../../kb-key-resources/docs/architecture/06-automation-center-key-resources.md`). This corrects an earlier claim that it was "partially configured with role-routing/discovery questions" and targeted for deployment "within days" — no such timeline is currently committed. Until the governed logic is built and tested, the founder runs discovery sessions manually with the warm-introduced prospect, using the chatbot only to capture the initial lead.

**Cross-sell direction (decided, Sept 2026): Automation Center leads.** A prospect from this channel is pursued for an Automation Center engagement first; Human Center consultancy (Shrinking AI) may be attached on top once that relationship exists, not the reverse (see `../../../kb-value-proposition/docs/products/03-automation-center.md`).

This resolves the previous open question (public/self-service vs. founder-assisted): **founder-led manually for the first cohort**; a public/self-service or chatbot-led deployment is an explicit later-phase decision gated on building the governed-interview logic, not the current plan.

Secondary channel candidates (accounting-firm/bookkeeper referrals, industry associations, cold outbound, paid media — see `../../../kb-key-partners/docs/partnerships/06-key-partners.md`) are **not currently pursued**; they remain candidates for a later phase once the warm-network channel's conversion is evidenced.

## Decisions / Rules
- Do not run a real, named-prospect discovery session through the Odoo chatbot, and do not launch any public-facing chatbot, before the governed-interview safety/escalation logic (consent disclosure, sensitive-data detection, human escalation triggers, role routing, evidence grading, stop rules) is actually built and tested in it — today's chatbot only performs generic lead capture.
- The chatbot must never be presented as providing a guaranteed ROI or binding commercial commitment; every session output is a screening decision, not a signed proposal.
- Treat the personal/professional network (the two partner relationships) as the sole active acquisition channel until it is evidenced to convert (or fail to convert) with the named prospects; do not simultaneously stand up other channels before that evidence exists.
- Automation Center's channel and Human Center's Shrinking AI booking-page channel may share the same top-of-funnel website traffic in the longer term, but must diverge into distinct qualification flows once a visitor's product interest is identified — not yet relevant while the channel is founder-network-only.
- Cross-sell direction: Automation Center leads; Human Center consultancy is attached after an Automation Center relationship exists, not before (see Current State).

## Evidence
- `../../../../Resources/Documents/Research/Chatbot-Led Automation Discovery  Critique and Revised Interview Playbook.md` — verified, evidences that conversational interview systems can elicit richer responses than web forms, with documented risks (over-probing, bias) that any future public channel must control for.
- `../../../../Resources/Documents/Research/Critical Review and Revised Chatbot ROI Interview Playbook.md` — verified, defines the screening-decision output shown to a prospect.
- `../../../../Resources/Documents/Research/financial_advisory_automation_mvp.xlsx` — verified, an implementation-ready MVP spec (chatbot question script, data model, ROI model, controls/scorecard, phased implementation plan) not previously cited in this KB; see `../../../kb-key-resources/docs/architecture/06-automation-center-key-resources.md` for how it maps to the Odoo/Frank build.
- **Founder-reported named prospect pipeline (Sept 2026)** — founder self-report, treated as reachability evidence only (not independently verified); mostly small advisory/consultancy firms with employees, most likely sourced from the two partner relationships (see `../../../kb-key-partners/docs/partnerships/06-key-partners.md`). Conversion remains completely unevidenced.

## Cross-Domain Links
- Related domains: `kb-customers`, `kb-solution`, `kb-unfair-advantage`, `kb-key-partners`, `kb-key-resources`
- Related documents: `../../../kb-customers/docs/gtm/04-automation-center-segments.md`, `../../../kb-customers/docs/gtm/05-financial-automation-segments.md`, `../../../kb-solution/docs/strategy/03-automation-center-solution.md`, `../../../kb-unfair-advantage/docs/strategy/11-automation-center-unfair-advantage.md`, `../../../kb-key-resources/docs/architecture/06-automation-center-key-resources.md`

## Open Actions
- Run the first founder-led manual discovery sessions with named prospects from the two partner relationships, owner: Founder/Consultant.
- Build the missing governed-interview logic into the Odoo chatbot on Frank before relying on it for any real session, owner: Founder/Consultant.
- Evidence whether the warm-network channel actually converts (named prospect → completed discovery session → screening decision) before investing in any secondary channel, owner: Founder/Consultant.
- Confirm with each partner whether/how they expect to be compensated for referrals, given the compensation model is currently undefined (see `../../../kb-key-partners/docs/partnerships/06-key-partners.md`), owner: Founder/Consultant.
- Revisit public/self-service or chatbot-led deployment only after the governed-interview logic is built and validated in practice, owner: Founder/Consultant.
