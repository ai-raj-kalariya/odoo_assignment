# -*- coding: utf-8 -*-

from odoo import api, models, fields
from odoo.exceptions import ValidationError, UserError


class SaleOrder(models.Model):
    """
    This model extends the 'sale.order' model to introduce additional approval
    conditions for confirming sale orders based on product stock availability.
    """
    _inherit = 'sale.order'

    is_check_ok = fields.Boolean(
        string="Check"
    )
    is_manager_approve = fields.Boolean(
        string="Is Manager Approve"
    )

    def action_confirm(self):
        """
        Overrides the default confirmation action. If any product in the order has
        a stock quantity of less than 5, a warning wizard is triggered instead of
        confirming the order. If a manager approves or no products have low stock,
        the order proceeds as usual.
        param: self
        return: base conform method
        """
        low_quantity_product = []
        for line in self.order_line:
            if line.product_template_id.qty_available < 5:
                low_quantity_product.append(line.product_template_id.name)
        if ((self.is_manager_approve and self.env.user.is_manager)
                or not low_quantity_product or self.is_manager_approve):
            return super().action_confirm()
        elif low_quantity_product and not self.is_manager_approve:
            product_list = "\n".join([product for product in low_quantity_product])
            message = f"Approval needed! The following books have low stock:\n{product_list}"
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

    def approve_order(self):
        """
        Approves the order if the user is a manager. If not, it raises a UserError. This method sets
        `is_manager_approve` to True, allowing the order to be confirmed even if stock is low.
        param: self
        """
        if not self.env.user.is_manager:
            raise UserError('Only managers can approve orders.')
        self.write({'is_check_ok': False, 'is_manager_approve': True})

    def reject_order(self):
        """
        Cancels the sale order if the user is a manager. If a non-manager attempts
        to reject the order, a UserError is raised.
        param: self
        return: base cancel method
        """
        if not self.env.user.is_manager:
            raise UserError('Only managers can reject orders.')
        self.action_cancel()
