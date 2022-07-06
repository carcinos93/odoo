from odoo import fields, models, api


class AvanceIndicadorProducto(models.Model):
    _name = 'planificacion.avance_indicador_producto'
    _description = 'Avance de indicador producto'

    def _compute_habilitarTrimestre(self):
        # Esta variable se declara en vista monitore.xml en Evaluación del poa
        permitirEditar = self._context.get('permitir_editar', False)
        self.update({
            'habilitarTrimestre1': self._compute_configuracion('trimestre1') and permitirEditar,
            'habilitarTrimestre2': self._compute_configuracion('trimestre2') and permitirEditar,
            'habilitarTrimestre3': self._compute_configuracion('trimestre3') and permitirEditar,
            'habilitarTrimestre4': self._compute_configuracion('trimestre4') and permitirEditar
        })

    def _compute_configuracion(self, trimestre):
        configuracion = self.env['planificacion.configuracion'].search([])
        for c in configuracion:
            return getattr(c, trimestre)
        return False

    indicadorResultado = fields.Many2one(comodel_name='planificacion.indicador_producto_resultado',
                                         string='Indicador producto',  ondelete='cascade')
    tipoValor = fields.Selection(related='indicadorResultado.tipoValor', string='Unidad de medida')
    indicadorTrimestre1 = fields.Float(related='indicadorResultado.trimestre1', string='Trimestre I')
    indicadorTrimestre2 = fields.Float(related='indicadorResultado.trimestre2', string='Trimestre II')
    indicadorTrimestre3 = fields.Float(related='indicadorResultado.trimestre3', string='Trimestre III')
    indicadorTrimestre4 = fields.Float(related='indicadorResultado.trimestre4', string='Trimestre IV')

    trimestre1 = fields.Float(string='Trimestre I')
    trimestre2 = fields.Float(string='Trimestre II')
    trimestre3 = fields.Float(string='Trimestre III')
    trimestre4 = fields.Float(string='Trimestre IV')
    avance = fields.Char(string='Avance cualitativo', required=False, size=200)

    # Detalle de riesgos
    riesgos = fields.One2many(comodel_name='planificacion.avance_indicador_producto_riesgos',
                              inverse_name='avanceIndicador_ids', string='Riesgos', required=False)

    # Obstaculos
    obstaculos = fields.One2many(comodel_name='planificacion.avance_indicador_producto_obstaculos',
                                 inverse_name='avanceIndicador_ids', string='Obstáculos', required=False)

    # Configuracion

    habilitarTrimestre1 = fields.Boolean(string='', compute=_compute_habilitarTrimestre)
    habilitarTrimestre2 = fields.Boolean(string='', compute=_compute_habilitarTrimestre)
    habilitarTrimestre3 = fields.Boolean(string='', compute=_compute_habilitarTrimestre)
    habilitarTrimestre4 = fields.Boolean(string='', compute=_compute_habilitarTrimestre)

    # Modelo padre
    productoResultado_ids = fields.Many2one(comodel_name='planificacion.producto_resultado_efecto_impacto', string='Producto', required=True, ondelete='cascade')
    # Consulta al modelo padre de producto resultado
    resultadoEfectoImpacto_ids = fields.Many2one(related='productoResultado_ids.resultadoEfectoImpacto_ids', string='Resultado')
    objetivoEstrategicoDetalle_ids = fields.Many2one(related='resultadoEfectoImpacto_ids.objetivoEstrategicoDetalle_ids', string='Objetivo estrátegico')
    eje_ids = fields.Many2one(related='objetivoEstrategicoDetalle_ids.eje_ids', string='Eje')
    poa_ids = fields.Many2one(related='eje_ids.poa_ids', string='POA')


class AvanceIndicadorProductoRiesgos(models.Model):
    _name = 'planificacion.avance_indicador_producto_riesgos'
    _description = 'Riesgos de avance de indicador producto'

    riesgo = fields.Char(string='Riesgos en la implementación', required=False, size=100)
    avanceIndicador_ids = fields.Many2one(comodel_name='planificacion.avance_indicador_producto',
                                          string='Avance indicador producto', required=True, ondelete='cascade')


class AvanceIndicadorProductoObstaculos(models.Model):
    _name = 'planificacion.avance_indicador_producto_obstaculos'
    _description = 'Obstáculos de avance de indicador producto'

    descripcionObstaculo = fields.Char(string='Descripción de los obstáculos ', required=False)
    gestiones = fields.Char(string='Gestión(es) que fueron realizadas para superar el obstáculo ', required=False,
                            size=100)
    acciones = fields.Char(string='Acción(es) necesaria(s) y apoyos requeridos a futuro para solventar el obstáculo' +
                                  ', en caso aun NO haya sido solventado (Indique el área a quien se solicita el apoyo especifico)',
                           required=False, size=100)

    avanceIndicador_ids = fields.Many2one(comodel_name='planificacion.avance_indicador_producto',
                                          string='Avance indicador producto', required=True, ondelete='cascade')
