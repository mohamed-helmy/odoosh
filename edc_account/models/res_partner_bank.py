# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _
from datetime import date, datetime
from odoo.exceptions import UserError


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    bank_iban = fields.Char(string="IBAN", required=True)
