from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    amount_commission = fields.Float(
        string="Commission Amount",
        readonly=True,
    )

    is_agent = fields.Boolean(
        string="Is Agent",
        related="partner_id.is_agent",
        readonly=True,
    )

    def _select(self):
        return super()._select() + (
            ", sum(l.amount_commission / COALESCE(cr.rate, 1.0)) "
            + "as amount_commission"
        )
