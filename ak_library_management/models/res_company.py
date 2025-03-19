# -*- coding: utf-8 -*-

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    borrowing_limit = fields.Integer(
        string="borrowing_limit"
    )
