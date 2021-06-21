# -*- coding: utf-8 -*-
{
    'name': "Custom Contacts",
    'summary': """Custom contacts""",
    'category': 'Base',
    "license": "AGPL-3",
    'version': '13',
    'images': [],
    'depends': ['base','mail'],
    'data': [
            'security/ir.model.access.csv',
            'views/commodity_type.xml',
            'views/res_partner_views.xml',
            'data/commodity_data.xml',
            'data/email_templates.xml',
            ],
    'installable': True,
}
