from odoo import fields, models, api


class IndicadorObjetivoEstrategicoDetalle(models.Model):
    _name = 'planificacion.indicador_objetivo_estrategico_detalle'
    # _inherit = 'base.auditoria'

    indicadorObjetivo = fields.Many2one(comodel_name='planificacion.indicador_objetivo', string='Indicador objetivo', required=False)
    indicadorDescripcion = fields.Text(related="indicadorObjetivo.descripcion", string="Indicador objetivo descripción")
    indicadorNombre = fields.Char(related="indicadorObjetivo.nombre", string="Indicador nombre")

    meta = fields.Float(related="indicadorObjetivo.meta", string='Meta', required=False)
    metaAnual = fields.Float(string='Meta anual', required=False)
    # fechaMedicion = fields.Date(string='Fecha prevista medición', required=False)
    fechaPrevista = fields.Selection( string='Fecha prevista de consecución',selection=[('1', 'I Trimestre'),('2', 'II Trimestre'),('3', 'III Trimestre'),('4', 'IV Trimestre')], required=False)
    tipoValor = fields.Selection(string='Unidad de medida', selection=[('1', 'Porcentaje'), ('2', 'Cantidad')], required=False)

    # Modelo padre
    objetivoEstrategicoDetalle_ids = fields.Many2one(comodel_name='planificacion.objetivo_estrategico_detalle', string='Indicador objetivo', required=True, ondelete='cascade')