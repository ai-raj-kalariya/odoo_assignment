# -*- coding: utf-8 -*-

from odoo import fields, models


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

    def action_cancel(self):
        """
        when click cancel button then current record is deleted.
        """
        rec = self.env.context.get('active_id')
        self.env["borrow.transaction.history"].browse(rec).unlink()
