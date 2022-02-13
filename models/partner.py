from odoo import api, fields, models


class Partner(models.Model):
    _inherit = ["res.partner"]
    _name = "res.partner"

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

    @api.constrains("agent_id")
    def _reset_agent_id(self):
        if self.is_agent and self.agent_id:
            # silently reset the agent_id for agents
            self.agent_id = None
