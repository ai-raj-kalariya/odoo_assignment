# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductTemplate(models.Model):

     _inherit = "product.template"

     is_library_book = fields.Boolean(
          string = "Library Book")
     author = fields.Char(
          string = "Author")
     publisher = fields.Char(
          string = "Publisher")
     edition = fields.Char(
          string = "Edition")
     published_date = fields.Char(
          string = "Published_date")
     pages = fields.Integer(
          string = "Pages")
     available = fields.Boolean(
          string = "Available")
     barcode = fields.Integer(
         string = "ISBN Number")
