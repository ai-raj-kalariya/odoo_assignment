# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request

class WebsiteCustomController(http.Controller):

    @http.route('/custom', type='http', auth='public', website=True)
    def custom_page(self, **kwargs):
        return request.render("ak_library_management.custom_web_page_template")

    @http.route('/custom/button_action', type='http', auth='public', website=True)
    def button_action(self, **kwargs):
        return request.redirect('/contactus')