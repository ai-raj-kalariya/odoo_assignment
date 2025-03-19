# -*- coding: utf-8 -*-

from datetime import datetime, date, timedelta
from odoo import api, models, fields
from odoo.exceptions import ValidationError


class BorrowTransactionHistory(models.Model):
    """
    This model handles the borrow transaction history for books in the library.
    It manages:
    - Borrowing transactions with conditions (stock availability, trustworthiness, limits).
    - Stock movement when books are borrowed.
    - Reminders for due and overdue books.
    """
    _name = 'borrow.transaction.history'
    _description = 'Borrow transaction history'
    _rec_name = 'customer_id'

    customer_id = fields.Many2one(
        comodel_name='res.partner',
        string="Customer",
        required=True
    )
    books_ids = fields.Many2many(
        comodel_name='product.template',
        string="Books",
    )
    borrow_start_date = fields.Date(
        string="Borrow start Date",
        default=datetime.today(),
        readonly=True
    )
    borrow_end_date = fields.Date(
        string="Borrow End Date",
        required=True
    )
    deposit_amount = fields.Float(
        string="Deposit Amount",
        required=True,
    )
    is_member = fields.Boolean(
        related='customer_id.is_member'
    )
    is_borrowing_limit = fields.Boolean()

    @api.constrains('borrow_start_date', 'borrow_end_date', 'deposit_amount')
    def _check_end_date(self):
        """
        Ensures that the borrow end date is not before the start date.
        :raise ValidationError: If the borrow end date is earlier than the start date.
        :raise ValidationError: If Non member is trying to borrow book without enter deposit amount.
        """
        if self.borrow_end_date < self.borrow_start_date:
            raise ValidationError("Borrow end date should be higher than start date.")
        if self.deposit_amount == 0 and not self.is_member:
            raise ValidationError("Deposit amount is required for non member.")

    def _cron_send_overdue_mail(self):
        """
       Sends a reminder for books due in 2 days or overdue.
       - If the due date is passed, a reminder is triggered.
       - If the due date has passed, an overdue alert is triggered.
       This method should be scheduled to run periodically.
        """
        all_books = self.search([('borrow_end_date', '<', date.today()),
                                 ('books_ids.state', '=', 'borrowed')])
        if all_books:
            for rec in all_books:
                mail_template = self.env.ref(
                    'ak_library_management.email_template_library_book_return_date_passed')
                mail_template.send_mail(rec.id, force_send=True)

    def _cron_book_returned_reminder(self):
        """
       Sends a reminder for books due in 2 days.
       - If the due date on next 2 days, a reminder is triggered.
       This method should be scheduled to run periodically.
        """
        alert_date_deadline = date.today() + timedelta(days=2)
        recs = self.search([('borrow_end_date', '=', alert_date_deadline)])
        for rec in recs:
            self.env['bus.bus']._sendone(rec.customer_id, 'simple_notification', {
                'type': 'warning',
                'message': f"reminder: your book return date is {rec.borrow_end_date}",
            })
            mail_template = self.env.ref(
                'ak_library_management.email_template_library_book_reminder')
            mail_template.send_mail(rec.id, force_send=True)

    def is_book_returned(self):
        """
        Marks books as returned and sends a confirmation notification to the customer.
        """
        for book in self.books_ids:
            if book.state == 'borrowed':
                book.write({'state': 'returned'})
                self.env['bus.bus']._sendone(self.customer_id, 'simple_notification', {
                    'type': 'success',
                    'message': f"{book.name} your return book has been recorded.",
                })

    def automated_action(self):
        """
        Prevents customers from borrowing new books if they have overdue books.
        :raise ValidationError: If the customer has overdue books.
        """
        for record in self:
            if record.customer_id and record.books_ids:
                overdue_transactions = self.env['borrow.transaction.history'].search([
                    ('customer_id', '=', record.customer_id.id),
                    ('borrow_end_date', '<', fields.Date.today()),
                    ('books_ids.state', '=', 'borrowed')
                ])
                if overdue_transactions:
                    overdue_books = []
                    for transaction in overdue_transactions:
                        overdue_books += [book.name for book in transaction.books_ids
                                          if book.state == 'borrowed']
                    overdue_books_list = ", ".join(overdue_books)
                    raise ValidationError(
                        f"Customer {record.customer_id.name} has overdue books:"
                        f" {overdue_books_list}. "
                        "Please return them before borrowing new books."
                    )
