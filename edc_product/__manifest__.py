# -*- coding: utf-8 -*-
{
    'name': 'EDC Product',
    'depends': [
        'base',
        'product',
        'stock',

    ],
    "description": """ Add some new fields in the product view and add view for this object in stock configration
   """,
    'author': "Ejaftech",

    'data': [
        'security/groups.xml',
        'data/sequences.xml',
        'views/product_main_equipment.xml',
        'views/product_sub_equipment.xml',
        'views/product_manufacturer.xml',
        'views/product_model.xml',
        'views/product_equipment_model.xml',
        'views/product_template.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
}
