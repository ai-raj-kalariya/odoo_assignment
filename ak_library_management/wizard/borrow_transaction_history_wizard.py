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

    def action_confirm(self):
        """
            Confirms the action by retrieving the active record from the context and executing
            the `decrease_product_quantity` method if it exists.
            Process:
            - Retrieves the active model and record ID from the Odoo context.
            - Browses the record based on the retrieved model and ID.
            - Checks if the record has the `decrease_product_quantity` method.
            - Calls `decrease_product_quantity` to decrease the product stock quantity.
            This method is typically triggered when a confirmation action is performed in a wizard.
        """
        model_name = self.env.context.get('active_model')
        record_id = self.env.context.get('active_id')
        if model_name and record_id:
            record = self.env[model_name].browse(record_id)
            if record and hasattr(record, 'decrease_product_quantity'):
                record.decrease_product_quantity()

    def action_cancel(self):
        """
        when click cancel button then current record is deleted.
        """
        rec = self.env.context.get('active_id')
        self.env["borrow.transaction.history"].browse(rec).unlink()
