# inteligente_content_matrix

Odoo 19 Community module: **Content Matrix Studio** (Inteligente).

Spec: `docs/incity-content-matrix-studio-spec.md`  
Operator guide: `docs/content-matrix-operator-guide.md`  
DOM map: `docs/incity-dom-anchor-map.md`  
Backlog: HC-024

Phases shipped: **P0–P4** + **Discuss Matrix Bot** (auth operators, combined section cards, Website Edit deep-links + iframe scroll, `dom_id`)

Version: **19.0.1.7.2**

### Discuss Matrix Bot
- Internal user + partner **Content Matrix Bot** (`im_status=bot`) so Discuss can list the bot
- Operators only (`group_operator` / Manager); **not** public Live Chat
- Option chips under each reply (or reply with the option number); free text for `edit …` / `reject …`
- Commands: `help`, `start [code]`, `proceed`/`next`, `pages`, `page …`, `sections`, `accept`, `edit …`, `reject …`, `skip`, `pause`/`resume`, `finish`, `preview`, `status`
- Section review = **one card** with fact + interpretation + suggestion → Accept / Open in editor / edit / reject
- Deep-links: relative `path?enable_editor=1#dom_id` (same window, Website Edit). JS scrolls the **builder iframe** to the block
- Session form **Open Matrix Bot**; website form **Import DOM anchor map**
- Seeds: `data/seeds/incity_matrix_v1.json`, `incity_matrix_v2_extra_pages.json`, `incity_dom_anchor_map.json`

## Install on Frank (InCity pilot)

```bash
# From laptop (example)
rsync -a ProductionBase/Inteligente/odoo_addons/inteligente_content_matrix/ \
  wera@wera-ss-pt-sn-1.tailfb390c.ts.net:/home/wera/incity-site/addons/inteligente_content_matrix/

ssh wera@wera-ss-pt-sn-1.tailfb390c.ts.net
cd /home/wera/incity-site/compose
docker stop incity-site-odoo
docker run --rm --network incity-site_incity-site-net \
  -v incity_site_odoo_data:/var/lib/odoo \
  -v /home/wera/incity-site/addons:/mnt/extra-addons \
  -v /home/wera/incity-site/odoo.conf:/etc/odoo/odoo.conf:ro \
  filantropia-odoo:19.0 \
  odoo -c /etc/odoo/odoo.conf -d incity_site -i inteligente_content_matrix --stop-after-init
docker compose up -d
# restore filestore symlink if needed
docker exec -u root incity-site-odoo bash -c \
  'mkdir -p /var/lib/odoo/.local/share/Odoo; ln -sfn /var/lib/odoo/filestore /var/lib/odoo/.local/share/Odoo/filestore; chown -R odoo:odoo /var/lib/odoo/filestore'
```

Upgrade:

```bash
# same run with -u inteligente_content_matrix
```

## Seed import

1. Open **Content Matrix → Import Matrix**
2. Seeds:
   - `data/seeds/incity_matrix_v1.json` — Home + Contact + Privacy (original P1 pilot)
   - `data/seeds/incity_matrix_v2_extra_pages.json` — Tours from Lisbon/Sintra, INTV, Reviews, Vasco/Goodfoot (menu routes)
3. Import is upsert by `website_code + page_url + anchor_key + lang` (safe to re-run; Home finals not wiped if omitted from payload)
4. Or via shell:

```python
wiz = env['copywriting.matrix.import.wizard'].create({
    'import_format': 'json',
    'data_text': open('/mnt/extra-addons/inteligente_content_matrix/data/seeds/incity_matrix_v1.json').read(),
})
wiz.action_import()
```

## Smoke

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://www.invisiblecity.site/
curl -s -o /dev/null -w "%{http_code}\n" "https://www.invisiblecity.site/web/login?db=incity_site"
```
