# -*- coding: utf-8 -*-

from odoo import models, fields


class LibraryMember(models.Model):
    """For create a member"""
    _name = "library.member"
    _description = "Library member"

    name=fields.Char(
        string = "Member Name")
    email = fields.Char(
        string = "Email ID")
    phone = fields.Char(
        string = "Contact Number")
    membership_date = fields.Date(
        string = "Membership Start Date")
