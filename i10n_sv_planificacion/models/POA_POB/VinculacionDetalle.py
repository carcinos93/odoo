from odoo import fields, models, api


class VinculacionDetalle(models.Model):
    _name = 'planificacion.vinculacion_detalle'
    _description = 'Vinculación entre el objetivo estratégico de Cenpromype y el efecto'

    vinculacion = fields.Text(string="Vinculación entre el objetivo estratégico de Cenpromype y el efecto", required=False)
    # Modelo padre
    #pobpob_ids = fields.Many2one(comodel_name='planificacion.poa_pob', string='POA/POB', required=True, ondelete='cascade')
    objetivoEstrategico_ids = fields.Many2one(comodel_name='planificacion.objetivo_estrategico_detalle', string='Detalle de objetivos estategicos en POA', required=True,ondelete='cascade')
