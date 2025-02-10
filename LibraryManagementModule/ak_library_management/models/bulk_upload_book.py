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
                print("\n\n\n books : ", books, len(books))
                for book in books:
                    products = rec.env['product.template'].create({
                        'name': book,
                        'author_id': rec.author_id.id,
                    })
                    rec.product_ids = [(4, products.id)]
                    print("\n\n products : ", products)
        # hello
        print("\n\n\n book : ", res)

        return res

    # def create_book(self):
    #     created_book = [book for book in self.book_name.split(",")]

    def revert_changes(self):
        print("\n\n:::::::::::::::::::::::::::revert changes\n")

    @api.depends('author_id')
    def _compute_created_book_count(self):
        """
        This method is used to calculate Borrowed books count which are available in borrow state.
        """
        for book in self:
            book.created_book_count = 0

    def action_create_book(self):
        print("\n????????????????????????? book show\n")
