# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _
from datetime import date, datetime
from odoo.exceptions import UserError


class ProductManufacturer(models.Model):
    _name = 'product.manufacturer'
    _rec_name = 'name'

    name = fields.Char(string="Name", required=True)
