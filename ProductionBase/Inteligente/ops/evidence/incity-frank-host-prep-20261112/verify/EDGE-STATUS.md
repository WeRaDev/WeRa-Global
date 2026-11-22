# InCity edge status (cutover complete)

## Public
- https://www.invisiblecity.site/ → 200 `Home | INVISIBLECITY.SITE`
- https://invisiblecity.site/ → 200 (same content)
- /contactus, /tours-from-lisbon, /web/login?db=incity_site → 200
- Interim alias still works: https://invisiblecity.wera.global/

## Tunnel
- Name/ID: filantropia-frank-origin / `1264ee64-e380-40d2-991e-6b76dfe55960`
- Config: `/home/wera-admin/cloudflared-frank/config.yml`
- Container: `filantropia-cloudflared-frank` (unless-stopped, host network)
- Origin: `http://127.0.0.1:8073` with `httpHostHeader: www.invisiblecity.site`

## DNS (zone invisiblecity.site)
- Proxied CNAME `@` → `1264ee64-e380-40d2-991e-6b76dfe55960.cfargotunnel.com`
- Proxied CNAME `www` → same
- Old SaaS A records (13.248.243.5 / 76.223.105.230) removed
- Google site-verification TXT left intact

## Odoo
- `proxy_mode = True`
- `website.domain = https://www.invisiblecity.site`
- Stack: `/home/wera/incity-site`, DB `incity_site`

## Note
- Tunnel-login cert token lacked permission to PATCH SSL setting via API; if TLS oddities appear, set SSL/TLS mode to **Full** in the zone dashboard.
- `cloudflared tunnel login` on 2026-11-13 authorized zone `invisiblecity.site` into local `~/.cloudflared/cert.pem`.
