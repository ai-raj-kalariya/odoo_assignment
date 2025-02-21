# -*- coding: utf-8 -*-
"""This is product template model inherit from sale/product"""
from odoo import _, api, models, fields
from odoo.exceptions import ValidationError
from datetime import date


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

    def is_available(self):
        """This method is convert state into available state"""
        self.write({'state': 'available'})

    @api.model_create_multi
    def create(self, vals_list):
        """This method create a book sequence for product template"""
        for val in vals_list:
            val['default_code'] = self.env['ir.sequence'].next_by_code('product.template')
        return super().create(vals_list)

    def is_borrowed(self):
        print("\n\n\n>>>>>>>", self.env.ref('ak_library_management.borrow_transaction_history_action').id)
        """This method is convert state into borrowed state"""
        message = "Customer is not trustworthy. Are you sure you want to continue?"
        return {
            'type': 'ir.actions.act_window',
            'name': "'Borrowed book wizard'",
            'res_model': 'borrow.transaction.history.wizard',
            'view_mode': 'form',
            'target': 'new',
        }

    # Python constrains
    @api.constrains('available')
    def check_book_availability(self):
        if self.state in ['borrowed', 'unavailable']:
            raise ValidationError("Book is not available %s" % self.author_id.name)
        self.write({'state': 'borrowed'})
        self.message_post(body=f'{self.author_id.name} is borrowed. Date of borrowed: {date.today()}')
        #
        # def create_activity(self):
        activty_type = self.env['mail.activity.type'].create({
            'name': 'To-Do',
        })
        activity = self.env['mail.activity'].create({
            'summary': 'Discuss about some topic',
            'activity_type_id': activty_type.id,
            'note': 'Discuss',
            'res_model_id': self.env['ir.model']._get_id('product.template'),
            'res_id': self.id
        })
        # return activity

    # @api.depends('activity_type_id')
    # def _compute_date_deadline(self):
    #     for scheduler in self:
    #         if scheduler.activity_type_id:
    #             scheduler.date_deadline = scheduler.activity_type_id._get_date_deadline()
    #         elif not scheduler.date_deadline:
    #             scheduler.date_deadline = fields.Date.context_today(scheduler)

    def is_returned(self):
        self.write({'state': 'returned'})
        self.message_post(body=f'{self.author_id.name} is return book. Date of return: {date.today()}')
