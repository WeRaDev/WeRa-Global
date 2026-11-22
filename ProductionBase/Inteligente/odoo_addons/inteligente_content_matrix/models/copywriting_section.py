# -*- coding: utf-8 -*-
import hashlib
import unicodedata

from odoo import api, fields, models


def _normalize_text(text):
    if not text:
        return ""
    text = unicodedata.normalize("NFKC", text)
    return " ".join(text.split())


def _hash_text(text):
    norm = _normalize_text(text)
    return hashlib.sha256(norm.encode("utf-8")).hexdigest() if norm else ""


class CopywritingSection(models.Model):
    _name = "copywriting.section"
    _description = "Content Matrix Section"
    _order = "page_id, sequence, id"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    page_id = fields.Many2one(
        "copywriting.page", required=True, ondelete="cascade", index=True
    )
    website_id = fields.Many2one(
        related="page_id.website_id", store=True, index=True, readonly=True
    )
    sequence = fields.Integer(default=10)
    name = fields.Char(required=True)
    role = fields.Selection(
        [
            ("h1", "H1"),
            ("h2", "H2"),
            ("h3", "H3"),
            ("subhead", "Subhead"),
            ("body", "Body"),
            ("cta", "CTA"),
            ("nav", "Nav"),
            ("footer", "Footer"),
            ("meta", "Meta"),
            ("other", "Other"),
        ],
        default="body",
        required=True,
    )
    anchor_key = fields.Char(
        required=True,
        index=True,
        help="Stable id, e.g. home.hero.h1",
    )
    lang = fields.Char(default="en_US", required=True)
    content_current = fields.Text(string="Current (fact)")
    content_interpretation = fields.Text(string="Interpretation")
    content_suggestion = fields.Text(string="Suggestion")
    content_final = fields.Text(string="Final", tracking=True)
    status = fields.Selection(
        [
            ("draft", "Draft"),
            ("pending_review", "Pending Review"),
            ("approved", "Approved"),
            ("updated", "Updated"),
            ("skipped", "Skipped"),
            ("rejected_interp", "Rejected Interpretation"),
        ],
        default="pending_review",
        required=True,
        tracking=True,
    )
    version = fields.Integer(default=1, required=True)
    content_hash_current = fields.Char(compute="_compute_hashes", store=True)
    content_hash_final = fields.Char(compute="_compute_hashes", store=True)
    apply_method = fields.Selection(
        [
            ("none", "None"),
            ("manual_checklist", "Manual checklist"),
            ("website_page_field", "Website page field"),
            ("ir_ui_view_replace", "View replace"),
        ],
        default="manual_checklist",
        required=True,
    )
    apply_target = fields.Char(help="Optional mapping target / notes")
    dom_id = fields.Char(
        string="DOM id",
        index=True,
        help="HTML id on the live page block (no #). Used for session/Discuss preview links.",
    )
    last_session_id = fields.Many2one(
        "copywriting.session",
        string="Last session",
        ondelete="set null",
        index=True,
        help="Most recent review session that touched this section",
    )
    version_ids = fields.One2many(
        "copywriting.section.version", "section_id", string="Versions"
    )
    active = fields.Boolean(default=True)
    color = fields.Integer(compute="_compute_color", store=False)

    _sql_constraints = [
        (
            "page_anchor_lang_uniq",
            "unique(page_id, anchor_key, lang)",
            "Anchor key must be unique per page and language.",
        ),
    ]

    def get_base_url(self):
        """Matrix website_id is copywriting.website, not website.website (no .domain)."""
        self.ensure_one()
        base = (self.website_id.base_url or "").rstrip("/") if self.website_id else ""
        if base:
            return base
        return self.env["ir.config_parameter"].sudo().get_param("web.base.url") or ""

    def _page_path(self):
        self.ensure_one()
        path = (self.page_id.url or "/") if self.page_id else "/"
        if not path.startswith("/"):
            path = "/" + path
        return path or "/"

    def get_preview_url(self, editor=False):
        """URL for this section: public page or Website Edit mode (+ optional #dom_id)."""
        self.ensure_one()
        path = self._page_path()
        dom = (self.dom_id or "").strip().lstrip("#")
        if editor:
            # Relative path keeps the on-site editor/chat session in the same window.
            # Odoo website edit mode: /path?enable_editor=1#anchor
            if path == "/":
                url = "/?enable_editor=1"
            else:
                url = "%s?enable_editor=1" % path
            if dom:
                url = "%s#%s" % (url, dom)
            return url
        base = (self.get_base_url() or "").rstrip("/")
        if not base:
            return False
        if path == "/":
            url = base + "/"
        else:
            url = base + path
        if dom:
            url = "%s#%s" % (url.rstrip("/") if path != "/" else base + "/", dom)
            if path == "/":
                url = base + "/#" + dom
        return url

    @api.depends("content_current", "content_final")
    def _compute_hashes(self):
        for rec in self:
            rec.content_hash_current = _hash_text(rec.content_current)
            rec.content_hash_final = _hash_text(rec.content_final)

    @api.depends("status")
    def _compute_color(self):
        # Kanban colors: pending amber, approved green, updated blue, skipped grey, rejected red
        palette = {
            "draft": 0,
            "pending_review": 3,
            "approved": 10,
            "updated": 4,
            "skipped": 8,
            "rejected_interp": 1,
        }
        for rec in self:
            rec.color = palette.get(rec.status, 0)

    def _create_version_snapshot(self, event="manual", note=False):
        """Append immutable version row and bump section.version."""
        self.ensure_one()
        Version = self.env["copywriting.section.version"].sudo()
        next_version = max(self.version_ids.mapped("version") or [0]) + 1
        Version.create(
            {
                "section_id": self.id,
                "version": next_version,
                "content_final": self.content_final,
                "status": self.status,
                "event": event,
                "user_id": self.env.user.id,
                "note": note or False,
            }
        )
        super(CopywritingSection, self).write({"version": next_version})
        return next_version

    def action_accept_suggestion(self):
        for rec in self:
            super(CopywritingSection, rec).write(
                {
                    "content_final": rec.content_suggestion or rec.content_final or "",
                    "status": "approved",
                }
            )
            rec._create_version_snapshot(event="accept")
        return True

    def action_set_final_updated(self):
        """Call after operator edits content_final in UI."""
        for rec in self:
            super(CopywritingSection, rec).write({"status": "updated"})
            rec._create_version_snapshot(event="edit")
        return True

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, "%s [%s]" % (rec.name, rec.anchor_key)))
        return result
