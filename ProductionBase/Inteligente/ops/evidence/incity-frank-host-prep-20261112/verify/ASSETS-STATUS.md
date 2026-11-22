# InCity assets restore (complete)

## Symptoms
- Red CSS fallback banner: "A css error occured, using an old style to render this page"
- Missing images (logo, page media) via /web/image/* HTTP 500

## Causes
1. Filestore mismatch: binaries at `/var/lib/odoo/filestore/incity_site` while runtime looked under `/var/lib/odoo/.local/share/Odoo/filestore/incity_site`.
2. SaaS dump CSS referenced snippet SCSS not present on community Odoo 19 image (s_bento_grid, s_appointments, etc.).

## Fixes applied
1. `data_dir = /var/lib/odoo` in odoo.conf
2. Symlink `~/.local/share/Odoo/filestore` -> `/var/lib/odoo/filestore`
3. Stub SCSS files for missing snippets (re-apply via `scripts/ensure-asset-stubs.sh` after container recreate)
4. Cleared and rebuilt `web.assets_frontend` bundle (~800 KiB)

## Verification (2026-11-13)
- CSS `/web/assets/1/a29fc80/web.assets_frontend.min.css` ~800487 bytes, no error banner
- logo 200 / 346651 bytes; sample media 200 / 14.5MB
- Public https://www.invisiblecity.site/ OK
