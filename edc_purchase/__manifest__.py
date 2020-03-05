# -*- coding: utf-8 -*-
{
    'name': 'EDC Purchase',
    'depends': [
        'base',
        'purchase',
        'purchase_stock',
        'edc_account',

    ],
    "description": """
   """,
    'author': "Ejaftech",

    'data': [
        'views/paper_format.xml',
        'views/purchase_order.xml',
        'views/res_company.xml',
        'views/res_config.xml',
        'views/purchase_order_report.xml',
        'views/custom_layout.xml',
        'views/purchase_order_template.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
}
