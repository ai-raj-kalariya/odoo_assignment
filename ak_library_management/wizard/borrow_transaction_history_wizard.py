# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError

class BorrowTransactionHistoryWizard(models.TransientModel):
    """
    Use to showing warning wizard for low quantity.
    """
    _name = 'borrow.transaction.history.wizard'
    _description = 'Borrow Transaction History Wizard'

    customer_name = fields.Many2one(
        'res.partner',
        string='Customer Name'
    )
    from_datetime = fields.Datetime(
        string='From Datetime'
    )
    end_datetime = fields.Datetime(
        string='End Datetime'
    )
    books = fields.Many2many(
        'product.template',
        string='Books '
    )
    deposit_amount = fields.Float(
        string='Deposit Amount'
    )

    def action_confirm(self):
        """

        """
        if not self.customer_name.not_trust_worthy:
            books = self.env['borrow.transaction.history'].create({
                'customer_id': self.customer_name.id,
                'books': self.books.ids,
                'borrow_start_date': self.from_datetime,
                'borrow_end_date': self.end_datetime,
                'deposit_amount': self.deposit_amount, }
            )
            return books

    def action_cancel(self):
        """ Closes the wizard without performing any action."""
        return {'type': 'ir.actions.act_window_close'}
