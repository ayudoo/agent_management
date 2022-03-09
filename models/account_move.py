from odoo import models, fields, api


class AccoutMove(models.Model):
    _inherit = ["agent_management.commission.mixin", "account.move"]
    _name = "account.move"

    @api.depends("invoice_origin", "partner_id", "agent_id")
    def _compute_default_agent_commission(self):
        for record in self:
            origin_commission = None
            if record.invoice_origin:
                if record.move_type in ["out_refund", "in_refund"]:
                    origin_commission = self.env["account.move"].search(
                        [["name", "=", self.invoice_origin]]
                    )
                else:
                    origin_commission = self.env["sale.order"].search(
                        [["name", "=", self.invoice_origin]]
                    )

            # Just set to the order's commission if the partner is same
            if origin_commission and origin_commission.partner_id == record.partner_id:
                record.default_agent_commission = origin_commission.agent_commission
            elif record.agent_id:
                record.default_agent_commission = record.agent_id.agent_commission
            else:
                record.default_agent_commission = 0.0

    commissioned = fields.Boolean(
        string="commissioned",
        default=False,
    )

    commission_date = fields.Date(
        string="Date when the commission was approved",
        readonly=True,
    )

    def action_move_approve_commission(self):
        self._approve_commission()

    def _approve_commission(self):
        date_now = fields.Date.context_today(self)
        for record in self:
            if not record.commissioned:
                record.commissioned = True
                record.commission_date = date_now

    def action_invoice_reset_approved_commission(self):
        for record in self:
            if record.commissioned:
                record.commissioned = False
                record.commission_date = None

    @api.depends(
        "invoice_line_ids.price_subtotal",
        "invoice_line_ids.commissionable",
        "currency_id",
        "company_id",
        "move_type",
    )
    def _compute_amount_commission_base(self):
        for record in self:
            if not record.agent_id:
                continue

            amount_commission_base = sum(
                line.price_subtotal
                for line in record.invoice_line_ids
                if line.commissionable is True
            )
            record.amount_commission_base = record._to_invoice_amount(
                amount_commission_base
            )

    @api.depends(
        "invoice_line_ids.amount_commission",
        "agent_commission",
        "currency_id",
        "company_id",
        "move_type",
    )
    def _compute_amount_commission(self):
        for record in self:
            if not record.agent_id:
                return

            amount_commission = sum(
                line.amount_commission
                for line in record.invoice_line_ids
                if line.commissionable is True
            )
            record.amount_commission = record._to_invoice_amount(amount_commission)

    def _to_invoice_amount(self, amount):
        if (
            self.currency_id
            and self.company_id
            and self.currency_id != self.company_id.currency_id
        ):
            currency_id = self.currency_id.with_context(date=self.invoice_date)
            amount = currency_id.compute(amount, self.company_id.currency_id)
        sign = self.move_type in ["in_refund", "out_refund"] and -1 or 1
        return sign * amount

    @api.depends("amount_commission", "commissioned")
    def _compute_approved_commission(self):
        for record in self:
            if record.commissioned:
                record.approved_commission = record.amount_commission
            else:
                record.approved_commission = 0.0

    approved_commission = fields.Monetary(
        string="Approved Commission",
        compute=_compute_approved_commission,
        readonly=True,
        store=True,
    )


class AccountMoveLine(models.Model):
    _inherit = ["agent_management.commission.line.mixin", "account.move.line"]
    _name = "account.move.line"

    @api.onchange("product_id")
    def _set_commissionable(self, update_existing=False):
        for record in self:
            if record.can_toggle_commissionable:
                if hasattr(record, "sale_line_ids") and len(record.sale_line_ids):
                    record.commissionable = record.sale_line_ids.commissionable
                elif record.product_id:
                    if not record.product_id.commissionable:
                        record.commissionable = False
                    elif update_existing or isinstance(record.id, models.NewId):
                        record.commissionable = True

    @api.depends("move_id.agent_commission")
    def _compute_agent_commission(self):
        for record in self:
            record.agent_commission = record.move_id.agent_commission

    agent_commission = fields.Float(
        digits=(3, 2),
        string="Commission",
        help="The commission for this document",
        group_operator="avg",
        related="move_id.agent_commission",
    )
