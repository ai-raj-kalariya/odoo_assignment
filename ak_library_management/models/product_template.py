# -*- coding: utf-8 -*-
"""This is product template model inherit from sale/product"""
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
        ('borrowed', 'Borrowed'),
        ('reserved', 'Reserved'),
    ], string="Book Availability")

    borrow_transaction_history_book= fields.Many2one(
        'borrow.transaction.history'
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


    def is_borrowed(self):
        print("\n\n\n>>>>>>>",self.env.ref('ak_library_management.borrow_transaction_history_action').id)
        """This method is convert state into borrowed state"""
        message = _(f"Borrowed book is ")
        return {
            'type': 'ir.actions.act_window',
            'name': "'Borrowed book wizard'",
            'res_model': 'borrow.transaction.history',
            'view_mode': 'form',
            'view_id': self.env.ref('ak_library_management.borrow_transaction_history_action').id,
            'target': 'new',
            # 'context': {
            #     'default_message': message,
            #     'default_res_partner_id': self.id,
            # }
        }

    # Python constrains
    @api.constrains('available')
    def check_book_availability(self):
        if not self.available == True:
            print("\n\n\n>>>>>>>in",self.available)
            raise ValidationError("Book is not available %s" % self.author_id.name)
        print("\n\n\n>>>>>>>out", self.available)
        return self.write({'state': 'borrowed'})

