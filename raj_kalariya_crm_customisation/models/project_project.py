# -*- coding: utf-8 -*-

from odoo import models, fields


class ProjectProject(models.Model):
    """
    This model extends the 'project.project' model and add new field.
    """
    _inherit = 'project.project'

    job_name = fields.Char(
        string="Job Name",
        related='sale_order_id.job_name',
        store="True"
    )
    sale_order_id = fields.Many2one(
        'sale.order',
        string="Sales Order"
    )
