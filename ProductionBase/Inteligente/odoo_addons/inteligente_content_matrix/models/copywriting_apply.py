# -*- coding: utf-8 -*-
"""Apply runs: v1 is manual checklist only (no silent live HTML rewrite)."""

from markupsafe import Markup, escape

from odoo import api, fields, models
from odoo.exceptions import UserError

# Optional future mappings. Keys: "{website_code}:{anchor_key}"
APPLY_REGISTRY = {
    # Example reserved mapping — still checklist until explicitly automated:
    "incity:home.footer.about": {
        "method": "manual_checklist",
        "note": "Paste into Website Editor footer about block",
    },
}


class CopywritingApplyRun(models.Model):
    _name = "copywriting.apply.run"
    _description = "Content Matrix Apply Run"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "id desc"

    name = fields.Char(compute="_compute_name", store=True)
    website_id = fields.Many2one(
        "copywriting.website", required=True, ondelete="cascade", index=True
    )
    page_ids = fields.Many2many(
        "copywriting.page",
        "copywriting_apply_run_page_rel",
        "run_id",
        "page_id",
        string="Pages scope",
        help="Empty = all active pages",
    )
    user_id = fields.Many2one(
        "res.users",
        required=True,
        default=lambda self: self.env.user,
        ondelete="restrict",
    )
    date_run = fields.Datetime(readonly=True)
    dry_run = fields.Boolean(
        default=True,
        help="Dry-run only builds the checklist. Uncheck + Manager confirm to mark lines applied (still no auto HTML rewrite in v1).",
    )
    manager_confirm = fields.Boolean(
        string="I confirm manual apply",
        help="Required when dry_run is disabled. Affirms operator will paste finals carefully.",
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("ok", "OK"),
            ("warn", "Warnings"),
            ("error", "Error"),
        ],
        default="draft",
        required=True,
        tracking=True,
    )
    line_ids = fields.One2many(
        "copywriting.apply.line", "run_id", string="Lines", copy=False
    )
    checklist_html = fields.Html(readonly=True)
    log_text = fields.Text(readonly=True)
    count_total = fields.Integer(readonly=True)
    count_checklist = fields.Integer(readonly=True)
    count_skipped = fields.Integer(readonly=True)
    count_blocked = fields.Integer(readonly=True)

    def get_base_url(self):
        self.ensure_one()
        base = (self.website_id.base_url or "").rstrip("/") if self.website_id else ""
        if base:
            return base
        return self.env["ir.config_parameter"].sudo().get_param("web.base.url") or ""

    @api.depends("website_id", "date_run", "state", "dry_run")
    def _compute_name(self):
        for rec in self:
            mode = "dry" if rec.dry_run else "apply"
            parts = [
                "apply",
                mode,
                rec.website_id.code or "site",
                fields.Datetime.to_string(rec.date_run) if rec.date_run else "draft",
                rec.state or "draft",
            ]
            rec.name = " / ".join(parts)

    def _scope_pages(self):
        self.ensure_one()
        if self.page_ids:
            return self.page_ids.filtered("active").sorted(lambda p: (p.sequence, p.id))
        return self.website_id.page_ids.filtered("active").sorted(
            lambda p: (p.sequence, p.id)
        )

    def _eligible_sections(self):
        self.ensure_one()
        pages = self._scope_pages()
        sections = pages.mapped("section_ids").filtered(
            lambda s: s.active
            and s.status in ("approved", "updated")
            and s.apply_method != "none"
            and (s.content_final or "").strip()
        )
        return sections.sorted(
            lambda s: (s.page_id.sequence, s.page_id.id, s.sequence, s.id)
        )

    def _resolve_method(self, section):
        key = "%s:%s" % (section.website_id.code or "", section.anchor_key or "")
        reg = APPLY_REGISTRY.get(key) or {}
        method = reg.get("method") or section.apply_method or "manual_checklist"
        note = reg.get("note") or section.apply_target or ""
        return method, note

    def action_build_checklist(self):
        for rec in self:
            rec._build_or_apply(execute=False)
        return True

    def action_run_apply(self):
        for rec in self:
            if rec.dry_run:
                rec._build_or_apply(execute=False)
            else:
                if not self.env.user.has_group(
                    "inteligente_content_matrix.group_manager"
                ):
                    raise UserError("Only managers can run non-dry apply.")
                if not rec.manager_confirm:
                    raise UserError(
                        "Check “I confirm manual apply” before leaving dry-run."
                    )
                rec._build_or_apply(execute=True)
        return True

    def _build_or_apply(self, execute=False):
        self.ensure_one()
        sections = self._eligible_sections()
        self.line_ids.unlink()
        Line = self.env["copywriting.apply.line"]
        log = []
        checklist_parts = [
            "<h2>Manual apply checklist — %s</h2>"
            % escape(self.website_id.name or self.website_id.code or ""),
            "<p>Mode: <b>%s</b>. v1 never rewrites live HTML automatically. "
            "Paste each Final into the Website Editor (or mapped target).</p>"
            % ("DRY-RUN" if not execute else "EXECUTE (manual mark only)"),
        ]
        counts = {"total": 0, "checklist": 0, "skipped": 0, "blocked": 0}
        current_page = False

        for section in sections:
            counts["total"] += 1
            method, note = self._resolve_method(section)
            page = section.page_id
            if page != current_page:
                if current_page:
                    checklist_parts.append("</ol>")
                current_page = page
                checklist_parts.append(
                    "<h3>%s <code>%s</code></h3>"
                    % (escape(page.name or ""), escape(page.url or ""))
                )
                checklist_parts.append("<ol>")

            if method not in ("manual_checklist", "website_page_field", "ir_ui_view_replace"):
                status = "blocked"
                counts["blocked"] += 1
                msg = "Unknown apply method %s" % method
            elif method in ("website_page_field", "ir_ui_view_replace"):
                # v1: refuse silent automation — force checklist path
                status = "blocked"
                counts["blocked"] += 1
                msg = (
                    "Auto method %s not enabled in v1; use manual_checklist "
                    "(see APPLY_REGISTRY)."
                ) % method
            else:
                status = "done" if execute else "todo"
                counts["checklist"] += 1
                msg = note or "Paste final via Website Editor"
                if execute:
                    section._create_version_snapshot(
                        event="apply", note="manual apply marked on run %s" % self.id
                    )

            Line.create(
                {
                    "run_id": self.id,
                    "section_id": section.id,
                    "page_id": page.id,
                    "apply_method": method,
                    "apply_target": note or section.apply_target,
                    "content_final": section.content_final,
                    "status": status,
                    "note": msg,
                }
            )
            log.append(
                "%s | %s | %s | %s"
                % (status, section.anchor_key, method, (section.content_final or "")[:80])
            )
            checklist_parts.append(
                "<li><b>%s</b> [<code>%s</code>] "
                "method=%s<br/>"
                "<pre style=\"white-space:pre-wrap;background:#f6f6f6;padding:8px;\">%s</pre>"
                "%s</li>"
                % (
                    escape(section.name or ""),
                    escape(section.anchor_key or ""),
                    escape(method),
                    escape(section.content_final or ""),
                    ("<i>%s</i>" % escape(msg)) if msg else "",
                )
            )

        if current_page:
            checklist_parts.append("</ol>")

        if not sections:
            checklist_parts.append(
                "<p><i>No eligible sections "
                "(need status approved/updated, apply_method != none, non-empty final).</i></p>"
            )
            counts["skipped"] = 0
            state = "warn"
        elif counts["blocked"] and not counts["checklist"]:
            state = "error"
        elif counts["blocked"]:
            state = "warn"
        else:
            state = "ok"

        html = "\n".join(checklist_parts)
        self.write(
            {
                "date_run": fields.Datetime.now(),
                "state": state,
                "checklist_html": html,
                "log_text": "\n".join(log),
                "count_total": counts["total"],
                "count_checklist": counts["checklist"],
                "count_skipped": counts["skipped"],
                "count_blocked": counts["blocked"],
            }
        )
        summary = (
            "<p><b>Apply run (%s)</b></p>"
            "<ul>"
            "<li>Eligible: %s</li>"
            "<li>Checklist rows: %s</li>"
            "<li>Blocked: %s</li>"
            "</ul>"
            % (
                "execute mark" if execute else "dry-run",
                counts["total"],
                counts["checklist"],
                counts["blocked"],
            )
        )
        partner = self.user_id.partner_id
        if partner:
            self.message_subscribe(partner_ids=partner.ids)
        self.message_post(
            body=Markup(summary),
            message_type="notification",
            subtype_xmlid="mail.mt_note",
        )
        return True


class CopywritingApplyLine(models.Model):
    _name = "copywriting.apply.line"
    _description = "Content Matrix Apply Line"
    _order = "id"

    run_id = fields.Many2one(
        "copywriting.apply.run", required=True, ondelete="cascade", index=True
    )
    section_id = fields.Many2one("copywriting.section", ondelete="set null", index=True)
    page_id = fields.Many2one("copywriting.page", ondelete="set null", index=True)
    anchor_key = fields.Char(related="section_id.anchor_key", store=True)
    apply_method = fields.Char()
    apply_target = fields.Char()
    content_final = fields.Text()
    status = fields.Selection(
        [
            ("todo", "Todo"),
            ("done", "Done"),
            ("blocked", "Blocked"),
            ("skipped", "Skipped"),
        ],
        default="todo",
        required=True,
    )
    note = fields.Text()
