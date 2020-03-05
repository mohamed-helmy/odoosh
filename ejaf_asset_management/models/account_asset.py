# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _
from datetime import date, datetime
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError



class AccountAsset(models.Model):
    _inherit = 'account.asset'

    model_name = fields.Char(string='Model Name')
    serial_no = fields.Char(string='serial NO')
    manufacturer = fields.Char(string='Manufacturer')
    warranty_start_date = fields.Date(string="Warranty Start Date")
    warranty_end_date = fields.Date(string="Warranty End Date")
    Property_stock_asset_location = fields.Many2one(comodel_name="stock.location", string="Current location",
                                                    company_dependent=True)

    @api.constrains('warranty_end_date')
    def _check_qty_work_on(self):
        for record in self:
            if record.warranty_end_date <= record.warranty_start_date:
                raise ValidationError(_('Warranty End Date must be greater than Warranty start Date!'))

