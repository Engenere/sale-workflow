# Copyright 2023 Engenere.one
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import _, api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # The use of a state field instead of a Boolean is to make it more visible to the
    # user who is selling the product for the first time and avoid mistakes. As the
    # creation of the module focused on reducing errors when entering products,
    # I found it more appropriate.

    product_first_sale = fields.Selection(
        [("first_sale", _("First Sale"))], string="First Sale?"
    )

    @api.onchange("product_id", "order_partner_id")
    def _change_product_first_sale(self):
        for record in self:
            if record.order_id.state != ["sale", "done"]:
                if record.product_id and record.order_partner_id:
                    domain = self._get_first_time_sale_domain(
                        record.product_id, record.order_partner_id
                    )
                    previous_orders = self.env["sale.order.line"].search(domain)
                    record.product_first_sale = (
                        "first_sale" if not previous_orders else False
                    )
                else:
                    record.product_first_sale = False

    @api.model
    def _get_first_time_sale_domain(self, product_id, partner_id):
        domain = [
            ("product_id", "=", product_id.id),
            ("order_partner_id", "=", partner_id.id),
            ("order_id.state", "in", ["sale", "done"]),
            ("product_uom_qty", ">", 0),
        ]
        get_param = self.env["ir.config_parameter"].sudo().get_param
        days_limit = int(get_param("sale_first_sale.days_limit", 0))
        if days_limit > 0:
            date_ago = fields.Date.today() - timedelta(days=days_limit)
            domain.append(("order_id.date_order", ">=", date_ago))
        return domain
