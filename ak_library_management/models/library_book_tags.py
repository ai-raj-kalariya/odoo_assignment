# -*- coding: utf-8 -*-
"""This is library book tags model"""
from odoo import models, fields


class LibraryBookTags(models.Model):
    """For create tag"""
    _name = "library.book.tags"
    _description = "Library book tags"

    name = fields.Char(
        string = "Name",
        required = True
    )
    # Use this M2O field to connect library_book_category model M2M field
    library_book_category_id = fields.Many2one(
        comodel_name = "library.book.category"
    )
    # Use this M2O field to connect library_book model M2O field
    library_book_id = fields.Many2one(
        comodel_name = "library.book" # parent model
    )
