"""Minimal stubs for SaaS-only models left in dump metadata."""
from odoo import fields, models


class ResSession(models.Model):
    _name = "res.session"
    _description = "User Session (community stub)"
    _order = "id desc"

    session_identifier = fields.Char(index=True)
    user_id = fields.Many2one("res.users", index=True, ondelete="cascade")
    last_activity = fields.Datetime(index=True)
    revoked = fields.Boolean(default=False)


class DiscussCategory(models.Model):
    _name = "discuss.category"
    _description = "Discuss Category (community stub)"
    _order = "sequence, id"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
