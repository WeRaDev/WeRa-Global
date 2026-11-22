# -*- coding: utf-8 -*-
from html import escape

from markupsafe import Markup

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class CopywritingSession(models.Model):
    _name = "copywriting.session"
    _description = "Content Matrix Review Session"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "id desc"

    name = fields.Char(compute="_compute_name", store=True)
    website_id = fields.Many2one(
        "copywriting.website", required=True, ondelete="cascade", index=True
    )
    user_id = fields.Many2one(
        "res.users",
        required=True,
        default=lambda self: self.env.user,
        index=True,
        ondelete="restrict",
    )
    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        required=True,
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("intro", "Intro"),
            ("page_select", "Select page"),
            ("page_intro", "Page intro"),
            ("section_fact", "Section fact"),
            ("section_interpret", "Section interpretation"),
            ("section_suggest", "Section suggestion"),
            ("section_decide", "Section decide"),
            ("page_done", "Page done"),
            ("finished", "Finished"),
            ("paused", "Paused"),
        ],
        default="draft",
        required=True,
        tracking=True,
        index=True,
    )
    resume_state = fields.Char(
        help="State to restore when resuming from paused"
    )
    current_page_id = fields.Many2one("copywriting.page", ondelete="set null")
    current_section_id = fields.Many2one("copywriting.section", ondelete="set null")
    page_ids = fields.Many2many(
        "copywriting.page",
        "copywriting_session_page_rel",
        "session_id",
        "page_id",
        string="Page scope",
        help="Empty = all active pages of the website",
    )
    date_start = fields.Datetime()
    date_end = fields.Datetime()
    event_ids = fields.One2many("copywriting.session.event", "session_id", string="Events")
    discuss_channel_id = fields.Many2one(
        "discuss.channel",
        string="Discuss channel",
        ondelete="set null",
        index=True,
        help="Optional Discuss channel bound to this review (Matrix Bot).",
    )

    # UI helpers
    executive_summary = fields.Html(
        related="website_id.executive_summary", readonly=True
    )
    page_analysis_html = fields.Html(
        related="current_page_id.analysis_html", readonly=True
    )
    page_guidelines_html = fields.Html(
        related="current_page_id.guidelines_html", readonly=True
    )
    section_name = fields.Char(related="current_section_id.name", readonly=True)
    section_anchor_key = fields.Char(
        related="current_section_id.anchor_key", readonly=True
    )
    section_role = fields.Selection(
        related="current_section_id.role", readonly=True
    )
    content_current = fields.Text(
        related="current_section_id.content_current", readonly=True
    )
    content_interpretation = fields.Text(
        related="current_section_id.content_interpretation", readonly=False
    )
    content_suggestion = fields.Text(
        related="current_section_id.content_suggestion", readonly=False
    )
    content_final = fields.Text(
        related="current_section_id.content_final", readonly=False
    )
    reject_note = fields.Text(
        string="Reject interpretation note",
        help="Required when rejecting interpretation",
    )
    edit_mode = fields.Boolean(
        string="Edit final",
        help="When set, decide step focuses on editing final text",
    )
    progress_done = fields.Integer(compute="_compute_progress")
    progress_total = fields.Integer(compute="_compute_progress")
    progress_ratio = fields.Float(compute="_compute_progress", string="Progress")
    progress_label = fields.Char(compute="_compute_progress", string="Progress label")
    scoped_section_ids = fields.Many2many(
        "copywriting.section",
        compute="_compute_scoped_sections",
        string="Sections in scope",
    )

    def get_base_url(self):
        """Matrix website_id is copywriting.website, not website.website (no .domain)."""
        self.ensure_one()
        base = (self.website_id.base_url or "").rstrip("/") if self.website_id else ""
        if base:
            return base
        return self.env["ir.config_parameter"].sudo().get_param("web.base.url") or ""

    def get_preview_url(self, editor=True):
        """URL for current page/section. Default editor=True (bot runs in Website Edit)."""
        self.ensure_one()
        if self.current_section_id:
            return self.current_section_id.get_preview_url(editor=editor)
        path = "/"
        if self.current_page_id:
            path = self.current_page_id.url or "/"
            if not path.startswith("/"):
                path = "/" + path
        if editor:
            if path == "/":
                return "/?enable_editor=1"
            return "%s?enable_editor=1" % path
        base = (self.get_base_url() or "").rstrip("/")
        if not base:
            return False
        if path == "/":
            return base + "/"
        return base + path

    def _format_section_review_html(self):
        """Single-message fact + interpretation + suggestion for bot/decide UX."""
        self.ensure_one()
        sec = self.current_section_id
        if not sec:
            return "<p>No current section.</p>"
        return (
            "<p><b>Section</b> %s · <code>%s</code> · role %s</p>"
            "<p><b>4.1 Fact (on site today)</b></p><pre>%s</pre>"
            "<p><b>4.2 Interpretation</b></p><pre>%s</pre>"
            "<p><b>4.3 Suggestion</b></p><pre>%s</pre>"
            "<p>Choose <b>Accept suggestion</b>, or type "
            "<code>edit …</code> / <code>reject …</code> if needed.</p>"
            % (
                escape(sec.name or ""),
                escape(sec.anchor_key or ""),
                escape(sec.role or ""),
                escape(sec.content_current or ""),
                escape(sec.content_interpretation or ""),
                escape(sec.content_suggestion or ""),
            )
        )

    def action_bot_open_section_review(self):
        """Enter current/next section directly at decide (combined card). Bot path only."""
        self.ensure_one()
        if self.state == "page_intro":
            page = self.current_page_id
            if not page:
                raise UserError("No page selected.")
            section = self._next_pending_section(page)
            if not section:
                self._set_state("page_done")
                page.status = "done"
                self._log_event("page_done")
                return True
            self._enter_section(section, start_at="section_decide")
            return True
        if self.state in (
            "section_fact",
            "section_interpret",
            "section_suggest",
        ):
            if not self.current_section_id:
                raise UserError("No current section.")
            self._set_state("section_decide")
            self._log_event(
                "decide",
                section=self.current_section_id,
                note="bot skip to combined decide",
            )
            return True
        if self.state == "section_decide":
            return True
        raise UserError("Cannot open section review from state %s." % self.state)

    def _preview_link_html(self):
        self.ensure_one()
        url = self.get_preview_url(editor=True)
        if not url:
            return ""
        # Website Edit mode + same window (bot chat only appears in editor).
        note = "Website Edit mode · same window · scrolls to block when anchored"
        return (
            '<p><a href="%s" class="o_matrix_preview_link">'
            "Open in editor</a> <span style=\"color:#666;\">(%s)</span></p>"
            % (escape(url, quote=True), escape(note))
        )

    def _format_step_card_html(self, include_preview=True):
        """HTML card for Discuss bot / chatter step summary."""
        self.ensure_one()
        state = self.state or "draft"
        site = escape(self.website_id.name or self.website_id.code or "")
        progress = escape(self.progress_label or "")
        parts = [
            "<p><b>Session</b> · %s · state <code>%s</code> · progress %s</p>"
            % (site, escape(state), progress)
        ]
        if state == "intro":
            parts.append(
                "<p>Read the executive summary below the options, then choose "
                "<b>Continue</b>.</p>"
            )
            if self.executive_summary:
                # short plain excerpt
                import re as _re

                plain = _re.sub(r"<[^>]+>", " ", self.executive_summary or "")
                plain = _re.sub(r"\s+", " ", plain).strip()[:400]
                if plain:
                    parts.append("<p><i>%s</i></p>" % escape(plain))
        elif state == "page_select":
            parts.append(
                "<p><b>Choose a page</b> from the options below "
                "(or type its number).</p>"
            )
        elif state == "page_intro":
            page = self.current_page_id
            pending = self._pending_sections_for_page(page) if page else self.env["copywriting.section"]
            closed = 0
            total = 0
            if page:
                secs = self._ordered_sections_for_page(page)
                total = len(secs)
                closed = total - len(pending)
            parts.append(
                "<p><b>Page ready:</b> %s (<code>%s</code>) · "
                "%s pending / %s sections.</p>"
                % (
                    escape(page.name or "") if page else "",
                    escape(page.url or "") if page else "",
                    len(pending),
                    total,
                )
            )
            if pending:
                parts.append(
                    "<p>Choose <b>Start sections</b> to review the next open copy block.</p>"
                )
            else:
                parts.append(
                    "<p><b>No open sections on this page</b> "
                    "(all are approved, updated, or skipped). "
                    "Choose another page, or finish the session.</p>"
                )
            if page and page.analysis_html:
                import re as _re

                plain = _re.sub(r"<[^>]+>", " ", page.analysis_html or "")
                plain = _re.sub(r"\s+", " ", plain).strip()[:350]
                if plain:
                    parts.append(
                        "<p><b>Analysis (excerpt)</b><br/><i>%s</i></p>"
                        % escape(plain)
                    )
        elif state in (
            "section_fact",
            "section_interpret",
            "section_suggest",
            "section_decide",
        ):
            # One combined card (fact + interpretation + suggestion) for organic chat UX.
            parts.append(self._format_section_review_html())
        elif state == "page_done":
            page = self.current_page_id
            label = escape(page.name or page.url or "page") if page else "page"
            parts.append(
                "<p><b>%s is complete for this session</b> "
                "(no pending sections left on it).</p>"
                "<p>Choose another page with open work, or finish.</p>"
                % label
            )
        elif state == "paused":
            parts.append(
                "<p>Paused at <code>%s</code>. Choose <b>Resume</b> when ready.</p>"
                % escape(self.resume_state or "")
            )
        elif state == "finished":
            parts.append("<p>Session finished.</p>")
        if include_preview and state not in ("draft", "finished"):
            parts.append(self._preview_link_html())
        return "".join(parts)

    @api.model
    def action_open_matrix_bot_home(self):
        """Menu entry: open Discuss DM with Matrix Bot (no session required)."""
        bot = self.env.ref(
            "inteligente_content_matrix.partner_matrix_bot", raise_if_not_found=False
        )
        if not bot:
            raise UserError("Content Matrix Bot partner is not installed.")
        Channel = self.env["discuss.channel"]
        if hasattr(Channel, "_get_or_create_chat"):
            channel = Channel._get_or_create_chat([bot.id])
        else:
            raise UserError("Discuss chat API is unavailable on this Odoo build.")
        greet = (
            "<p>Hi — I am the <b>Content Matrix Bot</b>.</p>"
            "<p>Use the option buttons below (or type a number).</p>"
        )
        # Idle options rendered by bot helper
        Bot = self.env["copywriting.matrix.bot"]
        body = Bot._with_options(greet, None, self.env.user, idle=True)
        channel.with_context(matrix_bot_skip=True).message_post(
            body=Markup(body),
            message_type="comment",
            subtype_xmlid="mail.mt_note",
            author_id=bot.id,
        )
        return {
            "type": "ir.actions.client",
            "tag": "mail.action_discuss",
            "context": {"active_id": channel.id},
        }

    def action_open_matrix_bot_dm(self):
        """Open/create a Discuss DM with the Content Matrix Bot and bind this session."""
        self.ensure_one()
        bot = self.env.ref(
            "inteligente_content_matrix.partner_matrix_bot", raise_if_not_found=False
        )
        if not bot:
            raise UserError("Content Matrix Bot partner is not installed.")
        # Odoo 19: _get_or_create_chat([other_partner_ids]) adds current user automatically.
        Channel = self.env["discuss.channel"].with_context(mail_create_nosubscribe=True)
        if hasattr(Channel, "_get_or_create_chat"):
            channel = Channel._get_or_create_chat([bot.id])
        elif hasattr(Channel, "channel_get"):
            try:
                channel = Channel.channel_get(partners_to=bot.ids)
            except TypeError:
                channel = Channel.channel_get(bot.ids)
        else:
            channel = Channel.create(
                {
                    "name": "Content Matrix · %s" % (self.display_name or "session"),
                    "channel_type": "channel",
                }
            )
            Member = self.env["discuss.channel.member"].sudo()
            for partner in (self.env.user.partner_id | bot):
                if not Member.search(
                    [
                        ("channel_id", "=", channel.id),
                        ("partner_id", "=", partner.id),
                    ],
                    limit=1,
                ):
                    Member.create(
                        {"channel_id": channel.id, "partner_id": partner.id}
                    )
        self.discuss_channel_id = channel.id
        bound = (
            "<p>Bound to session <b>%s</b>.</p>"
            % escape(self.display_name)
            + self._format_step_card_html(include_preview=True)
        )
        body = self.env["copywriting.matrix.bot"]._with_options(
            bound, self, self.env.user
        )
        channel.with_context(matrix_bot_skip=True).message_post(
            body=Markup(body),
            message_type="comment",
            subtype_xmlid="mail.mt_note",
            author_id=bot.id,
        )
        action = {
            "type": "ir.actions.client",
            "tag": "mail.action_discuss",
            "params": {},
        }
        # Odoo 19 discuss often uses context default_active_id
        action["context"] = {"active_id": channel.id}
        return action

    @api.depends("website_id", "user_id", "state")
    def _compute_name(self):
        for rec in self:
            parts = [
                rec.website_id.code or "matrix",
                rec.user_id.login or "user",
                rec.state or "draft",
            ]
            rec.name = " / ".join(parts)

    def _scope_pages(self):
        self.ensure_one()
        if self.page_ids:
            return self.page_ids.filtered("active").sorted(
                lambda p: (p.sequence, p.id)
            )
        return self.website_id.page_ids.filtered("active").sorted(
            lambda p: (p.sequence, p.id)
        )

    @api.depends("website_id", "page_ids", "page_ids.section_ids", "page_ids.section_ids.status")
    def _compute_scoped_sections(self):
        for rec in self:
            pages = rec._scope_pages() if rec.website_id else rec.env["copywriting.page"]
            sections = pages.mapped("section_ids").filtered("active")
            rec.scoped_section_ids = sections

    @api.depends(
        "website_id",
        "page_ids",
        "page_ids.section_ids.status",
        "page_ids.section_ids.active",
        "current_section_id",
        "state",
    )
    def _compute_progress(self):
        done_states = ("approved", "updated", "skipped")
        for rec in self:
            sections = rec.scoped_section_ids
            rec.progress_total = len(sections)
            rec.progress_done = len(sections.filtered(lambda s: s.status in done_states))
            rec.progress_ratio = (
                rec.progress_done / rec.progress_total if rec.progress_total else 0.0
            )
            rec.progress_label = "%s / %s" % (rec.progress_done, rec.progress_total)

    def _log_event(self, step, section=None, note=False, payload=False):
        self.ensure_one()
        self.env["copywriting.session.event"].create(
            {
                "session_id": self.id,
                "section_id": section.id if section else False,
                "step": step,
                "note": note or False,
                "payload_json": payload or False,
                "user_id": self.env.user.id,
            }
        )

    def _set_state(self, new_state):
        self.ensure_one()
        self.write({"state": new_state})

    def _require_state(self, *allowed):
        self.ensure_one()
        if self.state not in allowed:
            raise UserError(
                "Invalid session step. Current state is '%s'; expected one of %s."
                % (self.state, ", ".join(allowed))
            )

    def _ordered_sections_for_page(self, page):
        return page.section_ids.filtered("active").sorted(lambda s: (s.sequence, s.id))

    def _pending_sections_for_page(self, page):
        """Active sections on page not yet approved/updated/skipped."""
        if not page:
            return self.env["copywriting.section"]
        done = ("approved", "updated", "skipped")
        return self._ordered_sections_for_page(page).filtered(
            lambda s: s.status not in done
        )

    def _next_pending_section(self, page, after_section=None):
        """Next section not yet approved/updated/skipped."""
        done = ("approved", "updated", "skipped")
        sections = self._ordered_sections_for_page(page)
        if after_section:
            found_current = False
            for sec in sections:
                if sec.id == after_section.id:
                    found_current = True
                    continue
                if found_current and sec.status not in done:
                    return sec
        for sec in sections:
            if sec.status not in done:
                return sec
        return self.env["copywriting.section"]

    def _page_complete(self, page):
        done = ("approved", "updated", "skipped")
        sections = self._ordered_sections_for_page(page)
        return bool(sections) and all(s.status in done for s in sections)

    def _enter_section(self, section, start_at="section_fact"):
        self.ensure_one()
        self.write(
            {
                "current_section_id": section.id,
                "current_page_id": section.page_id.id,
                "edit_mode": False,
                "reject_note": False,
                "state": start_at,
            }
        )
        super(type(section), section).write({"last_session_id": self.id})
        event_by_state = {
            "section_fact": "fact",
            "section_interpret": "interpret",
            "section_suggest": "suggest",
            "section_decide": "decide",
        }
        self._log_event(
            event_by_state.get(start_at, "fact"), section=section
        )
        if section.page_id.status == "todo":
            section.page_id.status = "in_progress"

    # --- transitions ---

    def action_start(self):
        for rec in self:
            if rec.state == "paused":
                rec.action_resume()
                continue
            rec._require_state("draft")
            rec.write(
                {
                    "state": "intro",
                    "date_start": fields.Datetime.now(),
                    "current_page_id": False,
                    "current_section_id": False,
                    "edit_mode": False,
                    "reject_note": False,
                }
            )
            rec._log_event("intro")
        return True

    def action_proceed(self):
        for rec in self:
            rec._require_state("intro")
            rec._set_state("page_select")
            rec._log_event("page_select")
        return True

    def action_later(self):
        for rec in self:
            if rec.state == "finished":
                raise UserError("Session already finished.")
            if rec.state == "draft":
                raise UserError("Start the session before pausing.")
            prior = rec.state
            rec.write({"resume_state": prior, "state": "paused"})
            rec._log_event("pause", note="paused from %s" % prior)
            rec._notify_session(
                "Session paused at <b>%s</b> (%s/%s sections done)."
                % (prior, rec.progress_done, rec.progress_total),
                subtype_xmlid="mail.mt_note",
            )
        return True

    def action_resume(self):
        for rec in self:
            rec._require_state("paused")
            target = rec.resume_state or "intro"
            rec.write({"state": target, "resume_state": False})
            rec._log_event("resume", note="resumed to %s" % target)
            rec._notify_session(
                "Session resumed at <b>%s</b>." % target,
                subtype_xmlid="mail.mt_note",
            )
        return True

    def action_choose_page(self):
        """Requires current_page_id set (user selected page in UI)."""
        for rec in self:
            rec._require_state("page_select", "page_done")
            if not rec.current_page_id:
                raise UserError("Select a page first.")
            if rec.current_page_id not in rec._scope_pages():
                raise UserError("Selected page is not in session scope.")
            rec.write(
                {
                    "state": "page_intro",
                    "current_section_id": False,
                    "edit_mode": False,
                    "reject_note": False,
                }
            )
            rec._log_event("page_intro")
        return True

    def action_start_sections(self):
        for rec in self:
            rec._require_state("page_intro")
            page = rec.current_page_id
            if not page:
                raise UserError("No page selected.")
            section = rec._next_pending_section(page)
            if not section:
                rec._set_state("page_done")
                page.status = "done"
                rec._log_event("page_done")
                continue
            rec._enter_section(section, start_at="section_fact")
        return True

    def action_next_step(self):
        """Advance fact→interpret→suggest→decide."""
        for rec in self:
            mapping = {
                "section_fact": ("section_interpret", "interpret"),
                "section_interpret": ("section_suggest", "suggest"),
                "section_suggest": ("section_decide", "decide"),
            }
            rec._require_state(*mapping.keys())
            if not rec.current_section_id:
                raise UserError("No current section.")
            new_state, event_step = mapping[rec.state]
            rec._set_state(new_state)
            rec._log_event(event_step, section=rec.current_section_id)
        return True

    def action_accept_suggestion(self):
        for rec in self:
            rec._require_state("section_decide")
            sec = rec.current_section_id
            if not sec:
                raise UserError("No current section.")
            sec.action_accept_suggestion()
            rec._log_event("decide", section=sec, note="accepted suggestion")
            rec._advance_after_decide()
        return True

    def action_enable_edit_mode(self):
        for rec in self:
            rec._require_state("section_decide")
            sec = rec.current_section_id
            if not sec:
                raise UserError("No current section.")
            if not sec.content_final and sec.content_suggestion:
                super(type(sec), sec).write(
                    {"content_final": sec.content_suggestion}
                )
            rec.edit_mode = True
        return True

    def action_save_edit(self):
        for rec in self:
            rec._require_state("section_decide")
            if not rec.edit_mode:
                raise UserError("Enable edit mode first.")
            sec = rec.current_section_id
            if not sec:
                raise UserError("No current section.")
            if not (sec.content_final or "").strip():
                raise UserError("Final text is required.")
            sec.action_set_final_updated()
            rec._log_event("decide", section=sec, note="edited final")
            rec.edit_mode = False
            rec._advance_after_decide()
        return True

    def action_reject_interpretation(self):
        for rec in self:
            rec._require_state("section_decide")
            note = (rec.reject_note or "").strip()
            if not note:
                raise UserError(
                    "A note is required when rejecting the interpretation."
                )
            sec = rec.current_section_id
            if not sec:
                raise UserError("No current section.")
            super(type(sec), sec).write({"status": "rejected_interp"})
            rec._log_event(
                "decide", section=sec, note=note, payload='{"action":"reject_interp"}'
            )
            rec.write(
                {
                    "state": "section_interpret",
                    "reject_note": False,
                    "edit_mode": False,
                }
            )
            rec._log_event("interpret", section=sec, note="re-open after reject")
        return True

    def action_skip_section(self):
        """Manager-only skip."""
        for rec in self:
            if not self.env.user.has_group(
                "inteligente_content_matrix.group_manager"
            ):
                raise UserError("Only managers can skip sections.")
            rec._require_state(
                "section_fact",
                "section_interpret",
                "section_suggest",
                "section_decide",
            )
            sec = rec.current_section_id
            if not sec:
                raise UserError("No current section.")
            super(type(sec), sec).write({"status": "skipped"})
            rec._log_event("decide", section=sec, note="skipped")
            rec._advance_after_decide()
        return True

    def _advance_after_decide(self):
        self.ensure_one()
        page = self.current_page_id
        sec = self.current_section_id
        nxt = self._next_pending_section(page, after_section=sec)
        if nxt:
            self._enter_section(nxt, start_at="section_fact")
            return
        page.status = "done"
        self.write(
            {
                "state": "page_done",
                "current_section_id": False,
                "edit_mode": False,
                "reject_note": False,
            }
        )
        self._log_event("page_done")

    def action_next_page(self):
        for rec in self:
            rec._require_state("page_done")
            rec.write(
                {
                    "state": "page_select",
                    "current_page_id": False,
                    "current_section_id": False,
                }
            )
            rec._log_event("page_select")
        return True

    def action_finish(self):
        for rec in self:
            if rec.state not in ("page_done", "page_select", "intro"):
                rec._require_state("page_done", "page_select")
            rec.write(
                {
                    "state": "finished",
                    "date_end": fields.Datetime.now(),
                    "current_section_id": False,
                    "edit_mode": False,
                }
            )
            rec._log_event("finish")
            rec._notify_finish()
        return True

    def _partner_ids_to_notify(self):
        self.ensure_one()
        return self.user_id.partner_id.ids

    def _notify_session(self, body_html, subtype_xmlid="mail.mt_comment"):
        self.ensure_one()
        partner_ids = self._partner_ids_to_notify()
        if partner_ids:
            self.message_subscribe(partner_ids=partner_ids)
        self.message_post(
            body=Markup(body_html),
            message_type="notification",
            subtype_xmlid=subtype_xmlid,
            partner_ids=partner_ids if subtype_xmlid == "mail.mt_comment" else [],
        )

    def _notify_finish(self):
        self.ensure_one()
        done_states = ("approved", "updated", "skipped")
        sections = self.scoped_section_ids
        approved = len(sections.filtered(lambda s: s.status == "approved"))
        updated = len(sections.filtered(lambda s: s.status == "updated"))
        skipped = len(sections.filtered(lambda s: s.status == "skipped"))
        pending = len(sections.filtered(lambda s: s.status not in done_states))
        site_label = self.website_id.name or self.website_id.code or "website"
        user_label = self.user_id.name or self.user_id.login or "operator"
        body = (
            "<p><b>Content matrix review session finished.</b></p>"
            "<ul>"
            "<li>Website: %s</li>"
            "<li>Operator: %s</li>"
            "<li>Progress: %s / %s sections closed</li>"
            "<li>Approved: %s · Updated: %s · Skipped: %s · Still open: %s</li>"
            "</ul>"
            "<p>Next: export approved matrix, then run verify/apply checklist (P4).</p>"
            % (
                site_label,
                user_label,
                self.progress_done,
                self.progress_total,
                approved,
                updated,
                skipped,
                pending,
            )
        )
        self._notify_session(body, subtype_xmlid="mail.mt_comment")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            user_id = vals.get("user_id") or self.env.user.id
            website_id = vals.get("website_id")
            if website_id:
                existing = self.search(
                    [
                        ("user_id", "=", user_id),
                        ("website_id", "=", website_id),
                        ("state", "not in", ("finished", "draft")),
                    ],
                    limit=1,
                )
                if existing:
                    raise ValidationError(
                        "You already have an active session (%s) for this website."
                        % existing.display_name
                    )
        records = super().create(vals_list)
        for rec in records:
            partner = rec.user_id.partner_id
            if partner:
                rec.message_subscribe(partner_ids=partner.ids)
            site_label = rec.website_id.name or rec.website_id.code or "website"
            rec.message_post(
                body=Markup(
                    "Review session created for <b>%s</b>." % site_label
                ),
                message_type="notification",
                subtype_xmlid="mail.mt_note",
            )
        return records
