# InCity partnership proposal v1 — internal appendix (Inteligente only)

**Not client-facing.** Companion to `InCity-partnership-proposal-v1.html`.  
**Last updated:** 2026-11-09

## Related files
- Client HTML: `Resources/Documents/Proposals/InCity-partnership-proposal-v1.html`
- Dossier: `KnowledgeBase/kb-customers/docs/clients/incity.md`
- ADR: `docs/adr/0003-incity-minimum-effort-booking-mvp.md`
- MVP plan: `tasks/incity-mvp-booking-website.md`
- Research: `Resources/Documents/Research/Clients/InCity/04-booking-stack-odoo-vs-bokun.md`

## Source inputs merged into the proposal
- Founder audio brief / structured project note (2026-11-09): Odoo site, Mr. Local structure, Viator-first, partnership pricing, referral, IP retention, HTML proposal request.
- Prior Inteligente work: InCity dossier, ADR 0003 (engine as inventory master), MVP task plan, booking-stack research (Odoo is not a native tour OTA channel manager).
- Client-facing hybrid: **Odoo shell + Bókun backend**, keeping ADR 0003 inventory-master rule.

## Decisions locked (commercial / delivery)
| Topic | Decision |
|---|---|
| Document purpose | Client HTML proposal; this file = internal notes |
| Launch architecture | Odoo website + Bókun-class engine; Nextcloud optional later |
| Odoo hosting | **Self-host on Frank** (TRL4) |
| Launch guarantee | Site + widget + Viator + central calendar; no own engine/agent promise |
| Price | **€500 setup + €50/mo** |
| What €50 covers re suppliers | **Bókun (engine) subscription fee** among third-party platform subs; OTA commissions excluded |
| Setup copy | **Basic copywriting included** (not full brand studio / unlimited revisions) |
| Domain | **Client pays** for domain registration/DNS; client owns domain |
| Referral | Free own subscription **credit** after **5** active referred subscribers |
| IP | Provider product IP; client brand/content/domain-if-paid/data export |
| Languages in HTML | EN + PT |
| Catalogue | 3–5 packages; Mr. Local-inspired IA |
| Payments | Instant book+pay direct; OTA per channel |

## Unit economics (A3)
- Subscription set to **€50/mo** specifically to cover expected Bókun-class platform cost (~€50 / ~$49 band from brief and public plans).
- Still verify live Bókun quote (plan tier, booking %, Viator fee treatment). If engine cost exceeds €50/mo all-in, either raise sub, absorb loss intentionally, or change plan tier.
- OTA commissions (~20–30%) stay on the operator side of economics.
- Payment processor fees: excluded from sub unless later agreed; confirm Stripe/etc. account ownership with client.
- Path to better COGS: own engine/agent later may cut Bókun spend; client price does not auto-change without written agreement.

## Provider-resolved (no longer “open” internally)
- Domain payer/owner: **client**
- Odoo target: **Frank self-host**
- Setup includes: **basic copywriting**

## Still for the client to answer (also listed in HTML §10 / §PT-10)
- Exact 3–5 public packages, EUR prices, durations, pickup/meeting points
- Max pax / vehicle capacity and blackout / unavailable days pattern
- Preferred domain name string
- Photos with usage rights; guide bio facts to approve
- Payment account for direct checkout (provider)
- Viator supplier status / existing listings under other brands
- Languages required at launch beyond EN
- How offline/WhatsApp bookings should be handled day-to-day
- Confirmation of subscription start date and billing method
- Any must-have OTA beyond Viator at launch (default: Viator only)

## ADR 0003 relationship
ADR 0003 rejected Odoo-as-channel-manager and put the engine as inventory master. The proposal **keeps that rule** while using Odoo as brand CMS on Frank. Fallback under delivery pressure: engine-native site only (ADR path E) without splitting inventory truth.

## Support / SLA (not yet fixed — keep internal until defined)
- Define “maintenance” hours/month and response expectations before long-term ops.
- Frank ops: backups, updates, TLS/edge exposure policy remain Inteligente/WeRa infra responsibility unless contracted otherwise.

## Version history
- 2026-11-09: Extracted from HTML internal appendix; €50 sub; Frank host; client domain; basic copywriting; client Qs moved to HTML.
