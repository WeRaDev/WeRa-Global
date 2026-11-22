from odoo import api, fields, models


class WebsitePage(models.Model):
    _inherit = "website.page"

    # SaaS dump layout breadcrumbs expect these fields.
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
    )

    @api.depends("parent_id", "parent_id.parent_ids")
    def _compute_parent_ids(self):
        for page in self:
            ancestors = self.env["website.page"]
            current = page.parent_id
            # Guard against cycles in bad data.
            seen = set()
            while current and current.id not in seen:
                ancestors |= current
                seen.add(current.id)
                current = current.parent_id
            page.parent_ids = ancestors
