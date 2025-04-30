# -*- coding: utf-8 -*-

from odoo import api, models, fields
from odoo.exceptions import ValidationError


class ProductCatalogWizard(models.TransientModel):
    """
    """
    _name = 'product.catalog.wizard'
    _description = 'Product catalog wizard'

    catalog_style = fields.Selection([
        ('style1', 'Style 1'),
        ('style2', 'Style 2'),
    ], string="Catalog Style",
       required=True,
        default='style2'
    )
    product_ids = fields.Many2many(
        comodel_name='product.product',
        string="Product",
        default=lambda self: self._default_product_id()
    )
    page_break_after = fields.Integer(
        string="Page Break After",
    )


    def _default_product_id(self):
        return self.env['product.product'].search([('id','in',[15,16,23,36,18,19,20,21,50,22,11])])

    @api.constrains('page_break_after')
    def _check_page_limit(self):
        """
        """
        if self.page_break_after > 5:
            raise ValidationError("More than 5 product can not print in single page.")
        if self.page_break_after < 1 and self.catalog_style != 'style2':
            raise ValidationError("At least 1 select in page break after field.")

    def action_print_pdf(self):
        self.ensure_one()
        if self.catalog_style == 'style1':
            return self.env.ref('ak_product_cataloge_pdf.custom_product_catalog_style_1_report_id').report_action(self.id)
        return self.env.ref('ak_product_cataloge_pdf.custom_product_catalog_style_2_report_id').report_action(self.id)

    def action_cancel(self):
        """
        when click cancel button then current record is deleted.
        """
        rec = self.env.context.get('active_id')
        self.env["borrow.transaction.history.wizard"].browse(rec).unlink()
