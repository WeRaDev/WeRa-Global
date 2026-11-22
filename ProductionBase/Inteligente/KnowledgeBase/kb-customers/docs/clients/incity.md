---
metadata:
  primary_domain: customers
  secondary_domains: [value-proposition, revenue-streams, solution]
  owner_role: Founder/Consultant
  temporal_scope: current
  evidence_status: verified
  last_reviewed_at: 2026-11-22
  next_review_due: 2027-02-22
  provenance:
    actor: agent-warp
    source: "Customers/Vasco Da Lama source pack; InCity research pack 01-05; founder Shrinking AI notes (2026-09-29); booking research ADR 0003 (2026-10-19); client conversation simplified website scope ADR 0004 (2026-11-09); live site invisiblecity.site + public OTA/competitor desk refresh (2026-11-18)"
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
| Public digital presence | **Owned brochure site live:** `https://www.invisiblecity.site/` (Frank / ADR 0004). Facebook `invisiblecitylisboa` still active. GetYourGuide **supplier** page exists (Invisible city tours / Vasco Moura dos Santos). No phase-1 instant online booking. | verified site 2026-11; GYG supplier page public 2026; booking scope per ADR 0004 |
| Reputation asset | Historically ~95 Facebook reviews at 100% recommend; stagnant follower growth (~850) at pack time. OTA review mass still lags high-volume peers. | FB stats point-in-time; re-verify before external claims |

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
- Core gap: marketed costume/character identity ≠ reviewed private day-trip product (still visible on some OTA supplier bios).
- **Market structure (2026 refresh):** Lisbon OTA shelves are Sintra-day-trip heavy. Budget **group** combos often list from ~€24–€50; **private** peers commonly ~€65–€150+/person (tickets often extra) or per-vehicle day fees. InCity resume bands (A1–A3 ~€80–€130/adult) sit in private mid — competitive **if** discoverable.
- Competitors winning attention: OTA-optimized privates (Picta, SWINGO, Host Experiences, etc.), review machines (Yellow Cab TT, Magik-class), premium care brands (e.g. Yes You Deserve), local Sintra-station operators.
- **Phase-1 site is live** but copy/verify still shows drift/missing on Home — treat content quality as commercial, not cosmetic.
- Lead-gen priorities: Google Business NAP (Lisbon corridor ops); three public packages + from-prices; WhatsApp/form SLA; testimonials page; GYG/Viator SKU audit; reviews onto Google/Tripadvisor; EN/FR/ES/PT.
- Baseline strategy: `../../../../Resources/Documents/Research/Clients/InCity/03-competitive-and-website-strategy.md`.
- **Refresh (2026-11-18):** `../../../../Resources/Documents/Research/Clients/InCity/05-competitive-marketing-refresh-2026-11.md`.

### Inteligente engagement history
1. **Human Center / Shrinking AI (Sept 2026, paid)** — €50 / 60 minutes. Trigger: AI-assisted YouTube content did not produce expected engagement. Intervention: business analysis redirected priority from more YouTube production toward a **website booking path**; deliverables included a business-model canvas and business plan for website construction.
2. **Client-side progress (founder-reported follow-up, 2026-09-29)** — client started building the website. Website completion, leads, bookings, and revenue remain unknown.
3. **Automation Center interest (founder-reported, unqualified)** — expressed interest in **website-administration automation**. No proposal, order, delivery, DPA, or payment recorded.
4. **Current commercial status (2026-10-05)** — **Pipeline Automation Center opportunity** focused on website-admin automation. Not a signed Automation Center engagement. Not Financial Automation.
5. **Booking-stack research + MVP design (2026-10-19)** — Documented that Odoo alone cannot replace a Bókun-class tour channel manager. **ADR 0003** remains a **deferred optional** booking/OTA path, not current commercial scope.
6. **Client conversation simplified scope (2026-11-09)** — Phase 1 agreed: **brochure + lead-capture website on Frank**, online; **no** tourism-platform integrations, **no** online bookings, **no** payment channels; YouTube/Facebook/Instagram **links to the website** for leads; guide **schedules manually**. Fee **€300**; **no subscription**; **3 months free hosting**. Proposal: `../../../../Resources/Documents/Proposals/InCity-website-proposal-v2.html`. Architecture: **ADR 0004**.
7. **Phase-1 site operations (2026-11)** — Public site reachable at **https://www.invisiblecity.site/** (community Odoo on Frank). Content Matrix Studio pilot for fact→final copy workflow; verify tool distinguishes drift (approved not applied) vs missing (matrix/live mismatch).
8. **Competitive/marketing refresh (2026-11-18)** — Desk refresh of private Sintra corridor pricing, OTA shelf shape, peer brand patterns; see research `05`.
9. **Content Matrix Studio + Discuss bot (2026-11-22)** — Module `inteligente_content_matrix` 19.0.1.7.2 on `incity_site`: full 8-page matrix seed, live DOM anchors, auth-only Discuss Matrix Bot with combined section cards and Website Edit deep-links. Public copy still unchanged until explicit apply after client review.

### Marketing position (2026-11 working view)
| Win cell | High customization · mid private price · guide-as-brand (story, languages, optional Goodfoot) |
| Risk cell | Guests never see InCity because discovery defaults to cheap OTA group Sintra combos |
| Near-term job | Convert site visitors → WhatsApp/form leads; fix geo/NAP; simplify public SKUs; align OTA bio with private day-trip reality |
| Not near-term | Heavy custom Odoo booking engine; AI-YouTube-led growth; costume-only brand lead |

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
- `../../../../Resources/Documents/Research/Clients/InCity/05-competitive-marketing-refresh-2026-11.md` — post go-live competitive + marketing refresh.
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
- **HC-023 go-live follow-through:** finish Content Matrix Home/Contact finals, apply checklist, re-verify; ensure RNAAT/contact/WhatsApp visible on site, owner: Founder/Consultant.
- **Google Business / NAP:** set primary ops geography to Lisbon corridor; link website; enable messaging, owner: Founder/Consultant (+ client).
- **Public package cut:** publish ≤3 clear packages with from-€ prices on site (map from catalog A1/A3/B*), owner: Founder/Consultant (+ client).
- **OTA hygiene:** audit GYG (and Viator if any) live products under Invisible City Tours; retitle/descriptions to private day-trip offer; owner: Founder/Consultant (+ client).
- After go-live, set calendar for end of 3-month free hosting renewal conversation, owner: Founder/Consultant.
- Instrument lead volume (form/WhatsApp) for 30/60/90 days post content harden, owner: Founder/Consultant.
- Collect consent pack before any public case write-up, owner: Founder/Consultant, see `../../../../tasks/backlog.md` HC-005.
- HC-022 automation qualification only if client later expands beyond brochure scope, owner: Founder/Consultant.
