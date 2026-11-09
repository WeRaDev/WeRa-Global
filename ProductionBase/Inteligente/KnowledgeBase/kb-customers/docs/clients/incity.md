---
metadata:
  primary_domain: customers
  secondary_domains: [value-proposition, revenue-streams, solution]
  owner_role: Founder/Consultant
  temporal_scope: current
  evidence_status: verified
  last_reviewed_at: 2026-11-09
  next_review_due: 2027-02-09
  provenance:
    actor: agent-warp
    source: "Customers/Vasco Da Lama source pack; InCity research pack; founder Shrinking AI notes (2026-09-29); booking research ADR 0003 (2026-10-19); client conversation simplified website scope ADR 0004 (2026-11-09)"
    confidence: medium
    review_status: draft
  sensitivity: internal-only-client-record
---

# InCity (client dossier)

## Purpose
Canonical Inteligente client record for **InCity** (codename), operating publicly as **Invisible City Tours** — the formerly anonymized "Client B / self-employed tour guide" account.

## Scope
- In scope: identity, operator contacts (internal-only), business profile, tour catalog/pricing summary, competitive and website strategy summary, Inteligente engagement history, current pipeline status.
- Out of scope: committing raw client photos/media binaries; running automation against live client systems; public case publication without a signed consent pack.

## Current State

### Identity
| Field | Value | Evidence status |
|---|---|---|
| Inteligente client codename | **InCity** | verified (founder naming, 2026-10-05) |
| Operating brand | **Invisible City Tours** | verified (client materials + public Facebook page) |
| Related labels in client materials | DEEPSINTRA / Invisible City Lab (YouTube/lab framing) | unverified productization; keep secondary |
| Operator / brand face | Vasco Da Lama (also referenced as Vasco Mouradossantos on personal FB context) | verified from client source pack |
| Business model | Solo-operator private guided day tours (Lisbon corridor: Sintra, Cascais, Cabo da Roca) | verified from reviews/research synthesis |
| Registered address signal | Cebolais de Cima, Castelo Branco district (admin), while operations are Lisbon/Sintra/Cascais | verified from Facebook page research; geo mismatch is a known SEO risk |
| Public digital presence | Facebook page `invisiblecitylisboa`; no owned website or public online booking at research time | verified as of source research (2025–2026 pack) |
| Reputation asset | 100% recommend across ~95 Facebook reviews; stagnant follower growth (~850) | verified from page-insights research |

### Internal-only contacts
Treat as **internal client CRM data**. Do not publish on Inteligente marketing surfaces without explicit client consent.

| Channel | Value |
|---|---|
| Phone / WhatsApp candidate | `+351 967 761 674` |
| Email | `saintvasco@gmail.com` |
| Facebook business page | `https://www.facebook.com/invisiblecitylisboa/` |
| Source folder (local, out of umbrella git tracking) | `Customers/Vasco Da Lama/` |

### Offer snapshot (operating brand)
Real delivered product (from reviews and tour resume), not the outdated "costumed historical character walking tour" bio alone:

- Private, customizable day trips from Lisbon and/or Sintra station
- Multilingual guide/storytelling; personality-driven solo brand
- Optional regenerative "Goodfoot" park-help upgrades and gourmet stops
- Full-day and short packages spanning Cascais / Boca do Inferno / Cabo da Roca / Sintra center / selected palace parks

**Indicative client-listed price bands (EUR/adult, from tour resume; not Inteligente quotes):**

| Code | Product (summary) | Duration | Indicative price |
|---|---|---|---|
| A1 | Invisible Classic Grand Tour (circular / CP train variants) | 8h | 120 / 90 pax |
| A2 | Grand Tour with hero inside palace | 8h | 130 / 100 pax |
| A3 | Invisible Classic Short | 6h | 100 / 80 adult |
| A6 / B8 | Obvious Sintra 3-shot express | short multi-palace | 180 tickets-in / 100 adult variants |
| B1 | Twin Peaks / National Palace short | 3h | 70 pax (min 2) |
| B2–B4 | Pena / Regaleira / Montserrat specials | 4h | 100 adult |
| B5 | Panoramic through the park | 4h | 140 adult |
| B6 | Goodfoot tour | 6h | 60 adult symbolic |

Full structured catalog lives in research: `../../../../Resources/Documents/Research/Clients/InCity/02-tour-catalog-summary.md`.

### Competitive and website strategy (summary)
- Core gap: marketed costume/character identity ≠ reviewed private day-trip product.
- Competitors (Viator, Living Private Tours, Premiere Tours, Mr. Local, etc.) win on transparent pricing, OTA listings, owned websites, and booking friction removal.
- Recommended site IA: Home, Tours (+ destination landings), About/guide, Testimonials, Contact/booking, multi-language EN/FR/PT/ES; optional vehicles/blog/seasonal pages.
- Lead-gen priorities: fix Lisbon vs Castelo Branco geo signals; Google Business / TripAdvisor / GetYourGuide presence; WhatsApp + booking form; public "from €X" pricing; review funnel off Facebook-only trust.
- Detailed strategy: `../../../../Resources/Documents/Research/Clients/InCity/03-competitive-and-website-strategy.md`.

### Inteligente engagement history
1. **Human Center / Shrinking AI (Sept 2026, paid)** — €50 / 60 minutes. Trigger: AI-assisted YouTube content did not produce expected engagement. Intervention: business analysis redirected priority from more YouTube production toward a **website booking path**; deliverables included a business-model canvas and business plan for website construction.
2. **Client-side progress (founder-reported follow-up, 2026-09-29)** — client started building the website. Website completion, leads, bookings, and revenue remain unknown.
3. **Automation Center interest (founder-reported, unqualified)** — expressed interest in **website-administration automation**. No proposal, order, delivery, DPA, or payment recorded.
4. **Current commercial status (2026-10-05)** — **Pipeline Automation Center opportunity** focused on website-admin automation. Not a signed Automation Center engagement. Not Financial Automation.
5. **Booking-stack research + MVP design (2026-10-19)** — Documented that Odoo alone cannot replace a Bókun-class tour channel manager. **ADR 0003** remains a **deferred optional** booking/OTA path, not current commercial scope.
6. **Client conversation simplified scope (2026-11-09)** — Phase 1 agreed: **brochure + lead-capture website on Frank**, online; **no** tourism-platform integrations, **no** online bookings, **no** payment channels; YouTube/Facebook/Instagram **links to the website** for leads; guide **schedules manually**. Fee **€300**; **no subscription**; **3 months free hosting**. Proposal: `../../../../Resources/Documents/Proposals/InCity-website-proposal-v2.html`. Architecture: **ADR 0004**.

### Phase 1 architecture (ADR 0004 — current)
| Layer | Choice |
|---|---|
| Website | Brochure + contact/lead CTAs on **Frank** |
| Social | YT / FB / IG link to site |
| Scheduling | Manual by guide |
| Bookings / payments / OTAs | Out of scope |
| Price | €300; hosting free 3 months |

### Deferred booking path (ADR 0003 — not phase 1)
| Layer | Future option |
|---|---|
| Inventory / OTAs | Bókun-class engine |
| Direct book + pay | Engine widget |
| First OTA | Viator, etc. |

### Segment fit (hypothesis)
Closest existing Shrinking AI labels: solo creative/service professional / A3-adjacent independent professional — not a clean A4 consultant ICP match. For Automation Center, fits the broad solo-operator back-office automation hypothesis (booking/admin ops), still unscored.

## Decisions / Rules
- Use **InCity** as the Inteligente internal client codename; use **Invisible City Tours** when referring to the operating tourism brand.
- Prefer named **InCity** over legacy "Client B" wording in Inteligente docs.
- Keep this dossier **internal-only** for contact fields; strip contacts before any public case study.
- Do not run automation against real InCity accounts without signed authorization and a DPA (`../../../../WARP.md`, `../../../../AGENTS.md`).
- Do not commit raw client photo/media binaries from `Customers/Vasco Da Lama/Client materials/` into the Inteligente repo.
- Do not treat Automation Center interest as an order, revenue event, or validated cross-sell conversion.
- Website construction remains primarily client-owned unless a separate scoped Inteligente engagement is signed.
- Follow **ADR 0004** for current delivery: brochure site on Frank; no phase-1 booking/OTA/payments.
- If booking/OTA work is later ordered, revisit **ADR 0003** (engine as inventory master; not Odoo-native OTA channel manager).

## Evidence
- `../../../../Resources/Documents/Research/Clients/InCity/01-business-profile-and-audience.md` — sanitized synthesis of Facebook/audience research.
- `../../../../Resources/Documents/Research/Clients/InCity/02-tour-catalog-summary.md` — sanitized tour resume summary.
- `../../../../Resources/Documents/Research/Clients/InCity/03-competitive-and-website-strategy.md` — sanitized competitive + website strategy.
- `../../../../Resources/Documents/Research/Clients/InCity/04-booking-stack-odoo-vs-bokun.md` — Odoo vs Bókun-class OTA findings.
- `../../../../docs/adr/0004-incity-brochure-website-phase1.md` — current phase-1 decision.
- `../../../../docs/adr/0003-incity-minimum-effort-booking-mvp.md` — deferred booking/OTA path.
- `../../../../Resources/Documents/Proposals/InCity-website-proposal-v2.html` — client proposal v2.
- `../../../../tasks/incity-mvp-booking-website.md` — legacy booking MVP plan (superseded for phase 1).
- Local source pack (not in umbrella git): `Customers/Vasco Da Lama/` including `INVISIBLE CITY TOURS RESUME.docx(.md)`, desk-research markdowns, `COMPETITORS.docx`, `mr.Local - structure.md`, client materials.
- Founder-reported paid Shrinking AI session and Automation Center interest (business-analysis session, 2026-09-29) — primary retrospective; no independent client artifacts reviewed in-repo.

## Cross-Domain Links
- Related domains: `kb-customers`, `kb-value-proposition`, `kb-revenue-streams`, `kb-metrics`, `kb-solution`
- Related documents: `../gtm/03-customer-segments.md`, `../gtm/04-automation-center-segments.md`, `../../../kb-value-proposition/docs/products/02-services.md`, `../../../kb-value-proposition/docs/products/03-automation-center.md`, `../../../kb-metrics/docs/financial/09-key-metrics.md`

## Open Actions
- Confirm v2 proposal in writing and collect §8 client inputs (domain, tours, contacts, social URLs, photos), owner: Founder/Consultant.
- Deliver HC-023 phase-1 brochure website on Frank per ADR 0004 / proposal v2, owner: Founder/Consultant.
- After go-live, set calendar for end of 3-month free hosting renewal conversation, owner: Founder/Consultant.
- Collect consent pack before any public case write-up, owner: Founder/Consultant, see `../../../../tasks/backlog.md` HC-005.
- HC-022 automation qualification only if client later expands beyond brochure scope, owner: Founder/Consultant.
