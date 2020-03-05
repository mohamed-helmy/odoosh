# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _
from datetime import date, datetime
from odoo.exceptions import UserError


class SaleOrderline(models.Model):
    _inherit = 'sale.order.line'

    unit_disc = fields.Float(compute='_compute_amount_discount_unit', store=True)
    total_without_discount = fields.Float(compute="_compute_total_without_discount", store=True)

    @api.depends('discount', 'product_id',
                 'price_unit', 'product_uom_qty')
    def _compute_amount_discount_unit(self):
        for record in self:
            if record.product_id:
                record.unit_disc = (record.price_unit / 100 * record.discount) * record.product_uom_qty
            else:
                record.unit_disc = False

    @api.depends('unit_disc', 'price_subtotal')
    def _compute_total_without_discount(self):
        for record in self:
            if record.product_id:
                record.total_without_discount = record.price_subtotal + record.unit_disc
            else:
                record.total_without_discount = 0.0

    def _get_new_computed_name(self):
        self.ensure_one()
        if not self.product_id:
            return ''

        if self.order_id.partner_id.lang:
            product = self.product_id.with_context(lang=self.order_id.partner_id.lang)
        else:
            product = self.product_id

        name = ''
        if product.name:
            name += product.name + '\n'
        if product.product_main_equipment_id:
            name += ' ' + product.product_main_equipment_id.name
        if product.product_size:
            name += ' ' + product.product_size
        if product.product_model_id:
            name += ' ' + product.product_model_id.name

        if product.product_manufacturer_id:
            name += ' ' + product.product_manufacturer_id.name

        return name

    @api.onchange('product_id')
    def product_id_change(self):
        result = super(SaleOrderline, self).product_id_change()
        for line in self:
            if not line.product_id or line.display_type in ('line_section', 'line_note'):
                continue
            line.name = line._get_new_computed_name()
        return result
