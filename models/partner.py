from odoo import api, fields, models


class Partner(models.Model):
    _inherit = ["res.partner"]
    _name = "res.partner"

    def _commercial_fields(self):
        return super()._commercial_fields() + ["agent_id"]

    is_agent = fields.Boolean(
        string="Is Agent",
        related="business_relationship_id.is_agent",
        readonly=True,
    )

    agent_commission = fields.Float(
        digits=(3, 2),
        default=0.0,
        tracking=True,
    )

    agent_id = fields.Many2one(
        "res.partner",
        string="Agent",
        domain=[("business_relationship_id.is_agent", "=", True)],
        ondelete="restrict",
        tracking=True,
    )

    agent_partner_ids = fields.One2many(
        "res.partner",
        string="Agent's Partners",
        inverse_name="agent_id",
    )

    def _compute_agent_partner_count(self):
        for record in self:
            record.agent_partner_count = len(record.agent_partner_ids)

    agent_partner_count = fields.Integer(
        string="Agent Partner Count",
        compute=_compute_agent_partner_count,
    )

    @api.constrains("agent_id")
    def _reset_agent_id(self):
        if self.is_agent and self.agent_id:
            # silently reset the agent_id for agents
            self.agent_id = None

    def action_open_agent_partners(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "base.action_partner_customer_form"
        )
        action["context"] = {
            "search_default_agent_id": [self.id],
            "default_agent_id": self.id,
        }
        return action
