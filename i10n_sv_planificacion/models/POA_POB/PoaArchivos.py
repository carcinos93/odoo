from odoo import fields, models, api


class PoaArchivos(models.Model):
    _name = 'planificacion.poa_pob_archivos'
    _description = 'Archivos de poa'

    archivo = fields.Binary(string="Archivo", required=False)
    archivoNombre = fields.Char(string='Archivo nombre', required=False)
    # Modelo padre
    poa_ids = fields.Many2one(comodel_name='planificacion.poa_pob', string='POA',required=True, ondelete='cascade')

    @api.model
    def create(self, vals):
        res = super(PoaArchivos, self).create(vals)
        if 'archivo' in vals:
            message = "Carga de archivo %s" % vals['archivoNombre']
            res.poa_ids.message_post(body=message)
        return res
