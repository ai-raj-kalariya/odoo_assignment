# -*- coding: utf-8 -*-
"""This is product template model inherit from sale/product"""
from odoo import _, api, models, fields
from odoo.exceptions import ValidationError
from datetime import date, timedelta


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

    @api.model_create_multi
    def create(self, vals_list):
        """This method create a book sequence for product template"""
        for val in vals_list:
            val['default_code'] = self.env['ir.sequence'].next_by_code('product.template')
        return super().create(vals_list)

    def _compute_display_name(self):
        for rec in self:
            if self._context.get('add_author') and rec.author:
                rec.display_name = '[' + rec.author + ']' + rec.name
            else:
                rec.display_name = rec.name

    # Python constrains
    @api.constrains('available')
    def check_book_availability(self):
        if self.state in ['borrowed', 'unavailable']:
            raise ValidationError("Book is not available %s" % self.author_id.name)
        self.write({'state': 'borrowed'})
        self.message_post(body=f'{self.author_id.name} is borrowed. Date of borrowed: {date.today()}')

        # for activity...
        due_date = date.today() + timedelta(days=10)
        self.activity_schedule(
            act_type_xmlid='mail.mail_activity_data_todo',
            summary="Book Return Reminder",
            note=_(f"The book '{self.name}' borrowed by {self.author_id.name} should be returned by {due_date}."),
            user_id=self.env.user.id,
            date_deadline=due_date
        )
        self.message_post(body=f"{self.author_id.name} borrowed '{self.name}'. Due date: {due_date}")

    def is_returned(self):
        self.write({'state': 'returned'})
        self.message_post(body=f'{self.author_id.name} is return book. Date of return: {date.today()}')

    def borrow_books(self):
        return {
            'type': 'ir.actions.act_window',
            'name': "'Borrowed book'",
            'res_model': 'borrow.transaction.history',
            'view_mode': 'form',
            'target': 'new',
        }
