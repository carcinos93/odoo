from odoo import fields, models, api


class CorrespondenciaProyecto(models.Model):
    _name = 'planificacion.correspondencia_proyecto'
    # _inherit = 'base.auditoria'

    @api.model
    def _compute_default_currencyid(self):
        company = self.env['res.company'].search([])
        for c in company:
            return c.currency_id

    currency_id = fields.Many2one('res.currency','Currency',required=False, readonly=True, default=_compute_default_currencyid )
    proyecto = fields.Selection(string='Correspondencia',selection=[('1', 'Sin financiamiento')],required=True )
    monto = fields.Float(string='Monto', required=False)
    indicador_ids = fields.Many2one(comodel_name='planificacion.ficha_indicador', string='Indicador',required=True)
