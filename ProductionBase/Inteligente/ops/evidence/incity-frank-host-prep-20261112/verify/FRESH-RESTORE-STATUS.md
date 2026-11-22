# InCity fresh dump restore — 2026-11-14

## Source
- Local: Customers/Vasco Da Lama/invisiblecitysite.dump.zip (~218 MiB)
- Frank extract: /home/wera/incity-site/work/extract-fresh/
- Dump: Odoo saas~19.3+e, 75 installed modules, theme_aviato/bewise, login saintvasco@googlemail.com

## Target (isolated, not wera_sites)
- Stack: /home/wera/incity-site/compose
- DB: incity_site (293 tables after restore)
- HTTP: 127.0.0.1:8073 + Cloudflare tunnel invisiblecity.site
- Filestore: 242 MiB / 542 files under data_dir filestore/incity_site

## Compatibility applied
- Enterprise/missing modules forced uninstalled
- Schema sync from incity_ref (+ company_name etc.)
- theme_common + theme_aviato + incity_community_shim
- visibility '' + ir_ui_view shim for SaaS visibility=public 403
- Asset stubs for missing SaaS snippets
- Filestore chown odoo + data_dir=/var/lib/odoo
- proxy_mode=True; website.domain=https://www.invisiblecity.site

## Verify
- / /contactus /tours-from-lisbon /intv /reviews /privacy /web/login → 200
- CSS ~800KB clean; logo/images 200
- Public https://www.invisiblecity.site/ 200

## Admin
- URL: https://www.invisiblecity.site/web/login?db=incity_site
- Login: saintvasco@googlemail.com
- Password: /home/wera/incity-site/secrets/odoo_user_password (mode 600)
