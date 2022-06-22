from odoo import fields, models, api


class AvanceIndicadorProducto(models.Model):
    _name = 'planificacion.avance_indicador_producto'
    _description = 'Avance de indicador producto'

    indicadorProductoResultado = fields.Many2many(comodel_name='planificacion.indicador_producto_resultado', string='Indicador producto')
    trimestre1 = fields.Float(string='Trimestre I')
    trimestre2 = fields.Float(string='Trimestre II')
    trimestre3 = fields.Float(string='Trimestre III')
    trimestre4 = fields.Float(string='Trimestre IV')
    descripcionObstaculo = fields.Char(string='Descripción de los obstáculos ', required=False, size=100)
    gestiones = fields.Char(string='Gestión(es) que fueron realizadas para superar el obstáculo ', required=False, size=100)
    acciones = fields.Char(string='Acción(es) necesaria(s) y apoyos requeridos a futuro para solventar el obstáculo' +
                                  ', en caso aun NO haya sido solventado (Indique el área a quien se solicita el apoyo especifico)',
                           required=False, size=100)
    # Detalle de riesgos
    riesgos = fields.One2many(comodel_name='planificacion.avance_indicador_producto_riesgos',
                              inverse_name='avanceIndicador_ids', string='Riesgos', required=False)
    # Modelo padre
    productoResultado_ids = fields.Many2one(comodel_name='planificacion.producto_resultado_efecto_impacto',
                                            string='Producto resultado', required=True, ondelete='cascade')


class AvanceIndicadorProductoRiesgos(models.Model):
    _name = 'planificacion.avance_indicador_producto_riesgos'
    _description = 'Riesgos de avance de indicador producto'

    avanceIndicador_ids = fields.Many2one(comodel_name='planificacion.avance_indicador_producto',
                                            string='Avance indicador producto', required=True, ondelete='cascade')
