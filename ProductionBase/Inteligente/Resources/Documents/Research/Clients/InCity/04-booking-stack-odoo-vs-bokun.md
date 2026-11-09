# InCity — Booking stack findings (Odoo vs Bókun-class engines)

**Status:** research synthesis for Inteligente internal use  
**Client:** InCity / Invisible City Tours  
**Date packaged:** 2026-10-19  
**Related ADR:** `docs/adr/0003-incity-minimum-effort-booking-mvp.md`  
**Related plan:** `tasks/incity-mvp-booking-website.md`

## Problem framed
InCity needs a bookable digital funnel (not more AI YouTube content). The desired behaviour is “like [Bókun](https://www.bokun.io/)”: direct website booking plus live distribution to Viator, GetYourGuide, Tripadvisor Experiences surfaces, and ideally Booking.com Experiences — without double-booking.

## What Bókun-class systems provide
A tour/activity **reservation system + channel manager**:

- One inventory calendar (capacity, closeouts, cancellations)
- Direct sales via website builder and/or embeddable booking widget
- Certified connections to major experience OTAs and resellers
- Real-time availability sync across channels
- Confirmations, mobile tickets, payments, basic ops tooling

Public Bókun positioning (2024–2026 product pages): Marketplace with thousands of resellers / dozens of global OTAs; strong Viator path (Tripadvisor group); GetYourGuide premium-style connectivity; optional Channel Manager API if another system remains CRS. Paid plans commonly start around **$49/mo + ~1–1.5%** on applicable bookings; **0% Bókun fee on Viator** is a frequent paid-plan claim (OTA commission still applies).

Peers with similar role: Rezdy, FareHarbor, Peek Pro, Ventrata, TrekkSoft, Zaui, and others. Operators connect to OTAs **through these certified partners**, not by coding OTA APIs themselves.

## Channel map (operator language)
| Surface | Role | Notes |
|---|---|---|
| Own website / widget | Direct bookings | Highest margin; needs instant confirm + payments |
| Viator | Primary bookable OTA in Tripadvisor stack | Often first OTA; commission typically ~20–30% |
| Tripadvisor | Discovery + reviews; Experiences often via Viator connectivity | Fix geo/NAP; harvest reviews off Facebook-only |
| GetYourGuide | Major EU-leaning OTA | Usually requires connected booking system |
| Booking.com Experiences | Hotel-stack discovery/book path | Often via intermediary networks; not day-one MVP |
| Google Things to Do | High-intent discovery; often 0% Google fee | Still needs certified booking connectivity |

## What Odoo can and cannot do
### Odoo strengths for InCity
- Branded multi-language **Website** / CMS
- CRM, invoicing, contacts, portal
- Familiar stack for Inteligente (Odoo Online already used elsewhere in Automation Center context)
- Optional third-party “travel agency / tour package / appointment booking” modules for catalogue + enquiry flows

### Odoo gaps vs Bókun-like OTA distribution
- No native certified **Viator / GetYourGuide / Tripadvisor Experiences** tour channel manager
- Odoo Apps “channel manager” offerings are predominantly **hotel PMS** (Booking.com, Expedia, Airbnb rooms via WuBook/QloApps-class connectors) — wrong product shape for private day tours
- Third-party Odoo travel modules (e.g. SerpentCS tour agency, ECOSIRE travel suite) focus on packages, CRM, website enquiry/booking storefronts; **OTA channel managers are roadmap/custom add-ons**, not drop-in Bókun replacements
- Odoo Online (SaaS) blocks most third-party custom modules — relevant if someone assumed “just install a tour app on Odoo Online”
- Building custom Odoo ↔ OTA APIs is a multi-week engineering project and fights OTA partner programs that prefer few certified connectors

**Conclusion:** Odoo alone cannot truthfully “work like Bókun” for multi-OTA tour inventory. Odoo can host brand content and back office; a tour booking engine must own inventory if OTAs are required.

## Architecture options evaluated
| Option | Description | Effort | OTA fit | Verdict for min MVP |
|---|---|---|---|---|
| A | Bókun-class engine as inventory master + optional branded site/widget | Low–medium | High | **Preferred** |
| B | Odoo Website shell + embedded engine widget | Medium | High (via engine) | Good if Odoo brand required |
| C | Odoo-only website + forms/modules, manual OTA calendars | Medium | Poor / manual | Reject if OTAs are in scope |
| D | Odoo as CRS + Bókun Channel Manager API | High | High | Defer (overkill for solo) |
| E | Engine-only (Bókun site builder), no Odoo | Lowest | High | **Best absolute minimum** |

## Cost shape (order of magnitude)
- Engine subscription: often ~$0–$149+/mo class + possible platform % on some bookings
- OTA commission: typically **~20–30%** of OTA gross — dominates economics
- Custom Odoo↔OTA build: usually unjustified for a solo operator
- Inteligente Automation Center work should not begin until stack, authorization, and DPA boundaries are explicit

## Implications for Inteligente delivery
- Client pain is **bookings + funnel**, not “install Odoo travel module”
- Website-admin automation (pipeline interest) is **phase-after-MVP**, once a live booking system exists
- Do not promise ROI from discovery; do not access live accounts without signed auth + DPA
- MVP success = live direct book path + at least one live OTA with shared inventory, not a perfect multi-channel enterprise stack

## Sources (public product / industry pages used in synthesis)
- https://www.bokun.io/ and related Bókun Channel Manager / pricing / Viator / GetYourGuide partner pages
- Industry channel-manager explainers (Zaui, SambaHQ-style OTA connectivity guides; 2025–2026 market notes on OTA share of experiences)
- Odoo Apps / vendor pages for tour agency modules and hotel channel managers (SerpentCS, ECOSIRE, Webkul/QloApps, Agilorg WuBook) — used to confirm hotel vs tour gap

Treat vendor marketing claims (booking uplift %, exact fee tables) as **directional**; re-verify pricing and partner tiers at contract time.
