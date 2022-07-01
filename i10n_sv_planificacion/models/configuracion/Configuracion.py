from odoo import fields, models, api


class Configuracion(models.Model):
    _name = 'planificacion.configuracion'
    _description = 'Parametros de configuración de planificación'

    trimestre1 = fields.Boolean(string='Habilitar trimestre I', required=False, default=True)
    trimestre2 = fields.Boolean(string='Habilitar trimestre II', required=False, default=False)
    trimestre3 = fields.Boolean(string='Habilitar trimestre III', required=False, default=False)
    trimestre4 = fields.Boolean(string='Habilitar trimestre IV', required=False, default=False)