# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    borrowing_limit = fields.Integer(
        string="Borrowing limit"
    )