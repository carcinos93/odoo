from odoo import fields, models, api


class MetaObjetivoEstrategicoDetalle(models.Model):
    _name = 'planificacion.meta_objetivo_estrategico_detalle'

    valor = fields.Float(string='Meta', required=False)
    meta = fields.Many2one(comodel_name='planificacion.meta', string='Meta', required=True)
    tipoValor = fields.Selection(related="meta.tipoValor")


    # Modelo padre
    objetivoEstrategicoDetalle_ids = fields.Many2one(comodel_name='planificacion.objetivo_estrategico_detalle', string='Indicador objetivo', required=True, ondelete='cascade')