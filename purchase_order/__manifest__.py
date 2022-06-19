# -*- coding: utf-8 -*-
{
    'name': "Compras Centromype",

    'summary': """
        Gestion Compras""",

    'description': """
        Registros y Gestiones de compras de conamype
    """,

    'author': "alexars",
    'website': " ",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'purchase',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['purchase', 'hr', 'base', 'i10n_sv_planificacion', 'presupuesto', 'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/purchase_type_views.xml',
        'views/purchase_order_view.xml',
        'report/report_requisicion.xml',
        'report/report_requisicion_view.xml',
        'data/data_group_view.xml',
    ],


    'images' : ['static/img/icon.png'],
}