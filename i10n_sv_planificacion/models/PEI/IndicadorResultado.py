from odoo import fields, models, api
import re

class IndicadorResultado(models.Model):
    _name = 'planificacion.indicador_resultado'
    # _inherit = 'base.auditoria'

    def _codigo_generador(self):
        prefijo = "R.I"
        items = self._context.get('items')
        parent_codigo = self._context.get('parent_codigo')
        parent_codigo = re.sub("^([A-Za-z\\.]*)", "", parent_codigo)  # Se elimina el prefijo
        filtrados = list(filter( lambda x: x[0] != 2, items))
        codigo = (prefijo + "." if prefijo else "") + parent_codigo + "." + str(len(filtrados) + 1)
        return codigo

    codigo = fields.Char(string='Código de Indicador de resultado', readonly=False, default=_codigo_generador) # default=_default_codigo
    nombre = fields.Char(string='Nombre del indicador', required=False)
    descripcion = fields.Text(string="Definición detallada", required=False)
    unidadMedida = fields.Selection(string='Unidad de medida', selection=[('1', 'Porcentaje'), ('2', 'Cantidad')], required=False)
    meta = fields.Float(string='Meta', required=False)
    # Modelo padre
    resultado_ids = fields.Many2one(comodel_name='planificacion.resultado', string='Resultado')

    def name_get(self):
        result = []
        for data in self:
            name = '%s %s' % (data.codigo, data.descripcion)
            result.append((data.id, name,))
        return result
