from odoo import models

from odoo.addons.incity_community_shim.hooks import (
    ensure_offline_template_icon,
    ensure_snippet_view_groups,
)


class IrUiView(models.Model):
    _inherit = "ir.ui.view"

    def _handle_visibility(self, do_raise=True):
        # SaaS dumps store visibility='public' which is truthy and incorrectly
        # routes into private access checks on community. Treat as public.
        if self.visibility in ("public", "Public", ""):
            return True
        return super()._handle_visibility(do_raise=do_raise)

    def _register_hook(self):
        super()._register_hook()
        try:
            ensure_snippet_view_groups(self.env)
            ensure_offline_template_icon(self.env)
        except Exception:
            pass
