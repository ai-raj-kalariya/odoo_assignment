# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, models, fields
from odoo.exceptions import ValidationError


class BorrowTransactionHistoryWizard(models.TransientModel):
    """
    Use to showing warning wizard for low quantity.
    """
    _name = 'borrow.transaction.history.wizard'
    _description = 'Borrow Transaction History Wizard'

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
    message = fields.Char(
        string="Book Wizard",
        readonly=True
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

    def _check_borrowed_book_limit(self):
        """
        This method checks:
        - If the customer has exceeded the borrowing limit.
          so it triggers a warning wizard before proceeding.
        Returns:
           dict or None: If continue than dict or cancel than none.
        """
        search_record = self.env['borrow.transaction.history'].search(
            [('customer_id', "=", self.customer_id.id)])
        books = list(search_record[:-1].mapped("books_ids").filtered(
            lambda book: book.name).mapped("name"))
        if books:
            name = "Warning Wizard"
            message = (f"{self.customer_id.name} already has {books}"
                       f" open borrow transactions with {len(self.books_ids)} books."
                       " Are you want to borrow more books?")
            return self.get_warning_wizard(name, message, step=4)

        return self.get_warning_wizard(
            "Warning Wizard",
            "Are you want to allow borrowing more than 5 books for this customer?",
            step=4,
        )

    def decrease_product_quantity(self):
        """"
        Reduce the stock quantity for all books in the borrow transaction.
        This method searches for each book in stock and decreases its available quantity by 1
        if there is sufficient stock available.
        Steps:
        - Find the corresponding product in `product.product`.
        - Locate its stock quantity in `stock.quant`.
        - Decrease the stock if the quantity is greater than 0.
        Returns:
            None
        """
        for rec in self.books_ids:
            product_id = self.env['product.product'].search([('name', '=', rec.name)], limit=1)
            product_location = self.env['stock.quant'].search(
                [('product_id', '=', product_id.id)], limit=1)
            if product_id and product_location and product_location.quantity > 0:
                self.env['stock.quant']._update_available_quantity(
                    product_id, product_location.location_id, quantity=-1
                )

    def get_warning_wizard(self, name=None, message=None, step=1):
        """
        Open a warning wizard to notify the user before proceeding.
        The wizard displays warnings regarding:
        - Customer trustworthiness.
        - Stock availability.
        - Borrowing limits.
        Args:
            name (str, optional): Title of the wizard.
            message (str, optional): Warning message.
            step (int, optional): Current step of the wizard.
        Returns:
            dict: Dictionary containing action values for opening the warning wizard.
        """
        view_id = self.env.ref('ak_library_management.view_borrow_transaction_history_wizard').id
        return {
            'type': 'ir.actions.act_window',
            'name': name,
            'res_model': 'borrow.transaction.history.wizard',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'new',
            'context': {
                'default_message': message,
                'wizard_step': step,
                'default_customer_id': self.customer_id.id,
                'default_books_ids': self.books_ids.ids,
                'default_deposit_amount': self.deposit_amount,
                'default_borrow_end_date': self.borrow_end_date,
                'final_step': step
            }
        }

    def action_confirm(self):
        """
        Handles confirmation steps in the warning wizard.
        This method ensures that all warnings (trustworthiness, stock availability, and
        borrowing limit) are addressed before allowing the transaction.
        Steps:
        - Step 1: Ask for confirmation if the customer is not trustworthy.
        - Step 2: Warn if books are out of stock.
        - Step 3: Ask for confirmation if the customer is exceeding the book limit.
        Returns:
            dict or None: Warning wizard action dictionary or None if all checks pass.
        """
        wizard_step = self.env.context.get('wizard_step', 1)
        if wizard_step == 1 and self.customer_id.not_trust_worthy:
            return self.get_warning_wizard(
                name="Borrowed Book",
                message="Customer is not trustworthy. Are you sure you want to continue?",
                step=2)

        if wizard_step <= 2:
            low_quantity_product = [rec.name for rec in self.books_ids if rec.qty_available == 0]
            if low_quantity_product:
                return self.get_warning_wizard(
                    name="Low Quantity Warning",
                    message=f"The following books are out of stock: "
                            f"{', '.join(low_quantity_product)}. Are you sure?",
                    step=3)

        if wizard_step <= 3 and len(self.books_ids) > 5:
            return self._check_borrowed_book_limit()

        return self.create_borrow_transaction()

    def create_borrow_transaction(self):
        """
        Create a borrow transaction record in the history.
        The transaction includes:
        - Customer details.
        - Borrowed books.
        - Deposit amount.
        - Borrow start and end dates.
        This method also reduces the available stock quantity for the borrowed books.
        Returns:
            None
        """
        self.env['borrow.transaction.history'].create({
            'customer_id': self.customer_id.id,
            'books_ids': self.books_ids.ids,
            'deposit_amount': self.deposit_amount,
            'borrow_start_date': self.borrow_start_date,
            'borrow_end_date': self.borrow_end_date
        })
        return self.decrease_product_quantity()

    def action_cancel(self):
        """
        when click cancel button then current record is deleted.
        """
        rec = self.env.context.get('active_id')
        self.env["borrow.transaction.history.wizard"].browse(rec).unlink()