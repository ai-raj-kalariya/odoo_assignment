# -*- coding: utf-8 -*-

from odoo import api, models, fields


class ResUsers(models.Model):
    """
    This model is inherit res users model and add
    new field in this res users.
    """
    _inherit = 'res.users'

    is_manager = fields.Boolean(
        string="Is Manager"
    )
