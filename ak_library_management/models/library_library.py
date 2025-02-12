# -*- coding: utf-8 -*-
"""This is library  model"""
from odoo import api, models, fields


class Library(models.Model):
    """For create a library and also create a book using tab"""
    _name = "library.library"
    _description = "library"

    name = fields.Char(
        string="Name",
    )
    location = fields.Char(
        string="Location",
    )
    capacity = fields.Integer(
        string="Capacity"
    )
    notes = fields.Text(
        string="Notes"
    )
    # many to many field for create a book using library tab
    product_ids = fields.Many2many(
        comodel_name="product.template",  # parent model
        string="Book",
        domain="[('is_library_book', '=', True)]"
    )
    borrowed_book_count = fields.Integer(
        compute='_compute_borrowed_book_count',
        string="Borrowed Books"
    )

    @api.depends('product_ids')
    def _compute_borrowed_book_count(self):
        """
        This method is used to calculate Borrowed books count which are available in borrow state.
        """
        for library in self:
            library.borrowed_book_count = len(library.product_ids.filtered(
                lambda b: b.state == 'borrowed'
            )) if library and library.product_ids else 0.0

    def action_borrowed_book(self):
        """
        This method is used to open list views and form view when click on smart button.
        """
        action = {
            'name': 'Borrowed Books',
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'product.template',
            'domain': [('state', '=', 'borrowed'), ('id', 'in', self.product_ids.ids)],
        }
        return action
