# InCity website proposal v2 — internal notes (Inteligente only)

**Not client-facing.** Companion to `InCity-website-proposal-v2.html`.  
**Last updated:** 2026-11-09

## Related files
- Client HTML (current): `Resources/Documents/Proposals/InCity-website-proposal-v2.html`
- Superseded draft: `Resources/Documents/Proposals/InCity-partnership-proposal-v1.html` (+ `-internal.md`)
- Dossier: `KnowledgeBase/kb-customers/docs/clients/incity.md`
- ADR: `docs/adr/0004-incity-brochure-website-phase1.md` (supersedes booking MVP for phase 1)
- Prior booking ADR (historical): `docs/adr/0003-incity-minimum-effort-booking-mvp.md`

## Client conversation outcome (2026-11-09)
Agreed expected deliverable:

| Item | Decision |
|---|---|
| Deliverable | Website hosted on **Frank**, available online |
| Online booking | **No** |
| Payment channels | **No** |
| Tourism platform integrations (Viator, etc.) | **No** |
| Social | YouTube, Facebook, Instagram **links → website** for lead capture |
| Scheduling | **Manual** by the guide; site supports **communication** |
| Price | **€300** one-time |
| Subscription | **None** |
| Hosting | **Free for 3 months** from go-live |

## Implications vs v1
- Bókun / OTA / payments / referral programme / €500+€50 model **out of phase 1**.
- ADR 0003 remains useful research for a **later** booking phase; not the current commercial commitment.
- HC-023 should track brochure site delivery, not booking MVP.

## Delivery notes
- Prefer Odoo Website on Frank for consistency with Inteligente ops; if timeboxed delivery is at risk, a simpler static/CMS stack on Frank is acceptable if acceptance criteria (live URL, pages, contact CTAs, social link checklist) still pass—document actual stack at handover.
- “Social integration” = link hygiene + stable landing URLs, not Meta/Google APIs.
- After 3 months free hosting: define paid hosting/care or migrate off Frank before promising indefinite free ops.

## Still needed from client
See HTML §8: domain, tours list, contacts, social URLs, photos/bio, languages.

## Version history
- 2026-11-09: v2 created from post-conversation simplified scope.
