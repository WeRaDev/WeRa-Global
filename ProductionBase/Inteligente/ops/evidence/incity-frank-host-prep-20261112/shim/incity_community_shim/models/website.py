from odoo import models


class Website(models.Model):
    _inherit = "website"

    def _is_tracking_enabled(self, *args, **kwargs):
        # Dump QWeb may call with extra args; community may differ.
        return False
