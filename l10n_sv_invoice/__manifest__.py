# -*- coding: utf-8 -*-
{
    'name': "l10n_sv_invoice",

    'summary': """
        Módulo CRM para la gestión de facturas""",

    'description': """
        Módulo CRM para la gestión de facturas...
    """,

    'author': "OQM",
    'website': "http://www.oqm.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'views/l10n_sv_invoice_view.xml',

    ],

}
