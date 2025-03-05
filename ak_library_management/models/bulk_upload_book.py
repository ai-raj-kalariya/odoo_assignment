# -*- coding: utf-8 -*-

from odoo import api, models, fields


class BulkUploadBook(models.TransientModel):
    """
    For create multiple books using text field and this multiple book
    create to separate product in product model
    """
    _name = "bulk.upload.book"
    _description = "Bulk upload book"
    _rec_name = "book_names"

    book_names = fields.Text(
        string="Book Names",
        required=True
    )
    author_id = fields.Many2one(
        comodel_name='res.partner',
        string="Author"
    )
    category = fields.Char(
        string="Category"
    )
    price = fields.Float(
        string="Price"
    )
    created_book_count = fields.Integer(
        compute='_compute_created_book_count',
        string="Created Books"
    )
    product_ids = fields.Many2many(
        'product.template',
        string="Created Product"
    )

    def create_book(self):
        """
        Using split() method return separate book which is written in the book text field
        and if not exist already in product then create product,
        """
        for book in self.book_names.split(","):
            if not self.env['product.template'].search([('name', '=', book)]):
                products = self.env['product.template'].create({
                    'name': book,
                    'author_id': self.author_id.id,})
                self.product_ids = [(4, products.id)]

                # showing notification when book is created
                self.env['bus.bus']._sendone(
                    self.env.user.partner_id, 'simple_notification', {
                    'type': 'success',
                    'message': f"{products.name} is created.",
                    })

    def action_created_book(self):
        """
        This method is used to open list views and form view when click on smart button.
        If only one product created then redirect on form view else show list view and form view.
        """
        action = {
            'name': 'Created Books',
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'product.template',
            'domain': [('id', 'in', self.product_ids.ids)]
        }
        if len(self.product_ids) == 1:
            book_id = self.env['product.template'].search([('name', '=', self.product_ids.name)])
            action.update({'view_mode': 'form', 'res_id': book_id.id})
        return action

    def revert_changes(self):
        """
        This method revert (delete) the all product which is in current record
        and created using bulk_upload_book model.
        """
        self.product_ids.unlink()

    @api.depends('author_id')
    def _compute_created_book_count(self):
        """
        This compute method return the len of created book in current record.
        """
        for book in self:
            book.created_book_count = len(book.product_ids) if book and book.product_ids else 0.0
