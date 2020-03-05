# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _
from datetime import date, datetime
from odoo.exceptions import UserError


class AccountMoveline(models.Model):
    _inherit = 'account.move.line'

    unit_disc = fields.Float(compute='_compute_amount_discount_unit')

    @api.depends('discount', 'product_id',
                 'price_unit', 'quantity')
    def _compute_amount_discount_unit(self):
        for record in self:
            if record.product_id:
                record.unit_disc = (record.price_unit / 100 * record.discount) * record.quantity
            else:
                record.unit_disc = False

    def _get_new_computed_name(self):
        self.ensure_one()
        if not self.product_id:
            return ''

        if self.partner_id.lang:
            product = self.product_id.with_context(lang=self.partner_id.lang)
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
    def _onchange_product_id(self):
        result = super(AccountMoveline, self)._onchange_product_id()
        for line in self:
            if not line.product_id or line.display_type in ('line_section', 'line_note'):
                continue
            line.name = line._get_new_computed_name()
        return result
