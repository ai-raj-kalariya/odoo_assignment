# -*- coding: utf-8 -*-
"""This is library member model"""
from odoo import api, models, fields


class LibraryMember(models.Model):
    """For create a member"""
    _name = "library.member"
    _description = "Library member"

    name = fields.Char(
        string="Member Name"
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
    membership_no = fields.Char(
        string="Membership Number"
    )
    member_id = fields.Char(
        string ="Member ID"
    )

    @api.model_create_multi
    def create(self, vals_list):
        """This method create a member sequence for library member"""
        for val in vals_list:
            val['membership_no'] = self.env['ir.sequence'].next_by_code('library.member')
            return super().create(val)
