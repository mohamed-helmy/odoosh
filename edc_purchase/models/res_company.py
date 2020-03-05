# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _
from datetime import date, datetime
from odoo.exceptions import UserError


class ResCompany(models.Model):
    _inherit = 'res.company'

    purchase_terms_cond = fields.Html(string="Purchase Terms And Conditions", translate=True)
