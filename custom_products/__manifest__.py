# -*- coding: utf-8 -*-

{
    'name': "Custom Products",
    'summary': """Custom Products""",
    'category': 'Base', 
    "license": "AGPL-3",
    'version': '13',
    'images': [],
    'depends': ['product','stock'],
    'data': [
            'security/ir.model.access.csv',
            'views/product_views.xml',
            'views/qr_code_view.xml',],
    'installable': True,
}
