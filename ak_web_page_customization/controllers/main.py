# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import re
from odoo.tools.image import image_data_uri
from odoo.exceptions import ValidationError


class WebsiteCustomController(http.Controller):
    """
    Custom Website Controller for displaying res.partner records.
    """
    @http.route('/contacts', type='http', auth='public', website=True)
    def list_contacts(self):
        """
        Render a custom contact list view using a Kanban-style template.
        This method fetches all records from the `res.partner` model and passes them
        to the custom template for rendering.
        :return: Rendered HTML template displaying the list of contacts.
        """
        contacts = request.env['res.partner'].sudo().search([])
        return request.render('ak_web_page_customization.custom_contact_kanban_template',
                              {'contacts': contacts})

    @http.route('/contacts/<slug>',
                type='http', auth='public', website=True)
    def partner_detail(self, **params):
        """
        Render a detailed view of a specific contact.
        When a user clicks on a contact card, this method retrieves the contact details
        and renders them using a custom detail template.
        :param partner: The `res.partner` record retrieved from the URL slug.
        :return: Rendered HTML template displaying the details of the selected contact.
        """
        partner = request.env['res.partner'].sudo().search([('contact_slug', '=', params['slug'])])
        return request.render('ak_web_page_customization.custom_contact_form_template',
                              {'partner': partner})

    @http.route('/contact/update', type='json', auth='user', website=True)
    def update_contact(self, **params):
        """
        Update the selected contact if valid phone or email else showing validation.
        Check email and phone are unique or not.
        If all condition satisfy then update contact.
        :params: retrieve `res.partner` data from form view.
        :return: None
        """
        contact = request.env['res.partner'].sudo().search([('id', '=', params.get('contact_id'))])
        params.pop('contact_id')
        domain = [
            ('id', '!=', contact.id),
            '|',
            ('email', '=', params['email']),
            ('phone', '=', params['phone']),
        ]
        duplicate = request.env['res.partner'].sudo().search(domain)
        if not (params['email'] and params['phone'] and params['name']):
            raise ValidationError("Name or Email or Phone are required.")

        valid_email = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', params['email'])
        valid_phone = re.match(r"^\+?[1-9][0-9]{7,14}$", params['phone'])

        if not valid_email:
            raise ValidationError("Invalid Email")
        if not valid_phone:
            raise ValidationError("Invalid Phone")
        if duplicate:
            raise ValidationError("A contact with this email or phone already exists.")

        # create record in contact
        for key, val in params.items():
            contact.write({key: val})
        return
