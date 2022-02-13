# Copyright 2022 <mj@ayudoo.bg>
# License LGPLv3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).

{
    "name": "Agent Management",
    "summary": """
        Adds agent management with commission, evaluation and approval.""",
    "description": """
        Adds agent management with commission, evaluation and approval.""",
    "author": "Michael Jurke, Ayudoo Ltd",
    "category": "Sales",
    "version": "0.1",
    "depends": [
        "base",
        "business_relationships",
        "sale_management",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/agent_management_data.xml",
        "views/account_move_view.xml",
        "views/agent_report_view.xml",
        "views/business_relationship_view.xml",
        "views/partner_view.xml",
        "views/product_template_view.xml",
        "views/sale_order_view.xml",
        "views/templates.xml",
        "wizard/approve_commission_view.xml",
    ],
    "license": "LGPL-3",
}
