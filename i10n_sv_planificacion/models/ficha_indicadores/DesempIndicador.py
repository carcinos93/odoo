from odoo import fields, models, api


class DesempIndicador(models.Model):
    _name = 'planificacion.desemp_indicador'
    _description = 'Valor de desempeño del indicador'
    # _inherit = 'base.auditoria'
    medioVerificacion = fields.Char(string="Medio de verificación ", required=False) # todo remover
    metaProgramada = fields.Char(string="Meta programada por trimestre ", required=False)
    valorActual = fields.Char(string="Valor actual", required=False)
    comentarios = fields.Text(string="Comentarios", required=False)
    trimestre = fields.Selection(
        string='Trimestre',
        selection=[('1', 'I Trimestre'),
                   ('2', 'II Trimestre'),
                   ('3', 'III Trimestre'),
                   ('4', 'IV Trimestre')
                   ],
        required=False)
    indicador_ids = fields.Many2one(comodel_name='planificacion.ficha_indicador', string='Indicador',required=True, ondelete='cascade')


