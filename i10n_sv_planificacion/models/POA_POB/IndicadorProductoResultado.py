from odoo import fields, models, api


class IndicadorProductoResultado(models.Model):
    _name = 'planificacion.indicador_producto_resultado'
    # _inherit = 'base.auditoria'

    def _codigo_generador(self):
        if self._context.get('items') is None or self._context.get('parent_codigo') is None:
            return "0"
        items = self._context.get('items')
        parent_codigo = self._context.get('parent_codigo')
        filtrados = list(filter( lambda x: x[0] != 2, items))
        codigo = parent_codigo + "." + str(len(filtrados) + 1)
        return codigo

    # TODO quitar los campos de indicador producto
    indicadorProducto = fields.Many2one(comodel_name='planificacion.indicador_producto', string='Indicador producto', required=False)
    nombreIndicadorProducto = fields.Text(related="indicadorProducto.descripcion")

    codigoIndicador = fields.Char(string='Código indicador', required=False, default=_codigo_generador)
    descripcionIndicador = fields.Text(string="Definición detallada", required=False)
    nombreIndicador = fields.Char(string="Nombre indicador", required=False)
    meta = fields.Float(string='Meta', required=False)
    tipoValor = fields.Selection(string='Unidad de medida', selection=[('1', 'Porcentaje'), ('2', 'Cantidad')], required=False)
    fechaMedicion = fields.Date(string='Fecha prevista de consecución', required=False)
    fechaPrevista = fields.Selection( string='Fecha prevista de consecución',selection=[('1', 'I Trimestre'),('2', 'II Trimestre'),('3', 'III Trimestre'),('4', 'IV Trimestre')], required=False)
    trimestre1 = fields.Float(string='Trimestre I')
    trimestre2 = fields.Float(string='Trimestre II')
    trimestre3 = fields.Float(string='Trimestre III')
    trimestre4 = fields.Float(string='Trimestre IV')
    productoResultado_ids = fields.Many2one(comodel_name='planificacion.producto_resultado_efecto_impacto', string='Producto resultado', required=True, ondelete='cascade')