# -*- coding: utf-8 -*-
{
    'name': "Modulo de Control Activo Fijo",

    'summary': """
        Brinda las opciones para el Control del Activo Fijo de las Empresas""",

    'description': """
        Permite controlar, el registro de activos, la depreciaciones de estos y las asignaciones...
    """,

    'author': "TEACH TECNOLOGY",
    'website': "http://www.ttecnology.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Account Charts',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['account'],

    # always loaded
    'data': [
        'views/asset_process_views.xml',
        'views/asset_parameters_views.xml',
        'view_main.xml',
    ],

}
