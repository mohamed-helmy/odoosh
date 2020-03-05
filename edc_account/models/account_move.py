# -*- coding: utf-8 -*-
import logging
from odoo import fields, models, api, exceptions, _
_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    inventory_note = fields.Char(string="Inventory Note")
    contract_no = fields.Many2one('product.pricelist', string="Contract No")
    reference_no = fields.Char(string=" Reference No")
    cost_center_id = fields.Many2one('account.analytic.account')
    project_id = fields.Many2one('account.analytic.tag')
    bill_to = fields.Html(string="Bill to", compute="_compute_bill_to", store=True)

    @api.depends('partner_id', 'partner_id.child_ids')
    def _compute_bill_to(self):
        for order in self:
            invoice_address = order.partner_id.child_ids.filtered(lambda ch: ch.type == 'invoice')
            if invoice_address:
                order.bill_to = invoice_address[0].with_context({'html_format': True})._get_custom_address(
                    type='invoice')
            else:
                order.bill_to = order.partner_id.with_context({'html_format': True})._get_custom_address(
                    type='invoice')

    @api.model
    def create(self, values):
        result = super(AccountMove, self).create(values)
        if result.cost_center_id and result.invoice_line_ids:
            result.invoice_line_ids.sudo().write({'analytic_account_id': result.cost_center_id.id})
        if result.project_id and result.invoice_line_ids:
                    result.invoice_line_ids.sudo().write({'analytic_tag_ids': [(4, result.project_id.id)]})
        return result

    def write(self, values):

        result = super(AccountMove, self).write(values)
        for record in self:

            if record.cost_center_id and record.invoice_line_ids:
                record.invoice_line_ids.sudo().write({'analytic_account_id': record.cost_center_id.id})
            if record.project_id and record.invoice_line_ids:
                record.invoice_line_ids.sudo().write({'analytic_tag_ids': [(4, record.project_id.id)]})
        return result
