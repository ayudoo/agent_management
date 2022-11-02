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
    def _compute_can_be_commissionable(self):
        delivery = self.env.ref("delivery.product_category_deliveries", False)
        for record in self:
            if record.can_be_commissionable:
                # you can always unset commissionable
                continue

            if not record.sale_ok:
                record.can_be_commissionable = False
            else:
                if delivery and record.categ_id == delivery:
                    record.can_be_commissionable = False
                else:
                    record.can_be_commissionable = True

    can_be_commissionable = fields.Boolean(
        string="Can Be Commissionable",
        compute=_compute_can_be_commissionable,
    )

    @api.onchange("sale_ok", "categ_id")
    def _update_commissionable(self):
        if not self.can_be_commissionable:
            self.commissionable = False

    # TODO add init method for commissionable


class ProductProduct(models.Model):
    _inherit = "product.product"
    _name = "product.product"

    @api.model
    def _add_missing_default_values(self, values):
        defaults = super()._add_missing_default_values(values)

        template_id = defaults.get("product_tmpl_id", None)

        if template_id:
            product_template = self.env['product.template'].browse(template_id)

            if "commissionable" not in values:
                if not (product_template.sale_ok or defaults.get("sale_ok", False)):
                    defaults["commissionable"] = False
                else:
                    defaults["commissionable"] = True
        return defaults
