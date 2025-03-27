# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


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
        contacts = request.env['res.partner'].search([])
        return request.render('ak_library_management.custom_contact_kanban_template',
                              {'contacts': contacts})

    @http.route('/contacts/<model("res.partner"):partner>/',
                type='http', auth='public', website=True)
    def partner_detail(self, partner):
        """
        Render a detailed view of a specific contact.
        When a user clicks on a contact card, this method retrieves the contact details
        and renders them using a custom detail template.
        :param partner: The `res.partner` record retrieved from the URL slug.
        :return: Rendered HTML template displaying the details of the selected contact.
        """
        return request.render('ak_library_management.custom_contact_detail_template',
                              {'partner': partner})
