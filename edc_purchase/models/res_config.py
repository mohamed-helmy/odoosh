# -*- coding: utf-8 -*-

from odoo import fields, models, api, exceptions, _
from datetime import date, datetime
from odoo.exceptions import UserError


class ResConfigSettungs(models.TransientModel):
    _inherit = 'res.config.settings'

    purchase_terms_cond = fields.Html(related='company_id.purchase_terms_cond', string="Purchase Terms And Conditions",
                                      readonly=False)
