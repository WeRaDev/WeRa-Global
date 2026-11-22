# Content Matrix Studio — Operator guide

One-page runbook for Inteligente operators on InCity (`incity_site` / https://www.invisiblecity.site/).

Spec: `docs/incity-content-matrix-studio-spec.md` · Module: `inteligente_content_matrix` · Backlog: HC-024

## Who can do what

| Role | Group | Can |
|------|-------|-----|
| Operator | Content Matrix / Operator | Run sessions, accept/edit/reject, import/export |
| Manager | Content Matrix / Manager | Everything Operator can + skip sections + ACL |

Assign groups under **Settings → Users**. Admin is Manager by default after install.

## First-time setup (once per DB)

1. Install/upgrade module on Frank (`-i` / `-u inteligente_content_matrix`).
2. **Content Matrix → Import Matrix** → load `odoo_addons/inteligente_content_matrix/data/seeds/incity_matrix_v1.json`.
3. Confirm **Pages** show completion % and **Sections** kanban has pending cards.
4. Public site must stay unchanged until an explicit Apply step (P4).

## Run a review session

1. **Content Matrix → Review Sessions → New**
2. Pick website (`incity`). Optional: limit **Page scope** (e.g. Home only).
3. **Start** → read executive summary → **Proceed**.
4. Select a page → **Open page** → read analysis/guidelines → **Start sections**.
5. For each section walk the script:
   - **4.1 Fact** — exact live/import text (read-only) → **Next**
   - **4.2 Interpretation** — adjust if needed → **Next**
   - **4.3 Suggestion** — adjust if needed → **Next**
   - **Decide**
     - **Accept suggestion** → final = suggestion, status `approved`, version++
     - **Edit final** → edit text → **Save edited final** → status `updated`
     - **Reject interpretation** → **note required** → returns to 4.2
     - **Skip section** (Manager only) → status `skipped`
6. When the page is complete → **Finish session** or **Choose another page**.
7. Chatter posts a finish summary (Discuss notification to the operator).

Progress bar = sections closed (`approved` / `updated` / `skipped`) over sections in scope.

## Pause and resume

- **Later** at any active step → state `paused`; resume point stored.
- **Content Matrix → Paused Sessions** (or filter *Paused* / *My sessions*).
- **Resume** or **Start** restores the prior step. One active session per user + website.

## Import / export

- **Import Matrix**: JSON or CSV; upsert key = website_code + page_url + anchor_key + lang (idempotent).
- **Export Matrix**: filter by website/status; use approved/updated rows for apply checklist (P4).

## Discuss / chatter

- Session and section forms have chatter. Comment freely; do not treat chatter as the final text source of truth — finals live on the section.
- Finish posts a structured note (counts + next step). Pause/resume leave quiet notes on the session.

## Discuss Matrix Bot (auth operators)

Registered **internal** users with **Content Matrix / Operator** (or Manager) can drive a review session from Discuss. This is **not** public Live Chat (`im_livechat` is not required).

### Open the bot

1. Easiest: **Content Matrix → Matrix Bot (Discuss)** — opens a DM with the bot.
2. Or **Discuss** → start conversation → search **Content Matrix Bot** (internal user + bot `im_status`; partner-only is not enough for the picker).
3. Or open a review session → **Open Matrix Bot**.
4. **Recommended surface:** Website **Edit** mode. The floating Discuss panel appears while editing the site; bot deep-links stay in that session.

### Interaction model

1. Prefer **option buttons** under each bot reply (or reply with the number, e.g. `1`).
2. Free-text still needed only for: `edit …` and `reject …`.
3. Typed commands still work: `help`, `start [code]`, `next`/`proceed`, `pages`, `page …`, `sections`, `accept`, `edit …`, `reject …`, `skip` (Manager), `pause`/`resume`, `finish`, `preview`, `status`.
4. Typical flow: **Start review** → **Continue** → pick a page (labels show `N open` / `done`) → **Start sections** → combined section card → **Accept** / **edit** / **reject** → **Finish**.

### Combined section card

On section review the bot posts **one** message with:

- **4.1 Fact** (live/import text)
- **4.2 Interpretation**
- **4.3 Suggestion**
- Options: **Accept suggestion**, **Open in editor**, **Skip** (Manager), **Pause**; free-text `edit …` / `reject …`

Backend form sessions can still walk fact → interpret → suggest → decide step-by-step. The bot path jumps to a combined **decide** card for speed.

### Editor deep-links (not public preview)

- Links use **Website Edit** URLs: `path?enable_editor=1#dom_id` (relative, same window).
- Example Home bio: `/?enable_editor=1#home-bio`.
- Public fragment still works for spot-checks: `https://www.invisiblecity.site/#home-bio`.
- Frontend JS (`matrix_bot_choices.js`) targets the **Website Edit iframe**, scrolls to `#dom_id`, and briefly highlights the block. Parent-only hash navigation is not enough while Discuss lives in the editor shell.
- Deep-link shows **published current** copy on the page, not unapplied matrix suggestions.

### Access and visibility notes

- Public / portal users cannot use the bot.
- If the bot is missing from the Discuss user picker after upgrade: confirm internal user `matrix_bot`, partner **Content Matrix Bot**, and `im_status=bot`, then upgrade module.
- The “widget” in Website Edit is Discuss, not Live Chat. Re-open via the editor Discuss control or the menu if the panel was closed.

### DOM map

Manager: **Import DOM anchor map** on the matrix website form (seed `data/seeds/incity_dom_anchor_map.json`) after live `id=` anchors exist. Map doc: `docs/incity-dom-anchor-map.md`. Ops inject scripts: `ops/scripts/inject_incity_*_dom_ids.py` (Frank; restart Odoo after `arch_db` writes).

## What not to do

- Do not skip logging a final when marking approved (Accept or Edit path does this).
- Do not rewrite live Website pages from the matrix until P4 verify/apply checklist.
- Do not enable LLM hooks (disabled by design in v1).
- Do not open public unauthenticated review routes (none exist).

## Smoke after deploy

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://www.invisiblecity.site/
curl -s -o /dev/null -w "%{http_code}\n" "https://www.invisiblecity.site/web/login?db=incity_site"
```

Expect `200` both. Login: admin email on Frank; password in host secrets (not in git).

## Verify (P4)

1. **Content Matrix → Verify Runs → New**
2. Website = `incity`. Optional page scope (e.g. Home only).
3. Compare mode: **Final, else current** (default).
4. **Run verify** — fetches `base_url + page.url`, builds a live corpus, classifies each section:
   - **OK** — expected final (or current) found (exact, multipart `/`·`|` splits, or token coverage)
   - **Drift** — final not live, but current still matches
   - **Missing on live** — neither final nor current found in corpus
   - **Orphan live** — page had no section matches
   - **Error** — fetch failed
   - **Meta** sections (`role=meta` / `.meta.` anchors) match against `<title>` + meta description tags, not only visible body
5. Review **Lines** + **Log**. Export/copy log for evidence pack.

Public site content is **not** changed by verify.

## Apply checklist (P4)

1. **Content Matrix → Apply Runs → New** (dry-run left ON).
2. **Build checklist (dry-run)** — lists every `approved`/`updated` section with `apply_method != none` and non-empty final.
3. Paste finals into Website Editor using the checklist (v1 does **not** auto-rewrite HTML).
4. Optional Manager path: uncheck dry-run, tick confirm, **Run apply** — marks lines done + version snapshot `apply` only (still no HTML rewrite).
5. Re-run **Verify** after paste; drift/missing for applied anchors should clear.

`APPLY_REGISTRY` may document per-anchor notes (e.g. `incity:home.footer.about`); auto `website_page_field` / `ir_ui_view_replace` stay blocked in v1.

## After a full Home cycle

1. Export approved matrix.
2. Verify public text vs finals; build manual apply checklist.
3. Only then paste/apply live copy; re-verify.
4. Design-partner willingness-to-pay conversation only after first completed cycle (P5).
5. Store verify log under Frank `ops/evidence/` when running the pilot host.
