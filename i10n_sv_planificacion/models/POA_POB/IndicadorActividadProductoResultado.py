from odoo import fields, models, api, exceptions


class IndicadorActividadProductoResultado(models.Model):
    _name = 'planificacion.indicador_actividad_producto_resultado'

    def _codigo_generador(self):
        if self._context.get('items') is None or self._context.get('parent_codigo') is None:
            return "0"
        items = self._context.get('items')
        parent_codigo = self._context.get('parent_codigo')
        filtrados = list(filter( lambda x: x[0] != 2, items))
        codigo = parent_codigo + "." + str(len(filtrados) + 1)
        return codigo

    codigo = fields.Char(string='Código del indicador', default=_codigo_generador )
    nombre = fields.Char(string="Nombre del indicador", required=False)
    descripcion = fields.Text(string="Definición detallada", required=False)
    tipoValor = fields.Selection(string='Unidad de medida', selection=[('1', 'Porcentaje'), ('2', 'Cantidad')], required=False)
    trimestre1 = fields.Float(string='Trimestre I')
    trimestre2 = fields.Float(string='Trimestre II')
    trimestre3 = fields.Float(string='Trimestre III')
    trimestre4 = fields.Float(string='Trimestre IV')
    fechaPrevista = fields.Selection( string='Fecha prevista de consecución',selection=[('1', 'I Trimestre'),('2', 'II Trimestre'),('3', 'III Trimestre'),('4', 'IV Trimestre')], required=False)

    # Modelo padre
    actividad_resultado_ids = fields.Many2one(comodel_name='planificacion.actividad_producto_resultado', string='Actividad producto resultado', required=True, ondelete='cascade')
