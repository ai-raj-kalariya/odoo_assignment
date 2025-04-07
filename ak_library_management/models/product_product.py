# -*- coding: utf-8 -*-

from odoo import _, api, models, fields
from odoo.exceptions import ValidationError


class ProductProduct(models.Model):

    _inherit = "product.product"

    seller_ids = fields.One2many('product.supplierinfo',
                                 'Vendors', depends_context=('company',))
    variant_seller_ids = fields.One2many('product.supplierinfo', 'product_tmpl_id')