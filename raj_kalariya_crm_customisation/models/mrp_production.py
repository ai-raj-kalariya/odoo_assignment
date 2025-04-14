# -*- coding: utf-8 -*-

from odoo import models, fields


class MrpProduction(models.Model):
    """
    This model extends the 'mrp.production' model and add new field.
    """
    _inherit = 'mrp.production'

    job_name = fields.Char(
        related='move_dest_ids.job_name',
        string='Job Name'
    )
