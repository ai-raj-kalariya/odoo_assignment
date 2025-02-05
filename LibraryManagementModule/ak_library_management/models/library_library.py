# -*- coding: utf-8 -*-

from odoo import models, fields


class Library(models.Model):
    """For create a library and also create a book using tab"""
    _name = "library.library"
    _description = "library"

    name = fields.Char(
        string = "Name")
    location = fields.Char(
        string = "Location")
    capacity = fields.Integer(
        string = "Capacity")
    notes = fields.Text(
        string = "Notes")
    # one to many field for create a book using library tab
    book_ids = fields.One2many(
        comodel_name="library.book", # parent model
        inverse_name="library_id",   # relation field
         string = "Book")