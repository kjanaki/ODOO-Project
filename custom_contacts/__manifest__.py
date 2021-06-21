# -*- coding: utf-8 -*-

{
    'name': "Custom Contacts",
    'summary': """Custom contacts""",
    'category': 'Base',
    "license": "AGPL-3",
    'version': '13',
    'images': [],
    'depends': ['base','mail','account'],
    'data': [
            'views/commodity_type.xml',
            'data/commodity_data.xml',
            'data/email_templates.xml',
            'views/res_partner_views.xml',
            'security/ir.model.access.csv',],
    'installable': True,
}
