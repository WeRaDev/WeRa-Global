# InCity (Invisible City Tours) — Frank ops package

Isolated community Odoo 19 stack for **InCity / Invisible City** on SolarSeed TRL4 host **Frank** (`wera-ss-pt-sn-1`).

## Live

- Public: https://www.invisiblecity.site (Cloudflare tunnel → `127.0.0.1:8073`)
- Host path: `/home/wera/incity-site`
- Compose project: `incity-site` (not multi-brand `wera_sites`)
- DB: `incity_site` (Postgres 16)
- Image: `filantropia-odoo:19.0`
- Community shim: `addons/incity_community_shim` (v19.0.1.0.2)

## This package (repo)

| Path | Contents |
|------|----------|
| `addons/incity_community_shim/` | SaaS→community compatibility module |
| `compose/docker-compose.yml` | Stack definition (**password via env**, not committed) |
| `evidence/complete-20261114T124904Z/` | Checksums, module/page inventory, redacted conf |

**Not in git (Frank only):** DB dumps, filestore, `/home/wera/incity-site/secrets/`, raw `odoo.conf`.

## Backup (Frank)

Full operational backup taken **2026-11-14T12:49:04Z**:

`/home/wera/incity-site/work/backups/complete-20261114T124904Z/`

- `db/incity_site_complete.dump` (pg_dump `-Fc`)
- `addons/`, `compose/`, `html/` page snapshots
- SHA256 in `evidence/.../checksums.txt`

## Delivery snapshot (2026-11-14)

- SaaS dump restored on community Odoo 19 with shim (views visibility, snippet groups, settings/mail stubs, `res.session` / `discuss.category` stubs, offline template fix).
- Admin user: `admin@invisiblecity.site` (password only under Frank `secrets/`).
- WhatsApp CTAs: GOODFOOT, Lisbon/Sintra tour **BOOK NOW** buttons, Reviews **BOOK NOW** → `wa.me/351967761674?text=...` (tour-specific prefill).
- `/tours-from-sintra` still **unpublished** in DB (content present).

## Secrets

Set on host only, e.g.:

```bash
export INCITY_PG_PASSWORD='...'   # from Frank secrets/pg_password
```

Never commit passwords, admin_passwd, or dump binaries.
