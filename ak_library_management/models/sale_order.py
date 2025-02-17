# -*- coding: utf-8 -*-
"""This is sale order model inherit from sale"""

from odoo import _, api, models, fields
from odoo.exceptions import ValidationError, UserError

class SaleOrder(models.Model):
    """
    This model is inherit sale.order model from sale module and add
    new conditions in this sale order.
    """
    _inherit='sale.order'

    def action_confirm(self):
        for product in self.order_line:
            if not product.product_uom_qty >= 5:
                raise ValidationError(_("Approval needed! The following books have low stock:"))
        res=super(SaleOrder,self).action_confirm
        return res

    def approve_order(self):
        if not self.env.user.is_manager:
            raise UserError(_('Only managers can approve orders.'))
        res=super(SaleOrder,self).action_confirm
        return res

    def reject_order(self):
        if not self.env.user.is_manager:
            raise UserError(_('Only managers can reject orders.'))
        self.action_cancel()

