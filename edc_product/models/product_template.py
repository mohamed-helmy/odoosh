# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _
from datetime import date, datetime
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_main_equipment_id = fields.Many2one(comodel_name="product.equipment", string="Main Equipment", domain=[('type', '=', 'main')])
    product_sub_equipment_id = fields.Many2one(comodel_name="product.equipment", string="Sub Equipment", domain=[('type', '=', 'sub')])
    product_manufacturer_id = fields.Many2one(comodel_name="product.manufacturer", string="Manufacture")
    product_model_id = fields.Many2one(comodel_name="product.model", string="Model")
    product_pressure = fields.Char(string="Pressure")
    product_size = fields.Char(string="Size")
    product_equipment_model_id = fields.Many2one(comodel_name="product.equipment.model", string="Equipment Model")
    second_barcode = fields.Char(string="P/N2")
    default_code = fields.Char(default=lambda self: self.env['ir.sequence'].next_by_code('product.default.code'))
    _sql_constraints = [
        ('unique_second_barcode', 'unique (second_barcode)', 'P/N2 must be unique !')]

