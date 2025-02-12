# -*- coding: utf-8 -*-

from odoo import api, models, fields
from openpyxl.compat.product import product


class BulkUploadBook(models.TransientModel):
    _name = "bulk.upload.book"
    _description = "Bulk upload book"

    book_names = fields.Text(
        string="Book Names")
    author_id = fields.Many2one(
        comodel_name='res.partner',
        string="Author")
    category = fields.Char(
        string="Category")
    price = fields.Float(
        string="Price")
    created_book_count = fields.Integer(
        compute='_compute_created_book_count',
        string="Created Books"
    )
    product_ids = fields.Many2many(
        'product.template',
        string="Created Product"
    )

    def create_book(self):
        for rec in self:
            if rec.book_names:
                books = rec.book_names.split(",")
                for book in books:
                    result = rec.env['product.template'].search([('name', '=', book)])
                    if not result:
                        products = rec.env['product.template'].create({
                            'name': book,
                            'author_id': rec.author_id.id,
                        })
                        rec.product_ids = [(4, products.id)]
                        print("\n\n products : ", products)
            print("\n\n\n book : ", self)
        return self


    def action_created_book(self):
        """
        This method is used to open list views and form view when click on smart button.
        """
        if len(self.product_ids) > 1:
            action = {
                'name': 'Created Books',
                'type': 'ir.actions.act_window',
                'view_mode': 'list,form',
                'res_model': 'product.template',
                'domain': [('id', 'in', self.product_ids.ids)]
            }
            return action
        if len(self.product_ids) == 1:
            action ={
                'type': 'ir.actions.act_window',
                'view_mode':'form',
                'res_model': 'product.template',
                'domain': [('id', 'in', self.product_ids.ids)]
            }
            print("::::::::::::::::\n\n\nid:::::",self.product_ids.name)

            return action
    def revert_changes(self):
        print(self.product_ids.ids)
        self.product_ids.unlink()

    @api.depends('author_id')
    def _compute_created_book_count(self):
        for book in self:
            book.created_book_count = len(book.product_ids) if book and book.product_ids else 0.0