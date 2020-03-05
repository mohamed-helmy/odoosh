# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _
from datetime import date, datetime
from odoo.exceptions import UserError


class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'

    def add_quotation_vendors(self):
        self.ensure_one()
        return {
            'name': _('Add Vendors'),
            'type': 'ir.actions.act_window',
            'res_model': 'quotation.vendors',
            'view_mode': 'form',
            'target': 'new',
        }
