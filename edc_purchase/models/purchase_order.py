# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    mr_no = fields.Char(string="MR.NO")
    quotation_no = fields.Char(string="Quotation NO")
    ship_to = fields.Html(string="Ship to / Delivery point", compute="_compute_ship_to", store=True)
    bill_to = fields.Html(string="Bill to", compute="_compute_bill_to", store=True)
    total_discount = fields.Float(string="Total Discount", compute='_compute_amount_discount', store=True)
    total_without_discount = fields.Float(compute="_compute_total_without_discount", store=True)
    cost_center_id = fields.Many2one('account.analytic.account')
    project_id = fields.Many2one('account.analytic.tag')

    @api.depends('partner_id', 'partner_id.child_ids')
    def _compute_bill_to(self):
        for order in self:
            invoice_address = order.partner_id.child_ids.filtered(lambda ch: ch.type =='invoice')
            if invoice_address:
                order.bill_to = invoice_address[0].with_context({'html_format': True})._get_custom_address(type='invoice')
            else:
                order.bill_to = order.partner_id.with_context({'html_format': True})._get_custom_address(
                    type='invoice')

    @api.depends('picking_type_id', 'picking_type_id.warehouse_id', 'picking_type_id.warehouse_id.partner_id',
                 'picking_type_id.warehouse_id.partner_id.child_ids')
    def _compute_ship_to(self):
        for order in self:
            if order.picking_type_id.warehouse_id and order.picking_type_id.warehouse_id.partner_id:
                delivered_address = order.picking_type_id.warehouse_id.partner_id.child_ids.filtered(lambda ch: ch.type =='delivery')
                if delivered_address:
                    order.ship_to = delivered_address[0].with_context({'html_format': True})._get_custom_address(type='delivery')
                else:
                    order.ship_to = order.picking_type_id.warehouse_id.partner_id.with_context({'html_format': True})._get_custom_address(type='delivery')

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

    @api.model
    def create(self, values):
        result = super(PurchaseOrder, self).create(values)
        if result.cost_center_id and result.order_line:
            result.order_line.sudo().write({'account_analytic_id': result.cost_center_id.id})
        if result.project_id and result.order_line:
            result.order_line.sudo().write({'analytic_tag_ids': [(4, result.project_id.id)]})
        return result

    def write(self, values):

        result = super(PurchaseOrder, self).write(values)
        for record in self:

            if record.cost_center_id and record.order_line:
                record.order_line.sudo().write({'account_analytic_id': record.cost_center_id.id})
            if record.project_id and record.order_line:
                record.order_line.sudo().write({'analytic_tag_ids': [(4, record.project_id.id)]})
        return result


