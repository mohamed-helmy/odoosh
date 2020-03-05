# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

import logging

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _stock_account_prepare_anglo_saxon_out_lines_vals(self):
        result = super(AccountMove, self)._stock_account_prepare_anglo_saxon_out_lines_vals()
        for move in self:
            if move.type in ['out_invoice', 'out_refund']:
                    for line in result:
                        account_id = self.env['account.account'].sudo().browse(line.get('account_id'))
                        income_type = self.env.ref('account.data_account_type_revenue').id
                        expense_type = self.env.ref('account.data_account_type_expenses').id
                        cost_type = self.env.ref('account.data_account_type_direct_costs').id

                        if account_id.user_type_id.id not in [income_type, expense_type, cost_type]:

                            if line.get('analytic_account_id'):
                                line['analytic_account_id'] = False

                            if line.get('analytic_tag_ids'):
                                line['analytic_tag_ids'] = False
        return result

    def _stock_account_prepare_anglo_saxon_in_lines_vals(self):
        result = super(AccountMove, self)._stock_account_prepare_anglo_saxon_in_lines_vals()
        for move in self:
            if move.type in ['in_invoice', 'in_refund']:
                for line in result:
                    account_id = self.env['account.account'].sudo().browse(line.get('account_id'))
                    income_type = self.env.ref('account.data_account_type_revenue').id
                    expense_type = self.env.ref('account.data_account_type_expenses').id
                    cost_type = self.env.ref('account.data_account_type_direct_costs').id

                    if account_id.user_type_id.id not in [income_type, expense_type, cost_type]:

                        if line.get('analytic_account_id'):
                            line['analytic_account_id'] = False

                        if line.get('analytic_tag_ids'):
                            line['analytic_tag_ids'] = False
        return result


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def write(self, values):
        result = super(AccountMoveLine, self).write(values)
        if values.get('analytic_account_id'):
            self.analytic_line_ids.sudo().write({'account_id': values.get('analytic_account_id')})
        return result
