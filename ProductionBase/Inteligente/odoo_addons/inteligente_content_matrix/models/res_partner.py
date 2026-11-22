# -*- coding: utf-8 -*-
from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.depends("user_ids.manual_im_status", "user_ids.presence_ids.status")
    def _compute_im_status(self):
        super()._compute_im_status()
        bot = self.env.ref(
            "inteligente_content_matrix.partner_matrix_bot", raise_if_not_found=False
        )
        if not bot:
            return
        for partner in self:
            if partner.id == bot.id:
                partner.im_status = "bot"
