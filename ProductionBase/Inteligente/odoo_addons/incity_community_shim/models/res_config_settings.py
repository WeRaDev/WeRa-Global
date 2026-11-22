from odoo import api, fields, models
from odoo.exceptions import UserError


class ResConfigSettings(models.TransientModel):
    """SaaS dump settings views reference enterprise-only fields."""

    _inherit = "res.config.settings"

    # mail / discuss
    use_tenor_api = fields.Boolean(config_parameter="mail.use_tenor_api")
    use_google_translate_api = fields.Boolean(config_parameter="mail.use_google_translate_api")
    use_call_server = fields.Boolean(config_parameter="mail.use_call_server")

    # mobile / OCN
    enable_ocn = fields.Boolean(config_parameter="mobile.enable_ocn")
    disable_redirect_firebase_dynamic_link = fields.Boolean(
        config_parameter="mobile.disable_redirect_firebase_dynamic_link"
    )

    # maps
    map_box_token = fields.Char(config_parameter="web_map.map_box_token")

    # AI keys
    google_key_enabled = fields.Boolean(config_parameter="ai.google_key_enabled")
    google_key = fields.Char(config_parameter="ai.google_key")
    openai_key_enabled = fields.Boolean(config_parameter="ai.openai_key_enabled")
    openai_key = fields.Char(config_parameter="ai.openai_key")

    # calendar google
    cal_google_disable_auto_videocall_link = fields.Boolean(
        config_parameter="google_calendar.disable_auto_videocall_link"
    )

    def _is_layout_cover_required(self):
        """Snailmail expects legacy web.external_layout_{name} xmlids.

        Some dump/community mixes lack boxed/bold/striped; never crash Settings.
        """
        self.ensure_one()
        try:
            return super()._is_layout_cover_required()
        except (ValueError, UserError, Exception):
            return False

    @api.onchange("external_report_layout_id")
    def _onchange_layout(self):
        try:
            return super()._onchange_layout()
        except Exception:
            # Keep UI usable when layout xmlid/assets are incomplete.
            return None
