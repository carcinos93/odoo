# -*- coding: utf-8 -*-
{
    'name': "odoo_view_advanced",

    'summary': """
        Conceptos avanzados de vistas""",

    'description': """
        Curso de conceptos avanzados de vistas
    """,

    'author': "Darío Rodríguez García",
    'website': "https://www.udemy.com/user/dario-rodriguez-garcia/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    #         'odoo_view_advanced/static/src/js/action_call.js'
    # any module necessary for this one to work correctly
    'depends': ['base'],
    'assets': {
        'web.assets_backend': [
                'odoo_view_advanced/static/src/js/action_call.js'
            ],
        "web.assets_qweb": [
            'odoo_view_advanced/static/src/xml/button.xml'
        ]
    },
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'report/custom_item.xml',
        'report/custom_item_view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ]

}
