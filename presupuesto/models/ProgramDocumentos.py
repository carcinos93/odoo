from odoo import fields, models, api


class ProgramDocumentos(models.Model):
    _name = 'budget.program_documentos'
    _description = 'Documentos de proyectos'

    archivo = fields.Binary(string="Archivo", required=False)
    archivoNombre = fields.Char(string='Archivo nombre', required=False)
    titulo = fields.Char(string='Título', required=False)
    # Modelo padre
    program_ids = fields.Many2one(comodel_name='budget.program', string='Proyecto',required=True, ondelete='cascade')
