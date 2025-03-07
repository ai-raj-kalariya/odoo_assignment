# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    library_assistant = fields.Many2one(
        'hr.employee',
        string="Library Assistant"
    )
    workers_ids = fields.Many2many(
        'hr.employee',
        string="Worker"
    )

    @api.constrains('library_assistant')
    def _check_library_assistant(self):
        if self.search_count([('library_assistant', '=', self.library_assistant.id)]) > 1:
            raise ValidationError("A Library Assistant can be assigned to only one warehouse.")

    # @api.constrains('workers_ids')
    # def _check_unique_workers(self):
    #     if len(set(self.workers_ids.ids)) < len(self.workers_ids.ids):
    #         raise ValidationError("Duplicate Workers are not allowed.")
