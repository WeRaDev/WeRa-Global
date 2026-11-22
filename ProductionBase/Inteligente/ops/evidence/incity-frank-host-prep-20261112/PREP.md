# InCity → Frank hosting prep

| Field | Value |
|-------|--------|
| Evidence ID | `incity-frank-host-prep-20261112` |
| Station | Frank TRL4 — `wera-ss-pt-sn-1` / `wera-ss-pt-sn-1.tailfb390c.ts.net` |
| Source dump | `Customers/Vasco Da Lama/invisiblecitysite.dump.zip` (local, not in git) |
| Phase-1 commercial scope | ADR 0004 — brochure + lead capture; no OTA/booking/payments required |
| Skills loaded | `odoo-trl4-restore-operations`, `odoo-e2e-automation-loop`, `odoo-admin-app-governance` |
| Status | **Option A confirmed** (2026-11-12) — isolated stack; restore still gated on `CONFIRM DESTRUCTIVE` |
| Topology decision | **Option A — isolated stack** `/data/incity-site`, DB `incity_site`, loopback port **8073** (if free) |

## 1. Dump inventory (verified)

| Item | Finding |
|------|---------|
| Archive size | ~193 MiB zip; ~256 MiB uncompressed listing total |
| Layout | Standard Odoo backup: `dump.sql` + `filestore/<ab>/<sha1>` (839 filestore objects) |
| PostgreSQL dump | pg_dump **16.15** |
| Odoo series | **saas~19.3.x** (`base` `saas~19.3.1.3`) |
| Edition markers | **`web_enterprise`**, `website_enterprise`, `mail_enterprise`, `digest_enterprise` installed |
| Notable apps | `website`, `website_appointment`, `appointment`, `ai`, themes `theme_bewise`, `theme_aviato` |
| Installed modules | **79** (see `dump-module-inventory.txt`) |
| Websites in dump | **1** — name `INVISIBLECITY.SITE`, `domain` null in dump |
| Company | `INVISIBLECITY.SITE` |
| Website pages | **11** `website_page` rows |
| Login (non-secret) | `saintvasco@googlemail.com` (plus public/portal/system) |
| Filestore root | `filestore/` at zip root (map to `/var/lib/odoo/filestore/<db_name>/` on restore) |

**Implication:** This is an **Odoo 19.3 SaaS/Enterprise-flavored** website dump. Frank’s multi-brand stack runs **community** image `filantropia-odoo:19.0` on DB `wera_sites`. Expect **enterprise module prune** and possible schema/unblock work (same class of issues as prior WeRa multi-site restore).

## 2. Frank runtime snapshot (2026-11-12 probe)

| Item | Value |
|------|--------|
| Reachable | Yes (Tailscale ping + SSH as `wera`) |
| Existing multi-site | `/data/wera-sites` — containers `wera-sites-odoo`, `wera-sites-db` |
| Publish | `127.0.0.1:8070→8069` |
| DB | `wera_sites` (do **not** overwrite) |
| Brands already live | WeRa, Fonseca, Inteligente, … (many `website` rows) |
| Tunnel | `filantropia-cloudflared-frank` → origin **8070** |
| Disk `/data` | ~60 GiB free (sufficient for this dump) |
| Safety | Filantropia/other stacks present; Nextcloud AIO also running |

## 3. Recommended hosting topology (decision required)

### Option A — **Isolated stack (recommended)**
New tree e.g. `/data/incity-site/` with own compose, DB `incity_site` (or `invisiblecity`), loopback port **8073** (or next free), own filestore, optional own tunnel hostname later.

| Pros | Cons |
|------|------|
| Client data isolation from WeRa/Fonseca/Inteligente | Extra compose/appliance entry |
| Safer enterprise prune experiments | Separate backup class |
| Matches “client website on Frank” product | Tunnel ingress rule needed for public DNS |

### Option B — Import as extra website into `wera_sites`
Restore/merge content into existing multi-site DB.

| Pros | Cons |
|------|------|
| One Odoo process | High risk of rewrite/chrome/menu cross-talk |
| Shared tunnel already on 8070 | Enterprise prune on shared DB |
| | Violates “never restore client dump over multi-brand live DB” spirit |

**Owner decision (2026-11-12):** **Option A confirmed.** Do not restore into `wera_sites` or `filantropia_public`.

### Locked isolated stack parameters
| Parameter | Value |
|-----------|--------|
| Data root | `/data/incity-site` |
| Compose | `/data/incity-site/compose/docker-compose.yml` |
| DB name | `incity_site` |
| HTTP publish | `127.0.0.1:8073→8069` (adjust if busy) |
| Image | `filantropia-odoo:19.0` (community; same family as wera-sites) |
| Filestore | `/data/incity-site/filestore` → container `/var/lib/odoo/filestore` |
| Work/dump | `/data/incity-site/work/` |
| Network | dedicated `incity-site-net` (not shared with wera-sites unless required) |

## 4. Execution gates (from restore skill)

1. **Repo sync** — pin branch/commit used for any scripts/docs (worktree `ironwood-spire` or main as chosen).
2. **Preflight** — copy dump to Frank staging path on `/data` (not `/tmp` only); verify disk; confirm port free; LUKS `/data` mounted.
3. **Apply (destructive — needs `CONFIRM DESTRUCTIVE`)** — create isolated compose; restore SQL into **new** DB; place filestore under that DB name; start community Odoo 19.
4. **Upgrade/unblock** — uninstall/block `web_enterprise` and other enterprise-only modules; fix `to upgrade` / missing addons; theme handling (`theme_bewise` / `theme_aviato` may need community theme packages or neutralize).
5. **Website restore playbook** — inventory pages/menus/header/footer/rewrites; wire dump homepage; single chrome; company active; public access.
6. **Verification** — Host-header `/` 200; contact CTAs; assets; admin login with explicit `db=`.
7. **Edge** — add Cloudflare tunnel hostname when domain ready; keep Odoo on loopback only.
8. **Evidence + handoff** — pack under this folder + SolarCity ops mirror; update InCity dossier with non-secret URL.

## 5. Phase-1 commercial alignment (ADR 0004)

| ADR 0004 requirement | Dump capability | Action |
|----------------------|-----------------|--------|
| Brochure site | Yes (`website` + pages) | Keep |
| Lead/contact | Likely forms/appointment remnants | Prefer simple contact/WhatsApp CTAs; appointment modules optional |
| No OTA/booking/payments required | Dump has `appointment` / `website_appointment` | May leave installed if community-bootable, or disable public booking routes to match contract |
| Social links YT/FB/IG | Content/config | Wire CTAs + checklist post-go-live |
| €300 / 3 mo free host | Ops | Track free-host end date at go-live |

## 6. Blockers / open decisions (owner)

1. ~~**Topology:** Option A~~ — **confirmed 2026-11-12**.
2. **Public hostname:** domain string + who registers DNS (client pays per proposal).
3. **Enterprise prune policy:** community-only boot vs obtain enterprise addons (default: community + prune).
4. **Destructive confirm** — reply `CONFIRM DESTRUCTIVE` before DB create/restore on Frank.
5. **Admin password reset** after restore (do not store dump passwords in git).
6. **Whether to strip AI/appointment** for scope fidelity and smaller attack surface.

## 7. Local staging checklist (before Frank apply)

- [ ] `rsync`/`scp` zip to Frank e.g. `/data/incity-site/work/invisiblecitysite.dump.zip` (as `wera`, with sudo for `/data` as needed)
- [ ] Extract to `work/extract/{dump.sql,filestore}`
- [ ] Draft compose mirroring `wera-sites` but new project name/ports/volumes
- [ ] Local dry-run optional on a laptop community Odoo 19 if available
- [ ] Document exact image tag (`filantropia-odoo:19.0` or newer pin)

## 8. Explicit non-actions this prep session

- No restore into existing DBs
- No tunnel DNS cutover
- No commit of dump binary or credentials
- No public exposure

## 9. Next command batch (after Option A + CONFIRM DESTRUCTIVE)

To be written as a single batched SSH script:

1. Create `/data/incity-site/{compose,filestore,work,addons,logs,secrets}`
2. Place conf with `db_name=incity_site`, loopback publish
3. `docker compose up -d` db+odoo
4. `psql` create role/db; restore `dump.sql`
5. Copy filestore into container volume path for `incity_site`
6. Prune enterprise modules via `odoo -d … --stop-after-init` / SQL state fixes per prior UPGRADE-STATUS lessons
7. Probe `http://127.0.0.1:<port>/web/login?db=incity_site`
8. Website fidelity phases
9. Evidence update

## References

- `ProductionBase/Inteligente/docs/adr/0004-incity-brochure-website-phase1.md`
- `ProductionBase/Inteligente/Resources/Documents/Proposals/InCity-website-proposal-v2.html`
- `ProductionBase/SolarCity/ops/evidence/frank-odoo-multiwebsite-20261016/`
- Skills: `~/.agents/skills/odoo-trl4-restore-operations`, `odoo-e2e-automation-loop`, `odoo-admin-app-governance`
