from odoo import fields, models, api


class ResultadoEfectoImpacto(models.Model):
    _name = 'planificacion.resultado_efecto_impacto'
    #_inherit = 'base.auditoria'

    def _periodo_default(self):
        periodo = self._context.get('periodo')
        return periodo

    resultado = fields.Many2one(comodel_name='planificacion.resultado',string='Resultado',required=True)
    resultadoDescripcion = fields.Text(string='Resultado',related='resultado.descripcion', readonly=True)
    responsable = fields.Many2one('hr.employee', 'Responsable')
    grupoMeta = fields.Text(string='Grupo meta', required=False)
    efectoImpacto = fields.Text(string='Efecto impacto', required=False)
    #efectoImpacto = fields.Many2one(comodel_name='planificacion.efecto_impacto', string='Efecto impacto', required=True)
    vinculacion = fields.Text(string='Vinculación entre el resultado y el efecto al que contribuye', required=False)
    indicadores = fields.One2many(comodel_name='planificacion.indicador_resultado_efecto_impacto', inverse_name='resultadoEfectoImpacto_ids', string='Indicador efecto impacto', required=False, copy=True)
    productos = fields.One2many(comodel_name='planificacion.producto_resultado_efecto_impacto', inverse_name='resultadoEfectoImpacto_ids', string=' Producto efecto impacto', required=False, copy=True)
    metas = fields.One2many(comodel_name='planificacion.meta_resultado_efecto_impacto', inverse_name='resultadoEfectoImpacto_ids', string=' Metas resultado', required=False, copy=True)
    periodo = fields.Char(string='Periodo', size=4, default=_periodo_default)
    # pobpob_ids = fields.Many2one(comodel_name='planificacion.poa_pob', string='POA/POB', required=True)
    # Modelo padre
    objetivoEstrategicoDetalle_ids = fields.Many2one(comodel_name='planificacion.objetivo_estrategico_detalle', string='Objetivo estratégico', ondelete='cascade')
