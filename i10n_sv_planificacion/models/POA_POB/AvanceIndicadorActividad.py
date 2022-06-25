from odoo import fields, models, api


class AvanceIndicadorActividad(models.Model):
    _name = 'planificacion.avance_indicador_actividad'
    _description = 'Avance de indicador actividad'

    indicadorActividad = fields.Many2one(comodel_name='planificacion.indicador_actividad_producto_resultado', string='Indicador actividad')
    tipoValor = fields.Selection(related='indicadorActividad.tipoValor', string='Unidad de medida')
    indicadorTrimestre1 = fields.Float(related='indicadorActividad.trimestre1', string='Trimestre I')
    indicadorTrimestre2 = fields.Float(related='indicadorActividad.trimestre2', string='Trimestre II')
    indicadorTrimestre3 = fields.Float(related='indicadorActividad.trimestre3', string='Trimestre III')
    indicadorTrimestre4 = fields.Float(related='indicadorActividad.trimestre4', string='Trimestre IV')

    trimestre1 = fields.Float(string='Trimestre I')
    trimestre2 = fields.Float(string='Trimestre II')
    trimestre3 = fields.Float(string='Trimestre III')
    trimestre4 = fields.Float(string='Trimestre IV')

    # Modelo padre
    actividad_resultado_ids = fields.Many2one(comodel_name='planificacion.actividad_producto_resultado',
                                            string='Producto resultado', required=True, ondelete='cascade')


