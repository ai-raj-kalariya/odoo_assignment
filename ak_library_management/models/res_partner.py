# -*- coding: utf-8 -*-

from odoo import models, fields, api


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
    contact_slug = fields.Char(
        string="contact slug",
        compute="_compute_contact_slug",
        store=True
    )

    @api.depends('name')
    def _compute_contact_slug(self):
        """
        This Method is used to slugify the record set and convert into string.
        """
        for record in self:
            slug_record = self.env['ir.http']._slugify(str(record))
            record.contact_slug = slug_record