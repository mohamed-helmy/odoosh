# -*- coding: utf-8 -*-


from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.tools.float_utils import float_compare


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    discount = fields.Float('Discount %')
    unit_disc = fields.Float(compute="_compute_amount_discount_unit", store=True)
    total_without_discount = fields.Float(compute="_compute_total_without_discount", store=True)

    @api.depends('discount', 'product_id',
                 'price_unit', 'product_qty')
    def _compute_amount_discount_unit(self):
        for record in self:
            if record.product_id:
                record.unit_disc = (record.price_unit / 100 * record.discount) * record.product_qty
            else:
                record.unit_disc = 0.0

    @api.depends('product_qty', 'price_unit', 'taxes_id', 'discount')
    def _compute_amount(self):
        for line in self:
            taxes = line.taxes_id.compute_all(line.price_unit, line.order_id.currency_id, line.product_qty,
                                              product=line.product_id, partner=line.order_id.partner_id)
            if line.discount:
                discount = (line.price_unit * line.discount * line.product_qty) / 100
                line.update({
                    'price_tax': taxes['total_included'] - taxes['total_excluded'],
                    'price_total': taxes['total_included'],
                    'price_subtotal': taxes['total_excluded'] - discount,
                })
            else:
                line.update({
                    'price_tax': taxes['total_included'] - taxes['total_excluded'],
                    'price_total': taxes['total_included'],
                    'price_subtotal': taxes['total_excluded'],
                })

    @api.depends('unit_disc', 'price_subtotal')
    def _compute_total_without_discount(self):
        for record in self:
            if record.product_id:
                record.total_without_discount = record.price_subtotal + record.unit_disc
            else:
                record.total_without_discount = 0.0

    def _prepare_account_move_line(self, move):
        self.ensure_one()
        if self.product_id.purchase_method == 'purchase':
            qty = self.product_qty - self.qty_invoiced
        else:
            qty = self.qty_received - self.qty_invoiced
        if float_compare(qty, 0.0, precision_rounding=self.product_uom.rounding) <= 0:
            qty = 0.0

        if self.currency_id == move.company_id.currency_id:
            currency = False
        else:
            currency = move.currency_id

        return {
            'name': '%s: %s' % (self.order_id.name, self.name),
            'move_id': move.id,
            'currency_id': currency and currency.id or False,
            'purchase_line_id': self.id,
            'date_maturity': move.invoice_date_due,
            'product_uom_id': self.product_uom.id,
            'product_id': self.product_id.id,
            'price_unit': self.price_unit,
            'discount': self.discount,
            'quantity': qty,
            'partner_id': move.partner_id.id,
            'analytic_account_id': self.account_analytic_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'tax_ids': [(6, 0, self.taxes_id.ids)],
            'display_type': self.display_type,
        }

    def _get_stock_move_price_unit(self):
        # OVERRIDE
        # Consider discount in calculations
        self.ensure_one()
        line = self[0]
        order = line.order_id
        price_unit = line.price_unit

        # Our contribution: consider discount from purchase order line
        if line.discount:
            price_unit -= (price_unit * line.discount / 100.0)
        # End of our contribution

        if line.taxes_id:
            price_unit = line.taxes_id.with_context(round=False).compute_all(
                price_unit, currency=line.order_id.currency_id, quantity=1.0, product=line.product_id,
                partner=line.order_id.partner_id
            )['total_void']
        if line.product_uom.id != line.product_id.uom_id.id:
            price_unit *= line.product_uom.factor / line.product_id.uom_id.factor
        if order.currency_id != order.company_id.currency_id:
            price_unit = order.currency_id._convert(
                price_unit, order.company_id.currency_id, self.company_id, self.date_order or fields.Date.today(),
                round=False)
        return price_unit

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
    def _product_id_change(self):
        result = super(PurchaseOrderLine, self)._product_id_change()
        for line in self:
            if not line.product_id or line.display_type in ('line_section', 'line_note'):
                continue
            line.name = line._get_new_computed_name()
        return result
