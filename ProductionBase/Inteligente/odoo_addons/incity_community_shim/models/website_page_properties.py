from odoo import api, fields, models


class WebsitePagePropertiesBase(models.TransientModel):
    _inherit = "website.page.properties.base"

    publish_on = fields.Datetime(
        string="Publish on",
        compute="_compute_publish_on",
        inverse="_inverse_publish_on",
    )

    def _get_target_page(self):
        self.ensure_one()
        target = getattr(self, "target_model_id", False)
        if target is not None and getattr(target, "_name", None) == "website.page":
            return target
        return self.env["website.page"]

    @api.depends("target_model_id")
    def _compute_publish_on(self):
        for rec in self:
            page = rec._get_target_page()
            if page:
                rec.publish_on = (
                    getattr(page, "publish_on", False)
                    or getattr(page, "date_publish", False)
                )
            else:
                rec.publish_on = False

    def _inverse_publish_on(self):
        for rec in self:
            page = rec._get_target_page()
            if not page:
                continue
            vals = {"date_publish": rec.publish_on}
            if "publish_on" in page._fields:
                vals["publish_on"] = rec.publish_on
            page.write(vals)


class WebsitePageProperties(models.TransientModel):
    _inherit = "website.page.properties"

    parent_id = fields.Many2one(
        "website.page",
        string="Parent Page",
        compute="_compute_parent_fields",
        inverse="_inverse_parent_id",
    )
    has_parent_page = fields.Boolean(
        string="Has parent page",
        compute="_compute_parent_fields",
    )
    # publish_on inherited via base compute if MRO picks it up; redefine for safety
    publish_on = fields.Datetime(
        string="Publish on",
        compute="_compute_publish_on",
        inverse="_inverse_publish_on",
    )

    def _get_target_page(self):
        self.ensure_one()
        target = self.target_model_id
        if target is not None and getattr(target, "_name", None) == "website.page":
            return target
        return self.env["website.page"]

    @api.depends("target_model_id")
    def _compute_parent_fields(self):
        for rec in self:
            page = rec._get_target_page()
            rec.parent_id = page.parent_id if page else False
            rec.has_parent_page = bool(page and page.parent_id)

    def _inverse_parent_id(self):
        for rec in self:
            page = rec._get_target_page()
            if page:
                page.parent_id = rec.parent_id

    @api.depends("target_model_id")
    def _compute_publish_on(self):
        for rec in self:
            page = rec._get_target_page()
            if page:
                rec.publish_on = (
                    getattr(page, "publish_on", False)
                    or getattr(page, "date_publish", False)
                )
            else:
                rec.publish_on = False

    def _inverse_publish_on(self):
        for rec in self:
            page = rec._get_target_page()
            if not page:
                continue
            vals = {"date_publish": rec.publish_on}
            if "publish_on" in page._fields:
                vals["publish_on"] = rec.publish_on
            page.write(vals)
