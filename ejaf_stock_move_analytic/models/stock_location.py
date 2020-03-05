# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockLocation(models.Model):
    _inherit = 'stock.location'

    analytic_account_id = fields.Many2one(comodel_name="account.analytic.account",
                                          string="Analytic Account")
