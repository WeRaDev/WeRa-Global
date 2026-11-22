# -*- coding: utf-8 -*-
import logging
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from markupsafe import Markup

from odoo import api, fields, models
from odoo.exceptions import UserError

from .text_utils import (
    build_live_corpus,
    hash_text,
    normalize_text,
    text_matches,
)

_logger = logging.getLogger(__name__)

FETCH_TIMEOUT = 30
USER_AGENT = "InteligenteContentMatrixVerify/1.0 (+https://www.inteligente.site)"


class CopywritingVerifyRun(models.Model):
    _name = "copywriting.verify.run"
    _description = "Content Matrix Verify Run"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "id desc"

    name = fields.Char(compute="_compute_name", store=True)
    website_id = fields.Many2one(
        "copywriting.website", required=True, ondelete="cascade", index=True
    )
    page_ids = fields.Many2many(
        "copywriting.page",
        "copywriting_verify_run_page_rel",
        "run_id",
        "page_id",
        string="Pages scope",
        help="Empty = all active pages of the website",
    )
    user_id = fields.Many2one(
        "res.users",
        required=True,
        default=lambda self: self.env.user,
        ondelete="restrict",
    )
    date_run = fields.Datetime(readonly=True)
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
    compare_to = fields.Selection(
        [
            ("final_then_current", "Final, else current"),
            ("final_only", "Final only"),
            ("current_only", "Current only"),
        ],
        default="final_then_current",
        required=True,
        help="Which matrix text to treat as expected on the live page",
    )
    line_ids = fields.One2many(
        "copywriting.verify.line", "run_id", string="Lines", copy=False
    )
    log_text = fields.Text(readonly=True)
    summary_html = fields.Html(readonly=True)
    count_ok = fields.Integer(readonly=True)
    count_drift = fields.Integer(readonly=True)
    count_missing = fields.Integer(readonly=True)
    count_orphan = fields.Integer(readonly=True)
    count_error = fields.Integer(readonly=True)
    count_pages = fields.Integer(readonly=True)

    def get_base_url(self):
        self.ensure_one()
        base = (self.website_id.base_url or "").rstrip("/") if self.website_id else ""
        if base:
            return base
        return self.env["ir.config_parameter"].sudo().get_param("web.base.url") or ""

    @api.depends("website_id", "date_run", "state")
    def _compute_name(self):
        for rec in self:
            parts = [
                "verify",
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

    def _public_url(self, page):
        self.ensure_one()
        base = (self.website_id.base_url or "").rstrip("/")
        if not base:
            raise UserError(
                "Set Public Base URL on the matrix website before running verify."
            )
        path = page.url or "/"
        if not path.startswith("/"):
            path = "/" + path
        if path == "/":
            return base + "/"
        return base + path

    def _fetch_html(self, url):
        req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html"})
        with urlopen(req, timeout=FETCH_TIMEOUT) as resp:
            charset = resp.headers.get_content_charset() or "utf-8"
            raw = resp.read()
            status = getattr(resp, "status", 200)
        try:
            html = raw.decode(charset, errors="replace")
        except LookupError:
            html = raw.decode("utf-8", errors="replace")
        return status, html

    def _expected_texts(self, section):
        """Return list of (label, text) candidates in priority order."""
        self.ensure_one()
        finals = (section.content_final or "").strip()
        currents = (section.content_current or "").strip()
        if self.compare_to == "final_only":
            return [("final", finals)] if finals else []
        if self.compare_to == "current_only":
            return [("current", currents)] if currents else []
        out = []
        if finals:
            out.append(("final", finals))
        if currents:
            out.append(("current", currents))
        return out

    def action_run_verify(self):
        for rec in self:
            rec._run_verify()
        return True

    def _run_verify(self):
        self.ensure_one()
        if not self.website_id:
            raise UserError("Website is required.")
        pages = self._scope_pages()
        if not pages:
            raise UserError("No active pages in scope.")

        # Clear previous lines
        self.line_ids.unlink()

        Line = self.env["copywriting.verify.line"]
        log_lines = []
        counters = {
            "ok": 0,
            "drift": 0,
            "missing_matrix": 0,
            "orphan_live": 0,
            "error": 0,
        }
        page_live_norms = {}

        for page in pages:
            url = self._public_url(page)
            log_lines.append("PAGE %s → %s" % (page.name, url))
            try:
                status, html = self._fetch_html(url)
            except HTTPError as exc:
                counters["error"] += 1
                Line.create(
                    {
                        "run_id": self.id,
                        "page_id": page.id,
                        "url": url,
                        "result": "error",
                        "http_status": exc.code,
                        "note": "HTTP error: %s" % exc,
                    }
                )
                log_lines.append("  ERROR http %s" % exc)
                continue
            except URLError as exc:
                counters["error"] += 1
                Line.create(
                    {
                        "run_id": self.id,
                        "page_id": page.id,
                        "url": url,
                        "result": "error",
                        "note": "URL error: %s" % exc.reason,
                    }
                )
                log_lines.append("  ERROR url %s" % exc.reason)
                continue
            except Exception as exc:  # noqa: BLE001 — surface any fetch failure
                counters["error"] += 1
                Line.create(
                    {
                        "run_id": self.id,
                        "page_id": page.id,
                        "url": url,
                        "result": "error",
                        "note": "Fetch failed: %s" % exc,
                    }
                )
                log_lines.append("  ERROR %s" % exc)
                continue

            # Page-level body+meta corpus (section may refine further for meta roles)
            page_corpus, page_corpus_kind = build_live_corpus(html)
            page_live_norms[page.id] = page_corpus
            live_hash = hash_text(page_corpus)
            log_lines.append(
                "  fetched status=%s corpus=%s chars=%s hash=%s"
                % (status, page_corpus_kind, len(page_corpus), live_hash[:12])
            )

            matched_needles = set()
            sections = page.section_ids.filtered("active").sorted(
                lambda s: (s.sequence, s.id)
            )
            for section in sections:
                candidates = self._expected_texts(section)
                if not candidates:
                    Line.create(
                        {
                            "run_id": self.id,
                            "page_id": page.id,
                            "section_id": section.id,
                            "url": url,
                            "result": "missing_matrix",
                            "http_status": status,
                            "live_hash": live_hash,
                            "note": "No final/current text on section to compare",
                        }
                    )
                    counters["missing_matrix"] += 1
                    log_lines.append(
                        "  MISSING %s — empty matrix text" % section.anchor_key
                    )
                    continue

                # Meta sections search meta tags first; others use body (+meta backup)
                corpus, corpus_kind = build_live_corpus(
                    html, role=section.role, anchor_key=section.anchor_key
                )

                matched_label = False
                matched_text = ""
                expected_hash = ""
                match_mode = "none"
                for label, text in candidates:
                    h = hash_text(text)
                    ok_match, mode = text_matches(corpus, text, multipart=True)
                    if ok_match:
                        matched_label = label
                        matched_text = text
                        expected_hash = h
                        match_mode = mode
                        matched_needles.add(normalize_text(text))
                        break
                    if not expected_hash:
                        expected_hash = h
                        matched_text = text

                if matched_label == "final" or (
                    matched_label == "current" and self.compare_to == "current_only"
                ):
                    result = "ok"
                elif matched_label == "current" and any(
                    lab == "final" for lab, _ in candidates
                ):
                    # Final expected but only current found on live
                    result = "drift"
                elif matched_label:
                    result = "ok"
                else:
                    result = "missing_matrix"

                counters[result] = counters.get(result, 0) + 1
                if matched_label:
                    note = "Matched %s via %s (%s)" % (
                        matched_label,
                        match_mode,
                        corpus_kind,
                    )
                else:
                    note = (
                        "Matrix text not found in live corpus (%s); "
                        "tried exact, multipart, and token coverage"
                        % corpus_kind
                    )
                Line.create(
                    {
                        "run_id": self.id,
                        "page_id": page.id,
                        "section_id": section.id,
                        "url": url,
                        "result": result,
                        "http_status": status,
                        "expected_label": matched_label
                        or (candidates[0][0] if candidates else False),
                        "expected_text": matched_text
                        or (candidates[0][1] if candidates else False),
                        "expected_hash": expected_hash,
                        "live_hash": live_hash,
                        "note": note,
                    }
                )
                log_lines.append(
                    "  %s %s (%s/%s)"
                    % (
                        result.upper(),
                        section.anchor_key,
                        matched_label or "none",
                        match_mode,
                    )
                )

            # Orphan heuristic: long live page with zero section matches
            if sections and not matched_needles and page_corpus:
                counters["orphan_live"] += 1
                snippet = page_corpus[:240]
                Line.create(
                    {
                        "run_id": self.id,
                        "page_id": page.id,
                        "url": url,
                        "result": "orphan_live",
                        "http_status": status,
                        "live_hash": live_hash,
                        "live_snippet": snippet,
                        "note": (
                            "No matrix section text matched this page; "
                            "live content may be unmapped (orphan)."
                        ),
                    }
                )
                log_lines.append("  ORPHAN page — no section matched live text")

        # State
        if counters["error"] and not (
            counters["ok"] or counters["drift"] or counters["missing_matrix"]
        ):
            state = "error"
        elif counters["error"] or counters["drift"] or counters["missing_matrix"] or counters["orphan_live"]:
            state = "warn"
        else:
            state = "ok"

        summary = (
            "<p><b>Verify run complete</b> for %s</p>"
            "<ul>"
            "<li>Pages: %s</li>"
            "<li>OK: %s</li>"
            "<li>Drift: %s</li>"
            "<li>Missing (matrix not on live): %s</li>"
            "<li>Orphan live pages: %s</li>"
            "<li>Fetch errors: %s</li>"
            "</ul>"
            % (
                self.website_id.name or self.website_id.code,
                len(pages),
                counters["ok"],
                counters["drift"],
                counters["missing_matrix"],
                counters["orphan_live"],
                counters["error"],
            )
        )
        self.write(
            {
                "date_run": fields.Datetime.now(),
                "state": state,
                "log_text": "\n".join(log_lines),
                "summary_html": summary,
                "count_ok": counters["ok"],
                "count_drift": counters["drift"],
                "count_missing": counters["missing_matrix"],
                "count_orphan": counters["orphan_live"],
                "count_error": counters["error"],
                "count_pages": len(pages),
            }
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

    def action_export_log(self):
        """Return log text in a simple notification (download via chatter)."""
        self.ensure_one()
        if not self.log_text:
            raise UserError("No log yet. Run verify first.")
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Verify log ready",
                "message": "Open the Log tab or chatter to copy the full report.",
                "type": "success",
                "sticky": False,
            },
        }


class CopywritingVerifyLine(models.Model):
    _name = "copywriting.verify.line"
    _description = "Content Matrix Verify Line"
    _order = "id"

    run_id = fields.Many2one(
        "copywriting.verify.run", required=True, ondelete="cascade", index=True
    )
    page_id = fields.Many2one("copywriting.page", ondelete="set null", index=True)
    section_id = fields.Many2one("copywriting.section", ondelete="set null", index=True)
    url = fields.Char()
    result = fields.Selection(
        [
            ("ok", "OK"),
            ("drift", "Drift"),
            ("missing_matrix", "Missing on live"),
            ("orphan_live", "Orphan live"),
            ("error", "Error"),
        ],
        required=True,
        index=True,
    )
    http_status = fields.Integer()
    expected_label = fields.Char()
    expected_text = fields.Text()
    expected_hash = fields.Char()
    live_hash = fields.Char()
    live_snippet = fields.Text()
    note = fields.Text()
    anchor_key = fields.Char(related="section_id.anchor_key", store=True)
