from odoo import fields, models, api


class EjeEstrategicoDetalle(models.Model):
    _name = 'planificacion.eje_estrategico_detalle'
    _description = 'Detalle de ejes estategicos en POA'

    def _periodo_default(self):
        periodo = self._context.get('periodo')
        return periodo

    eje = fields.Many2one(comodel_name='planificacion.eje_estrategico', string='Eje estratégico')
    objetivos = fields.One2many(comodel_name='planificacion.objetivo_estrategico_detalle', inverse_name='eje_ids',string=' Objetivos estratégicos', copy=True)
    periodo = fields.Char(string='Periodo', size=4, default=_periodo_default)
    # Modelo padre
    poa_ids = fields.Many2one(comodel_name='planificacion.poa_pob', string='POA',required=True, ondelete='cascade')