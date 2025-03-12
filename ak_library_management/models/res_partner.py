# -*- coding: utf-8 -*-

from odoo import models, fields


class ResPartner(models.Model):
    """
    This model is inherit res partner model and add
    new field in this res partner.
    """
    _inherit = 'res.partner'

    not_trust_worthy = fields.Boolean(
        string="Not Trust Worthy"
    )
    is_member = fields.Boolean(
        string="Is Member"
    )
