# -*- coding: utf-8 -*-

from odoo import models, fields
from datetime import  datetime


class BorrowTransactionHistory(models.Model):
    _name = 'borrow.transaction.history'
    _rec_name='customer_id'

    customer_id = fields.Many2one(
        comodel_name='res.partner',
        string="Customer_id"
    )
    books = fields.Many2many(
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
