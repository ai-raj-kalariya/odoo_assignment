# -*- coding: utf-8 -*-
"""This is sale order model inherit from sale"""

from odoo import _, api, models, fields
from odoo.exceptions import ValidationError, UserError


class SaleOrder(models.Model):
    """
    This model is inherit sale.order model from sale module and add
    new conditions in this sale order.
    """
    _inherit = 'sale.order'

    check_ok = fields.Boolean(
        default=False
    )
    is_approve = fields.Boolean(
        default=False
    )

    def action_confirm(self):
        """
        Override action_confirm to check product quantity.
        If any product has less than 5 quantity, open the warning wizard instead of confirming the order.
        """
        if self.is_approve:
            return super(SaleOrder, self).action_confirm()

        low_quantity_product = self.order_line.filtered(lambda line: line.product_template_id.qty_available < 5)
        if low_quantity_product:
            product_list = "\n".join([line.product_template_id.name for line in low_quantity_product])
            message = _(f"Approval needed! The following books have low stock:\n{product_list}")

            return {
                'type': 'ir.actions.act_window',
                'name': "Sale Order Warning",
                'res_model': 'sale.order.warning.wizard',
                'view_mode': 'form',
                'view_id': self.env.ref('ak_library_management.sale_order_warning_wizard_view').id,
                'target': 'new',
                'context': {
                    'default_message': message,
                    'default_sale_order_id': self.id,
                }
            }
        return super(SaleOrder, self).action_confirm()

    def approve_order(self):
        """
        If is member than approve less than 5 product otherwise 
        showing UserError
        """
        if not self.env.user.is_manager:
            raise UserError(_('Only managers can approve orders.'))
        self.check_ok = False
        self.is_approve = True

    def reject_order(self):
        """
        This method is cancel the order.
        """
        if not self.env.user.is_manager:
            raise UserError(_('Only managers can reject orders.'))
        return super().action_cancel()
