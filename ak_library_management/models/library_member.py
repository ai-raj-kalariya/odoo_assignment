# -*- coding: utf-8 -*-
"""This is library member model"""
from odoo import _, api, models, fields
from odoo.exceptions import ValidationError



class LibraryMember(models.Model):
    """
    This model represents a library member.
    It stores details about members, including their contact information,
    membership start date, and a unique membership number.
    """
    _name = "library.member"
    _description = "Library member"

    membership_no = fields.Char(
        readonly=True,
        default=lambda self: _('New')
    )
    member_id = fields.Many2one(
        comodel_name='res.partner',
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
    html= fields.Html(
        string="Description"
    )

    @api.model_create_multi
    def create(self, vals_list):
        """
        Override the create method to generate a unique sequence number
        for each new library member.
        """
        for val in vals_list:
            val['membership_no'] = (self.env['ir.sequence'].next_by_code('library.member')
                                    or _('New'))
        return super().create(vals_list)

    def action_send_mail(self):
        """
        Allows only librarians to send membership renewal emails to library members.

        :raises ValidationError: If the user is not a librarian.
        :return: A mail compose wizard action to send the email.
        """
        mail_template = self.env.ref(
            'ak_library_management.email_template_library_membership_renewal')
        if self.env.user.is_librarian:
            return {
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mail.compose.message',
                'views': [(False, 'form')],
                'view_id': False,
                'target': 'new',
                'context': {
                    'default_template_id': mail_template.id
                }
            }
        raise ValidationError("Only librarian have access this button.")
