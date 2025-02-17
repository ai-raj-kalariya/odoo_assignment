# -*- coding: utf-8 -*-
"""This is library member model"""
from odoo import _, api, models, fields


class LibraryMember(models.Model):
    """For create a member"""
    _name = "library.member"
    _description = "Library member"

    membership_no = fields.Char(
        readonly=True,
        default=lambda self: _('New')
    )
    name = fields.Char(
        string="Member Name",
        required=True,
    )
    email = fields.Char(
        string="Email ID"
    )
    phone = fields.Char(
        string="Contact Number"
    )
    membership_date = fields.Date(
        string="Membership Start Date"
    )

    @api.model_create_multi
    def create(self, vals_list):
        """This method create a member sequence for library member"""
        for val in vals_list:
            val['membership_no'] = self.env['ir.sequence'].next_by_code('library.member') or _('New')
            return super().create(val)
