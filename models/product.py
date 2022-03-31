from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"
    _name = "product.template"

    commissionable = fields.Boolean(
        string="Commissionable",
        default=True,
        tracking=True,
    )

    @api.depends("sale_ok", "categ_id")
    def _compute_can_change_commissionable(self):
        delivery = self.env.ref("delivery.product_category_deliveries", False)
        for record in self:
            if record.can_change_commissionable:
                # you can always unset commissionable
                continue

            if not record.sale_ok:
                record.can_change_commissionable = False
            else:
                if delivery and record.categ_id == delivery:
                    record.can_change_commissionable = False
                else:
                    record.can_change_commissionable = True

    can_change_commissionable = fields.Boolean(
        string="Can Change Commissionable",
        compute=_compute_can_change_commissionable,
    )

    @api.onchange("sale_ok", "categ_id")
    def _update_commissionable(self):
        if not self.can_change_commissionable:
            self.commissionable = False

    # TODO add init method for commissionable


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
