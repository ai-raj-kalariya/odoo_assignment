# -*- coding: utf-8 -*-

from odoo import models


class SaleOrderLine(models.Model):
    """
    Inherits 'sale.order.line' to:
    - Add 'job_name' from sale order into the procurement values,
    enabling job-based tracking in downstream stock or manufacturing flows.
    """
    _inherit = 'sale.order.line'

    def _prepare_procurement_values(self, group_id):
        """
        Add 'job_name' from the parent sale order to the procurement values.
        This allows downstream operations like stock rules or manufacturing
        to access the job context.
        """
        values = super()._prepare_procurement_values(group_id)
        values['job_name'] = self.order_id.job_name
        return values
