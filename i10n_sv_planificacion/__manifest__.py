{
    'name': 'MÓDULO DE PLANIFICACIÓN',
    'version': '1.1',
    'summary': '',
    'description': '',
    'category': '',
    'author': 'Nelson Rodas',
    'website': 'https://oqmelsalvador.com',
    'license': '',
    'depends': ['base', 'mail', 'hr', 'portal', 'presupuesto'],
    # 'assets': {'web.report_assets_common': ['i10n_sv_planificacion/static/src/css/planificacion_theme.scss',]},
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/fichaIndicadores.xml',
        'views/pei_views.xml',
        'report/report_poa.xml',
        'report/report_poa_view.xml'
    ],
    'demo': [''],
    'installable': True,
    'auto_install': False
}
