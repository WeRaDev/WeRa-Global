# -*- coding: utf-8 -*-
from odoo import api, fields, models


class CopywritingPage(models.Model):
    _name = "copywriting.page"
    _description = "Content Matrix Page"
    _order = "website_id, sequence, id"

    website_id = fields.Many2one(
        "copywriting.website", required=True, ondelete="cascade", index=True
    )
    name = fields.Char(required=True)
    url = fields.Char(required=True, index=True, help="Path only, e.g. / or /contactus")
    sequence = fields.Integer(default=10)
    analysis_html = fields.Html(string="Page Analysis")
    guidelines_html = fields.Html(string="Guidelines")
    status = fields.Selection(
        [
            ("todo", "To Do"),
            ("in_progress", "In Progress"),
            ("done", "Done"),
        ],
        default="todo",
        required=True,
    )
    active = fields.Boolean(default=True)
    section_ids = fields.One2many("copywriting.section", "page_id", string="Sections")
    section_count = fields.Integer(compute="_compute_counts", store=True)
    approved_count = fields.Integer(compute="_compute_counts", store=True)
    completion_ratio = fields.Float(
        compute="_compute_counts", store=True, string="Completion"
    )

    _sql_constraints = [
        (
            "website_url_uniq",
            "unique(website_id, url)",
            "Page URL must be unique per website.",
        ),
    ]

    @api.depends("section_ids", "section_ids.status", "section_ids.active")
    def _compute_counts(self):
        for rec in self:
            sections = rec.section_ids.filtered("active")
            rec.section_count = len(sections)
            approved = sections.filtered(lambda s: s.status in ("approved", "updated"))
            rec.approved_count = len(approved)
            rec.completion_ratio = (len(approved) / len(sections)) if sections else 0.0

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, "%s (%s)" % (rec.name, rec.url)))
        return result
