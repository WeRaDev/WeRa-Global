# -*- coding: utf-8 -*-
import base64
import csv
import io
import json

from odoo import fields, models
from odoo.exceptions import UserError


class MatrixImportWizard(models.TransientModel):
    _name = "copywriting.matrix.import.wizard"
    _description = "Import Content Matrix"

    import_format = fields.Selection(
        [("json", "JSON"), ("csv", "CSV")],
        default="json",
        required=True,
    )
    data_file = fields.Binary(string="File")
    data_filename = fields.Char()
    data_text = fields.Text(string="Or paste content")
    result_log = fields.Text(readonly=True)

    def _read_payload(self):
        self.ensure_one()
        if self.data_file:
            raw = base64.b64decode(self.data_file)
            return raw.decode("utf-8")
        if self.data_text:
            return self.data_text
        raise UserError("Provide a file or paste content.")

    def action_import(self):
        self.ensure_one()
        payload = self._read_payload()
        if self.import_format == "json":
            log = self._import_json(payload)
        else:
            log = self._import_csv(payload)
        self.result_log = log
        return {
            "type": "ir.actions.act_window",
            "res_model": self._name,
            "view_mode": "form",
            "res_id": self.id,
            "target": "new",
        }

    def _import_json(self, payload):
        try:
            data = json.loads(payload)
        except json.JSONDecodeError as err:
            raise UserError("Invalid JSON: %s" % err) from err
        Website = self.env["copywriting.website"]
        Page = self.env["copywriting.page"]
        Section = self.env["copywriting.section"]
        wdata = data.get("website") or {}
        code = wdata.get("code") or "default"
        website = Website.search([("code", "=", code)], limit=1)
        vals_w = {
            "name": wdata.get("name") or code,
            "code": code,
            "base_url": wdata.get("base_url") or False,
            "executive_summary": wdata.get("executive_summary") or False,
        }
        if wdata.get("website_id"):
            vals_w["website_id"] = int(wdata["website_id"])
        elif self.env["website"].search([], limit=1):
            vals_w.setdefault("website_id", self.env["website"].search([], limit=1).id)
        if website:
            website.write(vals_w)
        else:
            website = Website.create(vals_w)
        pages_n = sections_n = 0
        for pdata in data.get("pages") or []:
            url = pdata.get("url") or "/"
            page = Page.search([("website_id", "=", website.id), ("url", "=", url)], limit=1)
            pvals = {
                "website_id": website.id,
                "name": pdata.get("name") or url,
                "url": url,
                "sequence": int(pdata.get("sequence") or 10),
                "analysis_html": pdata.get("analysis_html") or False,
                "guidelines_html": pdata.get("guidelines_html") or False,
                "status": pdata.get("status") or "todo",
            }
            if page:
                page.write(pvals)
            else:
                page = Page.create(pvals)
            pages_n += 1
            for sdata in pdata.get("sections") or []:
                anchor = sdata.get("anchor_key")
                if not anchor:
                    continue
                lang = sdata.get("lang") or "en_US"
                section = Section.search(
                    [
                        ("page_id", "=", page.id),
                        ("anchor_key", "=", anchor),
                        ("lang", "=", lang),
                    ],
                    limit=1,
                )
                svals = {
                    "page_id": page.id,
                    "name": sdata.get("name") or anchor,
                    "anchor_key": anchor,
                    "lang": lang,
                    "sequence": int(sdata.get("sequence") or 10),
                    "role": sdata.get("role") or "other",
                    "content_current": sdata.get("content_current") or False,
                    "content_interpretation": sdata.get("content_interpretation") or False,
                    "content_suggestion": sdata.get("content_suggestion") or False,
                    "content_final": sdata.get("content_final") or False,
                    "status": sdata.get("status") or "pending_review",
                    "apply_method": sdata.get("apply_method") or "manual_checklist",
                    "apply_target": sdata.get("apply_target") or False,
                    "dom_id": (sdata.get("dom_id") or "").strip() or False,
                }
                if section:
                    # avoid version spam on import
                    section.write({k: v for k, v in svals.items() if k != "page_id"})
                else:
                    section = Section.create(svals)
                    if section.content_final:
                        section._create_version_snapshot(event="import")
                sections_n += 1
        return "JSON import OK: website=%s pages=%s sections=%s" % (
            website.code,
            pages_n,
            sections_n,
        )

    def _import_csv(self, payload):
        reader = csv.DictReader(io.StringIO(payload))
        if not reader.fieldnames:
            raise UserError("CSV has no header.")
        # Group by website/page then reuse JSON path
        websites = {}
        for row in reader:
            code = (row.get("website_code") or "default").strip()
            w = websites.setdefault(
                code,
                {
                    "website": {
                        "code": code,
                        "name": code,
                        "base_url": row.get("base_url") or "",
                    },
                    "pages": {},
                },
            )
            url = (row.get("page_url") or "/").strip()
            page = w["pages"].setdefault(
                url,
                {
                    "url": url,
                    "name": (row.get("page_name") or url).strip(),
                    "sequence": int(row.get("page_sequence") or 10),
                    "sections": [],
                },
            )
            page["sections"].append(
                {
                    "anchor_key": (row.get("anchor_key") or "").strip(),
                    "name": (row.get("name") or row.get("anchor_key") or "").strip(),
                    "lang": (row.get("lang") or "en_US").strip(),
                    "sequence": int(row.get("sequence") or 10),
                    "role": (row.get("role") or "other").strip(),
                    "content_current": row.get("content_current") or "",
                    "content_interpretation": row.get("content_interpretation") or "",
                    "content_suggestion": row.get("content_suggestion") or "",
                    "content_final": row.get("content_final") or "",
                    "status": (row.get("status") or "pending_review").strip(),
                    "apply_method": (row.get("apply_method") or "manual_checklist").strip(),
                    "apply_target": row.get("apply_target") or "",
                    "dom_id": (row.get("dom_id") or "").strip(),
                }
            )
        logs = []
        for code, blob in websites.items():
            data = {
                "website": blob["website"],
                "pages": list(blob["pages"].values()),
            }
            logs.append(self._import_json(json.dumps(data)))
        return "\n".join(logs)
