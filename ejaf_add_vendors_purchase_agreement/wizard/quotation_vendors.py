# -*- coding: utf-8 -*-
import logging

from odoo import fields, models, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class QuotationVendors(models.TransientModel):
    _name = 'quotation.vendors'

    vendors_ids = fields.Many2many('res.partner', string='Vendors')

    def create_quotations(self):
        active_id = self.env.context.get('active_id')
        if active_id:
            run_data = self.env['purchase.requisition'].browse(active_id)
        if not self.vendors_ids:
            raise UserError(_("You must select Vendor(s) to create Quotation(s)."))

        for vendor in self.vendors_ids:
            res = {
                'requisition_id': active_id,
                'partner_id': vendor.id,
                'user_id': run_data.user_id.id,
                'picking_type_id': run_data.picking_type_id.id,
                'currency_id': run_data.currency_id.id,
                # 'date_order': fields.Datetime.from_string(run_data.ordering_date),
                'company_id': run_data.company_id.id,
            }
            request_line_ids = []
            for line in run_data.line_ids:
                request_line_ids.append((0, 0, {
                    'product_id': line.product_id.id,
                    'product_qty': line.product_qty,
                    'product_uom': line.product_uom_id.id,
                    'name': line.product_id.description or line.product_id.name,
                    'date_planned': line.schedule_date if line.schedule_date else fields.Datetime.now(),
                    'account_analytic_id': line.account_analytic_id.id,
                    'analytic_tag_ids': [(6, 0, line.analytic_tag_ids.ids)],
                    'price_unit': line.price_unit,

                }))
            res.update({'order_line': request_line_ids})

            self.env['purchase.order'].sudo().create(res)
        return {'type': 'ir.actions.act_window_close'}

    def cancel_request(self):
        return {'type': 'ir.actions.act_window_close'}
