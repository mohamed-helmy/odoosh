# -*- coding: utf-8 -*-
{
    'name': "Reports Sequences",
    'summary': """
       This module to customize reports PDF sequences""",
    'description': """
                This module to customize reports PDF sequences
    """,
    'author': "Ejaf Technology",
    'website': "http://www.ejaftech.com/",
    'version': '0.1',
    'depends': ['sale_management','purchase','stock'],
    'data': [
        'views/report_saleorder_document.xml',
        'views/report_delivery_document.xml',
        'views/report_picking.xml',
        'views/report_purchaseorder_document.xml',
        'views/report_purchasequotation_document.xml',
    ],
    'demo': [
    ],

}
