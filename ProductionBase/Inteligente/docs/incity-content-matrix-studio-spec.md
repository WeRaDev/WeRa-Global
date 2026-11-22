# Technical Specification: Content Matrix Studio

**Product name:** Content Matrix Studio (CMSW)  
**Odoo module technical name:** `inteligente_content_matrix`  
**Edition:** Odoo 19 Community  
**Primary pilot:** InCity / Invisible City Tours (`incity_site` on Frank)  
**Owner:** Inteligente (WeRa Global)  
**Status:** Implemented on Frank pilot (`incity_site`) — module `19.0.1.7.2` (P0–P4 + Discuss Matrix Bot)  
**Related:** copywriting analysis, redacted content matrix, operator guide, DOM anchor map

---

## 1. Purpose and goals

### 1.1 Problem
Website value is split into structure (Odoo/theme) and text (human + LLM readable). The pilot client needs ongoing copy improvement without a full-time copywriter. Ad-hoc ChatGPT pastes lack audit trail, section inventory, and safe apply/verify.

### 1.2 Goal
Deliver a **repeatable, deterministic content-review workflow** on Odoo CE that:

1. Stores a **content matrix** (every public text cell: page x section x version x status).
2. Runs a **guided review session** (fact → interpretation → suggestion → final).
3. Produces **exportable approved matrix** for website update and later translation.
4. Optionally **applies** approved rows and **verifies** live site vs matrix.

### 1.3 Non-goals (v1)
- Public website Live Chat bubble for this product.
- Native `im_livechat` chatbot as the primary state machine.
- LLM/agent autonomy, City of Light orchestration, self-writing scripts.
- Odoo Online-only API constraints (pilot is self-hosted).
- Multi-tenant SaaS packaging / App Store listing.
- Guaranteed Odoo SA revenue-share partnership.

### 1.4 Success metrics
| Metric | Target (pilot) |
|--------|----------------|
| Matrix coverage of public text | ≥ 95% of visible marketing copy rows have status `approved` or `updated` |
| Time per page session (Home) | ≤ 45 minutes operator-assisted |
| Client/operator approvals logged | 100% of changed sections have final + timestamp + actor |
| Verify script | 0 critical orphans (live text with no matrix row) on mapped pages |
| Reuse | Module installable on second CE DB without code fork |

### 1.5 Commercial framing
Client is a **design partner**. Fee for hosting + automation is validated **after** first full matrix cycle. Do not block MVP on subscription billing.

---

## 2. Users and access

| Actor | Odoo identity | Access |
|-------|---------------|--------|
| Operator (Inteligente) | Internal user, group `Content Matrix / Manager` | Full CRUD, sessions, export, apply, verify |
| Client reviewer (optional v1.1) | Portal user linked to partner, group `Content Matrix / Portal Reviewer` | Own sessions: accept/edit/reject; read matrix for their website |
| Public visitor | Public user | **No access** |
| Apply bot (optional) | Internal user `matrix_bot`, no interactive password, API key only | Apply/verify only |

**Groups**
- `inteligente_content_matrix.group_manager`
- `inteligente_content_matrix.group_operator` (run sessions, no ACL admin)
- `inteligente_content_matrix.group_portal_reviewer` (portal)

**Auth surfaces**
- Backend menus (v0–v1 primary).
- Portal route `/my/content-matrix` with `auth='user'` (v1.1).
- No public controller for review API without session auth.

---

## 3. System context

```text
┌─────────────────────────────────────────────────────────┐
│ Odoo 19 CE (incity_site)                                │
│  website + mail + portal                                │
│  incity_community_shim (compat)                         │
│  inteligente_content_matrix (this module)               │
└───────────────┬─────────────────────────┬───────────────┘
                │                         │
                ▼                         ▼
        Public site pages          Discuss notify
        (read/verify; apply)       (chatter + optional bus)
                │
                ▼
        Export CSV/JSON  →  translation / second tool
```

**Depends:** `base`, `mail`, `website`, `portal` (portal features optional via extra depends or soft code).  
**Conflicts:** none expected with `incity_community_shim`.  
**Deploy path (pilot):** `/home/wera/incity-site/addons/inteligente_content_matrix` + `-i` / `-u` on `incity_site`.

---

## 4. Functional requirements

### 4.1 Content matrix
- FR-M1: CRUD websites (logical site; default link to `website` record id=1).
- FR-M2: CRUD pages (`url`, `name`, `sequence`, `is_active`, publish flags).
- FR-M3: CRUD sections under page (`sequence`, `role`, `anchor_key`, current/suggestion/final text, status, version).
- FR-M4: Import matrix from CSV/JSON (seed from analysis artifacts).
- FR-M5: Export matrix filtered by website/lang/status.
- FR-M6: Version history on section text changes (simple: `copywriting.section.version` rows).
- FR-M7: Sitemap view = ordered pages + section counts + completion %.

### 4.2 Analysis artifacts
- FR-A1: Store site-level executive summary (HTML/text).
- FR-A2: Store per-page analysis notes (good/bad/best practices).
- FR-A3: Read-only presentment at session start (step 2 of script).

### 4.3 Review session (deterministic script)
State machine per `copywriting.session`:

| State | Description |
|-------|-------------|
| `draft` | Created, not started |
| `intro` | Exec summary shown; await proceed/later |
| `page_select` | Choose page |
| `page_intro` | Page analysis + guidelines |
| `section_fact` | 4.1 |
| `section_interpret` | 4.2 |
| `section_suggest` | 4.3 |
| `section_decide` | Accept / edit / reject interpretation |
| `page_done` | Page complete; next page or finish |
| `finished` | Session closed |
| `paused` | Later |

- FR-S1: Only one active session per user per website (configurable).
- FR-S2: Steps 4.1–4.3 show matrix fields; operator cannot skip logging final when marking approved.
- FR-S3: **Accept** copies suggestion → final, status `approved`, version++.
- FR-S4: **Edit** opens pre-filled final (default = suggestion); save → `updated`.
- FR-S5: **Reject interpretation** requires note; stores evidence event; allows new interpretation/suggestion (manual fields in v1; LLM hook later).
- FR-S6: Page completion requires all sections in scope `approved|updated|skipped` (skip allowed only for Manager).
- FR-S7: Discuss/chatter on session and section for free comments.
- FR-S8: Bus/Discuss message optional on session finish.

### 4.4 Apply and verify
- FR-P1: Apply job selects rows `approved|updated` with `apply_method != 'none'`.
- FR-P2: Apply methods (v1): `manual_checklist` (default), `website_page_field` (mapped), `ir_ui_view_replace` (mapped anchors only).
- FR-P3: No silent full-HTML rewrite without mapping.
- FR-P4: Verify job fetches public URLs (or renders via `ir.http`/`website`) and compares normalized text hashes to matrix `content_final` or `content_current`.
- FR-P5: Report orphans (live unmatched) and missing (matrix unmatched).

### 4.5 Translation readiness (data only in v1)
- FR-T1: Section stores `lang` (default `en_US`); unique (page_id, anchor_key, lang).
- FR-T2: Export includes lang column; no full translation UI in v1.

### 4.6 Non-functional
- NFR-1: Works offline of external LLM.
- NFR-2: All writes via ORM; no raw SQL in apply path.
- NFR-3: Audit: `create_uid`, `write_uid`, `write_date` + session events.
- NFR-4: Idempotent import (upsert on website_code + page_url + anchor_key + lang).
- NFR-5: Module uninstall does not delete website pages (only matrix data).

---

## 5. Data model

### 5.1 `copywriting.website`
| Field | Type | Notes |
|-------|------|-------|
| name | Char | Invisible City Tours |
| code | Char | `incity` unique |
| website_id | Many2one `website` | Optional link |
| base_url | Char | https://www.invisiblecity.site |
| executive_summary | Html | Step 2 |
| active | Boolean | |

### 5.2 `copywriting.page`
| Field | Type | Notes |
|-------|------|-------|
| website_id | Many2one `copywriting.website` required | |
| name | Char | Home, Contact, … |
| url | Char | `/`, `/contactus` |
| sequence | Integer | |
| analysis_html | Html | Per-page analysis |
| guidelines_html | Html | Best practices for this page |
| status | Selection | `todo`, `in_progress`, `done` |
| section_count / approved_count | Integer computed | |
| completion_ratio | Float computed | |

Constraint: unique `(website_id, url)`.

### 5.3 `copywriting.section`
| Field | Type | Notes |
|-------|------|-------|
| page_id | Many2one required ondelete cascade | |
| sequence | Integer | |
| name | Char | Hero H1, Footer about, … |
| role | Selection | `h1`,`h2`,`subhead`,`body`,`cta`,`nav`,`footer`,`meta`,`other` |
| anchor_key | Char | Stable id e.g. `home.hero.h1` |
| dom_id | Char | Live HTML id (no `#`); dual-key with anchor_key for editor/public deep-links |
| lang | Char | default `en_US` |
| content_current | Text | 4.1 fact (as on site / import) |
| content_interpretation | Text | 4.2 |
| content_suggestion | Text | 4.3 |
| content_final | Text | Approved/edited |
| status | Selection | `draft`,`pending_review`,`approved`,`updated`,`skipped`,`rejected_interp` |
| version | Integer | default 1 |
| content_hash_current | Char | sha256 normalized current |
| content_hash_final | Char | |
| apply_method | Selection | `none`,`manual_checklist`,`website_page_field`,`ir_ui_view_replace` |
| apply_target | Char | JSON or dotted target, e.g. view xmlid + note |
| last_session_id | Many2one session | |
| active | Boolean | |

Constraint: unique `(page_id, anchor_key, lang)`.

### 5.4 `copywriting.section.version`
| Field | Type |
|-------|------|
| section_id | Many2one cascade |
| version | Integer |
| content_final | Text |
| status | Selection |
| event | Selection `accept`,`edit`,`import`,`apply` |
| user_id | Many2one res.users |
| note | Text |

### 5.5 `copywriting.session`
| Field | Type |
|-------|------|
| name | Char computed |
| website_id | Many2one |
| user_id | Many2one required |
| state | Selection (see 4.3) |
| current_page_id | Many2one |
| current_section_id | Many2one |
| page_ids | Many2many scope (optional subset) |
| date_start / date_end | Datetime |
| company_id | Many2one | multi-company safe |

### 5.6 `copywriting.session.event`
| Field | Type |
|-------|------|
| session_id | Many2one cascade |
| section_id | Many2one |
| step | Selection `intro`,`fact`,`interpret`,`suggest`,`decide`,`page_done` |
| payload_json | Text | optional snapshot |
| note | Text | reject evidence |
| user_id | Many2one |

### 5.7 `copywriting.apply.run` / `copywriting.verify.run`
Header logs: user, timestamp, counters, log Html/Text, state `ok|warn|error`.

---

## 6. State machine (session)

```text
draft
  → action_start → intro
intro
  → action_proceed → page_select
  → action_later → paused
page_select
  → action_choose_page → page_intro
page_intro
  → action_start_sections → section_fact (first section by sequence)
section_fact
  → action_next → section_interpret
section_interpret
  → action_next → section_suggest
section_suggest
  → action_next → section_decide
section_decide
  → action_accept → (save final=suggestion, approved) → next section or page_done
  → action_edit_save → (final=edited, updated) → next
  → action_reject_interp → (note required, rejected_interp) → section_interpret
page_done
  → action_next_page → page_select
  → action_finish → finished
paused → action_resume → prior state (store resume_state)
```

Implement with explicit methods on `copywriting.session` (no bare write to `state` from UI except through buttons).  
Security: portal user only own `user_id` sessions.

---

## 7. UX specification

### 7.1 Backend (v0)
Menus under **Content Matrix**:
- Websites
- Pages
- Sections
- Sessions
- Import / Export (wizard)
- Apply runs
- Verify runs

**Session form**
- Statusbar on `state`
- Header: website, user, progress bar (sections done / total in scope)
- Notebook:
  - **Step content:** dynamic fields depending on state (summary / page analysis / 4.1–4.3 / decide)
  - **Section list:** tree of sections with status badges
  - **Chatter:** mail.thread

**Decide step**
- Buttons: Accept suggestion | Edit final | Reject interpretation | Skip (Manager)
- Edit: `content_final` editable, default suggestion via onchange when entering edit mode

### 7.2 Portal (v1.1)
- `/my/content-matrix` list sessions
- `/my/content-matrix/session/<id>` step UI (QWeb + JS minimal)
- Same transitions; no Apply/Verify

### 7.3 Discuss
- `_inherit mail.thread` on `copywriting.session`, `copywriting.section`
- `message_post` on session finish and on apply/verify completion
- Optional: subscribe client partner on website record

### 7.4 Discuss Matrix Bot (shipped)
Auth-only adapter over `copywriting.session` (not public Live Chat, not Ask AI):

- Internal user + partner **Content Matrix Bot** (`im_status=bot`) for Discuss picker visibility
- Groups: Operator / Manager only; portal and public denied
- State-aware **option list** under each bot message (click or reply with number)
- Combined section card: fact + interpretation + suggestion in one message → Accept / edit / reject
- Deep-links default to Website Edit: `path?enable_editor=1#dom_id` (same window). Assets JS scrolls/highlights the builder iframe target
- Menu: **Matrix Bot (Discuss)**; session button **Open Matrix Bot**; website **Import DOM anchor map**
- See operator guide for day-to-day flow

---

## 8. Import / export formats

### 8.1 CSV columns (sections)
```text
website_code,page_url,page_name,sequence,anchor_key,lang,role,name,
content_current,content_interpretation,content_suggestion,content_final,status,apply_method,apply_target
```

### 8.2 JSON
```json
{
  "website": {"code": "incity", "base_url": "https://www.invisiblecity.site", "executive_summary": "..."},
  "pages": [
    {
      "url": "/",
      "name": "Home",
      "analysis_html": "...",
      "guidelines_html": "...",
      "sections": [
        {
          "anchor_key": "home.hero.h1",
          "sequence": 10,
          "role": "h1",
          "name": "Hero title",
          "content_current": "EASY SINTRA",
          "content_interpretation": "...",
          "content_suggestion": "Sintra, told properly",
          "status": "pending_review"
        }
      ]
    }
  ]
}
```

Upsert key: `(website_code, page_url, anchor_key, lang)`.

---

## 9. Apply and verify design

### 9.1 Apply mapping registry
Python dict/registry in module (extendable):

```python
APPLY_REGISTRY = {
    "incity:home.footer.about": {
        "method": "manual_checklist",  # or view replace when stable
    },
    # future:
    # "incity:home.hero.h1": {"method": "ir_ui_view_replace", "view_xmlid": "...", "xpath": "..."},
}
```

v1 default all `manual_checklist`: export “paste list” for Website Editor.

### 9.2 Verify
- Input: website_id, optional url list
- For each page: HTTP GET `base_url + url` (server-side `requests`/`urllib`) or `website` render with public user
- Extract text blocks (same heuristics as inventory scripts) → normalize (whitespace, case option) → hash
- Match to sections by anchor mapping table or fuzzy containment (flag low confidence)
- Output: `copywriting.verify.run` lines: ok / drift / orphan_live / missing_matrix

### 9.3 Normalization
- Unicode NFKC
- Collapse whitespace
- Optional ignore ALL-CAPS difference flag for reporting only

---

## 10. Module structure

```text
inteligente_content_matrix/
  __init__.py
  __manifest__.py
  models/
    __init__.py
    copywriting_website.py
    copywriting_page.py
    copywriting_section.py
    copywriting_section_version.py
    copywriting_session.py
    copywriting_session_event.py
    copywriting_apply.py
    copywriting_verify.py
    matrix_discuss_bot.py
    res_partner.py             # Discuss channel hook
  wizards/
    __init__.py
    matrix_import_wizard.py
    matrix_export_wizard.py
  views/
    menus.xml
    copywriting_website_views.xml
    copywriting_page_views.xml
    copywriting_section_views.xml
    copywriting_session_views.xml
    copywriting_apply_views.xml
    copywriting_verify_views.xml
    wizards.xml
  security/
    content_matrix_security.xml
    ir.model.access.csv
  data/
    matrix_bot_data.xml
    seeds/incity_matrix_v1.json
    seeds/incity_matrix_v2_extra_pages.json
    seeds/incity_dom_anchor_map.json
  static/src/discuss/
    matrix_bot_choices.js
    matrix_bot_choices.scss
  tests/
  README.md
```

**Manifest depends:** `['mail', 'website', 'portal']`  
**Version:** `19.0.1.7.2`  
**License:** LGPL-3 (align WeRa/Odoo CE)  
**Author:** Inteligente / WeRa Global

---

## 11. Security matrix (access CSV summary)

| Model | Manager | Operator | Portal reviewer |
|-------|---------|----------|-----------------|
| website/page/section | R/W | R/W | R (own website) |
| section.version | R/W | R | R own |
| session/event | R/W | R/W own create | R/W own |
| apply/verify run | R/W | R/W | — |
| import/export wizard | yes | yes | export own only |

Record rules: portal `user_id = user.id` on sessions; website_id in allowed partners for sections.

---

## 12. Integration points

| System | Integration |
|--------|-------------|
| `website` | Link pages; optional apply; verify via public URL |
| `mail` | thread + optional activity |
| `incity_community_shim` | Independent; no hard depend |
| Frank deploy | addons path already mounts `/home/wera/incity-site/addons` |
| Seed data | JSON from Inteligente evidence / Resources |

---

## 13. Testing strategy

### 13.1 Unit / HTTP case tests (Odoo)
- Session transitions happy path Home 2 sections
- Reject interpretation requires note
- Import upsert idempotent
- Export round-trip
- Access: public user cannot read section
- Portal user cannot open others’ session

### 13.2 Pilot acceptance (InCity)
- [ ] Import redacted matrix for Home + Contact + global footer rows
- [ ] Run full session on Home as operator
- [ ] Export approved matrix
- [ ] Verify flags known intentional drifts
- [ ] Client or operator signs off sample finals

### 13.3 Regression
- Public site still 200 after module install
- No change to website content until Apply

---

## 14. Risks and mitigations

| Risk | Mitigation |
|------|------------|
| SaaS HTML sections lack stable anchors | anchor_key manual map; default apply=manual_checklist |
| Client won’t pay €10 | Design-partner framing; value demo first |
| Scope creep to agents | Spec freeze v1; LLM behind feature flag |
| Accidental live overwrite | Apply dry-run; Manager-only confirm; backup note on Frank |
| Translation explosion | lang key on section from day one; UI later |
| layout_background / shim noise | Keep content module separate from community_shim |

---

## 15. LLM extension (explicitly out of v1, interface only)

```python
class CopywritingSection(models.Model):
    def action_generate_interpretation(self):
        """Hook: raise UserError('LLM not enabled') unless ir.config_parameter set."""
    def action_generate_suggestion(self):
        """Same."""
```

Config params: `inteligente_content_matrix.llm_enabled`, `llm_endpoint`, `llm_model` — unused until v2.

---

## 16. Deliverables checklist

- [x] Module source in Inteligente repo and Frank addons  
- [x] This spec + operator guide + DOM anchor map  
- [x] Seed JSON for InCity (v1 Home/Contact/Privacy + v2 menu routes + DOM map)  
- [x] Operator guide (Discuss bot UX included)  
- [x] Pilot path: Home matrix largely approved; remaining site-wide sections open for client pass  
- [ ] Export/verify evidence pack after client manual test  
- [x] Discuss Matrix Bot (auth, options, combined card, editor deep-links)  

---

# Development plan and tasks

## Phases overview

| Phase | Name | Outcome |
|-------|------|---------|
| P0 | Foundations | Module installs on `incity_site` |
| P1 | Matrix + import/export | Seeded InCity matrix in DB |
| P2 | Session wizard | Deterministic review loop works backend |
| P3 | Discuss + polish | Notifications + UX |
| P4 | Verify (+ optional apply checklist) | Trust loop closed |
| P5 | Pilot with client | Feedback + pay conversation |
| P6 | Portal (optional) | Client self-serve review |
| P7 | LLM hooks (optional) | Assisted 4.2/4.3 |

---

## Task breakdown

### P0 — Foundations
| ID | Task | Acceptance | Est. |
|----|------|------------|------|
| T0.1 | Create module skeleton + manifest depends mail/website/portal | `-i inteligente_content_matrix` OK on incity_site | S |
| T0.2 | Security groups + empty menus | Menu visible to Manager only | S |
| T0.3 | README install steps for Frank addons path | Doc in module README | S |
| T0.4 | Smoke: public site still 200 after install | curl home/login 200 | S |

### P1 — Data model and matrix I/O
| ID | Task | Acceptance | Est. |
|----|------|------------|------|
| T1.1 | Models website/page/section + constraints/views | CRUD in UI | M |
| T1.2 | Section version model + write hooks on final change | Version row on accept/edit | M |
| T1.3 | Import wizard CSV+JSON upsert | Double import no dupes | M |
| T1.4 | Export wizard | CSV matches import columns | S |
| T1.5 | Build seed JSON from redacted matrix (Home, Contact, footer, meta) | File in `data/seeds/incity_matrix_v1.json` | M |
| T1.6 | Import seed on pilot DB | Sections listed with pending_review | S |
| T1.7 | Sitemap/list dashboard (completion %) | Page tree shows ratios | S |

### P2 — Review session engine
| ID | Task | Acceptance | Est. |
|----|------|------------|------|
| T2.1 | Session + event models | Create session for website | S |
| T2.2 | State machine methods + button statuses | Illegal transitions blocked | L |
| T2.3 | Session form UX for intro / page_select / page_intro | Matches script steps 2–3 | M |
| T2.4 | Section loop 4.1–4.3 display | Shows current/interpretation/suggestion | M |
| T2.5 | Decide: accept / edit / reject interpretation | Status+version+event correct | M |
| T2.6 | Multi-page scope + finish | page_done → select or finished | M |
| T2.7 | Automated tests for transitions | `HttpCase` or `TransactionCase` green | M |
| T2.8 | Operator dry-run on Home seed | All Home sections approved/updated | M |

### P3 — Discuss and operator UX
| ID | Task | Acceptance | Est. |
|----|------|------------|------|
| T3.1 | mail.thread on session + section | Chatter works | S |
| T3.2 | message_post on session finished | Notification in Discuss | S |
| T3.3 | Progress indicator + section kanban/filter by status | Operator can resume paused | S |
| T3.4 | One-page operator guide | `docs/content-matrix-operator-guide.md` | S |

### P4 — Verify and apply checklist
| ID | Task | Acceptance | Est. |
|----|------|------------|------|
| T4.1 | Verify run: fetch URLs, hash report | Run model stores lines | M |
| T4.2 | Orphan/missing classification | Documented in run log | M |
| T4.3 | Apply run dry-run + manual_checklist PDF/HTML | Checklist lists finals to paste | M |
| T4.4 | (Optional) one auto-apply mapped row e.g. footer about if safe | Documented mapping | L |
| T4.5 | Frank evidence: verify output attached under ops/evidence | File stored | S |

### P5 — Pilot
| ID | Task | Acceptance | Est. |
|----|------|------------|------|
| T5.1 | Full matrix seed remaining pages (Lisbon, Sintra, INTV, Reviews) | All URLs in matrix | M |
| T5.2 | Conduct Home+Contact session with design partner or proxy | Sign-off notes | L |
| T5.3 | Export finals; apply via checklist to live site | Spot-check live copy | M |
| T5.4 | Re-verify after apply | Drift list empty for applied anchors | S |
| T5.5 | Retro: time metrics + willingness-to-pay conversation | Written outcome | S |

### P6 — Portal (optional)
| ID | Task | Acceptance | Est. |
|----|------|------------|------|
| T6.1 | Portal security + controllers | auth user only | M |
| T6.2 | Portal session step UI | Client can accept/edit | L |
| T6.3 | Portal tests access denial anonymous | 303/403 | S |

### P7 — LLM hooks (optional)
| ID | Task | Acceptance | Est. |
|----|------|------------|------|
| T7.1 | Config flag + stub methods | Disabled by default | S |
| T7.2 | Provider adapter + prompt templates for 4.2/4.3 | Goldens on 5 sections | L |
| T7.3 | Cost/safety limits per session | Cap documented | S |

---

## Dependencies graph (implementation)

```text
T0.* → T1.* → T2.* → T3.* → T4.* → T5.*
                     ↘ T6.* (optional, after T2)
                     ↘ T7.* (optional, after T5)
```

---

## Estimation legend
- **S** = ≤ 0.5 day  
- **M** = 0.5–2 days  
- **L** = 2–4 days  

**MVP ship gate:** P0+P1+P2+T3.1+T3.4+T4.1+T4.3 complete (backend session + export + verify/checklist).  
**Pilot-partner gate:** P5.2–P5.5.

---

## Immediate next actions

1. Implement **T0.1–T0.4** on Frank `incity_site` addons path.  
2. Convert redacted content matrix → **T1.5 seed JSON**.  
3. **T1.1–T1.6** import.  
4. **T2** session engine; dry-run Home.  

---

## Document control

| Version | Date | Notes |
|---------|------|-------|
| 0.1 | 2026-11-17 | Initial spec from working note + CE rethink + InCity pilot constraints |
