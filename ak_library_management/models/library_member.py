# -*- coding: utf-8 -*-
"""This is library member model"""
from odoo import _, api, models, fields
from setuptools.dist import sequence


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
    membership_no = fields.Integer(
        string="Membership Number"
    )


# @api.model_create_multi
# def create(self, vals_list):
#     sequence_code = 'library.member'
#     for vals in vals_list:
#         vals['name'] = self.env['ir.sequence'].next_by_code(sequence_code) or _('New')
#     # print("\n\n\n\n :::::::::", vals_list)
#     return super().create(vals_list)
