# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Expense(models.Model):
    _inherit = "hr.expense"

    # change default to be by company
    payment_mode = fields.Selection(default='company_account')

