# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from xlsxwriter.contenttypes import defaults


class BorrowTransactionHistoryWizard(models.TransientModel):
    """
    Use to showing warning wizard for low quantity.
    """
    _name = 'borrow.transaction.history.wizard'
    _description = 'Borrow Transaction History Wizard'

    message = fields.Text(
        string="Borrowed Book",
        readonly=True
    )
    borrowed_book_id = fields.Many2one(
        'product.template',
        string="Product Template",
        required=True
    )
    author=fields.Char(
        defaults="Raj"
    )

    def action_cancel(self):
        """ Closes the wizard without performing any action."""
        return {'type': 'ir.actions.act_window_close'}
