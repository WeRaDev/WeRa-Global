# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError


class CopywritingWebsite(models.Model):
    _name = "copywriting.website"
    _description = "Content Matrix Website"
    _order = "name"

    name = fields.Char(required=True)
    code = fields.Char(required=True, index=True)
    website_id = fields.Many2one("website", string="Odoo Website")
    base_url = fields.Char(string="Public Base URL", help="e.g. https://www.invisiblecity.site")
    executive_summary = fields.Html(string="Executive Summary")
    active = fields.Boolean(default=True)
    page_ids = fields.One2many("copywriting.page", "website_id", string="Pages")
    page_count = fields.Integer(compute="_compute_counts")
    section_count = fields.Integer(compute="_compute_counts")
    approved_count = fields.Integer(compute="_compute_counts")
    completion_ratio = fields.Float(compute="_compute_counts", string="Completion")

    _sql_constraints = [
        ("code_uniq", "unique(code)", "Website code must be unique."),
    ]

    @api.depends(
        "page_ids",
        "page_ids.section_ids",
        "page_ids.section_ids.status",
        "page_ids.section_ids.active",
    )
    def _compute_counts(self):
        for rec in self:
            pages = rec.page_ids
            sections = pages.mapped("section_ids").filtered("active")
            rec.page_count = len(pages)
            rec.section_count = len(sections)
            approved = sections.filtered(lambda s: s.status in ("approved", "updated"))
            rec.approved_count = len(approved)
            rec.completion_ratio = (len(approved) / len(sections)) if sections else 0.0

    def action_import_dom_anchor_map(self):
        """Apply dom_id from module seed incity_dom_anchor_map.json (matched by page url + anchor_key)."""
        import json
        import os

        self.ensure_one()
        path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data",
            "seeds",
            "incity_dom_anchor_map.json",
        )
        if not os.path.isfile(path):
            raise UserError("DOM map seed not found: %s" % path)
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        updated = 0
        missing = 0
        Section = self.env["copywriting.section"]
        for page_blob in data.get("pages") or []:
            url = page_blob.get("url") or "/"
            page = self.page_ids.filtered(lambda p, u=url: p.url == u)[:1]
            if not page:
                missing += len(page_blob.get("sections") or [])
                continue
            for sblob in page_blob.get("sections") or []:
                anchor = sblob.get("anchor_key")
                if not anchor:
                    continue
                section = Section.search(
                    [
                        ("page_id", "=", page.id),
                        ("anchor_key", "=", anchor),
                    ],
                    limit=1,
                )
                if not section:
                    missing += 1
                    continue
                dom = (sblob.get("dom_id") or "") or False
                if isinstance(dom, str):
                    dom = dom.strip() or False
                section.dom_id = dom
                updated += 1
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "DOM map imported",
                "message": "Updated %s sections (%s unmatched anchors)." % (updated, missing),
                "type": "success",
                "sticky": False,
            },
        }
