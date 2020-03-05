# -*- coding: utf-8 -*-
{
    'name': 'Ejaf Asset Management',
    'version': '0.1',
    'category': 'custom',
    'summary': 'Asset Management',
    'license':'AGPL-3',
    'description': """
     Asset management is a simple system to manage assets owned by an organization.
""",
    'author': "Ejaftech",
    'depends': ['base','mail','account_asset','stock'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/asset_sequence.xml',
        'views/asset_view.xml',
        'views/asset_move_view.xml',
        'views/account_asset.xml',

             ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

