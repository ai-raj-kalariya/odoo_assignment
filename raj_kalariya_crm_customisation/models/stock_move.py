# -*- coding: utf-8 -*-

from odoo import models, fields


class StockMoveLine(models.Model):
    """
    This model extends the 'stock.move' model and add new field.
    """
    _inherit = 'stock.move'

    job_name = fields.Char(
        string='Job Name'
    )
