# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountMove(models.Model):
    """
    This model extends the 'account.move' model and add new field.
    """
    _inherit = 'account.move'

    job_name = fields.Char(
        string='Job Name'
    )
