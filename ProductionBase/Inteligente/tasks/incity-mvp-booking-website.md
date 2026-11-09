# InCity MVP — Minimum-effort bookable website + OTA path

**Status:** SUPERSEDED for phase 1 (2026-11-09) by brochure website scope — see `docs/adr/0004-incity-brochure-website-phase1.md` and `Resources/Documents/Proposals/InCity-website-proposal-v2.html`. Retain as deferred booking/OTA plan if later ordered.  
**Client:** InCity / Invisible City Tours  
**Owner:** Founder/Consultant  
**ADR:** `docs/adr/0003-incity-minimum-effort-booking-mvp.md`  
**Research:** `Resources/Documents/Research/Clients/InCity/04-booking-stack-odoo-vs-bokun.md`  
**Backlog:** HC-023 (delivery), HC-022 (qualification)

## Problem statement
InCity has strong in-person reviews but weak digital capture (phone/Gmail/Facebook). AI YouTube did not deliver expected engagement. They need a **minimum path to paid bookings** with transparent packages and at least one major OTA, without building a custom Odoo channel manager.

## Goal (MVP definition of done)
A traveller can:
1. Discover a clear InCity/Invisible City Tours offer online
2. See **from-price**, duration, and inclusions for a small set of tours
3. **Book and pay** on a direct channel (widget or engine site) with automatic confirmation
4. Book the same inventory via **Viator** without manual double-entry calendar risk
5. Operator sees all bookings in **one engine calendar**

Optional stretch (same sprint if free): GetYourGuide connected; Tripadvisor listing hygiene done.

## Non-goals
- Odoo as booking engine or OTA connector
- Full A1–B8 catalogue on the public site
- Booking.com Experiences, full Bókun Marketplace sprawl
- Website-admin automation product build
- AI content / DeepSintra lab
- Public case study without consent pack

## Scope

### In scope
- Choose engine (default Bókun; document if peer chosen)
- Simplify catalogue to 3–5 public products
- Configure availability, cut-offs, cancellation policy, mobile tickets
- Direct booking UX (engine site **or** embed on existing/simple page)
- Payment provider connected for direct channel
- Viator supplier connection + product mapping
- Basic brand facts: who Vasco is, what is private/day-trip positioning (not costume-first)
- Operator runbook: daily calendar check, closeouts, WhatsApp fallback for custom requests
- Success metrics baseline (see Validation)

### Out of scope
- Custom development on Odoo Online/sh for OTA APIs
- Multi-language perfection beyond what the engine gives cheaply
- Complex dynamic pricing / allocation manager enterprise features
- Migrating historical Facebook reviews automatically

## Minimum product set (proposal)
Collapse internal SKUs into public offers (names adjustable with client):

| Public MVP product | Based on | Notes |
|---|---|---|
| Classic Lisbon → Sintra day (8h) | A1 family | Full Moon / return options as variants if engine allows |
| Classic short day (6h) | A3 | Lower time/price band |
| Sintra station palace special (4h) | B2–B4 pattern | One palace choice or three separate products max |
| Custom private tour request | — | WhatsApp/form only; not OTA-first |

Hold Goodfoot / gourmet / 3-shot express for phase 2 unless client insists on one hero differentiator.

## Work plan (minimum effort sequence)

### Gate 0 — Commercial readiness (HC-022)
- Confirm budget for engine subscription + expected OTA commissions
- Confirm who owns accounts (client vs Inteligente-assisted)
- Written authorization for configuration access if Inteligente operates tools
- Privacy: list processors (engine, Stripe/PayPal, Viator, GYG)

### Step 1 — Engine foundation (day 1–2)
- Create engine account; set company profile, currency EUR, timezone Lisbon
- Connect payments for direct bookings
- Create resources (vehicle/guide capacity) matching real max pax

### Step 2 — Catalogue + calendar (day 2–4)
- Enter 3–5 products with photos (client-owned, consented), duration, meeting points, inclusions/exclusions
- Price bands from client resume; set direct rate and OTA-aware net/gross strategy
- Publish availability rules; block personal unavailable days

### Step 3 — Direct bookable surface (day 3–5)
- **Path E (absolute min):** publish engine website with EN copy
- **Path B (if brand URL required):** one-page or 5-page shell + embed widget (Odoo Website only if already decided and does not delay go-live)
- WhatsApp click-to-chat retained for custom requests

### Step 4 — Viator (day 5–15 wall-clock; much is approval wait)
- Start/complete Viator supplier onboarding early (parallel with steps 1–3)
- Map products; enable instant confirmation; align cancellation policy
- Verify test booking → engine calendar → inventory drop

### Step 5 — Hygiene + soft launch (day 5–10 parallel)
- Google Business / Facebook location: operational Lisbon corridor, not misleading Castelo Branco-only tourist geo
- Tripadvisor presence check
- Replace costume-first bio with private personalized day-tour positioning
- Operator checklist PDF/one-pager

### Step 6 — Post-MVP only
- GetYourGuide
- Google Things to Do
- FR/PT/ES
- Odoo CRM sync / Inteligente admin automation (separate signed scope)
- Review automation after-trip

## Validation plan
| Check | Pass criteria |
|---|---|
| Direct test booking | Paid or sandbox booking appears in engine; confirmation email/SMS works |
| Inventory integrity | After direct booking, Viator availability reduced (or product closed) without manual edit |
| Operator usability | Vasco can close a day and create a manual offline booking unassisted |
| Content | Public site does not claim costume-only product; shows from-pricing |
| Legal/ops | Cancellation policy and meeting-point instructions visible |
| Metrics (2–4 weeks) | Count: direct bookings, OTA bookings, abandoned chats, double-book incidents (=0 target) |

## Effort estimate (Inteligente-assisted, happy path)
- Hands-on configuration/coaching: **~1–3 working days** spread over 1–2 weeks
- Calendar time dominated by **OTA approval** and client asset supply (photos, policies, IBAN/payments)
- Custom Odoo OTA build alternative: **weeks+** — rejected for MVP per ADR 0003

## Dependencies
- Client product decisions (which 3–5 tours)
- Payment account
- Photo rights / guide bio text
- Viator (and optional GYG) supplier accounts
- No dependency on Frank, SolarSeed, or Inteligente Financial Automation pilot

## Risks and mitigations
| Risk | Mitigation |
|---|---|
| OTA rejection/delay | Launch direct widget first; OTA as parallel track |
| Over-catalogue complexity | Hard cap 5 public products |
| Commission shock | Show net-revenue scenarios before go-live |
| Double systems later | ADR: engine remains inventory master if Odoo added |
| Unauthorized access | HC-022 gate; client-owned credentials preferred |

## Deliverables checklist
- [ ] Engine account configured
- [ ] 3–5 live products + calendar
- [ ] Direct bookable URL
- [ ] Viator live or explicitly deferred with date
- [ ] Operator runbook
- [ ] MVP metrics sheet started
- [ ] Dossier + ADR references updated with actual URLs (no secrets in git)

## Handoff notes
- Prefer client-owned engine/OTA logins; Inteligente uses least-privilege if assisting
- Do not commit API keys, customer PII exports, or raw media binaries to the repo
- After MVP stability, reopen HC-022 automation scope only against the live engine (webhooks, review requests, lead triage)
