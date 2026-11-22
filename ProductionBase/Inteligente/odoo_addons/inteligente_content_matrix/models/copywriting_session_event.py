# -*- coding: utf-8 -*-
from odoo import fields, models


class CopywritingSessionEvent(models.Model):
    _name = "copywriting.session.event"
    _description = "Content Matrix Session Event"
    _order = "id desc"

    session_id = fields.Many2one(
        "copywriting.session", required=True, ondelete="cascade", index=True
    )
    section_id = fields.Many2one("copywriting.section", ondelete="set null", index=True)
    step = fields.Selection(
        [
            ("intro", "Intro"),
            ("page_select", "Page select"),
            ("page_intro", "Page intro"),
            ("fact", "Fact"),
            ("interpret", "Interpretation"),
            ("suggest", "Suggestion"),
            ("decide", "Decide"),
            ("page_done", "Page done"),
            ("finish", "Finish"),
            ("pause", "Pause"),
            ("resume", "Resume"),
        ],
        required=True,
    )
    payload_json = fields.Text()
    note = fields.Text()
    user_id = fields.Many2one(
        "res.users", default=lambda self: self.env.user, ondelete="set null"
    )
