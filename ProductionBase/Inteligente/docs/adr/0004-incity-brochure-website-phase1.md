# ADR 0004: InCity Brochure Website Phase 1 (Frank)

## Status
Accepted — 2026-11-09  
**Supersedes ADR 0003 for the current commercial phase** (booking/OTA MVP deferred, not discarded as future research).

## Context
After a brief client conversation, InCity’s expected deliverable was reduced from a bookable multi-channel stack to a simpler online presence:

- Website hosted on Frank and available online
- No tourism-platform integrations, no online bookings, no payment channels
- YouTube, Facebook, and Instagram used for lead capture via links to the website
- Guide schedules tours manually; website supports communication/contact
- Commercial terms: **€300** project fee, **no subscription**, **3 months free hosting**

ADR 0003 (Bókun-class engine + Viator, etc.) remains valid as a **later optional path** and research baseline, but it is not the phase-1 commitment.

## Decision
1. **Phase 1 deliverable** = brochure + lead-capture website on **Frank**, publicly reachable.
2. **In scope:** core marketing pages, tour presentation content, contact/lead CTAs, readiness for social profile links (YT/FB/IG), basic launch copywriting, 3 months free hosting from go-live.
3. **Out of scope for phase 1:** online booking engines, payment processors, Viator/GYG/Tripadvisor/Booking inventory sync, automatic scheduling, monthly subscription product.
4. **Scheduling authority** remains the human guide (manual).
5. **Commercial:** €300 one-time; no phase-1 subscription; hosting free for 3 months then renegotiate or stop.
6. Prefer Odoo Website on Frank when practical; substitute a lighter stack on Frank only if needed to meet acceptance without expanding scope.

## Consequences
### Positive
- Matches client ability/willingness to pay and current ops (manual scheduling)
- Fast path to a real public URL and social link targets
- Avoids OTA commission complexity and engine COGS in phase 1

### Negative / risks
- No automated anti-double-booking across OTAs (acceptable: OTAs not connected)
- Lead volume still depends on social traffic and manual response quality
- Free hosting window needs an explicit end/renewal conversation

### Follow-up actions
- Client proposal: `Resources/Documents/Proposals/InCity-website-proposal-v2.html`
- Update dossier and backlog HC-023 for brochure delivery
- Revisit ADR 0003 only if client later orders booking/OTA work

## References
- `Resources/Documents/Proposals/InCity-website-proposal-v2.html`
- `Resources/Documents/Proposals/InCity-website-proposal-v2-internal.md`
- `docs/adr/0003-incity-minimum-effort-booking-mvp.md` (deferred path)
- `KnowledgeBase/kb-customers/docs/clients/incity.md`
- `tasks/backlog.md` (HC-023)
