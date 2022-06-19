from odoo import fields, models, api


class PeriodoArchivos(models.Model):
    _name = 'planificacion.periodo_archivos'
    # _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _description = 'Archivos PEI'

    archivo = fields.Binary(string="Archivo", required=False)
    archivoNombre = fields.Char(string='Archivo nombre', required=False)
    periodo_ids = fields.Many2one(comodel_name='planificacion.periodo', string='Período')

    @api.model
    def create(self, vals):
        res = super(PeriodoArchivos, self).create(vals)
        if 'archivo' in vals:
            message = "Carga de archivo %s" % vals['archivoNombre']
            res.periodo_ids.message_post(body=message)
        return res
