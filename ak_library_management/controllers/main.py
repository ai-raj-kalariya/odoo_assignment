# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request

class WebsiteCustomController(http.Controller):

    @http.route('/custom', type='http', auth='public', website=True)
    def custom_page(self, **kwargs):
        employee=request.env['hr.employee'].search([])
        print("\n\nemployee:::::",employee,"\n\n")
        return request.render("ak_library_management.custom_web_page_template",{'employee':employee})

    @http.route('/custom/button_action', type='http', auth='public', website=True)
    def button_action(self, **kwargs):
        return request.redirect('/contactus')

    @http.route('/contacts', type='http', auth='public', website=True)
    def list_contacts(self, **kwargs):
        contacts = request.env['res.partner'].search([])
        print("\n\ncontacts:::::",contacts,"\n\n")
        return request.render('ak_library_management.contact_kanban_template', {'contacts': contacts})

    @http.route('/contact/<int:partner_id>', type='http', auth='public', website=True)
    def contact_details(self, partner_id, **kwargs):
        contact = request.env['res.partner'].browse(partner_id)
        print("\n\ncontact_partner::::::",contact,"\n\n")
        return request.render('ak_library_management.contact_detail_template', {'contact': contact})

