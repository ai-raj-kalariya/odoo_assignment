# -*- coding: utf-8 -*-

from odoo import _,models, fields, api
from odoo.exceptions import ValidationError
from datetime import  datetime


class BorrowTransactionHistory(models.Model):
    _name = 'borrow.transaction.history'
    _rec_name='customer_id'

    customer_id = fields.Many2one(
        comodel_name='res.partner',
        string="Customer_id"
    )
    books_ids = fields.Many2many(
        'product.template',
        string="Books",
    )
    borrow_start_date = fields.Datetime(
        string="Borrow start Date",
        default=datetime.today(),
        readonly=True
    )
    borrow_end_date = fields.Datetime(
        string="Borrow End Date"
    )
    deposit_amount = fields.Float(
        string="Deposit Amount"
    )

    @api.constrains('borrow_start_date', 'borrow_end_date')
    def _check_end_date(self):
        if self.borrow_end_date < self.borrow_start_date:
            raise ValidationError("Borrow end date should be higher than start date.")

    def get_wizard(self,name,message):
        return {
                'type': 'ir.actions.act_window',
                'name': name,
                'res_model': 'borrow.transaction.history.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_message': message,
                }
        }

    def action_confirm(self):
        """

        """
        print("\n\n\n>>>>>>>>>>..",low_quantity_product)
        if self.customer_id.not_trust_worthy:
            return self.get_wizard(
                name='Borrowed book',
                message ="Customer is not trustworthy. Are you sure you want to continue?")

        # low_quantity_product=[book.name for book in self.books_ids]
        # 
        # if low_quantity_product:
        #     product_list = "\n".join([line.product_template_id.name for line in low_quantity_product])
        #     return self.get_wizard(
        #         name='Law quantity book',
        #         message=_(f"Approval needed! The following books have low stock:\n{product_list}")
        #     )
        else:
            books = self.env['borrow.transaction.history'].create({
                'customer_id': self.customer_id.id,
                'books': self.books.ids,
                'borrow_start_date': self.borrow_start_date,
                'borrow_end_date': self.borrow_end_date,
                'deposit_amount': self.deposit_amount,
            })
            return books


    def action_cancel(self):
        """ Closes the wizard without performing any action."""
        return {'type': 'ir.actions.act_window_close'}
