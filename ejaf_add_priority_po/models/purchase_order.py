# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _
from datetime import date, datetime
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    priority = fields.Selection(string="Priority", index=True,
                                selection=[('0', 'Very Low'),
                                           ('1', 'Low'),
                                           ('2', 'Normal'),
                                           ('3', 'High'),
                                           ('4', 'Very High')])
