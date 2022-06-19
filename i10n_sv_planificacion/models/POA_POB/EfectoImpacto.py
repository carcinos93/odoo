from odoo import fields, models, api


class EfectoImpacto(models.Model):
    _name = 'planificacion.efecto_impacto'
    # _inherit = 'base.auditoria'

    efectoImpacto = fields.Text(string='Efecto o impacto al que contribuye', required=False)
    # Modelo padre
    pobpob_ids = fields.Many2one(comodel_name='planificacion.poa_pob', string='POA/POB', required=True, ondelete='cascade')

    # resultado ?
    def name_get(self):
        result = []
        for data in self:
            name = '%s' % data.efectoImpacto
            result.append((data.id, name,))
        return result
