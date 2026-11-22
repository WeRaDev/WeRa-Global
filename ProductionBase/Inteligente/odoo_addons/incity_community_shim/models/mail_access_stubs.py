from odoo import api, fields, models


class MailActivity(models.Model):
    _inherit = "mail.activity"

    # Enterprise dump ir.rules reference these; community has no columns.
    res_access_read = fields.Boolean(compute="_compute_res_access", default=True)
    res_access_write = fields.Boolean(compute="_compute_res_access", default=True)
    res_access_create = fields.Boolean(compute="_compute_res_access", default=True)
    res_access_unlink = fields.Boolean(compute="_compute_res_access", default=True)

    def _compute_res_access(self):
        for rec in self:
            rec.res_access_read = True
            rec.res_access_write = True
            rec.res_access_create = True
            rec.res_access_unlink = True


class MailMessage(models.Model):
    _inherit = "mail.message"

    res_access_read = fields.Boolean(compute="_compute_res_access", default=True)
    res_access_write = fields.Boolean(compute="_compute_res_access", default=True)
    res_access_create = fields.Boolean(compute="_compute_res_access", default=True)
    res_access_unlink = fields.Boolean(compute="_compute_res_access", default=True)

    def _compute_res_access(self):
        for rec in self:
            rec.res_access_read = True
            rec.res_access_write = True
            rec.res_access_create = True
            rec.res_access_unlink = True


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    res_access_read = fields.Boolean(compute="_compute_res_access", default=True)
    res_access_write = fields.Boolean(compute="_compute_res_access", default=True)

    def _compute_res_access(self):
        for rec in self:
            rec.res_access_read = True
            rec.res_access_write = True
