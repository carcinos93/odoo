from odoo import fields, models, api


class ObjetivoEstrategicoDetalle(models.Model):
    _name = 'planificacion.objetivo_estrategico_detalle'
    _description = 'Detalle de objetivos estategicos en POA'

    def _periodo_default(self):
        periodo = self._context.get('periodo')
        return periodo

    objetivo = fields.Many2one(comodel_name='planificacion.objetivo_estrategico', string='Objetivo estratégico')
    objetivoDescripcion = fields.Text(related='objetivo.descripcion', string='Objetivo estratégico descripción')
    indicadores = fields.One2many(comodel_name='planificacion.indicador_objetivo_estrategico_detalle',inverse_name='objetivoEstrategicoDetalle_ids',string=' Indicador efecto impacto', copy=True)
    metas = fields.One2many(comodel_name='planificacion.meta_objetivo_estrategico_detalle',inverse_name='objetivoEstrategicoDetalle_ids',string=' Meta', copy=True)
    resultados = fields.One2many(comodel_name='planificacion.resultado_efecto_impacto',inverse_name='objetivoEstrategicoDetalle_ids',string=' Resultados específicos', copy=True)
    periodo = fields.Char(string='Periodo', size=4, default=_periodo_default)
    indicadoresEfectoImpacto = fields.One2many(comodel_name='planificacion.indicador_efecto_impacto',inverse_name='objetivoEstrategico_ids',string=' Indicador que mide el efecto/impacto ', required=False, copy=True)
    vinculaciones = fields.One2many(comodel_name='planificacion.vinculacion_detalle', inverse_name='objetivoEstrategico_ids', string=' Vinculación', required=False, copy=True)
    grupoMetas = fields.One2many(comodel_name='planificacion.grupo_meta', inverse_name='objetivoEstrategico_ids', string='Grupo meta', required=False, copy=True)
    peso = fields.Float(string='Peso', required=False, default=0.00)
    # Modelo padre
    eje_ids = fields.Many2one(comodel_name='planificacion.eje_estrategico_detalle', string='Eje estratégico', ondelete='cascade')

    def name_get(self):
        result = []
        for data in self:
            name = '%s %s' % ( data.objetivo.codigo, data.objetivo.descripcion, )
            result.append((data.id, name,))
        return result
