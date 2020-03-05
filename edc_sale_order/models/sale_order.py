# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _
from datetime import date, datetime
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('order_line', 'order_line.analytic_tag_ids')
    def _compute_has_analytic_tags(self):
        for record in self:
            analytic_tag_ids = record.order_line.mapped('analytic_tag_ids')
            record.has_analytic_tags = True if len(analytic_tag_ids) > 0 else False

    inventory_note = fields.Char(string="Inventory Note")
    contract_no = fields.Char(string="Contract No")
    has_analytic_tags = fields.Boolean(compute=_compute_has_analytic_tags, store=True)
    project_id = fields.Many2one(comodel_name="account.analytic.tag", string="Project")
    note = fields.Html('Terms and conditions')
    bill_to = fields.Html(string="Bill to", compute="_compute_bill_to", store=True)
    total_without_discount = fields.Float(compute="_compute_total_without_discount", store=True)
    total_discount = fields.Float(string="Total Discount", compute='_compute_amount_discount', store=True)

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

    @api.depends('order_line', 'order_line.unit_disc')
    def _compute_amount_discount(self):
        for order in self:
            if order.order_line:
                order.total_discount = sum([line.unit_disc for line in order.order_line])
            else:
                order.total_discount = 0.0

    @api.depends('total_discount', 'amount_untaxed')
    def _compute_total_without_discount(self):
        for order in self:
            order.total_without_discount = order.amount_untaxed + order.total_discount

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['inventory_note'] = self.inventory_note
        invoice_vals['contract_no'] = self.contract_no
        return invoice_vals

    @api.model
    def create(self, values):
        result = super(SaleOrder, self).create(values)
        if result.project_id and result.order_line:
            result.order_line.sudo().write({'analytic_tag_ids': [(4, result.project_id.id)]})
        return result

    def write(self, values):

        result = super(SaleOrder, self).write(values)
        for record in self:
            if record.project_id and record.order_line:
                record.order_line.sudo().write({'analytic_tag_ids': [(4, record.project_id.id)]})
        return result
