# -*- coding: utf-8 -*-
{
    'name': 'Ejaf Add Vendors Purchase Agreement',
    'depends': [
        'base',
        'purchase_requisition',

    ],
    "description": """
   """,
    'author': "Ejaftech",

    'data': [
        'views/purchase_requisition.xml',
        'wizard/quotation_vendors.xml',
    ],
    'installable': True,
    'application': False,
}
