# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    remarks = fields.Char(string="Remarks")

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

    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        res = super(StockMove, self)._prepare_move_line_vals(quantity, reserved_quant)
        res['remarks'] = self.remarks
        return res

    @api.onchange('product_id')
    def onchange_product(self):
        result = super(StockMove, self).onchange_product()
        for line in self:
            line.description_picking = line._get_new_computed_name()
        return result


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    remarks = fields.Char(string="Remarks")
