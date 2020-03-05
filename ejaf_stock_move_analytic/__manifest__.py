# -*- coding: utf-8 -*-
{
    'name': 'Stock Move Analytic',
    'depends': [
        'stock_account',
        "analytic",

    ],
    "description": """
    Adds an analytic account to journal item generated from stock move
   """,
    'author': "Ejaftech",

    'data': [
        'views/location_view.xml',
    ],
}
