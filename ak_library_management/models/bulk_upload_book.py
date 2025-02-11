# -*- coding: utf-8 -*-

from odoo import api, models, fields


class BulkUploadBook(models.Model):
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
        string="Created Book"
    )

    @api.model_create_multi
    def create(self, vals_list):
        res = super(BulkUploadBook, self).create(vals_list)
        print("\n\n:::::::::::::::::::", res, res.book_names)
        for rec in res:
            if rec.book_names:
                books = rec.book_names.split(",")
                for book in books:
                    products = rec.env['product.template'].create({
                        'name': book,
                        'author_id': rec.author_id.id,
                    })
                    rec.product_ids = [(4, products.id)]
                    print("\n\n products : ", products)
        print("\n\n\n book : ", res)
        return res

    def action_created_book(self):
        """
        This method is used to open list views and form view when click on smart button.
        """
        action = {
            'name': 'Created Books',
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'product.template',
            'domain': [('id', 'in', self.product_ids.ids)]
        }
        return action

    def revert_changes(self):
        print(self.product_ids.ids)
        self.env['product.template'].browse(self.product_ids.ids).unlink()
        self.env['bulk.upload.book'].browse(self.author_id.id).unlink()

    @api.depends('author_id')
    def _compute_created_book_count(self):
        for book in self:
            book.created_book_count = len(book.product_ids) if book and book.product_ids else 0.0