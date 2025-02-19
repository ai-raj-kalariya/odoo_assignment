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

    stat = fields.Boolean()
    is_approve = fields.Boolean()

    def action_confirm(self):
        if self.is_approve:
            return super().action_confirm()

        low_quantity_product = self.order_line.filtered(lambda line: line.product_uom_qty < 5)
        if low_quantity_product:
            self.stat=True
            print("\n\n:::::::::::::",self.stat,"\n\n")
            product_list= "\n".join([line.product_id.display_name for line in low_quantity_product])
            raise UserError(_(f"Approval needed! The following books have low stock:\n{product_list}"))
        res = super().action_confirm()
        return res


    def approve_order(self):
        if not self.env.user.is_manager:
            raise UserError(_('Only managers can approve orders.'))
        self.stat = False
        self.is_approve = True

    # def reject_order(self):
    #     # if not self.env.user.is_manager:
    #     #     raise UserError(_('Only managers can reject orders.'))
    #     # self.stat = False
    #     # return super().action_cancel()
    #     pass

    def reject_order(self):
        if not self.env.user.is_manager:
            raise UserError(_('Only managers can reject orders.'))
        self.action_cancel()