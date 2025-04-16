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
        contacts = request.env['res.partner'].sudo().search([])
        return request.render('ak_library_management.custom_contact_kanban_template',
                              {'contacts': contacts})

    @http.route('/contacts/<slug>',
                type='http', auth='public', website=True)
    def partner_detail(self, **args):
        """
        Render a detailed view of a specific contact.
        When a user clicks on a contact card, this method retrieves the contact details
        and renders them using a custom detail template.
        :param args: The `res.partner` record retrieved from the URL slug.
        :return: Rendered HTML template displaying the details of the selected contact.
        """
        partner = request.env['res.partner'].sudo().search([('contact_slug', '=', args['slug'])])
        return request.render('ak_library_management.custom_contact_detail_template',
                              {'partner': partner})

    @http.route('/customer', type='http', auth='public', website=True)
    def customer_detail(self, **kwargs):
        """
        Renders the customer detail page.
        This route serves an HTML template that displays customer details.
        Returns:Rendered HTML page of customer form.
        """
        return request.render('ak_library_management.custom_customer_detail_template')

    # Fetch Customer Data using JSON
    @http.route('/customer/fetch', type='json', auth='public', csrf=False)
    def fetch_customer(self, email):
        """
        Fetch customer details based on the enter email.
        This JSON route searches for a customer in `res.partner` using the given email
        and returns essential details such as name, company, phone, and Tax ID.
        Args:
        email: The email of the customer to be fetched.
        Returns:
        dict: A dictionary containing customer details:
           - name: The customer's name.
           - company: The customer's associated company name (or "No Company" if not available).
           - phone: The customer's phone number (or "No Phone" if not available).
           - vat: The customer's Tax ID (or "No TaxID" if not available).
        """
        partner = request.env['res.partner'].sudo().search([('email', '=', email)])
        return {
            'name': partner.name,
            'company': partner.company_id.name or "No Company",
            'phone': partner.phone or "No Phone",
            'vat': partner.vat or "No TaxID",
        }
