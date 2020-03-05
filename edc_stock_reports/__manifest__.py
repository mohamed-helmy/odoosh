# -*- coding: utf-8 -*-
{
    'name': 'EDC Stock Reports',
    'depends': [
        'stock',
        'edc_product',
        'odoo_report_xlsx',

    ],
    "description": """
   """,
    'author': "Ejaftech",

    'data': [
        'views/picking_view.xml',
        'report/report_warehouse_issue.xml',
        'report/transfers_report.xml',
        'report/reports.xml',
    ],
}
