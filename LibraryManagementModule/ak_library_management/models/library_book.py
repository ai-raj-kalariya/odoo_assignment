# -*- coding: utf-8 -*-
"""This is library book model"""
from odoo import models, fields


class LibraryBook(models.Model):
    """For create a book and select state for book available or borrowed
        and select category """
    _name = "library.book"
    _description = "Library book"

    name = fields.Char(
        string = "Book Title")
    author = fields.Char(
        string = "Author Name")
    isbn = fields.Char(
        string = "ISBN Number")
    publication_date = fields.Date(
        string = "Date of Publication")
    # Show state book available or borrowed
    state = fields.Selection([
        ('available', 'Available'),
        ('borrowed', 'Borrowed')
    ], string = "Book Availability")
    category_id = fields.Many2one(
        comodel_name = 'library.book.category',
        string = "Category")
    description = fields.Text(
        string = "Book Summary")
    # when we select category then automatically selected tags
    tag_ids = fields.Many2many(
        related = "category_id.tag_ids",
        string = "Tags")
    library_id = fields.Many2one(
        "library.library",
        string="Library")
