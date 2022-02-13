from odoo import fields, models


class BusinessRelationship(models.Model):
    _inherit = "res.partner.business_relationship"

    is_agent = fields.Boolean(
        string="Agent",
        default=False,
        help="Specify, if this is an agent for commercial transactions",
    )
