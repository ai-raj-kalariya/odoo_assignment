# -*- coding: utf-8 -*-

from odoo import models, fields

class StockPicking(models.Model):
    """
    This model extends the 'stock.picking' model and add new field.
    """
    _inherit = 'stock.picking'

    job_name = fields.Char(
        related='move_ids.job_name',
        string="Job Name"
    )
