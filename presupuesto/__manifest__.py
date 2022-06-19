# -*- coding: utf-8 -*-
{
    'name': "budget",

    'summary': """
        Presupuesto Institucional""",

    'description': """
        Presupuesto Institucional
    """,

    'author': "Ricardo Rendon",
    'website': "https://www.cenpromype.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'report/report_program.xml',
        'report/report_program_view.xml'
    ],
    'assets' : {
        'web.assets_backend': [
            'presupuesto/static/src/scss/presupuesto_theme.scss'
        ]
    },
    'demo': [
        'demo/demo.xml',
    ],
}
