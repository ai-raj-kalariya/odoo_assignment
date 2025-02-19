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
    is_approve = fields.Boolean()

    def action_confirm(self):
        """
        This method is check if product quantity is less than 5 then return validation 
        error and if more than 5 then proceed base method.
        """
        if self.is_approve:
            return super().action_confirm()

        low_quantity_product = self.order_line.filtered(lambda line: line.product_uom_qty < 5)
        if low_quantity_product:
            self.check_ok = True
            product_list = "\n".join([line.product_id.display_name for line in low_quantity_product])
            raise UserError(_(f"Approval needed! The following books have low stock:\n{product_list}"))
        res = super().action_confirm()
        print("\n\n\n",self.check_ok)
        return res

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
