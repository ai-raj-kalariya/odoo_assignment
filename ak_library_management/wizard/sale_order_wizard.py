# -*- coding: utf-8 -*-
from odoo import fields, models


class SaleOrderWarningWizard(models.TransientModel):
    """
    Use to showing warning wizard for low quantity.
    """
    _name = 'sale.order.warning.wizard'
    _description = 'Sale Order Warning Wizard'

    message = fields.Text(
        string="Warning Message",
        readonly=True
    )
    sale_order_id = fields.Many2one(
        'sale.order',
        string="Sale Order",
    )

    def action_mark_approved(self):
        """ Set is_check_ok = True in Sale Order but do not confirm it."""
        if self.sale_order_id:
            self.sale_order_id.write({'is_check_ok': True})
        return {'type': 'ir.actions.act_window_close'}
