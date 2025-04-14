# -*- coding: utf-8 -*-

from odoo import api, models, fields


class SaleOrder(models.Model):
    """
    Inherits the 'sale.order' model to:
    - Add a 'job_name' field.
    - Sync job name from opportunity.
    - Pass job name to project, delivery, and invoice flows.
    """
    _inherit = 'sale.order'

    job_name = fields.Char(
        string="Job Name",
        compute='_compute_job_name',
        store=True
    )

    @api.depends('opportunity_id')
    def _compute_job_name(self):
        """
        This method print an opportunity name to the job name field.
        """
        for lead in self:
            if lead.opportunity_id:
                    lead.job_name = lead.opportunity_id.name

    def action_confirm(self):
        """
        Override the default sale order confirmation.
        If a job name is set, update related project names to follow the
        format: "<sale order number> - <job name>".
        """
        res = super(SaleOrder, self).action_confirm()

        for order in self:
            if not order.job_name:
                continue
            job_name = order.job_name
            sales_number = order.name
            full_project_name = f"{sales_number} - {job_name}"
            projects = self.env['project.project'].search([
                ('sale_order_id', '=', order.id),
                ('name', '!=', full_project_name)
            ])
            for project in projects:
                project.name = full_project_name
        return res


    def _get_action_view_picking(self, pickings):
        """
        Inject the job name into the context when viewing delivery pickings.
        """
        action = super()._get_action_view_picking(pickings)
        action['context']['default_job_name'] = self.job_name
        return action

    def _prepare_invoice(self):
        """
        Add the job name to the invoice when it's created from the sale order.
        """
        vals = super()._prepare_invoice()
        vals['job_name'] = self.job_name
        return vals
