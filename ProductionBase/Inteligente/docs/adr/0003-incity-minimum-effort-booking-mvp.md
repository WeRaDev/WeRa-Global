# ADR 0003: InCity Minimum-Effort Booking MVP Stack

## Status
**Superseded for phase-1 commercial delivery** by ADR 0004 (2026-11-09 brochure website on Frank).
Retained as **deferred optional path** if InCity later orders online booking / OTA integration.
Originally Accepted — 2026-10-19.

## Context
InCity (Invisible City Tours) is a solo private day-tour operator. Inteligente already delivered a paid Shrinking AI session that redirected priority from AI YouTube content to a **website booking path**. The client expressed unqualified interest in website-administration automation. Research into “Odoo website that works like Bókun and connects to Viator / Tripadvisor / GetYourGuide / Booking” shows:

1. Bókun-class systems are the industry default for tour inventory + OTA channel management.
2. Odoo is strong as CMS/CRM/accounting but **does not** natively provide certified tour OTA connectivity comparable to Bókun.
3. Odoo hotel channel-manager modules target lodging OTAs, not experience OTAs.
4. Custom Odoo↔OTA integration is disproportionate effort for a solo operator MVP.

InCity needs the **smallest stack that produces real bookings** without double-booking risk.

## Decision
1. **Inventory master for MVP = a tour booking engine with channel manager** (default candidate: **Bókun**; acceptable peers: Rezdy, FareHarbor, or equivalent certified Viator/GYG partner). Not Odoo.
2. **Minimum public surface:**
   - Engine-native website **or** a single-domain branded page set with an **embedded booking widget**
   - Simplified public catalogue: **3–5 packages** max (+ custom/WhatsApp path), not the full internal A1–B8 SKU list
   - Languages: **EN first**; add FR/PT/ES only if widget/site supports low-effort toggles
3. **Minimum distribution:**
   - **Direct widget/site** live with payments
   - **Viator** connected with real-time availability (Tripadvisor ecosystem path)
   - **GetYourGuide** as second OTA if onboarding time is short; otherwise immediately post-MVP
   - Tripadvisor business/listing hygiene (NAP, reviews) in parallel
   - **Defer** Booking.com Experiences and broad reseller marketplace sprawl
   - **Defer** Google Things to Do until engine support is confirmed and Viator path works
4. **Odoo role in MVP:** **out of critical path**. Optional later for CRM/invoicing sync or Inteligente admin automation. Do not block go-live on Odoo Website build, custom travel modules, or Odoo Online constraints.
5. **Explicit non-goals for MVP:** custom Odoo channel manager, full multi-OTA parity, AI content lab, regenerative Goodfoot ops automation, multi-currency enterprise packaging, Automation Center build without signed scope/DPA.
6. **Commercial/legal gate:** no live client-account configuration by Inteligente without written authorization and required privacy terms/DPA for guest data processors (engine + OTAs).

## Consequences
### Positive
- Fastest path to bookable direct + OTA demand
- One inventory truth reduces double-booking
- Aligns with competitor patterns (Mr. Local-class: engine + transparent packages)
- Keeps Inteligente scope coachable and billable in small increments

### Negative / risks
- Platform subscription + OTA commissions (often 20–30% on OTA sales)
- Tripadvisor-stack coupling if Bókun/Viator dominates volume
- Client must complete OTA supplier approvals (days–weeks), outside pure software control
- Brand site polish may lag if engine templates are used

### Follow-up actions
- Execute `tasks/incity-mvp-booking-website.md` and backlog **HC-023**
- Keep **HC-022** as commercial qualification (scope, budget, auth) before deep hands-on admin
- Update client dossier when engine choice is confirmed and go-live metrics exist
- Revisit Odoo only if there is a signed need for CRM/accounting consolidation or website-admin automation on a live stack

## References
- `Resources/Documents/Research/Clients/InCity/04-booking-stack-odoo-vs-bokun.md`
- `Resources/Documents/Research/Clients/InCity/03-competitive-and-website-strategy.md`
- `KnowledgeBase/kb-customers/docs/clients/incity.md`
- `tasks/incity-mvp-booking-website.md`
- `tasks/backlog.md` (HC-022, HC-023)
