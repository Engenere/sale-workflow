# Copyright 2023 Engenere.one
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Sale First Time State",
    "summary": """
        Indicates whether the product is being sold for the first time to the partner.""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "Engenere.one,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/sale-workflow",
    "depends": [
        "sale",
    ],
    "data": [
        "views/sale_order_view.xml",
        "views/sale_config_settings.xml",
    ],
    "demo": [],
}
