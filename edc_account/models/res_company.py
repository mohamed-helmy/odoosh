# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    invoice_terms = fields.Html(string='Default Terms and Conditions', translate=True)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    invoice_terms = fields.Html(related='company_id.invoice_terms', string="Terms & Conditions", readonly=False)
