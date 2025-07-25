from odoo import models, fields, api


class CommissionMixin(models.AbstractModel):
    _name = "agent_management.commission.mixin"
    _description = "Commission Mixin"

    currency_id = fields.Many2one("res.currency")
    partner_id = fields.Many2one("res.partner", string="Partner", ondelete="restrict")

    agent_id = fields.Many2one(
        "res.partner",
        string="Agent",
        help="The agent who placed this partner",
    )

    @api.onchange("partner_id")
    def _set_agent_id(self):
        for record in self:
            record.agent_id = record.partner_id.agent_id

    @api.model_create_multi
    def create(self, values_list):
        records = super().create(values_list)

        for record in records:
            # for orders, that aren't created using the form
            if record.partner_id.agent_id and not record.agent_id:
                record.agent_id = record.partner_id.agent_id

            if (
                record.agent_id
                and not record.agent_commission
                and not record.has_agent_commission
            ):
                record._compute_default_agent_commission()
                record.has_agent_commission = True
                record.agent_commission = record.default_agent_commission

        return records

    @api.depends("agent_id")
    def _compute_default_agent_commission(self):
        for record in self:
            record.default_agent_commission = record.agent_id.agent_commission

    @api.onchange("partner_id", "agent_id", "has_agent_commission")
    def _set_agent_commission(self):
        if not self.agent_id:
            self.has_agent_commission = False
            self.agent_commission = 0.0
        elif not self.has_agent_commission:
            self.has_agent_commission = True
            self.agent_commission = self.default_agent_commission

    @api.onchange("agent_id")
    def _reset_has_agent_commission(self):
        self.has_agent_commission = False

    default_agent_commission = fields.Float(
        digits=(3, 2),
        string="Default commission",
        help="The commission from the agent or origin (refund)",
        compute="_compute_default_agent_commission",
    )

    agent_commission = fields.Float(
        digits=(3, 2),
        string="Commission",
        help="The commission for this document",
        group_operator="avg",
        tracking=True,
    )

    # avoid duplicate checks and changes, as well as differentiate 0 and no commission
    has_agent_commission = fields.Boolean()

    amount_commission = fields.Monetary(
        string="Commission Amount",
        compute="_compute_amount_commission",
        readonly=True,
        store=True,
        currency_field="currency_id",
    )

    amount_commission_base = fields.Monetary(
        string="Commission Base",
        compute="_compute_amount_commission_base",
        store=True,
        readonly=True,
        currency_field="currency_id",
    )


class CommissionLineMixin(models.AbstractModel):
    _name = "agent_management.commission.line.mixin"
    _description = "Commission Line Mixin"

    currency_id = fields.Many2one("res.currency")

    @api.model_create_multi
    def create(self, values_list):
        """Set commissionable, works with events and _cart_update"""
        records = super().create(values_list)
        for record in records:
            record._set_commissionable(update_existing=True)
        return records

    @api.onchange("product_id")
    def _set_commissionable(self, update_existing=False):
        for record in self:
            if not record.product_id.commissionable:
                record.commissionable = False
            elif update_existing or isinstance(record.id, models.NewId):
                record.commissionable = True

    commissionable = fields.Boolean(string="Commissionable")

    @api.onchange("product_id", "commissionable")
    def _compute_can_toggle_commissionable(self):
        for record in self:
            # can always unset commissionable
            if record.commissionable:
                record.can_toggle_commissionable = True
            else:
                record.can_toggle_commissionable = record.product_id.commissionable

    can_toggle_commissionable = fields.Boolean(
        compute=_compute_can_toggle_commissionable,
        store=False,
    )
