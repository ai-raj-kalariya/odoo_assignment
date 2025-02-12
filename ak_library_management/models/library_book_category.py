# -*- coding: utf-8 -*-
"""This is library book category model"""
from odoo import models, fields


class LibraryBookCategory(models.Model):
    """For create a category for book and select multiple tag
            based on M2M field"""
    _name = "library.book.category"
    _description = "Library book category"

    name = fields.Char(
        string = "Name",
        required = True
    )
    # select multiple tag
    tag_ids = fields.Many2many(
        "library.book.tags",
        "library_book_category_id",
        string = "Tags"
    )
