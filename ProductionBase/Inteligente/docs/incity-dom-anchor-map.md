# InCity DOM anchor map (matrix ↔ live blocks)

**Website:** Invisible City Tours (`incity`)  
**Base URL:** `https://www.invisiblecity.site`  
**Purpose:** Dual-key map for session/Discuss deep-links while keeping matrix `anchor_key` as inventory identity.  
**Sources:** `incity_matrix_v1.json`, `incity_matrix_v2_extra_pages.json`, Home/Contact HTML evidence (2026-11-12).  
**Status:** Live DOM ids applied on Frank `incity_site` (2026-11-22). Public verified on `https://www.invisiblecity.site/`. Matrix field `copywriting.section.dom_id` + **Import DOM anchor map** ship in `inteligente_content_matrix` ≥ 19.0.1.7.x.

## Conventions

| Rule | Value |
|------|--------|
| DOM id charset | `[a-z0-9-]` only (no dots) |
| Prefix | optional `mx-` omitted here for shorter URLs; add if collisions appear |
| Uniqueness | unique **per page** (footer ids are global shared) |
| Placement | prefer `id` on wrapping **structure `<section>`** (or column wrapper), not on raw text nodes |
| Many matrix rows → one block | **allowed and expected** |
| Meta rows | `dom_id` empty; preview = page URL only; `preview_mode=none` or `page` |
| Missing live block | `dom_id` still defined as **target id to create** in Website Builder |
| Public preview URL | `{base_url}{url}` or `{base_url}{url}#{dom_id}` |
| Editor deep-link (bot default) | `{url}?enable_editor=1` or `{url}?enable_editor=1#{dom_id}` (relative; same window) |
| Global chrome | Footer keys live on Home matrix rows but apply site-wide; same `dom_id` on every page footer |

**How to apply in Website Builder**

1. Edit page → select block → Style → create/edit anchor → set exact `dom_id` from this doc → Save.  
2. Import the same values onto `copywriting.section.dom_id` via **Import DOM anchor map** (JSON companion).  
3. Bot / session link: editor mode by default; if `dom_id` set → fragment; else page-only.

**Machine-readable companion:** `odoo_addons/inteligente_content_matrix/data/seeds/incity_dom_anchor_map.json`

---

## Inventory summary

| Page URL | Matrix sections | DOM blocks (excl. meta) | Notes |
|----------|-----------------|-------------------------|--------|
| `/` | 19 | 12 page + 4 global footer | Home has densest block structure |
| `/contactus` | 7 | 4 | Form + trust + help |
| `/privacy` | 3 | 1 | Single content block |
| `/tours-from-lisbon` | 13 | 6 | Intro + 3 packages + CTA/custom |
| `/tours-from-sintra` | 11 | 6 | Intro + 4 product clusters + CTA |
| `/intv` | 5 | 2 | Hero + CTA row |
| `/reviews` | 5 | 3 | Hero + proof + sources |
| `/vasco-da-lama` | 6 | 3 | Hero/bio + Goodfoot + CTA |
| **Total** | **69** | | 8 public matrix routes |

Meta-only keys (no fragment): 8 (`*.meta.description` × 8 pages).

---

## Global footer (all pages)

Present in public layout (`#footer` / `#bottom`). Matrix rows currently seeded under **Home** only; `dom_id` is site-wide.

| dom_id | Builder target | Matrix `anchor_key` | Role | Preview URL example |
|--------|----------------|---------------------|------|---------------------|
| `global-footer-about` | Footer about / company blurb column | `global.footer.about` | footer | `https://www.invisiblecity.site/#global-footer-about` (or any page + same hash) |
| `global-footer-whatsapp` | Footer WhatsApp link/label | `global.footer.whatsapp` | cta | `…#global-footer-whatsapp` |
| `global-footer-follow` | Footer social heading | `global.footer.follow` | nav | `…#global-footer-follow` |
| `global-footer-odoo` | Odoo free-website chrome (remove) | `global.footer.odoo_chrome` | footer | `…#global-footer-odoo` |

If the whole footer is one section, you may set a single parent id `global-footer` on `#footer` and still keep the four logical ids on inner columns when possible. Minimum viable: **`global-footer`** on the footer structure for all four keys (shared scroll target).

**Minimum viable shared target (if inner ids are hard):**

| dom_id | anchor_keys sharing it |
|--------|------------------------|
| `global-footer` | `global.footer.about`, `global.footer.whatsapp`, `global.footer.follow`, `global.footer.odoo_chrome` |

---

## `/` — Home

Live structure (evidence): striped hero → title/masters → color tour cards → hexagonal Goodfoot → punchy image → masonry Vasco/reviews → regenerative packs → more masonry → quadrant CTA → popup promo → footer.

| # | dom_id | Live block (approx.) | Matrix `anchor_key`(s) | Notes |
|---|--------|----------------------|------------------------|-------|
| — | *(none)* | `<head>` meta | `home.meta.description` | page-only preview |
| 1 | `home-hero` | `s_striped_center_top` hero | `home.hero.h1`, `home.hero.subhead`, `home.hero.cta`, `home.hero.body` | Primary above-fold |
| 2 | `home-claim` | same hero cluster or next text block holding craft claim | `home.hero.claim`, `home.hero.claim_dup` | Dup is delete-candidate; same scroll OK |
| 3 | `home-masters` | `s_title` “ENTERTAINED BY MASTERS…” | `home.block.masters_h2` | |
| 4 | `home-tours-lisbon` | Left card `s_color_blocks_2` | *(no dedicated matrix row yet; commercial CTAs live in mashed row)* | Optional nav aid; link from `home.cta_row` if needed |
| 5 | `home-tours-sintra` | Right card `s_color_blocks_2` | *(optional; same)* | |
| 6 | `home-tours` | Whole `s_color_blocks_2` section | `home.cta_row` | Prefer **one** section id if cards lack own matrix keys |
| 7 | `home-goodfoot` | `s_image_hexagonal` Goodfoot | `home.goodfoot.h2_follow`, `home.goodfoot.body` | |
| 8 | `home-harmony` | `s_image_punchy` symbiotic | *(no matrix row yet)* | Optional; create matrix row later or skip id |
| 9 | `home-bio` | Masonry Vasco / reviews cards + Who is he / Check it | `home.bio_ctas` | |
| 10 | `home-regenerative` | Masonry regenerative / leave park / gourmet | `home.goodfoot.h2_leave`, `home.gourmet` | |
| 11 | `home-experiences` | Later masonry (Espeta, Capuchos, …) | *(optional future keys)* | Not in current matrix |
| 12 | `home-book-band` | `s_quadrant` “TOUR SINTRA WITH US” | *(optional; CTA band)* | |
| 13 | `home-promo-popup` | `s_popup` buy-pack / R$ promo | `home.promo.br` | Popup may need id on popup root (already has generated id — **replace** with stable `home-promo-popup`) |
| F | see Global footer | footer | `global.footer.*` | |

### Home — section → dom_id (authoritative for import)

| anchor_key | dom_id | preview_mode |
|------------|--------|--------------|
| `home.meta.description` | | `page` |
| `home.hero.h1` | `home-hero` | `fragment` |
| `home.hero.subhead` | `home-hero` | `fragment` |
| `home.hero.cta` | `home-hero` | `fragment` |
| `home.hero.body` | `home-hero` | `fragment` |
| `home.hero.claim` | `home-claim` | `fragment` |
| `home.hero.claim_dup` | `home-claim` | `fragment` |
| `home.block.masters_h2` | `home-masters` | `fragment` |
| `home.goodfoot.h2_follow` | `home-goodfoot` | `fragment` |
| `home.goodfoot.body` | `home-goodfoot` | `fragment` |
| `home.goodfoot.h2_leave` | `home-regenerative` | `fragment` |
| `home.gourmet` | `home-regenerative` | `fragment` |
| `home.cta_row` | `home-tours` | `fragment` |
| `home.promo.br` | `home-promo-popup` | `fragment` |
| `home.bio_ctas` | `home-bio` | `fragment` |
| `global.footer.about` | `global-footer` | `fragment` |
| `global.footer.whatsapp` | `global-footer` | `fragment` |
| `global.footer.follow` | `global-footer` | `fragment` |
| `global.footer.odoo_chrome` | `global-footer` | `fragment` |

**Example session links**

- Bot / Website Edit (preferred): `/?enable_editor=1#home-hero`  
- Public spot-check: `https://www.invisiblecity.site/#home-hero`  
- Promo: `/?enable_editor=1#home-promo-popup` · Footer: `/?enable_editor=1#global-footer`

---

## `/contactus` — Contact

| anchor_key | dom_id | preview_mode | Builder target |
|------------|--------|--------------|----------------|
| `contact.meta.description` | | `page` | meta only |
| `contact.h1` | `contact-hero` | `fragment` | Top title block |
| `contact.intro` | `contact-hero` | `fragment` | Same intro band |
| `contact.form.cta` | `contact-form` | `fragment` | Form section / submit |
| `contact.trust.h2` | `contact-trust` | `fragment` | “100.000 tourists…” band |
| `contact.help` | `contact-help` | `fragment` | Help + videos intro |
| `contact.topics` | `contact-help` | `fragment` | Topic list in same block |

Also attach **global footer** ids on this page’s footer instance (same ids as Home).

**Example:** `https://www.invisiblecity.site/contactus#contact-form`

---

## `/privacy` — Privacy

| anchor_key | dom_id | preview_mode | Builder target |
|------------|--------|--------------|----------------|
| `privacy.meta.description` | | `page` | meta only |
| `privacy.h1` | `privacy-body` | `fragment` | Main policy section |
| `privacy.body` | `privacy-body` | `fragment` | Same section (body may be empty today) |

**Example:** `https://www.invisiblecity.site/privacy#privacy-body`

---

## `/tours-from-lisbon` — Tours from Lisbon

Live page not in local HTML evidence; blocks are **logical commercial structure** to create/align in builder.

| anchor_key | dom_id | preview_mode | Builder target |
|------------|--------|--------------|----------------|
| `lisbon.meta.description` | | `page` | meta |
| `lisbon.h1` | `lisbon-hero` | `fragment` | Page hero |
| `lisbon.intro` | `lisbon-hero` | `fragment` | Intro under H1 |
| `lisbon.classic.name` | `lisbon-classic` | `fragment` | Classic package card/section |
| `lisbon.classic.duration` | `lisbon-classic` | `fragment` | |
| `lisbon.classic.price` | `lisbon-classic` | `fragment` | |
| `lisbon.classic.stops` | `lisbon-classic` | `fragment` | |
| `lisbon.grand.name` | `lisbon-grand` | `fragment` | Grand Tour card |
| `lisbon.grand.price` | `lisbon-grand` | `fragment` | |
| `lisbon.short.name` | `lisbon-short` | `fragment` | Short package card |
| `lisbon.short.price` | `lisbon-short` | `fragment` | |
| `lisbon.cta` | `lisbon-cta` | `fragment` | Primary CTA band |
| `lisbon.custom` | `lisbon-cta` | `fragment` | Custom request near CTA |

**Example:** `https://www.invisiblecity.site/tours-from-lisbon#lisbon-classic`

---

## `/tours-from-sintra` — Tours from Sintra

| anchor_key | dom_id | preview_mode | Builder target |
|------------|--------|--------------|----------------|
| `sintra.meta.description` | | `page` | meta |
| `sintra.h1` | `sintra-hero` | `fragment` | Hero |
| `sintra.intro` | `sintra-hero` | `fragment` | |
| `sintra.b1.name` | `sintra-short` | `fragment` | ~3h panoramic + National |
| `sintra.b1.price` | `sintra-short` | `fragment` | |
| `sintra.palace.name` | `sintra-palace` | `fragment` | Palace specials family |
| `sintra.palace.price` | `sintra-palace` | `fragment` | |
| `sintra.b5.name` | `sintra-panoramic` | `fragment` | Park & coast circuit |
| `sintra.b5.price` | `sintra-panoramic` | `fragment` | |
| `sintra.goodfoot` | `sintra-goodfoot` | `fragment` | Goodfoot from Sintra |
| `sintra.cta` | `sintra-cta` | `fragment` | Contact CTA |

**Example:** `https://www.invisiblecity.site/tours-from-sintra#sintra-palace`

---

## `/intv` — INTV / videos

| anchor_key | dom_id | preview_mode | Builder target |
|------------|--------|--------------|----------------|
| `intv.meta.description` | | `page` | meta |
| `intv.h1` | `intv-hero` | `fragment` | Title + intro |
| `intv.intro` | `intv-hero` | `fragment` | |
| `intv.cta_tours` | `intv-cta` | `fragment` | CTA row |
| `intv.cta_contact` | `intv-cta` | `fragment` | |

**Example:** `https://www.invisiblecity.site/intv#intv-cta`

---

## `/reviews` — Reviews

| anchor_key | dom_id | preview_mode | Builder target |
|------------|--------|--------------|----------------|
| `reviews.meta.description` | | `page` | meta |
| `reviews.h1` | `reviews-hero` | `fragment` | Title + intro |
| `reviews.intro` | `reviews-hero` | `fragment` | |
| `reviews.cta` | `reviews-cta` | `fragment` | After-proof CTA |
| `reviews.source_note` | `reviews-sources` | `fragment` | Facebook/Google note (or embed band) |

If quotes are only embeds with no discrete matrix rows, one extra optional id `reviews-wall` can mark the embed wall (no matrix key yet).

**Example:** `https://www.invisiblecity.site/reviews#reviews-hero`

---

## `/vasco-da-lama` — Vasco / Goodfoot

| anchor_key | dom_id | preview_mode | Builder target |
|------------|--------|--------------|----------------|
| `vasco.meta.description` | | `page` | meta |
| `vasco.h1` | `vasco-hero` | `fragment` | Name + subhead + bio |
| `vasco.subhead` | `vasco-hero` | `fragment` | |
| `vasco.bio` | `vasco-hero` | `fragment` | |
| `vasco.goodfoot` | `vasco-goodfoot` | `fragment` | Goodfoot explanation block |
| `vasco.cta` | `vasco-cta` | `fragment` | Tours CTA |

**Example:** `https://www.invisiblecity.site/vasco-da-lama#vasco-goodfoot`

---

## Unique DOM id registry (checklist)

Use this list when setting anchors in the builder (must not collide **on the same page**; global footer ids repeat across pages by design).

### Per-page ids

```text
home-hero
home-claim
home-masters
home-tours
home-goodfoot
home-regenerative
home-bio
home-promo-popup
# optional home: home-harmony home-experiences home-book-band home-tours-lisbon home-tours-sintra

contact-hero
contact-form
contact-trust
contact-help

privacy-body

lisbon-hero
lisbon-classic
lisbon-grand
lisbon-short
lisbon-cta

sintra-hero
sintra-short
sintra-palace
sintra-panoramic
sintra-goodfoot
sintra-cta

intv-hero
intv-cta

reviews-hero
reviews-cta
reviews-sources

vasco-hero
vasco-goodfoot
vasco-cta
```

### Global (every page footer)

```text
global-footer
```

---

## Builder pass order (ops)

1. Home — set all Home + `global-footer` ids; hard-refresh; spot-check `#home-hero`, `#global-footer`.  
2. Contact, Privacy.  
3. Lisbon, Sintra (commercial).  
4. INTV, Reviews, Vasco.  
5. Import `dom_id` into matrix (when field exists) from companion JSON.  
6. Optional verify soft-check: each non-meta `dom_id` appears in fetched HTML.

---

## Gaps / follow-ups

| Gap | Action |
|-----|--------|
| Home matrix vs live drift | Some live bands (`home-harmony`, experiences masonry) lack matrix rows — ids optional until inventory expands |
| `home.cta_row` is mashed labels | Maps to whole `#home-tours`; after rewrite, may split to column ids |
| Lisbon/Sintra/INTV/Reviews/Vasco HTML not in local evidence | Confirm block boundaries on live edit; adjust map if one section holds two packages |
| Popup id | Replace generated `sPopup…` with `home-promo-popup` |
| Nested footer columns | Start with single `global-footer`; refine to four ids if needed |
| Module field | Shipped: `dom_id`, import map, `get_preview_url(editor=True)` |
| Editor iframe scroll | Bot links need Discuss JS to scroll builder iframe (parent hash alone misses the block) |

---

## Document control

| Version | Date | Notes |
|---------|------|-------|
| 0.1 | 2026-11-22 | Full 8-page dual-key map from matrix seeds + Home/Contact structure |
| 0.2 | 2026-11-22 | Live ids on all 8 routes + `global-footer`; Odoo restart required after arch write; scripts under `ops/scripts/inject_incity_*_dom_ids.py` |
| 0.3 | 2026-11-22 | Editor deep-links + matrix `dom_id` import; bot UX documented |

## Live application notes (0.2)

| Item | Detail |
|------|--------|
| Home | All map blocks + optional `home-harmony`, `home-experiences`, `home-book-band` |
| `home-claim` | **Not a separate live block** — use `#home-hero` (or `#home-masters`) until claim is split |
| `lisbon-cta` / `lisbon.custom` | **No separate CTA snippet** — use `#lisbon-hero` until a CTA band exists |
| Footer | `id="global-footer"` on first section inside `#footer` (keeps `#footer` on parent) |
| Cache | `arch_db` write alone may not show until **odoo container restart** (QWeb cache) |
| Ops scripts | `ops/scripts/inject_incity_home_dom_ids.py`, `ops/scripts/inject_incity_rest_dom_ids.py` |
