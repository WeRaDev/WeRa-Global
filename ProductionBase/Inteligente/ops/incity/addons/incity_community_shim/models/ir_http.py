from odoo import models
from odoo.http import request


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def _frontend_pre_dispatch(cls):
        # Ensure request.lang is a real LangData with string code before cookie set.
        lang = getattr(request, "lang", None)
        code = getattr(lang, "code", None) if lang is not None else None
        if not isinstance(code, str):
            en = request.env["res.lang"]._get_data(code="en_US")
            if not getattr(en, "id", None):
                # fallback via search then id
                rec = request.env["res.lang"].search([("code", "=", "en_US")], limit=1) or request.env["res.lang"].search([("active", "=", True)], limit=1)
                en = request.env["res.lang"]._get_data(id=rec.id) if rec else en
            if getattr(en, "id", None):
                request.lang = en
        super()._frontend_pre_dispatch()

    @classmethod
    def _get_default_lang(cls):
        data = super()._get_default_lang()
        if not isinstance(getattr(data, "code", None), str):
            en = request.env["res.lang"]._get_data(code="en_US")
            if getattr(en, "id", None):
                return en
            rec = request.env["res.lang"].search([("active", "=", True)], limit=1)
            if rec:
                return request.env["res.lang"]._get_data(id=rec.id)
        return data

    def _get_visitor_from_request(self, force_create=False, **kwargs):
        """SaaS QWeb calls visitor helper on ir.http; community has it on website.visitor."""
        Visitor = self.env["website.visitor"]
        try:
            return Visitor._get_visitor_from_request(force_create=force_create)
        except Exception:
            return Visitor.browse()
