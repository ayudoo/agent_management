from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"
    _name = "product.template"

    commissionable = fields.Boolean(
        string="Commissionable",
        default=True,
        tracking=True,
    )

    @api.onchange("sale_ok")
    def _update_commissionable(self):
        if not self.sale_ok:
            self.commissionable = False


class ProductProduct(models.Model):
    _inherit = "product.product"
    _name = "product.product"

    @api.model
    def _add_missing_default_values(self, values):
        defaults = super()._add_missing_default_values(values)
        if "commissionable" not in values:
            if not defaults.get("sale_ok", False):
                defaults["commissionable"] = False
            else:
                defaults["commissionable"] = True
        return defaults
