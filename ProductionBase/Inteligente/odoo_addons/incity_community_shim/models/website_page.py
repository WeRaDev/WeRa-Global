from odoo import api, fields, models


class WebsitePage(models.Model):
    _inherit = "website.page"

    # SaaS dump layout breadcrumbs expect hierarchy fields.
    parent_id = fields.Many2one(
        "website.page",
        string="Parent Page",
        index=True,
        ondelete="set null",
    )
    parent_ids = fields.Many2many(
        "website.page",
        string="Ancestor Pages",
        compute="_compute_parent_ids",
        recursive=True,
    )

    # SaaS website page list/form views use publish_on; community uses date_publish.
    # Column may already exist in restored dump DB.
    publish_on = fields.Datetime(
        string="Publish on",
        help="Scheduled publish datetime from SaaS dump views.",
    )

    @api.depends("parent_id", "parent_id.parent_ids")
    def _compute_parent_ids(self):
        for page in self:
            ancestors = self.env["website.page"]
            current = page.parent_id
            seen = set()
            while current and current.id not in seen:
                ancestors |= current
                seen.add(current.id)
                current = current.parent_id
            page.parent_ids = ancestors

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("publish_on") and not vals.get("date_publish"):
                vals["date_publish"] = vals["publish_on"]
            if vals.get("date_publish") and not vals.get("publish_on"):
                vals["publish_on"] = vals["date_publish"]
        return super().create(vals_list)

    def write(self, vals):
        if vals.get("publish_on") and "date_publish" not in vals:
            vals = dict(vals, date_publish=vals["publish_on"])
        if vals.get("date_publish") and "publish_on" not in vals:
            vals = dict(vals, publish_on=vals["date_publish"])
        return super().write(vals)
