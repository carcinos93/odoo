from odoo import fields, models, api


class MedioVerificacion(models.Model):
    _name = 'planificacion.medio_verificacion'
    # _inherit = 'base.auditoria'

    medioVerificacion = fields.Char(string="Medio de verificación ", required=False)
    descripcionInstrumento = fields.Text(string="Descripción del instrumento", required=False)
    #instrumentoRecoleccion = fields.Boolean(string='¿Se cuenta con el instrumento de recolección de información?', required=False)
    instrumentoRecoleccion = fields.Selection(string='¿Se cuenta con el instrumento de recolección de información?', selection=[('1', 'SI'), ('0', 'NO'), ], required=False, )

        
    indicador_ids = fields.Many2one(comodel_name='planificacion.ficha_indicador', string='Indicador',required=True)