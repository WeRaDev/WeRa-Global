# -*- coding: utf-8 -*-
import base64
import csv
import io
import json

from odoo import fields, models
from odoo.exceptions import UserError


class MatrixExportWizard(models.TransientModel):
    _name = "copywriting.matrix.export.wizard"
    _description = "Export Content Matrix"

    website_id = fields.Many2one("copywriting.website", required=True)
    export_format = fields.Selection(
        [("json", "JSON"), ("csv", "CSV")],
        default="json",
        required=True,
    )
    status_filter = fields.Selection(
        [
            ("all", "All"),
            ("pending_review", "Pending Review"),
            ("approved", "Approved"),
            ("updated", "Updated"),
        ],
        default="all",
        required=True,
    )
    data_file = fields.Binary(readonly=True)
    data_filename = fields.Char(readonly=True)

    def action_export(self):
        self.ensure_one()
        website = self.website_id
        domain = [("website_id", "=", website.id), ("active", "=", True)]
        if self.status_filter != "all":
            domain.append(("status", "=", self.status_filter))
        sections = self.env["copywriting.section"].search(domain, order="page_id, sequence, id")
        if self.export_format == "csv":
            content, filename = self._export_csv(website, sections)
        else:
            content, filename = self._export_json(website, sections)
        self.write(
            {
                "data_file": base64.b64encode(content.encode("utf-8")),
                "data_filename": filename,
            }
        )
        return {
            "type": "ir.actions.act_window",
            "res_model": self._name,
            "view_mode": "form",
            "res_id": self.id,
            "target": "new",
        }

    def _export_csv(self, website, sections):
        buf = io.StringIO()
        fieldnames = [
            "website_code",
            "page_url",
            "page_name",
            "sequence",
            "anchor_key",
            "lang",
            "role",
            "name",
            "content_current",
            "content_interpretation",
            "content_suggestion",
            "content_final",
            "status",
            "apply_method",
            "apply_target",
            "dom_id",
        ]
        writer = csv.DictWriter(buf, fieldnames=fieldnames)
        writer.writeheader()
        for s in sections:
            writer.writerow(
                {
                    "website_code": website.code,
                    "page_url": s.page_id.url,
                    "page_name": s.page_id.name,
                    "sequence": s.sequence,
                    "anchor_key": s.anchor_key,
                    "lang": s.lang,
                    "role": s.role,
                    "name": s.name,
                    "content_current": s.content_current or "",
                    "content_interpretation": s.content_interpretation or "",
                    "content_suggestion": s.content_suggestion or "",
                    "content_final": s.content_final or "",
                    "status": s.status,
                    "apply_method": s.apply_method,
                    "apply_target": s.apply_target or "",
                    "dom_id": s.dom_id or "",
                }
            )
        return buf.getvalue(), "%s_matrix.csv" % website.code

    def _export_json(self, website, sections):
        pages = {}
        for s in sections:
            p = s.page_id
            blob = pages.setdefault(
                p.id,
                {
                    "url": p.url,
                    "name": p.name,
                    "sequence": p.sequence,
                    "analysis_html": p.analysis_html or "",
                    "guidelines_html": p.guidelines_html or "",
                    "status": p.status,
                    "sections": [],
                },
            )
            blob["sections"].append(
                {
                    "anchor_key": s.anchor_key,
                    "name": s.name,
                    "lang": s.lang,
                    "sequence": s.sequence,
                    "role": s.role,
                    "content_current": s.content_current or "",
                    "content_interpretation": s.content_interpretation or "",
                    "content_suggestion": s.content_suggestion or "",
                    "content_final": s.content_final or "",
                    "status": s.status,
                    "apply_method": s.apply_method,
                    "apply_target": s.apply_target or "",
                    "dom_id": s.dom_id or "",
                }
            )
        data = {
            "website": {
                "code": website.code,
                "name": website.name,
                "base_url": website.base_url or "",
                "executive_summary": website.executive_summary or "",
                "website_id": website.website_id.id if website.website_id else False,
            },
            "pages": list(pages.values()),
        }
        return json.dumps(data, ensure_ascii=False, indent=2), "%s_matrix.json" % website.code
