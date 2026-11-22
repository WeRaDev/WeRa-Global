# -*- coding: utf-8 -*-
from odoo import fields, models


class CopywritingSectionVersion(models.Model):
    _name = "copywriting.section.version"
    _description = "Content Matrix Section Version"
    _order = "section_id, version desc, id desc"

    section_id = fields.Many2one(
        "copywriting.section", required=True, ondelete="cascade", index=True
    )
    version = fields.Integer(required=True, default=1)
    content_final = fields.Text()
    status = fields.Selection(
        [
            ("draft", "Draft"),
            ("pending_review", "Pending Review"),
            ("approved", "Approved"),
            ("updated", "Updated"),
            ("skipped", "Skipped"),
            ("rejected_interp", "Rejected Interpretation"),
        ],
    )
    event = fields.Selection(
        [
            ("accept", "Accept"),
            ("edit", "Edit"),
            ("import", "Import"),
            ("apply", "Apply"),
            ("manual", "Manual"),
        ],
        default="manual",
    )
    user_id = fields.Many2one("res.users", default=lambda self: self.env.user, ondelete="set null")
    note = fields.Text()
