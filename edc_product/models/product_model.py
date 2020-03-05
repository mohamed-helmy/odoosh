# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _
from datetime import date, datetime
from odoo.exceptions import UserError


class ProductModel(models.Model):
    _name = 'product.model'
    _rec_name = 'name'

    name = fields.Char(string="Name", required=True)
