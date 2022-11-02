from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = ["agent_management.commission.mixin", "sale.order"]
    _name = "sale.order"

    @api.onchange('partner_id')
    def _br_onchange_partner_id(self):
        super()._br_onchange_partner_id()
        # this method is called in website logic, i.e. after login
        if self.agent_commission != self.agent_id.agent_commission:
            self._set_agent_commission()

    @api.depends("order_line.price_subtotal", "order_line.commissionable")
    def _compute_amount_commission_base(self):
        for order in self:
            if order.agent_id:
                amount_commission_base = sum(
                    line.price_subtotal
                    for line in order.order_line
                    if line.commissionable
                )
                order.amount_commission_base = order.pricelist_id.currency_id.round(
                    amount_commission_base
                )

    @api.depends("order_line.amount_commission")
    def _compute_amount_commission(self):
        for record in self:
            if record.agent_id:
                amount_commission = sum(
                    line.amount_commission for line in record.order_line
                )
                record.amount_commission = amount_commission

    def _get_lines(self):
        return self.order_line


class SaleOrderLine(models.Model):
    _inherit = ["agent_management.commission.line.mixin", "sale.order.line"]
    _name = "sale.order.line"

    agent_commission = fields.Float(
        digits=(3, 2),
        string="Commission",
        help="The commission for this document",
        group_operator="avg",
        related="order_id.agent_commission",
    )

    # TODO switch to use prepare invoice line
    # def _prepare_invoice_line(self, **optional_values):
