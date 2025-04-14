# -*- coding: utf-8 -*-

from odoo import models


class StockRule(models.Model):
    """
    Inherits the 'stock.rule' model to inject 'job_name' from procurement
    values into stock move values. This helps maintain job/project
    context during stock transfers.
    """
    _inherit = 'stock.rule'

    def _get_stock_move_values(self, product_id, product_qty, product_uom,
                               location_dest_id, name, origin, company_id, values):
        """
        Override to add 'job_name' to the stock move values dictionary,
        based on values passed during procurement rule execution.

        :param values: Dictionary of additional values passed from procurement,
                       expected to include 'job_name' if present.
        :return: Updated dictionary with 'job_name' key added.
        """
        res = super()._get_stock_move_values(product_id, product_qty, product_uom,
                                             location_dest_id, name, origin, company_id, values)
        res['job_name'] = values.get('job_name', False)
        return res
