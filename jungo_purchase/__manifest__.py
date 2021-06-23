# -*- coding: utf-8 -*-

{
    'name': "Bulk PO",
    'summary': """To create bulk Purchase Order""",
    'category': 'Base',
    "license": "AGPL-3",
    'version': '14',
    'images': [],
    'depends': ['purchase','custom_contacts'],
    'data': [
            'security/ir.model.access.csv',
            'views/bulk_po.xml',
            # 'data/cron.xml'
            ],
    'installable': True,
}
