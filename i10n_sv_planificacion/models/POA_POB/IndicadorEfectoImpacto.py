from odoo import fields, models, api


class IndicadorEfectoImpacto(models.Model):
    _name = 'planificacion.indicador_efecto_impacto'
    # _inherit = 'base.auditoria'

    indicadorEfecto = fields.Text(string='Indicadores que miden el efecto/impacto', required=False)
    # Modelo padre
    #pobpob_ids = fields.Many2one(comodel_name='planificacion.poa_pob', string='POA/POB', required=True, ondelete='cascade')
    objetivoEstrategico_ids = fields.Many2one(comodel_name='planificacion.objetivo_estrategico_detalle', string='Detalle de objetivos estategicos en POA', required=True,ondelete='cascade')