# -*- coding: utf-8 -*-
"""This is product template model inherit from sale/product"""
from datetime import date, timedelta
from odoo import _, api, models, fields
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    """This model is inherit product.template model from sale module and add
        new field in this product template."""
    _inherit = "product.template"

    is_library_book = fields.Boolean(
        string="Library Book"
    )
    author_id = fields.Many2one(
        comodel_name='res.partner',
        string="Author"
    )
    publisher = fields.Char(
        string="Publisher"
    )
    edition = fields.Char(
        string="Edition"
    )
    published_date = fields.Date(
        string="Published_date"
    )
    pages = fields.Integer(
        string="Pages"
    )
    available = fields.Boolean(
        string="Available"
    )
    state = fields.Selection([
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
    ], string="Book Availability",
        tracking=True)
    due_date = fields.Date(
        default=date.today()
    )

    def is_available(self):
        """This method is convert state into available state"""
        self.write({'state': 'available'})

    def is_borrowed(self):
        """This method is convert state into borrowed state"""
        self.with_context(state=self.state).write({'state': 'borrowed'})

    @api.model_create_multi
    def create(self, vals_list):
        """This method create a book sequence for product template"""
        for val in vals_list:
            val['default_code'] = self.env['ir.sequence'].next_by_code('product.template')
        return super().create(vals_list)

    def _compute_display_name(self):
        """
          override compute display name and change book name format to
          [author_name]book_name.
          param: none
        """
        for rec in self:
            if self._context.get('add_author') and rec.author_id:
                rec.display_name = '[' + rec.author_id.name + ']' + rec.name
            else:
                rec.display_name = rec.name

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=None):
        """
        override name_search method to search book by author name.
        param: name, args, operator, limit
        """
        args = list(args or [])
        if name:
            args += [('author_id', operator, name)]
        return super().name_search(args=args, limit=limit)

    # Python constrains
    @api.constrains('state')
    def _check_state(self):
        """
        In this method check if book is not borrowed then create activity and log else
        if state in borrowed then show the
        :return:
        """
        if self._context.get('state', False) in ['borrowed', 'unavailable']:
            raise ValidationError("Book is not available.")
        if self.state == 'borrowed':
            self.message_post(body=f'{self.env.user.name} is borrowed book. Date: {date.today()}')

            # for activity...
            due_date = date.today() + timedelta(days=10)
            self.activity_schedule(
                act_type_xmlid='mail.mail_activity_data_todo',
                summary="Book Return Reminder",
                note=_(f"'{self.name}' borrowed by {self.env.user.name} should be return {due_date}."),
                user_id=self.env.user.id,
                date_deadline=due_date
            )
            self.message_post(body=f"{self.env.user.name} borrowed '{self.name}'. Due date: {due_date}")

        if self.state == 'returned':
            self.env['bus.bus']._sendone(self.env.user.partner_id, 'simple_notification', {
                'type': 'warning',
                'message': f"{self.name} book state is changed to {self.state}",
            })

    def is_returned(self):
        """
        Using this method can change the state into returned.
        """
        self.write({'state': 'returned'})
        self.message_post(body=f'{self.env.user.name} is return book. Date: {date.today()}')

    def borrow_books(self):
        """
        This method use for open book_transaction_history wizard.
        """
        return {
            'type': 'ir.actions.act_window',
            'name': "'Borrowed book'",
            'res_model': 'borrow.transaction.history',
            'view_mode': 'form',
            'target': 'new',
        }
