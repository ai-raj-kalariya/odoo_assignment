# -*- coding: utf-8 -*-
"""This is sale order model inherit from sale"""

from odoo import _, api, models, fields
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    """
    This model is inherit sale.order model from sale module and add
    new conditions in this sale order.
    """
    _inherit='sale.order'

    def action_confirm(self):
        print("\n\n:::::quantity:::::",self.order_line)
        # for product in self.order_line:
        #     print(product.)
        # # if not self.product_uom_qyt >= 5:
        #     raise ValidationError(_("Approval needed! The following books have low stock: (list of products with quantity less than 5)"))
        res=super(SaleOrder,self).action_confirm
        print("\n\n:::::2\n\n")
        return res

    def approve_order(self):
        print("\n\n::::::approve",self)

    def reject_order(self):
        print("\n\n::::::reject",self)

