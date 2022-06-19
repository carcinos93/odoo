from odoo import fields, models, api


class GrupoMeta(models.Model):
    _name = 'planificacion.grupo_meta'
    # _inherit = 'base.auditoria'

    grupoMeta = fields.Text(string="Grupo meta",required=False)
    # Modelo padre
    # pobpob_ids = fields.Many2one(comodel_name='planificacion.poa_pob',string='POA/POB',required=True, ondelete='cascade')
    objetivoEstrategico_ids = fields.Many2one(comodel_name='planificacion.objetivo_estrategico_detalle', string='Detalle de objetivos estategicos en POA', required=True,ondelete='cascade')
