# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api
_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _prepare_account_move_line(self, qty, cost, credit_account_id, debit_account_id, description):
        self.ensure_one()
        result = super(StockMove, self)._prepare_account_move_line(qty, cost, credit_account_id, debit_account_id, description)
        if self.location_dest_id.usage in ['inventory', 'production'] and self.location_dest_id.analytic_account_id:
            # Add analytic account in debit line
            for num in range(0, 2):
                if result[num][2]["account_id"] != self.product_id. \
                        categ_id.property_stock_valuation_account_id.id:
                    result[num][2].update({
                        'analytic_account_id': self.location_dest_id.analytic_account_id.id,
                    })

        return result
