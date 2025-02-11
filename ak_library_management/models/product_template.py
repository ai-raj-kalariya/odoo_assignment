# -*- coding: utf-8 -*-
"""This is product template model inherit from sale/product"""
from odoo import models, fields


class ProductTemplate(models.Model):
    """This model is inherit product.template model from sale module and add
        new field in this product template."""
    _inherit = "product.template"

    is_library_book = fields.Boolean(
        string="Library Book")
    author_id = fields.Many2one(
        comodel_name='res.partner',
        string="Author")
    publisher = fields.Char(
        string="Publisher")
    edition = fields.Char(
        string="Edition")
    published_date = fields.Date(
        string="Published_date")
    pages = fields.Integer(
        string="Pages")
    available = fields.Boolean(
        string="Available")
    # overwrite ISBN Number to existing field barcode label
    barcode = fields.Integer(
        string="ISBN Number")
    state = fields.Selection([
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('reserved', 'Reserved'),
    ], string="Book Availability")

    def is_borrowed(self):
        """This method is convert state into borrowed state"""
        self.write({'state': 'borrowed'})

    def is_available(self):
        """This method is convert state into available state"""
        self.write({'state': 'available'})
