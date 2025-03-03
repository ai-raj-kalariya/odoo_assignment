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
        required=True
    )
    is_member = fields.Boolean(
        related='customer_id.is_member'
    )

    @api.constrains('borrow_start_date', 'borrow_end_date')
    def _check_end_date(self):
        """
        Ensures that the borrow end date is not before the start date.
        :raise ValidationError: If the borrow end date is earlier than the start date.
        """
        if self.borrow_end_date < self.borrow_start_date:
            raise ValidationError("Borrow end date should be higher than start date.")

    def get_warning_wizard(self, name, message):
        """
       Displays a warning popup wizard with a custom message.
       :param str name: Title of the warning popup.
       :param str message: Message to display in the popup.
       :return: Dictionary defining the wizard action.
       :rtype: dict
        """
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
        Confirms the borrow transaction with the following validations:
        - Ensures the customer is trustworthy.
        - Verifies book stock availability.
        - Limits the number of borrowed books.
        - Reduces stock when the book is borrowed.
        :return: Warning wizard if any condition fails, else proceeds with the transaction.
        :rtype: dict or None
        """
        if self.customer_id.not_trust_worthy:
            return self.get_warning_wizard(
                name='Borrowed book',
                message="Customer is not trustworthy. Are you sure you want to continue?")

        low_quantity_product = [rec.name for rec in self.books_ids if rec.qty_available == 0]
        if low_quantity_product:
            name = 'Low quantity wizard'
            message = (f"The following books are out of stock: {low_quantity_product}."
                       " Are you want to continue?")
            return self.get_warning_wizard(name, message)

        if len(self.books_ids) > 5:
            search_record = self.search([('customer_id.name', "=", self.customer_id.name)])
            books = []
            [books.append(book.name) for rec in search_record[:-1]
             for book in rec.books_ids if book.name not in books]

            if books:
                name = "Warning Wizard"
                message = (f"Customer already has [{self.customer_id.name}]"
                           f" open borrow transactions with {books} books."
                           " Are you want to borrow more books?")
                return self.get_warning_wizard(name, message)

            return self.get_warning_wizard(
                "Warning Wizard",
                "Are you want to allow borrowing more than 5 books for this customer?")

        for rec in self.books_ids:
            if rec.qty_available:
                rec.qty_available -= 1

    def book_returned_reminder(self):
        """
       Sends a reminder for books due in 2 days or overdue.
       - If the due date is in 2 days, a reminder is triggered.
       - If the due date has passed, an overdue alert is triggered.
       This method should be scheduled to run periodically.
        """
        borrowed_book = self.env['product.template'].search([('state', '=', 'borrowed')])
        for activity_deadline in borrowed_book:
            print("\n activity_deadline:", activity_deadline.activity_ids['date_deadline'])
            alert_date = activity_deadline.activity_ids['date_deadline'] - timedelta(days=2)
            if date.today() == alert_date:
                print("\n\ndate for returned:::::", date.today())
            if date.today() > alert_date:
                print("\n\nbook name:::::", activity_deadline)
