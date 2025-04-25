# -*- coding: utf-8 -*-
"""This is product template model inherit from sale/product"""
from datetime import date, timedelta
from odoo import _, api, models, fields
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    """This model is inherit product.template model from sale module and add
        new field in this product template."""
    _inherit = "product.template"

    is_out_of_stock = fields.Boolean(
        string="Not Available (Out of Stock)"
    )
    out_of_stock_message = fields.Html(
        string="Custom Out-of-Stock Message"
    )
