# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteCustomController(WebsiteSale):

    def sitemap_products(env, rule, qs):
        return super().sitemap_products()

    @http.route('/shop/<model("product.template"):product>/', type='http', auth='public', website=True,
                sitemap=sitemap_products, readonly=True)
    def list_out_of_stock_product(self, product, category='', search='', **kwargs):
        """
        Show custom out-of-stock page or standard product page.
        """
        if not request.website.has_ecommerce_access():
            return request.redirect('/web/login')

        if product.is_out_of_stock:
            return request.render('ak_out_of_stock_page.custom_out_of_stock_template', {
                'products': product
            })
        return super().product(product, category=category, search=search, **kwargs)


    # @http.route('/dashboard', type='http', auth='public', website=True)
    # def get_dashboard(self):
    #     """
    #     """
    #     total_amount = request.env['account.move'].sudo().read_group(domain=[('state', '=', 'posted')],
    #                                                           fields=['amount_untaxed_in_currency_signed:sum'],
    #                                                           groupby=[])
    #     paid = request.env['account.payment'].sudo().read_group(domain=[('state', '=', 'paid')],
    #                                                             fields=['amount_company_currency_signed:sum'],
    #                                                             groupby=[])
    #     amount_due = request.env['account.move'].sudo().read_group(domain=[],
    #                                                                fields=['amount_residual:sum'],
    #                                                                groupby=[])
    #
    #     quotations = request.env['sale.order'].sudo().read_group(domain=[('state', '=', 'draft')],
    #                                                              fields=['amount_total:sum'],
    #                                                              groupby=[])
    #
    #     conformed = request.env['sale.order'].sudo().read_group(domain=[('state', '=', 'sale')],
    #                                                             fields=['amount_total:sum'],
    #                                                             groupby=[])
    #     canceled = request.env['sale.order'].sudo().read_group(domain=[('state', '=', 'cancel')],
    #                                                            fields=['amount_total:sum'],
    #                                                            groupby=[])
    #
    #     delivery = request.env['stock.picking'].sudo().read_group(domain=[('state', '=', 'draft')],
    #                                                               fields=['name:count'],
    #                                                               groupby=[])
    #
    #     delivered = request.env['stock.picking'].sudo().read_group(domain=[('state', '=', 'done')],
    #                                                               fields=['name:count'],
    #                                                               groupby=[])
    #
    #     pending = request.env['stock.picking'].sudo().read_group(domain=[('state', '!=', 'done'),('state', '!=', 'cancel')],
    #                                                               fields=['name:count'],
    #                                                               groupby=[])
    #
    #     return request.render('ak_out_of_stock_page.custom_my_dashboard_template',
    #                           {'total_amount':total_amount[0]['amount_untaxed_in_currency_signed'],
    #                            'paid': paid[0]['amount_company_currency_signed'],
    #                            'amount_due': amount_due[0]['amount_residual'],
    #                            'quotations': quotations[0]['amount_total'],
    #                            'conformed': conformed[0]['amount_total'],
    #                            'canceled': canceled[0]['amount_total'],
    #                            'delivery': delivery[0]['name'],
    #                            'delivered': delivered[0]['name'],
    #                            'pending':pending[0]['name'],}
    #                           )
