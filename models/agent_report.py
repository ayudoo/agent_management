from odoo import tools
from odoo import models, fields


class AgentReport(models.Model):
    _name = "agent_management.agent_report"
    _description = "Agent Evaluation"
    _auto = False
    _rec_name = "agent_id"
    _order = "invoice_date desc"

    # dummy field so we can rely on odoo's many2one widget to name and link
    # to the invoice
    def _get_invoice_id(self):
        for record in self:
            record.invoice_id = record.id

    invoice_id = fields.Many2one(
        string="Invoice",
        compute=_get_invoice_id,
        comodel_name="account.move",
        readonly=True,
        store=False,
    )

    # agent mixin fields

    agent_id = fields.Many2one(
        "res.partner",
        string="Agent",
        help="The agent who placed this partner",
        readonly=True,
    )
    agent_commission = fields.Float(
        digits=(3, 2),
        string="Commission",
        help="The agent's commission",
        group_operator="avg",
        readonly=True,
    )
    amount_commission_base = fields.Monetary(
        string="Commission Base",
        readonly=True,
    )

    # commissionable invoice specific fields

    commissioned = fields.Boolean(string="commissioned", readonly=True)
    commission_date = fields.Date(
        string="Commission Date",
        readonly=True,
    )
    amount_commission = fields.Monetary(
        string="Ammount Commission",
        readonly=True,
    )
    approved_commission = fields.Monetary(
        string="Approved Commission",
        readonly=True,
    )

    # other invoice fields to show in the evaluation

    invoice_date = fields.Date(readonly=True)
    name = fields.Char(string="Invoice Number", readonly=True)
    amount_residual_signed = fields.Monetary(
        string="Amount Due in Invoice Currency",
        help="Remaining amount due in the currency of the invoice.",
        readonly=True,
    )

    currency_id = fields.Many2one("res.currency", string="Currency", readonly=True)
    partner_id = fields.Many2one("res.partner", string="Partner", readonly=True)
    commercial_partner_id = fields.Many2one(
        "res.partner", string="Partner Company", help="Commercial Entity"
    )

    move_type = fields.Selection(
        [
            ("entry", "Journal Entry"),
            ("out_invoice", "Customer Invoice"),
            ("out_refund", "Customer Credit Note"),
            ("in_invoice", "Vendor Bill"),
            ("in_refund", "Vendor Credit Note"),
            ("out_receipt", "Sales Receipt"),
            ("in_receipt", "Purchase Receipt"),
        ],
        string="Invoice Type",
        readonly=True,
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("posted", "Posted"),
            ("cancel", "Cancelled"),
        ],
        string="Invoice Status",
        readonly=True,
    )

    def _select(self):
        select_str = """
            SELECT
                am.id,
                am.invoice_date,
                am.partner_id,
                am.currency_id,
                am.move_type,
                am.state,
                am.name,
                am.amount_residual_signed,
                am.company_id,
                am.commercial_partner_id,

                am.agent_id,
                am.agent_commission,
                am.amount_commission_base,
                am.commissioned,
                am.commission_date,
                am.amount_commission,
                am.approved_commission
        """
        return select_str

    def _from(self):
        from_str = """
            FROM account_move am
            JOIN res_partner partner ON am.commercial_partner_id = partner.id
        """
        return from_str

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        create_view = """
            CREATE or REPLACE VIEW {table} as (
                WITH currency_rate AS ({companies_rates})
                {select} {from_table}
                LEFT JOIN currency_rate cr ON (
                    cr.currency_id = am.currency_id AND
                    cr.company_id = am.company_id AND
                    cr.date_start <= COALESCE(am.invoice_date, NOW()) AND
                    (
                        cr.date_end IS NULL OR
                        cr.date_end > COALESCE(am.invoice_date, NOW())
                    )
                )
            )
        """.format(
            table=self._table,
            companies_rates=self.env["res.currency"]._select_companies_rates(),
            select=self._select(),
            from_table=self._from(),
        )
        self.env.cr.execute(create_view)
