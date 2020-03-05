# -*- coding: utf-8 -*-
from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    rfq_name = fields.Char('Rfq Reference', default='New', required=True, select=True, copy=False,
                           help="Unique number of the purchase order, "
                                "computed automatically when the purchase order is created.")
    po_sequence = fields.Char('PO Sequence')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            name = self.env['ir.sequence'].next_by_code('purchase.order.quot') or 'New'
            vals['rfq_name'] = vals['name'] = name

        return super(PurchaseOrder, self).create(vals)

    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        for order in self:
            if order.po_sequence:
                order.write({'name': order.po_sequence})
            else:
                new_name = self.env['ir.sequence'].next_by_code('purchase.order.confirmed') or '/'
                order.write({'name': new_name})
            self.picking_ids.write({'origin': order.name})
            if self.picking_ids:
                for pick in self.picking_ids:
                    pick.move_lines.write({'origin': order.name})
        return res

    def button_draft(self):
        res = super(PurchaseOrder, self).button_draft()
        if self.rfq_name:
            self.write({'po_sequence': self.name})
            self.write({'name': self.rfq_name})

        return res