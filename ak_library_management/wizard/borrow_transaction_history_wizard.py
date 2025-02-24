# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime,timedelta


class BorrowTransactionHistoryWizard(models.TransientModel):
    """
    Use to showing warning wizard for low quantity.
    """
    _name = 'borrow.transaction.history.wizard'
    _description = 'Borrow Transaction History Wizard'

    message = fields.Char(
        string="Book Wizard",
        readonly=True
    )

    # customer_name = fields.Many2one(
    #     'res.partner',
    #     string='Customer Name'
    # )
    # from_datetime = fields.Datetime(
    #     string='From Datetime',
    #     default=datetime.today(),
    #     readonly=True
    # )
    # end_datetime = fields.Datetime(
    #     string='End Datetime'
    # )
    # books = fields.Many2many(
    #     'product.template',
    #     string='Books '
    # )
    # deposit_amount = fields.Float(
    #     string='Deposit Amount'
    # )
    #
    # def action_confirm(self):
    #     """
    #
    #     """
    #     if not self.customer_name.not_trust_worthy:
    #         books = self.env['borrow.transaction.history'].create({
    #             'customer_id': self.customer_name.id,
    #             'books': self.books.ids,
    #             'borrow_start_date': self.from_datetime,
    #             'borrow_end_date': self.end_datetime,
    #             'deposit_amount': self.deposit_amount, }
    #         )
    #         return books
    #     return {
    #
    #     }
    #
    #
    # def action_cancel(self):
    #     """ Closes the wizard without performing any action."""
    #     return {'type': 'ir.actions.act_window_close'}
    #
    # @api.constrains('borrow_start_date', 'borrow_end_date')
    # def _check_end_date(self):
    #     if self.borrow_end_date < self.borrow_start_date:
    #         raise ValidationError("Borrow end date should be higher than start date.")
