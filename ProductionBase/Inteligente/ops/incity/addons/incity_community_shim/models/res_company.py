from odoo import models

class ResCompany(models.Model):
    _inherit = "res.company"
    # no extra fields - dump had incompatible report_tables_id values
