# InCity Frank restore status (20261112T202516Z)

## Goal
Isolated community Odoo 19 stack serving Invisible City Tours dump with dump-like website content.

## Runtime
- Host path: `/home/wera/incity-site`
- Containers: `incity-site-db` (postgres:16), `incity-site-odoo` (filantropia-odoo:19.0)
- Bind: `127.0.0.1:8073->8069`
- DB: `incity_site`
- Volumes: `incity_site_pg`, `incity_site_odoo_data` (filestore under filestore/incity_site)

## HTTP checks (local on Frank)
See fidelity.json in this directory. Expected:
- `/`, `/contactus`, `/tours-from-lisbon`, `/intv`, `/reviews`, `/web/login?db=incity_site` -> 200
- Unpublished `/tours-from-sintra`, `/vasco-da-lama` -> 404 (matches publish flags)

## Compatibility work applied
1. Enterprise/missing modules force-uninstalled; schema columns synced from community ref DB.
2. Themes installed: `theme_common`, `theme_aviato` (assets required by dump).
3. Shim addon `incity_community_shim`:
   - `Website._is_tracking_enabled(*args)` stub
   - `website.page.parent_id` / `parent_ids` for SaaS layout breadcrumbs
   - `ir.http._get_visitor_from_request` bridge to `website.visitor`
   - lang default hardening if LangData dummy/bool code appears
4. Removed broken `_get_cached` override (it returned recordsets and broke default_lang -> frontend_lang cookie TypeError).

## Non-goals / remaining
- No public tunnel/DNS yet (loopback only).
- Admin password was reset during restore; secrets live under `/home/wera/incity-site/secrets/` and odoo.conf (mode restricted) — do not commit.
- Some SaaS/enterprise features remain uninstalled; brochure pages are the deliverable.
- Optional: publish remaining draft pages, tighten CTAs, edge/domain when approved.

## Probe commands
```bash
curl -sI http://127.0.0.1:8073/
curl -sI 'http://127.0.0.1:8073/web/login?db=incity_site'
```
