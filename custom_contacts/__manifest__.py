# -*- coding: utf-8 -*-

{
    'name': "Custom Contacts",
    'summary': """Custom contacts""",
    'author': "Raghu",
    'category': 'Base',
    "license": "AGPL-3",
    'version': '13',
    'images': [],
    'depends': ['base','mail','account'],
    'data': [
            'views/commodity_type.xml',
            'data/commodity_data.xml',
            'views/res_partner_views.xml',
            'security/ir.model.access.csv',],
    'installable': True,
}
