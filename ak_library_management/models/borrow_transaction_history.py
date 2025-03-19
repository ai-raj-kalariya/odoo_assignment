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
        # readonly=True
    )
    borrow_end_date = fields.Date(
        string="Borrow End Date",
        required=True
    )
    deposit_amount = fields.Float(
        string="Deposit Amount",
    )
    is_member = fields.Boolean(
        related='customer_id.is_member'
    )
    is_borrowing_limit = fields.Boolean(
        string="Is Borrowing Limit",
        compute="_compute_is_borrowing_limit",
        store=True
    )

    is_active_transaction = fields.Boolean(
        string="Is Active Transaction",
        compute="_compute_is_active_transaction",
        store=True
    )

    @api.depends('borrow_end_date')
    def _compute_is_active_transaction(self):
        today = date.today()
        for record in self.search([]):
            record.is_active_transaction = record.borrow_end_date >= today

    @api.depends('books_ids')
    def _compute_is_borrowing_limit(self):
        for rec in self:
            print("\n\n",rec,"\n\n")
            borrowing_limit = self.env.user.company_id.borrowing_limit
            print("\n\nborrowing_limit:::",borrowing_limit,"\n\n")
            search_record = self.env['borrow.transaction.history'].search([('customer_id', "=", self.customer_id.id)])
            print("\n\nsearch_record:::",search_record,"\n\n")
            total_borrowed_books = list(search_record.mapped("books_ids").filtered(
                lambda book: book.name).mapped("name"))
            print("\n\ntotal_borrowed_books:::",total_borrowed_books,"\n\n")
            if len(total_borrowed_books) > borrowing_limit:
                rec.is_borrowing_limit = True
            else:
                rec.is_borrowing_limit = False

    @api.constrains('borrow_start_date', 'borrow_end_date')
    def _check_end_date(self):
        """
        Ensures that the borrow end date is not before the start date.
        :raise ValidationError: If the borrow end date is earlier than the start date.
        :raise ValidationError: If Non member is trying to borrow book without enter deposit amount.
        """
        if self.borrow_end_date < self.borrow_start_date:
            raise ValidationError("Borrow end date should be higher than start date.")

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
