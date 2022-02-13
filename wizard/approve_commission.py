from odoo import api, fields, models


class AccountMoveApproveCommission(models.TransientModel):
    _name = "account.move.approve_commission"
    _description = "Approve the commission of the selected invoices"

    def _get_active_ids(self):
        return self._context.get("active_ids", [])

    invalid_invoices = fields.Integer(
        string="Invalid Invoices",
        help="Draft and cancelled invoices.",
        store=False,
        readonly=True,
        default=0,
    )
    approved_commissions = fields.Integer(
        string="Approved Commissions", store=False, readonly=True, default=0
    )
    commissions_to_approve = fields.Integer(
        string="Commissions to Approve", store=False, readonly=True, default=0
    )

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        active_ids = self._get_active_ids()

        for count in [
            "invalid_invoices",
            "approved_commissions",
            "commissions_to_approve",
        ]:
            if count not in defaults:
                defaults[count] = 0

        for record in self.env["account.move"].browse(active_ids):
            if record.commissioned:
                defaults["approved_commissions"] += 1
            elif not self._record_can_be_approved(record):
                defaults["invalid_invoices"] += 1
            else:
                defaults["commissions_to_approve"] += 1
        return defaults

    def _record_can_be_approved(self, record):
        return record.state not in ["draft", "cancel"]

    def move_approve_commission(self):
        active_ids = self._get_active_ids()

        for record in self.env["account.move"].browse(active_ids):
            if not record.commissioned and self._record_can_be_approved(record):
                record.action_move_approve_commission()
        return {"type": "ir.actions.act_window_close"}

    def invoice_reset_approved_commission(self):
        active_ids = self._get_active_ids()

        for record in self.env["account.move"].browse(active_ids):
            if record.commissioned:
                record.action_invoice_reset_approved_commission()
        return {"type": "ir.actions.act_window_close"}
