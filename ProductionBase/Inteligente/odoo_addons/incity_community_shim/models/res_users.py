from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    # SaaS dump user forms reference session_ids (One2many -> res.session).
    # Community has no sessions app; stub model is provided by saas_stubs.
    session_ids = fields.One2many(
        "res.session",
        "user_id",
        string="User Sessions",
        copy=False,
    )
