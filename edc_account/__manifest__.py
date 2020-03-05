# -*- coding: utf-8 -*-
{
    'name': 'EDC Account',
    'depends': [
        'base',
        'account',
        'edc_product',

    ],
    "description": """
   """,
    'author': "Ejaftech",

    'data': [
        'views/res_partner.xml',
        'views/account_move.xml',
        'views/account_move_line.xml',
        'views/invoices_report.xml',
        'views/custom_layout.xml',
        'views/account_invoice_template.xml',
        'views/res_partner_bank.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
}
