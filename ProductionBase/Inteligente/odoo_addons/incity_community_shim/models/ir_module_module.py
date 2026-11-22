# -*- coding: utf-8 -*-
"""SaaS dump Apps views reference enterprise-only fields. Stub them on CE."""
from odoo import fields, models


class IrModuleModule(models.Model):
    _inherit = "ir.module.module"

    # Referenced by base_import_module Apps inherit / SaaS form arch
    total_lines_of_code = fields.Integer(
        string="Lines of Code",
        default=0,
        help="SaaS/enterprise leftover; unused on community.",
    )
    iap_paid_service = fields.Boolean(
        string="IAP Paid Service",
        default=False,
        help="SaaS/enterprise leftover; unused on community.",
    )
