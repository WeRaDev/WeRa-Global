# Preflight after Option A confirm (2026-11-12)

| Check | Result |
|-------|--------|
| Option A | Confirmed by owner |
| `/data/incity-site` | Does not exist yet (clean) |
| Port 8070 | In use (`wera-sites-odoo`) |
| Port 8073 | **Free** (planned) |
| Port 8080 | In use (Nextcloud AIO) |
| Disk `/data` | ~60 GiB free |
| Images | `filantropia-odoo:19.0`, `odoo:19.0` present |
| Existing multi-site | Untouched |

Still required before apply: `CONFIRM DESTRUCTIVE`, enterprise prune default OK, public hostname when known.
