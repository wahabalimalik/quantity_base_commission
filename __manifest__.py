# -*- coding: utf-8 -*-
{
    'name': "Quantity Base Commission",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','sale','purchase'],
    'data': [
        'data/auto_vendor_bill.xml',
        'views/views.xml',
    ],
}