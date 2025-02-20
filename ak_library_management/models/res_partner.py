# -*- coding: utf-8 -*-

from odoo import api, models, fields
from setuptools.extern import names


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
    display_name = fields.Char(
        compute='_compute_display_name',
        store=True)
    #
    # @api.depends('name','phone')
    # def name_get(self):
    #     result=[]
    #     for record in self:
    #         name= record.name
    #         if record.phone:
    #             name += f" ({record.phone})"
    #         result.append((record.id, name))
    #     return result
    #
    #
    # @api.depends('name', 'phone')  # Fields that trigger recomputation
    # def _compute_display_name(self):
    #     for record in self:
    #         record.display_name = f"{record.name} ({record.phone})" if record.phone else record.name
    #
