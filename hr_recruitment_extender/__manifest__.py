# -*- coding: utf-8 -*-
{
    'name': "Modulo de Recursos Humanos",

    'summary': """
        Módulo de Recursos Humanos para CENPROMYPE""",

    'description': """
        Módulo Extension de Recursos Humanos...
    """,

    'author': "OQM",
    'website': "http://www.oqm.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [ 'base'
       
    ],

    # always loaded
    'data': [
        'views/hr_reqemp_view.xml'
    ],

}
